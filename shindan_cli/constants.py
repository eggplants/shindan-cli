"""Constants for the shindan CLI."""

TARGET_KEYS_BY_TYPE = {
    "ai": ("_token", "shindanName", "type", "shindan_token"),
    "branch": ("_token", "shindanName", "hiddenName", "type", "shindan_token", "rbr"),
    "check": ("_token", "shindanName", "hiddenName", "type", "shindan_token"),
    "name": ("_token", "shindanName", "hiddenName", "type", "shindan_token"),
}

BASE_URL = "https://shindanmaker.com"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    ),
}

__all__ = (
    "TARGET_KEYS_BY_TYPE",
    "BASE_URL",
    "HEADERS",
)
