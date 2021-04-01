import os
import pandas as pd
import time
import schedule
import speedtest
from datetime import datetime


def check_internet(file="internet.xlsx"):
    try:
        if not os.path.exists(file):
            writer = pd.ExcelWriter(file)
            pd.DataFrame({'Date': [], 'Time': [], 'Speed': []}).to_excel(writer, 'base', index=False)
            writer.save()
            print("Excel file created!")
        df = pd.read_excel(file)
        s = speedtest.Speedtest()
        current_date = datetime.now().strftime('%d/%m/%Y')
        current_time = datetime.now().strftime('%H:%M')
        speed = s.download(threads=None)*(10**-6)
        df.loc[len(df)] = {'Date': current_date, 'Time': current_time, 'Speed': speed}
        print("Log: ", df.loc[len(df)-1])
        df.to_excel(
            file,
            sheet_name='base',
            index=False
        )
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # Task scheduling
    # After every 1 min is called.
    schedule.every(1).minutes.do(check_internet)
    # Loop so that the scheduling task
    # keeps on running all time.
    while True:
        # Checks whether a scheduled task
        # is pending to run or not
        schedule.run_pending()
        time.sleep(1)
