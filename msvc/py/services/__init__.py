# -- Load library --
from flask import Flask
import os, sys
import configuration
import os.path as osp

# -- Init Flask object --
app = Flask(__name__, static_url_path='')

# -- Set configuration --
app.config.from_object(configuration.ProductionConfig)

# -- Set system path
for path in app.config['MODULE_DIRS']:
	sys.path.append(path) 


def main():
	import route
	port = int(os.getenv("PORT", 5000))
	app.run(host='0.0.0.0', port=port, threaded=True)