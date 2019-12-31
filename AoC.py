# coding: utf-8

import appex
from aoc_utils import download_input
from importlib import import_module, reload
from datetime import datetime


def main():
	if not appex.is_running_extension():
		print('This script is intended to be run from the sharing extension.')
		return
		
	# Highest priority: selected text > "Share..."
	text = appex.get_text()
	
	# 2nd priority: web page url > "Û"
	if not text:
		text = download_input(url=appex.get_url())
	if not text:
		print('No text input found.')
		return
	
	# Run code against today's code
	day = 1     # datetime.now().day
	year = 2019 # datetime.now().year
	today_code = import_module("%d.day%02d" % (year, day))
	reload(today_code)
	today_code.run(text)
	

if __name__ == '__main__':
	main()

