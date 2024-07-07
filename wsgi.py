import sys
path='/home/user/mylist'
if path not in sys.path:
    sys.path.append(path)
from app import app as application