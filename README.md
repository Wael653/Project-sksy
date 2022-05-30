# STARS

Requirements:
Python needs to be installed

Build Steps (for Windows):

Download the source code from the repository into a directory of your choice:
git clone https://github.com/Wael653/Project-sksy

Create a new virtual environment by running:
python -m venv env

Activate your virtual environment:
env\Scripts\activate

Install django in the virtual environment:
pip install django

Now from the directory where you stored the repo locally, start the app:
python manage.py runserver

Open a browser and point it to http://127.0.0.1:8000/

Hints for Developers:

changing something on the models:
• Change your models (in models.py)
• Run python manage.py makemigrations to create migrations for those changes
• Run python manage.py migrate to apply those changes to the database
