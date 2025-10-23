FROM python:3.12-slim-bullseye

WORKDIR /app

RUN useradd -m myuser

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir logs qr_codes && chown myuser:myuser logs qr_codes

COPY --chown=myuser:myuser . .

USER myuser


ENTRYPOINT ["python", "main.py"]
CMD ["--url","https://github.com/SuvarnaChandrika3002"]