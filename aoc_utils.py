import os
import requests
from datetime import datetime

# Getting session-cookie using Chrome:
# - Navigate to Advent of Code and login
# - Right-click > "Inspect" > "Application"-tab
# - "Storage" > "Session Storage" > "Cookies" > https://adventofcode.com
# - ...and "Session"-key! Copy&paste here --v
cookies = {
	"session": "53616c7465645f5fa6b9c6e6be138d55b4fc1f22418b3a9833c1405021c3767efa6e7f3e2850fcc6346818a62106a03b"
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
