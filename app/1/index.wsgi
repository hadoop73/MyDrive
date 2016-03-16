import sae
sae.add_vendor_dir('vendor')
from main.views import app

application = sae.create_wsgi_app(app)