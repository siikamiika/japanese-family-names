#!/usr/bin/env python3
import os
import sys
import csv
from bs4 import BeautifulSoup as BS

INFO_DIR = 'name_info'

FALLBACK = {
    '米内山': 'よないやま',
}

HIRAGANA_START = 0x3041
HIRAGANA_END = 0x3096

def is_hiragana(word):
    for c in word:
        o = ord(c)
        if o < HIRAGANA_START or o > HIRAGANA_END:
            return False
    return True

def get_names(filename):
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        return [tuple(row) for row in reader]

def get_info(name):
    if name in FALLBACK:
        return FALLBACK[name], 0.0

    info_files = os.listdir(INFO_DIR)
    for file in info_files:
        if file.split('.')[0] == name:
            with open(os.path.join(INFO_DIR, file), encoding='utf-8') as f:
                soup = BS(f.read(), 'html5lib')

            paragraphs = soup.find_all('p')

            # Readings
            readings = paragraphs[0]
            if not readings.find('a'):
                raise Exception('Unexpected format: {}'.format(file))
            readings = [r.strip() for r in readings.find(text=True).split('、')]
            for r in readings:
                if not is_hiragana(r):
                    raise Exception('Unexpected format: {}\nUnexpected reading: {}'.format(file, r))

            # Nandokudo
            nandokudo = paragraphs[2]
            if not nandokudo.text.startswith('難読度：'):
                raise Exception('Unexpected format: {}'.format(file))
            nandokudo = float(nandokudo.text[4:].strip())

            return readings, nandokudo

    raise Exception('Name info not found: {}'.format(name))

def main():
    names = get_names(sys.argv[1])
    with open(sys.argv[2], 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for name in names:
            info = get_info(name[0])
            writer.writerow([
                name[0],            # name
                '|'.join(info[0]),  # reading
                name[1],            # number of people who have this name
                info[1],            # 難読度 from kanji.reader.bz
            ])

if __name__ == '__main__':
    main()
