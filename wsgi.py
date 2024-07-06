import sys
path='/home/micinlezatoz/todolist'
if path not in sys.path:
    sys.path.append(path)
from app import app as application