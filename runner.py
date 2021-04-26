import time
import schedule
import speedtest
from datetime import datetime
from sqlalchemy import create_engine, MetaData, Table, Column, Numeric


# Creating database
db_connect = create_engine('sqlite:///internet.db')
# Creating table
meta = MetaData()
students = Table(
   'speed', meta,
   Column('ts', Numeric, primary_key=True),
   Column('download', Numeric),
   Column('upload', Numeric),
)
meta.create_all(db_connect)


def check_internet():
    the_moment = datetime.utcnow()
    ts = the_moment.timestamp()
    log_time = the_moment.strftime('%d/%m/%Y %H:%M')
    try:
        s = speedtest.Speedtest()
        download = s.download() / 1024 / 1024
        upload = s.upload() / 1024 / 1024
        conn = db_connect.connect()
        conn.execute("INSERT INTO speed (ts,download,upload) VALUES ({},{},{})".format(
            ts, download, upload))
        print("Success: ",
              log_time,
              "|",
              "(D)", download,
              "(U)", upload,
              "()", )
    except Exception as e:
        print("Error:", "(", log_time, ")", e)


if __name__ == '__main__':
    # Task scheduling
    # After every 1 min is called.
    print("Scheduling...")
    schedule.every(1).minutes.do(check_internet)
    print("done.")
    # Creates the flask API
    # Loop so that the scheduling task
    # keeps on running all time.
    try:
        while True:
            # Checks whether a scheduled task
            # is pending to run or not
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exit by pressing CTRL+C")
    except Exception as err:
        print(err)
