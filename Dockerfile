FROM tiangolo/meinheld-gunicorn-flask:python3.9
RUN pip install --upgrade setuptools
ENV STATIC_URL /static
ENV STATIC_PATH /app/static

COPY / /app/.
COPY application.py /app/main.py
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt
