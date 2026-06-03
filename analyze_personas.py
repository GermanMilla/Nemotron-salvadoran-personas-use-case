import json
import requests
from pathlib import Path

LLAMA_SERVER_URL = "http://127.0.0.1:8080/v1/chat/completions"

INPUT_FILE = Path("persona_elsalvador.json")
OUTPUT_FILE = Path("persona_analysis.json")

SYSTEM_PROMPT = """
You are a senior product analyst designing a localized fitness app for El Salvador.

You analyze synthetic personas and extract product requirements.

Rules: 
- Focus on fitness-related insights.
- Identify key motivations, barriers, and preferences related to fitness.
- Convert negative personality traits into neutral product insights.
- Do not make medical claims
- Return a valid JSON only
- Do not include markdown
- Do not include explanations outside the JSON
- If something is uncertain, use "unknown" or explain it in "confidence_notes".
"""


USER_PROMPT_TEMPLATE = """
Analyze this synthetic Salvadoran persona and extract fitness app feature needs.

Persona JSON:
{persona_json}

Return this exact JSON structure:

{{
    "persona_summary": {{
        "age": "",
        "sex": "",
        "location": "",
        "occupation": "",
        "fitness_context": "",
        "nutrition_context": "",
        "lifestyle_context": ""
    }},
    "fitness_signals": [],
    "nutrition_signals": [],
    "barriers": [],
    "motivators": [],
    "recommended_feature_tags": [],
    "p0_features": [
    {{
        "feature": "",
        "why_it_matters": "",
        "related_persona_signal": ""
    }}
    ],
    "p1_features": [
    {{
        "feature": "",
        "why_it_matters": "",
        "related_persona_signal": ""
    }}
    ],
    "p2_features": [
    {{
        "feature": "",
        "why_it_matters": "",
        "related_persona_signal": ""
    }}
    ],
    "features_to_avoid_for_now": [],
    "recommended_onboarding_questions": [],
    "recommended_retention_features": [],
    "recommended_nutrition_features": [],
    "recommended_activity_features": [],
    "app_tone_recommendation": "",
    "one_sentence_product_insight": "",
    "confidence_notes": ""
}}
"""

def load_persona(path: str) -> dict:
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Persona file not found at {path}")
    
    with file_path.open("r", encoding="utf-8") as f:
        return json.load(f)

def call_llama_api(persona: dict) -> str:
    payload = {
        "model": "gemma4-local",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT.strip()},
            {"role": "user", "content": USER_PROMPT_TEMPLATE.format(persona_json=json.dumps(persona, ensure_ascii=False, indent=2))}
        ],
        "max_tokens": 2500,
        "temperature": 0.2,
        "top_p": 0.9
    }
    
    response = requests.post(
        LLAMA_SERVER_URL, 
        headers={"Content-Type": "application/json"},
        json=payload,
        timeout=180)
    


    
    print("Status code:", response.status_code)
    print("Response text:", response.text)
    
    response.raise_for_status()
    
    data = response.json()
    message = data["choices"][0]["message"]

    print("Parsed response:")
    print(message)
    
    content = message.get("content", "")
    
    print("Model content:")
    print(content)
    
    return content
    

def parse_json_safely(model_output: str) -> dict:
    if not model_output or not model_output.strip():
        raise ValueError("Model returned empty output.")

    text = model_output.strip()

    # Try parsing the full response first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Remove markdown code fences if the model used them
    if text.startswith("```"):
        text = text.replace("```json", "", 1)
        text = text.replace("```", "", 1)
        text = text.strip()

    # Try again after removing code fences
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Extract JSON from first { to last }
    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1 or end <= start:
        raise ValueError(f"No JSON object found in model output:\n{text}")

    cleaned = text[start:end + 1].strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Failed to parse JSON after cleaning.\n"
            f"Original error: {e}\n\n"
            f"Cleaned output:\n{cleaned}"
        ) from e
    
    
def main():
    persona = load_persona(INPUT_FILE)
    model_output = call_llama_api(persona)
    analysis = parse_json_safely(model_output)
    
    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)
    
    print(f"Analysis saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()