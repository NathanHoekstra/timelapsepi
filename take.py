import argparse
import os
import logging
from logging.handlers import RotatingFileHandler
import requests
import threading
import time
from picamera2 import Picamera2
from libcamera import Transform, controls
from datetime import datetime, timedelta
from config import config

# Openweather API base_url
base_url = 'https://api.openweathermap.org/data/2.5/weather?'

# complete url address
API_URL = f'{base_url}appid={config["openweather"]["api_key"]}&units=metric&q={config["openweather"]["city"]}'

# Time to make the daily API call (24-hour format)
CALL_HOUR = 4    # 4 AM
CALL_MINUTE = 0  # 0 minutes past the hour

# Offset used for the sunset/sunrise
OFFSET_MINUTES = 40

# Global variables to store the start/end time for taking pictures
am = None
pm = None

def parse_args():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='TimelapsePi')
    parser.add_argument(
        '-d', '--debug', 
        action='store_true', 
        help='Enable debug logging',
		default=False
    )
    
    # Parse arguments
    args = parser.parse_args()
	
    LEVEL = logging.INFO
    # Setup logging level based on the debug parameter
    if args.debug:
        LEVEL = logging.DEBUG

    logging.basicConfig(
        handlers=[
            RotatingFileHandler('./timelapsepi.log', maxBytes=config['logfile']['maxsize'], backupCount=config['logfile']['backupcount'])
        ],
        level=LEVEL,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
	)

def call_api():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            x = response.json()
            logging.debug(f'API call successful: {x}')
            # Check the value of 'cod' key is equal to '404' means city is found,
            # otherwise city is not found
            if x['cod'] != '404':
                global am, pm
                am = (datetime.fromtimestamp(x['sys']['sunrise']) + timedelta(minutes=-OFFSET_MINUTES)).strftime("%H%M")
                pm = (datetime.fromtimestamp(x['sys']['sunset']) + timedelta(minutes=OFFSET_MINUTES)).strftime("%H%M")
                logging.info(f'Shots will be taken between {am} AM and {pm} PM')
                return 0
            else:
                logging.error("The configured city is not found!")
                return 1
        else:
            logging.error(f'API call failed with status code: {response.status_code}')
    except requests.RequestException as e:
        logging.error(f'API call error: {e}')

def time_until_next_call():
    now = datetime.now()
    next_call_time = now.replace(hour=CALL_HOUR, minute=CALL_MINUTE, second=0, microsecond=0)
    
    # If the target time today has already passed, set it for the next day
    if next_call_time <= now:
        next_call_time += timedelta(days=1)
    
    return (next_call_time - now).total_seconds()

def daily_api_call():
    while True:
        # Wait until the next scheduled call time
        wait_time = time_until_next_call()
        logging.info(f'Waiting {wait_time / 3600:.2f} hours until the next API call.')
        time.sleep(wait_time)
        
        # Call the API
        call_api()

def try_to_mkdir(path: str):
	if os.path.exists(path) == False:
		os.makedirs(path)

def prepare_dir(base: str, now: datetime):
	path = now.strftime('%Y.%m.%d')
	try_to_mkdir(f'{base}/{path}')
	return path

def annotate(file_name: str):
	i = datetime.now()
	time = i.strftime('%d-%m-%Y %H:%M:%S')

	os_command = f'/usr/bin/convert {file_name} -pointsize 25 -fill white -annotate +{config["width"] - 240}+{config["height"] - 20} {repr(time)} '
	os_command += f'-pointsize 25 -fill white -annotate +10+{config["height"] - 20} {repr(config["annotation_text"])} {file_name}'
	logging.info('Adding annotation to picture')
	os.system(os_command)

def run_loop():
    base = config['base_path']
    pause = config['delay']
    global am, pm

    if not config['use_openweather']:
        am = config['am']
        pm = config['pm']
        logging.info(f'Shots will be taken between {am} AM and {pm} PM')
    else:
        if not config['openweather']['api_key'] or not config['openweather']['city']:
             logging.error("openweather api_key or city is not set in config!")
             exit(1)
        # Call the API once at startup
        call_api()
        # Start a background thread to call the API daily at the specified time
        thread = threading.Thread(target=daily_api_call)
        thread.daemon = True  # Ensures the thread stops if the main program exits
        thread.start()

    picam2 = Picamera2()
    picam2.options['quality'] = config['quality']

    camera_config = picam2.create_still_configuration(
        main={'size': (config['width'], config['height'])},
        transform=Transform(hflip=config['flip_horizontal'], vflip=config['flip_vertical']),
        display=None
    )

    picam2.configure(camera_config)
    picam2.start()
    try:
        picam2.set_controls({'AfMode': controls.AfModeEnum.Continuous})
    except Exception:
        logging.info(f'set_contols not supported (older camera).')
    # Wait a couple seconds for the camera settings
    time.sleep(2)

    while True:
        time_now = int(time.strftime('%H%M'))

        if time_now > int(am) and time_now < int(pm):
            now = datetime.now()
            path = prepare_dir(base, now)

            name = f'{time_now}.jpg'
            logging.info(f'Capturing {name}')

            file_name = f'{base}/{path}/{name}'
            picam2.capture_file(file_name)
            logging.info(f'Written: {file_name}')

            if config['enable_annotation']:
                annotate(file_name)
        else:
            logging.info(f'Shot cancelled during hours of darkness time: {time_now}')
        
        logging.info(f'Pausing {pause} seconds')
        time.sleep(pause)

if __name__ == '__main__':
	parse_args()
	try:
		run_loop()
	except KeyboardInterrupt:
		print('Stopping take.py')
