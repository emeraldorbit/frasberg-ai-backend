"""
Speech-to-Text Module - OpenAI Whisper integration.

Features:
- Multi-language support (100+ languages)
- Real-time transcription
- Timestamp generation
- High accuracy speech recognition
- Multiple model sizes
"""

import logging
from typing import List, Dict, Optional, Union, Callable
from pathlib import Path
import numpy as np

logger = logging.getLogger(__name__)


class SpeechToText:
    """
    Speech-to-text using OpenAI Whisper.
    
    Example:
        >>> stt = SpeechToText(model_size="base")
        >>> text = stt.transcribe("meeting.wav")
        >>> print(text)
    """
    
    MODEL_SIZES = ["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"]
    
    def __init__(
        self,
        model_size: str = "base",
        language: Optional[str] = None,
        device: str = "cpu"
    ):
        """
        Initialize speech-to-text system.
        
        Args:
            model_size: Whisper model size ("tiny", "base", "small", "medium", "large")
            language: Source language (ISO 639-1 code), None for auto-detect
            device: Device to use ("cpu" or "cuda")
        """
        if model_size not in self.MODEL_SIZES:
            logger.warning(f"Model size {model_size} not recognized, using 'base'")
            model_size = "base"
        
        self.model_size = model_size
        self.language = language
        self.device = device
        
        self._model = None
        self._initialize_model()
        
        logger.info(f"SpeechToText initialized with {model_size} model")
    
    def _initialize_model(self):
        """Initialize Whisper model."""
        try:
            import whisper
            self._model = whisper.load_model(self.model_size, device=self.device)
            logger.info(f"Whisper {self.model_size} model loaded")
        except ImportError:
            logger.error("Whisper not installed. Install with: pip install openai-whisper")
            raise
        except Exception as e:
            logger.error(f"Error loading Whisper model: {e}")
            raise
    
    def transcribe(
        self,
        audio: Union[str, Path, np.ndarray],
        language: Optional[str] = None
    ) -> str:
        """
        Transcribe audio to text.
        
        Args:
            audio: Audio file path or numpy array
            language: Override default language
            
        Returns:
            Transcribed text
        """
        try:
            result = self._model.transcribe(
                str(audio) if isinstance(audio, (str, Path)) else audio,
                language=language or self.language,
                verbose=False
            )
            
            return result["text"].strip()
            
        except Exception as e:
            logger.error(f"Error during transcription: {e}")
            return ""
    
    def transcribe_with_timestamps(
        self,
        audio: Union[str, Path, np.ndarray],
        language: Optional[str] = None
    ) -> List[Dict]:
        """
        Transcribe audio with word-level timestamps.
        
        Args:
            audio: Audio file path or numpy array
            language: Override default language
            
        Returns:
            List of segments with timestamps:
            [
                {
                    "start": 0.0,
                    "end": 2.5,
                    "text": "Hello world"
                }
            ]
        """
        try:
            result = self._model.transcribe(
                str(audio) if isinstance(audio, (str, Path)) else audio,
                language=language or self.language,
                verbose=False,
                word_timestamps=True
            )
            
            segments = []
            for segment in result["segments"]:
                segments.append({
                    "start": segment["start"],
                    "end": segment["end"],
                    "text": segment["text"].strip()
                })
            
            return segments
            
        except Exception as e:
            logger.error(f"Error during transcription: {e}")
            return []
    
    def transcribe_batch(
        self,
        audio_files: List[Union[str, Path]],
        language: Optional[str] = None
    ) -> List[str]:
        """
        Transcribe multiple audio files.
        
        Args:
            audio_files: List of audio file paths
            language: Override default language
            
        Returns:
            List of transcribed texts
        """
        results = []
        for audio_file in audio_files:
            text = self.transcribe(audio_file, language)
            results.append(text)
        
        return results
    
    def stream_transcribe(
        self,
        source: str = "microphone",
        callback: Optional[Callable[[str], None]] = None,
        language: Optional[str] = None,
        chunk_duration: int = 5
    ):
        """
        Real-time streaming transcription.
        
        Args:
            source: Audio source ("microphone" or audio stream)
            callback: Function to call with transcribed text
            language: Override default language
            chunk_duration: Duration of audio chunks in seconds
        """
        try:
            import pyaudio
            import wave
            import tempfile
            import os
            
            # Audio settings
            CHUNK = 1024
            FORMAT = pyaudio.paInt16
            CHANNELS = 1
            RATE = 16000
            
            p = pyaudio.PyAudio()
            
            stream = p.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK
            )
            
            logger.info("Started real-time transcription...")
            
            frames = []
            frame_count = 0
            max_frames = int(RATE / CHUNK * chunk_duration)
            
            try:
                while True:
                    data = stream.read(CHUNK, exception_on_overflow=False)
                    frames.append(data)
                    frame_count += 1
                    
                    # Process chunk when accumulated enough frames
                    if frame_count >= max_frames:
                        # Save to temporary file
                        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                            temp_path = temp_file.name
                            wf = wave.open(temp_path, 'wb')
                            wf.setnchannels(CHANNELS)
                            wf.setsampwidth(p.get_sample_size(FORMAT))
                            wf.setframerate(RATE)
                            wf.writeframes(b''.join(frames))
                            wf.close()
                        
                        # Transcribe chunk
                        text = self.transcribe(temp_path, language)
                        
                        # Cleanup
                        os.unlink(temp_path)
                        
                        # Call callback
                        if callback and text:
                            callback(text)
                        
                        # Reset for next chunk
                        frames = []
                        frame_count = 0
            
            except KeyboardInterrupt:
                logger.info("Stopped transcription")
            
            finally:
                stream.stop_stream()
                stream.close()
                p.terminate()
        
        except ImportError:
            logger.error("PyAudio not installed. Install with: pip install pyaudio")
        except Exception as e:
            logger.error(f"Error during streaming transcription: {e}")
    
    def detect_language(
        self,
        audio: Union[str, Path, np.ndarray]
    ) -> Dict:
        """
        Detect the language spoken in audio.
        
        Args:
            audio: Audio file path or numpy array
            
        Returns:
            Language detection result:
            {
                "language": "en",
                "language_name": "English",
                "confidence": 0.98
            }
        """
        try:
            # Load audio
            import whisper
            audio_data = whisper.load_audio(str(audio) if isinstance(audio, (str, Path)) else audio)
            audio_data = whisper.pad_or_trim(audio_data)
            
            # Make log-Mel spectrogram
            mel = whisper.log_mel_spectrogram(audio_data).to(self._model.device)
            
            # Detect language
            _, probs = self._model.detect_language(mel)
            
            # Get top language
            top_lang = max(probs, key=probs.get)
            
            return {
                "language": top_lang,
                "language_name": whisper.tokenizer.LANGUAGES[top_lang],
                "confidence": probs[top_lang]
            }
            
        except Exception as e:
            logger.error(f"Error detecting language: {e}")
            return {"language": "unknown", "language_name": "Unknown", "confidence": 0.0}
    
    def get_model_info(self) -> Dict:
        """
        Get information about the loaded model.
        
        Returns:
            Model information
        """
        return {
            "model_size": self.model_size,
            "language": self.language or "auto-detect",
            "device": self.device,
            "supported_languages": len(self._model.tokenizer.all_language_tokens) if self._model else 0
        }
