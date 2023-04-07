"""Main Application"""
# pylint: disable=all
from http import HTTPStatus
from flask import Flask, jsonify, render_template
from app import limiter, route
from app import Main, route
from errors import ValidationError
from werkzeug.exceptions import HTTPException
from env import environ

HOST = environ.get("HOST", "127.0.0.1")
PORT = int(environ.get("PORT", 5000))
app = Flask(__name__)
limiter.init_app(app)
route.init_app(app)


@app.errorhandler(ValidationError)
def handle_validationerror(exc: ValidationError):
    return jsonify({
        "message": str(exc),
        "status": 'error'
    }), 400


@app.errorhandler(Exception)
def handle_main(exc: Exception):
    return jsonify({
        "message": f"Internal Server Error. {str(exc)}",
        "status": "error"
    })


@app.errorhandler(HTTPException)
def handle_others(exc: HTTPException):
    return render_template('error.html', name=exc.name, value=exc.get_description())


@app.route("/")
def root():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route('/u/<binded>')
def urls(binded: str):
    return Main.show(binded)


if __name__ == '__main__':
    app.run(HOST, PORT, debug=True)
