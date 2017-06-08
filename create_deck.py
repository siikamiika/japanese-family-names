#!/usr/bin/env python3
import argparse
import string
import csv
from resources import get_kanjidic2, myoji_yurai

POPULATION = 127*10**6

CJK_IDEO_START = 0x4e00
CJK_IDEO_END = 0x9faf

def is_kanji(char):
    return CJK_IDEO_START <= ord(char) <= CJK_IDEO_END

class Card(object):
    """Represents a Japanese family name flashcard."""

    with open('flashcard_template/front.html', encoding='utf-8') as f:
        front_template = string.Template(f.read().replace('\n', ''))
    with open('flashcard_template/back.html', encoding='utf-8') as f:
        back_template = string.Template(f.read().replace('\n', ''))

    def __init__(self, name):
        self.name = name
        self.name_info = myoji_yurai.get(self.name)
        self.kanji_info = self._get_kanji_info()

    def get_front(self):
        return Card.front_template.substitute(NAME=self.name)

    def get_back(self):
        name_info = myoji_yurai.get(self.name)
        return Card.back_template.substitute(
            # Most common readings as provided by kanji.reader.bz
            TOP_READINGS='、'.join([self._get_reading_with_aliases_html(r) for r in name_info['readings']]),
            # Frequency information
            RANK='{}.'.format(name_info['rank']),
            PEOPLE='{:,}'.format(name_info['people']),
            OF_ALL='{:.03f}%'.format((name_info['people'] / POPULATION) * 100),
            # kanji information
            KANJI_INFO=''.join([self._get_single_kanji_info_html(info) for info in self.kanji_info]),
        )

    def _get_kanji_info(self):
        output = []
        for c in self.name:
            if not is_kanji(c):
                continue
            output.append(get_kanjidic2(c))
        return output

    def _get_single_kanji_info_html(self, kanji):
        return ''.join([
            '<li>',
            '{}: '.format(kanji['literal']),
            ', '.join(kanji['meaning']),
            '</li>',
        ])

    def _get_reading_with_aliases_html(self, reading):
        aliases = []
        for name in myoji_yurai.names:
            if name is not self.name:
                info = myoji_yurai.get(name)
                if reading in info['readings']:
                    aliases.append((name, info['rank']))
        if not aliases:
            return reading
        return reading + '<span class="normal"> ({})</span>'.format(', '.join([
            '{}<sup>{}</sup>'.format(*a) for a in aliases
        ]))

class Deck(object):
    """Represents a deck of Japanese family name flashcards."""

    def __init__(self, filename):
        self.filename = filename
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def write(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write(''.join([
                '{}\t{}\n'.format(c.get_front(), c.get_back()) for c in self.cards
            ]))

def main():
    deck = Deck(args.output)
    for name in myoji_yurai.names:
        print(name)
        deck.add_card(Card(name))
    print('writing to {}...'.format(args.output))
    deck.write()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # deck filename
    parser.add_argument('--output', '-o')

    args = parser.parse_args()
    if not args.output:
        parser.error('--output required')
    main()
