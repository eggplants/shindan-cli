"""Constants for the shindan CLI."""

from typing import Literal, TypedDict


class AIParams(TypedDict):
    _token: str
    randname: str
    type: Literal["ai"]
    shindan_token: str
    encrypted_exec_key: str


class BranchParams(TypedDict):
    _token: str
    randname: str
    hiddenName: str
    type: Literal["branch"]
    shindan_token: str
    rbr: str


class CheckParams(TypedDict):
    _token: str
    randname: str
    hiddenName: str
    type: Literal["check"]
    shindan_token: str
    # input-check-choice[choice_id]: str


class NameParams(TypedDict):
    _token: str
    randname: str
    hiddenName: str
    type: Literal["name"]
    shindan_token: str


class TargetKeysByType(TypedDict):
    ai: AIParams
    branch: BranchParams
    check: CheckParams
    name: NameParams


TARGET_KEYS_BY_TYPE = {
    "ai": AIParams.__annotations__.keys(),
    "branch": BranchParams.__annotations__.keys(),
    "check": CheckParams.__annotations__.keys(),
    "name": NameParams.__annotations__.keys(),
}

BASE_URL = "https://shindanmaker.com"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    ),
}

__all__ = (
    "BASE_URL",
    "HEADERS",
    "TARGET_KEYS_BY_TYPE",
)
