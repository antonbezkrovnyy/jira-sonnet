from typing import List, Optional
import requests
from app.schemas.link import ExternalLink, ResourceType
from app.services.jira import get_jira_client
from app.core.logging import get_logger

logger = get_logger()

class ExternalLinksService:
    """Service for managing external links"""
    
    def get_external_links(self, task_key: str) -> List[ExternalLink]:
        """Get all external links for a task"""
        try:
            client = get_jira_client()
            # Get fresh issue data
            issue = client.issue(task_key, fields=['remotelinks'])
            
            # Get remote links
            remote_links = client.remote_links(issue)
            logger.debug(f"Remote links response: {[link.raw for link in remote_links]}")
            
            if not remote_links:
                logger.debug("No remote links found")
                return []
                
            links = []
            for remote_link in remote_links:
                # Extract URL and title from response
                link_object = remote_link.raw.get('object', {})
                url = link_object.get('url')
                title = link_object.get('title')
                
                logger.debug(f"Processing remote link: url={url}, title={title}")
                
                if not url:
                    continue
                    
                link_type = self._determine_link_type(url)
                links.append(ExternalLink(
                    id=str(remote_link.id),
                    type=link_type,
                    source=task_key,
                    target=title or url,
                    title=title or url,
                    url=url
                ))
            
            logger.debug(f"Found {len(links)} external links")
            return links
            
        except Exception as e:
            logger.error(f"Error getting external links for task {task_key}: {str(e)}")
            logger.exception(e)  # Log full traceback
            return []
    
    def create_external_link(
        self, 
        task_key: str,
        title: str,
        url: str,
        link_type: ResourceType
    ) -> Optional[ExternalLink]:
        """Create new external link"""
        try:
            client = get_jira_client()
            
            # Prepare destination object
            destination = {
                "url": url,
                "title": title
            }
            
            # Create remote link using JIRA client
            remote_link = client.add_remote_link(
                issue=task_key,
                destination=destination,
                globalId=url,  # Using URL as globalId for uniqueness
                application={
                    "type": link_type.value,
                    "name": title
                }
            )
            
            # Return ExternalLink object
            return ExternalLink(
                id=str(remote_link.id),
                type=link_type,
                source=task_key,
                target=title,
                title=title,
                url=url
            )
            
        except Exception as e:
            logger.error(f"Error creating external link for task {task_key}: {str(e)}")
            logger.exception(e)
            return None
            
    def _determine_link_type(self, url: str) -> ResourceType:
        """Determine resource type from URL"""
        if 'confluence' in url.lower():
            return ResourceType.CONFLUENCE
        elif 'docs.google.com' in url.lower():
            return ResourceType.GDOC
        else:
            return ResourceType.WEB