# crowd-decision-api
Research project on designing systems for seamless voting / decision-making with minimal human oversight & intervention.


## Running

Download dependencies and set up virtualenv:
```sh
poetry install
poetry shell
```

Run for development 
```sh
uvicorn crowd_decision.main:app --reload
```
or through VSCode Run & Debug (`F5`)


## OpenAPI / Swagger documentation

Automatically generated by FastAPI, found at [localhost:8000/docs](http://localhost:8000/docs)