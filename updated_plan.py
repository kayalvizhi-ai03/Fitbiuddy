from .config import get_settings
from .gemini_service import generate_text


def update_workout_plan(original_plan: str, feedback: str) -> str:
    settings = get_settings()
    if settings.demo_mode or not settings.google_api_key:
        return original_plan + f"\n\nUPDATED BASED ON FEEDBACK\n- Requested change: {feedback}\n- Adjust the sessions above to reflect this preference while keeping at least one recovery day."
    prompt = f"""You are revising a FitBuddy 7-day workout plan.
Original plan:
{original_plan}

User feedback:
{feedback}

Return ONLY the complete revised 7-day plan. Preserve useful parts of the original plan, apply the feedback, and keep the structure Day 1 through Day 7 with focus, warm-up, main workout, and cool-down/recovery. Keep advice general and safe; do not diagnose or prescribe treatment."""
    return generate_text(prompt, settings.workout_model)
