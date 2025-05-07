# Arkkitehtuurikuvaus

## Rakenne

Sovellus noudattaa kolmitasoista kerrosarkkitehtuuria

![Pakkausrakenne](./kuvat/pakkauskaavio.png)

Pakkaus _ui_ sisältää käyttöliittymästä, _services_ sovelluslogiikasta ja _repositories_ tiedon tallennuksesta vastaavan koodin. Pakkaus _entities_ sisältää sovelluksen tietokohteita kuvaavat luokat.

## Käyttöliittymä

Käyttöliittymä sisältää viisi erilaista näkymää:

- Artikkeli-lista
- Artikkelin luominen
- Artikkelin lukeminen
- Artikkelin editointi
- Artikkelien etsiminen RSS-syötteestä

Jokainen näkymä on toteutettu omana luokkanaan, joista ainoastaa yksi on kerrallaan näkyvillä. Näkymien näyttämisestä vastaa [UI](../src/ui/ui.py)-luokka. Käyttöliittymä on pyritty eristämään sovelluslogiikasta. Se kutsuu ainoastaan [ArticleService](../src/services/article_service.py) ja [FeedService](../src/services/feed_service.py)-luokkien metodeja.

## Tietojen pysyväistallennus

Pakkauksen _repositories_ luokka `ArticleRepository` huolehtii artikkelien tallentamisesta. Tiedot tallennetaan SQLite-tietokantaan.

### Tiedostot

Sovellus sisältää json-tiedoston, jossa on muutamia esimerkkisyötteitä RSS-lukutoimintoa varten.

Sovellus tallentaa artikkelit SQLite-tietokannan tauluun `articles`, joka alustetaan [initialize_database.py](https://github.com/jipeso/ohjelmistotekniikka/blob/main/src/initialize_database.py)-tiedostossa.

Sovelluksen juureen voidaan luoda halutessa .env tiedosto, jossa tiedoston nimi voidaan määritellä.

## Päätoiminnallisuudet

Seuraavaksi kuvataan sovelluksen toimintalogiikkaa sekvenssikaavioiden avulla.

### Artikkelin luominen

Uuden artikkelin luovan "create article"-painikkeen klikkaamisen jälkeen sovelluksen kontrolli etenee seuraavan sekvenssikaavion mukaisesti:

```mermaid
sequenceDiagram
  actor User
  participant UI
  participant ArticleService
  participant ArticleRepository
  participant article
  User->>UI: click "create article"
  UI->>ArticleService: create_article("title", "content", "url")
  ArticleService->>article: Article("title", "content", "url")
  ArticleService->>ArticleRepository: create(article)
  ArticleRepository-->>ArticleService: article
  ArticleService-->>UI: article
  UI->>UI: initialize_article_list()
```

Tapahtumankäsittelijä kutsuu sovelluslogiikan metodia create_article antaen parametreiksi luotavan artikkelin tiedot. Sovelluslogiikka luo uuden `Article`-olion ja tallettaa sen kutsumalla `ArticleRepository`:n metodia `create`. Tästä seurauksena on se, että käyttöliittymä päivittää näytettävät articlet kutsumalla omaa metodiaan `initialize_article_list`.


### RSS-syötteen lukeminen

```mermaid
sequenceDiagram
  actor User
  participant UI
  participant FeedService
  participant FeedRepository
  User->>UI: select a RSS-feed
  UI->>FeedService: parse_feed("url")
  FeedService->>UI: articles
  UI->>UI: initialize_result_list(articles)
```

### Muut toiminnallisuudet

Samat periaatteet toistuu kaikissa toiminnallisuuksissa, käyttöliittymän tapahtumankäsittelijä kutsuu sopivaa sovelluslogiikan metodia, joka päivittää artikkelien tilaa. Kontrollin palautuessa käyttöliittymään aktiivinen näkymä päivitetään.