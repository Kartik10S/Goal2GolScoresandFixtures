import os
import json
import datetime
from fastapi import FastAPI, HTTPException
from urllib.parse import unquote

app = FastAPI(title="Goal2GolScoresandFixtures API")

DATA_FOLDER = "data"
SCHEDULES_FOLDER = os.path.join(DATA_FOLDER, "schedules")
STANDINGS_FOLDER = os.path.join(DATA_FOLDER, "standings")
MATCHES_FOLDER = os.path.join(DATA_FOLDER, "matches")
SEASON_FIXTURES_FOLDER = os.path.join(DATA_FOLDER, "season_fixtures")
LEAGUE_FIXTURES_FOLDER = os.path.join(DATA_FOLDER, "league_fixtures")

# -----------------------------
# Load JSON
# -----------------------------
def load_json_file(path):
    if not os.path.isfile(path):
        return None
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

def get_latest_schedule_file():
    files = sorted(os.listdir(SCHEDULES_FOLDER))
    if not files:
        return None
    return os.path.join(SCHEDULES_FOLDER, files[-1])

# -----------------------------
# API Endpoints
# -----------------------------
@app.get("/")
def get_root():
    return {"message": "Welcome to the Goal2GolScoresandFixtures API!"}

@app.get("/api/scores")
def get_scores():
    path = get_latest_schedule_file()
    data = load_json_file(path)
    if not data:
        raise HTTPException(status_code=503, detail="Daily match data not ready.")
    
    all_matches = []
    for league in data.get("Stages", []):
        league_name = league.get("Snm", "Unknown League")
        league_id = league.get("Cid") or league.get("Sid")
        for evt in league.get("Events", []):
            home_team = evt.get("T1")[0].get("Nm", "N/A") if evt.get("T1") else "N/A"
            away_team = evt.get("T2")[0].get("Nm", "N/A") if evt.get("T2") else "N/A"
            all_matches.append({
                "leagueName": league_name,
                "leagueId": league_id,
                "homeTeamName": home_team,
                "awayTeamName": away_team,
                "matchTime": evt.get("Esd"),
                "matchStatus": evt.get("Eps"),
                "homeScore": evt.get("Tr1"),
                "awayScore": evt.get("Tr2"),
                "matchId": evt.get("Eid")
            })
    
    live_scores = [m for m in all_matches if m["matchStatus"] not in ["NS", "FT", "Sched", "Cancelled", "Postponed", "Awarded"]]
    fixtures = [m for m in all_matches if m["matchStatus"] in ["NS", "Sched"]]
    return {"live": live_scores, "fixtures": fixtures, "all": all_matches}

@app.get("/api/leagues")
def get_leagues():
    path = get_latest_schedule_file()
    data = load_json_file(path)
    if not data:
        raise HTTPException(status_code=503, detail="Daily match data not ready.")

    leagues = []
    seen = set()
    for league in data.get("Stages", []):
        league_name = league.get("Snm", "Unknown League")
        league_id = league.get("Cid") or league.get("Sid")
        if league_id not in seen:
            leagues.append({"leagueName": league_name, "leagueId": league_id})
            seen.add(league_id)
    return leagues

@app.get("/api/fixtures/{league_name}/{team_name}")
def get_team_fixtures(league_name: str, team_name: str):
    path = os.path.join(SEASON_FIXTURES_FOLDER, f"{unquote(team_name).lower()}.json")
    data = load_json_file(path)
    if not data:
        raise HTTPException(status_code=404, detail=f"Season fixtures not found for team '{team_name}'.")
    return data

@app.get("/api/fixtures/{league_name}")
def get_league_fixtures(league_name: str):
    path = os.path.join(LEAGUE_FIXTURES_FOLDER, f"{unquote(league_name).lower().replace(' ', '-')}.json")
    data = load_json_file(path)
    if not data:
        raise HTTPException(status_code=404, detail=f"League fixtures not found for '{league_name}'.")
    return data

@app.get("/api/standings/{league_name}")
def get_standings(league_name: str):
    path = os.path.join(STANDINGS_FOLDER, f"{unquote(league_name).lower().replace(' ', '-')}.json")
    data = load_json_file(path)
    if not data:
        raise HTTPException(status_code=404, detail=f"Standings not found for league '{league_name}'.")
    return data

@app.get("/api/match/{league_name}/{match_id}")
def get_matches(league_name: str):
    path = os.path.join(MATCHES_FOLDER, f"{unquote(league_name).lower().replace(' ', '-')}_match.json")
    data = load_json_file(path)
    if not data:
        raise HTTPException(status_code=404, detail="Matches data not found.")
    return data.get("Players", [])
