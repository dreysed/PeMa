"""
PeMa API v2 — FastAPI + SQLAlchemy (SQLite)
Auth: JWT Bearer tokens, bcrypt passwords
Run: uvicorn api.main:app --reload --port 8000
"""
from __future__ import annotations

import calendar as cal_module
import json
import os
import uuid
from datetime import date as Date, datetime, timedelta
from typing import Any, Optional

from fastapi import Depends, FastAPI, File, HTTPException, Query, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import bcrypt as _bcrypt
from pydantic import BaseModel, field_validator
from sqlalchemy import (
    Boolean, Column, Float, ForeignKey, Integer, String, Text, create_engine,
)
from sqlalchemy.orm import Session, declarative_base, sessionmaker

# ─── Config ──────────────────────────────────────────────────────────────────

SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_ME_IN_PRODUCTION_PLEASE_SET_ENV_VAR")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

DATABASE_URL = "sqlite:///./pema.db"
OLLAMA_CLOUD_HOST = os.getenv("OLLAMA_CLOUD_HOST", "https://ollama.com")
OLLAMA_CLOUD_MODEL = os.getenv("OLLAMA_CLOUD_MODEL", "kimi-k2.6")


def _ollama_model_candidates() -> list[str]:
    configured = [m.strip() for m in OLLAMA_CLOUD_MODEL.split(",") if m.strip()]
    defaults = ["kimi-k2.6", "kimi-k2.6:cloud", "kimi-k2:1t-cloud"]
    result = []
    for model in configured + defaults:
        if model not in result:
            result.append(model)
    return result

# ─── Database ────────────────────────────────────────────────────────────────

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def _hash_password(plain: str) -> str:
    return _bcrypt.hashpw(plain.encode(), _bcrypt.gensalt(rounds=12)).decode()

def _verify_password(plain: str, hashed: str) -> bool:
    return _bcrypt.checkpw(plain.encode(), hashed.encode())

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def new_id() -> str:
    return str(uuid.uuid4())


# ─── Models ──────────────────────────────────────────────────────────────────

class UserDB(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)          # "coach" | "athlete"
    password_hash = Column(String, nullable=False)
    athlete_id = Column(String, ForeignKey("athletes.id"), nullable=True)
    created_at = Column(String, nullable=False)
    openai_key           = Column(String, nullable=True)
    strava_client_id     = Column(String, nullable=True)
    strava_client_secret = Column(String, nullable=True)
    strava_access_token  = Column(String, nullable=True)
    strava_refresh_token = Column(String, nullable=True)
    strava_token_expiry  = Column(Integer, nullable=True)   # unix timestamp
    strava_athlete_id    = Column(String, nullable=True)


class AthleteDB(Base):
    __tablename__ = "athletes"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)


class CoachAthleteLinkDB(Base):
    __tablename__ = "coach_athlete_links"
    coach_user_id = Column(String, ForeignKey("users.id"), primary_key=True)
    athlete_id = Column(String, ForeignKey("athletes.id"), primary_key=True)


class WorkoutDB(Base):
    __tablename__ = "workouts"
    id = Column(String, primary_key=True)
    athlete_id = Column(String, ForeignKey("athletes.id"), nullable=False)
    date = Column(String, nullable=False)          # YYYY-MM-DD
    title = Column(String, nullable=False)
    category = Column(String, nullable=False, default="run")
    distance_km = Column(Float, default=0.0)
    duration_min = Column(Integer, default=0)
    intensity = Column(String, default="moderate")
    notes = Column(Text, default="")
    hidden = Column(Boolean, default=False)
    intervals_json = Column(Text, default="[]")
    status = Column(String, default="planned")     # planned | done | skipped
    athlete_feedback = Column(Text, default="")
    athlete_mood = Column(String, default="")
    perceived_exertion = Column(Integer, default=0)

    # Actual values from watch import (.gpx/.fit) or athlete-reported facts
    actual_distance_km    = Column(Float,   nullable=True)
    actual_duration_min   = Column(Integer, nullable=True)
    actual_avg_pace       = Column(Float,   nullable=True)   # min/km
    actual_avg_hr         = Column(Integer, nullable=True)   # bpm
    actual_max_hr         = Column(Integer, nullable=True)
    actual_calories       = Column(Integer, nullable=True)
    actual_elevation_gain = Column(Float,   nullable=True)   # metres
    route_geojson         = Column(Text,    nullable=True)   # GeoJSON LineString
    source_file           = Column(String,  nullable=True)   # imported file name


class GoalDB(Base):
    __tablename__ = "goals"
    id            = Column(String, primary_key=True)
    athlete_id    = Column(String, ForeignKey("athletes.id"), nullable=False)
    title         = Column(String, nullable=False)            # "Марафон Москва"
    target_date   = Column(String, nullable=False)            # ISO YYYY-MM-DD
    type          = Column(String, default="race")            # race | volume | weight
    target_value  = Column(Float,  nullable=True)             # for volume: km
    target_unit   = Column(String, nullable=True)             # km | kg | runs
    created_at    = Column(String, nullable=False)
    completed_at  = Column(String, nullable=True)


class RouteDB(Base):
    """AI-generated running routes saved by a user."""
    __tablename__ = "routes"
    id          = Column(String, primary_key=True)
    user_id     = Column(String, ForeignKey("users.id"), nullable=False)
    name        = Column(String, nullable=False)
    distance_km = Column(Float, nullable=True)
    geojson     = Column(Text, nullable=True)      # GeoJSON LineString
    description = Column(Text, nullable=True)      # AI description
    start_lat   = Column(Float, nullable=True)
    start_lon   = Column(Float, nullable=True)
    created_at  = Column(String, nullable=False)


class CommentDB(Base):
    __tablename__ = "comments"
    id = Column(String, primary_key=True)
    workout_id = Column(String, ForeignKey("workouts.id"), nullable=False)
    author = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(String, nullable=False)


class TemplateDB(Base):
    __tablename__ = "templates"
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False, default="run")
    distance_km = Column(Float, default=0.0)
    duration_min = Column(Integer, default=0)
    intensity = Column(String, default="moderate")
    intervals_json = Column(Text, default="[]")
    notes = Column(Text, default="")
    tags = Column(String, default="")


# ─── Auth schemas ─────────────────────────────────────────────────────────────

VALID_ROLES = {"coach", "athlete"}


class RegisterRequest(BaseModel):
    email: str
    name: str
    password: str
    role: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        v = v.strip().lower()
        parts = v.split("@")
        if len(parts) != 2 or not parts[0] or "." not in parts[1] or not parts[1].split(".")[-1]:
            raise ValueError("Некорректный формат email")
        return v

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Имя не может быть пустым")
        if len(v) > 100:
            raise ValueError("Имя слишком длинное")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("Пароль должен содержать минимум 6 символов")
        return v

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: str) -> str:
        if v not in VALID_ROLES:
            raise ValueError(f"Роль должна быть одной из: {', '.join(VALID_ROLES)}")
        return v


