#!/usr/bin/env python3
import sys
import csv
from bs4 import BeautifulSoup as BS

REPLACEMENTS = {
    'ケ': 'ヶ',
}

def normalize(text):
    output = []
    for c in text:
        output.append(REPLACEMENTS.get(c) or c)
    return ''.join(output)

def main():
    input_filename = sys.argv[1]
    with open(input_filename, 'r', encoding='shift-jis') as f:
        soup = BS(f.read(), 'html5lib')

    tables = soup.find('table', {'width': '500'}).find_all('table')

    data = []
    for table in tables:
        for row in table.find_all('tr')[1:]:
            row = row.find_all('td')
            data.append((
                #int(row[0].get_text()),
                normalize(row[1].get_text()),
                int(row[2].get_text()),
            ))

    print(data)
    print(len(data))

    output_filename = '{}.csv'.format(sys.argv[1])
    print('Writing to {}...'.format(output_filename))

    with open(output_filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for d in data:
            writer.writerow(d)

if __name__ == '__main__':
    main()
