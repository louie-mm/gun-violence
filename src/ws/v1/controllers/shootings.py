import json

from bson import json_util
from flask import Flask

from src.ws.facades.shootings_facade import ShootingsFacade

app = Flask(__name__)


@app.route('/ws/v1/shootings')
def read_shootings_data():
    response_body = ShootingsFacade().build_optimized_array()
    return json.dumps(response_body, default=json_util.default)
