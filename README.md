# STARS

Requirements:
Python needs to be installed

Build Steps (for Windows):

Download the source code from the repository into a directory of your choice:
`git clone https://github.com/Wael653/Project-sksy`

Create a new virtual environment by running:
```
python -m venv env
```

Activate your virtual environment:
```
env\Scripts\activate.bat
```

Install django in the virtual environment:
```
pip install django
```

Install psycopg2 in the virtual environment (for DB):
```
pip install psycopg2
```

Create a Superuser for Administration: 
```
python manage.py createsuperuser
```
Now from the directory where you stored the repo locally, start the app:
```
python manage.py runserver
```
Open a browser and point it to http://127.0.0.1:8000/

Or for Administration point it to: http://127.0.0.1:8000/admin

To import the given example data, run the following command:
```
python manage.py loaddata initialData.json
```

## Hints for Developers:

### The database system of PostgreSQL is used:
- Install PostgreSQL
- Create a User named starsuser with the Password `stars123` and a Database named `starsdb`
- Connect starsuser and starsdb

### Changing something on the models:
- Change your models (in models.py)
- Run the following command to create migrations for those changes
```
python manage.py makemigrations
```
- Run following command to apply those changes to the database
```
python manage.py migrate
```


# If you switch your branch to a branch with a different model file, be sure to follow these steps:
- Run this command while being in the old branch
```
python manage.py migrate starsApp zero
```
- Switch branch
- Run the following command to create migrations for those changes
```
python manage.py migrate
```

<details><summary><h3>If the models are still not properly created try the following steps:</h3></summary>
<p>

- Run 
```
python manage.py migrate starsApp zero
```
- delete the 0001_initial.py file in the migrations folder
- Run the following command to create migrations for those changes
```
python manage.py makemigrations
```
- Run following command to apply those changes to the database
```
python manage.py migrate
```
  </p>
 </details>
<details><summary><h3>If all of this is not helping, try the following steps as well:</h3></summary>
<p>
- Run your PostgreSQL admin tool and delete all tables starting with `starsApp` manually

- delete the 0001_initial.py file in the migrations folder
- Run the following command to create migrations for those changes
```
python manage.py makemigrations
```
- Run following command to apply those changes to the database
```
python manage.py migrate
```
</p>
 </details>




## Used Apps:
`star_ratings`, an app to create star rating fields more easily -> `https://django-star-ratings.readthedocs.io/en/latest/`
run `pip install django-star-ratings` to install, further installation hints can be found at the link
