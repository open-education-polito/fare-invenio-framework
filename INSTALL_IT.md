# Installazione della piattaforma

### Versione della guida semplificata in lingua italiana. 

Il deploy è basato su immagini `docker` e usa `docker-compose`.

1. Fare una pull dell'immagine già buildata e inserita nel registry. Per farlo:

```bash
docker pull ghcr.io/open-education-polito/fare:0.8.0
```

Questo evita di doversi fare la build in locale. 
Siccome in `docker-compose` la build è chiama `fare` è necessario modificare il
tag in questo modo:

```bash
docker tag ghcr.io/open-education-polito/fare:0.8.0 fare
```

Ovviamente il tag vero e proprio, ovvero `0.8.0` varia al variare della
versione scaricata.
Se, invece, si vuole fare la build direttamente in locale si può fare:

```bash
./docker/build-images.sh
```

2. Scaricare anche il resto del repo in locale (tramite `git clone` oppure
   direttamente da GitHub):

```bash
git clone https://github.com/open-education-polito/fare-platform.git
```

Nota bene: si può clonare via `HTTPS` o via `GIT`, la seconda è consigliata in
modo da poter poi lavorare in un repository Git.

3. Settare tutte le env variables nel file `.env`

Per avere un'idea delle env vars da settare si può consulare il file
[.env](https://github.com/open-education-polito/fare-platform/blob/master/.env.example)

4. Far partire tutti i docker in locale:
 
```bash
docker-compose -f docker-compose.fare.yml up -d
```

La prima volta che verrà utilizzato questo comando docker scaricherà tutte le
base image in locale e quindi ci metterà del tempo. 

Il file
[docker-compose.fare.yml](https://github.com/open-education-polito/fare-platform/blob/master/docker-compose.fare.yml#L60)
contiene la definizione e i ref di tutta l'infrastruttura.

5. A questo punto tutti i servizi essenziali dovrebbero essere partiti. 
Si può lanciare un `docker ps` per vedere se sono tutti up & running.

6. Inizializzazione di cache e DB:

```bash
docker-compose -f docker-compose.fare.yml run --rm web-ui ./scripts/setup
```

7. A questo punto il servizio dovrebbee essere raggiungibile in localhost
   dunque via browser puntare a `127.0.0.1` in locale.
   Se il Load Balancer è correttamente partito dovrebbe gestire direttamente il
   redirect `80 -> 443` e ci sarà una notice di certificati non trusted dal
   browser. Proseguire, siamo in fase di test quindi è OK.

I servizi sono configurati in modalità "restart always" il che non è il massimo
in fase di debug ma comunque con un `docker logs nome_servizio` si possono
consultare i log del singolo servizio.

### Configurazione dei certificati reali
I certificati reali possono essere creati gratuitamente con [let's encrypt](https://letsencrypt.org/getting-started/).

Una volta creati, per configurare i certificati bisogna seguire la seguente procedura:

* Copiare chiave e certificato in  `/docker/nginx/official_certificates`
**NOTA:** se i certificati non vengono creati con let's encrypt è necessario sostituire ` /etc/letsencrypt/live/NOME_DOMINIO/` con il percorso in cui sono stati salvati i certificati

 ```bash
 sudo cp /etc/letsencrypt/live/NOME_DOMINIO/fullchain.pem ./docker/nginx/official_certificates/fullchain.crt
 sudo cp /etc/letsencrypt/live/NOME_DOMINIO/privkey.pem ./docker/nginx/official_certificates/privkey.key
   ```
* Concatenare chiave e certificato in `/docker/haproxy/official_certificates`
   ```bash
   sudo cat ./docker/nginx/official_certificates/fullchain.crt ./docker/nginx/official_certificates/privkey.key > ./docker/haproxy/official_certificates/haproxy_cert.pem
 ```
 
* Aggiornare le seguenti voci nel file `.env` 
 ```bash
HAPROXY_CERT=./official_certificates/haproxy_cert.pem
NGINX_CERT=./official_certificates/fullchain.crt
NGINX_KEY=./official_certificates/privkey.key
```

* Fare la build dei servizi frontend e lb per caricare i nuovi certificati
 ```bash
sudo docker-compose -f docker-compose.fare.yml build --no-cache lb frontend
docker-compose -f docker-compose.fare.yml up -d
```


### Creazione utenti e ruoli

* Entrare nel container e nell'environment 

```bash
docker exec -it fare-platform_web-ui_1 /bin/bash
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

In fase di startup verrà creato un ruolo `roomCreator` dunque per usare la
funzionalità di videoconferenza sarà necessario aggiungere un utente a quel
ruolo come visto poco sopra.
