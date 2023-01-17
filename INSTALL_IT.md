# Installazione di test

Il sistema si basa su Docker. Bisogna avercelo installato in locale.

1. Fare una pull dell'immagine già buildata e inserita nel registry. Per farlo:

```bash
docker pull ghcr.io/open-education-polito/fare:0.8.0
```

Questo evita di doversi fare la build in locale. Se, invece, si vuole fare la build si può facendo:

```bash
./docker/build-images.sh
```

2. Scaricare anche il resto del repo in locale (tramite git clone oppure direttamente da GitHub):

```bash
git clone https://github.com/open-education-polito/fare-platform.git
```

3. Settare tutte le env variables nel file `.env`

Per avere un'idea delle env vars da settare si può consulare il file [.env](https://github.com/open-education-polito/fare-platform/blob/master/.env.example)

4. Far partire tutti i docker in locale:
 
```bash
docker-compose -f docker-compose.fare.yml up -d
```

La prima volta che verrà utilizzato questo comando docker scaricherà tutte le base images in locale e quindi ci metterà del tempo.
Se si da un'occhiata al file [docker-compose.fare.yml](https://github.com/open-education-polito/fare-platform/blob/master/docker-compose.fare.yml#L60) si noterà che la base image per la nostra web app è `fare`. Dunque questa deve essere presente nella dir locale oppure deve essere conosciuta da docker (è stata scaricata al punto 1).

5. A questo punto tutti i servizi essenziali dovrebbero essere su
Si può lanciare un `docker ps` per vedere se sono tutti up & running.

6. Inizializzazione di cache e DB:

```bash
docker-compose -f docker-compose.fare.yml run --rm web-ui ./scripts/setup
```

7. A questo punto il servizio dovrebbee essere raggiungibile su `127.0.0.1:5000` in locale. 

8. Se si vogliono avere dei certificati non di test la procedura è la seguente. 

I certificati vengono copiati in fase di startup dei container da due cartelle, una è `/docker/haproxy` e l'altra `/docker/nginx`. Quindi nel file `.env` non ci sono path hardcoded ma solo il nome dei file in quelle cartelle rispettivamente:

```bash
HAPROXY_CERT=haproxy_cert.pem
NGINX_CERT=test.crt
NGINX_KEY=test.key
```

Attenzione al fatto che per nginx ci sono key e crt mentre per haproxy c'è solo un pem: si può fare una concatenazione tipo:

```bash
cat test.crt test.key > haproxy_cert.pem 
```
in modo tale da appendere la chiave al certificato. Se non c'è la chiave ci sarà un problema in fase di startup del load balancer.

I servizi sono configurati in modalità "restart always" il che non è il massimo in fase di debug ma comunque con un `docker logs nome_servizio` si possono consultare i log del singolo servizio.

### Creazione utenti e ruoli

* Entrare nel container e nell'environment 

```bash
docker exec -it fare-invenio_web-ui_1 /bin/bash
```

* Creazione utente di prova 

```bash
invenio users create -a email_address
```

* Aggiunta dell'utente al ruolo di admin

```bash
invenio roles add email_address_di_prima admin
```

In questo modo si è creato il primo utente admin che può avere permessi da "root" sul resto

In fase di startup verrà creato un ruolo `roomCreator` dunque per usare la funzionalità di videoconferenza sarà necessario aggiungere un utente a quel ruolo come visto poco sopra.