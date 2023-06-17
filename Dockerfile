FROM python:3.10

WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["sanic", "src.adapters.left.http.app:app", "--host", "0.0.0.0", "--port", "8000"]
