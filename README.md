## Ohjelmistotekniikka, harjoitustyö

![CI](https://github.com/jipeso/ohjelmistotekniikka/actions/workflows/main.yml/badge.svg)

Uutisartikkelihallinta-sovellus, tehty ohjelmistotekniikan harjoitustyönä keväällä 2025.

### Dokumentaatio

[Vaatimusmäärittely](https://github.com/jipeso/ohjelmistotekniikka/blob/main/dokumentaatio/vaatimusmaarittely.md)

[Tuntikirjanpito](https://github.com/jipeso/ohjelmistotekniikka/blob/main/dokumentaatio/tuntikirjanpito.md)

[Changelog](https://github.com/jipeso/ohjelmistotekniikka/blob/main/dokumentaatio/changelog.md)

### Sovelluksen käyttö

Asenna riippuvuudet komennolla:

```bash
poetry install --no-root
```

Sovellus käynnistyy komennolla:

```bash
poetry run invoke start
```

Tesit voi suorittaa komennolla:

```bash
poetry run invoke test
```

Testikattavuusraportin voi generoida htmlcov-hakemistoon komennolla:

```bash
poetry run invoke coverage-report
```

Tiedoston [.pylintrc](./.pylintrc) määrittelemät tarkistukset voi suorittaa komennolla:

```bash
poetry run invoke lint
```