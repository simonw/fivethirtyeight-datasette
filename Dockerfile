FROM python:3.6-slim-stretch
RUN apt-get update
RUN apt-get install -y python3-dev gcc git
ADD data.zip .
ADD datasette.zip .
ADD requirements.txt .
RUN pip install -r requirements.txt
RUN pip install datasette.zip
RUN pip install csvs-to-sqlite
RUN unzip data.zip
RUN csvs-to-sqlite data fivethirtyeight.db
RUN datasette inspect fivethirtyeight.db --inspect-file inspect-data.json
ADD make_metadata.py .
RUN python make_metadata.py

EXPOSE 8001

CMD datasette serve fivethirtyeight.db --host 0.0.0.0 \
    --cors --port 8001 --inspect-file inspect-data.json -m metadata.json \
    --limit facet_time_limit_ms:1000
