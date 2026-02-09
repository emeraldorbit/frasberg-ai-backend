"""
Speaker Identification Module - Voice biometrics and speaker recognition.

Features:
- Speaker enrollment (voice registration)
- Speaker identification (1:N)
- Speaker verification (1:1)
- Voice embedding generation
- Speaker database management
"""

import logging
from typing import List, Dict, Optional, Union
from pathlib import Path
import numpy as np
import json
from datetime import datetime

logger = logging.getLogger(__name__)


class SpeakerIdentification:
    """
    Speaker identification using voice biometrics.
    
    Example:
        >>> speaker_id = SpeakerIdentification()
        >>> speaker_id.enroll_speaker("john_voice.wav", "john123")
        >>> result = speaker_id.identify("unknown_voice.wav")
        >>> print(f"Speaker: {result['speaker_id']}")
    """
    
    def __init__(
        self,
        database_path: Optional[str] = None,
        similarity_threshold: float = 0.7
    ):
        """
        Initialize speaker identification system.
        
        Args:
            database_path: Path to store speaker database
            similarity_threshold: Threshold for speaker matching (0.0-1.0)
        """
        self.similarity_threshold = similarity_threshold
        self.database_path = database_path or "./speaker_database.json"
        
        self.speaker_database = self._load_database()
        
        self._model = None
        self._initialize_model()
        
        logger.info("SpeakerIdentification initialized")
    
    def _initialize_model(self):
        """Initialize speaker recognition model."""
        try:
            # For demonstration, using a simple approach
            # In production, use models like SpeechBrain, Resemblyzer, or PyAnnote
            import librosa
            self._model = "librosa"  # Placeholder
            logger.info("Speaker recognition model initialized")
        except ImportError:
            logger.error("Required audio libraries not installed")
            raise
    
    def _load_database(self) -> Dict:
        """Load speaker database from disk."""
        try:
            if Path(self.database_path).exists():
                with open(self.database_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Could not load database: {e}")
        
        return {"speakers": []}
    
    def _save_database(self):
        """Save speaker database to disk."""
        try:
            with open(self.database_path, 'w') as f:
                json.dump(self.speaker_database, f, indent=2)
        except Exception as e:
            logger.error(f"Could not save database: {e}")
    
    def generate_voice_embedding(
        self,
        audio: Union[str, Path, np.ndarray]
    ) -> np.ndarray:
        """
        Generate voice embedding (speaker representation).
        
        Args:
            audio: Audio file path or numpy array
            
        Returns:
            Voice embedding as numpy array
        """
        try:
            import librosa
            
            # Load audio
            if isinstance(audio, (str, Path)):
                y, sr = librosa.load(str(audio), sr=16000)
            else:
                y = audio
                sr = 16000
            
            # Extract MFCC features as a simple embedding
            # In production, use models like SpeechBrain x-vectors or d-vectors
            mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
            embedding = np.mean(mfcc, axis=1)
            
            return embedding
            
        except Exception as e:
            logger.error(f"Error generating voice embedding: {e}")
            raise
    
    def enroll_speaker(
        self,
        audio: Union[str, Path, np.ndarray],
        speaker_id: str,
        name: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> bool:
        """
        Enroll a speaker in the database.
        
        Args:
            audio: Audio sample of the speaker
            speaker_id: Unique speaker identifier
            name: Speaker's name
            metadata: Optional metadata
            
        Returns:
            Success status
        """
        try:
            # Generate voice embedding
            embedding = self.generate_voice_embedding(audio)
            
            # Create speaker entry
            speaker_entry = {
                "speaker_id": speaker_id,
                "name": name or speaker_id,
                "embedding": embedding.tolist(),
                "enrolled_at": datetime.now().isoformat(),
                "metadata": metadata or {}
            }
            
            # Add to database
            self.speaker_database["speakers"].append(speaker_entry)
            self._save_database()
            
            logger.info(f"Enrolled speaker: {speaker_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error enrolling speaker: {e}")
            return False
    
    def identify(
        self,
        audio: Union[str, Path, np.ndarray],
        top_k: int = 3
    ) -> Dict:
        """
        Identify speaker from audio.
        
        Args:
            audio: Audio containing unknown speaker
            top_k: Return top K matches
            
        Returns:
            Identification result:
            {
                "speaker_id": "john123",
                "name": "John Doe",
                "confidence": 0.96,
                "similarity": 0.89,
                "alternatives": [...]
            }
        """
        if len(self.speaker_database["speakers"]) == 0:
            logger.warning("Speaker database is empty. Enroll speakers first.")
            return {"speaker_id": "unknown", "confidence": 0.0}
        
        try:
            # Generate embedding for unknown speaker
            query_embedding = self.generate_voice_embedding(audio)
            
            # Compare with all enrolled speakers
            similarities = []
            
            for speaker in self.speaker_database["speakers"]:
                db_embedding = np.array(speaker["embedding"])
                similarity = self._cosine_similarity(query_embedding, db_embedding)
                
                similarities.append({
                    "speaker_id": speaker["speaker_id"],
                    "name": speaker["name"],
                    "similarity": float(similarity),
                    "confidence": float(similarity),
                    "metadata": speaker.get("metadata", {})
                })
            
            # Sort by similarity
            similarities.sort(key=lambda x: x["similarity"], reverse=True)
            
            # Get best match
            if similarities[0]["similarity"] >= self.similarity_threshold:
                result = similarities[0].copy()
                result["alternatives"] = similarities[1:top_k]
                return result
            else:
                return {
                    "speaker_id": "unknown",
                    "confidence": 0.0,
                    "alternatives": similarities[:top_k]
                }
        
        except Exception as e:
            logger.error(f"Error during identification: {e}")
            return {"speaker_id": "unknown", "confidence": 0.0}
    
    def verify(
        self,
        audio: Union[str, Path, np.ndarray],
        speaker_id: str
    ) -> Dict:
        """
        Verify if audio matches claimed speaker (1:1 verification).
        
        Args:
            audio: Audio to verify
            speaker_id: Claimed speaker ID
            
        Returns:
            Verification result:
            {
                "verified": True,
                "speaker_id": "john123",
                "confidence": 0.92
            }
        """
        try:
            # Find speaker in database
            speaker = next(
                (s for s in self.speaker_database["speakers"] if s["speaker_id"] == speaker_id),
                None
            )
            
            if not speaker:
                return {"verified": False, "speaker_id": speaker_id, "confidence": 0.0}
            
            # Generate embedding for verification audio
            query_embedding = self.generate_voice_embedding(audio)
            db_embedding = np.array(speaker["embedding"])
            
            # Calculate similarity
            similarity = self._cosine_similarity(query_embedding, db_embedding)
            
            return {
                "verified": similarity >= self.similarity_threshold,
                "speaker_id": speaker_id,
                "confidence": float(similarity)
            }
        
        except Exception as e:
            logger.error(f"Error during verification: {e}")
            return {"verified": False, "speaker_id": speaker_id, "confidence": 0.0}
    
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors."""
        vec1_norm = vec1 / np.linalg.norm(vec1)
        vec2_norm = vec2 / np.linalg.norm(vec2)
        return float(np.dot(vec1_norm, vec2_norm))
    
    def remove_speaker(self, speaker_id: str) -> bool:
        """
        Remove a speaker from the database.
        
        Args:
            speaker_id: Speaker ID to remove
            
        Returns:
            Success status
        """
        original_count = len(self.speaker_database["speakers"])
        self.speaker_database["speakers"] = [
            s for s in self.speaker_database["speakers"]
            if s["speaker_id"] != speaker_id
        ]
        
        removed = original_count - len(self.speaker_database["speakers"])
        if removed > 0:
            self._save_database()
            logger.info(f"Removed speaker: {speaker_id}")
            return True
        
        return False
    
    def list_enrolled_speakers(self) -> List[Dict]:
        """
        List all enrolled speakers.
        
        Returns:
            List of enrolled speakers (without embeddings)
        """
        return [
            {
                "speaker_id": s["speaker_id"],
                "name": s["name"],
                "enrolled_at": s["enrolled_at"],
                "metadata": s.get("metadata", {})
            }
            for s in self.speaker_database["speakers"]
        ]
    
    def get_database_stats(self) -> Dict:
        """
        Get database statistics.
        
        Returns:
            Database statistics
        """
        return {
            "total_speakers": len(self.speaker_database["speakers"]),
            "database_path": self.database_path,
            "similarity_threshold": self.similarity_threshold
        }
