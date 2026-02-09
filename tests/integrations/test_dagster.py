"""Tests for Dagster Integration"""

import pytest
from unittest.mock import Mock, patch
from backend.app.integrations.dagster_pipeline import DagsterPipeline


class TestDagsterPipeline:
    """Test suite for DagsterPipeline"""
    
    def test_init_basic(self):
        """Test basic initialization"""
        with patch('backend.app.integrations.dagster_pipeline.op') as mock_op:
            with patch('backend.app.integrations.dagster_pipeline.job') as mock_job:
                pipeline = DagsterPipeline("test-pipeline")
                
                assert pipeline.pipeline_name == "test-pipeline"
                assert pipeline.dagster_op == mock_op
                assert pipeline.dagster_job == mock_job
    
    def test_init_without_dagster(self):
        """Test initialization fails without dagster package"""
        with patch('backend.app.integrations.dagster_pipeline.op', side_effect=ImportError):
            with pytest.raises(ImportError):
                DagsterPipeline("test-pipeline")
    
    def test_op_decorator(self):
        """Test op decorator"""
        with patch('backend.app.integrations.dagster_pipeline.op') as mock_op:
            with patch('backend.app.integrations.dagster_pipeline.job'):
                mock_op.return_value = lambda f: f
                
                pipeline = DagsterPipeline("test-pipeline")
                
                @pipeline.op
                def test_operation():
                    return "test"
                
                result = test_operation()
                assert result == "test"
    
    def test_job_decorator(self):
        """Test job decorator"""
        with patch('backend.app.integrations.dagster_pipeline.op'):
            with patch('backend.app.integrations.dagster_pipeline.job') as mock_job:
                mock_decorator = Mock()
                mock_decorator.return_value = lambda f: f
                mock_job.return_value = mock_decorator
                
                pipeline = DagsterPipeline("test-pipeline")
                
                @pipeline.job
                def test_job():
                    return "job"
                
                result = test_job()
                assert result == "job"
    
    def test_pipeline_with_kwargs(self):
        """Test pipeline with additional kwargs"""
        with patch('backend.app.integrations.dagster_pipeline.op'):
            with patch('backend.app.integrations.dagster_pipeline.job'):
                pipeline = DagsterPipeline(
                    "test-pipeline",
                    description="Test pipeline",
                    tags={"env": "dev"}
                )
                
                assert pipeline.kwargs["description"] == "Test pipeline"
                assert pipeline.kwargs["tags"]["env"] == "dev"
    
    def test_multiple_ops(self):
        """Test multiple ops in a pipeline"""
        with patch('backend.app.integrations.dagster_pipeline.op') as mock_op:
            with patch('backend.app.integrations.dagster_pipeline.job'):
                mock_op.return_value = lambda f: f
                
                pipeline = DagsterPipeline("test-pipeline")
                
                @pipeline.op
                def op1():
                    return "op1"
                
                @pipeline.op
                def op2():
                    return "op2"
                
                assert op1() == "op1"
                assert op2() == "op2"
    
    def test_op_with_context(self):
        """Test op with context parameter"""
        with patch('backend.app.integrations.dagster_pipeline.op') as mock_op:
            with patch('backend.app.integrations.dagster_pipeline.job'):
                mock_op.return_value = lambda f: f
                
                pipeline = DagsterPipeline("test-pipeline")
                
                @pipeline.op
                def op_with_context(context, value):
                    return f"context: {value}"
                
                result = op_with_context(None, "test")
                assert result == "context: test"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
