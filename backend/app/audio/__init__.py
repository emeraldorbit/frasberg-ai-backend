"""
Sofia Core Audio Module - Voice Recognition and Analysis.

Provides comprehensive audio processing capabilities including:
- Speech-to-text (Whisper)
- Speaker identification (voice biometrics)
- Speaker diarization (who spoke when)
- Voice emotion detection
- Real-time audio processing
"""

from .speech_to_text import SpeechToText
from .speaker_identification import SpeakerIdentification
from .speaker_diarization import SpeakerDiarization
from .voice_emotion import VoiceEmotionDetection
from .voice_activity import VoiceActivityDetection

__all__ = [
    "SpeechToText",
    "SpeakerIdentification",
    "SpeakerDiarization",
    "VoiceEmotionDetection",
    "VoiceActivityDetection",
]

__version__ = "6.6.0"
