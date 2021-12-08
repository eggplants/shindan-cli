# shindan-cli

[![PyPI]](https://pypi.org/project/shindan-cli
) [![PyPI - Python Version]](https://pypi.org/project/shindan-cli
)

[![Release Package]](https://github.com/eggplants/shindan-cli/actions/workflows/release.yml
) [![Maintainability]](https://codeclimate.com/github/eggplants/shindan-cli/maintainability
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
usage: shindan [-h] [-w] [-V] ID NAME

ShindanMaker (https://shindanmaker.com) CLI

positional arguments:
  ID             shindan page id
  NAME           shindan name

optional arguments:
  -h, --help     show this help message and exit
  -w, --wait     take random wait
  -V, --version  show program's version number and exit

$ shindan 1036646 hoge
ねこって、むしだ。

𝙐𝙉𝙄𝙌𝙇𝙊
```

### Library

```python
from shindan_cli import shindan
# type: (int, str, optional[bool]) -> str
shindan.shindan(1036646, 'hoge', wait=False)
#=>'ねこって、むしだ。\n\n𝙐𝙉𝙄𝙌𝙇𝙊'
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

[Release Package]: https://github.com/eggplants/shindan-cli/actions/workflows/release.yml/badge.svg
[PyPI]: https://img.shields.io/pypi/v/shindan-cli?color=blue
[PyPI - Python Version]: https://img.shields.io/pypi/pyversions/shindan-cli
[Maintainability]: https://api.codeclimate.com/v1/badges/9134b56a4241e91dfa01/maintainability
