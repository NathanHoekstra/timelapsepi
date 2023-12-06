import os
import time
from datetime import datetime
from config import config

def create_log(string):
	i = datetime.now()
	time = i.strftime('[%d-%m-%Y %H:%M:%S]')

	with open('log.txt', 'a') as log_file:
		log_file.write(time + ' ' + string + '\n')

def try_to_mkdir(path):
	if os.path.exists(path) == False:
		os.makedirs(path)

def prepare_dir(base, now):
	path = now.strftime('%d-%m-%Y')
	try_to_mkdir(base + '/' + path)
	return path

def make_os_command(config, file_name):
	height = config['height']
	width = config['width']

	os_command = '/usr/bin/raspistill -q ' + str(config['quality']) + ' '
	if config['flip_horizontal']:
		os_command = os_command + '-hf '
	if config['flip_vertical']:
		os_command = os_command + '-vf '

	os_command = os_command + '-h ' + str(height)+ ' -w ' + str(width) + ' -o ' + file_name
	return os_command

def annotate(file_name):
	i = datetime.now()
	time = i.strftime('%d-%m-%Y %H:%M:%S')

	os_command = '/usr/bin/convert ' + file_name + ' -pointsize 25 -fill white -annotate +1680+1060 ' + repr(time) + ' '
	os_command += '-pointsize 25 -fill white -annotate +10+1060 ' + repr(config['annotation_text']) + ' ' +  file_name
	create_log('Adding annotation to picture')
	os.system(os_command)

def run_loop(base, pause, config):
	am = config['am']
	pm = config['pm']

	create_log('Shots will be taken between {} AM and {} PM'.format(am, pm))

	while True:
		time_now = int(time.strftime('%H%M'))

		if time_now > am and pm > time_now:
			now = datetime.now()
			path = prepare_dir(base, now)

			name = str(time_now) + '.jpg'
			create_log('Capturing {}'.format(name))
			file_name = base + '/' + path + '/' + name

			os_command = make_os_command(config, file_name)
			os.system(os_command)
			create_log('Written: {}'.format(file_name))

			if config['enable_annotation']:
				annotate(file_name)
		else:
			create_log('Shot cancelled during hours of darkness time: {}'.format(time_now))
		
		create_log('Pausing {} seconds'.format(pause))
		time.sleep(pause)

if __name__ == '__main__':
	try:
		pause_interval = config['delay']
		base_path = config['base_path']
		run_loop(base_path, pause_interval, config)
	except KeyboardInterrupt:
		print('Cancelling take.py')
