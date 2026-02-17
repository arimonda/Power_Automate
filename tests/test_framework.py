"""
Framework Tests
Test cases for PAD Framework
"""

import pytest
from pad_framework import PADFramework, Config, FlowManager


class TestFramework:
    """Test PAD Framework core functionality"""
    
    @pytest.fixture
    def pad(self):
        """Create framework instance for testing"""
        return PADFramework()
    
    def test_framework_initialization(self, pad):
        """Test framework initializes correctly"""
        assert pad is not None
        assert pad.config is not None
        assert pad.logger is not None
        assert pad.flow_manager is not None
    
    def test_list_flows(self, pad):
        """Test listing flows"""
        flows = pad.list_flows()
        assert isinstance(flows, list)
    
    def test_health_status(self, pad):
        """Test health status check"""
        health = pad.get_health_status()
        assert "status" in health
        assert "version" in health
        assert health["status"] == "healthy"
    
    def test_create_flow(self, pad):
        """Test flow creation"""
        flow_name = "TestFlow"
        result = pad.create_flow(flow_name)
        # Cleanup
        if result:
            pad.flow_manager.delete_flow(flow_name)
    
    def test_validate_flow(self, pad):
        """Test flow validation"""
        flow_name = "TestFlow"
        pad.create_flow(flow_name)
        
        validation = pad.validate_flow(flow_name)
        assert "valid" in validation
        assert "errors" in validation
        assert "warnings" in validation
        
        # Cleanup
        pad.flow_manager.delete_flow(flow_name)


class TestConfig:
    """Test configuration management"""
    
    def test_config_initialization(self):
        """Test config initializes with defaults"""
        config = Config()
        assert config is not None
        assert config.config is not None
    
    def test_config_get(self):
        """Test getting config values"""
        config = Config()
        level = config.get("logging.level")
        assert level is not None
    
    def test_config_set(self):
        """Test setting config values"""
        config = Config()
        config.set("test.value", "test123")
        assert config.get("test.value") == "test123"


class TestFlowManager:
    """Test flow management"""
    
    @pytest.fixture
    def config(self):
        """Create config for testing"""
        return Config()
    
    @pytest.fixture
    def logger(self):
        """Create logger for testing"""
        from pad_framework.utils.logger import Logger
        return Logger(Config())
    
    @pytest.fixture
    def flow_manager(self, config, logger):
        """Create flow manager for testing"""
        return FlowManager(config, logger)
    
    def test_list_flows(self, flow_manager):
        """Test listing flows"""
        flows = flow_manager.list_flows()
        assert isinstance(flows, list)
    
    def test_create_and_delete_flow(self, flow_manager):
        """Test creating and deleting flows"""
        flow_name = "TestFlowTemp"
        
        # Create
        created = flow_manager.create_flow(flow_name)
        assert created == True
        
        # Verify exists
        flows = flow_manager.list_flows()
        assert flow_name in flows
        
        # Delete
        deleted = flow_manager.delete_flow(flow_name)
        assert deleted == True
        
        # Verify deleted
        flows = flow_manager.list_flows()
        assert flow_name not in flows


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
