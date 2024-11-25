## .env 파일 생성
* .env_example을 .env로 변경
* cp .env_example .env

## DB generation (alembic)
* alembic init migrations
* alembic revision --autogenerate
* alembic upgrade head

## Docker Container 생성
* docker build -t myapi . 
* docker run --name myapi-container -dit -p 8000:8000 -v $(pwd) myapi
* docker ps -a

## Container (myapi-container)
* docker attach CONTAINER_NAME
* docker exec -it CONTAINER_NAME /bin/bash
### Run FastAPI Backend
* uvicorn main:app --reload --host 0.0.0.0
### Run Svelte Frontend
* npm run dev

