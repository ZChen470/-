# 基于深度学习的星系分类Web应用

功能描述：
- 在单图像部分，上传的单张星系图像进行分类，返回类别、置信度、该类别的描述以及已知的同类别星系图片和信息
- 在多图像部分，上传的多张星系图像进行分类，并将图片文件名修改为类别以此对图像进行类别标注
- 在单坐标部分，通过Aladin交互界面通过输入坐标、拖动和缩放选择星系，点击获取类别获取相应的信息
- 在多坐标部分，上传保存了星系坐标的csv文件，返回包含类别标注的星系图像

# frontend

npm create vue@latest  
npm install quasar @quasar/extras 

### cmd quasar_ui_test下执行

npm run dev

# backend

cd ./venv/Scripts  

### 激活虚拟环境

activate  
cd ..  
cd ./astronomy/app  

### 安装依赖

pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

### 使用python3.9的python.exe运行主程序

python39 main.py



## test_data中是用于测试的数据

### 运行MongoDB中的.py文件将数据保存到MongoDB Astronomy数据库GalaxyCategory集合中






