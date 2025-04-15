from typing import TypedDict
import os

class Settings(TypedDict):
    jira_url: str
    jira_user: str
    jira_token: str

def get_settings() -> Settings:
    return {
        'jira_url': os.getenv('JIRA_URL', ''),
        'jira_user': os.getenv('JIRA_USER', ''),
        'jira_token': os.getenv('JIRA_TOKEN', '')
    }