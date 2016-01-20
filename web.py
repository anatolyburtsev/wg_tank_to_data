from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory, send_file, url_for
from flask import abort
import time
import wg_api
import tank
import sql_api

app = Flask(__name__)


@app.route("/old_style")
def tanks_and_ids():
    tanks = wg_api.get_tanks_and_ids()
    api_version = wg_api.get_api_version()
    return render_template("tanks_and_ids.html", wg_api_version=api_version, tanks_data=tanks)


@app.route("/")
def tanks_by_nation():
    # tanks_raw = wg_api.get_raw_vehicle()
    api_version = wg_api.get_api_version()
    t = sql_api.TanksDB(api_version)
    return render_template("tanks_by_nation.html", wg_api_version=api_version, ussr_tanks_data=t.ussr(), usa_tanks_data=t.usa(),
                           uk_tanks_data=t.uk(), germany_tanks_data=t.germany(), china_tanks_data=t.china(),
                           japan_tanks_data=t.japan())


@app.route("/tanks_data/<tank_id>")
def tanks_data(tank_id):
    assert str(tank_id).isdigit()
    t = tank.Tank(tank_id)
    t.fetch_info()
    t.parse_info()
    return str(t).replace("\n", "<br/>")


if __name__ == "__main__":
    # app.debug
    app.run(host='0.0.0.0', port=8000)
