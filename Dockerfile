FROM python
WORKDIR /home/filippoonesti/mobile_sensing
COPY mqtt.py .
RUN ["pip3","install","paho-mqtt"]
ENTRYPOINT ["python3", "mqtt.py"]
