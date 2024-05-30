FROM python:3.12
LABEL authors="hexa"

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8089

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8089"]