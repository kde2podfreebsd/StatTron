FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

CMD ["pip", "install", "--upgrade", "pip"]

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY UserBot /code/app

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "80"]