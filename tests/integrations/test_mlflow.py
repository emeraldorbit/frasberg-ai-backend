"""Tests for MLflow Integration"""

import pytest
from unittest.mock import Mock, patch
from backend.app.integrations.mlflow_tracker import MLflowTracker


class TestMLflowTracker:
    """Test suite for MLflowTracker"""
    
    def test_init_basic(self):
        """Test basic initialization"""
        with patch('backend.app.integrations.mlflow_tracker.mlflow') as mock_mlflow:
            tracker = MLflowTracker()
            assert tracker.tracking_uri is None
            assert tracker.experiment_name is None
    
    def test_init_with_tracking_uri(self):
        """Test initialization with tracking URI"""
        with patch('backend.app.integrations.mlflow_tracker.mlflow') as mock_mlflow:
            tracker = MLflowTracker(tracking_uri="http://localhost:5000")
            assert tracker.tracking_uri == "http://localhost:5000"
            mock_mlflow.set_tracking_uri.assert_called_once_with("http://localhost:5000")
    
    def test_init_with_experiment(self):
        """Test initialization with experiment name"""
        with patch('backend.app.integrations.mlflow_tracker.mlflow') as mock_mlflow:
            tracker = MLflowTracker(experiment_name="test-experiment")
            assert tracker.experiment_name == "test-experiment"
            mock_mlflow.set_experiment.assert_called_once_with("test-experiment")
    
    def test_init_without_mlflow(self):
        """Test initialization fails without mlflow package"""
        with patch('backend.app.integrations.mlflow_tracker.mlflow', side_effect=ImportError):
            with pytest.raises(ImportError):
                MLflowTracker()
    
    def test_start_run(self):
        """Test starting a run"""
        with patch('backend.app.integrations.mlflow_tracker.mlflow') as mock_mlflow:
            mock_run = Mock()
            mock_mlflow.start_run.return_value = mock_run
            
            tracker = MLflowTracker()
            run = tracker.start_run(run_name="test-run")
            
            assert run == mock_run
            mock_mlflow.start_run.assert_called_once_with(run_name="test-run")
    
    def test_log_params(self):
        """Test logging parameters"""
        with patch('backend.app.integrations.mlflow_tracker.mlflow') as mock_mlflow:
            tracker = MLflowTracker()
            params = {"learning_rate": 0.001, "batch_size": 32}
            tracker.log_params(params)
            
            mock_mlflow.log_params.assert_called_once_with(params)
    
    def test_log_metrics(self):
        """Test logging metrics"""
        with patch('backend.app.integrations.mlflow_tracker.mlflow') as mock_mlflow:
            tracker = MLflowTracker()
            metrics = {"accuracy": 0.95, "loss": 0.05}
            tracker.log_metrics(metrics)
            
            mock_mlflow.log_metrics.assert_called_once_with(metrics, step=None)
    
    def test_log_metrics_with_step(self):
        """Test logging metrics with step"""
        with patch('backend.app.integrations.mlflow_tracker.mlflow') as mock_mlflow:
            tracker = MLflowTracker()
            metrics = {"accuracy": 0.95}
            tracker.log_metrics(metrics, step=10)
            
            mock_mlflow.log_metrics.assert_called_once_with(metrics, step=10)
    
    def test_log_model(self):
        """Test logging model"""
        with patch('backend.app.integrations.mlflow_tracker.mlflow') as mock_mlflow:
            tracker = MLflowTracker()
            model = Mock()
            tracker.log_model(model, "model-path")
            
            # Just verify it doesn't crash
            assert True
    
    def test_end_run(self):
        """Test ending a run"""
        with patch('backend.app.integrations.mlflow_tracker.mlflow') as mock_mlflow:
            tracker = MLflowTracker()
            tracker.end_run()
            
            mock_mlflow.end_run.assert_called_once()
    
    def test_complete_workflow(self):
        """Test complete workflow"""
        with patch('backend.app.integrations.mlflow_tracker.mlflow') as mock_mlflow:
            mock_run = Mock()
            mock_mlflow.start_run.return_value = mock_run
            
            tracker = MLflowTracker(experiment_name="test")
            tracker.start_run(run_name="run-1")
            tracker.log_params({"lr": 0.001})
            tracker.log_metrics({"accuracy": 0.95})
            tracker.end_run()
            
            mock_mlflow.start_run.assert_called_once()
            mock_mlflow.log_params.assert_called_once()
            mock_mlflow.log_metrics.assert_called_once()
            mock_mlflow.end_run.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
