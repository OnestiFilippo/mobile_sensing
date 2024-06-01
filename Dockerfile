FROM python
WORKDIR /home/filippoonesti/mobile_sensing
COPY mqttMS.py .
RUN ["pip3","install","paho-mqtt"]
ENTRYPOINT ["python3", "mqttMS.py"]
