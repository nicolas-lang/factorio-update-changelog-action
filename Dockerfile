# Dockerfile
FROM python:3.9-slim

COPY entrypoint.sh /entrypoint.sh
COPY main.py /main.py

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
