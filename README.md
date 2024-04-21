This project uses conda as an environment, pip for python packages and invoke to run tasks

To create and activate a new environment, use the following commands:

```sh
$ cd bd-project
$ conda env create -f environment.yaml && conda activate kepler-shop
```

To migrate the database and run the server, use the following command:

```sh
$ invoke migrate
```

Create a .env file in the root of the project with the following content:

```dotenv
DB_HOST=localhost:5432
DB_NAME=kepler_db
DB_USER=[username]
DB_PASS=[password]

SECRET_KEY=[secret_key]
```

To run the server, use the following command:

```sh
$ invoke setup dev
```

# Migrations
If you have made changes to the models, you need to generate the migrations and apply them to the database. To do this, run the following commands:

```sh
$ flask db migrate -m "<migration message>"
$ invoke migrate
```

The first command generates the migration file,
and the second applies the migration to the database.
To apply the migration to the database, 
you need to have the database running and the database env variables set.
