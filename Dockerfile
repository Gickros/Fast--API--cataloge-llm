FROM python:3.13-alpine
WORKDIR /Fast--API--cataloge-llm
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirments.txt

COPY . .
CMD ["uvicorn" , "main:app" , "-host" , "0.0.0.0" , "--port" , "5432"]