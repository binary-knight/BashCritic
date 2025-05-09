import time
import requests

def analyze_script(prompt, model="mistral", host="http://localhost:11434", timeout=60):
    try:
        return _send_prompt(prompt, model, host, timeout)
    except requests.exceptions.ReadTimeout:
        print("First request timed out — warming up model...")

        # Try a short dummy prompt to load model
        dummy_prompt = prompt[:200]
        try:
            _ = _send_prompt(dummy_prompt, model, host, timeout)
            print("Model warm-up complete. Retrying...")
        except Exception as e:
            print("Warm-up failed:", e)
            return "[Error] Model warm-up failed."

        time.sleep(2)
        try:
            return _send_prompt(prompt, model, host, timeout)
        except requests.exceptions.ReadTimeout:
            return "[Error] Request to LLM timed out (even after warm-up)."

def _send_prompt(prompt, model, host, timeout):
    response = requests.post(
        f"{host}/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        },
        timeout=timeout
    )
    response.raise_for_status()
    return response.json().get("response", "")
