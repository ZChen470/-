import os
import numpy as np
import pandas as pd
from pathlib import Path
from zoobot.pytorch.predictions import predict_on_catalog
from typing import List, Tuple
from model.models import dataset_labels

def galaxy_classify_zoobot(image_path:str, filename:List[str], id_list:List[str], model) -> Tuple[List[str], List[float]]:
    """
    classification process
    - params:
    image_path(str): galaxy image for classification. classify only one image at a time.
    model(pl.LightningModule): pretrained machine learning model for classification.
    - return:
    predict_res(str): most likely type for input image
    predict_probability(float): confidence associated with predict_res
    result_dict(dict): confidences of all types .
    """

    # check path:
    # if not os.path.exists(image_path):
    #     print(f"Image {image_path} not exists. Please check!")
    #     return None

    # make data catalog: just one image
    file_list: List[str] = []
    for fn in filename:
        file_list.append(os.path.join(image_path,fn))
    test_catalog = pd.DataFrame({'id_str':id_list,'file_loc':file_list})
    
    # predict:
    prediction = predict_on_catalog.predict(
      test_catalog,
      model,
      n_samples = 1,
      label_cols = dataset_labels,  # name the output columns
      save_loc = str(Path(__file__).resolve().parents[2] / 'outputs/finetuned_predictions.csv'),
      trainer_kwargs = {'accelerator': 'cpu'},
      datamodule_kwargs = {'num_workers': 2, 'batch_size': 32, 'greyscale': False},
    )
    predict_idx = np.argmax(prediction[:,:,0],axis=1)
    predict_res = [dataset_labels[i.item()] for i in predict_idx]
    predict_probability = [prediction[i,predict_idx[i],0].item() for i in range(predict_idx.shape[0])]
 

    return predict_res,predict_probability