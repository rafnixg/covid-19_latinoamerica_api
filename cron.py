"""Job for update data.csv file."""
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from etl import etl


sched = BackgroundScheduler()


@sched.scheduled_job('interval', minutes=60)
def update_data():
    """Function to update dataset."""
    print("[INFO] Updating data")
    data = etl()
    data.to_csv('data.csv', index=False)
    print(f"[INFO] Data has been updated on {datetime.now}.")


sched.start()
