FROM ubuntu:22.04


RUN apt-get update && \
    apt-get install -y python3 python3-pip &&\
    pip3 install Flask


CMD ["python3", "-m", "run", "host", "0.0.0.0", "port", "8080"]
