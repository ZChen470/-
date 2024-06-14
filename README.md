# 基于深度学习的星系分类Web应用

功能描述：

- 在单图像部分，上传的单张星系图像进行分类，返回类别、置信度、该类别的描述以及已知的同类别星系图片和信息
- 在多图像部分，上传的多张星系图像进行分类，并将图片文件名修改为类别以此对图像进行类别标注
- 在单坐标部分，通过Aladin交互界面通过输入坐标、拖动和缩放选择星系，点击获取类别获取相应的信息
- 在多坐标部分，上传保存了星系坐标的csv文件，返回包含类别标注的星系图像

# frontend
```
npm create vue@latest  
npm install quasar @quasar/extras
```

### cmd quasar_ui_test下执行

`npm run dev`

# backend

`cd ./venv/Scripts  `

### 激活虚拟环境
```
activate  
cd ..  
cd ./astronomy/app  
```
### 安装依赖

`pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt`

### 使用python3.9的python.exe运行主程序

`python39 main.py`



## test_data中是用于测试的数据

### 运行MongoDB中的.py文件将数据保存到MongoDB Astronomy数据库GalaxyCategory集合中



更多信息请参考 [GitHub - RuiNov1st/galaxy_classification: Galaxy Classification demo for UCAS AstroInformatics 2024](https://github.com/RuiNov1st/galaxy_classification)



### 修改Docker Image

```bash
# venv下执行
docker . -t galaxy_back  
# 构建好镜像后打开镜像
docker run -it galaxy_back /bin/bash
# 参考链接中的方法，修改/usr/.../Lib/site-packages下的zoobot和galaxy_datasets 绝对路径：/app/app/model/zoobot/convnext_nano/pytorch_model.bin
exit
# 提交修改
# 先查看刚刚run的容器的ID或name
docker ps -a
docker commit <ID/name> galaxy_back -c 'CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]'
# 完成修改后在宿主机运行
docker run galaxy_back -d
```


