This project uses conda as enviroment, pip for python packages and invoke to run tasks

To create and activate a new enviroment use the following commands:

```sh
$ cd bd-project
$ conda env create -f environment.yaml && conda activate kepler-shop
$ invoke setup dev
```

# Migrations
If you have made changes to the models, you need to generate the migrations and apply them to the database. To do this, run the following commands:

```sh
$ flask db migrate -m "<migration message>"
$ invoke migrate
```

The first command generates the migration file and the second applies the migration to the database.
In order to apply the migration to the database, you need to have the database running and the database env variables set.
