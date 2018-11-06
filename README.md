# SI Converter Web Service

This project provides an HTTP endpoint `/units` for converting units to their
SI counterparts. Specifically, for a given input of any number of units
multiplied and/or divided, it returns the name of SI equivalent of those units,
and a multiplication factor that can be used to convert the non-SI units to
their SI counterparts. Ex:

```
GET "/units/si?units=degree/minute" -> { “unit_name”: "rad/s", “multiplication_factor”: 0.00029088820866572 }
```

## Usage

Docker:

```
docker build -t tkennedy/si-converter .
docker run --rm -d -p 8080:80 --name si-converter tkennedy/si-converter
```

The service will be accessible under http://localhost:8080.

To clean up:

```
docker stop si-converter
docker rmi tkennedy/si-converter
```

## Development

The docker image is setup to auto-reload on source file changes. Simply run the
container with the app directory mounted under `/var/www/app`:

```
docker build -t tkennedy/si-converter .
docker run --rm -d -p 8080:80 -v $PWD:/var/www/app --name si-converter tkennedy/si-converter
```

Once the app is running, you can get stack traces and debug output by running:

```
docker exec si-converter tail -f  /var/log/uwsgi/app/app.log
```
