"""Persistent top-five score storage for Traffic Escape."""
import json
import math
from pathlib import Path

# Predictable location: the project root, alongside main.py.
SCORE_FILE = Path(__file__).resolve().parent.parent / "high_scores.json"
MAX_SCORES = 5


def load_scores():
    """Load scores safely; missing, empty, or malformed files mean no saved scores."""
    try:
        if not SCORE_FILE.exists():
            return []
        raw = SCORE_FILE.read_text(encoding="utf-8").strip()
        if not raw:
            return []
        data = json.loads(raw)
        if not isinstance(data, list):
            return []
        scores = []
        for item in data:
            # Accept either simple integer records or {"score": n} records.
            value = item.get("score") if isinstance(item, dict) else item
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                continue
            if value < 0:
                continue
            scores.append(int(value))
        return sorted(scores, reverse=True)[:MAX_SCORES]
    except (OSError, UnicodeError, json.JSONDecodeError, TypeError, ValueError):
        return []


def save_scores(scores):
    """Write only the five highest non-negative scores, safely and consistently."""
    clean = []
    for value in scores:
        if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
            continue
        clean.append(int(value))
    clean = sorted(clean, reverse=True)[:MAX_SCORES]
    try:
        SCORE_FILE.parent.mkdir(parents=True, exist_ok=True)
        temp_file = SCORE_FILE.with_suffix(".json.tmp")
        temp_file.write_text(json.dumps(clean, indent=2) + "\n", encoding="utf-8")
        temp_file.replace(SCORE_FILE)
        return True
    except (OSError, UnicodeError, TypeError, ValueError):
        return False


def record_score(score):
    """Record one finished run, then return the current top five."""
    scores = load_scores()
    if isinstance(score, bool) or not isinstance(score, (int, float)) or score < 0:
        score = 0
    scores.append(int(score))
    scores = sorted(scores, reverse=True)[:MAX_SCORES]
    save_scores(scores)
    return scores
