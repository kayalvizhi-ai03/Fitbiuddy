from .config import get_settings


def generate_text(prompt: str, model: str) -> str:
    settings = get_settings()
    if not settings.google_api_key:
        raise RuntimeError("GOOGLE_API_KEY is not configured. Add it to .env or enable DEMO_MODE=true.")
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=settings.google_api_key)
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.6,
            max_output_tokens=5000,
        ),
    )
    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text.strip()


def demo_workout(goal: str, intensity: str) -> str:
    multiplier = {"low": "2 sets", "medium": "3 sets", "high": "3 sets"}[intensity]
    return f"""DAY 1 — Full Body\nWarm-up: 7 minutes brisk walking + mobility.\nMain: Squats ({multiplier} x 10), incline push-ups ({multiplier} x 8), glute bridges ({multiplier} x 12), plank (3 x 20-30 sec).\nCool-down: 5 minutes easy stretching.\n\nDAY 2 — Cardio & Core\nWarm-up: 5 minutes easy movement.\nMain: Brisk walk/cycle 20-30 minutes; dead bug (3 x 10/side); bird dog (3 x 8/side).\nCool-down: gentle stretching.\n\nDAY 3 — Upper Body\nWarm-up: shoulder circles + easy cardio.\nMain: wall/incline push-ups ({multiplier} x 8-12), resistance-band rows ({multiplier} x 10-12), light shoulder press ({multiplier} x 10).\nCool-down: chest and shoulder stretches.\n\nDAY 4 — Recovery\nEasy walk 15-25 minutes, mobility, and relaxed stretching.\n\nDAY 5 — Lower Body\nWarm-up: 7 minutes.\nMain: squats ({multiplier} x 10), reverse lunges ({multiplier} x 8/side), calf raises ({multiplier} x 15), glute bridges ({multiplier} x 12).\nCool-down: lower-body stretches.\n\nDAY 6 — Goal-Focused Conditioning\nWarm-up: 5-7 minutes.\nMain: 20-25 minutes of comfortable cardio intervals with 1-2 minutes easy recovery between efforts; finish with light core work.\nCool-down: easy walking and stretching.\n\nDAY 7 — Rest & Reflection\nRest or gentle mobility. Note energy, soreness, and what felt comfortable so the next plan can be adjusted.\n\nGoal focus: {goal}. Intensity: {intensity}."""


def demo_tip(goal: str) -> str:
    tips = {
        "muscle gain": "Include a protein-rich food at each main meal and drink enough water throughout the day to support training and recovery.",
        "weight loss": "Build meals around vegetables, a protein source, whole-food carbohydrates, and water; focus on consistency rather than extreme restriction.",
        "general wellness": "Aim for regular meals, adequate water, varied whole foods, and enough sleep to support everyday energy and recovery.",
        "flexibility": "Hydrate well and pair gentle mobility work with balanced meals that provide protein and a variety of fruits and vegetables.",
    }
    return tips.get(goal, tips["general wellness"])
