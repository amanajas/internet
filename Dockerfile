FROM python

RUN mkdir -p /app/internet

WORKDIR /app/internet

COPY requirements.txt .
COPY api.py .
COPY runner.py .
COPY scripts/wrapper.sh start.sh

RUN chmod +x start.sh

RUN pip install -r requirements.txt

CMD ["./start.sh"]
