
FROM python:3.11-slim


RUN apt-get update && \
    apt-get install -y libgdiplus fonts-dejavu-core && \
    ln -s /usr/lib/libgdiplus.so /usr/lib/gdiplus.dll && \
    apt-get clean

WORKDIR /app


COPY . /app


RUN pip install --upgrade pip
RUN pip install -r requirements.txt


EXPOSE 8000

CMD ["gunicorn", "projecteFinalDAW.wsgi:application", "--bind", "0.0.0.0:8000"]
