# Flask Python Project - To Do List with Autentication System

## Free Python Hosting

- [pythonanywhere by Anaconda](https://www.pythonanywhere.com)

## Tutorial Video (not mine)

- [Making To Do List](https://www.youtube.com/watch?v=45P3xQPaYxc)
- [Authentication System](https://www.youtube.com/watch?v=Fr2MxT9M0V4)

## My Website

- [http://yourlist.pythonanywhere.com](https://yourlist.pythonanywhere.com)

## Installation on PythonAnywhere
1. Make account or login
2. Open consoles tab and open bash
- create virtual environment
  ```cli
  mkvirtualenv myvirtualenv --python=/usr/bin/python3.10
  ```
- clone this repository
  ```cli
  git clone https://github.com/AMRIZH/todolist.git
  ```
- open the app directory
  ```cli
  cd todolist
  ```
- install all requirements
  ```cli
  pip install -r requirements.txt
  ```
3. open WEB tab
- add a new web app (choose manual configuration, python 3.10)
- scroll below and add the source code 
  ```path
  home/username/todolist
  ```
- modify wsgi configuration file.<br>
  clear all existing code (ctr+A, delete)<br>
  replace with this code
  ```python
  import sys
  path='/home/username/todolist'
  if path not in sys.path:
      sys.path.append(path)
  from app import app as application
  ```
- add virtual env path
  ```path
  /home/username/.virtualenvs/myvirtualenv
  ```
- scroll to top and reload username.pythonanywhere.com
- Run Your Website

Note : change the 'username' with your pythonanywhere username.
