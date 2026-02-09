"""
Voice Activity Detection (VAD) - Detect speech vs non-speech segments.

Features:
- Detect speech segments in audio
- Filter out silence and noise
- Real-time VAD
- Multiple VAD backends
"""

import logging
from typing import List, Dict, Union
from pathlib import Path
import numpy as np

logger = logging.getLogger(__name__)


class VoiceActivityDetection:
    """
    Voice activity detection - identify speech segments.
    
    Example:
        >>> vad = VoiceActivityDetection()
        >>> segments = vad.detect("recording.wav")
        >>> for seg in segments:
        ...     if seg['is_speech']:
        ...         print(f"Speech: {seg['start']:.1f}s - {seg['end']:.1f}s")
    """
    
    def __init__(
        self,
        aggressiveness: int = 2,
        frame_duration_ms: int = 30
    ):
        """
        Initialize VAD system.
        
        Args:
            aggressiveness: VAD aggressiveness (0-3, higher = more aggressive filtering)
            frame_duration_ms: Frame duration in milliseconds (10, 20, or 30)
        """
        self.aggressiveness = aggressiveness
        self.frame_duration_ms = frame_duration_ms
        
        self._vad = None
        self._initialize_vad()
        
        logger.info("VoiceActivityDetection initialized")
    
    def _initialize_vad(self):
        """Initialize VAD engine."""
        try:
            import webrtcvad
            self._vad = webrtcvad.Vad(self.aggressiveness)
            logger.info(f"WebRTC VAD initialized (aggressiveness: {self.aggressiveness})")
        except ImportError:
            logger.warning("webrtcvad not installed, using energy-based VAD")
            self._vad = "energy"  # Fallback to energy-based VAD
    
    def detect(
        self,
        audio: Union[str, Path, np.ndarray],
        sample_rate: int = 16000
    ) -> List[Dict]:
        """
        Detect voice activity in audio.
        
        Args:
            audio: Audio file path or numpy array
            sample_rate: Audio sample rate (must be 8000, 16000, 32000, or 48000)
            
        Returns:
            List of segments:
            [
                {
                    "start": 1.2,
                    "end": 5.8,
                    "is_speech": True,
                    "confidence": 0.95
                }
            ]
        """
        try:
            # Load audio
            if isinstance(audio, (str, Path)):
                import librosa
                y, sr = librosa.load(str(audio), sr=sample_rate)
            else:
                y = audio
                sr = sample_rate
            
            # Detect speech segments
            if isinstance(self._vad, str) and self._vad == "energy":
                segments = self._energy_based_vad(y, sr)
            else:
                segments = self._webrtc_vad(y, sr)
            
            return segments
            
        except Exception as e:
            logger.error(f"Error during VAD: {e}")
            return []
    
    def _webrtc_vad(self, audio: np.ndarray, sr: int) -> List[Dict]:
        """WebRTC-based VAD."""
        # Convert to int16
        audio_int16 = (audio * 32768).astype(np.int16)
        
        # Frame parameters
        frame_duration_samples = int(sr * self.frame_duration_ms / 1000)
        
        segments = []
        current_segment = None
        
        # Process frames
        for i in range(0, len(audio_int16), frame_duration_samples):
            frame = audio_int16[i:i+frame_duration_samples]
            
            # Pad last frame if necessary
            if len(frame) < frame_duration_samples:
                frame = np.pad(frame, (0, frame_duration_samples - len(frame)))
            
            # Convert to bytes
            frame_bytes = frame.tobytes()
            
            # Check if speech
            is_speech = self._vad.is_speech(frame_bytes, sr)
            
            time = i / sr
            
            if is_speech:
                if current_segment is None:
                    # Start new speech segment
                    current_segment = {
                        "start": time,
                        "is_speech": True,
                        "confidence": 0.9
                    }
            else:
                if current_segment is not None:
                    # End speech segment
                    current_segment["end"] = time
                    segments.append(current_segment)
                    current_segment = None
                    
                    # Add silence segment
                    if segments and time > segments[-1]["end"]:
                        segments.append({
                            "start": segments[-1]["end"],
                            "end": time,
                            "is_speech": False,
                            "confidence": 0.9
                        })
        
        # Close final segment if still open
        if current_segment is not None:
            current_segment["end"] = len(audio_int16) / sr
            segments.append(current_segment)
        
        return segments
    
    def _energy_based_vad(self, audio: np.ndarray, sr: int) -> List[Dict]:
        """Energy-based VAD (fallback method)."""
        import librosa
        
        # Calculate frame-level energy
        frame_length = int(sr * 0.025)  # 25ms
        hop_length = int(sr * 0.010)  # 10ms
        
        # Calculate RMS energy
        rms = librosa.feature.rms(y=audio, frame_length=frame_length, hop_length=hop_length)[0]
        
        # Calculate threshold (median + offset)
        threshold = np.median(rms) * 1.5
        
        # Detect speech frames
        speech_frames = rms > threshold
        
        segments = []
        in_speech = False
        segment_start = 0.0
        
        for i, is_speech in enumerate(speech_frames):
            time = i * hop_length / sr
            
            if is_speech and not in_speech:
                # Start of speech
                segment_start = time
                in_speech = True
            elif not is_speech and in_speech:
                # End of speech
                segments.append({
                    "start": segment_start,
                    "end": time,
                    "is_speech": True,
                    "confidence": 0.8  # Lower confidence for energy-based
                })
                in_speech = False
        
        # Close final segment
        if in_speech:
            segments.append({
                "start": segment_start,
                "end": len(audio) / sr,
                "is_speech": True,
                "confidence": 0.8
            })
        
        return segments
    
    def get_speech_ratio(self, segments: List[Dict]) -> float:
        """
        Calculate ratio of speech to total duration.
        
        Args:
            segments: VAD segments
            
        Returns:
            Speech ratio (0.0 to 1.0)
        """
        if not segments:
            return 0.0
        
        total_duration = segments[-1]["end"]
        speech_duration = sum(
            seg["end"] - seg["start"]
            for seg in segments
            if seg["is_speech"]
        )
        
        return speech_duration / total_duration if total_duration > 0 else 0.0
    
    def filter_speech_segments(
        self,
        audio: Union[str, Path, np.ndarray],
        min_duration: float = 0.5
    ) -> List[np.ndarray]:
        """
        Extract speech segments from audio, filtering out silence.
        
        Args:
            audio: Input audio
            min_duration: Minimum segment duration in seconds
            
        Returns:
            List of speech segment arrays
        """
        import librosa
        
        # Load audio
        if isinstance(audio, (str, Path)):
            y, sr = librosa.load(str(audio), sr=16000)
        else:
            y = audio
            sr = 16000
        
        # Detect segments
        segments = self.detect(y, sr)
        
        # Extract speech segments
        speech_segments = []
        for seg in segments:
            if seg["is_speech"]:
                duration = seg["end"] - seg["start"]
                if duration >= min_duration:
                    start_sample = int(seg["start"] * sr)
                    end_sample = int(seg["end"] * sr)
                    speech_segments.append(y[start_sample:end_sample])
        
        return speech_segments
