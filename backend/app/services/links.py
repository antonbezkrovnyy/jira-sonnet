from typing import List, Optional
from datetime import datetime
from app.schemas.link import TaskLink, LinkType
from app.services.jira import get_jira_client
from app.core.logging import get_logger

logger = get_logger()

class LinksService:
    """Service for managing task links"""
    
    def get_task_links(self, task_key: str) -> List[TaskLink]:
        """Get all links for a task"""
        try:
            client = get_jira_client()
            issue = client.issue(task_key)
            
            links = []
            for link in issue.fields.issuelinks:
                # Get target issue and link type
                if hasattr(link, "outwardIssue"):
                    target = link.outwardIssue
                    link_type = link.type.outward
                elif hasattr(link, "inwardIssue"):
                    target = link.inwardIssue
                    link_type = link.type.inward
                else:
                    continue
                    
                links.append(TaskLink(
                    id=str(link.id),
                    type=link_type,
                    source=task_key,
                    target=target.key
                ))
                
            return links
            
        except Exception as e:
            logger.error(f"Error getting links for task {task_key}: {str(e)}")
            return []
            
    def create_task_link(self, source: str, link_type: LinkType, target: str) -> Optional[TaskLink]:
        """Create new task link"""
        try:
            client = get_jira_client()
            
            # Create link in JIRA
            client.create_issue_link(
                type=self._map_to_jira_link_type(link_type),
                inwardIssue=target,
                outwardIssue=source
            )
            
            # Return new link object
            return TaskLink(
                id="new",  # JIRA doesn't return link ID
                type=link_type,
                source=source,
                target=target,
                created=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Error creating link {source} -> {target}: {str(e)}")
            return None
            
    def _map_jira_link_type(self, jira_type: str) -> LinkType:
        """Map JIRA link type to internal enum"""
        mapping = {
            "Blocks": LinkType.BLOCKS,
            "Is blocked by": LinkType.BLOCKED_BY,
            "Relates": LinkType.RELATES_TO,
            "Duplicates": LinkType.DUPLICATES,
            "Is duplicated by": LinkType.DUPLICATED_BY
        }
        return mapping.get(jira_type, LinkType.RELATES_TO)
        
    def _map_to_jira_link_type(self, link_type: LinkType) -> str:
        """Map internal enum to JIRA link type"""
        mapping = {
            LinkType.BLOCKS: "Blocks",
            LinkType.BLOCKED_BY: "Blocks",
            LinkType.RELATES_TO: "Relates",
            LinkType.DUPLICATES: "Duplicates",
            LinkType.DUPLICATED_BY: "Duplicates"
        }
        return mapping[link_type]