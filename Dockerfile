FROM python:3.8-slim-buster
# FROM python:3.7-alpine
WORKDIR /code
ENV FLASK_APP=api.py
ENV FLASK_RUN_HOST=0.0.0.0

COPY requirements.txt requirements.txt
# RUN pip install pandas

RUN pip3 install -r requirements.txt
EXPOSE 8000
COPY . .
ENTRYPOINT [ "python" ]
CMD ["app.py"]