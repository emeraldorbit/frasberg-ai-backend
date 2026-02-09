"""
Sofia Core Vision Module - Face Recognition and Analysis.

Provides comprehensive computer vision capabilities including:
- Face detection (multiple backends)
- Face recognition with deep learning embeddings
- Face analysis (age, gender, emotion)
- Real-time video processing
"""

from .face_detection import FaceDetection
from .face_recognition import FaceRecognition
from .face_analysis import FaceAnalysis
from .video_stream import VideoStream

__all__ = [
    "FaceDetection",
    "FaceRecognition",
    "FaceAnalysis",
    "VideoStream",
]

__version__ = "6.6.0"
