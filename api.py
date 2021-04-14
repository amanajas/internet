import os
from flask import Flask
from flask_restful import Api
from sqlalchemy import create_engine


# Creating database
db_connect = create_engine('sqlite:///internet.db')
# Create Flask API objects
app = Flask(__name__)
api = Api(app)

# Get port
port = int(os.environ.get("PORT", 5000))


@app.route('/speed', methods=['GET'])
def get():
    try:
        conn = db_connect.connect()
        query = conn.execute("select ts, download, upload from speed")
        if query.rowcount > 0:
            ts, download, upload = [(t, d, u) for t, d, u in query.cursor.fetchall()]
            return {
                'ts': ts,
                'download': download,
                'upload': upload
            }
    except Exception as err:
        print({"error": err})
    return {}


if __name__ == '__main__':
    # Creates the flask API
    app.run(host='0.0.0.0', port=port)
    print("API active...")