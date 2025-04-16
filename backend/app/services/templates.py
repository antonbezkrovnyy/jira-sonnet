from pathlib import Path
from typing import Dict, List, Optional
import yaml
from datetime import datetime
from app.schemas.checklist import ChecklistTemplate, ChecklistType
from app.core.logging import get_logger

logger = get_logger()

class TemplateService:
    """Service for managing DoR/DoD templates"""
    
    def __init__(self, templates_dir: str = "checklists"):
        self.base_path = Path(__file__).parent.parent.parent / templates_dir
        self.templates: Dict[ChecklistType, Dict[str, ChecklistTemplate]] = {
            ChecklistType.DOR: {},
            ChecklistType.DOD: {}
        }
        self._load_templates()
    
    def _load_templates(self) -> None:
        """Load all templates from filesystem"""
        for checklist_type in ChecklistType:
            type_dir = self.base_path / checklist_type.value
            if not type_dir.exists():
                logger.warning(f"Directory not found: {type_dir}")
                continue
                
            for template_file in type_dir.glob("*.md"):
                try:
                    template = self._parse_template(template_file, checklist_type)
                    self.templates[checklist_type][template.key] = template
                    logger.info(f"Loaded template: {template.key} ({checklist_type})")
                except Exception as e:
                    logger.error(f"Error loading template {template_file}: {str(e)}")
    
    def _parse_template(self, file_path: Path, type: ChecklistType) -> ChecklistTemplate:
        """Parse markdown template file"""
        content = file_path.read_text(encoding='utf-8')
        
        if not content.startswith('---'):
            raise ValueError(f"No frontmatter found in {file_path}")
            
        _, frontmatter, content = content.split('---', 2)
        metadata = yaml.safe_load(frontmatter)
        
        return ChecklistTemplate(
            key=file_path.stem,
            type=type,
            content=content.strip(),
            **metadata
        )
    
    def get_template(self, type: ChecklistType, key: str) -> Optional[ChecklistTemplate]:
        """Get template by type and key"""
        return self.templates[type].get(key)
    
    def get_templates(self, type: ChecklistType) -> List[ChecklistTemplate]:
        """Get all templates of given type"""
        return list(self.templates[type].values())
    
    def delete_template(self, type: ChecklistType, key: str) -> bool:
        """Delete template file"""
        try:
            template_path = self.base_path / type.value / f"{key}.md"
            if not template_path.exists():
                return False
                
            template_path.unlink()
            del self.templates[type][key]
            logger.info(f"Deleted template: {key} ({type})")
            return True
        except Exception as e:
            logger.error(f"Error deleting template {key}: {str(e)}")
            return False
    
    def update_template(
        self, 
        type: ChecklistType, 
        key: str, 
        name: str,
        description: str,
        content: str,
        version: str = "1.0"
    ) -> Optional[ChecklistTemplate]:
        """Update existing template"""
        try:
            template_path = self.base_path / type.value / f"{key}.md"
            if not template_path.exists():
                return None
                
            # Create template content
            template_content = f"""---
name: {name}
description: {description}
version: {version}
---
{content}"""

            # Write to file
            template_path.write_text(template_content, encoding='utf-8')
            
            # Update cache
            template = self._parse_template(template_path, type)
            self.templates[type][key] = template
            
            logger.info(f"Updated template: {key} ({type})")
            return template
            
        except Exception as e:
            logger.error(f"Error updating template {key}: {str(e)}")
            return None

# Global instance
_template_service: Optional[TemplateService] = None

def get_template_service() -> TemplateService:
    """Get or create template service instance"""
    global _template_service
    if _template_service is None:
        _template_service = TemplateService()
    return _template_service