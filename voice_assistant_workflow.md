# 🧠 Voice Assistant Sequence Diagram

This sequence diagram illustrates the interaction between the major components of the Python Voice Assistant:

```mermaid
sequenceDiagram
    participant User
    participant Assistant as VoiceAssistant
    participant Recognizer as SpeechRecognizer
    participant Processor as CommandProcessor
    participant TTS as TextToSpeech
    participant Pattern as PatternCommand (optional)

    User->>Assistant: start()
    Assistant->>TTS: speak("Voice Assistant is now running...")

    loop Command Loop
        Assistant->>Recognizer: listen_for_command()
        Recognizer-->>Assistant: text
        Assistant->>Processor: handle_command(text)

        alt Fixed command match
            Processor->>TTS: speak(...)
            Processor->>System: perform action (e.g., open notepad)
        else Pattern command match
            Processor->>Pattern: match(text)
            Pattern-->>Processor: match result
            Pattern->>TTS: speak(...)
            Pattern->>System: perform action (e.g., type text)
        else No match
            Processor->>TTS: speak("Sorry, can't recognize this command")
        end
    end
