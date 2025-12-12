async function doTranslate() {
    const text = document.getElementById("trans-input").value;
    const target = document.getElementById("trans-lang").value;
    const outputText = document.getElementById("trans-output-text");

    if (!text.trim()) {
        alert("Please enter text.");
        return;
    }

    // Show Loader
    outputText.innerHTML = '<div class="spinner"></div> Translating...';

    try {
        const response = await fetch("/translate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text, target })
        });

        const data = await response.json();
        if (response.ok) {
            outputText.innerText = data.translatedText;
        } else {
            outputText.innerText = "Error: " + (data.error || "Unknown");
        }
    } catch (err) {
        outputText.innerText = "Network Error";
    }
}

async function speakText(elementId, langElementId, isDiv = false) {
    let text;
    if (isDiv) {
        text = document.getElementById(elementId).innerText;
    } else {
        text = document.getElementById(elementId).value;
    }

    let lang = document.getElementById(langElementId).value;
    if (lang === 'auto') lang = 'en';

    if (!text || text === "Translation will appear here...") return;

    try {
        const response = await fetch("/tts", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                text: text,
                lang: lang
            })
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = URL.createObjectURL(blob);
            const audio = document.getElementById("tts-audio");
            audio.src = url;
            audio.play();
        } else {
            console.error("TTS Failed");
        }
    } catch (err) {
        console.error(err);
    }
}

async function handleTTS(action) {
    const text = document.getElementById("tts-input").value;
    const lang = document.getElementById("tts-lang-select").value;

    if (!text.trim()) {
        alert("Please enter some text to speak.");
        return;
    }

    // Loader Logic for Buttons
    let btn;
    let originalText;

    // Simple selector logic based on class structure
    if (action === 'play') {
        btn = document.querySelector('.tts-card .action-btn:nth-of-type(1)');
    } else {
        btn = document.querySelector('.tts-card .action-btn:nth-of-type(2)');
    }

    if (btn) {
        originalText = btn.innerHTML;
        btn.innerHTML = '<div class="spinner"></div> Processing...';
        btn.disabled = true;
    }

    try {
        const response = await fetch("/tts", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text, lang })
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = URL.createObjectURL(blob);

            if (action === 'play') {
                const audio = document.getElementById("tts-audio");
                audio.src = url;
                audio.play();
            } else if (action === 'download') {
                const a = document.createElement('a');
                a.href = url;
                a.download = 'speech.mp3';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            }
        } else {
            alert("Error generating audio");
        }
    } catch (err) {
        console.error(err);
        alert("Network error");
    } finally {
        if (btn) {
            btn.innerHTML = originalText;
            btn.disabled = false;
        }
    }
}

function copyText(elementId) {
    const text = document.getElementById(elementId).innerText;
    navigator.clipboard.writeText(text);
}
