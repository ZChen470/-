# -*- coding: utf-8 -*-

from fastapi import FastAPI, UploadFile, File, status, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import pandas as pd
from typing import List
import io
import base64
import zipfile
import tempfile
from contextlib import asynccontextmanager
import gc
from pathlib import Path
from search_tool import hips_fits_url,save_fits,parse_survey,query_information,hips_fits_url_catalog
from astropy.table import Table
# from app.models import PredictOut
from models import PredictOut, disciptions, represents, Coordinate
from utils import genID
from galaxy_classify import galaxy_classify_zoobot

from zoobot.pytorch.training.finetune import FinetuneableZoobotClassifier

# save img to local
model = None
model_path = Path(__file__).resolve().parents[1] / 'model/zoobot/finetune_model/FinetuneableZoobotClassifier.ckpt'

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    global model
    model = FinetuneableZoobotClassifier.load_from_checkpoint(model_path, map_location='cpu')
    print('load model successfully')
    yield
    # Clean up the ML models and release the resources
    del model
    gc.collect()
    print('shut down')

app = FastAPI(lifespan=lifespan)

# This is necessary because QUploader uses an AJAX request
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def initial_path()->List[Path]:
    # create the file to save img
    img_file_name = 'img' + genID.get_id()
    img_path = Path(__file__).resolve().parents[1] / img_file_name
    img_path.mkdir(parents=True, exist_ok=True)
    frontend = Path(__file__).resolve().parents[1] / 'frontend'
    return [img_path, frontend]

def rename_img(img_path: Path, new_name: List[str], origin_name: List[str], suffix_list: List[str]):
    """
    Rename the image files with new name and suffix
    :param img_path: Path to the image folder
    :param new_name: List of new names for the image files
    :param origin_name: List of origin names for the image files
    :param suffix_list: List of suffixes for the image files
    """
    # 生成新的文件名列表
    new_filenames = [f"{name}_{suffix}" for name, suffix in zip(new_name, suffix_list)]
    new_filenames = [ name+Path(ogn).suffix for name, ogn in zip(new_filenames, origin_name)]
    origin_new_zip = zip(origin_name, new_filenames)
    
    # 遍历原始文件列表并重命名文件
    for origin, new in origin_new_zip:
        origin_file_path = img_path / origin
        new_file_path = img_path / new
        if origin_file_path.exists():
            origin_file_path.rename(new_file_path)


def clear_file(path:Path):
    if path.is_file():
        path.unlink()
    elif path.is_dir():
        for item in path.iterdir():
            clear_file(item)
        path.rmdir()

# test API
@app.get("/")
async def hello():
    item = {'message': 'Hello'}
    return JSONResponse(status_code=status.HTTP_200_OK, content=item)

# 接收坐标数据
@app.post('/coord')
async def get_coordinate(*, coordinate:Coordinate, path:List[Path] = Depends(initial_path), background_tasks: BackgroundTasks):
    # get coords & view info
    ra = coordinate.ra
    dec = coordinate.dec
    fov = coordinate.fov
    size = coordinate.size
    survey_id = coordinate.surveyid

    # image path
    img_path, _ = path[0], path[1]
    
    # get survey info:
    survey = parse_survey(survey_id)
    
    # get image:
    url,filename = hips_fits_url(ra,dec,fov,size,survey)
    filename = filename+'.png'
    print(url,filename)
    status_code = await save_fits(url,filename,img_path)
    if status_code != 200:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={'message': 'download image failed'})
    
    info_table = await query_information(ra,dec)
    id = genID.get_id()
    predict_res,predict_probability = galaxy_classify_zoobot(str(img_path), [filename], [id], model)
    
    # create background task
    background_tasks.add_task(clear_file, path=img_path)
    print("创建的文件是：", img_path)

    # return response:
    response_content = {}
    response_content['info_table'] = info_table
    confidence = ["{:.2%}".format(res) for res in predict_probability]
    desc = [disciptions[res] for res in predict_res if res in disciptions]
    response_content['category'] = predict_res[0]
    response_content['confidence'] = confidence[0]
    response_content['description'] = desc[0]
    return JSONResponse(content=response_content, status_code=status.HTTP_200_OK)

