"""
Flow Manager
Manages Power Automate Desktop flows
"""

import os
import json
import shutil
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime


class FlowManager:
    """Manages PAD flows"""
    
    def __init__(self, config, logger):
        """
        Initialize Flow Manager
        
        Args:
            config: Configuration object
            logger: Logger object
        """
        self.config = config
        self.logger = logger
        self.flows_path = config.get_path("flows")
        
    def list_flows(self, search_pattern: Optional[str] = None) -> List[str]:
        """
        List all available flows
        
        Args:
            search_pattern: Optional search pattern
            
        Returns:
            List of flow names
        """
        try:
            flows = []
            
            if not self.flows_path.exists():
                self.logger.warning(f"Flows path does not exist: {self.flows_path}")
                return flows
            
            for item in self.flows_path.rglob("*.json"):
                flow_name = item.stem
                
                if search_pattern:
                    if search_pattern.lower() in flow_name.lower():
                        flows.append(flow_name)
                else:
                    flows.append(flow_name)
            
            return sorted(flows)
            
        except Exception as e:
            self.logger.error(f"Error listing flows: {str(e)}")
            return []
    
    def get_flow(self, flow_name: str) -> Optional[Dict[str, Any]]:
        """
        Get flow definition
        
        Args:
            flow_name: Name of the flow
            
        Returns:
            Flow definition or None
        """
        try:
            flow_path = self.flows_path / f"{flow_name}.json"
            
            if not flow_path.exists():
                self.logger.error(f"Flow not found: {flow_name}")
                return None
            
            with open(flow_path, 'r', encoding='utf-8') as f:
                flow_data = json.load(f)
            
            return flow_data
            
        except Exception as e:
            self.logger.error(f"Error loading flow {flow_name}: {str(e)}")
            return None
    
    def create_flow(self, flow_name: str, template: Optional[str] = None) -> bool:
        """
        Create a new flow
        
        Args:
            flow_name: Name for the new flow
            template: Optional template name
            
        Returns:
            Success status
        """
        try:
            flow_path = self.flows_path / f"{flow_name}.json"
            
            if flow_path.exists():
                self.logger.warning(f"Flow already exists: {flow_name}")
                return False
            
            # Create flow from template or default
            flow_data = self._get_template(template) if template else self._get_default_flow()
            flow_data["name"] = flow_name
            flow_data["created_at"] = datetime.now().isoformat()
            
            with open(flow_path, 'w', encoding='utf-8') as f:
                json.dump(flow_data, f, indent=2)
            
            self.logger.info(f"Flow created: {flow_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating flow {flow_name}: {str(e)}")
            return False
    
    def delete_flow(self, flow_name: str) -> bool:
        """
        Delete a flow
        
        Args:
            flow_name: Name of the flow to delete
            
        Returns:
            Success status
        """
        try:
            flow_path = self.flows_path / f"{flow_name}.json"
            
            if not flow_path.exists():
                self.logger.warning(f"Flow not found: {flow_name}")
                return False
            
            flow_path.unlink()
            self.logger.info(f"Flow deleted: {flow_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error deleting flow {flow_name}: {str(e)}")
            return False
    
    def validate_flow(self, flow_name: str) -> Dict[str, Any]:
        """
        Validate a flow
        
        Args:
            flow_name: Name of the flow to validate
            
        Returns:
            Validation results
        """
        results = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "info": []
        }
        
        try:
            flow_data = self.get_flow(flow_name)
            
            if not flow_data:
                results["valid"] = False
                results["errors"].append("Flow not found")
                return results
            
            # Validate required fields
            required_fields = ["name", "version", "actions"]
            for field in required_fields:
                if field not in flow_data:
                    results["valid"] = False
                    results["errors"].append(f"Missing required field: {field}")
            
            # Validate actions
            if "actions" in flow_data:
                if not isinstance(flow_data["actions"], list):
                    results["valid"] = False
                    results["errors"].append("Actions must be a list")
                elif len(flow_data["actions"]) == 0:
                    results["warnings"].append("Flow has no actions")
            
            # Validate variables
            if "variables" in flow_data:
                if not isinstance(flow_data["variables"], dict):
                    results["valid"] = False
                    results["errors"].append("Variables must be a dictionary")
            
            results["info"].append(f"Flow validation completed for: {flow_name}")
            
        except Exception as e:
            results["valid"] = False
            results["errors"].append(f"Validation error: {str(e)}")
        
        return results
    
    def export_flow(self, flow_name: str, output_path: str) -> bool:
        """
        Export a flow
        
        Args:
            flow_name: Name of the flow to export
            output_path: Path to export the flow
            
        Returns:
            Success status
        """
        try:
            flow_path = self.flows_path / f"{flow_name}.json"
            
            if not flow_path.exists():
                self.logger.error(f"Flow not found: {flow_name}")
                return False
            
            shutil.copy2(flow_path, output_path)
            self.logger.info(f"Flow exported: {flow_name} -> {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting flow {flow_name}: {str(e)}")
            return False
    
    def import_flow(self, flow_path: str, flow_name: Optional[str] = None) -> bool:
        """
        Import a flow
        
        Args:
            flow_path: Path to the flow file
            flow_name: Optional name for the imported flow
            
        Returns:
            Success status
        """
        try:
            source_path = Path(flow_path)
            
            if not source_path.exists():
                self.logger.error(f"Flow file not found: {flow_path}")
                return False
            
            # Determine target name
            if not flow_name:
                flow_name = source_path.stem
            
            target_path = self.flows_path / f"{flow_name}.json"
            
            # Load and validate
            with open(source_path, 'r', encoding='utf-8') as f:
                flow_data = json.load(f)
            
            flow_data["name"] = flow_name
            flow_data["imported_at"] = datetime.now().isoformat()
            
            # Save to flows directory
            with open(target_path, 'w', encoding='utf-8') as f:
                json.dump(flow_data, f, indent=2)
            
            self.logger.info(f"Flow imported: {flow_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error importing flow: {str(e)}")
            return False
    
    def _get_default_flow(self) -> Dict[str, Any]:
        """Get default flow template"""
        return {
            "name": "",
            "description": "New Power Automate Desktop Flow",
            "version": "1.0",
            "enabled": True,
            "variables": {
                "input": {},
                "output": {}
            },
            "actions": [],
            "error_handling": {
                "on_error": "stop",
                "retry_count": 0
            },
            "settings": {
                "timeout": 300,
                "priority": 5
            }
        }
    
    def _get_template(self, template_name: str) -> Dict[str, Any]:
        """
        Get flow template
        
        Args:
            template_name: Name of the template
            
        Returns:
            Template data
        """
        templates_path = self.config.get_path("configs") / "templates"
        template_file = templates_path / f"{template_name}.json"
        
        if template_file.exists():
            with open(template_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        return self._get_default_flow()
