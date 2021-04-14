FROM python

RUN mkdir -p /app/internet

WORKDIR /app/internet

COPY . .

RUN pip install -r requirements.txt

RUN python check.py&

ENTRYPOINT ["python"]

CMD ["api.py"]