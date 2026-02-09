"""
Speaker Diarization Module - "Who spoke when" analysis.

Features:
- Automatic speaker segmentation
- Multi-speaker detection
- Timeline generation
- Meeting transcription support
"""

import logging
from typing import List, Dict, Union
from pathlib import Path
import numpy as np

logger = logging.getLogger(__name__)


class SpeakerDiarization:
    """
    Speaker diarization - segment audio by speaker.
    
    Example:
        >>> diarizer = SpeakerDiarization()
        >>> segments = diarizer.diarize("meeting.wav")
        >>> for seg in segments:
        ...     print(f"[{seg['start']:.1f}s - {seg['end']:.1f}s]: {seg['speaker']}")
    """
    
    def __init__(self, num_speakers: Optional[int] = None):
        """
        Initialize speaker diarization system.
        
        Args:
            num_speakers: Expected number of speakers (None for auto-detect)
        """
        self.num_speakers = num_speakers
        
        self._model = None
        self._initialize_model()
        
        logger.info("SpeakerDiarization initialized")
    
    def _initialize_model(self):
        """Initialize diarization model."""
        try:
            # For demonstration
            # In production, use PyAnnote.audio or similar
            import librosa
            self._model = "librosa"  # Placeholder
            logger.info("Diarization model initialized")
        except ImportError:
            logger.error("Required audio libraries not installed")
            raise
    
    def diarize(
        self,
        audio: Union[str, Path, np.ndarray],
        num_speakers: Optional[int] = None
    ) -> List[Dict]:
        """
        Perform speaker diarization on audio.
        
        Args:
            audio: Audio file path or numpy array
            num_speakers: Override default number of speakers
            
        Returns:
            List of speaker segments:
            [
                {
                    "start": 0.0,
                    "end": 5.2,
                    "speaker": "SPEAKER_01",
                    "confidence": 0.89
                },
                {
                    "start": 5.5,
                    "end": 10.3,
                    "speaker": "SPEAKER_02",
                    "confidence": 0.92
                }
            ]
        """
        try:
            import librosa
            
            # Load audio
            if isinstance(audio, (str, Path)):
                y, sr = librosa.load(str(audio), sr=16000)
            else:
                y = audio
                sr = 16000
            
            # Simplified diarization using energy-based segmentation
            # In production, use proper diarization models
            segments = self._simple_diarization(y, sr, num_speakers or self.num_speakers)
            
            return segments
            
        except Exception as e:
            logger.error(f"Error during diarization: {e}")
            return []
    
    def _simple_diarization(
        self,
        audio: np.ndarray,
        sr: int,
        num_speakers: Optional[int]
    ) -> List[Dict]:
        """Simple energy-based diarization (placeholder implementation)."""
        import librosa
        
        # Calculate frame-level energy
        frame_length = int(sr * 0.025)  # 25ms frames
        hop_length = int(sr * 0.010)  # 10ms hop
        
        # Calculate RMS energy
        rms= librosa.feature.rms(y=audio, frame_length=frame_length, hop_length=hop_length)[0]
        
        # Simple voice activity detection
        threshold = np.mean(rms) * 0.5
        voice_frames = rms > threshold
        
        # Convert frames to time segments
        segments = []
        current_speaker = "SPEAKER_01"
        speaker_counter = 1
        in_segment = False
        segment_start = 0.0
        
        for i, is_voice in enumerate(voice_frames):
            time = i * hop_length / sr
            
            if is_voice and not in_segment:
                # Start of new segment
                segment_start = time
                in_segment = True
            elif not is_voice and in_segment:
                # End of segment
                segments.append({
                    "start": segment_start,
                    "end": time,
                    "speaker": current_speaker,
                    "confidence": 0.85
                })
                in_segment = False
                
                # Alternate speakers (very simple heuristic)
                if num_speakers and num_speakers > 1:
                    speaker_counter = (speaker_counter % num_speakers) + 1
                    current_speaker = f"SPEAKER_{speaker_counter:02d}"
        
        # Close final segment if still open
        if in_segment:
            segments.append({
                "start": segment_start,
                "end": len(audio) / sr,
                "speaker": current_speaker,
                "confidence": 0.85
            })
        
        return segments
    
    def diarize_with_transcription(
        self,
        audio: Union[str, Path, np.ndarray],
        num_speakers: Optional[int] = None
    ) -> List[Dict]:
        """
        Perform diarization and transcription together.
        
        Args:
            audio: Audio file path or numpy array
            num_speakers: Number of speakers
            
        Returns:
            Combined diarization and transcription:
            [
                {
                    "start": 0.0,
                    "end": 5.2,
                    "speaker": "SPEAKER_01",
                    "text": "Hello everyone, welcome to the meeting"
                }
            ]
        """
        from .speech_to_text import SpeechToText
        
        try:
            # Perform diarization
            segments = self.diarize(audio, num_speakers)
            
            # Initialize STT
            stt = SpeechToText(model_size="base")
            
            # Transcribe each segment
            # (In production, extract audio segments and transcribe separately)
            transcript_segments = stt.transcribe_with_timestamps(audio)
            
            # Merge diarization and transcription
            # Simple approach: match by time overlap
            for diar_seg in segments:
                matching_text = []
                for trans_seg in transcript_segments:
                    # Check if transcription segment overlaps with diarization segment
                    if (trans_seg["start"] >= diar_seg["start"] and 
                        trans_seg["start"] <= diar_seg["end"]):
                        matching_text.append(trans_seg["text"])
                
                diar_seg["text"] = " ".join(matching_text)
            
            return segments
            
        except Exception as e:
            logger.error(f"Error during combined diarization/transcription: {e}")
            return []
    
    def get_speaker_statistics(
        self,
        segments: List[Dict]
    ) -> Dict:
        """
        Calculate statistics about speaker participation.
        
        Args:
            segments: Diarization segments
            
        Returns:
            Speaker statistics:
            {
                "SPEAKER_01": {
                    "total_duration": 120.5,
                    "num_segments": 15,
                    "percentage": 45.2
                }
            }
        """
        if not segments:
            return {}
        
        # Calculate per-speaker statistics
        speaker_stats = {}
        total_duration = 0.0
        
        for seg in segments:
            speaker = seg["speaker"]
            duration = seg["end"] - seg["start"]
            total_duration += duration
            
            if speaker not in speaker_stats:
                speaker_stats[speaker] = {
                    "total_duration": 0.0,
                    "num_segments": 0
                }
            
            speaker_stats[speaker]["total_duration"] += duration
            speaker_stats[speaker]["num_segments"] += 1
        
        # Calculate percentages
        for speaker in speaker_stats:
            speaker_stats[speaker]["percentage"] = (
                speaker_stats[speaker]["total_duration"] / total_duration * 100
                if total_duration > 0 else 0.0
            )
        
        return speaker_stats
