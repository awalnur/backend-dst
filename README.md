## BE AGRI CHICKEN HEALTH
## prerequisites
  - docker
  - postgres
## Running locally in development mode
### cloning the repository
To get started, you must clone the repository by running the following command:

    git clone https://github.com/awalnur/backend-dst.git
    cd backend-dst

### configure database server
To get started, you must have a postgres database running. You can either run a local postgres server or use a docker container. To run a postgres server using docker, you can run the following command:

    docker run --name postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres

This will start a postgres server running on port 5432 with the username `postgres` and password `postgres`. You can then create a database called `be-sistem-pakar` by running the following command:

    docker exec -it postgres psql -U postgres -c "CREATE DATABASE be-sistem-pakar"

after creating the database please import sql file in `database` folder to the database
    
    docker exec -i postgres psql -U postgres -d be-sistem-pakar < database/backup.sql

### Running the backend server

To run backend server of this project, you must update the `env/.env_devel` file with the correct database credentials
to run the backend server, you can run the following command:

    docker compose up --build -d
