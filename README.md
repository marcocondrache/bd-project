# Kepler Shop

This project uses conda as an environment, pip for python packages and invoke to run tasks

## Boot up

**From the root of the project**

Create and activate a new environment:

```sh
conda env create -f environment.yaml && conda activate kepler-shop
```

Build the Postgres database and apply the migrations:

```sh
docker-compose up -d
invoke migrate
```

Create a .env file in the root of the project with the following content:

```dotenv
DB_HOST=localhost:5432
DB_NAME=kepler_db
DB_USER=[username]
DB_PASS=[password]

SECRET_KEY=[secret_key]
```

Run the server:

```sh
$ invoke setup dev
```

## Migrations
If you have made changes to the models, you need to generate the migrations and apply them to the database. To do this, run the following commands:

```sh
flask db migrate -m "<migration message>"
invoke migrate
```

The first command generates the migration file,
and the second applies the migration to the database.
To apply the migration to the database, 
you need to have the database running and the database env variables set.
