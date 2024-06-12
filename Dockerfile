FROM python:3.12
LABEL authors="hexa"
# Install gcc and other dependencies
RUN apt-get update && \
    apt-get install -y gcc libc-dev libffi-dev libssl-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install setuptools
RUN pip install --upgrade pip setuptools

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8089

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8089"]