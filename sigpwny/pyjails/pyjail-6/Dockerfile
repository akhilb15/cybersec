FROM ubuntu:20.04

RUN apt-get update && apt-get install -y socat python3 python3-pip

COPY flag.txt /
RUN chmod 444 /flag.txt

RUN python3 -m pip install RestrictedPython requests
RUN adduser chal

RUN mkdir -p /chal
WORKDIR /chal

COPY chal.py .
RUN chmod 555 chal.py
USER chal

CMD socat -T60 TCP-LISTEN:1337,fork,reuseaddr EXEC:"python3 chal.py",stderr
