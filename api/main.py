"""
PeMa API v2 — FastAPI + SQLAlchemy (SQLite)
Auth: JWT Bearer tokens, bcrypt passwords
Run: uvicorn api.main:app --reload --port 8000
"""
from __future__ import annotations

import calendar as cal_module
import json
import os

# Load .env if present (development convenience)
try:
    from pathlib import Path as _Path
    _env = _Path(__file__).parent / ".env"
    if _env.exists():
        for _line in _env.read_text().splitlines():
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _, _v = _line.partition("=")
                os.environ.setdefault(_k.strip(), _v.strip())
except Exception:
    pass
import uuid
from datetime import date as Date, datetime, timedelta
from typing import Optional

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
    notes = Column(Text, default="")   # coach's private notes about this athlete


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

        # coach_athlete_links: notes column
        existing_cal = {row[1] for row in conn.execute(text("PRAGMA table_info(coach_athlete_links)"))}
        if "notes" not in existing_cal:
            conn.execute(text("ALTER TABLE coach_athlete_links ADD COLUMN notes TEXT DEFAULT ''"))


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


# ─── Coach notes ─────────────────────────────────────────────────────────────

@app.get("/api/athletes/{athlete_id}/notes")
def get_coach_notes(
    athlete_id: str,
    current_user: UserDB = Depends(require_coach),
    db: Session = Depends(get_db),
):
    link = db.query(CoachAthleteLinkDB).filter(
        CoachAthleteLinkDB.coach_user_id == current_user.id,
        CoachAthleteLinkDB.athlete_id == athlete_id,
    ).first()
    if not link:
        raise HTTPException(404, "Атлет не найден")
    return {"notes": link.notes or ""}


class CoachNotesUpdate(BaseModel):
    notes: str


@app.put("/api/athletes/{athlete_id}/notes", status_code=200)
def update_coach_notes(
    athlete_id: str,
    data: CoachNotesUpdate,
    current_user: UserDB = Depends(require_coach),
    db: Session = Depends(get_db),
):
    link = db.query(CoachAthleteLinkDB).filter(
        CoachAthleteLinkDB.coach_user_id == current_user.id,
        CoachAthleteLinkDB.athlete_id == athlete_id,
    ).first()
    if not link:
        raise HTTPException(404, "Атлет не найден")
    link.notes = data.notes
    db.commit()
    return {"notes": link.notes}


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


