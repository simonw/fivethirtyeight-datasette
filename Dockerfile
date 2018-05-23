FROM python:3.6-slim-stretch
RUN apt-get update
RUN apt-get install -y python3-dev gcc git
ADD datasette .
RUN pip install datasette/
ADD fivethirtyeight.db .
ADD metadata.json .
RUN datasette inspect fivethirtyeight.db --inspect-file inspect-data.json

EXPOSE 8001

CMD datasette serve fivethirtyeight.db --host 0.0.0.0 \
    --cors --port 8001 --inspect-file inspect-data.json -m metadata.json \
    --config facet_time_limit_ms:1000
