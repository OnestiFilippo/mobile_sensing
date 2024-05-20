# Progetto Laboratorio Industria 4.0

## Mobile Sensing

Realizzazione di un sistema in grado di rilevare buche. 
Il sistema è composto da un dispositivo posizionabile su una bicicletta o un carretto, in grado di rilevare tramite un accelerometro la presenza di buche e la posizione esatta della rilevazione tramite un modulo GPS, e un componente server in grado di ricevere i dati dal dispositivo, di elaborarli e di permetterne la visualizzazione tramite un'interfaccia web.

## Installazione

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
    ports:
      - '8083:80'
    volumes:
      - /home/filippoonesti/mobile_sensing/html:/var/www/html/
  mqtt_mobile_sensing:
    image: filippoonesti/mobile_sensing_mqtt:1.5
    container_name: mqtt_mobile_sensing
    volumes:
      - /home/filippoonesti/mobile_sensing/html/records:/home/filippoonesti/mobile_sensing/html/records
```

Per eseguire il file docker-compose e per avviare i container si utilizza il seguente comando:

```
docker compose up -d
```
