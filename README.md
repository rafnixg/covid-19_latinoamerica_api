# Covid-19 Latinoamerica API

API desarrollada para el proyecto [covid-19_latinoamerica](https://github.com/DataScienceResearchPeru/covid-19_latinoamerica)

## Instalación

Creamos entorno virtual en python e instalamos las dependencias

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
```

O en Anaconda
```bash
$ conda create -n covid19 python=3.7 --y
$ conda activate covid19
$ pip install -r requirements.txt
```


## ETL

El ETL extrae la data de todos los archivos CSV del repositorio [covid-19_latinoamerica](https://github.com/DataScienceResearchPeru/covid-19_latinoamerica) y la concatena en 1 solo archivo `data.csv`, ademas que guarda cada uno de los archivos en el directorio `data`.

```bash
$ python3 etl.py
```

## API
El API se actualiza automáticamente cada hora en base a los archivos del repositorio [covid-19_latinoamerica](https://github.com/DataScienceResearchPeru/covid-19_latinoamerica)


```bash
export FLASK_APP=app.py
flask run
```

Versión online del API en [https://covid19latam.herokuapp.com/](https://covid19latam.herokuapp.com/)
