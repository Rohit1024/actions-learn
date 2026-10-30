FROM python:3.14-alpine
ENV PYTHONDONTWRITEBYTECODE=1
COPY worker.py entrypoint.sh /opt/action/
RUN chmod +x /opt/action/entrypoint.sh
ENTRYPOINT ["/opt/action/entrypoint.sh"]
