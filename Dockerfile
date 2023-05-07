FROM Python:3.11.3

WORKDIR /Flask webserver
COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT [ "Python" ]
CMD ["server.py"]
