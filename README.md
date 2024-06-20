# Progetto Laboratorio Industria 4.0

## Mobile Sensing

Realizzazione di un sistema in grado di rilevare buche. 
Il sistema è composto da un dispositivo posizionabile su una bicicletta o un carretto, in grado di rilevare tramite un accelerometro la presenza di buche e la posizione esatta della rilevazione tramite un modulo GPS, e un componente server in grado di ricevere i dati dal dispositivo, di elaborarli e di permetterne la visualizzazione tramite un'interfaccia web.

## Installazione Componente Server

Per il componente server viene utilizzato docker per la creazione dei container necessari per la ricezione dei dati dal dispositivo e per la visualizzazione dei risultati nella pagina web dedicata.
Viene utilizzato un file docker-compose.yml per la creazione dei container. Vengono creati i container per la visualizzazione dei grafici tramite grafana e per la creazione del webserver Apache su cui è possibile accedere alle pagine web. 

```
version: "3.8"
services:
  grafana_mobile_sensing:
    image: grafana/grafana:latest
    container_name: grafana_mobile_sensing
    restart: unless-stopped
    ports:
     - '3003:3000'
  php_mobile_sensing:
    image: php:apache
    container_name: webserver_mobile_sensing
    restart: unless-stopped
    ports:
      - '8083:80'
    volumes:
      - /home/filippoonesti/mobile_sensing/html:/var/www/html/
  mqtt_mobile_sensing:
    image: filippoonesti/mobile_sensing_mqtt:latest
    container_name: mqtt_mobile_sensing
    restart: unless-stopped
    volumes:
      - /home/filippoonesti/mobile_sensing/html/records:/home/filippoonesti/mobile_sensing/html/records
```

Per eseguire il file docker-compose e per avviare i container si utilizza il seguente comando:

```
docker compose up -d
```

Una volta messi in esecuzione tutti i container necessari, è possibile accedere alla pagina web per la visualizzazione dei record all'indirizzo *http://localhost:8083*.

![Webpage](https://github.com/OnestiFilippo/mobile_sensing/assets/77025139/d6f8cd72-aaa1-408e-8258-fa120c57f258)

## Componente Client

La componente client del progetto consiste in un dispositivo hardware composto da un microcontrollore Raspberry Pi Pico W, un accelerometro, un modulo GPS, un display e due pulsanti.
Sul microcontrollore, tramite MicroPython, vengono letti i dati dai sensori e vengono inviati alla componente Server tramite MQTT.
I file per l'esecuzione dello scirpt MicroPython e le librerie necessarie sono all'interno della cartella `code-pico`.

![MS](https://github.com/OnestiFilippo/mobile_sensing/assets/77025139/be6a75e0-7746-47ff-bd65-1dd09d1a98cf)


