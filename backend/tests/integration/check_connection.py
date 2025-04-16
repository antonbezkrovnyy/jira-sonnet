from jira import JIRA
import os
from dotenv import load_dotenv

def check_jira_connection():
    load_dotenv('.env.test.integration')
    
    # Create JIRA client
    jira = JIRA(
        server=os.getenv('JIRA_URL'),
        basic_auth=(os.getenv('JIRA_USER'), os.getenv('JIRA_TOKEN'))
    )
    
    # Get project info
    project = jira.project(os.getenv('TEST_PROJECT_KEY'))
    print(f"Connected to project: {project.name}")
    
    # Find epics
    epics = jira.search_issues('project = LOGIQPROD AND issuetype = Epic', maxResults=5)
    print("\nAvailable Epics:")
    for epic in epics:
        print(f"Key: {epic.key}, Summary: {epic.fields.summary}")
    
    # Find tasks
    tasks = jira.search_issues('project = LOGIQPROD AND issuetype = Engineer', maxResults=5)
    print("\nAvailable Tasks:")
    for task in tasks:
        print(f"Key: {task.key}, Summary: {task.fields.summary}")

if __name__ == '__main__':
    check_jira_connection()