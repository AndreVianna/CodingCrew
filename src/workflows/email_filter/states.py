"""States for the email workflow."""

from typing import TypedDict

class EmailFilterState(TypedDict):
    """
    Represents the state of emails in the workflow.

    Attributes:
        quit (bool): Indicates whether the workflow should quit.
        checked_emails_ids (List[str]): A list of IDs of checked emails.
        emails (List[dict]): A list of email dictionaries.
        action_required_emails (dict): A dictionary of action required emails.
    """
    quit: bool
    checked_emails_ids: list[str]
    emails: list[dict]
    action_required_emails: dict
