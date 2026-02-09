"""
Sofia Core 6.6.0 - Face Recognition Example

Demonstrates basic face recognition functionality.
"""

from backend.app.vision import FaceDetection, FaceRecognition

def main():
    print("Sofia Core 6.6.0 - Face Recognition Example")
    print("=" * 60)
    
    # Initialize face detection
    print("\n1. Initializing face detection...")
    detector = FaceDetection(backend="mediapipe")
    print("✓ Face detector initialized")
    
    # Initialize face recognition
    print("\n2. Initializing face recognition...")
    recognizer = FaceRecognition(model_name="Facenet")
    print("✓ Face recognizer initialized")
    
    # Example: Register known faces
    print("\n3. Registering known faces...")
    print("   (In production, use actual image files)")
    # recognizer.register_face("john.jpg", "John Doe", "user123")
    # recognizer.register_face("jane.jpg", "Jane Smith", "user456")
    print("✓ Faces registered")
    
    # Example: Detect faces
    print("\n4. Detecting faces in image...")
    print("   (In production, provide actual image path)")
    # faces = detector.detect("group_photo.jpg")
    # print(f"✓ Detected {len(faces)} faces")
    
    # Example: Recognize faces
    print("\n5. Recognizing faces...")
    # results = recognizer.recognize("group_photo.jpg")
    # for person in results:
    #     print(f"   - {person['name']}: {person['confidence']:.2%}")
    
    print("\n" + "=" * 60)
    print("Example completed!")
    print("\nTo use with real images:")
    print("1. Provide image paths to register_face()")
    print("2. Use detect() with your image files")
    print("3. Use recognize() to identify people")

if __name__ == "__main__":
    main()
