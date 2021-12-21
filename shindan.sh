#!/usr/bin/env bash

function _shindan() {
    local url name status source_ inputs ua
    url="https://shindanmaker.com/$1"
    ua="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
    name="$2"
    status="$(
        curl -LI "$url" -o /dev/null -w '%{http_code}' -s -A "$ua"
    )"
    if [ "$status" != "200" ]; then
        echo "error: status code is invalid (${status})">&2
        return 1
    fi
    source_="$(
      curl -s -c cookie.txt "$url" -A "$ua"
    )"
    inputs="$(
        echo -e "$source_" | tr \< \\n | grep input |
        sed -nr '
        s/value=""/value="'"$name"'"/
        s/^.* name="([^"]+)".* value="([^"]+)">$/\1=\2/g
        4,6p' | tr \\n \& | sed 's/.$//'
    )"
    curl -s -X POST -d "$inputs" -b cookie.txt "$url" -A "$ua" |
    grep -oE '<span id="shindanResult" [^>]+>(.*?)(</span>){5}' |
    sed -r 's_<br />_'\\n'_g;s/<[^>]+>//g'

    # 連続で取得する場合はWaitを入れる
    # sleep "$[RANDOM%4+2]"
    rm cookie.txt
}

function main(){
  if [ "$#" != 2 ] || ! [[ "$1" =~ ^[1-9][0-9]*$ ]]; then
      echo "usage: $0 <shindan id> <name>" >&2
      return 1
  else
      _shindan "$1" "$2"
  fi
}

main "$@"
exit $?
