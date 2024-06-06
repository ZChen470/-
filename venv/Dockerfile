FROM python:3.9

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY ./astronomy /app/app

WORKDIR /app/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]