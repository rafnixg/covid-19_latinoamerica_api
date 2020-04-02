# Covid-19 Latinoamerica API

API desarrollada para el proyecto [covid-19_latinoamerica](https://github.com/DataScienceResearchPeru/covid-19_latinoamerica)

## Instalación

Creamos entorno virtual en python e instalamos las dependencias

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install -r requeriments.txt
```

## ETL

El ETL extrae la data de todos los archivos CSV del repositorio [covid-19_latinoamerica](https://github.com/DataScienceResearchPeru/covid-19_latinoamerica) y la concatena en 1 solo archivo `data.csv`, ademas que guarda cada uno de los archivos en el directorio `data`.

```bash
$ python3 etl.py
```

## API

```bash
export FLASK_APP=app.py
flask run
```
