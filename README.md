# japanese-family-names

Top 5000 Japanese family names ordered by frequency.

## Format

CSV, ordered by frequency, separated with `,`, quoted with `"`.

### `myoji-yurai.csv`

| name (string, kanji) | number of people (integer) |
| -------------------- | -------------------------- |
| 佐藤 | 1894000 |

### `myoji-yurai-readings.csv`

| name (string, kanji) | readings (list of strings separated with "\|", hiragana) | number of people (integer) | 難読度 (float) |
| -------------------- | -------------------------------------------------------- | -------------------------- | ------------- |
| 田中 | たなか\|でんちゅう | 1346000 | 0.98 |

## Legal

### `myoji-yurai.csv` and `myoji-yurai-readings.csv`

Commercial use not allowed. Attribution required. Source: [名字由来net](https://myoji-yurai.net/prefectureRanking.htm).

### Readings and 難読度 in `myoji-yurai-readings.csv`

Scraped from http://kanji.reader.bz/.

`robots.txt` 2017-06-08:

    #User-agent: *
    #Disallow:
    Sitemap: http://kanji.reader.bz/sitemap.xml
