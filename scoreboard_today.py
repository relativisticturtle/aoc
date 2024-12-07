import os
import sys
import json
import requests
from datetime import datetime as dt
from datetime import timezone as tz



def _download_leaderboard(year, leaderboard_id):
    url = 'https://adventofcode.com/{}/leaderboard/private/view/{}.json'.format(year, leaderboard_id)
    session_file = os.path.join(os.path.dirname(__file__), 'session.txt')
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


def get_leaderboard(year=None, leaderboard_id='4232372', cache_timeout=900):
    if year is None:
        year = dt.now().year

    # Check if cached recently
    leaderboard = None
    leaderboard_file = os.path.join(os.path.dirname(__file__), str(year), 'leaderboard.json')
    if os.path.isfile(leaderboard_file):
        timestamp = os.path.getmtime(leaderboard_file)
        if (dt.now() - dt.fromtimestamp(timestamp)).seconds < cache_timeout:
            print('Reading local \'%s\'...' % leaderboard_file)
            with open('{}\\leaderboard.json'.format(year), encoding='utf-8') as fp:
                leaderboard = json.load(fp)

    # Not cached recently. Download
    if leaderboard is None:
        raw_text = _download_leaderboard(year, leaderboard_id)
        leaderboard = json.loads(raw_text)
        with open('{}\\leaderboard.json'.format(year), 'w', encoding='utf-8') as fp:
            fp.write(raw_text)

    return leaderboard


def leaderboard_to_table(leaderboard, day=None):
    if day is None:
        day = dt.now().day

    # Problem opens at 05:00:00 UTC
    year = int(leaderboard['event'])
    problem_start = dt(year, 12, int(day), 5, tzinfo=tz.utc)

    results = []
    for member in leaderboard['members'].values():
        results.append([member['name']])
        for star in ['1', '2']:
            try:
                ts = member['completion_day_level'][str(day)][star]['get_star_ts']
                problem_solved = dt.fromtimestamp(int(ts), tz=tz.utc)
                results[-1].append(problem_solved - problem_start)
            except KeyError:
                results[-1].append(None)
        results[-1].append(member['local_score'])
    results.sort(key=lambda x: x[-1], reverse=True)

    star_podium = tuple(
        tuple(a[0] for a in sorted(results, key=lambda x: (x[s] or 1e12) if x[s] is None else x[s].seconds)[:3])
        for s in [1, 2]
    )

    for member in leaderboard['members'].values():
        if member['global_score'] > 0:
            print('\n\nGLOBAL SCORE by {}: {}\n\n'.format(member['name'], member['global_score']))

    return results, star_podium


def verbose(time):
    if time is None:
        return ''
    elif time.seconds > 24 * 60 * 60:
        return '> 1 day'
    elif time.seconds > 60 * 60:
        return '{:2d}h {:2d}min {:2d}s'.format(
            time.seconds // 3600,
            (time.seconds % 3600) // 60,
            time.seconds % 60
        )
    else:
        return '{:2d}min {:2d}s'.format(
            (time.seconds % 3600) // 60,
            time.seconds % 60
        )


if __name__ == '__main__':
    if len(sys.argv) > 1:
        day = sys.argv[1]
    else:
        day = None
    
    leaderboard, star_podium = leaderboard_to_table(get_leaderboard(), day)

    for name, star1, star2, local_score in leaderboard:
        if star1 is None:
            continue
        medal = [
            '[{}]'.format(podium.index(name) + 1) if name in podium else ''
            for podium in star_podium
        ]
        print('{:4d}   {:<30s}{:>20s}{:>4s}{:>20s}{:>4s}'.format(
            local_score,
            name,
            verbose(star1),
            medal[0],
            verbose(star2),
            medal[1],
        ))

    print('')