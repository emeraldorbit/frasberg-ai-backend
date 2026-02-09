"""
Sofia Core 6.6.0 - Speech-to-Text Example

Demonstrates speech recognition with Whisper.
"""

from backend.app.audio import SpeechToText

def main():
    print("Sofia Core 6.6.0 - Speech-to-Text Example")
    print("=" * 60)
    
    # Initialize speech-to-text
    print("\n1. Initializing Whisper model...")
    stt = SpeechToText(model_size="base", language="en")
    print("✓ Whisper model loaded")
    
    # Example: Transcribe audio
    print("\n2. Transcribing audio...")
    print("   (In production, provide actual audio file)")
    # text = stt.transcribe("meeting.wav")
    # print(f"✓ Transcription: {text}")
    
    # Example: Transcribe with timestamps
    print("\n3. Transcribing with timestamps...")
    # segments = stt.transcribe_with_timestamps("meeting.wav")
    # for seg in segments:
    #     print(f"   [{seg['start']:.1f}s - {seg['end']:.1f}s]: {seg['text']}")
    
    # Example: Detect language
    print("\n4. Detecting language...")
    # lang_info = stt.detect_language("audio.wav")
    # print(f"✓ Detected: {lang_info['language_name']} ({lang_info['confidence']:.2%})")
    
    print("\n" + "=" * 60)
    print("Example completed!")
    print("\nTo use with real audio:")
    print("1. Provide audio file path to transcribe()")
    print("2. Supports 100+ languages")
    print("3. Use transcribe_with_timestamps() for detailed output")

if __name__ == "__main__":
    main()
