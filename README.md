# Django Graph Database

A Grah Database implementation in Django


## Docker

### building the image

```shell
docker build -t jadgraphdb:latest .
```

### running the image

```shell
docker run -it --network="host" --rm --env-file .env jadgraphdb:latest
```


### query by jad_id

http://127.0.0.1:8000/jad/q?jad-id=jad_occurrence__1&max-distance=0.09&amount=3


### import JAD (short) Passages:
```shell
uv run manage.py import_jad_passages
```

> done in 0:08:28 (1.23K requests; 26.146K input tokens)

### import JAD (full text) Passages:
```shell
uv run manage.py import_jad_full_texts
```

> done in 0:08:26 (~600K input tokens)


### import JAD (sentences) Passages:
```shell
uv uv run manage.py import_jad_sentences
```

> done in 1:44:50 (~700K input tokens)


### import Vulgata (32.921 verses)
```shell
uv run manage.py import_vulgata
```

> done in 3 hours (~1.5M input tokens)