class LoginRequest(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower()


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    name: str
    role: str
    athlete_id: Optional[str] = None


# ─── Workout / template schemas ───────────────────────────────────────────────

class WorkoutCreate(BaseModel):
    athlete_id: str
    date: str
    title: str
    category: str = "run"
    distance_km: float = 0.0
    duration_min: int = 0
    intensity: str = "moderate"
    notes: str = ""
    hidden: bool = False
    intervals_json: str = "[]"


class WorkoutUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    distance_km: Optional[float] = None
    duration_min: Optional[int] = None
    intensity: Optional[str] = None
    notes: Optional[str] = None
    hidden: Optional[bool] = None
    intervals_json: Optional[str] = None


class WorkoutStatusUpdate(BaseModel):
    status: str
    athlete_feedback: str = ""
    athlete_mood: str = ""
    perceived_exertion: int = 0


class CommentCreate(BaseModel):
    text: str

    @field_validator("text")
    @classmethod
    def text_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Комментарий не может быть пустым")
        return v.strip()


class TemplateCreate(BaseModel):
    title: str
    category: str = "run"
    distance_km: float = 0.0
    duration_min: int = 0
    intensity: str = "moderate"
    intervals_json: str = "[]"
    notes: str = ""
    tags: str = ""


class TemplateUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    distance_km: Optional[float] = None
    duration_min: Optional[int] = None
    intensity: Optional[str] = None
    intervals_json: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[str] = None


class PlanFromTemplate(BaseModel):
    athlete_id: str
    date: str


class AICoachApplyRequest(BaseModel):
    athlete_id: str
    horizon_days: int = 14
    create_templates: bool = True
    apply_schedule: bool = True


class AICoachChatRequest(BaseModel):
    athlete_id: str
    message: str
    horizon_days: int = 14


class AddAthleteRequest(BaseModel):
    athlete_email: str

    @field_validator("athlete_email")
    @classmethod
    def normalize(cls, v: str) -> str:
        return v.strip().lower()


# ─── JWT helpers ──────────────────────────────────────────────────────────────

def create_access_token(user_id: str, role: str) -> str:
    payload = {
        "sub": user_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> UserDB:
    exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неверный или просроченный токен",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if not user_id:
            raise exc
    except JWTError:
        raise exc

    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        raise exc
    return user


def require_coach(current_user: UserDB = Depends(get_current_user)) -> UserDB:
    if current_user.role != "coach":
        raise HTTPException(status_code=403, detail="Только для тренеров")
    return current_user


# ─── Formatters ──────────────────────────────────────────────────────────────

def category_icon(cat: str) -> str:
    return {"run": "🏃", "bike": "🚴", "swim": "🏊"}.get(cat, "⚡")


def intensity_label(i: str) -> str:
    return {"easy": "Легко", "moderate": "Умеренно", "hard": "Тяжело"}.get(i, i)


def intensity_color(i: str) -> str:
    return {"easy": "#10b981", "moderate": "#f59e0b", "hard": "#ef4444"}.get(i, "#6b7280")


def status_label(s: str) -> str:
    return {"planned": "Запланировано", "done": "Выполнено", "skipped": "Пропущено"}.get(s, s)


def workout_to_card(w: WorkoutDB) -> dict:
    return {
        "id": w.id,
        "title": w.title,
        "category": w.category,
        "typeIcon": category_icon(w.category),
        "distance": f"{w.distance_km:.1f} км",
        "duration": f"{w.duration_min} мин",
        "distanceKm": w.distance_km,
        "durationMin": w.duration_min,
        "intensity": w.intensity,
        "intensityLabel": intensity_label(w.intensity),
        "intensityColor": intensity_color(w.intensity),
        "status": w.status,
        "statusLabel": status_label(w.status),
        "hidden": w.hidden,
        "dateIso": w.date,
        "notes": w.notes,
        "intervalsJson": w.intervals_json,
        "athleteFeedback": w.athlete_feedback or "",
        "athleteMood": w.athlete_mood or "",
        "perceivedExertion": w.perceived_exertion or 0,
        "athleteId": w.athlete_id,
        # Actual data from watch import (may be null)
        "actualDistanceKm":   w.actual_distance_km,
        "actualDurationMin":  w.actual_duration_min,
        "actualAvgPace":      w.actual_avg_pace,
        "actualAvgHr":        w.actual_avg_hr,
        "actualMaxHr":        w.actual_max_hr,
        "actualCalories":     w.actual_calories,
        "actualElevationGain": w.actual_elevation_gain,
        "routeGeojson":       w.route_geojson,
        "sourceFile":         w.source_file,
    }


def tpl_to_dict(t: TemplateDB) -> dict:
    return {
        "id": t.id,
        "title": t.title,
        "category": t.category,
        "distanceKm": t.distance_km,
        "durationMin": t.duration_min,
        "intensity": t.intensity,
        "intervals": t.intervals_json,
        "notes": t.notes,
        "tags": t.tags,
    }


# ─── App ─────────────────────────────────────────────────────────────────────

app = FastAPI(title="PeMa API", version="2.0.0", docs_url="/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── OSM tile proxy (no auth) ──────────────────────────────────────────────────
# Qt Image doesn't send a User-Agent; OSM blocks such requests with 418.
# We proxy through the local backend which sends a proper UA.
_TILE_CACHE: dict = {}   # simple in-memory cache  {(z,x,y): bytes}

@app.get("/api/tiles/{z}/{x}/{y}")
async def proxy_osm_tile(z: int, x: int, y: int):
    import httpx
    key = (z, x, y)
    if key in _TILE_CACHE:
        return Response(content=_TILE_CACHE[key], media_type="image/png",
                        headers={"Cache-Control": "public, max-age=86400"})
    url = f"https://tile.openstreetmap.org/{z}/{x}/{y}.png"
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.get(url, headers={
                "User-Agent": "PeMa/1.0 (desktop sport training app; https://github.com/sportcal)",
                "Accept": "image/png,image/*",
                "Referer": "https://www.openstreetmap.org/",
            })
        if r.status_code == 200:
            _TILE_CACHE[key] = r.content
            return Response(content=r.content, media_type="image/png",
                            headers={"Cache-Control": "public, max-age=86400"})
        raise HTTPException(status_code=r.status_code, detail="Tile fetch failed")
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=str(e))


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    _migrate_schema()


def _migrate_schema():
    """Lightweight forward-only migrations for SQLite (ADD COLUMN if missing)."""
    from sqlalchemy import text
    new_workout_cols = {
        "actual_distance_km":    "REAL",
        "actual_duration_min":   "INTEGER",
        "actual_avg_pace":       "REAL",
        "actual_avg_hr":         "INTEGER",
        "actual_max_hr":         "INTEGER",
        "actual_calories":       "INTEGER",
        "actual_elevation_gain": "REAL",
        "route_geojson":         "TEXT",
        "source_file":           "TEXT",
    }
    new_user_cols = {
        "openai_key":           "TEXT",
        "strava_client_id":     "TEXT",
        "strava_client_secret": "TEXT",
        "strava_access_token":  "TEXT",
        "strava_refresh_token": "TEXT",
        "strava_token_expiry":  "INTEGER",
        "strava_athlete_id":    "TEXT",
    }
    with engine.begin() as conn:
        existing_w = {row[1] for row in conn.execute(text("PRAGMA table_info(workouts)"))}
        for col, sql_type in new_workout_cols.items():
            if col not in existing_w:
                conn.execute(text(f"ALTER TABLE workouts ADD COLUMN {col} {sql_type}"))

        existing_u = {row[1] for row in conn.execute(text("PRAGMA table_info(users)"))}
        for col, sql_type in new_user_cols.items():
            if col not in existing_u:
                conn.execute(text(f"ALTER TABLE users ADD COLUMN {col} {sql_type}"))


# ─── Auth ─────────────────────────────────────────────────────────────────────

@app.post("/api/auth/register", response_model=TokenResponse, status_code=201)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(UserDB).filter(UserDB.email == data.email).first():
        raise HTTPException(400, "Email уже зарегистрирован")

    athlete_id = None
    if data.role == "athlete":
        athlete = AthleteDB(id=new_id(), name=data.name)
        db.add(athlete)
        db.flush()
        athlete_id = athlete.id

    user = UserDB(
        id=new_id(),
        email=data.email,
        name=data.name,
        role=data.role,
        password_hash=_hash_password(data.password),
        athlete_id=athlete_id,
        created_at=datetime.utcnow().isoformat(),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return TokenResponse(
        access_token=create_access_token(user.id, user.role),
        user_id=user.id,
        name=user.name,
        role=user.role,
        athlete_id=user.athlete_id,
    )


@app.post("/api/auth/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.email == data.email).first()
    if not user or not _verify_password(data.password, user.password_hash):
        # Same error for both to prevent email enumeration
        raise HTTPException(401, "Неверный email или пароль")

    return TokenResponse(
        access_token=create_access_token(user.id, user.role),
        user_id=user.id,
        name=user.name,
        role=user.role,
        athlete_id=user.athlete_id,
    )


@app.get("/api/auth/me")
def get_me(current_user: UserDB = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "role": current_user.role,
        "athleteId": current_user.athlete_id,
    }


# ─── Athletes ────────────────────────────────────────────────────────────────

@app.get("/api/athletes")
def list_athletes(
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role == "coach":
        links = db.query(CoachAthleteLinkDB).filter(
            CoachAthleteLinkDB.coach_user_id == current_user.id
        ).all()
        ids = [lnk.athlete_id for lnk in links]
        athletes = db.query(AthleteDB).filter(AthleteDB.id.in_(ids)).order_by(AthleteDB.name).all()
    else:
        athletes = (
            db.query(AthleteDB).filter(AthleteDB.id == current_user.athlete_id).all()
            if current_user.athlete_id else []
        )
    return [{"id": a.id, "name": a.name} for a in athletes]


@app.post("/api/athletes/link", status_code=201)
def link_athlete(
    data: AddAthleteRequest,
    current_user: UserDB = Depends(require_coach),
    db: Session = Depends(get_db),
):
    athlete_user = db.query(UserDB).filter(
        UserDB.email == data.athlete_email,
        UserDB.role == "athlete",
    ).first()
    if not athlete_user or not athlete_user.athlete_id:
        raise HTTPException(404, "Атлет с таким email не найден")

    existing = db.query(CoachAthleteLinkDB).filter(
        CoachAthleteLinkDB.coach_user_id == current_user.id,
        CoachAthleteLinkDB.athlete_id == athlete_user.athlete_id,
    ).first()
    if existing:
        raise HTTPException(409, "Атлет уже добавлен")

    db.add(CoachAthleteLinkDB(
        coach_user_id=current_user.id,
        athlete_id=athlete_user.athlete_id,
    ))
    db.commit()
    return {"athleteId": athlete_user.athlete_id, "name": athlete_user.name}


@app.delete("/api/athletes/{athlete_id}/link", status_code=204)
def unlink_athlete(
    athlete_id: str,
    current_user: UserDB = Depends(require_coach),
    db: Session = Depends(get_db),
):
    link = db.query(CoachAthleteLinkDB).filter(
        CoachAthleteLinkDB.coach_user_id == current_user.id,
        CoachAthleteLinkDB.athlete_id == athlete_id,
    ).first()
    if not link:
        raise HTTPException(404, "Связь не найдена")
    db.delete(link)
    db.commit()


# ─── Calendar ────────────────────────────────────────────────────────────────

@app.get("/api/calendar/{year}/{month}")
def get_calendar(
    year: int,
    month: int,
    athlete_id: str,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _assert_athlete_access(current_user, athlete_id, db)

    first_day = Date(year, month, 1)
    last_day = Date(year, month, cal_module.monthrange(year, month)[1])
    grid_start = first_day - timedelta(days=first_day.weekday())

    start_fetch = grid_start - timedelta(days=1)
    end_fetch = last_day + timedelta(days=14)
    show_hidden = current_user.role == "coach"

    workouts_q = db.query(WorkoutDB).filter(
        WorkoutDB.athlete_id == athlete_id,
        WorkoutDB.date >= start_fetch.strftime("%Y-%m-%d"),
        WorkoutDB.date <= end_fetch.strftime("%Y-%m-%d"),
    ).all()

    by_date: dict[str, list] = {}
    for w in workouts_q:
        if w.hidden and not show_hidden:
            continue
        by_date.setdefault(w.date, []).append(workout_to_card(w))

    today_iso = Date.today().strftime("%Y-%m-%d")
    cells = []
    for i in range(42):
        d = grid_start + timedelta(days=i)
        d_iso = d.strftime("%Y-%m-%d")
        in_month = d.month == month
        cells.append({
            "dateIso": d_iso,
            "dayNumber": str(d.day),
            "inCurrentMonth": in_month,
            "isToday": d_iso == today_iso,
            "background": "#dbeafe" if d_iso == today_iso else ("#ffffff" if in_month else "#f8fafc"),
            "workouts": by_date.get(d_iso, []),
        })
    return cells


# ─── Workouts ────────────────────────────────────────────────────────────────

@app.get("/api/workouts")
def list_workouts(
    athlete_id: str,
    date: Optional[str] = Query(None),
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _assert_athlete_access(current_user, athlete_id, db)
    q = db.query(WorkoutDB).filter(WorkoutDB.athlete_id == athlete_id)
    if date:
        q = q.filter(WorkoutDB.date == date)
    show_hidden = current_user.role == "coach"
    return [
        workout_to_card(w) for w in q.order_by(WorkoutDB.date).all()
        if not (w.hidden and not show_hidden)
    ]


@app.post("/api/workouts", status_code=201)
def create_workout(
    workout: WorkoutCreate,
    current_user: UserDB = Depends(require_coach),
    db: Session = Depends(get_db),
):
    _assert_coach_athlete_link(current_user.id, workout.athlete_id, db)
    try:
        json.loads(workout.intervals_json)
    except Exception:
        raise HTTPException(400, "Некорректный JSON интервалов")

    w = WorkoutDB(
        id=new_id(), athlete_id=workout.athlete_id, date=workout.date,
        title=workout.title, category=workout.category,
        distance_km=workout.distance_km, duration_min=workout.duration_min,
        intensity=workout.intensity, notes=workout.notes,
        hidden=workout.hidden, intervals_json=workout.intervals_json,
        status="planned",
    )
    db.add(w)
    db.commit()
    db.refresh(w)
    return workout_to_card(w)


@app.get("/api/workouts/{workout_id}")
def get_workout(
    workout_id: str,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    w = _get_workout_or_404(workout_id, db)
    _assert_athlete_access(current_user, w.athlete_id, db)
    if w.hidden and current_user.role != "coach":
        raise HTTPException(403, "Нет доступа")
    return workout_to_card(w)


@app.put("/api/workouts/{workout_id}")
def update_workout(
    workout_id: str,
    update: WorkoutUpdate,
    current_user: UserDB = Depends(require_coach),
    db: Session = Depends(get_db),
):
    w = _get_workout_or_404(workout_id, db)
    _assert_coach_athlete_link(current_user.id, w.athlete_id, db)

    if update.title is not None:         w.title = update.title
    if update.category is not None:      w.category = update.category
    if update.distance_km is not None:   w.distance_km = update.distance_km
    if update.duration_min is not None:  w.duration_min = update.duration_min
    if update.intensity is not None:     w.intensity = update.intensity
    if update.notes is not None:         w.notes = update.notes
    if update.hidden is not None:        w.hidden = update.hidden
    if update.intervals_json is not None:
        try:
            json.loads(update.intervals_json)
        except Exception:
            raise HTTPException(400, "Некорректный JSON интервалов")
        w.intervals_json = update.intervals_json

    db.commit()
    db.refresh(w)
    return workout_to_card(w)


@app.delete("/api/workouts/{workout_id}", status_code=204)
def delete_workout(
    workout_id: str,
    current_user: UserDB = Depends(require_coach),
    db: Session = Depends(get_db),
):
    w = _get_workout_or_404(workout_id, db)
    _assert_coach_athlete_link(current_user.id, w.athlete_id, db)
    db.query(CommentDB).filter(CommentDB.workout_id == workout_id).delete()
    db.delete(w)
    db.commit()


@app.put("/api/workouts/{workout_id}/status")
def update_workout_status(
    workout_id: str,
    update: WorkoutStatusUpdate,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    w = _get_workout_or_404(workout_id, db)
    _assert_athlete_access(current_user, w.athlete_id, db)
    if update.status not in {"planned", "done", "skipped"}:
        raise HTTPException(400, "Недопустимый статус")

    w.status = update.status
    w.athlete_feedback = update.athlete_feedback
    w.athlete_mood = update.athlete_mood
    w.perceived_exertion = update.perceived_exertion
    db.commit()
    db.refresh(w)
    return workout_to_card(w)


# ─── Watch import (.gpx / .fit) ──────────────────────────────────────────────

@app.post("/api/workouts/{workout_id}/import")
async def import_watch_file(
    workout_id: str,
    file: UploadFile = File(...),
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    w = _get_workout_or_404(workout_id, db)
    _assert_athlete_access(current_user, w.athlete_id, db)

    raw = await file.read()
    if not raw:
        raise HTTPException(400, "Файл пустой")

    name = (file.filename or "").lower()
    try:
        if name.endswith(".gpx"):
            data = _parse_gpx(raw)
        elif name.endswith(".fit"):
            data = _parse_fit(raw)
        else:
            raise HTTPException(400, "Поддерживаются только .gpx и .fit файлы")
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(400, f"Не удалось разобрать файл: {exc}")

    w.actual_distance_km    = data.get("distance_km")
    w.actual_duration_min   = data.get("duration_min")
    w.actual_avg_pace       = data.get("avg_pace")
    w.actual_avg_hr         = data.get("avg_hr")
    w.actual_max_hr         = data.get("max_hr")
    w.actual_calories       = data.get("calories")
    w.actual_elevation_gain = data.get("elevation_gain")
    if data.get("geojson"):
        w.route_geojson = data["geojson"]
    w.source_file = file.filename
    w.status = "done"
    db.commit()
    db.refresh(w)
    return workout_to_card(w)


def _parse_gpx(raw: bytes) -> dict:
    import gpxpy
    text = raw.decode("utf-8", errors="ignore")
    gpx = gpxpy.parse(text)

    coords: list[list[float]] = []
    hr_values: list[int] = []
    total_distance_m = 0.0
    elevation_gain_m = 0.0
    start_time = None
    end_time = None

    for track in gpx.tracks:
        for segment in track.segments:
            prev = None
            for pt in segment.points:
                coords.append([pt.longitude, pt.latitude])
                if pt.time:
                    if start_time is None or pt.time < start_time: start_time = pt.time
                    if end_time   is None or pt.time > end_time:   end_time = pt.time
                if prev is not None:
                    total_distance_m += pt.distance_2d(prev) or 0.0
                    if pt.elevation is not None and prev.elevation is not None:
                        diff = pt.elevation - prev.elevation
                        if diff > 0: elevation_gain_m += diff
                prev = pt
                # HR from extensions (optional)
                for ext in (pt.extensions or []):
                    for child in list(ext):
                        if child.tag.endswith("hr") and child.text:
                            try: hr_values.append(int(child.text))
                            except ValueError: pass

    distance_km   = round(total_distance_m / 1000.0, 2)
    duration_min  = int((end_time - start_time).total_seconds() / 60) if start_time and end_time else None
    avg_pace      = round(duration_min / distance_km, 2) if duration_min and distance_km > 0 else None
    avg_hr        = int(sum(hr_values) / len(hr_values)) if hr_values else None
    max_hr        = max(hr_values) if hr_values else None

    geojson = json.dumps({
        "type": "LineString",
        "coordinates": coords,
    }) if coords else None

    return {
        "distance_km":    distance_km,
        "duration_min":   duration_min,
        "avg_pace":       avg_pace,
        "avg_hr":         avg_hr,
        "max_hr":         max_hr,
        "calories":       None,
        "elevation_gain": round(elevation_gain_m, 1) if elevation_gain_m else None,
        "geojson":        geojson,
    }


def _parse_fit(raw: bytes) -> dict:
    import io
    from fitparse import FitFile
    fit = FitFile(io.BytesIO(raw))

    coords: list[list[float]] = []
    hr_values: list[int] = []
    total_distance_m = 0.0
    elev_first = None
    elev_max_gain = 0.0
    last_elev = None
    elapsed_seconds = 0
    calories = None

    for record in fit.get_messages("record"):
        v = {f.name: f.value for f in record.fields}
        lat = v.get("position_lat")
        lon = v.get("position_long")
        # FIT positions are stored as semicircles
        if lat is not None and lon is not None:
            lat_deg = lat * (180.0 / 2 ** 31)
            lon_deg = lon * (180.0 / 2 ** 31)
            coords.append([lon_deg, lat_deg])
        if v.get("heart_rate"):
            hr_values.append(int(v["heart_rate"]))
        if v.get("distance") is not None:
            total_distance_m = max(total_distance_m, float(v["distance"]))
        if v.get("altitude") is not None:
            altitude = float(v["altitude"])
            if last_elev is not None and altitude > last_elev:
                elev_max_gain += altitude - last_elev
            last_elev = altitude

    for sess in fit.get_messages("session"):
        v = {f.name: f.value for f in sess.fields}
        if v.get("total_distance") is not None and v["total_distance"] > total_distance_m:
            total_distance_m = float(v["total_distance"])
        if v.get("total_elapsed_time") is not None:
            elapsed_seconds = max(elapsed_seconds, int(v["total_elapsed_time"]))
        if v.get("total_calories"):
            calories = int(v["total_calories"])

    distance_km  = round(total_distance_m / 1000.0, 2)
    duration_min = int(elapsed_seconds / 60) if elapsed_seconds else None
    avg_pace     = round(duration_min / distance_km, 2) if duration_min and distance_km > 0 else None
    avg_hr       = int(sum(hr_values) / len(hr_values)) if hr_values else None
    max_hr       = max(hr_values) if hr_values else None

    geojson = json.dumps({
        "type": "LineString",
        "coordinates": coords,
    }) if coords else None

    return {
        "distance_km":    distance_km,
        "duration_min":   duration_min,
        "avg_pace":       avg_pace,
        "avg_hr":         avg_hr,
        "max_hr":         max_hr,
        "calories":       calories,
        "elevation_gain": round(elev_max_gain, 1) if elev_max_gain else None,
        "geojson":        geojson,
    }


@app.get("/api/workouts/{workout_id}/comments")
def list_comments(
    workout_id: str,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    w = _get_workout_or_404(workout_id, db)
    _assert_athlete_access(current_user, w.athlete_id, db)
    comments = db.query(CommentDB).filter(
        CommentDB.workout_id == workout_id
    ).order_by(CommentDB.created_at).all()
    return [
        {"id": c.id, "workoutId": c.workout_id, "author": c.author,
         "text": c.text, "createdAt": c.created_at}
        for c in comments
    ]


@app.post("/api/workouts/{workout_id}/comments", status_code=201)
def add_comment(
    workout_id: str,
    comment: CommentCreate,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    w = _get_workout_or_404(workout_id, db)
    _assert_athlete_access(current_user, w.athlete_id, db)
    c = CommentDB(
        id=new_id(), workout_id=workout_id,
        author=current_user.name,
        text=comment.text,
        created_at=datetime.utcnow().isoformat(),
    )
    db.add(c)
    db.commit()
    db.refresh(c)
    return {"id": c.id, "workoutId": c.workout_id, "author": c.author,
            "text": c.text, "createdAt": c.created_at}


# ─── Templates ───────────────────────────────────────────────────────────────

@app.get("/api/templates")
def list_templates(
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return [tpl_to_dict(t) for t in db.query(TemplateDB).order_by(TemplateDB.title).all()]


@app.post("/api/templates", status_code=201)
def create_template(
    tpl: TemplateCreate,
    current_user: UserDB = Depends(require_coach),
    db: Session = Depends(get_db),
):
    t = TemplateDB(
        id=new_id(), title=tpl.title, category=tpl.category,
        distance_km=tpl.distance_km, duration_min=tpl.duration_min,
        intensity=tpl.intensity, intervals_json=tpl.intervals_json,
        notes=tpl.notes, tags=tpl.tags,
    )
    db.add(t)
    db.commit()
    db.refresh(t)
    return tpl_to_dict(t)


@app.put("/api/templates/{template_id}")
def update_template(
    template_id: str,
    update: TemplateUpdate,
    current_user: UserDB = Depends(require_coach),
    db: Session = Depends(get_db),
):
    t = db.query(TemplateDB).filter(TemplateDB.id == template_id).first()
    if not t:
        raise HTTPException(404, "Шаблон не найден")
    for key, val in update.model_dump(exclude_none=True).items():
        if hasattr(t, key):
            setattr(t, key, val)
    db.commit()
    db.refresh(t)
    return tpl_to_dict(t)


@app.delete("/api/templates/{template_id}", status_code=204)
def delete_template(
    template_id: str,
    current_user: UserDB = Depends(require_coach),
    db: Session = Depends(get_db),
):
    t = db.query(TemplateDB).filter(TemplateDB.id == template_id).first()
    if not t:
        raise HTTPException(404, "Шаблон не найден")
    db.delete(t)
    db.commit()


@app.post("/api/templates/{template_id}/plan", status_code=201)
def plan_from_template(
    template_id: str,
    plan: PlanFromTemplate,
    current_user: UserDB = Depends(require_coach),
    db: Session = Depends(get_db),
):
    _assert_coach_athlete_link(current_user.id, plan.athlete_id, db)
    t = db.query(TemplateDB).filter(TemplateDB.id == template_id).first()
    if not t:
        raise HTTPException(404, "Шаблон не найден")
    w = WorkoutDB(
        id=new_id(), athlete_id=plan.athlete_id, date=plan.date,
        title=t.title, category=t.category,
        distance_km=t.distance_km, duration_min=t.duration_min,
        intensity=t.intensity, notes=t.notes,
        intervals_json=t.intervals_json, status="planned",
    )
    db.add(w)
    db.commit()
    db.refresh(w)
    return workout_to_card(w)


# ─── Analytics ───────────────────────────────────────────────────────────────

def _effective_distance(w: WorkoutDB) -> float:
    return w.actual_distance_km if w.actual_distance_km is not None else (w.distance_km or 0.0)

def _effective_duration(w: WorkoutDB) -> int:
    return w.actual_duration_min if w.actual_duration_min is not None else (w.duration_min or 0)


def _parse_iso_date(value: str) -> Optional[Date]:
    try:
        return Date.fromisoformat(value)
    except Exception:
        return None


def _coach_action_to_workout(action: dict[str, Any], athlete_id: str) -> WorkoutDB:
    return WorkoutDB(
        id=new_id(),
        athlete_id=athlete_id,
        date=action["date"],
        title=action["title"],
        category=action.get("category", "run"),
        distance_km=float(action.get("distanceKm", 0.0)),
        duration_min=int(action.get("durationMin", 0)),
        intensity=action.get("intensity", "moderate"),
        notes=action.get("notes", ""),
        intervals_json=action.get("intervalsJson", "[]"),
        status="planned",
    )


def _extract_json_object(raw: str) -> Optional[dict]:
    raw = (raw or "").strip()
    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.lower().startswith("json"):
            raw = raw[4:].strip()
    start = raw.find("{")
    end = raw.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    try:
        value = json.loads(raw[start:end + 1])
    except Exception:
        return None
    return value if isinstance(value, dict) else None


def _normalize_ai_report(candidate: dict, fallback: dict, horizon_days: int, model_name: str) -> dict:
    today = Date.today()
    max_date = today + timedelta(days=max(7, min(horizon_days, 42)))
    normalized = dict(fallback)
    normalized["modelMode"] = f"ollama-cloud:{model_name}"

    if isinstance(candidate.get("riskLevel"), str) and candidate["riskLevel"] in {"low", "medium", "high"}:
        normalized["riskLevel"] = candidate["riskLevel"]
    if isinstance(candidate.get("focus"), str) and candidate["focus"] in {"recover", "stabilize", "rebuild", "build"}:
        normalized["focus"] = candidate["focus"]

    recs = []
    for item in candidate.get("recommendations", []):
        if not isinstance(item, dict):
            continue
        title = str(item.get("title", "")).strip()[:120]
        detail = str(item.get("detail", "")).strip()[:500]
        priority = str(item.get("priority", "medium")).strip()
        if title and detail:
            recs.append({
                "title": title,
                "detail": detail,
                "priority": priority if priority in {"low", "medium", "high"} else "medium",
            })
    if recs:
        normalized["recommendations"] = recs[:6]

    actions = []
    for item in candidate.get("actions", []):
        if not isinstance(item, dict):
            continue
        action_date = _parse_iso_date(str(item.get("date", "")))
        if not action_date or action_date <= today or action_date > max_date:
            continue
        category = str(item.get("category", "run"))
        intensity = str(item.get("intensity", "moderate"))
        intervals = str(item.get("intervalsJson", "[]") or "[]")
        try:
            json.loads(intervals)
        except Exception:
            intervals = "[]"
        title = str(item.get("title", "")).strip()[:100]
        if not title:
            continue
        actions.append({
            "date": action_date.isoformat(),
            "title": title,
            "category": category if category in {"run", "bike", "swim"} else "run",
            "distanceKm": round(max(0.0, min(float(item.get("distanceKm", 0.0) or 0.0), 80.0)), 1),
            "durationMin": max(0, min(int(item.get("durationMin", 0) or 0), 300)),
            "intensity": intensity if intensity in {"easy", "moderate", "hard"} else "moderate",
            "notes": str(item.get("notes", "")).strip()[:700],
            "intervalsJson": intervals,
            "templateTitle": str(item.get("templateTitle", f"AI · {title}")).strip()[:100],
        })
    if actions:
        normalized["actions"] = actions[:10]

    templates = []
    for action in normalized["actions"]:
        templates.append({
            "title": action.get("templateTitle") or f"AI · {action['title']}",
            "category": action["category"],
            "distanceKm": action["distanceKm"],
            "durationMin": action["durationMin"],
            "intensity": action["intensity"],
            "notes": action["notes"],
            "tags": f"ai,{normalized['focus']},ollama",
            "intervalsJson": action["intervalsJson"],
        })
    normalized["templates"] = templates
    return normalized


def _try_ollama_cloud_report(athlete_id: str, db: Session, fallback: dict, horizon_days: int) -> Optional[dict]:
    api_key = os.getenv("OLLAMA_API_KEY", "").strip()
    if not api_key:
        fallback["cloudError"] = "OLLAMA_API_KEY is not set"
        return None

    workouts = db.query(WorkoutDB).filter(
        WorkoutDB.athlete_id == athlete_id,
        WorkoutDB.date >= (Date.today() - timedelta(days=84)).isoformat(),
    ).order_by(WorkoutDB.date).all()

    workout_rows = []
    for w in workouts[-80:]:
        workout_rows.append({
            "date": w.date,
            "title": w.title,
            "category": w.category,
            "plannedDistanceKm": w.distance_km,
            "plannedDurationMin": w.duration_min,
            "intensity": w.intensity,
            "status": w.status,
            "actualDistanceKm": w.actual_distance_km,
            "actualDurationMin": w.actual_duration_min,
            "avgPaceMinPerKm": w.actual_avg_pace,
            "avgHrBpm": w.actual_avg_hr,
            "mood": w.athlete_mood,
            "rpe": w.perceived_exertion,
            "feedback": (w.athlete_feedback or "")[:400],
        })

    system_prompt = (
        "You are an endurance training planning assistant for a coach. "
        "Analyze athlete progress and return only valid JSON. "
        "Do not include markdown. Do not include medical diagnosis. "
        "If pain, injury, extreme fatigue, or high RPE appears, reduce load and recommend coach review. "
        "Use Russian text for titles, notes, and recommendations. "
        "Consider athlete's goals when making recommendations - align training with their target events. "
        "Pay attention to success/failure patterns: build on what works, avoid what fails."
    )
    user_prompt = {
        "task": "Create training-plan corrections for the next days.",
        "requiredJsonShape": {
            "riskLevel": "low|medium|high",
            "focus": "recover|stabilize|rebuild|build",
            "recommendations": [{"title": "string", "detail": "string", "priority": "low|medium|high"}],
            "actions": [{
                "date": "YYYY-MM-DD",
                "title": "string",
                "category": "run|bike|swim",
                "distanceKm": 0,
                "durationMin": 0,
                "intensity": "easy|moderate|hard",
                "notes": "string",
                "intervalsJson": "[]",
                "templateTitle": "AI · string",
            }],
        },
        "constraints": [
            f"Plan only dates after {Date.today().isoformat()} and within {horizon_days} days.",
            "Return 3 to 7 actions.",
            "Use realistic progressive load and at least one easy/recovery day if risk is medium or high.",
            "intervalsJson must be a JSON string.",
        ],
        "fallbackSignalReport": fallback,
        "workouts": workout_rows,
        "athleteGoals": fallback.get("summary", {}).get("activeGoals", []),
        "successPatterns": fallback.get("summary", {}).get("successPatterns", []),
        "failurePatterns": fallback.get("summary", {}).get("failurePatterns", []),
    }

    try:
        import httpx
        with httpx.Client(timeout=45.0) as client:
            for model_name in _ollama_model_candidates():
                resp = client.post(
                    f"{OLLAMA_CLOUD_HOST.rstrip('/')}/api/chat",
                    headers={"Authorization": f"Bearer {api_key}"},
                    json={
                        "model": model_name,
                        "stream": False,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": json.dumps(user_prompt, ensure_ascii=False)},
                        ],
                        "options": {"temperature": 0.2},
                    },
                )
                if resp.status_code >= 400:
                    fallback["cloudError"] = f"{model_name}: HTTP {resp.status_code} {resp.text[:240]}"
                    continue
                content = resp.json().get("message", {}).get("content", "")
                candidate = _extract_json_object(content)
                if not candidate:
                    fallback["cloudError"] = f"{model_name}: response did not contain valid JSON"
                    continue
                return _normalize_ai_report(candidate, fallback, horizon_days, model_name)
        if not fallback.get("cloudError"):
            fallback["cloudError"] = "No Ollama Cloud model candidate returned a usable response"
        return None
    except Exception as e:
        fallback["cloudError"] = f"Ollama Cloud request failed: {type(e).__name__}: {e}"
        return None


def _recent_workout_context(athlete_id: str, db: Session, days: int = 84) -> list[dict[str, Any]]:
    workouts = db.query(WorkoutDB).filter(
        WorkoutDB.athlete_id == athlete_id,
        WorkoutDB.date >= (Date.today() - timedelta(days=days)).isoformat(),
    ).order_by(WorkoutDB.date).all()
    rows = []
    for w in workouts[-80:]:
        rows.append({
            "date": w.date,
            "title": w.title,
            "category": w.category,
            "plannedDistanceKm": w.distance_km,
            "plannedDurationMin": w.duration_min,
            "intensity": w.intensity,
            "status": w.status,
            "actualDistanceKm": w.actual_distance_km,
            "actualDurationMin": w.actual_duration_min,
            "avgPaceMinPerKm": w.actual_avg_pace,
            "avgHrBpm": w.actual_avg_hr,
            "mood": w.athlete_mood,
            "rpe": w.perceived_exertion,
            "feedback": (w.athlete_feedback or "")[:400],
        })
    return rows


def _fallback_ai_chat_answer(message: str, report: dict) -> str:
    summary = report.get("summary", {})
    recs = report.get("recommendations", [])
    actions = report.get("actions", [])
    first_rec = recs[0] if recs else {}
    lines = [
        f"Текущее состояние: риск {report.get('riskLevel', 'low')}, фокус {report.get('focus', 'build')}.",
        f"За период: выполнено {summary.get('completedWorkouts', 0)}, пропущено {summary.get('skippedWorkouts', 0)}, объем {summary.get('distanceKm', 0)} км, выполнение {round(float(summary.get('completionRate', 0)) * 100)}%.",
    ]
    if summary.get("avgRpe"):
        lines.append(f"Средний RPE: {summary.get('avgRpe')}.")
    if summary.get("painSignal"):
        lines.append("В обратной связи есть сигнал боли или сильной усталости, поэтому нагрузку лучше снижать.")
    if first_rec:
        lines.append(f"Главная корректировка: {first_rec.get('title')}. {first_rec.get('detail')}")
    if actions:
        lines.append("Ближайшее изменение плана: " + "; ".join(
            f"{a.get('date')} - {a.get('title')} ({a.get('distanceKm')} км, {a.get('durationMin')} мин)"
            for a in actions[:3]
        ))
    lines.append("Запрос тренера учтен: " + message[:300])
    return "\n".join(lines)


def _try_ollama_cloud_chat(athlete_id: str, db: Session, message: str, report: dict, horizon_days: int) -> Optional[str]:
    api_key = os.getenv("OLLAMA_API_KEY", "").strip()
    if not api_key:
        return None

    system_prompt = (
        "You are an AI assistant for a sports coach inside a training planning app. "
        "Answer in Russian. Be concrete and operational. "
        "Use athlete data and current plan context. "
        "Consider athlete's goals when making recommendations - align training with their target events. "
        "Pay attention to success/failure patterns: build on what works, avoid what fails. "
        "You may suggest corrections to workload, intensity, rest, templates, and calendar scheduling. "
        "Do not diagnose medical conditions; if pain or injury risk appears, advise reducing load and coach/medical review. "
        "Keep the answer concise: current state, reasoning, suggested corrections, next step."
    )
    user_payload = {
        "coachMessage": message,
        "today": Date.today().isoformat(),
        "horizonDays": horizon_days,
        "currentAiReport": report,
        "recentWorkouts": _recent_workout_context(athlete_id, db),
        "athleteGoals": report.get("summary", {}).get("activeGoals", []),
        "successPatterns": report.get("summary", {}).get("successPatterns", []),
        "failurePatterns": report.get("summary", {}).get("failurePatterns", []),
    }

    try:
        import httpx
        with httpx.Client(timeout=45.0) as client:
            for model_name in _ollama_model_candidates():
                resp = client.post(
                    f"{OLLAMA_CLOUD_HOST.rstrip('/')}/api/chat",
                    headers={"Authorization": f"Bearer {api_key}"},
                    json={
                        "model": model_name,
                        "stream": False,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": json.dumps(user_payload, ensure_ascii=False)},
                        ],
                        "options": {"temperature": 0.3},
                    },
                )
                if resp.status_code >= 400:
                    continue
                answer = resp.json().get("message", {}).get("content", "").strip()
                if answer:
                    return answer[:4000]
        return None
    except Exception:
        return None


def _build_ai_coach_report(athlete_id: str, db: Session, horizon_days: int = 14) -> dict:
    today = Date.today()
    window_start = today - timedelta(days=56)
    workouts = db.query(WorkoutDB).filter(
        WorkoutDB.athlete_id == athlete_id,
        WorkoutDB.date >= window_start.isoformat(),
    ).order_by(WorkoutDB.date).all()
    
    # Load athlete goals for context
    from sqlalchemy.orm import joinedload
    goals = db.query(GoalDB).filter(
        GoalDB.athlete_id == athlete_id,
        GoalDB.completed_at.is_(None),
    ).order_by(GoalDB.target_date).all()
    
    goals_context = []
    for g in goals:
        try:
            tgt = Date.fromisoformat(g.target_date)
            days_left = (tgt - today).days
        except Exception:
            days_left = None
        goals_context.append({
            "title": g.title,
            "type": g.type,
            "targetDate": g.target_date,
            "daysLeft": days_left,
            "targetValue": g.target_value,
            "targetUnit": g.target_unit,
        })

    done = [w for w in workouts if w.status == "done"]
    planned = [w for w in workouts if w.status == "planned" and w.date >= today.isoformat()]
    skipped = [w for w in workouts if w.status == "skipped"]
    
    # Analyze success/failure patterns
    success_patterns = []
    failure_patterns = []
    
    # Group workouts by week to identify patterns
    weekly_success_rate = {}
    for w in workouts:
        d = _parse_iso_date(w.date)
        if not d:
            continue
        week_key = d.strftime("%Y-W%W")
        if week_key not in weekly_success_rate:
            weekly_success_rate[week_key] = {"done": 0, "skipped": 0, "total": 0}
        weekly_success_rate[week_key]["total"] += 1
        if w.status == "done":
            weekly_success_rate[week_key]["done"] += 1
        elif w.status == "skipped":
            weekly_success_rate[week_key]["skipped"] += 1
    
    # Identify successful weeks (>=80% completion)
    for week, stats in weekly_success_rate.items():
        if stats["total"] >= 2:
            rate = stats["done"] / stats["total"]
            if rate >= 0.8:
                success_patterns.append(f"Неделя {week}: выполнение {round(rate*100)}%")
            elif rate < 0.5:
                failure_patterns.append(f"Неделя {week}: выполнение {round(rate*100)}% (низкое)")
    
    # Analyze what types of workouts are most often completed vs skipped
    category_completion = {}
    intensity_completion = {}
    for w in workouts:
        cat = w.category
        intensity = w.intensity
        if cat not in category_completion:
            category_completion[cat] = {"done": 0, "skipped": 0}
        if intensity not in intensity_completion:
            intensity_completion[intensity] = {"done": 0, "skipped": 0}
        
        if w.status == "done":
            category_completion[cat]["done"] += 1
            intensity_completion[intensity]["done"] += 1
        elif w.status == "skipped":
            category_completion[cat]["skipped"] += 1
            intensity_completion[intensity]["skipped"] += 1
    
    # Find best performing categories/intensities
    for cat, stats in category_completion.items():
        total = stats["done"] + stats["skipped"]
        if total >= 3:
            rate = stats["done"] / total
            if rate >= 0.75:
                success_patterns.append(f"{cat}: выполнение {round(rate*100)}% (успешный тип)")
            elif rate < 0.5:
                failure_patterns.append(f"{cat}: выполнение {round(rate*100)}% (часто пропускается)")
    
    for intensity, stats in intensity_completion.items():
        total = stats["done"] + stats["skipped"]
        if total >= 3:
            rate = stats["done"] / total
            if rate >= 0.75:
                success_patterns.append(f"{intensity}: выполнение {round(rate*100)}% (комфортная интенсивность)")
            elif rate < 0.5:
                failure_patterns.append(f"{intensity}: выполнение {round(rate*100)}% (часто пропускается)")
    
    total_distance = sum(_effective_distance(w) for w in done)
    total_duration = sum(_effective_duration(w) for w in done)
    avg_rpe_values = [w.perceived_exertion for w in done if w.perceived_exertion]
    avg_rpe = round(sum(avg_rpe_values) / len(avg_rpe_values), 1) if avg_rpe_values else None
    completion_base = len(done) + len(skipped)
    completion_rate = round(len(done) / completion_base, 2) if completion_base else 0.0

    recent_feedback = " ".join((w.athlete_feedback or "").lower() for w in done[-8:])
    pain_markers = ["pain", "ache", "бол", "травм", "устал", "слаб", "тяжел"]
    has_pain_signal = any(marker in recent_feedback for marker in pain_markers)

    weekly: dict[str, float] = {}
    for w in done:
        d = _parse_iso_date(w.date)
        if not d:
            continue
        week_start = d - timedelta(days=d.weekday())
        weekly[week_start.isoformat()] = weekly.get(week_start.isoformat(), 0.0) + _effective_distance(w)
    weekly_values = [round(v, 1) for _, v in sorted(weekly.items())][-6:]
    last_week = weekly_values[-1] if weekly_values else 0.0
    previous_week = weekly_values[-2] if len(weekly_values) > 1 else 0.0
    load_jump = previous_week > 0 and last_week > previous_week * 1.35

    risk_level = "low"
    if has_pain_signal or (avg_rpe is not None and avg_rpe >= 8) or load_jump:
        risk_level = "high"
    elif completion_rate < 0.65 or (avg_rpe is not None and avg_rpe >= 6.5):
        risk_level = "medium"

    focus = "build"
    if risk_level == "high":
        focus = "recover"
    elif completion_rate < 0.65:
        focus = "stabilize"
    elif last_week > 0 and previous_week > 0 and last_week < previous_week * 0.75:
        focus = "rebuild"

    recommendations: list[dict[str, str]] = []
    if focus == "recover":
        recommendations.append({
            "title": "Снизить нагрузку на ближайшую неделю",
            "detail": "Есть признаки усталости, боли или резкого скачка объема. Лучше убрать тяжелые работы и оставить легкие аэробные тренировки.",
            "priority": "high",
        })
    if focus == "stabilize":
        recommendations.append({
            "title": "Упростить план до регулярного ритма",
            "detail": "Процент выполнения низкий. План стоит сделать короче и предсказуемее, чтобы спортсмен снова стабильно закрывал тренировки.",
            "priority": "medium",
        })
    if focus in {"build", "rebuild"}:
        recommendations.append({
            "title": "Плавно нарастить объем",
            "detail": "Текущие данные позволяют добавить небольшой прогресс без резкого увеличения интенсивности.",
            "priority": "medium",
        })
    recommendations.append({
        "title": "Сверять план с самочувствием после каждой тренировки",
        "detail": "AI учитывает RPE, статус выполнения, фактический темп, пульс и текст обратной связи. Чем больше данных, тем точнее корректировки.",
        "priority": "low",
    })

    start = today + timedelta(days=1)
    base_distance = max(3.0, min(12.0, round((total_distance / max(len(done), 1)) or 5.0, 1)))
    actions: list[dict[str, Any]] = []
    if focus == "recover":
        pattern = [
            (1, "Восстановительный бег", "easy", 0.55, 30),
            (3, "Мобилити + легкая аэробика", "easy", 0.0, 35),
            (6, "Легкий контрольный бег", "easy", 0.7, 40),
            (10, "Ровный бег без форсирования", "moderate", 0.8, 45),
        ]
    elif focus == "stabilize":
        pattern = [
            (1, "Легкий бег по самочувствию", "easy", 0.7, 35),
            (4, "Ровная аэробная тренировка", "moderate", 0.85, 45),
            (7, "Длинная легкая тренировка", "easy", 1.05, 55),
            (11, "Техника + короткие ускорения", "moderate", 0.8, 45),
        ]
    else:
        pattern = [
            (1, "Легкий бег + техника", "easy", 0.85, 40),
            (3, "Темповая работа контролируемо", "hard", 0.75, 45),
            (6, "Длинная аэробная тренировка", "easy", 1.25, 65),
            (9, "Восстановительный бег", "easy", 0.65, 35),
            (12, "Прогрессивная тренировка", "moderate", 1.0, 55),
        ]

    for offset, title, intensity, distance_factor, duration in pattern:
        if offset > horizon_days:
            continue
        dist = round(base_distance * distance_factor, 1) if distance_factor else 0.0
        actions.append({
            "date": (start + timedelta(days=offset - 1)).isoformat(),
            "title": title,
            "category": "run",
            "distanceKm": dist,
            "durationMin": duration,
            "intensity": intensity,
            "notes": f"AI Coach: {recommendations[0]['title']}",
            "intervalsJson": "[]",
            "templateTitle": f"AI · {title}",
        })

    templates = []
    seen = set()
    for action in actions:
        key = (action["title"], action["intensity"])
        if key in seen:
            continue
        seen.add(key)
        templates.append({
            "title": action["templateTitle"],
            "category": action["category"],
            "distanceKm": action["distanceKm"],
            "durationMin": action["durationMin"],
            "intensity": action["intensity"],
            "notes": action["notes"],
            "tags": f"ai,{focus}",
            "intervalsJson": "[]",
        })

    local_report = {
        "modelMode": "local-coach-engine",
        "athleteId": athlete_id,
        "generatedAt": datetime.utcnow().isoformat(),
        "horizonDays": horizon_days,
        "riskLevel": risk_level,
        "focus": focus,
        "summary": {
            "completedWorkouts": len(done),
            "plannedWorkouts": len(planned),
            "skippedWorkouts": len(skipped),
            "completionRate": completion_rate,
            "distanceKm": round(total_distance, 1),
            "durationMin": total_duration,
            "avgRpe": avg_rpe,
            "lastWeekKm": round(last_week, 1),
            "previousWeekKm": round(previous_week, 1),
            "loadJump": load_jump,
            "painSignal": has_pain_signal,
            "successPatterns": success_patterns,
            "failurePatterns": failure_patterns,
            "activeGoals": goals_context,
        },
        "recommendations": recommendations,
        "actions": actions,
        "templates": templates,
    }
    return _try_ollama_cloud_report(athlete_id, db, local_report, horizon_days) or local_report


@app.get("/api/ai/coach/analysis")
def ai_coach_analysis(
    athlete_id: str,
    horizon_days: int = Query(14, ge=7, le=42),
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _assert_athlete_access(current_user, athlete_id, db)
    return _build_ai_coach_report(athlete_id, db, horizon_days)


@app.post("/api/ai/coach/apply")
def apply_ai_coach_plan(
    data: AICoachApplyRequest,
    current_user: UserDB = Depends(require_coach),
    db: Session = Depends(get_db),
):
    _assert_coach_athlete_link(current_user.id, data.athlete_id, db)
    horizon = max(7, min(data.horizon_days, 42))
    report = _build_ai_coach_report(data.athlete_id, db, horizon)

    created_templates = 0
    created_workouts = 0

    if data.create_templates:
        existing_titles = {
            t.title for t in db.query(TemplateDB).filter(TemplateDB.title.like("AI ·%")).all()
        }
        for tpl in report["templates"]:
            if tpl["title"] in existing_titles:
                continue
            db.add(TemplateDB(
                id=new_id(),
                title=tpl["title"],
                category=tpl["category"],
                distance_km=tpl["distanceKm"],
                duration_min=tpl["durationMin"],
                intensity=tpl["intensity"],
                intervals_json=tpl["intervalsJson"],
                notes=tpl["notes"],
                tags=tpl["tags"],
            ))
            created_templates += 1

    if data.apply_schedule:
        for action in report["actions"]:
            exists = db.query(WorkoutDB).filter(
                WorkoutDB.athlete_id == data.athlete_id,
                WorkoutDB.date == action["date"],
                WorkoutDB.title == action["title"],
            ).first()
            if exists:
                continue
            db.add(_coach_action_to_workout(action, data.athlete_id))
            created_workouts += 1

    db.commit()
    return {
        "createdTemplates": created_templates,
        "createdWorkouts": created_workouts,
        "report": report,
    }


@app.post("/api/ai/coach/chat")
def ai_coach_chat(
    data: AICoachChatRequest,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _assert_athlete_access(current_user, data.athlete_id, db)
    message = data.message.strip()
    if not message:
        raise HTTPException(400, "Сообщение не может быть пустым")
    horizon = max(7, min(data.horizon_days, 42))
    report = _build_ai_coach_report(data.athlete_id, db, horizon)
    answer = _try_ollama_cloud_chat(data.athlete_id, db, message, report, horizon)
    if not answer:
        answer = _fallback_ai_chat_answer(message, report)
    return {
        "message": answer,
        "modelMode": report.get("modelMode", "local-coach-engine"),
        "report": report,
    }


@app.get("/api/analytics")
def get_analytics(
    athlete_id: str,
    period: str = Query("all"),       # 30d | 90d | year | all
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _assert_athlete_access(current_user, athlete_id, db)

    today = Date.today()
    period_start: Optional[Date] = None
    if period == "30d":  period_start = today - timedelta(days=30)
    elif period == "90d": period_start = today - timedelta(days=90)
    elif period == "year": period_start = today - timedelta(days=365)

    q = db.query(WorkoutDB).filter(WorkoutDB.athlete_id == athlete_id)
    if period_start:
        q = q.filter(WorkoutDB.date >= period_start.strftime("%Y-%m-%d"))
    workouts = q.all()

    done = [w for w in workouts if w.status == "done"]
    planned_count = sum(1 for w in workouts if w.status == "planned")
    skipped_count = sum(1 for w in workouts if w.status == "skipped")

    by_intensity = {"easy": 0, "moderate": 0, "hard": 0}
    by_category  = {"run": 0, "bike": 0, "swim": 0}
    by_status    = {"planned": 0, "done": 0, "skipped": 0}
    for w in workouts:
        by_intensity[w.intensity] = by_intensity.get(w.intensity, 0) + 1
        by_category[w.category]   = by_category.get(w.category,   0) + 1
        by_status[w.status]       = by_status.get(w.status,       0) + 1

    distance_total = sum(_effective_distance(w) for w in done)
    duration_total = sum(_effective_duration(w) for w in done)

    avg_pace = round(duration_total / distance_total, 2) if distance_total > 0 else None

    hr_values = [w.actual_avg_hr for w in done if w.actual_avg_hr]
    avg_hr = int(sum(hr_values) / len(hr_values)) if hr_values else None

    total_logged = len(done) + planned_count + skipped_count
    completion_rate = round(len(done) / total_logged, 2) if total_logged > 0 else 0.0

    # ── Streak (consecutive days with completed workout, ending today/yesterday) ──
    done_dates = sorted({w.date for w in done}, reverse=True)
    current_streak = 0
    cursor = today
    done_set = set(done_dates)
    if done_set:
        # allow streak to start from today OR yesterday (rest day tolerance)
        if cursor.strftime("%Y-%m-%d") not in done_set:
            cursor = cursor - timedelta(days=1)
        while cursor.strftime("%Y-%m-%d") in done_set:
            current_streak += 1
            cursor = cursor - timedelta(days=1)

    longest_streak = 0
    if done_dates:
        run = 1
        sorted_asc = sorted(done_set)
        prev = Date.fromisoformat(sorted_asc[0])
        longest_streak = 1
        for ds in sorted_asc[1:]:
            d = Date.fromisoformat(ds)
            if (d - prev).days == 1:
                run += 1
                longest_streak = max(longest_streak, run)
            else:
                run = 1
            prev = d

    # ── Weekly volume (last 8 weeks, Mon-anchored) ────────────────────────────
    weekly: dict[str, dict] = {}
    for w in done:
        d = Date.fromisoformat(w.date)
        week_start = d - timedelta(days=d.weekday())
        key = week_start.strftime("%Y-%m-%d")
        e = weekly.setdefault(key, {"weekStart": key, "distance": 0.0, "duration": 0, "count": 0})
        e["distance"] += _effective_distance(w)
        e["duration"] += _effective_duration(w)
        e["count"] += 1
    weekly_list = sorted(weekly.values(), key=lambda x: x["weekStart"])[-8:]
    for e in weekly_list:
        e["distance"] = round(e["distance"], 1)

    # ── Monthly volume (last 6 months) ────────────────────────────────────────
    monthly: dict[str, dict] = {}
    for w in done:
        m = w.date[:7]
        e = monthly.setdefault(m, {"month": m, "distance": 0.0, "duration": 0, "count": 0})
        e["distance"] += _effective_distance(w)
        e["duration"] += _effective_duration(w)
        e["count"] += 1
    monthly_list = sorted(monthly.values(), key=lambda x: x["month"])[-6:]
    for e in monthly_list:
        e["distance"] = round(e["distance"], 1)

    # ── Active goals + progress ───────────────────────────────────────────────
    goals = db.query(GoalDB).filter(
        GoalDB.athlete_id == athlete_id,
        GoalDB.completed_at.is_(None),
    ).order_by(GoalDB.target_date).all()

    active_goals = []
    for g in goals:
        try:
            tgt = Date.fromisoformat(g.target_date)
            days_left = (tgt - today).days
        except Exception:
            days_left = None

        progress = 0.0
        if g.type == "volume" and g.target_value:
            try:
                created = Date.fromisoformat(g.created_at[:10])
            except Exception:
                created = today
            done_in_window = [w for w in done if Date.fromisoformat(w.date) >= created]
            progressed = sum(_effective_distance(w) for w in done_in_window)
            progress = min(1.0, round(progressed / g.target_value, 3))

        active_goals.append({
            "id": g.id,
            "title": g.title,
            "targetDate": g.target_date,
            "type": g.type,
            "targetValue": g.target_value,
            "targetUnit": g.target_unit,
            "daysLeft": days_left,
            "progress": progress,
        })

    return {
        "workoutsCount":  len(done),
        "plannedCount":   planned_count,
        "skippedCount":   skipped_count,
        "completionRate": completion_rate,
        "distanceTotal":  round(distance_total, 1),
        "durationTotal":  duration_total,
        "avgPaceMinPerKm": avg_pace,
        "avgHrBpm":        avg_hr,
        "currentStreak":   current_streak,
        "longestStreak":   longest_streak,
        "byIntensity":     by_intensity,
        "byCategory":      by_category,
        "byStatus":        by_status,
        "weeklyVolume":    weekly_list,
        "monthlyVolume":   monthly_list,
        "activeGoals":     active_goals,
    }


# ─── Goals ───────────────────────────────────────────────────────────────────

class GoalCreate(BaseModel):
    athlete_id: str
    title: str
    target_date: str
    type: str = "race"               # race | volume | weight
    target_value: Optional[float] = None
    target_unit: Optional[str] = None


@app.get("/api/goals")
def list_goals(
    athlete_id: str,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _assert_athlete_access(current_user, athlete_id, db)
    goals = db.query(GoalDB).filter(GoalDB.athlete_id == athlete_id) \
        .order_by(GoalDB.target_date).all()
    return [_goal_to_dict(g) for g in goals]


@app.post("/api/goals", status_code=201)
def create_goal(
    data: GoalCreate,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _assert_athlete_access(current_user, data.athlete_id, db)
    goal = GoalDB(
        id=new_id(),
        athlete_id=data.athlete_id,
        title=data.title,
        target_date=data.target_date,
        type=data.type,
        target_value=data.target_value,
        target_unit=data.target_unit,
        created_at=datetime.utcnow().isoformat(),
    )
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return _goal_to_dict(goal)


@app.delete("/api/goals/{goal_id}", status_code=204)
def delete_goal(
    goal_id: str,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    g = db.query(GoalDB).filter(GoalDB.id == goal_id).first()
    if not g:
        raise HTTPException(404, "Цель не найдена")
    _assert_athlete_access(current_user, g.athlete_id, db)
    db.delete(g)
    db.commit()


def _goal_to_dict(g: GoalDB) -> dict:
    return {
        "id":          g.id,
        "athleteId":   g.athlete_id,
        "title":       g.title,
        "targetDate":  g.target_date,
        "type":        g.type,
        "targetValue": g.target_value,
        "targetUnit":  g.target_unit,
        "createdAt":   g.created_at,
        "completedAt": g.completed_at,
    }


# ─── Access helpers ───────────────────────────────────────────────────────────

def _assert_athlete_access(user: UserDB, athlete_id: str, db: Session) -> None:
    if user.role == "athlete":
        if user.athlete_id != athlete_id:
            raise HTTPException(403, "Нет доступа")
    else:
        _assert_coach_athlete_link(user.id, athlete_id, db)


def _assert_coach_athlete_link(coach_user_id: str, athlete_id: str, db: Session) -> None:
    link = db.query(CoachAthleteLinkDB).filter(
        CoachAthleteLinkDB.coach_user_id == coach_user_id,
        CoachAthleteLinkDB.athlete_id == athlete_id,
    ).first()
    if not link:
        raise HTTPException(403, "Нет доступа к этому атлету")


def _get_workout_or_404(workout_id: str, db: Session) -> WorkoutDB:
    w = db.query(WorkoutDB).filter(WorkoutDB.id == workout_id).first()
    if not w:
        raise HTTPException(404, "Тренировка не найдена")
    return w


# ─── Routes ───────────────────────────────────────────────────────────────────

class RouteGenerateRequest(BaseModel):
    start_lat: float
    start_lon: float
    distance_km: float
    preferences: str = ""


class OpenAiKeyRequest(BaseModel):
    key: str


def _route_to_dict(r: RouteDB) -> dict:
    return {
        "id":          r.id,
        "name":        r.name,
        "distanceKm":  r.distance_km,
        "geojson":     r.geojson,
        "description": r.description,
        "startLat":    r.start_lat,
        "startLon":    r.start_lon,
        "createdAt":   r.created_at,
    }


@app.get("/api/routes")
def get_routes(
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    routes = db.query(RouteDB).filter(RouteDB.user_id == current_user.id).all()
    return [_route_to_dict(r) for r in routes]


@app.delete("/api/routes/{route_id}", status_code=204)
def delete_route(
    route_id: str,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    r = db.query(RouteDB).filter(RouteDB.id == route_id, RouteDB.user_id == current_user.id).first()
    if not r:
        raise HTTPException(404, "Маршрут не найден")
    db.delete(r)
    db.commit()


@app.put("/api/auth/openai-key", status_code=204)
def set_openai_key(
    data: OpenAiKeyRequest,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Store user's OpenAI API key (plaintext — user owns the key)."""
    current_user.openai_key = data.key.strip()
    db.commit()


@app.get("/api/auth/openai-key")
def get_openai_key_status(
    current_user: UserDB = Depends(get_current_user),
):
    """Returns whether the user has an OpenAI key set (not the key itself)."""
    return {"hasKey": bool(current_user.openai_key)}


@app.post("/api/routes/generate")
def generate_route(
    data: RouteGenerateRequest,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Generate a circular running route using geometric waypoints + OSRM road snapping.
    No AI or paid API required — completely free.
    """
    import math, httpx

    lat = data.start_lat
    lon = data.start_lon
    target_km = data.distance_km

    # ── Step 1: Generate circular waypoints ────────────────────────────────────
    # radius so that a loop through N points ≈ target_km
    n_points = 5  # pentagon gives a natural variety
    radius_km = target_km / (2 * math.pi)

    dlat = radius_km / 111.0
    dlon = radius_km / (111.0 * max(math.cos(math.radians(lat)), 0.01))

    # Start going roughly north, then clockwise
    waypoints: list = [[lon, lat]]
    for i in range(1, n_points + 1):
        angle = -math.pi / 2 + 2 * math.pi * i / n_points
        wlat = lat + dlat * math.sin(angle)
        wlon = lon + dlon * math.cos(angle)
        waypoints.append([wlon, wlat])
    waypoints.append([lon, lat])   # close the loop

    # ── Step 2: Reverse-geocode start to get location name (Nominatim, free) ───
    route_name = f"Маршрут {target_km:.0f} км"
    try:
        with httpx.Client(timeout=6, headers={"User-Agent": "PeMa/2.0"}) as client:
            nom = client.get(
                f"https://nominatim.openstreetmap.org/reverse"
                f"?lat={lat}&lon={lon}&format=json&zoom=14"
            )
        if nom.status_code == 200:
            addr = nom.json().get("address", {})
            locality = (
                addr.get("suburb") or addr.get("neighbourhood") or
                addr.get("city_district") or addr.get("village") or
                addr.get("town") or addr.get("city", "")
            )
            if locality:
                route_name = f"{locality} · {target_km:.0f} км"
    except Exception:
        pass

    # ── Step 3: Snap to road network via OSRM (free public server) ─────────────
    coords_str = ";".join(f"{p[0]},{p[1]}" for p in waypoints)
    geojson_coords = waypoints   # fallback: straight lines
    actual_dist = target_km

    try:
        with httpx.Client(timeout=15) as client:
            osrm_resp = client.get(
                f"http://router.project-osrm.org/route/v1/foot/{coords_str}"
                f"?overview=full&geometries=geojson"
            )
        if osrm_resp.status_code == 200:
            osrm_data = osrm_resp.json()
            osrm_routes = osrm_data.get("routes", [])
            if osrm_routes:
                geojson_coords = osrm_routes[0]["geometry"]["coordinates"]
                actual_dist = osrm_routes[0].get("distance", 0) / 1000.0
    except Exception:
        pass   # offline / unavailable → use geometric waypoints

    description = f"Круговой маршрут {actual_dist:.1f} км по дорогам"
    if data.preferences:
        description += f" · {data.preferences}"

    geojson = json.dumps({"type": "LineString", "coordinates": geojson_coords})

    # ── Step 4: Persist ─────────────────────────────────────────────────────────
    route = RouteDB(
        id=new_id(),
        user_id=current_user.id,
        name=route_name,
        distance_km=round(actual_dist, 2),
        geojson=geojson,
        description=description,
        start_lat=lat,
        start_lon=lon,
        created_at=datetime.utcnow().isoformat(),
    )
    db.add(route)
    db.commit()
    db.refresh(route)
    return _route_to_dict(route)


# ── Custom waypoints route (from map editor) ──────────────────────────────────

class CustomRouteRequest(BaseModel):
    waypoints: list   # [[lon, lat], ...]
    name: str = "Мой маршрут"

@app.post("/api/routes/from-waypoints")
def route_from_waypoints(
    data: CustomRouteRequest,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Build a route from user-drawn waypoints via OSRM, then save."""
    import httpx

    wps = data.waypoints
    if len(wps) < 2:
        raise HTTPException(400, "Нужно минимум 2 точки")

    coords_str = ";".join(f"{p[0]},{p[1]}" for p in wps)
    geojson_coords = wps
    actual_dist = 0.0

    try:
        with httpx.Client(timeout=15) as client:
            resp = client.get(
                f"http://router.project-osrm.org/route/v1/foot/{coords_str}"
                f"?overview=full&geometries=geojson"
            )
        if resp.status_code == 200:
            rdata = resp.json().get("routes", [])
            if rdata:
                geojson_coords = rdata[0]["geometry"]["coordinates"]
                actual_dist = rdata[0].get("distance", 0) / 1000.0
    except Exception:
        pass

    geojson = json.dumps({"type": "LineString", "coordinates": geojson_coords})
    route = RouteDB(
        id=new_id(),
        user_id=current_user.id,
        name=data.name,
        distance_km=round(actual_dist, 2),
        geojson=geojson,
        description=f"Ручной маршрут {actual_dist:.1f} км",
        start_lat=wps[0][1],
        start_lon=wps[0][0],
        created_at=datetime.utcnow().isoformat(),
    )
    db.add(route); db.commit(); db.refresh(route)
    return _route_to_dict(route)


# ── Strava OAuth ──────────────────────────────────────────────────────────────

class StravaCredentials(BaseModel):
    client_id: str
    client_secret: str

@app.put("/api/strava/credentials", status_code=204)
def save_strava_credentials(
    data: StravaCredentials,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    current_user.strava_client_id = data.client_id.strip()
    current_user.strava_client_secret = data.client_secret.strip()
    db.commit()

@app.get("/api/strava/auth-url")
def strava_auth_url(current_user: UserDB = Depends(get_current_user)):
    cid = current_user.strava_client_id
    if not cid:
        raise HTTPException(400, "Сначала укажите Strava Client ID в настройках")
    redirect = "http://localhost:8000/api/strava/callback"
    url = (
        f"https://www.strava.com/oauth/authorize"
        f"?client_id={cid}&response_type=code&redirect_uri={redirect}"
        f"&approval_prompt=force&scope=activity:read_all"
    )
    return {"url": url}

@app.get("/api/strava/callback")
def strava_callback(
    code: str,
    db: Session = Depends(get_db),
):
    """
    Strava redirects here after user approves.
    We exchange the code for tokens — but we can't know which user this is
    without state. For simplicity, exchange tokens for the last user who
    initiated connect (or store pending code with TTL).
    We return a simple HTML page telling user to go back to the app.
    """
    import httpx, time
    from fastapi.responses import HTMLResponse

    # Find user with pending strava credentials (has client_id but no access_token yet)
    user = db.query(UserDB).filter(
        UserDB.strava_client_id.isnot(None),
        UserDB.strava_access_token.is_(None),
    ).order_by(UserDB.created_at.desc()).first()

    if not user or not user.strava_client_secret:
        return HTMLResponse("<h2>Ошибка: не найден пользователь с Strava Client ID. Попробуйте снова.</h2>")

    try:
        with httpx.Client(timeout=10) as client:
            resp = client.post("https://www.strava.com/oauth/token", data={
                "client_id":     user.strava_client_id,
                "client_secret": user.strava_client_secret,
                "code":          code,
                "grant_type":    "authorization_code",
            })
        if resp.status_code != 200:
            return HTMLResponse(f"<h2>Ошибка Strava: {resp.text[:200]}</h2>")

        tok = resp.json()
        user.strava_access_token  = tok.get("access_token")
        user.strava_refresh_token = tok.get("refresh_token")
        user.strava_token_expiry  = tok.get("expires_at", int(time.time()) + 21600)
        user.strava_athlete_id    = str(tok.get("athlete", {}).get("id", ""))
        db.commit()
    except Exception as e:
        return HTMLResponse(f"<h2>Ошибка: {e}</h2>")

    return HTMLResponse("""
        <html><body style="font-family:sans-serif;text-align:center;padding:60px">
        <h2>✅ Strava подключена!</h2>
        <p>Вернитесь в приложение PeMa и нажмите «Синхронизировать».</p>
        </body></html>
    """)

@app.get("/api/strava/status")
def strava_status(current_user: UserDB = Depends(get_current_user)):
    return {
        "connected":   bool(current_user.strava_access_token),
        "hasClientId": bool(current_user.strava_client_id),
        "athleteId":   current_user.strava_athlete_id or "",
    }

@app.delete("/api/strava/disconnect", status_code=204)
def strava_disconnect(
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Revoke stored Strava tokens (keeps client credentials for easy reconnect)."""
    current_user.strava_access_token  = None
    current_user.strava_refresh_token = None
    current_user.strava_token_expiry  = None
    current_user.strava_athlete_id    = None
    db.commit()

def _refresh_strava_token(user: UserDB, db: Session) -> bool:
    import httpx, time
    if not user.strava_refresh_token:
        return False
    try:
        with httpx.Client(timeout=10) as client:
            resp = client.post("https://www.strava.com/oauth/token", data={
                "client_id":     user.strava_client_id,
                "client_secret": user.strava_client_secret,
                "grant_type":    "refresh_token",
                "refresh_token": user.strava_refresh_token,
            })
        if resp.status_code == 200:
            tok = resp.json()
            user.strava_access_token  = tok["access_token"]
            user.strava_refresh_token = tok["refresh_token"]
            user.strava_token_expiry  = tok["expires_at"]
            db.commit()
            return True
    except Exception:
        pass
    return False

@app.post("/api/strava/sync")
def strava_sync(
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Pull recent Strava activities and create/update workouts."""
    import httpx, time

    if not current_user.strava_access_token:
        raise HTTPException(400, "Strava не подключена")

    # Refresh token if expired
    expiry = current_user.strava_token_expiry or 0
    if time.time() > expiry - 60:
        if not _refresh_strava_token(current_user, db):
            raise HTTPException(401, "Не удалось обновить токен Strava. Переподключитесь.")

    try:
        with httpx.Client(timeout=15) as client:
            resp = client.get(
                "https://www.strava.com/api/v3/athlete/activities",
                headers={"Authorization": f"Bearer {current_user.strava_access_token}"},
                params={"per_page": 30, "page": 1},
            )
        if resp.status_code == 401:
            current_user.strava_access_token = None
            db.commit()
            raise HTTPException(401, "Strava отклонила токен. Переподключитесь.")
        if resp.status_code != 200:
            raise HTTPException(502, f"Strava API error {resp.status_code}")

        activities = resp.json()
    except httpx.RequestError as e:
        raise HTTPException(502, f"Ошибка сети: {e}")

    created = 0
    for act in activities:
        strava_id = f"strava_{act['id']}"
        # Skip if already imported
        existing = db.query(WorkoutDB).filter(WorkoutDB.source_file == strava_id).first()
        if existing:
            continue

        cat_map = {
            "Run": "run", "VirtualRun": "run",
            "Ride": "bike", "VirtualRide": "bike",
            "Swim": "swim",
        }
        cat = cat_map.get(act.get("type", ""), "run")
        start_date = (act.get("start_date_local") or act.get("start_date") or "")[:10]
        dist_km = round(act.get("distance", 0) / 1000.0, 2)
        dur_min = round(act.get("moving_time", 0) / 60)
        avg_hr  = act.get("average_heartrate")
        max_hr  = act.get("max_heartrate")
        elev    = act.get("total_elevation_gain")
        avg_speed = act.get("average_speed", 0)  # m/s
        avg_pace  = (1000 / avg_speed / 60) if avg_speed > 0 else None

        # Build GeoJSON from summary_polyline
        route_geojson = None
        poly = act.get("map", {}).get("summary_polyline", "")
        if poly:
            try:
                coords = _decode_polyline(poly)
                route_geojson = json.dumps({"type": "LineString", "coordinates": coords})
            except Exception:
                pass

        w = WorkoutDB(
            id=new_id(),
            title=act.get("name") or f"Strava · {cat}",
            category=cat,
            distance_km=dist_km,
            duration_min=dur_min,
            intensity="moderate",
            status="done",
            date=start_date,
            notes=f"Импортировано из Strava",
            source_file=strava_id,
            actual_distance_km=dist_km,
            actual_duration_min=dur_min,
            actual_avg_pace=avg_pace,
            actual_avg_hr=int(avg_hr) if avg_hr else None,
            actual_max_hr=int(max_hr) if max_hr else None,
            actual_elevation_gain=elev,
            route_geojson=route_geojson,
        )
        # Assign to current user's athlete
        if current_user.athlete_id:
            w.athlete_id = current_user.athlete_id
        db.add(w)
        created += 1

    db.commit()
    return {"synced": created, "total": len(activities)}


def _decode_polyline(polyline_str: str) -> list:
    """Decode Google-encoded polyline to [[lon, lat], ...] list."""
    coords = []
    index = 0; lat = 0; lng = 0
    while index < len(polyline_str):
        result = 0; shift = 0
        while True:
            b = ord(polyline_str[index]) - 63; index += 1
            result |= (b & 0x1f) << shift; shift += 5
            if b < 0x20: break
        dlat = ~(result >> 1) if result & 1 else result >> 1
        lat += dlat
        result = 0; shift = 0
        while True:
            b = ord(polyline_str[index]) - 63; index += 1
            result |= (b & 0x1f) << shift; shift += 5
            if b < 0x20: break
        dlng = ~(result >> 1) if result & 1 else result >> 1
        lng += dlng
        coords.append([lng / 1e5, lat / 1e5])  # [lon, lat] for GeoJSON
    return coords
