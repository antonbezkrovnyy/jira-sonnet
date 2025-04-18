import os
import sys
import logging
from pathlib import Path

# Add backend directory to PYTHONPATH
backend_dir = Path(__file__).parent.parent
sys.path.append(str(backend_dir))

# Now we can import app modules
from app.services.external_links import ExternalLinksService
from app.schemas.link import ResourceType
from app.core.logging import get_logger

# Configure more verbose logging
logging.basicConfig(level=logging.DEBUG)
logger = get_logger()

def test_external_links():
    """Debug script for testing external links"""
    
    logger.info(f"Backend dir: {backend_dir}")
    logger.info(f"Python path: {sys.path}")
    
    # Test data
    task_key = "LOGIQPROD-635"
    test_url = "https://example.com/test-doc"
    test_title = "Test External Link"
    
    # Create service
    service = ExternalLinksService()
    
    # 1. First check existing links
    logger.info("Getting existing links...")
    existing_links = service.get_external_links(task_key)
    logger.info(f"Found {len(existing_links)} existing links")
    for link in existing_links:
        logger.info(f"Link: {link.title} -> {link.url}")
        
    # 2. Try creating new link
    logger.info("\nCreating new link...")
    new_link = service.create_external_link(
        task_key=task_key,
        title=test_title,
        url=test_url,
        link_type=ResourceType.WEB
    )
    
    if new_link:
        logger.info(f"Created link: {new_link.title} -> {new_link.url}")
    else:
        logger.error("Failed to create link")
        
    # 3. Verify link was created
    logger.info("\nVerifying new link...")
    updated_links = service.get_external_links(task_key)
    logger.info(f"Found {len(updated_links)} links after creation")
    
    found = False
    for link in updated_links:
        logger.info(f"Link: {link.title} -> {link.url}")
        if str(link.url) == test_url:  # Convert Url object to string for comparison
            found = True
            logger.info("Found our test link!")
            
    if not found:
        logger.error("Test link not found in results")
    print("Updated links found:", [
        f"{link.title} ({str(link.url)})" 
        for link in updated_links
    ])
        
if __name__ == "__main__":
    test_external_links()