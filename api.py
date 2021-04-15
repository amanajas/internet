import json
import os
from flask import Flask
from flask_restful import Api
from sqlalchemy import create_engine

# Database connection
db_connect = None
# Create Flask API objects
app = Flask(__name__)
api = Api(app)

# Get port
port = int(os.environ.get("PORT", 5000))


@app.route('/', methods=['GET'])
def home():
    return {"message": "Everything running :)"}


@app.route('/speed', methods=['GET'])
def get():
    try:
        conn = db_connect.connect()
        query = conn.execute("select ts, download, upload from speed")
        values = [{"ts": t[0], "download": t[1], "upload": t[2]} for t in query.cursor.fetchall()]
        return {"speed": values}
    except Exception as err:
        print({"error": err})


if __name__ == '__main__':
    try:
        # Creates the flask API
        print("Connecting to database")
        db_connect = create_engine('sqlite:///internet.db')
        print("API active")
        app.run(host='0.0.0.0', port=port)
    except Exception as e:
        print(e)
