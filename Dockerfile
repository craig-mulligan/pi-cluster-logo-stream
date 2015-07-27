FROM resin/raspberrypi2-python

# RUN systemd in container, keeps the container open even if you main process fails.
ENV INITSYSTEM on

# Install deps
RUN apt-get update
RUN apt-get install -y fbi

# install ibm IoT python lib
RUN pip install tweepy

# copy current directory into /app
COPY . /app

# run start script when container starts on device
CMD ["bash", "/app/start.sh"]