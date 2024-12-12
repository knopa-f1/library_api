FROM python:3.10

RUN mkdir /library_api

WORKDIR /library_api

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 8000
