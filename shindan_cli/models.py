"""Models for shindan-cli."""

from __future__ import annotations

from typing import TypedDict


class ShindanResult(TypedDict):
    """TypedDict Class for result of shindan."""

    results: list[str]
    hashtags: list[str]
    shindan_url: str


class QuestionBranchChoice(TypedDict):
    label: str
    next_branch_id: str


class QuestionBranch(TypedDict):
    """TypedDict Class for question branch."""

    question: str
    choices: list[QuestionBranchChoice]


class QuestionChoiceChoice(TypedDict):
    label: str
    choice_id: str


class QuestionChoice(TypedDict):
    """TypedDict Class for question choice."""

    question: str
    choices: list[QuestionChoiceChoice]


class UserInput(TypedDict):
    """TypedDict Class for user input."""

    q: str
    a: str | None


UserInputs = dict[str, UserInput]

__all__ = (
    "QuestionBranch",
    "QuestionChoice",
    "ShindanResult",
    "UserInput",
    "UserInputs",
)
