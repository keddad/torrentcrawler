FROM python:3.9-slim

WORKDIR /app

COPY ./* ./

RUN pip install pipenv

RUN pipenv install --deploy --system

CMD ["uvicorn", "main:app", "--ws", "none", "--host", "0.0.0.0"]