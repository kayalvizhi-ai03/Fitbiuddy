from pydantic import BaseModel, Field, field_validator

GOALS = {"weight loss", "muscle gain", "general wellness", "flexibility"}
INTENSITIES = {"low", "medium", "high"}


class UserInput(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    user_id: str = Field(min_length=2, max_length=80, pattern=r"^[A-Za-z0-9_-]+$")
    age: int = Field(ge=13, le=100)
    weight: float = Field(gt=20, le=400)
    goal: str
    intensity: str

    @field_validator("name")
    @classmethod
    def clean_name(cls, value: str) -> str:
        return " ".join(value.strip().split())

    @field_validator("goal")
    @classmethod
    def valid_goal(cls, value: str) -> str:
        value = value.strip().lower()
        if value not in GOALS:
            raise ValueError(f"Goal must be one of: {', '.join(sorted(GOALS))}")
        return value

    @field_validator("intensity")
    @classmethod
    def valid_intensity(cls, value: str) -> str:
        value = value.strip().lower()
        if value not in INTENSITIES:
            raise ValueError(f"Intensity must be one of: {', '.join(sorted(INTENSITIES))}")
        return value


class FeedbackRequest(BaseModel):
    user_id: str = Field(min_length=2, max_length=80, pattern=r"^[A-Za-z0-9_-]+$")
    feedback: str = Field(min_length=3, max_length=1200)

    @field_validator("feedback")
    @classmethod
    def clean_feedback(cls, value: str) -> str:
        return value.strip()


class NutritionRequest(BaseModel):
    goal: str

    @field_validator("goal")
    @classmethod
    def valid_goal(cls, value: str) -> str:
        value = value.strip().lower()
        if value not in GOALS:
            raise ValueError(f"Goal must be one of: {', '.join(sorted(GOALS))}")
        return value
