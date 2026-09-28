from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from pathlib import Path
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .config import get_settings
from .database import get_db, get_all_plans, get_all_users, get_latest_plan, get_user, save_plan, save_user, update_plan
from .gemini_flash_generator import generate_nutrition_tip_with_flash
from .gemini_generator import generate_workout_gemini
from .schemas import FeedbackRequest, NutritionRequest, UserInput
from .updated_plan import update_workout_plan

router = APIRouter()
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
settings = get_settings()


def render_error(request: Request, message: str, status_code: int = 400):
    return templates.TemplateResponse(request=request, name="error.html", context={"message": message}, status_code=status_code)


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"goals": sorted({"weight loss", "muscle gain", "general wellness", "flexibility"}), "intensities": ["low", "medium", "high"]})


@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout_form(
    request: Request,
    name: str = Form(...), user_id: str = Form(...), age: int = Form(...), weight: float = Form(...),
    goal: str = Form(...), intensity: str = Form(...), db: Session = Depends(get_db)
):
    try:
        data = UserInput(name=name, user_id=user_id, age=age, weight=weight, goal=goal, intensity=intensity)
        plan = generate_workout_gemini(
    data.name,
    data.age,
    data.weight,
    data.goal,
    data.intensity
)
        tip = generate_nutrition_tip_with_flash(data.goal)
        save_user(db, **data.model_dump())
        save_plan(db, data.user_id, plan, tip)
        return templates.TemplateResponse(request=request, name="result.html", context={"user": data, "workout_plan": plan, "nutrition_tip": tip, "message": None})
    except Exception as exc:
        return render_error(request, str(exc), 400)


@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback_form(request: Request, user_id: str = Form(...), feedback: str = Form(...), db: Session = Depends(get_db)):
    try:
        data = FeedbackRequest(user_id=user_id, feedback=feedback)
        user = get_user(db, data.user_id)
        plan = get_latest_plan(db, data.user_id)
        if not user or not plan:
            raise ValueError("No saved plan was found for this User ID.")
        original = plan.updated_plan or plan.original_plan
        revised = update_workout_plan(original, data.feedback)
        tip = generate_nutrition_tip_with_flash(user.goal)
        update_plan(db, plan, revised, data.feedback, tip)
        user_input = UserInput(name=user.name, user_id=user.user_id, age=user.age, weight=user.weight, goal=user.goal, intensity=user.intensity)
        return templates.TemplateResponse(request=request, name="result.html", context={"user": user_input, "workout_plan": revised, "nutrition_tip": tip, "message": "Your plan was updated using your feedback."})
    except Exception as exc:
        return render_error(request, str(exc), 400)


@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request, token: str | None = None, db: Session = Depends(get_db)):
    if token != settings.admin_token:
        return render_error(request, "Unauthorized. Add the configured admin token as ?token=...", 401)
    users = get_all_users(db)
    plans = get_all_plans(db)
    plan_by_user = {p.user_id: p for p in plans}
    return templates.TemplateResponse(request=request, name="all_users.html", context={"users": users, "plan_by_user": plan_by_user})


@router.post("/api/generate-workout")
def generate_workout_api(payload: UserInput, db: Session = Depends(get_db)):
    plan = generate_workout_gemini(payload.name, payload.age, payload.weight, payload.goal, payload.intensity)
    tip = generate_nutrition_tip_with_flash(payload.goal)
    save_user(db, **payload.model_dump())
    saved = save_plan(db, payload.user_id, plan, tip)
    return {"user": payload.model_dump(), "plan_id": saved.id, "workout_plan": plan, "nutrition_tip": tip}


@router.post("/api/submit-feedback")
def submit_feedback_api(payload: FeedbackRequest, db: Session = Depends(get_db)):
    user = get_user(db, payload.user_id)
    plan = get_latest_plan(db, payload.user_id)
    if not user or not plan:
        raise HTTPException(status_code=404, detail="User or plan not found")
    original = plan.updated_plan or plan.original_plan
    revised = update_workout_plan(original, payload.feedback)
    tip = generate_nutrition_tip_with_flash(user.goal)
    update_plan(db, plan, revised, payload.feedback, tip)
    return {"user_id": payload.user_id, "workout_plan": revised, "nutrition_tip": tip, "message": "Plan updated successfully"}


@router.post("/api/nutrition-tip")
def nutrition_tip_api(payload: NutritionRequest):
    return {"goal": payload.goal, "nutrition_tip": generate_nutrition_tip_with_flash(payload.goal)}


@router.get("/api/users")
def users_api(token: str, db: Session = Depends(get_db)):
    if token != settings.admin_token:
        raise HTTPException(status_code=401, detail="Invalid admin token")
    users = get_all_users(db)
    plans = get_all_plans(db)
    plan_by_user = {p.user_id: p for p in plans}
    return {"users": [{"user_id": u.user_id, "name": u.name, "age": u.age, "weight": u.weight, "goal": u.goal, "intensity": u.intensity, "original_plan": plan_by_user.get(u.user_id).original_plan if plan_by_user.get(u.user_id) else None, "updated_plan": plan_by_user.get(u.user_id).updated_plan if plan_by_user.get(u.user_id) else None} for u in users]}