@app.get("/api/analytics")
def get_analytics(
    athlete_id: str,
    period: str = Query("all"),       # 7d | 30d | 90d | year | all
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _assert_athlete_access(current_user, athlete_id, db)

    today = Date.today()
    period_start: Optional[Date] = None
    if period == "7d":   period_start = today - timedelta(days=7)
    elif period == "30d":  period_start = today - timedelta(days=30)
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

    # For goal progress we need ALL workouts regardless of the period filter
    all_athlete_workouts = db.query(WorkoutDB).filter(
        WorkoutDB.athlete_id == athlete_id
    ).all()
    all_done = [w for w in all_athlete_workouts if w.status == "done"]

    active_goals = []
    for g in goals:
        try:
            tgt = Date.fromisoformat(g.target_date)
            days_left = (tgt - today).days
        except Exception:
            tgt = today
            days_left = None

        try:
            goal_created = Date.fromisoformat(g.created_at[:10])
        except Exception:
            goal_created = today

        # Workouts since goal was created
        done_since = [w for w in all_done
                      if Date.fromisoformat(w.date) >= goal_created]

        progress = 0.0
        progress_label = "авто 50/50"
        actual_value = None

        if g.target_value:
            unit = (g.target_unit or "km").lower()
            if unit == "km":
                actual = round(sum(_effective_distance(w) for w in done_since), 1)
                progress = min(1.0, round(actual / g.target_value, 3))
                actual_value = actual
                progress_label = f"{actual} / {g.target_value} км"
            elif unit in ("min", "мин"):
                actual = sum(_effective_duration(w) for w in done_since)
                progress = min(1.0, round(actual / g.target_value, 3))
                actual_value = actual
                tv = int(g.target_value)
                progress_label = f"{actual} / {tv} мин"
            elif unit == "runs":
                actual = len(done_since)
                progress = min(1.0, round(actual / g.target_value, 3))
                actual_value = actual
                tv = int(g.target_value)
                progress_label = f"{actual} / {tv} пробежек"
            else:
                actual = round(sum(_effective_distance(w) for w in done_since), 1)
                progress = min(1.0, round(actual / g.target_value, 3))
                actual_value = actual
                progress_label = f"{actual} / {g.target_value}"
        else:
            # Combo 50/50: temporal progress + workout completion rate
            try:
                total_days = max(1, (tgt - goal_created).days)
                elapsed = max(0, (today - goal_created).days)
                temporal_p = min(1.0, elapsed / total_days)
            except Exception:
                temporal_p = 0.0

            all_since = [w for w in all_athlete_workouts
                         if Date.fromisoformat(w.date) >= goal_created]
            done_cnt = len([w for w in all_since if w.status == "done"])
            total_cnt = len(all_since)
            workout_p = done_cnt / total_cnt if total_cnt > 0 else temporal_p
            progress = round((temporal_p + workout_p) / 2, 3)
            progress_label = "авто 50/50"

        active_goals.append({
            "id":            g.id,
            "title":         g.title,
            "targetDate":    g.target_date,
            "type":          g.type,
            "targetValue":   g.target_value,
            "targetUnit":    g.target_unit,
            "daysLeft":      days_left,
            "progress":      progress,
            "actualValue":   actual_value,
            "progressLabel": progress_label,
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
    count: int = 3          # number of variants to generate (1–5)


def _haversine_km(coords: list) -> float:
    """Sum of great-circle distances along a coordinate list [[lon, lat], ...]."""
    import math
    total = 0.0
    for i in range(1, len(coords)):
        lon1, lat1 = coords[i - 1][0], coords[i - 1][1]
        lon2, lat2 = coords[i][0],     coords[i][1]
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat / 2) ** 2
             + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2))
             * math.sin(dlon / 2) ** 2)
        total += 6371.0 * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return total


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
    routes = (db.query(RouteDB)
               .filter(RouteDB.user_id == current_user.id)
               .order_by(RouteDB.created_at.desc())
               .all())
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


def _generate_one_route(lat: float, lon: float, target_km: float,
                         preferences: str, locality_name: str,
                         user_id: str, db) -> "RouteDB":
    """Build and persist a single randomised circular route. Called N times per request."""
    import math, random, httpx

    n_points  = random.randint(3, 5)
    radius_km = target_km / (2 * math.pi)

    # Elliptical distortion: stretch one axis to create variety
    # (x_stretch, y_stretch) sum kept near 2 so total perimeter ≈ target
    x_stretch = random.uniform(0.55, 1.55)
    y_stretch  = random.uniform(0.55, 1.55)

    dlat = radius_km * y_stretch / 111.0
    dlon = radius_km * x_stretch / (111.0 * max(math.cos(math.radians(lat)), 0.01))

    # Non-uniform angular spacing — more organic shape
    raw_angles = sorted(random.uniform(0, 2 * math.pi) for _ in range(n_points))
    # Ensure minimum separation so waypoints aren't too close together
    start_angle = random.uniform(0, 2 * math.pi)

    waypoints: list = [[lon, lat]]
    for i, ang in enumerate(raw_angles):
        perturb = random.uniform(0.55, 1.55)   # wider radius variation
        a = start_angle + ang
        waypoints.append([lon + dlon * perturb * math.cos(a),
                           lat + dlat * perturb * math.sin(a)])
    waypoints.append([lon, lat])

    coords_str    = ";".join(f"{p[0]},{p[1]}" for p in waypoints)
    geojson_coords = waypoints
    actual_dist   = _haversine_km(waypoints)

    try:
        with httpx.Client(timeout=15) as client:
            resp = client.get(
                f"http://router.project-osrm.org/route/v1/foot/{coords_str}"
                f"?overview=full&geometries=geojson&continue_straight=false"
            )
        if resp.status_code == 200:
            routes = resp.json().get("routes", [])
            if routes:
                geojson_coords = routes[0]["geometry"]["coordinates"]
                actual_dist    = routes[0].get("distance", 0) / 1000.0
    except Exception:
        pass

    route_name  = f"{locality_name} · {actual_dist:.1f} км" if locality_name else f"Маршрут {actual_dist:.1f} км"
    description = f"Круговой маршрут {actual_dist:.1f} км"
    if preferences:
        description += f" · {preferences}"

    route = RouteDB(
        id=new_id(), user_id=user_id, name=route_name,
        distance_km=round(actual_dist, 2),
        geojson=json.dumps({"type": "LineString", "coordinates": geojson_coords}),
        description=description, start_lat=lat, start_lon=lon,
        created_at=datetime.utcnow().isoformat(),
    )
    db.add(route); db.commit(); db.refresh(route)
    return route


