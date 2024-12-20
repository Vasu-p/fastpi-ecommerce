FROM python:3.13
WORKDIR /app

ADD requirements.txt /app/requirements.txt

RUN pip install --upgrade -r requirements.txt

EXPOSE 8000

COPY ./ /app

CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]