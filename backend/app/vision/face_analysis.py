"""
Face Analysis Module - Age, Gender, Emotion Detection.

Analyzes facial attributes including:
- Age estimation
- Gender classification
- Emotion recognition (7 emotions)
- Facial features analysis
"""

import logging
from typing import List, Dict, Optional, Union
from pathlib import Path
import numpy as np

logger = logging.getLogger(__name__)


class FaceAnalysis:
    """
    Facial attribute analysis including age, gender, and emotion.
    
    Example:
        >>> analyzer = FaceAnalysis()
        >>> result = analyzer.analyze("person.jpg")
        >>> print(f"Age: {result['age']}, Gender: {result['gender']}, Emotion: {result['emotion']}")
    """
    
    EMOTIONS = ["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]
    
    def __init__(self, gpu: bool = False):
        """
        Initialize face analysis system.
        
        Args:
            gpu: Use GPU acceleration if available
        """
        self.gpu = gpu
        self._model = None
        self._detector = None
        self._initialize()
        
        logger.info("FaceAnalysis initialized")
    
    def _initialize(self):
        """Initialize face analysis models."""
        try:
            from deepface import DeepFace
            self._model = DeepFace
            logger.info("DeepFace models initialized")
        except ImportError:
            logger.error("DeepFace not installed. Install with: pip install deepface")
            raise
        
        # Initialize face detector
        from .face_detection import FaceDetection
        self._detector = FaceDetection(backend="mediapipe")
    
    def analyze(
        self,
        image: Union[str, Path, np.ndarray],
        actions: Optional[List[str]] = None
    ) -> Dict:
        """
        Analyze facial attributes.
        
        Args:
            image: Image path or numpy array
            actions: List of analysis actions ["age", "gender", "emotion", "race"]
                    Default: all actions
            
        Returns:
            Analysis results:
            {
                "age": 32,
                "gender": {
                    "dominant": "Man",
                    "confidence": {"Woman": 0.05, "Man": 0.95}
                },
                "emotion": {
                    "dominant": "happy",
                    "confidence": {
                        "angry": 0.01,
                        "disgust": 0.00,
                        "fear": 0.02,
                        "happy": 0.92,
                        "sad": 0.03,
                        "surprise": 0.01,
                        "neutral": 0.01
                    }
                },
                "confidence": 0.94
            }
        """
        if actions is None:
            actions = ["age", "gender", "emotion"]
        
        try:
            # Analyze using DeepFace
            result = self._model.analyze(
                img_path=str(image) if isinstance(image, (str, Path)) else image,
                actions=actions,
                enforce_detection=False,
                silent=True
            )
            
            # Extract results (handle both single face and multiple faces)
            if isinstance(result, list):
                result = result[0] if result else {}
            
            # Format output
            output = {}
            
            if "age" in actions and "age" in result:
                output["age"] = int(result["age"])
            
            if "gender" in actions and "gender" in result:
                output["gender"] = {
                    "dominant": result["dominant_gender"],
                    "confidence": result["gender"]
                }
            
            if "emotion" in actions and "emotion" in result:
                output["emotion"] = {
                    "dominant": result["dominant_emotion"],
                    "confidence": result["emotion"]
                }
            
            if "race" in actions and "race" in result:
                output["race"] = {
                    "dominant": result["dominant_race"],
                    "confidence": result["race"]
                }
            
            # Overall confidence (use emotion confidence as proxy)
            if "emotion" in output:
                emotion_conf = output["emotion"]["confidence"]
                dominant_emotion = output["emotion"]["dominant"]
                output["confidence"] = emotion_conf.get(dominant_emotion, 0.0)
            else:
                output["confidence"] = 1.0
            
            return output
            
        except Exception as e:
            logger.error(f"Error during analysis: {e}")
            return {"error": str(e)}
    
    def analyze_batch(
        self,
        images: List[Union[str, Path, np.ndarray]],
        actions: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Analyze multiple images.
        
        Args:
            images: List of image paths or numpy arrays
            actions: List of analysis actions
            
        Returns:
            List of analysis results
        """
        results = []
        for image in images:
            result = self.analyze(image, actions)
            results.append(result)
        
        return results
    
    def detect_emotion(self, image: Union[str, Path, np.ndarray]) -> Dict:
        """
        Detect emotion only.
        
        Args:
            image: Image path or numpy array
            
        Returns:
            Emotion analysis result
        """
        result = self.analyze(image, actions=["emotion"])
        return result.get("emotion", {})
    
    def estimate_age(self, image: Union[str, Path, np.ndarray]) -> int:
        """
        Estimate age only.
        
        Args:
            image: Image path or numpy array
            
        Returns:
            Estimated age
        """
        result = self.analyze(image, actions=["age"])
        return result.get("age", 0)
    
    def detect_gender(self, image: Union[str, Path, np.ndarray]) -> Dict:
        """
        Detect gender only.
        
        Args:
            image: Image path or numpy array
            
        Returns:
            Gender analysis result
        """
        result = self.analyze(image, actions=["gender"])
        return result.get("gender", {})
    
    def analyze_faces_in_image(
        self,
        image: Union[str, Path, np.ndarray],
        actions: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Analyze all faces detected in an image.
        
        Args:
            image: Image containing multiple faces
            actions: List of analysis actions
            
        Returns:
            List of analysis results for each face
        """
        # Load image
        if isinstance(image, (str, Path)):
            import cv2
            img = cv2.imread(str(image))
        else:
            img = image
        
        # Detect faces
        detected_faces = self._detector.detect(img)
        
        if len(detected_faces) == 0:
            logger.info("No faces detected in image")
            return []
        
        results = []
        
        # Analyze each face
        for face_bbox in detected_faces:
            x, y, w, h = face_bbox["x"], face_bbox["y"], face_bbox["width"], face_bbox["height"]
            
            # Extract face region with some padding
            padding = int(max(w, h) * 0.2)
            x1 = max(0, x - padding)
            y1 = max(0, y - padding)
            x2 = min(img.shape[1], x + w + padding)
            y2 = min(img.shape[0], y + h + padding)
            
            face_img = img[y1:y2, x1:x2]
            
            try:
                # Analyze this face
                analysis = self.analyze(face_img, actions)
                analysis["bbox"] = face_bbox
                results.append(analysis)
            except Exception as e:
                logger.warning(f"Could not analyze face: {e}")
                continue
        
        return results
    
    def get_emotion_from_expression(
        self,
        image: Union[str, Path, np.ndarray]
    ) -> str:
        """
        Get dominant emotion name only.
        
        Args:
            image: Image path or numpy array
            
        Returns:
            Dominant emotion name (e.g., "happy", "sad")
        """
        result = self.detect_emotion(image)
        return result.get("dominant", "neutral")
