from deep_translator import GoogleTranslator
import edge_tts
import pyttsx3
from langdetect import detect, detect_langs, LangDetectException
import io
import asyncio
import os
import uuid
from typing import Optional, List, Dict, Any

class FreeClient:
    """
    Wrapper for FREE community tools.
    1. Online: 'edge-tts' (Neural/High-Quality).
    2. Offline: 'pyttsx3' (System/Robotic Fallback).
    3. Translation: 'deep-translator'.
    """
    def __init__(self):
        pass

    def translate_text(self, text: str, target: str) -> Dict[str, str]:
        if not text:
            return {"translatedText": "", "detectedSourceLanguage": "und"}
        
        try:
            translator = GoogleTranslator(source='auto', target=target)
            translated = translator.translate(text)
            
            try:
                detected_lang = detect(text)
            except:
                detected_lang = "und"

            return {
                "translatedText": translated,
                "detectedSourceLanguage": detected_lang
            }
        except Exception as e:
            raise Exception(f"Translation failed: {str(e)}")

    def detect_language(self, text: str) -> List[Dict[str, Any]]:
        if not text: return []
        clean_results = []
        try:
            results = detect_langs(text)
            for res in results:
                clean_results.append({"language": res.lang, "confidence": res.prob})
        except:
            pass
        return clean_results

    def list_voices(self, language_code: str = None) -> Dict[str, Any]:
        return {"voices": []}

    def synthesize_speech(self, text: str, language_code: str, voice_name: Optional[str] = None, audio_format: str = "mp3") -> bytes:
        """
        Tries Neural TTS (Online) first.
        If that fails (no internet), falls back to System TTS (Offline).
        """
        if not text:
            return b""
        
        # --- 1. Try Online Neural TTS ---
        try:
            # MAPPING TO HIGH QUALITY VOICES
            voice_map = {
                'en-US': 'en-US-JennyNeural',
                'en-GB': 'en-GB-SoniaNeural',
                'en-IN': 'en-IN-NeerjaNeural',
                'hi-IN': 'hi-IN-SwaraNeural',
                'bn-IN': 'bn-IN-TanishaaNeural',
                'ta-IN': 'ta-IN-PallaviNeural',
                'te-IN': 'te-IN-ShrutiNeural',
                'mr-IN': 'mr-IN-AarohiNeural',
                'gu-IN': 'gu-IN-DhwaniNeural',
                'kn-IN': 'kn-IN-SapnaNeural',
                'fr-FR': 'fr-FR-DeniseNeural',
                'es-ES': 'es-ES-ElviraNeural',
                'de-DE': 'de-DE-KatjaNeural',
                'ja-JP': 'ja-JP-NanamiNeural',
            }

            selected_voice = voice_map.get(language_code, 'en-US-JennyNeural')

            if language_code not in voice_map:
                for code, v in voice_map.items():
                    if language_code.startswith(code.split('-')[0]):
                        selected_voice = v
                        break
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # This will throw exception if no internet
            result = loop.run_until_complete(self._run_edge_tts(text, selected_voice))
            loop.close()
            return result

        except Exception as e:
            print(f"Online Neural TTS failed ({e}). Switching to Offline System TTS...")
            return self._run_offline_tts(text)

    async def _run_edge_tts(self, text: str, voice: str) -> bytes:
        communicate = edge_tts.Communicate(text, voice)
        out = io.BytesIO()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                out.write(chunk["data"])
        out.seek(0)
        return out.getvalue()

    def _run_offline_tts(self, text: str) -> bytes:
        """
        Uses pyttsx3 to generate audio offline.
        Saves to temp file, reads bytes, deletes file.
        """
        try:
            # unique filename to avoid conflicts
            filename = f"temp_tts_{uuid.uuid4().hex}.mp3"
            
            engine = pyttsx3.init()
            # Set properties if needed (speed, volume)
            engine.setProperty('rate', 150) 

            # Saving to file is the most reliable way to get bytes from pyttsx3
            engine.save_to_file(text, filename)
            engine.runAndWait()

            if os.path.exists(filename):
                with open(filename, "rb") as f:
                    data = f.read()
                os.remove(filename)
                return data
            else:
                return b""
        except Exception as e:
            print(f"Offline TTS also failed: {e}")
            return b""
