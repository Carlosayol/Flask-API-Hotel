# Flask-API-Hotel

This project is a small API for managing hotel entities.

<br>This code was written with Python, using Flask and MongoDB

## Repository overview

```
├── README.md
├── README.md
├── .gitignore
├── main.py
├── requirements.txt
├── Pipfile
├── Pipfile.lock
├── src
│   ├── routes
|   │   └── hotel.py
│   ├── models
|   │   ├── hotel.py
|   │   └── pyObjectId.py
│   ├── functions.py
│   ├── database.py
│   └── app.py
└── tests
    ├── conftest.py
    └── test_endpoints.py

```

## How to run

- Clone the project
- Install the requirements with pipenv
- Run mongodb with hotel db
- Run main.py

## Endpoints

Resource: Hotel

**POST** 
```
endpoint: 
     {{host}}/api/v1/hotels 
body:
    {
        "name": string
        "city": string
        "address": string
        "contact_email": string
        "image_url": string
    }
```

**GET** 
```
endpoint:
     {{host}}/api/v1/hotels
endpoint: 
     {{host}}/api/v1/hotels?city=Bogota
endpoint: 
     {{host}}/api/v1/hotels/<id>
```       

**PUT**
```
endpoint:
    {{host}}/api/v1/hotels
body:
     {
         "_id": string
         "name": string
         "city": string
         "address": string
         "contact_email": string
         "image_url": string
     }
```

**DELETE**
```
endpoint:
    {{host}}/api/v1/hotels/<id>
```
