import os
import time
from picamera2 import Picamera2
from libcamera import Transform, controls
from datetime import datetime
from config import config

def create_log(string: str):
	i = datetime.now()
	time = i.strftime('[%d-%m-%Y %H:%M:%S]')

	with open('log.txt', 'a') as log_file:
		log_file.write(f'{time} {string}\n')

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
	create_log('Adding annotation to picture')
	os.system(os_command)

def run_loop():
	base = config["base_path"]
	pause = config["delay"]
	am = config["am"]
	pm = config["pm"]

	picam2 = Picamera2()
	picam2.options["quality"] = config["quality"]

	camera_config = picam2.create_still_configuration(
		main={"size": (config["width"], config["height"])},
		transform=Transform(hflip=config["flip_horizontal"], vflip=config["flip_vertical"]),
		display=None
	)

	picam2.configure(camera_config)
	picam2.start()
	try:
		picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
	except Exception:
		create_log(f'set_contols not supported (older camera).')
	time.sleep(2)

	create_log(f'Shots will be taken between {am} AM and {pm} PM')

	while True:
		time_now = int(time.strftime('%H%M'))

		if time_now > am and time_now < pm:
			now = datetime.now()
			path = prepare_dir(base, now)

			name = f'{time_now}.jpg'
			create_log(f'Capturing {name}')

			file_name = f'{base}/{path}/{name}'
			picam2.capture_file(file_name)
			create_log(f'Written: {file_name}')

			if config["enable_annotation"]:
				annotate(file_name)
		else:
			create_log(f'Shot cancelled during hours of darkness time: {time_now}')
		
		create_log(f'Pausing {pause} seconds')
		time.sleep(pause)

if __name__ == '__main__':
	try:
		run_loop()
	except KeyboardInterrupt:
		print('Cancelling take.py')
