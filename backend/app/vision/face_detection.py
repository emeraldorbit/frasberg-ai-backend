"""
Face Detection Module - Multiple backend support.

Supports:
- MediaPipe Face Detection (fast, accurate)
- OpenCV Haar Cascades (classic, lightweight)
- MTCNN (Multi-task Cascaded CNN)
- RetinaFace (state-of-the-art accuracy)
"""

import logging
from typing import List, Dict, Optional, Union, Tuple
from pathlib import Path
import numpy as np

logger = logging.getLogger(__name__)


class FaceDetection:
    """
    Face detection with multiple backend support.
    
    Example:
        >>> detector = FaceDetection(backend="mediapipe")
        >>> faces = detector.detect("photo.jpg")
        >>> print(f"Found {len(faces)} faces")
    """
    
    SUPPORTED_BACKENDS = ["mediapipe", "opencv", "mtcnn", "retinaface"]
    
    def __init__(
        self,
        backend: str = "mediapipe",
        min_confidence: float = 0.5,
        gpu: bool = False
    ):
        """
        Initialize face detector.
        
        Args:
            backend: Detection backend ("mediapipe", "opencv", "mtcnn", "retinaface")
            min_confidence: Minimum detection confidence (0.0-1.0)
            gpu: Use GPU acceleration if available
        """
        if backend not in self.SUPPORTED_BACKENDS:
            raise ValueError(f"Backend must be one of {self.SUPPORTED_BACKENDS}")
        
        self.backend = backend
        self.min_confidence = min_confidence
        self.gpu = gpu
        
        self._detector = None
        self._initialize_detector()
        
        logger.info(f"FaceDetection initialized with {backend} backend")
    
    def _initialize_detector(self):
        """Initialize the detection backend."""
        if self.backend == "mediapipe":
            self._initialize_mediapipe()
        elif self.backend == "opencv":
            self._initialize_opencv()
        elif self.backend == "mtcnn":
            self._initialize_mtcnn()
        elif self.backend == "retinaface":
            self._initialize_retinaface()
    
    def _initialize_mediapipe(self):
        """Initialize MediaPipe face detection."""
        try:
            import mediapipe as mp
            self._detector = mp.solutions.face_detection.FaceDetection(
                min_detection_confidence=self.min_confidence
            )
            logger.info("MediaPipe face detector initialized")
        except ImportError:
            logger.warning("MediaPipe not installed, falling back to OpenCV")
            self.backend = "opencv"
            self._initialize_opencv()
    
    def _initialize_opencv(self):
        """Initialize OpenCV Haar Cascade detector."""
        try:
            import cv2
            # Load pre-trained Haar Cascade
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            self._detector = cv2.CascadeClassifier(cascade_path)
            logger.info("OpenCV face detector initialized")
        except Exception as e:
            logger.error(f"Failed to initialize OpenCV detector: {e}")
            raise
    
    def _initialize_mtcnn(self):
        """Initialize MTCNN detector."""
        try:
            from mtcnn import MTCNN
            self._detector = MTCNN(min_face_size=20)
            logger.info("MTCNN face detector initialized")
        except ImportError:
            logger.warning("MTCNN not installed, falling back to OpenCV")
            self.backend = "opencv"
            self._initialize_opencv()
    
    def _initialize_retinaface(self):
        """Initialize RetinaFace detector."""
        try:
            from retinaface import RetinaFace
            self._detector = RetinaFace
            logger.info("RetinaFace detector initialized")
        except ImportError:
            logger.warning("RetinaFace not installed, falling back to MediaPipe")
            self.backend = "mediapipe"
            self._initialize_mediapipe()
    
    def detect(
        self,
        image: Union[str, Path, np.ndarray],
        return_landmarks: bool = False
    ) -> List[Dict]:
        """
        Detect faces in an image.
        
        Args:
            image: Image path or numpy array (BGR format)
            return_landmarks: Return facial landmarks if available
            
        Returns:
            List of detected faces with bounding boxes and confidence:
            [
                {
                    "x": 100,
                    "y": 150,
                    "width": 200,
                    "height": 250,
                    "confidence": 0.98,
                    "landmarks": {...}  # Optional
                }
            ]
        """
        # Load image if path provided
        if isinstance(image, (str, Path)):
            image = self._load_image(str(image))
        
        if self.backend == "mediapipe":
            return self._detect_mediapipe(image, return_landmarks)
        elif self.backend == "opencv":
            return self._detect_opencv(image)
        elif self.backend == "mtcnn":
            return self._detect_mtcnn(image, return_landmarks)
        elif self.backend == "retinaface":
            return self._detect_retinaface(image, return_landmarks)
    
    def _load_image(self, image_path: str) -> np.ndarray:
        """Load image from file."""
        try:
            import cv2
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError(f"Could not load image: {image_path}")
            return img
        except Exception as e:
            logger.error(f"Error loading image: {e}")
            raise
    
    def _detect_mediapipe(
        self,
        image: np.ndarray,
        return_landmarks: bool
    ) -> List[Dict]:
        """Detect faces using MediaPipe."""
        import cv2
        import mediapipe as mp
        
        # Convert BGR to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self._detector.process(rgb_image)
        
        faces = []
        if results.detections:
            h, w = image.shape[:2]
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
                
                face_dict = {
                    "x": int(bbox.xmin * w),
                    "y": int(bbox.ymin * h),
                    "width": int(bbox.width * w),
                    "height": int(bbox.height * h),
                    "confidence": detection.score[0]
                }
                
                if return_landmarks:
                    landmarks = {}
                    for idx, landmark in enumerate(detection.location_data.relative_keypoints):
                        landmarks[f"point_{idx}"] = {
                            "x": int(landmark.x * w),
                            "y": int(landmark.y * h)
                        }
                    face_dict["landmarks"] = landmarks
                
                faces.append(face_dict)
        
        return faces
    
    def _detect_opencv(self, image: np.ndarray) -> List[Dict]:
        """Detect faces using OpenCV Haar Cascades."""
        import cv2
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces_cv = self._detector.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        faces = []
        for (x, y, w, h) in faces_cv:
            faces.append({
                "x": int(x),
                "y": int(y),
                "width": int(w),
                "height": int(h),
                "confidence": 0.9  # OpenCV doesn't provide confidence
            })
        
        return faces
    
    def _detect_mtcnn(
        self,
        image: np.ndarray,
        return_landmarks: bool
    ) -> List[Dict]:
        """Detect faces using MTCNN."""
        import cv2
        
        # Convert BGR to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        detections = self._detector.detect_faces(rgb_image)
        
        faces = []
        for detection in detections:
            if detection['confidence'] >= self.min_confidence:
                bbox = detection['box']
                face_dict = {
                    "x": bbox[0],
                    "y": bbox[1],
                    "width": bbox[2],
                    "height": bbox[3],
                    "confidence": detection['confidence']
                }
                
                if return_landmarks:
                    face_dict["landmarks"] = detection['keypoints']
                
                faces.append(face_dict)
        
        return faces
    
    def _detect_retinaface(
        self,
        image: np.ndarray,
        return_landmarks: bool
    ) -> List[Dict]:
        """Detect faces using RetinaFace."""
        faces_dict = self._detector.detect_faces(image)
        
        faces = []
        for key, face_data in faces_dict.items():
            if face_data['score'] >= self.min_confidence:
                bbox = face_data['facial_area']
                face_dict = {
                    "x": bbox[0],
                    "y": bbox[1],
                    "width": bbox[2] - bbox[0],
                    "height": bbox[3] - bbox[1],
                    "confidence": face_data['score']
                }
                
                if return_landmarks:
                    face_dict["landmarks"] = face_data['landmarks']
                
                faces.append(face_dict)
        
        return faces
    
    def detect_batch(
        self,
        images: List[Union[str, Path, np.ndarray]],
        return_landmarks: bool = False
    ) -> List[List[Dict]]:
        """
        Detect faces in multiple images.
        
        Args:
            images: List of image paths or numpy arrays
            return_landmarks: Return facial landmarks if available
            
        Returns:
            List of face detection results for each image
        """
        results = []
        for image in images:
            faces = self.detect(image, return_landmarks)
            results.append(faces)
        
        return results
    
    def __del__(self):
        """Cleanup resources."""
        if hasattr(self, '_detector') and self._detector is not None:
            if self.backend == "mediapipe":
                try:
                    self._detector.close()
                except:
                    pass
