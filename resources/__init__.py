#!/usr/bin/env python3
from .kanjidic2 import Kanjidic2
from .myoji_yurai import Names

kd2 = Kanjidic2('resources/kanjidic2.xml')
def get_kanjidic2(kanji):
    return kd2.get(kanji)

myoji_yurai = Names('myoji-yurai-readings.csv')
