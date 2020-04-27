
from datetime import date, datetime
from json import dumps, loads
from os import stat
from re import search


def tsprint(message, end='\n'):
    ts = str(datetime.now().strftime('%Y %m %d %H:%M:%S'))
    print('%s %s' % (ts, message), end=end)

def file_size(path):
    return stat(path).st_size

def get_days_old(now, parsed_date):
    d = date(*parsed_date[:3])
    published = datetime.combine(d, datetime.min.time())
    return (now - published).days

def simplify_bytes(bytes, suffix='B'):
    for unit in ('','K','M','G','T','P','E','Z'):
        if abs(bytes) < 1024.0:
            return "%3.1f%s%s" % (bytes, unit, suffix)
        bytes /= 1024.0
    return "%.1f%s%s" % (bytes, 'Y', suffix)

class DataHandler:
    def __init__(self, output_path):
        self.data = {}
        self.has_changed = False
        self.just_created = False
        self.output_path = output_path


    def read_data(self):
        try:
            with open(self.output_path, 'r') as file:
                self.data = loads(file.read())
            fsize = simplify_bytes(file_size(self.output_path))
            tsprint('read %s from %s' % (fsize, self.output_path))
            tsprint('got %s entries from %s' % (len(self.get_all_entries()), self.output_path))
        except FileNotFoundError:
            self.just_created = True
            tsprint('%s not found. Creating...' % self.output_path)
            with open(self.output_path, 'w') as file:
                file.write('{}')


    def write_data(self):
        if not self.has_changed:
            tsprint('data has not changed, skipping writing to file...')
            return
        tsprint('writing data to %s' % self.output_path)
        with open(self.output_path, 'w') as file:
            file.write(dumps(self.data))
        fsize = simplify_bytes(file_size(self.output_path))
        tsprint('wrote %s to %s' % (fsize, self.output_path))


    def entry_exists(self, id_):
        for url, entries in self.data.items():
            if id_ in entries.keys(): return True
        return False


    def add_entry(self, url, entry_id, entry):
        self.has_changed = True
        if url not in self.data: self.data[url] = {}
        self.data[url][entry_id] = entry


    def remove_old_entries(self, days):
        if self.just_created: return
        tsprint('removing entries older than %s days' % days)
        now = datetime.now()
        removed = 0
        to_remove = {}
        for url, entries in self.data.items():
            if url not in to_remove: to_remove[url] = []
            for id_, entry in entries.items():
                if get_days_old(now, entry['published_parsed']) >= days:
                    to_remove[url].append(id_)
        for url, ids in to_remove.items():
            for id_ in ids:
                del self.data[url][id_]
                removed += 1
        if removed > 0: self.has_changed = True
        tsprint('removed %s entries' % removed)
        tsprint('%s entries total' % len(self.get_all_entries()))


    def get_all_entries(self):
        entries = []
        for url, entries_ in self.data.items():
            for entry_id in entries_:
                entries.append(entries_[entry_id])
        return entries

