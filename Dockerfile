FROM python:3.12

RUN mkdir /wb_price_bot

WORKDIR /wb_price_bot

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]