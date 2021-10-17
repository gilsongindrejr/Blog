# Blog

Blog app made with django 3 following the awesome book Django 3 by Example from Antonio Melé.
The app is translated to pt_BR and es using po files.

# Running backend server

#### Clone this repository
```
$ git clone <https://github.com/gilsongindrejr/Blog.git>
```

#### Access the project folder
```
$ cd Blog
```

#### Activate the virtual enviroment
```
$ source venv/bin/activate
```

#### Install requirements
```
$ pip install -r requirements.txt
```

#### Migrate the database
```
$ python manage.py migrate
```

#### Run server
```
$ python manage.py runserver
```

#### The server will be initiated on port 8000 - access <http://127.0.0.1:8000> 

# Testing

The tests was made using pytest.


#### Run tests and show coverage
```
$ pytest --cov
```

#### Run tests and create coverage html page
```
$ pytest --cov --cov-report=html
```

Access htmlcov folder
```
$ cd htmlcov/
```

Run python http server
```
$ python -m http.server
```

Access the server on <http://127.0.0.1:8000> 
