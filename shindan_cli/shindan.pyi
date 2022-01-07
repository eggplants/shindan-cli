from typing import List, Optional, TypedDict

class ShindanResult(TypedDict):
    results: List[str]
    hashtags: List[str]
    shindan_url: str

def shindan(page_id: int, shindan_name: str, wait: Optional[bool] = ...) -> ShindanResult: ...
