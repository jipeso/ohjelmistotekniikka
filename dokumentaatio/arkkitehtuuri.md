## Arkkitehtuurikuvaus

### Rakenne

Sovellus noudattaa kolmitasoista kerrosarkkitehtuuria

![Pakkausrakenne](./kuvat/pakkauskaavio.png)

Pakkaus _ui_ sisältää käyttöliittymästä, _services_ sovelluslogiikasta ja _repositories_ tiedon tallennuksesta vastaavan koodin. Pakkaus _entities_ sisältää sovelluksen tietokohteita kuvaavat luokat.

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
