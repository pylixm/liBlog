FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && rm -rf requirements.txt

COPY . /code/
COPY ./compose/production/gunicorn.sh /code/
RUN sed -i 's/\r//' gunicorn.sh \
    && chmod +x gunicorn.sh

COPY ./compose/production/entrypoint.sh /code/
RUN sed -i 's/\r//' entrypoint.sh \
    && chmod +x entrypoint.sh

ENTRYPOINT ["/bin/bash", "entrypoint.sh"]