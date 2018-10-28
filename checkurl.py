import sys, datetime, time, urllib2

DEFAULT_INPUT_FILENAME = 'urls.txt'

TIMEOUT = 10 # seconds
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.'

is_valid_url = lambda url: url.startswith('http://') or url.startswith('https://')


def get_input():
    input = sys.argv[1:]
    return DEFAULT_INPUT_FILENAME if len(input) == 0 else input[0]


def read_input_file(fpath):
    lines = None
    with open(fpath) as f:
        lines = [line.strip() for line in f.readlines()]
    fn = lambda s: s and s[0] != '#'
    lines = filter(fn, lines)
    return lines


def format_log_line(info, is_error=False):
    ts = datetime.time().strftime('%H:%M:%S')
    status = 'ERROR! ' if is_error else ''
    return '%s %s%s' % (ts, status, info)


def print_log_line(info, is_error=False, log_path=None, error_path=None):
    line = format_log_line(info, is_error)
    print(line)
    if log_path:
        with open(log_path, 'a') as f1:
            f1.write(line + '\n')
    if is_error and error_path:
        with open(error_path, 'a') as f2:
            f2.write(line + '\n')


def get_url_opener():
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', USER_AGENT)]
    return opener



def check_url(opener, url):
    ret = None
    try:
        res = opener.open(url, timeout=TIMEOUT)
    except urllib2.HTTPError as e:
        ret = e.code
    return ret

def build_output_filename(prefix='log'):
    ds = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    return '%s-%s.txt' % (prefix, ds)


def run_task(input_path, log_path, error_path):
    entries = read_input_file(input_path)
    if not entries or not len(entries):
        print_log_line('No input URLs provided')
        return
    opener = None
    print_log_line('%s input URLs in %s' % (len(entries), input_path))
    for url in entries:
        if is_valid_url(url):
            if opener is None:
                opener = get_url_opener()
            result = check_url(opener, url)
            if result is None:
                print_log_line('%s -- OK' % url, False, log_path)
            else:
                print_log_line('response code %s from %s' % (result, url), True, log_path, error_path)
        else:
            print_log_line('invalid URL: %s' % url, True, log_path, error_path)
    print_log_line('Done!')


fn_input = get_input()
fn_log = build_output_filename()
fn_error = build_output_filename('errorlog')

try:
    run_task(fn_input, fn_log, fn_error)
except Exception as e:
    print_log_line(e, True, fn_log, fn_error)