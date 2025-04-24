FROM python:3.12-slim

WORKDIR /src

COPY ./src /src/src
COPY requirements.txt /src/

RUN apt-get update && apt-get install -y sqlite3

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
