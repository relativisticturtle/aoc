import os
import requests
from datetime import datetime

# Get session cookie with, e.g., chrome extension
cookies = {
		"session": "53616c7465645f5ffa162416b46bd27d39696733057615740075f40710a0cad3c10822b7110841dc276d4b02f6896a70"
	}

def download_input(day=None, year=None, url=None):
	if not url:
		day = day if day else datetime.now().day
		year = year if year else datetime.now().year
		url = "https://adventofcode.com/%d/day/%d/input" % (year, day)
	
	try:
		print("Downloading...")
		read = requests.get(url, cookies=cookies)
		data = [chunk for chunk in read.iter_content(chunk_size=512)]
		data = b"".join(data).decode()
		print("Done!")
		return data
	except requests.RequestException as e:
		print("Error :%s" % e)
		return None


def get_input(day=None, year=None):
	filename = "input%02d.txt" % day
	if os.path.isfile(filename):
		print("Reading local '%s'..." % filename)
		with open(filename) as f:
			data = f.read()
		print("Done!")
	else:
		print("No local file.")
		data = download_input(day, year)
		if not data:
			return None
		print("Storing locally as '%s'..." % filename)
		with open(filename, "w") as f:
			f.write(data)
		print("Done!")
	return data


def clipboard_set(text):
	try:
		import clipboard
		if hasattr(clipboard, "set"):
			clipboard.set(text)
		elif hasattr(clipboard, "copy"):
			clipboard.copy(text)
		else:
			print("Warning: couldn't copy to clipboard")
	except ImportError:
		print("Warning: no clipboard module")


if __name__ == "__main__":
	data = get_input(1)
	print("---- 1 ----")
	print(data)
