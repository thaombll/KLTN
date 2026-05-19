from google import genai
import time

client = genai.Client(api_key="AIzaSyC-IZjwWpaGCx7QuH_fph5nFufqGrKsXOY")

def get_llm_response_sys(sysprompt: str, prompt: str, max_retries: int = 5):
    delay = 60  # bắt đầu 60s khi bị rate limit
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="models/gemini-2.0-flash",
                contents=f"{sysprompt}\n\n{prompt}"
            )
            time.sleep(5)  # nghỉ 5s sau mỗi request thành công
            return response.text

        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "quota" in error_str.lower() or "rate" in error_str.lower():
                print(f"[Retry {attempt+1}] Rate limit. Sleeping {delay}s...")
                time.sleep(delay)
                delay *= 2
            elif "502" in error_str or "503" in error_str:
                print(f"[Retry {attempt+1}] Server error. Sleeping 60s...")
                time.sleep(60)
            else:
                raise e

    raise Exception("Max retries exceeded")