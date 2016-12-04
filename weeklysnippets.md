# Oppimispäiväkirja

Tänne kirjataan koosteet siitä, mitä projektityön aikana opitaan ja mitä aikoo tehdä.

## Viikko 48
* Tuomas: 
  * __Mitä tein:__ RESTful API:a tein ensin Socketeilla yksinkertaiseen Python scriptiin ja homma eteni nopeasti, eikä HTTP requestiin ollut vaikeaa vastata oikeassa formaatissa. 1,5h työllä sai paljon aikaiseksi ja API olisi valmistunut nopeasti jatkamalla tällä tyylillä. Vaihdettiin kuitenkin Django Rest Frameworkkiin, koska ajateltiin Databasen käytön olevan sutjakkaaampaa käyttämällä Djangon ORM:ia. Djangon käytössä törmäsin erinäisiin ongelmiin ja aikaa paloi paljon debuggaukseen. Django ORM kuitenkin nopeutti hieman tietomallien suunnittelua, toteutusta ja käyttöä.
  * __Mitä opin:__ RESTful API ja HTTP-protokolla eivät olleet täysin vieraita entuudestaan, joten en koe oppineeni niistä mitään uutta. Opin kuitenkin Pythonista uutta muutaman kirjaston osalta (logging ja traceback), joita en ollut ennen käyttänyt. Lisäksi tyypilliset Python parametrit *args ja **kwargs tulivat paremmin tutuiksi.
  * __Mitä tulevalla viikolla:__ Eiköhän tämä harjoitustyö ole valmis.

* Aleksi:
  * **Mitä tein:** Keskityin frontin tekemiseen tässä harjoitustyössä sekä RESTful API:n dokumentoimiseen ja testaukseen. Suurin osa harjoitustyöhön käyttämästäni ajasta kului REST API:n palauttaman json datan paloittelemiseen ja esittämiseen siististi frontissa. Ensin tein tämän lisäämällä javascriptin innerHTML -metodilla dataa, mutta tästä tuli epäselvä ratkaisu. Muutin ratkaisua siten, että määrittelin ensin ulkoasun tulosten esittämiselle ja tämän jälkeen dataa käsiteltäessä täydensin näihin elementteihin JQueryllä datan. Tämän lisäksi toteutin virhekäsittelyä REST:iin eli miten toimintaan tilanteessa, jossa esimerkiksi OMDb ei löydä elokuvaa.
  * **Mitä opin:** RESTful API ja HTTP olivat minullekin jo entuudestaan jokseenkin tuttuja. Opin harjoitustyöstä kuinka kannattaa tehdä RESTful API:n dokumentaatio. Harjoitustyössä tulin myös miettineeksi HTTP-vastauskoodeja ja koen oppineeni näistä lisää.
  * **Mitä tulevalla viikolla:** Harjoitustyö toteutus on valmis eikä sitä jatketa ensi viikolla enää. Tulevalla viikolla demoillaan assistentille meidän ratkaisua.