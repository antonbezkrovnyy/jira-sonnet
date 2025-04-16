from dotenv import load_dotenv
from jira import JIRA
import os

def debug_jira_connection():
    # Load environment variables
    load_dotenv('.env.test.integration')
    
    print("=== JIRA Connection Debug ===")
    
    # Print configuration
    print("\nConfiguration:")
    print(f"JIRA URL: {os.getenv('JIRA_URL')}")
    print(f"JIRA User: {os.getenv('JIRA_USER')}")
    print(f"Project Key: {os.getenv('TEST_PROJECT_KEY')}")
    print(f"Epic Key: {os.getenv('TEST_EPIC_KEY')}")
    print(f"Task Key: {os.getenv('TEST_TASK_KEY')}")
    
    try:
        # Create JIRA client
        jira = JIRA(
            server=os.getenv('JIRA_URL'),
            basic_auth=(os.getenv('JIRA_USER'), os.getenv('JIRA_TOKEN'))
        )
        print("\nJIRA Connection: Success")
        
        # Get epic
        epic_key = os.getenv('TEST_EPIC_KEY')
        epic = jira.issue(epic_key)
        print(f"\nEpic Data (key={epic_key}):")
        print(f"Key: {epic.key}")
        print(f"Summary: {epic.fields.summary}")
        epic_name = getattr(epic.fields, 'customfield_10604', None)
        print(f"Epic Name (customfield_10604): {epic_name}")
        
        # Search for tasks with correct JQL
        print(f"\nSearching tasks for Epic Link: {epic_name}")
        jql = f'"Epic Link" = {epic_key} AND issuetype = Engineer'
        print(f"JQL: {jql}")
        
        tasks = jira.search_issues(jql)
        print("\nLinked Tasks:")
        if tasks:
            for task in tasks:
                print(f"Key: {task.key}")
                print(f"Summary: {task.fields.summary}")
                # Print task's Epic Link field
                task_epic = getattr(task.fields, 'customfield_10601', None)
                print(f"Task's Epic Link: {task_epic}")
                print("---")
        else:
            print("No tasks found")
            
        # Try alternative search
        print("\nTrying direct parent search:")
        parent_jql = f'parent = {epic_key} AND issuetype = Engineer'
        print(f"JQL: {parent_jql}")
        parent_tasks = jira.search_issues(parent_jql)
        if parent_tasks:
            for task in parent_tasks:
                print(f"Key: {task.key}")
                print(f"Summary: {task.fields.summary}")
                print("---")
        else:
            print("No tasks found via parent search")
            
    except Exception as e:
        print(f"\nError: {str(e)}")
        raise  # Re-raise to see full stack trace

if __name__ == '__main__':
    debug_jira_connection()