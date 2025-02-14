FROM python:3.12


WORKDIR /HistoryService

COPY . /HistoryService


RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]