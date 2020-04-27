
from data_handler import DataHandler


handler = DataHandler()
handler.read_data()

publishes = []

for entry in handler.get_all_entries():
    publishes.append(entry['published'])

print('\nPublish dates for entries are:')

for date in publishes:
    print('    %s' % date)

print('\n%s total entries.' % len(publishes))
