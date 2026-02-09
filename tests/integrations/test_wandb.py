"""Tests for Weights & Biases Integration"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from backend.app.integrations.wandb_logger import WandBLogger


class TestWandBLogger:
    """Test suite for WandBLogger"""
    
    def test_init_basic(self):
        """Test basic initialization"""
        with patch('backend.app.integrations.wandb_logger.wandb') as mock_wandb:
            mock_wandb.init.return_value = Mock()
            
            logger = WandBLogger(project="test-project")
            
            assert logger.project == "test-project"
            mock_wandb.init.assert_called_once()
    
    def test_init_with_entity(self):
        """Test initialization with entity"""
        with patch('backend.app.integrations.wandb_logger.wandb') as mock_wandb:
            mock_wandb.init.return_value = Mock()
            
            logger = WandBLogger(
                project="test-project",
                entity="test-team"
            )
            
            assert logger.entity == "test-team"
            assert logger.project == "test-project"
    
    def test_init_with_config(self):
        """Test initialization with configuration"""
        with patch('backend.app.integrations.wandb_logger.wandb') as mock_wandb:
            mock_wandb.init.return_value = Mock()
            
            config = {"learning_rate": 0.001, "batch_size": 32}
            logger = WandBLogger(project="test-project", config=config)
            
            assert logger.config == config
    
    def test_init_without_wandb(self):
        """Test initialization fails without wandb package"""
        with patch('backend.app.integrations.wandb_logger.wandb', side_effect=ImportError):
            with pytest.raises(ImportError):
                WandBLogger(project="test-project")
    
    def test_log_metrics(self):
        """Test logging metrics"""
        with patch('backend.app.integrations.wandb_logger.wandb') as mock_wandb:
            mock_wandb.init.return_value = Mock()
            mock_wandb.log = Mock()
            
            logger = WandBLogger(project="test-project")
            metrics = {"accuracy": 0.95, "loss": 0.05}
            logger.log_metrics(metrics)
            
            mock_wandb.log.assert_called_once_with(metrics, step=None)
    
    def test_log_metrics_with_step(self):
        """Test logging metrics with step"""
        with patch('backend.app.integrations.wandb_logger.wandb') as mock_wandb:
            mock_wandb.init.return_value = Mock()
            mock_wandb.log = Mock()
            
            logger = WandBLogger(project="test-project")
            metrics = {"accuracy": 0.95}
            logger.log_metrics(metrics, step=10)
            
            mock_wandb.log.assert_called_once_with(metrics, step=10)
    
    def test_log_model(self):
        """Test logging model"""
        with patch('backend.app.integrations.wandb_logger.wandb') as mock_wandb:
            mock_wandb.init.return_value = Mock()
            mock_artifact = Mock()
            mock_wandb.Artifact.return_value = mock_artifact
            
            logger = WandBLogger(project="test-project")
            model = Mock()
            logger.log_model(model, name="test-model")
            
            mock_wandb.Artifact.assert_called_once_with(
                "test-model",
                type="model",
                metadata=None
            )
    
    def test_finish(self):
        """Test finishing run"""
        with patch('backend.app.integrations.wandb_logger.wandb') as mock_wandb:
            mock_run = Mock()
            mock_run.finish = Mock()
            mock_wandb.init.return_value = mock_run
            
            logger = WandBLogger(project="test-project")
            logger.finish()
            
            mock_run.finish.assert_called_once()
    
    def test_multiple_metrics(self):
        """Test logging multiple metrics"""
        with patch('backend.app.integrations.wandb_logger.wandb') as mock_wandb:
            mock_wandb.init.return_value = Mock()
            mock_wandb.log = Mock()
            
            logger = WandBLogger(project="test-project")
            
            # Log multiple times
            logger.log_metrics({"accuracy": 0.9}, step=1)
            logger.log_metrics({"accuracy": 0.92}, step=2)
            logger.log_metrics({"accuracy": 0.95}, step=3)
            
            assert mock_wandb.log.call_count == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
