import os
import inspect
import requests
from datetime import datetime
from dateutil import tz


def _download_input(day, year):
    url = 'https://adventofcode.com/{}/day/{}/input'.format(year, day)
    session_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'session.txt')
    # https://www.reddit.com/r/adventofcode/comments/z9dhtd/please_include_your_contact_info_in_the_useragent/
    user_agent = 'github.com/relativisticturtle/aoc by mxrten@gmail.com'
    
    if not os.path.isfile(session_file):
        raise FileNotFoundError('Missing \'session.txt\' (read in README.md how to obtain)')
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


def get_input(day=None, year=None, test=None, silent=False):
    if year is None:
        year = os.path.basename(os.path.dirname(inspect.stack()[1].filename))

    if day is None:
        day = int(os.path.basename(inspect.stack()[1].filename)[3:5])

    year_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), str(year))
    if test is not None:
        filename = os.path.join(year_folder, 'input%02d_%s.txt' % (day, test))
        if not silent:
            print('Reading test-file \'%s\'...' % filename)
        with open(filename) as f:
            data = f.read()
        if not silent:
            print('Done!')
        return data

    # Cache input to avoid unnecessary server-load
    filename = os.path.join(year_folder, 'input%02d.txt' % day)
    if os.path.isfile(filename):
        if not silent:
            print('Reading local \'%s\'...' % filename)
        with open(filename) as f:
            data = f.read()
        if not silent:
            print('Done!')
    else:
        print('No local file.')

        # Check we are not trying to get problem too early
        unlocks_at = datetime(int(year), 12, int(day), tzinfo=tz.gettz('UTC-5'))
        now_EST = datetime.now(tz.gettz('UTC-5'))
        if now_EST < unlocks_at:
             raise RuntimeError('Problem hasn\'t been unlocked yet!')

        # Download
        data = _download_input(day, year)

        # Check server didn't give stern reply
        please_dont = 'Please don\'t repeatedly request this endpoint before it unlocks!'
        if data.startswith(please_dont):
             raise RuntimeError(please_dont)

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
