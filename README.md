# django_tutorial

### this project was followed by this tutorial as the base, then i've updated it
`https://docs.djangoproject.com/en/4.1/intro/install/`

### In this tutorial, we will learn the first step to django

### For db, we use sqlite

### First of all, you need to run this command to create environment for this project

`cd project_name`

`python3 -m venv venv`

`source venv/bin/activate`

`pip install -r requirements.txt`

### Now, you are good to go
### Other information i've comment in the code
### Try to read it to know how to use this api project

# Knowledge i've used in this project:

----------

### Model handling
### Please check in this file:
`store/models.py`

----------

### Query handling
### Please check in this file:
`store/views.py`

----------

### Insert data to database by import CSV
### Please check in this file:
`store/migrations/0005_auto_20230222_0915.py`
### Note: for file csv, we use [https://www.mockaroo.com/]() to generate dummy csv  file

----------

### Insert data to database by using library "faker"
### Please check in this file:
`store/migrations/0006_auto_20230222_1706.py`
`store/migrations/0007_auto_20230223_0944.py`

----------

### Debug by using "django debug toolbar"
### Follow by this instruction:
[https://www.tutorialspoint.com/how-to-add-django-debug-toolbar-to-your-project]()
### Note: This debug can help us show what's the sql query that we used
### But it only work if we use the "templates" and debug in UI
### It doesn't work when we just return some text without using "templates"
### such as 'return HttpResponse("Hello, you are in the sample page.")'

----------