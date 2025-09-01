import os
import json
import datetime
import logging
import requests
import traceback
from config import telegram_bot_token, telegram_chatid

# -----------------------------
# Logging & Setup
# -----------------------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

DATA_FOLDER = "data"
SCHEDULES_FOLDER = os.path.join(DATA_FOLDER, "schedules")
STANDINGS_FOLDER = os.path.join(DATA_FOLDER, "standings")
TOPSCORERS_FOLDER = os.path.join(STANDINGS_FOLDER, "topscorers")
SEASON_FIXTURES_FOLDER = os.path.join(DATA_FOLDER, "season_fixtures")
LEAGUE_FIXTURES_FOLDER = os.path.join(DATA_FOLDER, "league_fixtures")

for folder in [SCHEDULES_FOLDER, STANDINGS_FOLDER, TOPSCORERS_FOLDER, SEASON_FIXTURES_FOLDER, LEAGUE_FIXTURES_FOLDER]:
    os.makedirs(folder, exist_ok=True)

# -----------------------------
# URLs & Config
# -----------------------------
TEAM_FIXTURE_URLS = {
    "arsenal": "https://fixturedownload.com/feed/json/epl-2025/arsenal",
    "man-city": "https://fixturedownload.com/feed/json/epl-2025/man-city"
}

LEAGUE_FIXTURE_URLS = {
    "premier-league": "https://fixturedownload.com/feed/json/epl-2025"
}

THESPORTSDB_LEAGUE_IDS = {
    "premier-league": 4328
}
CURRENT_SEASON_PARAM = "2025-2026"

# -----------------------------
# Helper Functions
# -----------------------------
def send_telegram_alert(message: str):
    if not telegram_bot_token or not telegram_chatid:
        return
    try:
        url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
        payload = {"chat_id": telegram_chatid, "text": f"⚠️ OpenScoreCollector Error:\n{message}"}
        requests.post(url, json=payload, timeout=10)
    except Exception:
        pass

def save_json(content, path):
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=2)
        logging.info(f"Saved JSON to {path}")
    except Exception:
        logging.error(f"Failed to save JSON to {path}")

def fetch_data_for_date(date_str):
    try:
        url = f"https://prod-public-api.livescore.com/v1/api/app/date/soccer/{date_str}/0"
        res = requests.get(url, timeout=20)
        res.raise_for_status()
        return res.json()
    except requests.RequestException:
        return {}

# -----------------------------
# Scraper Functions
# -----------------------------
def save_team_fixture_data():
    for team_name, url in TEAM_FIXTURE_URLS.items():
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            save_json(response.json(), os.path.join(SEASON_FIXTURES_FOLDER, f"{team_name}.json"))
        except Exception as e:
            logging.error(f"Could not fetch fixture data for {team_name}: {e}")

def save_league_fixture_data():
    for league_name, url in LEAGUE_FIXTURE_URLS.items():
        try:
            response = requests.get(url, timeout=20)
            response.raise_for_status()
            save_json(response.json(), os.path.join(LEAGUE_FIXTURES_FOLDER, f"{league_name}.json"))
        except Exception as e:
            logging.error(f"Could not fetch full fixture data for {league_name}: {e}")

def save_standings_from_thesportsdb():
    for league_name, league_id in THESPORTSDB_LEAGUE_IDS.items():
        try:
            url = f"https://www.thesportsdb.com/api/v1/json/3/lookuptable.php?l={league_id}&s={CURRENT_SEASON_PARAM}"
            response = requests.get(url, timeout=20)
            response.raise_for_status()
            data = response.json()
            standings_data = data.get('table', [])
            reformatted_data = []
            for team in standings_data:
                team_stats = {
                    "rank": team.get('intRank'),
                    "team": {"name": team.get('strTeam')},
                    "games": team.get('intPlayed'),
                    "wins": team.get('intWin'),
                    "draws": team.get('intDraw'),
                    "losses": team.get('intLoss'),
                    "goalsFor": team.get('intGoalsFor'),
                    "goalsAgainst": team.get('intGoalsAgainst'),
                    "goalDifference": team.get('intGoalDifference'),
                    "points": team.get('intPoints')
                }
                reformatted_data.append(team_stats)
            save_json(reformatted_data, os.path.join(STANDINGS_FOLDER, f"{league_name}.json"))
        except Exception as e:
            logging.error(f"Failed to fetch standings for {league_name}: {e}")

# -----------------------------
# Main Update Function
# -----------------------------
def updateToday():
    logging.info("Starting daily update...")
    try:
        save_standings_from_thesportsdb()
        save_team_fixture_data()
        save_league_fixture_data()

        today_utc = datetime.datetime.utcnow().date()
        yesterday_utc = today_utc - datetime.timedelta(days=1)
        today_str = today_utc.strftime("%Y%m%d")
        yesterday_str = yesterday_utc.strftime("%Y%m%d")

        today_data = fetch_data_for_date(today_str)
        yesterday_data = fetch_data_for_date(yesterday_str)

        combined_stages = yesterday_data.get("Stages", []) + today_data.get("Stages", [])

        merged_stages = {}
        for stage in combined_stages:
            stage_id = stage.get("Sid")
            if not stage_id:
                continue
            if stage_id not in merged_stages:
                merged_stages[stage_id] = stage
            else:
                existing_events = {evt.get("Eid") for evt in merged_stages[stage_id].get("Events", [])}
                new_events = [evt for evt in stage.get("Events", []) if evt.get("Eid") not in existing_events]
                merged_stages[stage_id]["Events"].extend(new_events)

        final_data = {"Stages": list(merged_stages.values())}
        save_json(final_data, os.path.join(SCHEDULES_FOLDER, f"{today_str}.json"))

        logging.info("✅ Daily update completed successfully.")
    except Exception:
        err = traceback.format_exc()
        logging.error(f"❌ updateToday failed:\n{err}")
        send_telegram_alert(f"❌ updateToday crashed:\n{err}")
        raise

# -----------------------------
# Run once (for Render Scheduled Job)
# -----------------------------
if __name__ == "__main__":
    updateToday()
