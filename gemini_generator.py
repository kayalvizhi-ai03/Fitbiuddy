from .config import get_settings
from .gemini_service import generate_text, demo_workout


def generate_workout_gemini(name: str, age: int, weight: float, goal: str, intensity: str) -> str:
    settings = get_settings()
    prompt = f"""You are FitBuddy, a responsible fitness planning assistant.
Create a practical 7-day beginner-to-intermediate workout plan for this user:
Name: {name}
Age: {age}
Weight: {weight} kg
Goal: {goal}
Preferred intensity: {intensity}

Return ONLY a clearly formatted plan with Day 1 through Day 7. For each day include:
- Focus
- Warm-up (5-10 minutes)
- Main workout (exercise, sets/reps or duration, rest)
- Cool-down/recovery
Include at least one recovery/rest day. Keep recommendations general and safe.
Do not diagnose conditions, prescribe treatment, or claim guaranteed results.
If an exercise may be unsuitable for someone with an injury or medical condition, say to consult a qualified professional.
"""
    if settings.demo_mode or not settings.google_api_key:
        return demo_workout(goal, intensity)
    return generate_text(prompt, settings.workout_model)
