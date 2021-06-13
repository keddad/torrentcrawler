FROM python:3.9-slim

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv

RUN pipenv install --deploy --system

COPY ./* ./

CMD ["uvicorn", "main:app", "--ws", "none", "--host", "0.0.0.0"]