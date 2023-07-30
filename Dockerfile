FROM python:3.9

EXPOSE 8888
EXPOSE 8877
WORKDIR /app

RUN apt -y update
RUN apt -y install socat

COPY ./chal .

RUN chmod +x /app/alice.py /app/bob.py /app/run.sh
RUN pip install -r /app/requirements.txt

CMD socat TCP-LISTEN:8888,fork,reuseaddr EXEC:"/app/alice.py" & socat TCP-LISTEN:8877,fork,reuseaddr EXEC:"/app/bob.py"