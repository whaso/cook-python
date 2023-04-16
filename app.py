from flask import Flask

app = Flask(__name__)


@app.route("/test", methods=["GET", "POST"])
def test():
    from flask import request
    print(request.headers)
    return {"ok": "0k"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")