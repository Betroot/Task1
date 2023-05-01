#!/usr/bin/python3
import sys
import logging
from main import app as application

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/myapp/")
#
# activate_this = "/var/www/Task1/venv/bin/activate_this.py"
# with open(activate_this) as file_:
#     exec(file_.read(), dict(__file__=activate_this))

application.secret_key = 'your_secret_key_here'
