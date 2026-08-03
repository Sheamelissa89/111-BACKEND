from flask import Flask, jsonify, request
import sqlite3


app = Flask(__name__) # Instance of Flask


@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "OK"
                    }), 200


if __name__ == "__main__":
    app.run(debug=True)