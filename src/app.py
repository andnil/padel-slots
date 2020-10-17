from padel import Padel

from flask import Flask, request, jsonify
app = Flask(__name__)


@app.route('/padel/',  methods=['POST'])
def respond():
    padel = Padel()
    result = padel.get_free_slots()

    text = 'Lediga tider\n\n'
    for date in result:
        for slot in result[date]:
            text += f'*{slot["start_date"]} {slot["start_time"]}* - {slot["name"]} Pris: {slot["price"]}\n'


    view_dict = {
        'text': text
    }

    return jsonify(view_dict)


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True)
