# shindan-cli

[![Test](
  <https://github.com/eggplants/shindan-cli/actions/workflows/test.yml/badge.svg>
)](
  <https://github.com/eggplants/shindan-cli/actions/workflows/test.yml>
) [![Release Package](
  <https://github.com/eggplants/shindan-cli/actions/workflows/release.yml/badge.svg>
)](
  <https://github.com/eggplants/shindan-cli/actions/workflows/release.yml>
) [![PyPI](
    <https://img.shields.io/pypi/v/shindan-cli?color=blue>
)](
  <https://pypi.org/project/shindan-cli>
) [![PyPI - Python Version](
    <https://img.shields.io/pypi/pyversions/shindan-cli>
  )](
  <https://pypi.org/project/shindan-cli>
)

[![Maintainability](
  <https://qlty.sh/badges/9e2de2a6-51c0-4797-bc60-da4a2ff28737/maintainability.svg>
  )](
  <https://qlty.sh/gh/eggplants/projects/shindan-cli>
) [![Code Coverage](
  <https://qlty.sh/badges/9e2de2a6-51c0-4797-bc60-da4a2ff28737/test_coverage.svg>
  )](
  <https://qlty.sh/gh/eggplants/projects/shindan-cli>
)

ShindanMaker (診断メーカー, <https://shindanmaker.com>) CLI + Library

## Install

```bash
pip install shindan-cli
```

## Usage

Supported types of diagnosis:

- [Name-based diagnosis (名前診断)](https://shindanmaker.com/list/name)
- [Branching diagnosis (分岐診断)](https://shindanmaker.com/list/branch)
- [AI diagnosis (AI診断)](https://shindanmaker.com/list/ai)
- [Check Diagnosis (チェック診断)](https://shindanmaker.com/list/check)

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
    - Library (Unmaintained)
- Go
  - [kakakaya/goshindan](https://github.com/kakakaya/goshindan)
    - Library + CLI (Archived)
    - <https://pkg.go.dev/github.com/kakakaya/goshindan>
- Java
  - [shibafu528/shindan4j](https://github.com/shibafu528/shindan4j)
    - Library (Unmaintained)
    - <https://jitpack.io/#shibafu528/shindan4j>
- JavaScript
  - [asawo/shindan-scraper](https://github.com/asawo/shindan-scraper)
    - Library (Unmaintained)
  - [stawberri/shindan](https://github.com/stawberri/shindan)
    - Library (Archived)
    - <https://www.npmjs.com/package/shindan>
- Perl
  - [Likk/WebService-ShindanMaker](https://github.com/Likk/WebService-ShindanMaker)
    - Library (Unmaintained)
- PHP
  - [moroya/php-shindanmaker](https://github.com/moroya/php-shindanmaker)
    - Library (Unmaintained)
    - <https://packagist.org/packages/moroya/php-shindanmaker>
- Python
  - [Le96/auto_shindanmaker](https://github.com/Le96/auto_shindanmaker)
    - Bot Server (Unmaintained)
  - [tanitanin/shindan-python](https://github.com/tanitanin/shindan-python)
    - CLI (Unmaintained)
- Ruby
  - [osak/shindanmaker](https://github.com/osak/shindanmaker)
    - [Mikutter](https://github.com/mikutter/mikutter) Plugin (Unmaintained)
  - [gouf/shindan](https://github.com/gouf/shindan)
    - Library (Unmaintained)
  - [ikaruga777/shindan-cli](https://github.com/ikaruga777/shindan-cli)
    - CLI (Unmaintained)
  - [yasuhito/shindan](https://github.com/yasuhito/shindan)
    - CLI (Unmaintained)
    - <https://rubygems.org/gems/shindan>
- TypeScript
  - [dqn/shindanmaker-js](https://github.com/dqn/shindanmaker-js)
    - Library (Archived)
