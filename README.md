# FitBuddy – AI Fitness Plan Generator

FitBuddy is a FastAPI + Jinja2 + SQLite application that generates personalized 7-day workout plans, nutrition/recovery tips, and AI-updated plans from user feedback.

## Architecture

- **Frontend:** Jinja2 HTML + responsive CSS
- **Backend:** FastAPI
- **AI:** Google Gemini through the current `google-genai` SDK
- **Database:** SQLite + SQLAlchemy
- **API docs:** FastAPI Swagger UI at `/docs`

## Project structure

```text
fitbuddy/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── gemini_flash_generator.py
│   ├── gemini_generator.py
│   ├── gemini_service.py
│   ├── main.py
│   ├── routes.py
│   ├── schemas.py
│   └── updated_plan.py
├── static/
│   └── style.css
├── templates/
│   ├── all_users.html
│   ├── base.html
│   ├── error.html
│   ├── index.html
│   └── result.html
├── tests/
│   └── test_app.py
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Important model note

The supplied project document specifies Gemini 1.5 Pro and Gemini Flash. Those model names/SDK instructions are now outdated. This implementation keeps the document's **two-role AI design** but uses currently available Gemini model IDs through Google's current `google-genai` Python SDK. The model names are configurable in `.env`.

## VS Code setup

### 1. Open the folder

Open the `fitbuddy` folder in VS Code.

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```cmd
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Gemini

Copy `.env.example` to `.env`.

```text
GOOGLE_API_KEY=your_real_key
DEMO_MODE=false
```

Get a Gemini API key from Google AI Studio. Never commit `.env` to Git.

### 5. Run the application

```bash
uvicorn app.main:app --reload
```

Open:

- Website: http://127.0.0.1:8000
- API docs: http://127.0.0.1:8000/docs

## Test without an API key

Set:

```text
DEMO_MODE=true
```

Then restart Uvicorn. The application will use built-in deterministic demo responses, allowing you to test the UI, database, routes, feedback flow, and API without consuming Gemini requests.

## Admin dashboard

The admin route is protected by the `ADMIN_TOKEN` environment variable.

Example:

```text
http://127.0.0.1:8000/view-all-users?token=change-this-token
```

Change the token before real use.

## API examples

### Generate a plan

`POST /api/generate-workout`

```json
{
  "name": "Anu",
  "user_id": "anu001",
  "age": 21,
  "weight": 58,
  "goal": "general wellness",
  "intensity": "medium"
}
```

### Update a plan

`POST /api/submit-feedback`

```json
{
  "user_id": "anu001",
  "feedback": "Add more cardio and one extra rest day."
}
```

### Nutrition tip

`POST /api/nutrition-tip`

```json
{
  "goal": "muscle gain"
}
```

## Automated tests

With the virtual environment activated:

```bash
pytest -q
```

The tests force demo mode so they do not require a Gemini API key.

## Troubleshooting

**`GOOGLE_API_KEY is not configured`**: check `.env`, or use `DEMO_MODE=true`.

**PowerShell blocks activation**: use Command Prompt, or run PowerShell as appropriate for your machine's execution policy.

**Port 8000 is busy**:

```bash
uvicorn app.main:app --reload --port 8001
```

Then open http://127.0.0.1:8001.
