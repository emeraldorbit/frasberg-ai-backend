"""Tests for Hugging Face Transformers Integration"""

import pytest
from unittest.mock import Mock, patch
from backend.app.integrations.huggingface import HuggingFaceTransformer


class TestHuggingFaceTransformer:
    """Test suite for HuggingFaceTransformer"""
    
    def test_init_basic(self):
        """Test basic initialization"""
        with patch('backend.app.integrations.huggingface.AutoModel'):
            with patch('backend.app.integrations.huggingface.AutoTokenizer'):
                model = HuggingFaceTransformer("gpt2")
                assert model.model_name == "gpt2"
                assert model.device == "auto"
                assert model.use_sofia_cache is True
    
    def test_init_with_custom_device(self):
        """Test initialization with custom device"""
        with patch('backend.app.integrations.huggingface.AutoModel'):
            with patch('backend.app.integrations.huggingface.AutoTokenizer'):
                model = HuggingFaceTransformer("gpt2", device="cpu")
                assert model.device == "cpu"
    
    def test_init_without_transformers(self):
        """Test initialization fails without transformers package"""
        with patch('backend.app.integrations.huggingface.AutoModel', side_effect=ImportError):
            with pytest.raises(ImportError):
                HuggingFaceTransformer("gpt2")
    
    def test_generate(self):
        """Test text generation"""
        with patch('backend.app.integrations.huggingface.AutoModel'):
            with patch('backend.app.integrations.huggingface.AutoTokenizer'):
                with patch('backend.app.integrations.huggingface.pipeline') as mock_pipeline:
                    mock_gen = Mock()
                    mock_gen.return_value = [{"generated_text": "Hello world generated"}]
                    mock_pipeline.return_value = mock_gen
                    
                    model = HuggingFaceTransformer("gpt2")
                    result = model.generate("Hello", max_length=50)
                    
                    assert result == "Hello world generated"
                    mock_gen.assert_called_once()
    
    def test_classify(self):
        """Test text classification"""
        with patch('backend.app.integrations.huggingface.AutoModel'):
            with patch('backend.app.integrations.huggingface.AutoTokenizer'):
                with patch('backend.app.integrations.huggingface.pipeline') as mock_pipeline:
                    mock_classifier = Mock()
                    mock_classifier.return_value = [{"label": "POSITIVE", "score": 0.99}]
                    mock_pipeline.return_value = mock_classifier
                    
                    model = HuggingFaceTransformer("bert-base-uncased")
                    result = model.classify("Great!")
                    
                    assert result["label"] == "POSITIVE"
                    assert result["score"] == 0.99
    
    def test_cache_enabled(self):
        """Test Sofia Core caching is enabled"""
        with patch('backend.app.integrations.huggingface.AutoModel'):
            with patch('backend.app.integrations.huggingface.AutoTokenizer'):
                model = HuggingFaceTransformer("gpt2", use_sofia_cache=True)
                assert model.use_sofia_cache is True
    
    def test_cache_disabled(self):
        """Test Sofia Core caching can be disabled"""
        with patch('backend.app.integrations.huggingface.AutoModel'):
            with patch('backend.app.integrations.huggingface.AutoTokenizer'):
                model = HuggingFaceTransformer("gpt2", use_sofia_cache=False)
                assert model.use_sofia_cache is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
