## BE AGRI CHICKEN HEALTH
## prerequisites
  - docker
  - postgres
## Running locally in development mode

To get started, you must have a postgres database running. You can either run a local postgres server or use a docker container. To run a postgres server using docker, you can run the following command:

    docker run --name postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres

This will start a postgres server running on port 5432 with the username `postgres` and password `postgres`. You can then create a database called `be-sistem-pakar` by running the following command:

    docker exec -it postgres psql -U postgres -c "CREATE DATABASE be-sistem-pakar"

To run backend server of this project, just clone this repository and run the following commands:
    
    git clone https://github.com/awalnur/backend-dst.git
    cd backend-dst

after cloning the repository, you must update the `env/.env_devel` file with the correct database credentials 
to run the backend server, you can run the following command:

    docker compose up --build -d
