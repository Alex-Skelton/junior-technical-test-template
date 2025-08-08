# Midnite - Take Home Technical Test

## Introduction  

This project consists of a Flask based API server that runs on port `5000`.
The application includes a `Makefile`, testing is handled 
with `pytest`, and dependency management is done via [Poetry](https://python-poetry.org/docs/).

Instructions for installation, running the server, and running tests are included below.

## Approach and Assumptions 

### Challenges
The most significant challenge revolved around the conditional checks that required additional historical user data.
In a real world scenario, this would most likely be resolved with retrieval of data through: 
- API calls to a service managing the database connection
- direct connection to a database 
- through a message queue e.g. Kafka

To simulate the data retrival, the current implementation mocks historical user data.
- during runtime: fake user data is randomly generated.
- during tests: historical data is predefined and injected via mocks.

### Assumptions
Some assumptions were made regarding how conditional checks should behave. In a real work scenario I would typically verify this
logic with a product owner / stakeholder.

### Future improvements

- Enable logging to be used in internal service modules. e.g. `user_service.py` and `user_database.py`
- Add data validation for the historical user data retrival
- Containerise the application (e.g., Docker) for easier deployment.

### Additional test to consider
- sending `/event` invalid data types: e.g. int instead of string, or misspelled type strings `depossit`
- sending zeroes and negative values
- triggering multiple conditional codes within a single api call
- sending requests with no JSON body
- any other edge case scenarios encountered with future development / bugs

## Getting started

### Requirements

- Python 3.12
- [Poetry](https://python-poetry.org/docs/) for dependency management

### Install dependencies

```sh
poetry install
```

### Start API server

```sh
make run
```

### Run tests

```sh
make test
```

## Testing

```sh
curl -XPOST 'http://127.0.0.1:5000/event' -H 'Content-Type: application/json' \
-d '{
"type": "deposit",
"amount": "112.00",
"user_id": 1,
"time": 1000
}'
```