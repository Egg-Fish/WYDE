from flask import Flask, render_template, send_file, request, make_response

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"


if __name__ == "__main__":
    app.run(
        host="localhost",
        port=8080,
        debug=True
    )