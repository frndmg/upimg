# Image uploader API

Image uploader API using django, postgres, and minio.

## Run

Lets run the server, migrate the database and prepare a new super user.
Actually any user could do the job but better to have super powers, no?

```bash
$ make up
$ make web-shell
(container)$ ./manage.py migrate
(container)$ ./manage.py createsuperuser
Username (leave blank to use 'root'): admin
Email address: admin@email.com
Password: ***** (admin)
Password (again): ***** (admin)
```

## Get upload link

There has to be a user on the database with that login to request an
upload link.

```bash
$ http --auth admin:admin :8000/api/v1/upload_link expire_at=2019-08-22
HTTP/1.1 200 OK
...

"/api/v1/upload/vh65CYbvw0ILnKoF"
```

## Upload images

This token can only be used by the owner.

```bash
$ http --auth admin:admin -f PUT :8000/api/v1/upload/vh65CYbvw0ILnKoF images@data/me.jpg images@data/lena.png
HTTP/1.1 201 Created
...

[
    18,
    19
]
```

## Retrieve an image

It is rendereable by a browser or directly on a web application.

Anybody can retrieve an image from the system.

```bash
$ http :8000/api/v1/19
HTTP/1.1 200 OK
Content-Type: image/PNG
...

+-----------------------------------------+
| binary data                             |
+-----------------------------------------+
```

## Statistics

```bash
$ http --auth admin:admin :8000/api/v1/statistics
HTTP/1.1 200 OK
...

{
    "common_formats": [
        {
            "count": 4,
            "meta__format": "JPEG"
        },
        {
            "count": 3,
            "meta__format": "PNG"
        }
    ],
    "common_models": [
        {
            "count": 15,
            "meta__Model": "TOSHIBA Web Camera - HD: TOSHIB"
        }
    ],
    "uploaded_freq_per_day": 0.7
}
```

## Token authentication

You can request your token authentication using

```bash
$ http :8000/api-token-auth/ username=admin password=admin
HTTP/1.1 200 OK
...

{
    "token": "28dcfe0efde275793262a1e82e01f15fd49a1102"
}
```

And then remove the `--auth` parameter by a header parameter. For example when
uploading an image:

```bash
$ http -f PUT :8000/api/v1/upload/vh65CYbvw0ILnKoF "Authorization: Token 28dcfe0efde275793262a1e82e01f15fd49a1102" images@data/me.jpg images@data/lena.png
HTTP/1.1 201 Created
...

[
    20,
    21
]
```
