# Flask Python Project - To Do List with Autentication System

## Free Pyhton Hosting

- [python anywhere by anaconda](https://www.pythonanywhere.com)

## Tutorial Video (not mine)

- [making to do list](https://www.youtube.com/watch?v=45P3xQPaYxc)
- [authentication](https://www.youtube.com/watch?v=Fr2MxT9M0V4)

## My Website

- [http://yourlist.pythonanywhere.com](http://yourlist.pythonanywhere.com)

## installation on PythonAnywhere
1. make account or login
2. open consoles tab and bash
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
3. open WEB tab and add a new web app (choose manual configuration, python 3.10)
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
- Your Website is ready

Note : change the 'username' with your pythonanywhere username.
