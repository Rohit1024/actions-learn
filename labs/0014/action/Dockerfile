FROM python:3.14-alpine
ENV PYTHONDONTWRITEBYTECODE=1
COPY runtime-policy.txt /opt/action/runtime-policy.txt
RUN python3 -c "from pathlib import Path; assert Path('/opt/action/runtime-policy.txt').read_text().strip() == 'single-line-inputs'; print('runtime policy checked')"
COPY entrypoint.py /opt/action/entrypoint.py
ENTRYPOINT ["python3", "/opt/action/entrypoint.py"]
