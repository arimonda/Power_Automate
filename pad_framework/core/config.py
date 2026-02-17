"""
Configuration Management
Handles all framework configuration
"""

import os
import yaml
from typing import Dict, Any, Optional
from pathlib import Path
from dataclasses import dataclass, field
from dotenv import load_dotenv


@dataclass
class FlowConfig:
    """Configuration for individual flows"""
    name: str
    description: str = ""
    timeout: int = 300
    retry_count: int = 3
    retry_delay: int = 5
    input_variables: Dict[str, Any] = field(default_factory=dict)
    output_variables: Dict[str, Any] = field(default_factory=dict)
    enabled: bool = True
    priority: int = 5
    tags: list = field(default_factory=list)


class Config:
    """Main configuration class"""
    
    DEFAULT_CONFIG = {
        "framework": {
            "name": "PAD Framework",
            "version": "1.0.0",
            "debug": False
        },
        "paths": {
            "flows": "flows",
            "logs": "logs",
            "data": "data",
            "configs": "configs",
            "tests": "tests"
        },
        "logging": {
            "level": "INFO",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "max_file_size": 10485760,  # 10MB
            "backup_count": 5,
            "console_output": True,
            "file_output": True
        },
        "execution": {
            "default_timeout": 300,
            "max_concurrent_flows": 5,
            "retry_enabled": True,
            "default_retry_count": 3,
            "retry_delay": 5,
            "capture_screenshots": True
        },
        "performance": {
            "monitoring_enabled": True,
            "collect_metrics": True,
            "performance_threshold_warning": 80,
            "performance_threshold_critical": 95,
            "memory_threshold_mb": 1024
        },
        "database": {
            "enabled": False,
            "type": "sqlite",
            "connection_string": "",
            "pool_size": 5
        },
        "email": {
            "enabled": False,
            "smtp_server": "",
            "smtp_port": 587,
            "use_tls": True,
            "sender": "",
            "recipients": []
        },
        "notifications": {
            "enabled": True,
            "on_success": False,
            "on_failure": True,
            "on_warning": True
        },
        "security": {
            "encrypt_credentials": True,
            "credential_store": "configs/credentials.enc",
            "api_key_required": False
        },
        "integrations": {
            "web_automation": {
                "enabled": True,
                "browser": "chrome",
                "headless": False,
                "implicit_wait": 10
            },
            "api": {
                "enabled": True,
                "timeout": 30,
                "max_retries": 3
            },
            "file_operations": {
                "enabled": True,
                "temp_folder": "temp",
                "archive_folder": "archive"
            }
        },
        "testing": {
            "enabled": True,
            "auto_test_on_change": False,
            "coverage_threshold": 80
        },
        "scheduling": {
            "enabled": True,
            "timezone": "UTC",
            "max_scheduled_flows": 50
        }
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration
        
        Args:
            config_path: Optional path to configuration file
        """
        # Load environment variables
        load_dotenv()
        
        # Set base path
        self.base_path = Path(os.getcwd())
        
        # Load configuration
        self.config = self.DEFAULT_CONFIG.copy()
        
        if config_path:
            self.load_from_file(config_path)
        else:
            # Try to load from default locations
            default_paths = [
                self.base_path / "configs" / "config.yaml",
                self.base_path / "config.yaml",
                Path.home() / ".pad_framework" / "config.yaml"
            ]
            
            for path in default_paths:
                if path.exists():
                    self.load_from_file(str(path))
                    break
        
        # Override with environment variables
        self.load_from_env()
        
        # Create necessary directories
        self.create_directories()
    
    def load_from_file(self, file_path: str) -> None:
        """
        Load configuration from YAML file
        
        Args:
            file_path: Path to configuration file
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                file_config = yaml.safe_load(f)
                
            if file_config:
                self._deep_update(self.config, file_config)
                
        except Exception as e:
            print(f"Warning: Could not load config from {file_path}: {str(e)}")
    
    def load_from_env(self) -> None:
        """Load configuration from environment variables"""
        env_mappings = {
            "PAD_DEBUG": ("framework", "debug", bool),
            "PAD_LOG_LEVEL": ("logging", "level", str),
            "PAD_FLOWS_PATH": ("paths", "flows", str),
            "PAD_DB_CONNECTION": ("database", "connection_string", str),
            "PAD_SMTP_SERVER": ("email", "smtp_server", str),
            "PAD_SMTP_PORT": ("email", "smtp_port", int),
        }
        
        for env_var, (section, key, type_func) in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                if type_func == bool:
                    value = value.lower() in ('true', '1', 'yes')
                else:
                    value = type_func(value)
                self.config[section][key] = value
    
    def _deep_update(self, target: Dict, source: Dict) -> None:
        """
        Deep update dictionary
        
        Args:
            target: Target dictionary
            source: Source dictionary
        """
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._deep_update(target[key], value)
            else:
                target[key] = value
    
    def create_directories(self) -> None:
        """Create necessary directories"""
        for path_key, path_value in self.config["paths"].items():
            full_path = self.base_path / path_value
            full_path.mkdir(parents=True, exist_ok=True)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value
        
        Args:
            key: Dot-separated configuration key (e.g., 'logging.level')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value
        
        Args:
            key: Dot-separated configuration key
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def get_path(self, path_type: str) -> Path:
        """
        Get full path for a path type
        
        Args:
            path_type: Path type (flows, logs, data, etc.)
            
        Returns:
            Full path
        """
        relative_path = self.config["paths"].get(path_type, path_type)
        return self.base_path / relative_path
    
    def save(self, file_path: Optional[str] = None) -> None:
        """
        Save configuration to file
        
        Args:
            file_path: Optional path to save configuration
        """
        if not file_path:
            file_path = self.base_path / "configs" / "config.yaml"
        
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, default_flow_style=False)
    
    def to_dict(self) -> Dict[str, Any]:
        """Return configuration as dictionary"""
        return self.config.copy()
