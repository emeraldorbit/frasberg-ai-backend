"""
Face Recognition Module - Deep learning-based face recognition.

Features:
- Face embedding generation (512-D vectors)
- 1:1 face verification
- 1:N face identification
- Face database management
- Multiple model architectures support
"""

import logging
from typing import List, Dict, Optional, Union, Tuple
from pathlib import Path
import numpy as np
import json
from datetime import datetime

logger = logging.getLogger(__name__)


class FaceRecognition:
    """
    Face recognition with deep learning embeddings.
    
    Example:
        >>> recognizer = FaceRecognition(model_name="Facenet")
        >>> recognizer.register_face("john.jpg", "John Doe", "user123")
        >>> results = recognizer.recognize("group_photo.jpg")
    """
    
    SUPPORTED_MODELS = ["Facenet", "Facenet512", "VGG-Face", "ArcFace", "DeepFace"]
    
    def __init__(
        self,
        model_name: str = "Facenet",
        database_path: Optional[str] = None,
        similarity_threshold: float = 0.6,
        gpu: bool = False
    ):
        """
        Initialize face recognition system.
        
        Args:
            model_name: Model architecture ("Facenet", "VGG-Face", "ArcFace", etc.)
            database_path: Path to store face database
            similarity_threshold: Threshold for face matching (0.0-1.0)
            gpu: Use GPU acceleration if available
        """
        if model_name not in self.SUPPORTED_MODELS:
            logger.warning(f"Model {model_name} not in supported list, using Facenet")
            model_name = "Facenet"
        
        self.model_name = model_name
        self.similarity_threshold = similarity_threshold
        self.gpu = gpu
        
        # Face database
        self.database_path = database_path or "./face_database.json"
        self.face_database = self._load_database()
        
        # Initialize model
        self._model = None
        self._detector = None
        self._initialize_model()
        
        logger.info(f"FaceRecognition initialized with {model_name}")
    
    def _initialize_model(self):
        """Initialize the face recognition model."""
        try:
            from deepface import DeepFace
            # DeepFace will automatically download and initialize the model
            self._model = DeepFace
            logger.info(f"{self.model_name} model initialized")
        except ImportError:
            logger.error("DeepFace not installed. Install with: pip install deepface")
            raise
        
        # Initialize face detector
        from .face_detection import FaceDetection
        self._detector = FaceDetection(backend="mediapipe")
    
    def _load_database(self) -> Dict:
        """Load face database from disk."""
        try:
            if Path(self.database_path).exists():
                with open(self.database_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Could not load database: {e}")
        
        return {"faces": []}
    
    def _save_database(self):
        """Save face database to disk."""
        try:
            with open(self.database_path, 'w') as f:
                json.dump(self.face_database, f, indent=2)
        except Exception as e:
            logger.error(f"Could not save database: {e}")
    
    def generate_embedding(
        self,
        image: Union[str, Path, np.ndarray]
    ) -> np.ndarray:
        """
        Generate face embedding vector.
        
        Args:
            image: Image path or numpy array
            
        Returns:
            Face embedding as numpy array (typically 512-D)
        """
        try:
            # Generate embedding using DeepFace
            embedding = self._model.represent(
                img_path=str(image) if isinstance(image, (str, Path)) else image,
                model_name=self.model_name,
                enforce_detection=False
            )
            
            if isinstance(embedding, list) and len(embedding) > 0:
                return np.array(embedding[0]["embedding"])
            elif isinstance(embedding, dict):
                return np.array(embedding["embedding"])
            else:
                return np.array(embedding)
                
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise
    
    def register_face(
        self,
        image: Union[str, Path, np.ndarray],
        name: str,
        user_id: str,
        metadata: Optional[Dict] = None
    ) -> bool:
        """
        Register a face in the database.
        
        Args:
            image: Image containing the face
            name: Person's name
            user_id: Unique user identifier
            metadata: Optional metadata to store
            
        Returns:
            Success status
        """
        try:
            # Generate embedding
            embedding = self.generate_embedding(image)
            
            # Create face entry
            face_entry = {
                "user_id": user_id,
                "name": name,
                "embedding": embedding.tolist(),
                "registered_at": datetime.now().isoformat(),
                "metadata": metadata or {}
            }
            
            # Add to database
            self.face_database["faces"].append(face_entry)
            self._save_database()
            
            logger.info(f"Registered face for {name} (ID: {user_id})")
            return True
            
        except Exception as e:
            logger.error(f"Error registering face: {e}")
            return False
    
    def recognize(
        self,
        image: Union[str, Path, np.ndarray],
        top_k: int = 5
    ) -> List[Dict]:
        """
        Recognize faces in an image.
        
        Args:
            image: Image containing faces to recognize
            top_k: Return top K matches for each face
            
        Returns:
            List of recognized faces with confidence scores:
            [
                {
                    "name": "John Doe",
                    "user_id": "user123",
                    "confidence": 0.98,
                    "similarity": 0.85,
                    "bbox": {"x": 100, "y": 150, "width": 200, "height": 250}
                }
            ]
        """
        if len(self.face_database["faces"]) == 0:
            logger.warning("Face database is empty. Register faces first.")
            return []
        
        try:
            # Detect faces in image
            detected_faces = self._detector.detect(image)
            
            if len(detected_faces) == 0:
                logger.info("No faces detected in image")
                return []
            
            # Load image
            if isinstance(image, (str, Path)):
                import cv2
                img = cv2.imread(str(image))
            else:
                img = image
            
            results = []
            
            # Process each detected face
            for face_bbox in detected_faces:
                # Extract face region
                x, y, w, h = face_bbox["x"], face_bbox["y"], face_bbox["width"], face_bbox["height"]
                face_img = img[y:y+h, x:x+w]
                
                # Generate embedding for detected face
                try:
                    face_embedding = self.generate_embedding(face_img)
                    
                    # Compare with database
                    matches = self._find_matches(face_embedding, top_k)
                    
                    if matches:
                        # Add bounding box to best match
                        best_match = matches[0].copy()
                        best_match["bbox"] = face_bbox
                        results.append(best_match)
                
                except Exception as e:
                    logger.warning(f"Could not process face: {e}")
                    continue
            
            return results
            
        except Exception as e:
            logger.error(f"Error during recognition: {e}")
            return []
    
    def _find_matches(
        self,
        query_embedding: np.ndarray,
        top_k: int = 5
    ) -> List[Dict]:
        """Find matching faces in database."""
        matches = []
        
        for face_entry in self.face_database["faces"]:
            db_embedding = np.array(face_entry["embedding"])
            
            # Calculate cosine similarity
            similarity = self._cosine_similarity(query_embedding, db_embedding)
            
            if similarity >= self.similarity_threshold:
                matches.append({
                    "name": face_entry["name"],
                    "user_id": face_entry["user_id"],
                    "similarity": float(similarity),
                    "confidence": float(similarity),  # Use similarity as confidence
                    "metadata": face_entry.get("metadata", {})
                })
        
        # Sort by similarity and return top K
        matches.sort(key=lambda x: x["similarity"], reverse=True)
        return matches[:top_k]
    
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors."""
        vec1_norm = vec1 / np.linalg.norm(vec1)
        vec2_norm = vec2 / np.linalg.norm(vec2)
        return float(np.dot(vec1_norm, vec2_norm))
    
    def verify(
        self,
        image1: Union[str, Path, np.ndarray],
        image2: Union[str, Path, np.ndarray]
    ) -> Dict:
        """
        Verify if two images contain the same person (1:1 verification).
        
        Args:
            image1: First image
            image2: Second image
            
        Returns:
            Verification result:
            {
                "verified": True,
                "similarity": 0.89,
                "confidence": 0.89
            }
        """
        try:
            result = self._model.verify(
                img1_path=str(image1) if isinstance(image1, (str, Path)) else image1,
                img2_path=str(image2) if isinstance(image2, (str, Path)) else image2,
                model_name=self.model_name,
                enforce_detection=False
            )
            
            return {
                "verified": result["verified"],
                "similarity": result["distance"],
                "confidence": 1.0 - result["distance"]  # Convert distance to confidence
            }
            
        except Exception as e:
            logger.error(f"Error during verification: {e}")
            return {"verified": False, "similarity": 0.0, "confidence": 0.0}
    
    def remove_face(self, user_id: str) -> bool:
        """
        Remove a face from the database.
        
        Args:
            user_id: User ID to remove
            
        Returns:
            Success status
        """
        original_count = len(self.face_database["faces"])
        self.face_database["faces"] = [
            face for face in self.face_database["faces"]
            if face["user_id"] != user_id
        ]
        
        removed = original_count - len(self.face_database["faces"])
        if removed > 0:
            self._save_database()
            logger.info(f"Removed {removed} face(s) for user {user_id}")
            return True
        
        return False
    
    def list_registered_faces(self) -> List[Dict]:
        """
        List all registered faces.
        
        Returns:
            List of registered faces (without embeddings)
        """
        return [
            {
                "user_id": face["user_id"],
                "name": face["name"],
                "registered_at": face["registered_at"],
                "metadata": face.get("metadata", {})
            }
            for face in self.face_database["faces"]
        ]
    
    def get_database_stats(self) -> Dict:
        """
        Get database statistics.
        
        Returns:
            Database statistics
        """
        return {
            "total_faces": len(self.face_database["faces"]),
            "model": self.model_name,
            "database_path": self.database_path,
            "similarity_threshold": self.similarity_threshold
        }
