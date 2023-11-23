from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/')
def hello_geek():
    return '<h1>Hello from Flask & Docker</h2>'


@app.route('/api/teams/moh/status', methods=['POST'])
def teams_webhook():
    message = request.json['text']
    message.strip()
    message = message[-5:]
    message.strip()
    if (message[0] == "4" or message[0] == "6"):
        message = "Avin"
    elif (message[0] == "8"):
        message = "Innovation"
    else:
        message = "Coral"
    test = {
        "type": "message",
        "text": "Company: "+ message,
    }
    return jsonify(test)


if __name__ == "__main__":
    app.run(debug=True)