from flask import Flask, request, render_template, redirect, url_for, jsonify
import json

app = Flask(__name__)
application = app


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        return redirect(url_for("local"))
    return render_template("index.html")


@app.route("/local", methods=["GET"])
def local():
    return render_template("local.html")


@app.route("/response", methods=["GET"])
def response():
    # Page to return local information
    data = {
        "message": "Form submitted successfully",
        "status": "200",
        "data": [
            {
                "state": 17,
                "fips": 17031,
                "zip": 60615,
                "obligation": "$1,000 ",
                "paid": "$1,000 ",
                "cut": "$10 ",
                "desc": "Medicaid",
            },
            {
                "state": 17,
                "fips": 17031,
                "zip": 60615,
                "obligation": "$100 ",
                "paid": "$90 ",
                "cut": "$0 ",
                "desc": "SNAP",
            },
        ],
    }
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
