import keyboard
import pyautogui
import time
import os
from threading import Lock, Thread
global space_bar_screenshots
global key_down_screenshots
global user_id

########################################## START Config ############################################
DEBUG = True
# DEBUG = False

user = 'vignesh'
# user = 'niranjana'
# user = 'prakash'
########################################## END Config ############################################

if user == 'vignesh':
	user_id = 1
elif user == 'niranjana':
	user_id = 2
elif user == 'prakash':
	user_id = 3

current_directory = os.getcwd()

directory_jump = os.path.join(current_directory, 'raw_data', 'jump')
directory_duck = os.path.join(current_directory, 'raw_data', 'duck')
directory_inaction = os.path.join(current_directory, 'raw_data', 'inaction')

directory_cleaned_jump = os.path.join(current_directory, 'cleaned_data', 'jump')
directory_cleaned_duck = os.path.join(current_directory, 'cleaned_data', 'duck')
directory_cleaned_inaction = os.path.join(current_directory, 'cleaned_data', 'inaction')

mutex = Lock()


def process_space_bar():
	mutex.acquire()
	global space_bar_screenshots
	print("space_bar") if DEBUG else None
	space_bar_screenshots.append(pyautogui.screenshot())
	time.sleep(0.5)
	mutex.release()


def process_key_down():
	global key_down_screenshots
	print("key_down") if DEBUG else None
	key_down_screenshots.append(pyautogui.screenshot())


def process_inaction():
	print("inaction") if DEBUG else None
	save_single_screenshot(pyautogui.screenshot(), directory_inaction)


def save_single_screenshot(screenshot, directory):
	file_id = str(time.time())
	file_id = "{}_{}_{}".format(user_id, file_id.split(".")[0], file_id.split(".")[1])
	file_name = os.path.join(directory, '{}.jpg'.format(file_id))
	screenshot.save(file_name)


def save_all_screenshots():
	print("Saving all screenshots...")
	print("---")

	for screenshot in space_bar_screenshots:
		save_single_screenshot(screenshot, directory_jump)

	for screenshot in key_down_screenshots:
		save_single_screenshot(screenshot, directory_duck)


def create_necessary_folders():
	print("Creating necessary folders...")
	print("---")

	# create necessary data folders
	os.makedirs(directory_jump) if not os.path.exists(directory_jump) else None
	os.makedirs(directory_duck) if not os.path.exists(directory_duck) else None
	os.makedirs(directory_inaction) if not os.path.exists(directory_inaction) else None

	os.makedirs(directory_cleaned_jump) if not os.path.exists(directory_cleaned_jump) else None
	os.makedirs(directory_cleaned_duck) if not os.path.exists(directory_cleaned_duck) else None
	os.makedirs(directory_cleaned_inaction) if not os.path.exists(directory_cleaned_inaction) else None


def capture_jump_duck():
	# Keyboard waiting for input...
	print("Waiting for keyboard input...")
	keyboard.wait()


def capture_inaction():
	while True:
		mutex.acquire()
		process_inaction()
		mutex.release()
		time.sleep(1)


def main():
	print("Running data collection script...")
	print("---")
	create_necessary_folders()

	# initialize arrays for screenshots
	global space_bar_screenshots, key_down_screenshots
	space_bar_screenshots = []
	key_down_screenshots = []

	# assign function for each key press
	keyboard.add_hotkey('space', lambda: process_space_bar())
	keyboard.add_hotkey(keyboard.KEY_UP, lambda: process_space_bar())
	keyboard.add_hotkey(keyboard.KEY_DOWN, lambda: process_key_down())

	p1 = Thread(target=capture_jump_duck)
	p1.start()
	p2 = Thread(target=capture_inaction)
	p2.start()
	p1.join()
	p2.join()


if __name__ == '__main__':
	try:
		main()
	finally:
		save_all_screenshots()