# 接收坐标csv文件
@app.post('/coord_csv')
async def get_coor_catelog(*, file:UploadFile = File(...), path:List[Path] = Depends(initial_path), background_tasks: BackgroundTasks):
    img_path, _ = path[0], path[1]
    file_content = await file.read()
    # BytesIO在这里充当了一个桥梁，连接了二进制数据与需要文件对象的函数，使得可以直接从内存中的字节流读取CSV数据。
    df = pd.read_csv(io.BytesIO(file_content))
    url_list,filename_list = hips_fits_url_catalog(df[:-1])
    filename_list = [f'{filename}.png' for filename in filename_list]
    id_list = []
    for i in range(len(url_list)):
        id_list.append(genID.get_id())
        # get image
        status_code = await save_fits(url_list[i],filename_list[i],img_path)
    
    predict_res,predict_probability = galaxy_classify_zoobot(str(img_path), filename_list, id_list, model)
    # rename all files in img_path
    rename_img(img_path, predict_res, filename_list, id_list)

    background_tasks.add_task(clear_file, path=img_path)

    with tempfile.NamedTemporaryFile(delete=False) as temp_zip:
        with zipfile.ZipFile(temp_zip, "w", zipfile.ZIP_DEFLATED, False) as zip_file:
            for img_file in img_path.iterdir():
                if img_file.is_file():
                    zip_file.write(img_file, img_file.name)

    # create background task
    background_tasks.add_task(clear_file, path=Path(temp_zip.name))

    return FileResponse(temp_zip.name, filename='images.zip', media_type="application/zip")

# 接收前端传入的图片
@app.post('/predict', response_model=PredictOut)
async def get_file(*, files:List[UploadFile] = File(...), path:List[Path] = Depends(initial_path), background_tasks: BackgroundTasks):
    
    img_path,frontend = path[0], path[1]
    filenames:List[str] = []
    id_list:List[str] = []

    if files is None:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'message': 'No files uploaded'})
    else:
        for file in files:
            file_content = await file.read()
            filename:str = file.filename # error for file is None
            filenames.append(filename)
            filepath = img_path / filename
            with open(filepath, 'wb') as f:
                f.write(file_content)
            id_list.append(genID.get_id())

    predict_res,predict_probability = galaxy_classify_zoobot(str(img_path), filenames, id_list, model)
    
    # create background task
    background_tasks.add_task(clear_file, path=img_path)
    
    if len(predict_res) == 1:
        confidence = ["{:.2%}".format(res) for res in predict_probability]
        desc = [disciptions[res].encode("utf-8") for res in predict_res if res in disciptions]
        represent = represents[predict_res[0]]
        # get galaxy image with the same category
        img_path = frontend / f"{predict_res[0]}.jpg"
        with open(img_path, 'rb') as imfile:
            image = base64.b64encode(imfile.read()).decode('utf-8')


        return PredictOut(category=predict_res[0],
                        confidence=confidence[0],
                        description=desc[0],
                        represent=represent,
                        image=image
                )
    elif len(predict_res) > 1:
        # rename all files in img_path
        rename_img(img_path, predict_res, filenames, id_list)


        with tempfile.NamedTemporaryFile(delete=False) as temp_zip:
            with zipfile.ZipFile(temp_zip, "w", zipfile.ZIP_DEFLATED, False) as zip_file:
                for img_file in img_path.iterdir():
                    if img_file.is_file():
                        zip_file.write(img_file, img_file.name)

        # create background task
        background_tasks.add_task(clear_file, path=Path(temp_zip.name))

        return FileResponse(temp_zip.name, filename='images.zip', media_type="application/zip")


if __name__ == "__main__":
   import uvicorn
   uvicorn.run("main:app", host="127.0.0.1", port=8080)