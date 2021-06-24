# pip install -r requirements.txt
from flask import Flask, render_template, url_for, request, flash
import crypto_module

app = Flask(__name__)
app.config['SECRET_KEY'] = "123kjliuhliguikuhguyrtuyykuytuyfytrytikutgjuyhhu65546"


menu = [{'name': "MAIN PAGE", "url": "index"},
        {'name': "ENCODE", 'url': 'encode'},
        {'name': "DECODE", 'url': 'decode'},
        {'name': "HELP", 'url': 'help'},]


@app.route("/index")
@app.route("/")
def main_page():
    return render_template("index.html", menu=menu)


@app.route("/encode", methods=['POST', 'GET'])
def encode_page():
    if request.method == "POST":
        text = request.form['message']
        print(text)

        if len(text) > 1:
            flash(f'timestamp and encrypted string: {str(crypto_module.encrypt_func(text))}', category='success')
            flash("To decrypt the message later you must remember the timestamp", category='success')
        else:
            flash("You have entered nothing", category='error')

    return render_template("encode.html", title="Encode the ASCII text ", menu=menu)


@app.route("/decode", methods=['POST', 'GET'])
def decode_page():
    if request.method == "POST":
        text = request.form['timestamp']
        print(text)

        if len(text) > 1:
            flash(f'decrypted text: {crypto_module.decrypt_func(text)}', category='success')
        else:
            flash("You have entered nothing", category='error')

    return render_template("decode.html", title="Decode the ASCII text ", menu=menu)


@app.route("/help")
def help_page():

    return render_template('help.html', title="HELP information", menu=menu)


if __name__ == '__main__':
    app.run(debug=True)