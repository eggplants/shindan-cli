"""Constants for the shindan CLI."""

from typing import Literal, TypedDict


class AIParams(TypedDict):
    _token: str
    randname: str
    type: Literal["ai"]
    encrypted_exec_key: str


class BranchParams(TypedDict):
    _token: str
    randname: str
    type: Literal["branch"]
    rbr: str


class CheckParams(TypedDict):
    _token: str
    randname: str
    type: Literal["check"]


class NameParams(TypedDict):
    _token: str
    randname: str
    type: Literal["name"]


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

# Browser `curl_cffi` impersonates. Cloudflare fingerprints the TLS and HTTP/2
# handshake, so a hand-written `User-Agent` is not enough to pass for a browser:
# the connection itself has to look like one.
IMPERSONATE = "chrome"

# Only what a browser varies per request. `User-Agent`, `Accept`, `sec-ch-ua`
# and friends are filled in by the impersonation and must not be overridden, or
# they stop agreeing with the fingerprint on the wire.
HEADERS = {
    "Accept-Language": "ja,en-US;q=0.9,en;q=0.8",
}

__all__ = (
    "BASE_URL",
    "HEADERS",
    "IMPERSONATE",
    "TARGET_KEYS_BY_TYPE",
)
