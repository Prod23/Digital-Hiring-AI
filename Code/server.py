from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/send_drive_link', methods=['POST'])
def send_drive_link():
    if 'drive_link' not in request.form:
        return jsonify({"message": "Drive link not provided."}), 400

    drive_link = request.form['drive_link']
    return jsonify({"drive_link": drive_link})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)



