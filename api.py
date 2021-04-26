import os
from datetime import datetime
from flask import Flask
from flask_restful import Api, request
from sqlalchemy import create_engine
from flask_cors import CORS

# Database connection
db_connect = None
# Create Flask API objects
app = Flask(__name__)
api = Api(app)
cors = CORS(app)


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
        return {"error": err}


@app.route('/speed/<from_date>', methods=['GET'])
def date(from_date):
    if not isinstance(from_date, str):
        return {"error": "Date is not valid"}
    try:
        ts = datetime.strptime(from_date, '%d.%m.%Y')
    except ValueError:
        return {"error": "Incorrect data format, should be DD.MM.YYYY"}
    sql = "select * from speed where datetime(ts,'unixepoch') BETWEEN '{} 00:00:00' AND '{} 23:59:59'".format(
        ts.date(), ts.date())
    conn = db_connect.connect()
    query = conn.execute(sql)
    values = [{"ts": t[0], "download": t[1], "upload": t[2]} for t in query.cursor.fetchall()]
    return {"speed": values}


@app.route('/speed/<from_date>,<to_date>', methods=['GET'])
def date(from_date):
    if not isinstance(from_date, str):
        return {"error": "From date is not valid"}
    if not isinstance(from_date, str):
        return {"error": "To date is not valid"}
    try:
        from_ts = datetime.strptime(from_date, '%d.%m.%Y')
        to_ts = datetime.strptime(from_date, '%d.%m.%Y')
    except ValueError:
        return {"error": "Incorrect data format, should be DD.MM.YYYY"}
    sql = "select * from speed where datetime(ts,'unixepoch') BETWEEN '{} 00:00:00' AND '{} 23:59:59'".format(
        from_ts.date(), to_ts.date())
    conn = db_connect.connect()
    query = conn.execute(sql)
    values = [{"ts": t[0], "download": t[1], "upload": t[2]} for t in query.cursor.fetchall()]
    return {"speed": values}


@app.route('/speed/add', methods=['POST'])
def add():
    ts = request.args.get('ts', type=float)
    download = request.args.get('download', type=float)
    upload = request.args.get('upload', type=float)
    if ts is None or ts is not None and not isinstance(ts, float):
        return {"error": "Field timestamp is required"}
    if download is None or download is not None and not isinstance(download, float):
        return {"error": "Field download is required"}
    if upload is None or upload is not None and not isinstance(upload, float):
        return {"error": "Field upload is required"}
    try:
        conn = db_connect.connect()
        query = conn.execute("INSERT INTO speed (ts, download, upload) VALUES ({},{},{})".format(
            ts, download, upload
        ))
    except Exception as err:
        return {"error": err}
    if query.rowcount == 0:
        return {"message": "Nothing happened :("}
    return {"success": "{}".format(query.rowcount)}


@app.route('/speed/avg', methods=['GET'])
def avg():
    try:
        conn = db_connect.connect()
        query = conn.execute("select AVG(download) as 'download', AVG(upload) as 'upload' from speed")
        values = [{"download": t[0], "upload": t[1]} for t in query.cursor.fetchall()]
        return {"average": values}
    except Exception as err:
        return {"error": err}


if __name__ == '__main__':
    try:
        # Creates the flask API
        print("Connecting to database")
        db_connect = create_engine('sqlite:///internet.db')
        print("API active")
        app.run(host='0.0.0.0', port=port)
    except Exception as e:
        print(e)
