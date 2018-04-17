import json

from bson import json_util
from flask import Flask

from src.ws.facades.shootings_facade import ShootingsFacade

app = Flask(__name__)


@app.route('/ws/v1/shootings')
def read_shootings_data():
    optimized_array = ShootingsFacade().build_array()
    return json.dumps(optimized_array, default=json_util.default)
