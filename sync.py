from apscheduler.schedulers.blocking import BlockingScheduler
from server.sync import sync_blocks
from server.sync import sync_peers

background = BlockingScheduler()
background.add_job(sync_blocks, "interval", seconds=5)
background.add_job(sync_peers, "interval", minutes=1)
background.start()
