import os
import io
import logging
from flask import Flask, request, jsonify, send_file, render_template
# Changed from GCloudClient to FreeClient
from gcloud_client import FreeClient

# Note to self: Set up basic logging to see errors in the console.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize our helper client
gcloud = FreeClient()

# Fix paths for separate frontend folder
# Assuming running from backend/ or root, relative path to frontend
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'templates'))
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'static'))

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

@app.route("/")
def index():
    """
    Serves the frontend interface.
    """
    return render_template("index.html")

@app.route("/health", methods=["GET"])
def health_check():
    """
    Simple health check endpoint for monitoring.
    """
    return jsonify({"status": "ok"})

@app.route("/translate", methods=["POST"])
def translate_endpoint():
    try:
        data = request.get_json(force=True, silent=True) # silent=True returns None if not valid JSON
        
        if not data:
            return jsonify({"error": "Invalid JSON body"}), 400
            
        text = data.get("text")
        target_lang = data.get("target")

        # Simple validation
        if not text:
            return jsonify({"error": "Missing 'text' parameter"}), 400
        if not target_lang:
            return jsonify({"error": "Missing 'target' parameter"}), 400

        result = gcloud.translate_text(text, target_lang)
        return jsonify(result)

    except Exception as e:
        logger.error(f"Translation error: {e}")
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

@app.route("/detect-language", methods=["POST"])
def detect_endpoint():
    try:
        data = request.get_json(force=True, silent=True)
        
        if not data:
            return jsonify({"error": "Invalid JSON body"}), 400
            
        text = data.get("text")
        if not text:
            return jsonify({"error": "Missing 'text' parameter"}), 400

        detections = gcloud.detect_language(text)
        
        # Return the first/best detection for simplicity, or the whole list if requested.
        # Spec says "return detected language and confidence", implied single or primary.
        # We will return the primary one as top-level fields for convenience? 
        # Actually spec said "Returns detected language and confidence". Let's wrap it nicely.
        if detections:
            primary = detections[0]
            return jsonify({
                "language": primary["language"],
                "confidence": primary["confidence"],
                "all_detections": detections
            })
        else:
            return jsonify({"language": "und", "confidence": 0.0})

    except Exception as e:
        logger.error(f"Detection error: {e}")
        return jsonify({"error": f"Failed to detect language: {str(e)}"}), 500

@app.route("/tts", methods=["POST"])
def tts_endpoint():
    try:
        data = request.get_json(force=True, silent=True)
        if not data:
            return jsonify({"error": "Invalid JSON body"}), 400

        text = data.get("text")
        lang = data.get("lang", "en-US")
        voice = data.get("voice") # Optional
        fmt = data.get("format", "mp3") # mp3 or linear16

        if not text:
            return jsonify({"error": "Missing 'text' parameter"}), 400

        # Call our wrapper
        audio_bytes = gcloud.synthesize_speech(
            text=text, 
            language_code=lang, 
            voice_name=voice, 
            audio_format=fmt
        )

        # Prepare for download
        # Note to self: Use io.BytesIO to handle in-memory bytes like a file.
        mem_file = io.BytesIO(audio_bytes)
        mem_file.seek(0)
        
        # Determine mimetype and extension
        if fmt.lower() == "linear16":
            mimetype = "audio/wav"
            filename = "output.wav"
        else:
            mimetype = "audio/mpeg"
            filename = "output.mp3"

        return send_file(
            mem_file,
            mimetype=mimetype,
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        logger.error(f"TTS error: {e}")
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

@app.route("/voices", methods=["GET"])
def voices_endpoint():
    """
    Helper endpoint for the frontend to list voices.
    """
    try:
        lang = request.args.get("lang")
        voices = gcloud.list_voices(language_code=lang)
        return jsonify(voices)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Note for dev: Access on 0.0.0.0 to verify docker mapping easily if needed.
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
