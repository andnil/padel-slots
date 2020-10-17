from padel import Padel

from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/padel/',  methods=['POST'])
def respond():
    padel = Padel()
    result = padel.get_free_slots()
    print(result)
    return jsonify(result)



if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)