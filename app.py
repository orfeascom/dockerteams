from flask import Flask, request, jsonify
from stationStatus import zabbixGetHost
import re

app = Flask(__name__)

@app.route('/')
def hello_geek():
    return '<h1>Hello from Flask & Docker</h2>'


@app.route('/api/teams/moh/status', methods=['POST'])
def teams_webhook():
    message = request.json['text']
    station = re.sub("[^0-9]", "", message)

    if (len(station) == 3):
        siteName = "coral-" + station
        result = zabbixGetHost(siteName)
    elif (len(station) == 4 and station[0] == "8"):
        siteName = "coral-inno-8101-gw"
        result = zabbixGetHost(siteName)
    elif (len(station) == 4 and (station[0] == "4" or station[0] == "6")):
        siteName = "GW" + station
        result = zabbixGetHost(siteName)
    else:
        result = "Please provide a valid gas station..."
    test = {
        "type": "message",
        "text": result
    }
    return jsonify(test)


if __name__ == "__main__":
    app.run(debug=True)