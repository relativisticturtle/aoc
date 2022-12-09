import os
import requests
from datetime import datetime

# Getting session-cookie using Chrome:
# - Navigate to Advent of Code and login
# - Right-click > "Inspect" > "Application"-tab
# - "Storage" > "Session Storage" > "Cookies" > https://adventofcode.com
# - Copy&paste to session.txt

# Installing virtual environment
# python -m venv --prompt aoc .venv

def _download_input(day, year):
    url = 'https://adventofcode.com/%d/day/%d/input' % (year, day)
    session_file = os.path.join(os.path.dirname(__file__), 'session.txt')
    # https://www.reddit.com/r/adventofcode/comments/z9dhtd/please_include_your_contact_info_in_the_useragent/
    user_agent = 'github.com/relativisticturtle/aoc by mxrten@gmail.com'
    
    if not os.path.isfile(session_file):
        raise FileNotFoundError('Missing \'session.txt\' (read in source-code how to obtain)')
    with open(session_file) as f:
        session = f.readline()

    try:
        print('Downloading...')
        read = requests.get(url, cookies={'session': session}, headers={'User-Agent': user_agent})
        data = [chunk for chunk in read.iter_content(chunk_size=512)]
        data = b''.join(data).decode()
        print('Done!')
        return data
    except requests.RequestException as e:
        print('Error :%s' % e)
        return None


def get_input(day, year, test=None):
    year_folder = os.path.join(os.path.dirname(__file__), str(year))
    if test is not None:
        filename = os.path.join(year_folder, 'input%02d_%s.txt' % (day, test))
        print('Reading test-file \'%s\'...' % filename)
        with open(filename) as f:
            data = f.read()
        print('Done!')
        return data

    # Cache input to avoid unnecessary server-load
    filename = os.path.join(year_folder, 'input%02d.txt' % day)
    if os.path.isfile(filename):
        print('Reading local \'%s\'...' % filename)
        with open(filename) as f:
            data = f.read()
        print('Done!')
    else:
        print('No local file.')
        data = _download_input(day, year)
        if not data:
            return None
        print('Storing locally as \'%s\'...' % filename)
        with open(filename, 'w') as f:
            f.write(data)
        print('Done!')
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
    

if __name__ == '__main__':
    input = get_input(datetime.now().day, datetime.now().year)
    print('----- INPUT (input%02d.txt) -----' % datetime.now().day)
    print(input)
    print('-------------------------------')
