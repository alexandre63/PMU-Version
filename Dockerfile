FROM python:3.12-alpine

COPY server /server

RUN pip install -r /server/requirements.txt

ENTRYPOINT ["fastapi", "run", "/server/main.py"]