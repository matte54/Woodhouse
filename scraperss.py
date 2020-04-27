#!/usr/bin/python3

from datetime import datetime
from os import getcwd
from re import search, subn
from sys import argv

from feedparser import parse

from data_handler import DataHandler, get_days_old, tsprint


URLS_PATH = 'urls.txt'
BAD_TAGS_PATH = 'bad_tags.txt'
DAYS_TO_KEEP = 2
VERBOSE = '-v' in argv or '--verbose' in argv
OUTPUT = 'data.json'

for i, arg in enumerate(argv):
    if arg == '-o':
        if len(argv) >= i + 2:
            OUTPUT = argv[i + 1]
        else:
            print('output path must come after -o option')
            exit(-1)

def vprint(message):
    if not VERBOSE: return
    tsprint('verbose: %s' % message)

def get_file_items(filename):
    vprint('getting items from %s...' % filename)
    try:
        with open(filename, 'r') as file:
            items = [item for item in file.read().split('\n') if item and not item.startswith('#')]
            vprint('items: %s' % items)
            return items
    except Exception as e:
        tsprint('unable to read file %s: %s' %s (filename, error.__name__))
        exit(-1)

BAD_TAGS = get_file_items(BAD_TAGS_PATH)

def is_new(parsed_date):
    return get_days_old(datetime.now(), parsed_date) < DAYS_TO_KEEP

def good_tag(tag):
    if not tag or len(tag) < 3: return False
    return tag not in BAD_TAGS

def clean_unique_tags(tags):
    new_tags = []
    for tag in tags:
        tag = tag.replace('-', ' ')
        words = subn(r'[^\w ]', '', tag.lower())[0].split()
        new_tags += [word for word in words if good_tag(word) and word not in new_tags]
    return new_tags

def clean_entry(entry, tags, **kwargs):
    published = None
    if 'published_parsed' in entry:
        published = entry['published_parsed']
    elif 'updated_parsed' in entry:
        published = entry['updated_parsed']
    else: return
    d = {
        'link': entry['link'],
        'published_parsed': published,
        'tags': tags
    }
    for key, val in kwargs.items():
        d[key] = val
    return d

def scrape():
    vprint('working from %s' % getcwd())
    handler = DataHandler(OUTPUT)
    handler.read_data()
    handler.remove_old_entries(DAYS_TO_KEEP)
    added, per_url = 0, 0
    for url in get_file_items(URLS_PATH):
        vprint('requesting feed from %s...' % url)
        feed = parse(url)
        if not feed or 'status' not in feed:
            tsprint('error: unable to reach target url. aborting.')
            exit(-1)
        status = feed['status']
        if status != 200:
            tsprint('error: request from %s responded with error code %s. skipping...' % (url, status))
            continue
        vprint('status returned normal. scanning entries...')
        for entry in feed['entries']:
            try:
                id_ = entry['id']
                published = None
                if 'published_parsed' in entry:
                    published = entry['published_parsed']
                elif 'updated_parsed' in entry:
                    published = entry['updated_parsed']
                else:
                    print('entries may not have dates. skipping...')
                    break
                if not is_new(published) or handler.entry_exists(id_):
                    continue
                tags = []
                if 'www.reddit.com' in url or 'tags' not in entry or not entry['tags']:
                    tags = clean_unique_tags([entry['title']])
                    if per_url == 0:
                        vprint('no tags for entries, using title instead:\n  %s' % tags)
                else:
                    tags = clean_unique_tags([tag['term'] for tag in entry['tags']])
                if not tags: continue
                extras = {}
                if 'www.reddit.com' in url and 'summary' in entry:
                    m = search(r'href="(\S+)">\[link\]', entry['summary'])
                    if m: extras = {"dlink": m.group(1)}
                handler.add_entry(url, id_, clean_entry(entry, tags, **extras))
                added += 1
                per_url += 1
            except KeyError as e:
                print('%s\nskipping...' % e)
                per_url = 0
                break
        vprint('got %s entries from %s' % (per_url, url))
        per_url = 0
    handler.write_data()
    tsprint('added %s new entries' % added)
    tsprint('%s entries total' % len(handler.get_all_entries()))

tsprint('starting scrape...')
scrape()
tsprint('done.\n')

