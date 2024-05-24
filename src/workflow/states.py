from typing import TypedDict

class EmailsState(TypedDict):
    quit: bool
    checked_emails_ids: list[str]
    emails: list[dict]
    action_required_emails: dict