@app.post("/api/routes/generate")
def generate_route(
    data: RouteGenerateRequest,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Generate N circular running route variants (default 3).
    Returns an array so the client can show all variants for selection.
    """
    import httpx

    lat, lon, target_km = data.start_lat, data.start_lon, data.distance_km
    count = max(1, min(data.count, 5))

    # Reverse-geocode once — reuse locality name for all variants
    locality_name = ""
    try:
        with httpx.Client(timeout=6, headers={"User-Agent": "PeMa/2.0"}) as client:
            nom = client.get(
                f"https://nominatim.openstreetmap.org/reverse"
                f"?lat={lat}&lon={lon}&format=json&zoom=14"
            )
        if nom.status_code == 200:
            addr = nom.json().get("address", {})
            locality_name = (
                addr.get("suburb") or addr.get("neighbourhood") or
                addr.get("city_district") or addr.get("village") or
                addr.get("town") or addr.get("city", "")
            )
    except Exception:
        pass

    results = []
    for _ in range(count):
        route = _generate_one_route(
            lat, lon, target_km, data.preferences, locality_name,
            current_user.id, db
        )
        results.append(_route_to_dict(route))

    return results   # ← array, not a single object


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
    actual_dist = _haversine_km(wps)   # fallback: straight-line distance

    try:
        with httpx.Client(timeout=15) as client:
            resp = client.get(
                f"http://router.project-osrm.org/route/v1/foot/{coords_str}"
                f"?overview=full&geometries=geojson&continue_straight=false"
            )
        if resp.status_code == 200:
            rdata = resp.json().get("routes", [])
            if rdata:
                geojson_coords = rdata[0]["geometry"]["coordinates"]
                actual_dist = rdata[0].get("distance", 0) / 1000.0
    except Exception:
        pass   # keep Haversine fallback

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
    print(f"[Strava] Credentials saved for user {current_user.email}, client_id={data.client_id.strip()}")

@app.get("/api/strava/auth-url")
def strava_auth_url(current_user: UserDB = Depends(get_current_user)):
    cid = current_user.strava_client_id
    print(f"[Strava] auth-url requested, client_id={cid!r}")
    if not cid:
        raise HTTPException(400, "Сначала укажите Strava Client ID в настройках")
    redirect = "http://localhost:8000/api/strava/callback"
    url = (
        f"https://www.strava.com/oauth/authorize"
        f"?client_id={cid}&response_type=code&redirect_uri={redirect}"
        f"&approval_prompt=force&scope=activity:read_all"
    )
    print(f"[Strava] Opening URL: {url}")
    return {"url": url}

@app.get("/api/strava/callback")
def strava_callback(
    code: str,
    db: Session = Depends(get_db),
):
    import httpx, time
    from fastapi.responses import HTMLResponse

    print(f"[Strava] Callback received, code={code[:8]}...")

    # Find user with pending strava credentials (has client_id but no access_token yet)
    user = db.query(UserDB).filter(
        UserDB.strava_client_id.isnot(None),
        UserDB.strava_access_token.is_(None),
    ).order_by(UserDB.created_at.desc()).first()

    print(f"[Strava] Found pending user: {user.email if user else None}")

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
        print(f"[Strava] Token exchange status: {resp.status_code}")
        if resp.status_code != 200:
            print(f"[Strava] Token error: {resp.text}")
            return HTMLResponse(f"<h2>Ошибка Strava: {resp.text[:300]}</h2>")

        tok = resp.json()
        user.strava_access_token  = tok.get("access_token")
        user.strava_refresh_token = tok.get("refresh_token")
        user.strava_token_expiry  = tok.get("expires_at", int(time.time()) + 21600)
        user.strava_athlete_id    = str(tok.get("athlete", {}).get("id", ""))
        db.commit()
        print(f"[Strava] Connected! athlete_id={user.strava_athlete_id}")
    except Exception as e:
        print(f"[Strava] Exception: {e}")
        return HTMLResponse(f"<h2>Ошибка: {e}</h2>")

    return HTMLResponse("""
        <html><body style="font-family:sans-serif;text-align:center;padding:60px">
        <h2>✅ Strava подключена!</h2>
        <p>Вернитесь в приложение PeMa — статус обновится автоматически.</p>
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

        # Determine athlete_id: use own profile or first linked athlete
        target_athlete_id = current_user.athlete_id
        if not target_athlete_id:
            link = db.query(CoachAthleteLinkDB).filter(
                CoachAthleteLinkDB.coach_user_id == current_user.id
            ).first()
            if link:
                target_athlete_id = link.athlete_id

        if not target_athlete_id:
            continue  # no athlete to attach to — skip

        w = WorkoutDB(
            id=new_id(),
            athlete_id=target_athlete_id,
            title=act.get("name") or f"Strava · {cat}",
            category=cat,
            distance_km=dist_km,
            duration_min=dur_min,
            intensity="moderate",
            status="done",
            date=start_date,
            notes="Импортировано из Strava",
            source_file=strava_id,
            actual_distance_km=dist_km,
            actual_duration_min=dur_min,
            actual_avg_pace=avg_pace,
            actual_avg_hr=int(avg_hr) if avg_hr else None,
            actual_max_hr=int(max_hr) if max_hr else None,
            actual_elevation_gain=elev,
            route_geojson=route_geojson,
        )
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


# ─── AI Coach (Google Gemini — free tier) ─────────────────────────────────────

import re as _re

AI_API_KEY = os.getenv("CEREBRAS_API_KEY", "")
AI_BASE    = "https://api.cerebras.ai/v1"
AI_MODEL   = "llama3.1-8b"

def _ai_execute_action(action: dict, athlete_id: str, db: Session) -> str:
    """Execute a structured action from AI JSON response."""
    atype = action.get("type", "")

    if atype == "create":
        w = WorkoutDB(
            id=new_id(),
            athlete_id=athlete_id,
            date=action.get("date", Date.today().strftime("%Y-%m-%d")),
            title=action.get("title", "Тренировка"),
            category=action.get("category", "run"),
            distance_km=float(action.get("distance_km") or 0),
            duration_min=int(action.get("duration_min") or 0),
            intensity=action.get("intensity", "moderate"),
            notes=action.get("notes", ""),
            status="planned",
        )
        db.add(w)
        db.commit()
        return f"Создана: «{w.title}» на {w.date}"

    elif atype == "update":
        wid = action.get("workout_id", "")
        w = db.query(WorkoutDB).filter(
            WorkoutDB.id == wid,
            WorkoutDB.athlete_id == athlete_id,
        ).first()
        if not w:
            return f"Не найдена тренировка {wid}"
        if "title"        in action: w.title       = action["title"]
        if "date"         in action: w.date         = action["date"]
        if "distance_km"  in action: w.distance_km  = float(action["distance_km"])
        if "duration_min" in action: w.duration_min = int(action["duration_min"])
        if "intensity"    in action: w.intensity    = action["intensity"]
        if "notes"        in action: w.notes        = action["notes"]
        db.commit()
        return f"Обновлена: «{w.title}»"

    elif atype == "delete":
        wid = action.get("workout_id", "")
        w = db.query(WorkoutDB).filter(
            WorkoutDB.id == wid,
            WorkoutDB.athlete_id == athlete_id,
        ).first()
        if not w:
            return f"Не найдена тренировка {wid}"
        title = w.title
        db.delete(w)
        db.commit()
        return f"Удалена: «{title}»"

    return f"Неизвестное действие: {atype}"


def _build_ai_context(athlete_id: str, db: Session) -> dict:
    today = Date.today()

    # Recent workouts (last 21 days)
    since = (today - timedelta(days=21)).strftime("%Y-%m-%d")
    recent = db.query(WorkoutDB).filter(
        WorkoutDB.athlete_id == athlete_id,
        WorkoutDB.date >= since,
    ).order_by(WorkoutDB.date.desc()).limit(14).all()

    recent_list = [
        {
            "date":         w.date,
            "category":     w.category,
            "title":        w.title,
            "distance_km":  _effective_distance(w),
            "duration_min": _effective_duration(w),
            "intensity":    w.intensity,
            "status":       w.status,
        }
        for w in recent
    ]

    # Upcoming planned workouts (next 21 days) — with IDs so AI can edit them
    upcoming = db.query(WorkoutDB).filter(
        WorkoutDB.athlete_id == athlete_id,
        WorkoutDB.date >= today.strftime("%Y-%m-%d"),
        WorkoutDB.status == "planned",
    ).order_by(WorkoutDB.date).limit(20).all()

    upcoming_list = [
        {
            "id":           w.id,
            "date":         w.date,
            "title":        w.title,
            "category":     w.category,
            "distance_km":  w.distance_km,
            "duration_min": w.duration_min,
            "intensity":    w.intensity,
        }
        for w in upcoming
    ]

    # Active goals
    goals_list = [
        {
            "title":       g.title,
            "targetDate":  g.target_date,
            "targetValue": g.target_value,
            "targetUnit":  g.target_unit,
        }
        for g in db.query(GoalDB).filter(
            GoalDB.athlete_id == athlete_id,
            GoalDB.completed_at.is_(None),
        ).order_by(GoalDB.target_date).all()
    ]

    # Pain points from recent feedback
    pain_labels = {
        "head": "Голова", "neck": "Шея",
        "lshoulder": "Лев. плечо", "rshoulder": "Прав. плечо",
        "chest": "Грудь/пресс", "lback": "Поясница",
        "lelbow": "Лев. локоть", "relbow": "Прав. локоть",
        "lwrist": "Лев. запястье", "rwrist": "Прав. запястье",
        "lhip": "Лев. бедро", "rhip": "Прав. бедро",
        "lknee": "Лев. колено", "rknee": "Прав. колено",
        "lshin": "Лев. голень", "rshin": "Прав. голень",
        "lankle": "Лев. лодыжка", "rankle": "Прав. лодыжка",
    }
    pain_ids: set[str] = set()
    for w in recent:
        m = _re.search(r"\[PainIds:([^\]]*)\]", w.athlete_feedback or "")
        if m:
            for pid in m.group(1).split(","):
                pid = pid.strip()
                if pid:
                    pain_ids.add(pid)
    pain_human = [pain_labels.get(p, p) for p in pain_ids]

    # 30-day stats
    since30 = (today - timedelta(days=30)).strftime("%Y-%m-%d")
    done30  = db.query(WorkoutDB).filter(
        WorkoutDB.athlete_id == athlete_id,
        WorkoutDB.date >= since30,
        WorkoutDB.status == "done",
    ).all()
    dist30 = round(sum(_effective_distance(w) for w in done30), 1)
    dur30  = sum(_effective_duration(w) for w in done30)

    # Athlete name
    athlete = db.query(AthleteDB).filter(AthleteDB.id == athlete_id).first()

    return {
        "name":              athlete.name if athlete else "Атлет",
        "today":             today.strftime("%Y-%m-%d"),
        "goals":             goals_list,
        "pain_points":       pain_human,
        "recent_workouts":   recent_list,
        "upcoming_workouts": upcoming_list,
        "stats": {
            "workoutsCount": len(done30),
            "distanceTotal": dist30,
            "durationTotal": dur30,
        },
    }


def _build_system_prompt(ctx: dict) -> str:
    goals_str = "\n".join([
        f"  - {g['title']} (до {g['targetDate']}"
        + (f", цель: {g['targetValue']} {g['targetUnit']}" if g.get("targetValue") else "")
        + ")"
        for g in ctx.get("goals", [])
    ]) or "  Цели не заданы"

    injuries_str = ", ".join(ctx.get("pain_points", [])) or "Нет"

    recent_str = "\n".join([
        f"  - {w['date']}: {w['category']} {w['distance_km']} км"
        f" {w['duration_min']} мин [{w['status']}]"
        for w in ctx.get("recent_workouts", [])[:7]
    ]) or "  Нет данных"

    upcoming = ctx.get("upcoming_workouts", [])
    upcoming_str = "\n".join([
        f"  - [id:{w['id']}] {w['date']}: {w['title']} ({w['category']},"
        f" {w['distance_km']} км, {w['duration_min']} мин, {w['intensity']})"
        for w in upcoming
    ]) or "  Запланированных тренировок нет"

    stats = ctx.get("stats", {})
    today = ctx.get("today", "")
    return (
        f"Ты персональный AI тренер в приложении PeMa. Помогаешь атлету планировать тренировки.\n"
        f"Сегодня: {today}\n\n"
        f"ВАЖНО: Отвечай ТОЛЬКО на вопросы о тренировках, спорте, восстановлении и питании.\n"
        f"На другие темы вежливо откажись.\n\n"
        f"Профиль атлета: {ctx.get('name', 'Атлет')}\n"
        f"Активные цели:\n{goals_str}\n"
        f"Болевые точки: {injuries_str}\n"
        f"Последние тренировки:\n{recent_str}\n"
        f"Предстоящие тренировки (используй workout_id для изменений):\n{upcoming_str}\n"
        f"Статистика 30 дней: {stats.get('workoutsCount', 0)} тренировок, "
        f"{stats.get('distanceTotal', 0)} км, {stats.get('durationTotal', 0)} мин.\n\n"
        f"ФОРМАТ ОТВЕТА — строго JSON без markdown:\n"
        f'{{"message": "текст ответа атлету на русском", "actions": []}}\n\n'
        f"Поле actions заполняй ТОЛЬКО когда нужно изменить план:\n"
        f'  Создать: {{"type":"create","date":"YYYY-MM-DD","title":"...","category":"run|bike|swim","distance_km":0,"duration_min":0,"intensity":"easy|moderate|hard","notes":"..."}}\n'
        f'  Изменить: {{"type":"update","workout_id":"...","title":"...","distance_km":0,...}}\n'
        f'  Удалить: {{"type":"delete","workout_id":"..."}}\n'
        f"Иначе actions = []. Не превышай 250 слов в message."
    )


class AiMessage(BaseModel):
    role: str
    content: str

class AiChatRequest(BaseModel):
    athlete_id: str
    messages: list[AiMessage]


@app.get("/api/ai/status")
def ai_status(current_user: UserDB = Depends(get_current_user)):
    return {"available": bool(AI_API_KEY)}


@app.post("/api/ai/chat")
async def ai_chat(
    data: AiChatRequest,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not AI_API_KEY:
        raise HTTPException(503, "CEREBRAS_API_KEY не задан на сервере")

    _assert_athlete_access(current_user, data.athlete_id, db)

    ctx           = _build_ai_context(data.athlete_id, db)
    system_prompt = _build_system_prompt(ctx)

    loop_messages = [{"role": "system", "content": system_prompt}] + [
        {"role": m.role, "content": m.content} for m in data.messages
    ]

    import httpx
    async with httpx.AsyncClient(timeout=45.0) as client:
        resp = await client.post(
            f"{AI_BASE}/chat/completions",
            headers={
                "Authorization": f"Bearer {AI_API_KEY}",
                "Content-Type":  "application/json",
            },
            json={
                "model":           AI_MODEL,
                "messages":        loop_messages,
                "response_format": {"type": "json_object"},
                "max_tokens":      900,
            },
        )

    if resp.status_code != 200:
        err = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else {}
        err_msg = err.get("error", {}).get("message", "") or resp.text[:200]
        print(f"[AI] ERROR {resp.status_code}: {err_msg}")
        # Return friendly Russian error instead of raw JSON
        if resp.status_code == 429:
            friendly = "Слишком много запросов — сервер AI перегружен. Подождите минуту и попробуйте снова."
        elif resp.status_code >= 500:
            friendly = "Сервер AI временно недоступен. Попробуйте через несколько минут."
        elif resp.status_code == 401:
            friendly = "Ошибка авторизации AI. Обратитесь к администратору."
        else:
            friendly = f"Ошибка AI ({resp.status_code}). Попробуйте позже."
        raise HTTPException(502, friendly)

    raw_content = resp.json()["choices"][0]["message"]["content"] or ""

    # Parse structured JSON from AI
    changes_made = False
    message = raw_content  # fallback: show raw if not JSON

    try:
        parsed = json.loads(raw_content)
        message = parsed.get("message", raw_content)
        actions = parsed.get("actions") or []
        for action in actions:
            result = _ai_execute_action(action, data.athlete_id, db)
            print(f"[AI] Action {action.get('type')}: {result}")
            changes_made = True
    except Exception as e:
        print(f"[AI] JSON parse error: {e}, raw: {raw_content[:200]}")
        # AI returned plain text instead of JSON — use it as-is
        message = raw_content

    return {"reply": message, "changes_made": changes_made}

