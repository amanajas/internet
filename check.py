import os
import pandas as pd
import time
import schedule
import speedtest
from datetime import datetime


def check_internet(file="internet.xlsx"):
    if not os.path.exists(file):
        writer = pd.ExcelWriter(file)
        pd.DataFrame({'Date': [], 'Time': [], 'Download': [], 'Upload': []}).to_excel(writer, 'base', index=False)
        writer.save()
        print("Excel file created!")
    df = pd.read_excel(file)
    s = speedtest.Speedtest()
    current_date = datetime.now().strftime('%d/%m/%Y')
    current_time = datetime.now().strftime('%H:%M')
    download = s.download()
    upload = s.upload()
    df.loc[len(df)] = {'Date': current_date, 'Time': current_time, 'Download': download, 'Upload': upload}
    print("Log: ", df.loc[len(df) - 1])
    df.to_excel(
        file,
        sheet_name='base',
        index=False
    )


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
