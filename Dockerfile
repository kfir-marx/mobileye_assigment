FROM alpine:latest

RUN apk update && \
    apk add python3 py3-pip
RUN ln -sf /usr/bin/python3 /usr/bin/python
RUN rm -rf /var/cache/apk/*

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000/tcp
CMD ["python", "/app/main.py"]
