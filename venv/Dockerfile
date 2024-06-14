FROM python:3.9

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY ./astronomy /app/app

ENV PYTHONPATH /app/app/app


# 先安装 Vim
RUN apt-get update && \
    apt-get install -y vim

# 设置PYTHONPATH，优先使用/app/zoobot
# ENV PYTHONPATH="/app/app/zoobot:$PYTHONPATH"

WORKDIR /app/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]