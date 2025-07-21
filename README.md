# derbynames microservice

[![Docker](https://github.com/bdunnette/derbynames-microservice-markovify/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/bdunnette/derbynames-microservice-markovify/actions/workflows/docker-publish.yml)

Generating amusing (?) derby names using [markovify](https://github.com/jsvine/markovify).

## Building

```bash
docker build -t derbynames .
docker run -p 5000:5000 derbynames
```

## Deploying to dokku

```bash
git remote add dokku dokku@your-dokku-host:derbynames
git push dokku main
```
