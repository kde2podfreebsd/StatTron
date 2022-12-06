FROM python:3.10

WORKDIR /client
COPY requirements.txt /client
RUN pip install --upgrade pip &&  python -m pip install -r requirements.txt

EXPOSE 5000

COPY ../client /client
