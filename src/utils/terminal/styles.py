from typing import Literal

Style = Literal[
    "bold",
    "dim",
    "italic",
    "underline",
    "blink",
    "reverse",
    "conceal",
    "strikethrough",
]

STYLES: dict[Style, int] = {
    "bold": 1,
    "dim": 2,
    "italic": 3,
    "underline": 4,
    "blink": 5,
    "reverse": 7,
    "conceal": 8,
    "strikethrough": 9,
}