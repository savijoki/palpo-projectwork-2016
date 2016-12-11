# Palvelupohjaiset järjestelmät
Harjoitustyön tekijöiden kurssin ilmoittautumiseen käyttämät sähköpostit:
aleksi.savijoki@student.tut.fi
tuomas.a.aho@student.tut.fi
## Projektisuunnitelma
Tässä projektissa käytetään kahta avointa RESTful rajapintaa (OMDb ja MyAPIFilms) ja näistä saadut tiedot yhdistetään ja tarjotaan ulospäin oma RESTful rajapinta. Projekti tullaan toteuttamaan käyttämällä Djangoa.

Lopullisessa tuotteessa käyttäjä syöttää hakusanan (jonkin elokuvan nimi tai sarjan nimi tms.) hakukenttään ja tällä hakusanalla järjestelmä tekee haut OMDb -ja MyAPIFilmsin tarjoamiin rajapintoihin ja yhdistää niiden tulokset uudeksi rajapinnaksi.

Rajapinta tallentaa hakuja tietokantaan tulevien vastaavien hakujen nopeuttamiseksi. Lisäksi onnistuneista hauista tallennetaan elokuvan tiedot, sekä siihen liitetään haetut trailerit. Näin ollen järjestelmä säilyttää lokaalisti elokuvien tiedot ja niihin liitetyt trailerit, jolloin yhteydenotot ulkoisiin rajapintoihin saadaan minimoitua ja omaan rajapintaan tehtyjen pyyntöjen vastausaikaa lyhennettyä.

## API

Alla esitetty API:n endpointit.

### Title (hakeminen nimellä)

Palauttaa json dataa elokuvan tiedoista sekä yhden tai useamman trailerin.

* **URL**:
/api/search/title?query=:title&count=:count

* **Metodi**:
GET

* **URL parametrit**:
**Pakollinen**:
title=[string]
**Vapaaehtoinen**:
count=[integer]

* **Data parametrit**:
\-

* **Onnistunut vastaus**
**Koodi**: 200
**Sisältö**: 
```json
{"title":"...","imdbId":"...","director":"...","writer":"...","actors":"...","poster":"...","genre":"...","runtime":"...","released":"...","plot":"...","imdbLink":"...","imdbRating":"...","trailers":[{"embed":"..."}]}
```

* **Virheellinen vastaus**:
**Koodi**: 404
**Sisältö**: {}

* **Esimerkki**:
```javascript
$.ajax({
    'url' : '/api/search/title',
    'type' : 'GET',
    'dataType': 'json',
    'data' : {
        'query' : 'Deadpool',
        'count' : 1
    },
    success: function(data) {
        console.log(data);
    }
});
```

### IMDbId (hakeminen IMDb-tunnuksella)

Palauttaa json dataa elokuvan tiedoista sekä yhden tai useamman trailerin.

* **URL**:
/api/search/imdbid?query=:imdbid&count=:count

* **Metodi**:
GET

* **URL parametrit**:
**Pakollinen**:
imdbid=[string]
**Vapaaehtoinen**:
count=[integer]

* **Data parametrit**:
\-

* **Onnistunut vastaus**
**Koodi**: 200
**Sisältö**: 
```json
{"title":"...","imdbId":"...","director":"...","writer":"...","actors":"...","poster":"...","genre":"...","runtime":"...","released":"...","plot":"...","imdbLink":"...","imdbRating":"...","trailers":[{"embed":"..."}]}
```

* **Virheellinen vastaus**:
**Koodi**: 404
**Sisältö**: {}

* **Esimerkki**:
```javascript
$.ajax({
    'url' : '/api/search/imdbid',
    'type' : 'GET',
    'dataType': 'json',
    'data' : {
        'query' : 'tt1431045',
        'count' : 1
    },
    success: function(data) {
        console.log(data);
    }
});
```

### Top10 (suosituimmat haut)

Palauttaa listan json dataa suosituimmista hauista sekä hakujen lukumääristä tietyllä aikavälillä.

* **URL**:
/api/search/top?days=:days

* **Metodi**:
GET

* **URL parametrit**:
**Vapaaehtoinen**:
days=[integer]

* **Data parametrit**:
\-

* **Onnistunut vastaus**
**Koodi**: 200
**Sisältö**: 
```json
[{"days": ..., "title": "...", "poster": "...", "imdbId": "...", "imdbRating": "...", "searches": ..., "imdbLink": "..."},{...}]
```

* **Virheellinen vastaus**:
**Koodi**: 404
**Sisältö**: {}

* **Esimerkki**:
```javascript
$.ajax({
    'url' : '/api/search/top',
    'type' : 'GET',
    'dataType': 'json',
    'data' : {
        'days' : 7
    },
    success: function(data) {
        console.log(data);
    }
});
```


