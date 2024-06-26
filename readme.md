# ATS Sample Application

## Setup without Docker

The first thing to do is to clone the repository:

Create a virtual env

Then install the dependencies:

```sh
pip install -r requirements.txt
```

Once `pip` has finished downloading the dependencies:
```sh
python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/`.

Extra
Want some test data to try out
```sh
python manage.py create_test_data
```
Play around with the data

## Setup with Docker

Docker installed on your machine
Docker Compose installed on your machine

The first thing to do is to clone the repository:

```sh
cd ats_project
docker-compose up --build
```
