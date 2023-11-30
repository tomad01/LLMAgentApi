FROM python:3.11

ENV LANG=C.UTF-8

RUN mkdir /app 
WORKDIR /app

COPY README.md /app/
COPY pyproject.toml /app/

ENV PYTHONPATH=${PYTHONPATH}:${PWD} 
RUN pip3 install poetry
RUN poetry config virtualenvs.create false

COPY src /app/src
RUN poetry install --only main

CMD ["echo"]