#!/usr/bin/env bash

_shindan() {
    local url name status source inputs
    url="$1"
    name="$2"
    status="$(
        curl -LI "$url" -o /dev/null -w '%{http_code}' -s
    )"
    if [ "$status" != "200" ]; then
        echo "error: status code is invalid (${status})">&2
        return 1
    fi
    source="$(curl -s -c cookie.txt "$url")"
    inputs="$(
        echo -e "$source" | tr \< \\n | grep input |
        sed -nr '
        s/value=""/value="'$name'"/
        s/^.* name="([^"]+)".* value="([^"]+)">$/\1=\2/g
        4,6p' | tr \\n \& | sed 's/.$//'
    )"
    curl -s -X POST -d "$inputs" -b cookie.txt "$url" |
    grep -oE '<span id="shindanResult" [^>]+>(.*?)(</span>){5}' |
    sed -r 's_<br />_'\\n'_g;s/<[^>]+>//g'

    # 連続で取得する場合はWaitを入れる
    # sleep "$[RANDOM%4+2]"

    rm cookie.txt
}

main(){
  if [ "$#" != 2 ]; then
      echo "Usage: $0 <url> <name>" >&2
      return 1
  else

      _shindan "$1" "$2"
  fi
}

main "$@"
exit $?
