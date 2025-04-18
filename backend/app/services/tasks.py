from typing import Optional
from datetime import datetime

from app.core.logging import get_logger
from app.services.jira import get_jira_client 
from app.schemas.create_task import CreateTaskRequest, TaskPriority

logger = get_logger(__name__)

class TasksService:
    """Service for creating and managing JIRA tasks"""
    
    def __init__(self):
        self.client = get_jira_client()
        # Important: These are the correct custom field IDs for JIRA
        self.field_config = {
            'EPIC_LINK_FIELD': 'customfield_10601',  # Epic Link field ID
            'TIME_TRACKING': 'timetracking',  # Built-in JIRA field
        }

    def create_task(self, request: CreateTaskRequest) -> Optional[dict]:
        """
        Create new JIRA issue with all fields including Epic Link and Time Tracking
        
        The method uses specific field IDs and formats:
        - Epic Link: Uses customfield_10601
        - Time Tracking: Uses built-in 'timetracking' with format "Xh Ym"
        """
        try:
            # Create base issue with all fields at once
            fields = {
                'project': {'key': request.project_key},
                'summary': request.summary,
                'issuetype': {'name': request.issue_type},
                'priority': {'name': request.priority.value}
            }

            # Add optional fields
            if request.description:
                fields['description'] = request.description
                
            if request.due_date:
                fields['duedate'] = request.due_date.strftime('%Y-%m-%d')
                
            if request.labels:
                fields['labels'] = request.labels
                
            if request.assignee:
                fields['assignee'] = {'name': request.assignee}

            # Epic Link field must use customfield_10601 (not 10014)
            if request.epic_link:
                fields[self.field_config['EPIC_LINK_FIELD']] = request.epic_link
                logger.info(f"Setting Epic Link {request.epic_link} using field {self.field_config['EPIC_LINK_FIELD']}")

            # Time tracking must use JIRA's format "Xh Ym"
            if request.estimate:
                hours = int(request.estimate)
                minutes = int((request.estimate - hours) * 60)
                estimate = f"{hours}h {minutes}m"
                fields[self.field_config['TIME_TRACKING']] = {
                    'originalEstimate': estimate  # Correct format for time tracking
                }
                logger.info(f"Setting Time Estimate to {estimate}")

            # Create issue with all fields
            new_issue = self.client.create_issue(fields=fields)
            logger.info(f"Successfully created task {new_issue.key}")

            # Get and return updated issue
            updated_issue = self.client.issue(new_issue.key)
            return updated_issue.raw

        except Exception as e:
            logger.error(f"Error creating task: {str(e)}")
            return None

    def get_task_types(self, project_key: str) -> list:
        """Get available issue types for project"""
        try:
            project = self.client.project(project_key)
            types = [
                {'id': t.id, 'name': t.name}
                for t in project.issueTypes
            ]
            logger.debug(f"Found {len(types)} issue types for project {project_key}")
            return types
        except Exception as e:
            logger.error(f"Error getting issue types: {str(e)}")
            return []

    def get_field_ids(self, issue_key: str) -> dict:
        """Get all available field IDs for issue"""
        try:
            fields = self.client.fields()
            return {
                field['name']: field['id'] 
                for field in fields
            }
        except Exception as e:
            logger.error(f"Error getting field IDs: {str(e)}")
            return {}