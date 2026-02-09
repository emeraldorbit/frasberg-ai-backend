"""
Video Stream Processing - Real-time face recognition and analysis.

Features:
- Real-time face detection in video streams
- Live face recognition
- Stream from webcam, video file, or RTSP
- Frame buffering and processing
"""

import logging
from typing import Callable, Optional, Dict, List
import time
import threading

logger = logging.getLogger(__name__)


class VideoStream:
    """
    Real-time video stream processing for face recognition.
    
    Example:
        >>> stream = VideoStream(source="webcam")
        >>> stream.start(callback=lambda frame, faces: print(f"Found {len(faces)} faces"))
    """
    
    def __init__(
        self,
        source: str = "webcam",
        fps: int = 30,
        resolution: tuple = (640, 480)
    ):
        """
        Initialize video stream processor.
        
        Args:
            source: Video source ("webcam", file path, or RTSP URL)
            fps: Target frames per second
            resolution: Video resolution (width, height)
        """
        self.source = source
        self.fps = fps
        self.resolution = resolution
        
        self._cap = None
        self._running = False
        self._thread = None
        
        self._detector = None
        self._recognizer = None
        
        logger.info(f"VideoStream initialized for {source}")
    
    def initialize(
        self,
        enable_detection: bool = True,
        enable_recognition: bool = False,
        enable_analysis: bool = False
    ):
        """
        Initialize processing components.
        
        Args:
            enable_detection: Enable face detection
            enable_recognition: Enable face recognition
            enable_analysis: Enable face analysis (age, gender, emotion)
        """
        if enable_detection:
            from .face_detection import FaceDetection
            self._detector = FaceDetection(backend="mediapipe")
        
        if enable_recognition:
            from .face_recognition import FaceRecognition
            self._recognizer = FaceRecognition()
        
        if enable_analysis:
            from .face_analysis import FaceAnalysis
            self._analyzer = FaceAnalysis()
    
    def start(
        self,
        callback: Callable[[object, List[Dict]], None],
        process_every_n_frames: int = 1
    ):
        """
        Start video stream processing.
        
        Args:
            callback: Function to call with (frame, results) for each processed frame
            process_every_n_frames: Process every N frames (default 1 = all frames)
        """
        try:
            import cv2
            
            # Open video source
            if self.source == "webcam":
                self._cap = cv2.VideoCapture(0)
            elif self.source.startswith("rtsp://"):
                self._cap = cv2.VideoCapture(self.source)
            else:
                self._cap = cv2.VideoCapture(self.source)
            
            if not self._cap.isOpened():
                raise RuntimeError(f"Could not open video source: {self.source}")
            
            # Set resolution
            self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
            self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
            
            self._running = True
            frame_count = 0
            
            logger.info(f"Started video stream from {self.source}")
            
            while self._running:
                ret, frame = self._cap.read()
                
                if not ret:
                    logger.warning("Failed to read frame, stopping stream")
                    break
                
                frame_count += 1
                
                # Process frame
                if frame_count % process_every_n_frames == 0:
                    results = self._process_frame(frame)
                    callback(frame, results)
                
                # Control fps
                time.sleep(1.0 / self.fps)
            
        except Exception as e:
            logger.error(f"Error in video stream: {e}")
        finally:
            self.stop()
    
    def start_async(
        self,
        callback: Callable[[object, List[Dict]], None],
        process_every_n_frames: int = 1
    ):
        """
        Start video stream processing in background thread.
        
        Args:
            callback: Function to call with results
            process_every_n_frames: Process every N frames
        """
        self._thread = threading.Thread(
            target=self.start,
            args=(callback, process_every_n_frames),
            daemon=True
        )
        self._thread.start()
    
    def _process_frame(self, frame) -> List[Dict]:
        """Process a single frame."""
        results = []
        
        try:
            # Face detection
            if self._detector:
                faces = self._detector.detect(frame)
                results = faces
                
                # Face recognition
                if self._recognizer and len(faces) > 0:
                    recognized = self._recognizer.recognize(frame)
                    
                    # Match recognized faces with detected faces
                    for i, rec in enumerate(recognized):
                        if i < len(results):
                            results[i].update(rec)
                
                # Face analysis
                if hasattr(self, '_analyzer') and self._analyzer and len(faces) > 0:
                    import cv2
                    for i, face in enumerate(faces):
                        x, y, w, h = face["x"], face["y"], face["width"], face["height"]
                        face_img = frame[y:y+h, x:x+w]
                        
                        try:
                            analysis = self._analyzer.analyze(face_img)
                            if i < len(results):
                                results[i]["analysis"] = analysis
                        except:
                            pass
        
        except Exception as e:
            logger.debug(f"Error processing frame: {e}")
        
        return results
    
    def stop(self):
        """Stop video stream processing."""
        self._running = False
        
        if self._cap:
            self._cap.release()
            self._cap = None
        
        logger.info("Video stream stopped")
    
    def is_running(self) -> bool:
        """Check if stream is running."""
        return self._running
    
    def __del__(self):
        """Cleanup resources."""
        self.stop()
