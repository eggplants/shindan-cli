# shindan-cli

[![Release Package](
  <https://github.com/eggplants/shindan-cli/actions/workflows/release.yml/badge.svg>
)](
  <https://github.com/eggplants/shindan-cli/actions/workflows/release.yml>
) [![PyPI](
    <https://img.shields.io/pypi/v/shindan-cli?color=blue>
  ) ![PyPI - Python Version](
    <https://img.shields.io/pypi/pyversions/shindan-cli>
  )
](
  <https://pypi.org/project/shindan-cli>
)

[![Test](
  <https://github.com/eggplants/shindan-cli/actions/workflows/test.yml/badge.svg>
)](
  <https://github.com/eggplants/shindan-cli/actions/workflows/test.yml>
) [![Maintainability](
  <https://api.codeclimate.com/v1/badges/9134b56a4241e91dfa01/maintainability>
)](
  <https://codeclimate.com/github/eggplants/shindan-cli/maintainability>
) [![Test Coverage](
  <https://api.codeclimate.com/v1/badges/9134b56a4241e91dfa01/test_coverage>
)](
  <https://codeclimate.com/github/eggplants/shindan-cli/test_coverage>
)

ShindanMaker (<https://shindanmaker.com>) CLI

## Install

```bash
pip install shindan-cli
```

## Usage

### CLI

```shellsession
$ shindan -h
usage: shindan [-h] [-w] [-H] [-l] [-V] ID NAME

ShindanMaker (https://shindanmaker.com) CLI

positional arguments:
  ID             shindan page id
  NAME           shindan name

optional arguments:
  -h, --help     show this help message and exit
  -w, --wait     insert random wait
  -H, --hashtag  add hashtag `#shindanmaker`
  -l, --link     add link to last of output
  -V, --version  show program's version number and exit

$ shindan 1036646 hoge
ねこって、むしだ。

𝙐𝙉𝙄𝙌𝙇𝙊

$ shindan 1036646 huga -l
ねこって、むしだ。

𝙉𝙄𝙎𝙎𝙄𝙉
https://shindanmaker.com/1036646

$ shindan 1036646 huga -l -H
ねこって、むしだ。

𝙁𝙐𝙅𝙄𝙏𝙎𝙐
#shindanmaker
https://shindanmaker.com/1036646
```

### Library

```python
from shindan_cli import shindan
# type: (int, str, optional[bool]) -> ShindanResults
shindan(1036646, 'hoge', wait=False)
```

Returns:

```python
{
  'results': ['ねこって、むしだ。', '', '𝙏𝙊𝙆𝙔𝙊 𝙈𝙀𝙏𝙍𝙊'],
  'hashtags': ['#shindanmaker'],
  'shindan_url': 'https://shindanmaker.com/1036646'
}
```

## License

MIT

---

## Similar Imprementations

- C#
  - [misodengaku/ShindanMaker](https://github.com/misodengaku/ShindanMaker)
    - Library
- Go
  - [kakakaya/goshindan](https://github.com/kakakaya/goshindan)
    - Library + CLI
    - <https://pkg.go.dev/github.com/kakakaya/goshindan>
- Java
  - [shibafu528/shindan4j](https://github.com/shibafu528/shindan4j)
    - Library
    - <https://jitpack.io/#shibafu528/shindan4j>
- JavaScript
  - [asawo/shindan-scraper](https://github.com/asawo/shindan-scraper)
    - Library
  - [stawberri/shindan](https://github.com/stawberri/shindan)
    - Library (Archived)
    - <https://www.npmjs.com/package/shindan>
- Perl
  - [Likk/WebService-ShindanMaker](https://github.com/Likk/WebService-ShindanMaker)
    - Library
- PHP
  - [moroya/php-shindanmaker](https://github.com/moroya/php-shindanmaker)
    - Library
    - <https://packagist.org/packages/moroya/php-shindanmaker>
- Python
  - [Le96/auto_shindanmaker](https://github.com/Le96/auto_shindanmaker)
    - Bot Server
  - [tanitanin/shindan-python](https://github.com/tanitanin/shindan-python)
    - CLI (Script)
- Ruby
  - [osak/shindanmaker](https://github.com/osak/shindanmaker)
    - [Mikutter](https://github.com/mikutter/mikutter) Plugin
  - [gouf/shindan](https://github.com/gouf/shindan)
    - Library
  - [ikaruga777/shindan-cli](https://github.com/ikaruga777/shindan-cli)
    - CLI
  - [yasuhito/shindan](https://github.com/yasuhito/shindan)
    - CLI
    - <https://rubygems.org/gems/shindan>
- TypeScript
  - [dqn/shindanmaker-js](https://github.com/dqn/shindanmaker-js)
    - Library
