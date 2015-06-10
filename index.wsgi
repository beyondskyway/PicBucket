import sae


import os
import sys
root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(root, 'site-packages'))

from myapp import app




application = sae.create_wsgi_app(app)
