import argparse
import logging
import time
import json
import google.cloud.logging
import pathlib
import sys
import signal
from google.oauth2 import service_account
from google.cloud.logging.handlers import CloudLoggingHandler
from google.cloud.logging_v2.handlers import setup_logging

parser = argparse.ArgumentParser(description='Write heartbeat log to google cloud on an interval')
parser.add_argument('service_account_file', type=str, help='path/to/service_account_file.json')
parser.add_argument('--interval', type=int, default=30, help='Write log every interval seconds')
args = parser.parse_args()
service_account_file = args.service_account_file
interval = args.interval

# Unique identifier for this run
RUN_ID = int(time.time())
# Labels to attach to every cloud log
LABELS = {'service': 'surface', 'type': 'heartbeat',  'runId': f'{RUN_ID}'}

# Register google cloud logger
credentials = service_account.Credentials.from_service_account_file(service_account_file)
client = google.cloud.logging.Client(credentials=credentials)
handler = CloudLoggingHandler(client, labels=LABELS)
setup_logging(handler)

# Setup default logger
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# # Log to stdout
# stream_handler = logging.StreamHandler(sys.stdout)
# stream_handler.setFormatter(formatter)
# log.addHandler(stream_handler)

# Log to file
log_dir = pathlib.Path('./logs')
log_dir.mkdir(exist_ok=True)
log_file = log_dir.joinpath(f'run_{RUN_ID}.log')
file_handler = logging.FileHandler(log_file, encoding='utf-8')
file_handler.setFormatter(formatter)
log.addHandler(file_handler)


# Graceful shutdown
def handle_signal(*args, **kwargs):
	log.info('exiting')
	sys.exit(0)

signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTERM, handle_signal)

# Main loop
log.info(f'Started run {RUN_ID}')
try:
	while True:
		time.sleep(interval)
		log.info('hearbeat')
except Exception:
	log.exception('Fatal error')
