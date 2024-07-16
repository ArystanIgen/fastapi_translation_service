
# Translation Service

![Docker Version](https://img.shields.io/badge/docker-v26.1.1-2496ED.svg?style=for-the-badge&logo=docker)
![Python Version](https://img.shields.io/badge/python-v3.11-blue.svg?style=for-the-badge&logo=python) ![MongoDB](https://img.shields.io/badge/MongoDB-47A248.svg?style=for-the-badge&logo=mongodb&logoColor=white)

---

## Steps to run the application with Docker Compose

1. Make sure you have Docker installed on your machine.
```sh
$ docker version && docker compose version
```

2. Make sure you create Docker network.
```sh
$ make network
```

3. Run Docker Compose
```sh
$ make build
```
---
## 📕 API Documentation

> ❗ This API provides translation services.

### 1. GetWordDetails
#### Request
```http request
GET /v1/words/word-sample HTTP/1.1
Host: fastapi-transaltion-service
```
#### Response
Status: 200 OK
```json
{
  "word": "sample-word",
  "examples": ["example usage of the word"],
  "translations": [
    {
      "translation": "translated-word",
      "synonyms": ["synonym1", "synonym2"]
    }
  ],
  "definitions": [
    {
      "definition": "definition of the word",
      "example": "example usage in definition",
      "synonyms": ["synonym1", "synonym2"]
    }
  ]
}
```

### 2. GetListOfWords
#### Request
```http request
GET /v1/words?sort=-word&include=definitions&include=translations&include=synonyms&size=20&page=1 HTTP/1.1
Host: fastapi-transaltion-service
```
#### Response
Status: 200 OK
```json
{
  "items": [
    {
      "word": "sample-word",
      "examples": ["example usage of the word"],
      "translations": [
        {
          "translation": "translated-word",
          "synonyms": ["synonym1", "synonym2"]
        }
      ],
      "definitions": [
        {
          "definition": "definition of the word",
          "example": "example usage in definition",
          "synonyms": ["synonym1", "synonym2"]
        }
      ]
    }
  ],
  "total": 1,
  "limit": 50,
  "offset": 0
}
```

### 3. DeleteWordDetails
#### Request
```http request
PATCH /v1/words/{word} HTTP/1.1
Host: fastapi-transaltion-service
Content-Type: application/json
```
#### Response
Status: 204 No Content

---
## Tests
To run written tests, run
   ```sh
   make test
   ```
---

## Linters
To run written tests, run
   ```sh
   make lint
   ```
---

## Ports where other applications are running

- MongoDB: http://localhost:27017
- FastApi: http://localhost:8000