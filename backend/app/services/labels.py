from typing import List, Optional
from app.schemas.label import LabelSchema
from app.services.jira import get_jira_client
from app.core.logging import get_logger, log_request_response

logger = get_logger()

async def get_label(key: str) -> Optional[LabelSchema]:
    """Get label by key"""
    try:
        logger.debug(f"Getting label with key: {key}")
        client = get_jira_client()
        
        # Log JIRA request
        jql = f'labels = "{key}" AND project = LOGIQPROD'
        logger.debug(f"JIRA JQL query: {jql}")
        
        issues = client.search_issues(jql)
        logger.debug(f"Found {len(issues)} issues with label {key}")
        
        if not issues:
            logger.warning(f"No issues found with label {key}")
            return None
            
        # Get task keys and log them
        used_in = [issue.key for issue in issues]
        logger.debug(f"Label {key} is used in: {used_in}")
        
        # Use first issue for dates
        sample_issue = issues[0]
        
        # Create schema and log conversion
        label_data = {
            "key": key,
            "name": key.capitalize(),
            "created": sample_issue.fields.created,
            "updated": sample_issue.fields.updated,
            "used_in": used_in
        }
        logger.debug(f"Converting to LabelSchema: {label_data}")
        
        label = LabelSchema(**label_data)
        log_request_response(
            logger=logger,
            endpoint="get_label",
            request_data={"key": key},
            response_data=label.model_dump()
        )
        return label
        
    except Exception as e:
        log_request_response(
            logger=logger,
            endpoint="get_label",
            request_data={"key": key},
            error=e
        )
        return None

async def get_project_labels() -> List[LabelSchema]:
    """Get all project labels"""
    try:
        client = get_jira_client()
        
        # Get all project issues with labels
        issues = client.search_issues('project = LOGIQPROD AND labels IS NOT EMPTY')
        
        # Collect unique labels
        labels_dict = {}
        for issue in issues:
            for label in issue.fields.labels:
                if label not in labels_dict:
                    labels_dict[label] = {
                        'key': label,
                        'name': label.capitalize(),
                        'created': issue.fields.created,
                        'updated': issue.fields.updated,
                        'used_in': []
                    }
                labels_dict[label]['used_in'].append(issue.key)
        
        return [LabelSchema(**data) for data in labels_dict.values()]
    except Exception as e:
        logger.error(f"Error getting project labels: {str(e)}")
        return []