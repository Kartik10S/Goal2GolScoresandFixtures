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
# -----------------------------
# URLs & Config
# -----------------------------
TEAM_FIXTURE_URLS = {
    # example teams
    "arsenal": "https://fixturedownload.com/feed/json/epl-2025/arsenal",
    "man-city": "https://fixturedownload.com/feed/json/epl-2025/man-city",
    "man-utd": "https://fixturedownload.com/feed/json/epl-2025/man-utd",
	"bournemouth": "https://fixturedownload.com/feed/json/epl-2025/bournemouth",
	"brentford": "https://fixturedownload.com/feed/json/epl-2025/brentford",
	"brighton": "https://fixturedownload.com/feed/json/epl-2025/brighton",
	"burnley": "https://fixturedownload.com/feed/json/epl-2025/burnley",
	"chelsea": "https://fixturedownload.com/feed/json/epl-2025/chelsea",
	"crystal-palace": "https://fixturedownload.com/feed/json/epl-2025/crystal-palace",
	"everton": "https://fixturedownload.com/feed/json/epl-2025/everton",
	"fulham": "https://fixturedownload.com/feed/json/epl-2025/fulham",
	"leeds": "https://fixturedownload.com/feed/json/epl-2025/leeds",
	"liverpool": "https://fixturedownload.com/feed/json/epl-2025/liverpool",
	"newcastle": "https://fixturedownload.com/feed/json/epl-2025/newcastle",
	"nott'm-forest": "https://fixturedownload.com/feed/json/epl-2025/nott'm-forest",
	"spurs": "https://fixturedownload.com/feed/json/epl-2025/spurs",
	"sunderland": "https://fixturedownload.com/feed/json/epl-2025/sunderland",
	"wolves": "https://fixturedownload.com/feed/json/epl-2025/wolves",
	"west-ham": "https://fixturedownload.com/feed/json/epl-2025/west-ham",
	"austin": "https://fixturedownload.com/feed/json/mls-2025/austin",
	"atlanta": "https://fixturedownload.com/feed/json/mls-2025/atlanta",
	"charlotte": "https://fixturedownload.com/feed/json/mls-2025/charlotte",
	"chicago": "https://fixturedownload.com/feed/json/mls-2025/chicago",
	"cincinnati": "https://fixturedownload.com/feed/json/mls-2025/cincinnati",
	"colorado": "https://fixturedownload.com/feed/json/mls-2025/colorado",
	"columbus": "https://fixturedownload.com/feed/json/mls-2025/columbus",
	"dc": "https://fixturedownload.com/feed/json/mls-2025/dc",
	"dallas": "https://fixturedownload.com/feed/json/mls-2025/dallas",
	"houston": "https://fixturedownload.com/feed/json/mls-2025/houston",
	"kansas-city": "https://fixturedownload.com/feed/json/mls-2025/kansas-city",
	"lafc": "https://fixturedownload.com/feed/json/mls-2025/lafc",
	"la": "https://fixturedownload.com/feed/json/mls-2025/la",
	"miami": "https://fixturedownload.com/feed/json/mls-2025/miami",
	"minnesota": "https://fixturedownload.com/feed/json/mls-2025/minnesota",
	"montréal": "https://fixturedownload.com/feed/json/mls-2025/montréal",
	"nashville": "https://fixturedownload.com/feed/json/mls-2025/nashville",
	"new-england": "https://fixturedownload.com/feed/json/mls-2025/new-england",
	"new-york": "https://fixturedownload.com/feed/json/mls-2025/new-york",
	"new-york-city": "https://fixturedownload.com/feed/json/mls-2025/new-york-city",
	"orlando": "https://fixturedownload.com/feed/json/mls-2025/orlando",
	"philadelphia": "https://fixturedownload.com/feed/json/mls-2025/philadelphia",
	"salt-lake": "https://fixturedownload.com/feed/json/mls-2025/salt-lake",
	"san-diego": "https://fixturedownload.com/feed/json/mls-2025/san-diego",
	"san-jose": "https://fixturedownload.com/feed/json/mls-2025/san-jose",
	"seattle": "https://fixturedownload.com/feed/json/mls-2025/seattle",
	"toronto": "https://fixturedownload.com/feed/json/mls-2025/toronto",
	"st-louis": "https://fixturedownload.com/feed/json/mls-2025/st-louis",
	"vancouver": "https://fixturedownload.com/feed/json/mls-2025/vancouver",
	"atlanta": "https://fixturedownload.com/feed/json/serie-a-2025/atalanta",
	"bologna": "https://fixturedownload.com/feed/json/serie-a-2025/bologna",
	"cagliari": "https://fixturedownload.com/feed/json/serie-a-2025/cagliari",
	"como": "https://fixturedownload.com/feed/json/serie-a-2025/como",
	"cremonese": "https://fixturedownload.com/feed/json/serie-a-2025/cremonese",
	"fiorentina": "https://fixturedownload.com/feed/json/serie-a-2025/fiorentina",
	"genoa": "https://fixturedownload.com/feed/json/serie-a-2025/genoa",
	"hellas-verona": "https://fixturedownload.com/feed/json/serie-a-2025/hellas-verona",
	"inter": "https://fixturedownload.com/feed/json/serie-a-2025/inter",
	"juventus": "https://fixturedownload.com/feed/json/serie-a-2025/juventus",
	"lazio": "https://fixturedownload.com/feed/json/serie-a-2025/lazio",
	"lecce": "https://fixturedownload.com/feed/json/serie-a-2025/lecce",
	"milan": "https://fixturedownload.com/feed/json/serie-a-2025/milan",
	"napoli": "https://fixturedownload.com/feed/json/serie-a-2025/napoli",
	"parma": "https://fixturedownload.com/feed/json/serie-a-2025/parma",
	"pisa": "https://fixturedownload.com/feed/json/serie-a-2025/pisa",
	"roma": "https://fixturedownload.com/feed/json/serie-a-2025/roma",
	"sassuolo": "https://fixturedownload.com/feed/json/serie-a-2025/sassuolo",
	"torino": "https://fixturedownload.com/feed/json/serie-a-2025/torino",
	"udinese": "https://fixturedownload.com/feed/json/serie-a-2025/udinese",
	"fc-heidenheim": "https://fixturedownload.com/feed/json/bundesliga-2025/1-fc-heidenheim-1846",
	"fc-koln": "https://fixturedownload.com/feed/json/bundesliga-2025/1-fc-k%C3%B6ln",
	"union-berlin": "https://fixturedownload.com/feed/json/bundesliga-2025/1-fc-union-berlin",
	"leverkusen": "https://fixturedownload.com/feed/json/bundesliga-2025/bayer-04-leverkusen",
	"dortmund": "https://fixturedownload.com/feed/json/bundesliga-2025/borussia-dortmund",
	"mönchengladbach": "https://fixturedownload.com/feed/json/bundesliga-2025/borussia-m%C3%B6nchengladbach",
	"frankfurt": "https://fixturedownload.com/feed/json/bundesliga-2025/eintracht-frankfurt",
	"augsburg": "https://fixturedownload.com/feed/json/bundesliga-2025/fc-augsburg",
	"bayern": "https://fixturedownload.com/feed/json/bundesliga-2025/fc-bayern-m%C3%BCnchen",
	"hamburger-sv": "https://fixturedownload.com/feed/json/bundesliga-2025/hamburger-sv",
	"leipzig": "https://fixturedownload.com/feed/json/bundesliga-2025/rb-leipzig",
	"freiburg": "https://fixturedownload.com/feed/json/bundesliga-2025/sport-club-freiburg",
	"werder-bremen": "https://fixturedownload.com/feed/json/bundesliga-2025/sv-werder-bremen",
	"hoffenheim": "https://fixturedownload.com/feed/json/bundesliga-2025/tsg-hoffenheim",
	"stuttgart": "https://fixturedownload.com/feed/json/bundesliga-2025/vfb-stuttgart",
	"wolfsburg": "https://fixturedownload.com/feed/json/bundesliga-2025/vfl-wolfsburg",
	"auxerre": "https://fixturedownload.com/feed/json/ligue-1-2025/aj-auxerre",
	"angers-sco": "https://fixturedownload.com/feed/json/ligue-1-2025/angers-sco",
	"monaco": "https://fixturedownload.com/feed/json/ligue-1-2025/as-monaco",
	"lorient": "https://fixturedownload.com/feed/json/ligue-1-2025/fc-lorient",
	"nantes": "https://fixturedownload.com/feed/json/ligue-1-2025/fc-nantes",
	"havre-athletic-club": "https://fixturedownload.com/feed/json/ligue-1-2025/havre-athletic-club",
	"losc-lille": "https://fixturedownload.com/feed/json/ligue-1-2025/losc-lille",
	"nice": "https://fixturedownload.com/feed/json/ligue-1-2025/ogc-nice",
	"marseille": "https://fixturedownload.com/feed/json/ligue-1-2025/olympique-de-marseille",
	"lyon": "https://fixturedownload.com/feed/json/ligue-1-2025/olympique-lyonnais",
	"paris-fc": "https://fixturedownload.com/feed/json/ligue-1-2025/paris-fc",
	"paris-saint-germain": "https://fixturedownload.com/feed/json/ligue-1-2025/paris-saint-germain",
	"lens": "https://fixturedownload.com/feed/json/ligue-1-2025/rc-lens",
	"strasbourg": "https://fixturedownload.com/feed/json/ligue-1-2025/rc-strasbourg-alsace",
	"brest": "https://fixturedownload.com/feed/json/ligue-1-2025/stade-brestois-29",
	"rennais": "https://fixturedownload.com/feed/json/ligue-1-2025/stade-rennais-fc",
	"toulouse": "https://fixturedownload.com/feed/json/ligue-1-2025/toulouse-fc",
	"atheletic-bilbao": "https://fixturedownload.com/feed/json/la-liga-2025/athletic-club",
	"atletico-de-madrid": "https://fixturedownload.com/feed/json/la-liga-2025/atl%C3%A9tico-de-madrid",
	"atheletic-bilbao": "https://fixturedownload.com/feed/json/la-liga-2025/ca-osasuna",
	"osasuna": "https://fixturedownload.com/feed/json/la-liga-2025/athletic-club",
	"celta": "https://fixturedownload.com/feed/json/la-liga-2025/celta",
	"deportivo-alavés": "https://fixturedownload.com/feed/json/la-liga-2025/deportivo-alav%C3%A9s",
	"elche": "https://fixturedownload.com/feed/json/la-liga-2025/elche-cf",
	"barcelona": "https://fixturedownload.com/feed/json/la-liga-2025/fc-barcelona",
	"getafe": "https://fixturedownload.com/feed/json/la-liga-2025/getafe-cf",
	"girona": "https://fixturedownload.com/feed/json/la-liga-2025/girona-fc",
	"levante": "https://fixturedownload.com/feed/json/la-liga-2025/levante-ud",
	"rayo-vallecano": "https://fixturedownload.com/feed/json/la-liga-2025/rayo-vallecano",
	"espanyol": "https://fixturedownload.com/feed/json/la-liga-2025/rcd-espanyol-de-barcelona",
	"mallorca": "https://fixturedownload.com/feed/json/la-liga-2025/rcd-mallorca",
	"real-betis": "https://fixturedownload.com/feed/json/la-liga-2025/real-betis",
	"real-madrid": "https://fixturedownload.com/feed/json/la-liga-2025/real-madrid",
	"real-oviedo": "https://fixturedownload.com/feed/json/la-liga-2025/real-oviedo",
	"sociedad": "https://fixturedownload.com/feed/json/la-liga-2025/real-sociedad",
	"sevilla": "https://fixturedownload.com/feed/json/la-liga-2025/sevilla-fc",
	"valencia": "https://fixturedownload.com/feed/json/la-liga-2025/valencia-cf",
	"villarreal": "https://fixturedownload.com/feed/json/la-liga-2025/villarreal-cf",
	"alanyaspor": "https://fixturedownload.com/feed/json/super-lig-2025/alanyaspor",
	"antalyaspor": "https://fixturedownload.com/feed/json/super-lig-2025/antalyaspor",
	"besiktas": "https://fixturedownload.com/feed/json/super-lig-2025/besiktas",
	"caykur-rizespor": "https://fixturedownload.com/feed/json/super-lig-2025/%C3%A7aykur-rizespor",
	"eyupspor": "https://fixturedownload.com/feed/json/super-lig-2025/ey%C3%BCpspor",
	"fatih-karagumruk": "https://fixturedownload.com/feed/json/super-lig-2025/fatih-karag%C3%BCmr%C3%BCk",
	"galatasaray": "https://fixturedownload.com/feed/json/super-lig-2025/galatasaray",
	"gaziantep": "https://fixturedownload.com/feed/json/super-lig-2025/gaziantep",
	"genclerbirligi": "https://fixturedownload.com/feed/json/super-lig-2025/gen%C3%A7lerbirligi",
	"goztepe": "https://fixturedownload.com/feed/json/super-lig-2025/g%C3%B6ztepe",
	"istanbul-basaksehir": "https://fixturedownload.com/feed/json/super-lig-2025/istanbul-basaksehir",
	"kasimpasa": "https://fixturedownload.com/feed/json/super-lig-2025/kasimpasa",
	"kayserispor": "https://fixturedownload.com/feed/json/super-lig-2025/kayserispor",
	"kocaelispor": "https://fixturedownload.com/feed/json/super-lig-2025/kocaelispor",
	"samsunspor": "https://fixturedownload.com/feed/json/super-lig-2025/samsunspor",
	"trabzonspor": "https://fixturedownload.com/feed/json/super-lig-2025/trabzonspor",
	"afs": "https://fixturedownload.com/feed/json/primeira-liga-2025/afs",
	"casa-pia-ac": "https://fixturedownload.com/feed/json/primeira-liga-2025/casa-pia-ac",
	"cd-nacional": "https://fixturedownload.com/feed/json/primeira-liga-2025/cd-nacional",
	"tondela": "https://fixturedownload.com/feed/json/primeira-liga-2025/cd-tondela",
	"estoril-praia": "https://fixturedownload.com/feed/json/primeira-liga-2025/estoril-praia",
	"estrela-amadora": "https://fixturedownload.com/feed/json/primeira-liga-2025/estrela-amadora",
	"fc-alverca": "https://fixturedownload.com/feed/json/primeira-liga-2025/fc-alverca",
	"fc-arouca": "https://fixturedownload.com/feed/json/primeira-liga-2025/fc-arouca",
	"famalicao": "https://fixturedownload.com/feed/json/primeira-liga-2025/fc-famalic%C3%A3o",
	"porto": "https://fixturedownload.com/feed/json/primeira-liga-2025/fc-porto",
	"gil-vicente-fc": "https://fixturedownload.com/feed/json/primeira-liga-2025/gil-vicente-fc",
	"moreirense-fc": "https://fixturedownload.com/feed/json/primeira-liga-2025/moreirense-fc",
	"rio-ave-fc": "https://fixturedownload.com/feed/json/primeira-liga-2025/rio-ave-fc",
	"santa-clara": "https://fixturedownload.com/feed/json/primeira-liga-2025/santa-clara",
	"fc-braga": "https://fixturedownload.com/feed/json/primeira-liga-2025/sc-braga",
	"sl-benfica": "https://fixturedownload.com/feed/json/primeira-liga-2025/sl-benfica",
	"sporting-cp": "https://fixturedownload.com/feed/json/primeira-liga-2025/sporting-cp",
	"vitoria-sc": "https://fixturedownload.com/feed/json/primeira-liga-2025/vit%C3%B3ria-sc",
	"ajax": "https://fixturedownload.com/feed/json/eredivisie-2025/ajax",
	"az": "https://fixturedownload.com/feed/json/eredivisie-2025/az",
	"rotterdam": "https://fixturedownload.com/feed/json/eredivisie-2025/excelsior-rotterdam",
	"groningen": "https://fixturedownload.com/feed/json/eredivisie-2025/fc-groningen",
	"twente": "https://fixturedownload.com/feed/json/eredivisie-2025/fc-twente",
	"utrecht": "https://fixturedownload.com/feed/json/eredivisie-2025/fc-utrecht",
	"volendam": "https://fixturedownload.com/feed/json/eredivisie-2025/fc-volendam",
	"feyenoord": "https://fixturedownload.com/feed/json/eredivisie-2025/feyenoord",
	"fortuna-sittard": "https://fixturedownload.com/feed/json/eredivisie-2025/fortuna-sittard",
	"eagles": "https://fixturedownload.com/feed/json/eredivisie-2025/go-ahead-eagles",
	"heracles-almelo": "https://fixturedownload.com/feed/json/eredivisie-2025/heracles-almelo",
	"nec-nijmegen": "https://fixturedownload.com/feed/json/eredivisie-2025/nec-nijmegen",
	"breda": "https://fixturedownload.com/feed/json/eredivisie-2025/nac-breda",
	"zwolle": "https://fixturedownload.com/feed/json/eredivisie-2025/pec-zwolle",
	"psv": "https://fixturedownload.com/feed/json/eredivisie-2025/psv",
	"heerenveen": "https://fixturedownload.com/feed/json/eredivisie-2025/sc-heerenveen",
	"sparta-rotterdam": "https://fixturedownload.com/feed/json/eredivisie-2025/sparta-rotterdam",
	"telstar": "https://fixturedownload.com/feed/json/eredivisie-2025/telstar",
	"cl-ajax": "https://fixturedownload.com/feed/json/champions-league-2025/ajax",
	"cl-arsenal": "https://fixturedownload.com/feed/json/champions-league-2025/arsenal",
	"cl-atlanta": "https://fixturedownload.com/feed/json/champions-league-2025/atalanta",
	"cl-athletic-club": "https://fixturedownload.com/feed/json/champions-league-2025/athletic-club",
	"cl-atleti": "https://fixturedownload.com/feed/json/champions-league-2025/atleti",
	"cl-dortmund": "https://fixturedownload.com/feed/json/champions-league-2025/b-dortmund",
	"cl-barcelona": "https://fixturedownload.com/feed/json/champions-league-2025/barcelona",
	"cl-bayern": "https://fixturedownload.com/feed/json/champions-league-2025/bayern-m%C3%BCnchen",
	"cl-benfica": "https://fixturedownload.com/feed/json/champions-league-2025/benfica",
	"cl-bodo-glimt": "https://fixturedownload.com/feed/json/champions-league-2025/bod%C3%B8-glimt",
	"cl-chelsea": "https://fixturedownload.com/feed/json/champions-league-2025/chelsea",
	"cl-club-brugge": "https://fixturedownload.com/feed/json/champions-league-2025/club-brugge",
	"cl-copenhagen": "https://fixturedownload.com/feed/json/champions-league-2025/copenhagen",
	"cl-frankfurt": "https://fixturedownload.com/feed/json/champions-league-2025/frankfurt",
	"cl-galatasaray": "https://fixturedownload.com/feed/json/champions-league-2025/galatasaray",
	"cl-inter": "https://fixturedownload.com/feed/json/champions-league-2025/inter",
	"cl-juventus": "https://fixturedownload.com/feed/json/champions-league-2025/juventus",
	"cl-kairat-almaty": "https://fixturedownload.com/feed/json/champions-league-2025/kairat-almaty",
	"cl-leverkusen": "https://fixturedownload.com/feed/json/champions-league-2025/leverkusen",
	"cl-liverpool": "https://fixturedownload.com/feed/json/champions-league-2025/liverpool",
	"cl-man-city": "https://fixturedownload.com/feed/json/champions-league-2025/man-city",
	"cl-marseille": "https://fixturedownload.com/feed/json/champions-league-2025/marseille",
	"cl-monaco": "https://fixturedownload.com/feed/json/champions-league-2025/monaco",
	"cl-napoli": "https://fixturedownload.com/feed/json/champions-league-2025/napoli",
	"cl-newcastle": "https://fixturedownload.com/feed/json/champions-league-2025/newcastle",
	"cl-olympiacos": "https://fixturedownload.com/feed/json/champions-league-2025/olympiacos",
	"cl-pafos": "https://fixturedownload.com/feed/json/champions-league-2025/pafos",
	"cl-paris-saint-germain": "https://fixturedownload.com/feed/json/champions-league-2025/paris",
	"cl-psv": "https://fixturedownload.com/feed/json/champions-league-2025/psv",
	"cl-qarabag": "https://fixturedownload.com/feed/json/champions-league-2025/qarabag",
	"cl-real-madrid": "https://fixturedownload.com/feed/json/champions-league-2025/real-madrid",
	"cl-slavia-praha": "https://fixturedownload.com/feed/json/champions-league-2025/slavia-praha",
	"cl-sporting-cp": "https://fixturedownload.com/feed/json/champions-league-2025/sporting-cp",
	"cl-spurs": "https://fixturedownload.com/feed/json/champions-league-2025/tottenham",
	"cl-villarreal": "https://fixturedownload.com/feed/json/champions-league-2025/villarreal",
	"birmingham-city": "https://fixturedownload.com/feed/json/championship-2025/birmingham-city",
	"blackburn-rovers": "https://fixturedownload.com/feed/json/championship-2025/blackburn-rovers",
	"bristol-city": "https://fixturedownload.com/feed/json/championship-2025/bristol-city",
	"charlton-athletic": "https://fixturedownload.com/feed/json/championship-2025/charlton-athletic",
	"conventry": "https://fixturedownload.com/feed/json/championship-2025/coventry-city",
	"derby-county": "https://fixturedownload.com/feed/json/championship-2025/derby-county",
	"hull-city": "https://fixturedownload.com/feed/json/championship-2025/hull-city",
	"ipswich": "https://fixturedownload.com/feed/json/championship-2025/ipswich-town",
	"leicester-city": "https://fixturedownload.com/feed/json/championship-2025/leicester-city",
	"middlesbrough": "https://fixturedownload.com/feed/json/championship-2025/middlesbrough",
	"millwall": "https://fixturedownload.com/feed/json/championship-2025/millwall",
	"norwich-city": "https://fixturedownload.com/feed/json/championship-2025/norwich-city",
	"oxford-united": "https://fixturedownload.com/feed/json/championship-2025/oxford-united",
	"preston-north-end": "https://fixturedownload.com/feed/json/championship-2025/preston-north-end",
	"queens-park-rangers": "https://fixturedownload.com/feed/json/championship-2025/queens-park-rangers",
	"sheffield-united": "https://fixturedownload.com/feed/json/championship-2025/sheffield-united",
	"sheffield-wednesday": "https://fixturedownload.com/feed/json/championship-2025/sheffield-wednesday",
	"southampton": "https://fixturedownload.com/feed/json/championship-2025/southampton",
	"stoke-city": "https://fixturedownload.com/feed/json/championship-2025/stoke-city",
	"swansea-city": "https://fixturedownload.com/feed/json/championship-2025/swansea-city",
	"watford": "https://fixturedownload.com/feed/json/championship-2025/watford",
	"west-bromwich-albion": "https://fixturedownload.com/feed/json/championship-2025/west-bromwich-albion",
	"wrexham": "https://fixturedownload.com/feed/json/championship-2025/wrexham",
	"el-aston-villa": "https://fixturedownload.com/feed/json/europa-league-2025/aston-villa",
	"el-basel": "https://fixturedownload.com/feed/json/europa-league-2025/basel",
	"el-bologna": "https://fixturedownload.com/feed/json/europa-league-2025/bologna",
	"el-braga": "https://fixturedownload.com/feed/json/europa-league-2025/braga",
	"el-brann": "https://fixturedownload.com/feed/json/europa-league-2025/brann",
	"el-celta": "https://fixturedownload.com/feed/json/europa-league-2025/celta",
	"el-celtic": "https://fixturedownload.com/feed/json/europa-league-2025/celtic",
	"el-crvena-zvezda": "https://fixturedownload.com/feed/json/europa-league-2025/crvena-zvezda",
	"el-fcsb": "https://fixturedownload.com/feed/json/europa-league-2025/fcsb",
	"el-fenerbahce": "https://fixturedownload.com/feed/json/europa-league-2025/fenerbah%C3%A7e",
	"el-ferencvaros": "https://fixturedownload.com/feed/json/europa-league-2025/ferencv%C3%A1ros",
	"el-freiburg": "https://fixturedownload.com/feed/json/europa-league-2025/freiburg",
	"el-genk": "https://fixturedownload.com/feed/json/europa-league-2025/genk",
	"el-dinamo": "https://fixturedownload.com/feed/json/europa-league-2025/gnk-dinamo",
	"el-eagles": "https://fixturedownload.com/feed/json/europa-league-2025/go-ahead-eagles",
	"el-lille": "https://fixturedownload.com/feed/json/europa-league-2025/lille",
	"el-ludogorets": "https://fixturedownload.com/feed/json/europa-league-2025/ludogorets",
	"el-lyon": "https://fixturedownload.com/feed/json/europa-league-2025/lyon",
	"el-m-tel-aviv": "https://fixturedownload.com/feed/json/europa-league-2025/m-tel-aviv",
	"el-malmo": "https://fixturedownload.com/feed/json/europa-league-2025/malm%C3%B6",
	"el-midtyjylland": "https://fixturedownload.com/feed/json/europa-league-2025/midtjylland",
	"el-nice": "https://fixturedownload.com/feed/json/europa-league-2025/nice",
	"el-nott'm-forest": "https://fixturedownload.com/feed/json/europa-league-2025/nott'm-forest",
	"el-panathinaikos": "https://fixturedownload.com/feed/json/europa-league-2025/panathinaikos",
	"el-paok": "https://fixturedownload.com/feed/json/europa-league-2025/paok",
	"el-rangers": "https://fixturedownload.com/feed/json/europa-league-2025/rangers",
	"el-real-betis": "https://fixturedownload.com/feed/json/europa-league-2025/real-betis",
	"el-roma": "https://fixturedownload.com/feed/json/europa-league-2025/roma",
	"el-salzburg": "https://fixturedownload.com/feed/json/europa-league-2025/salzburg",
	"el-sturm-graz": "https://fixturedownload.com/feed/json/europa-league-2025/sturm-graz",
	"el-stuttgart": "https://fixturedownload.com/feed/json/europa-league-2025/stuttgart",
	"el-utrecht": "https://fixturedownload.com/feed/json/europa-league-2025/utrecht",
	"el-viktoria-plzen": "https://fixturedownload.com/feed/json/europa-league-2025/viktoria-plzen",
	"el-young-boys": "https://fixturedownload.com/feed/json/europa-league-2025/young-boys"
}

LEAGUE_FIXTURE_URLS = {
    "premier-league": "https://fixturedownload.com/feed/json/epl-2025",
    "serie-a": "https://fixturedownload.com/feed/json/serie-a-2025",
	"efl-championship": "https://fixturedownload.com/feed/json/championship-2025",
	"uefa-champions-league": "https://fixturedownload.com/feed/json/champions-league-2025",
	"eredivisie": "https://fixturedownload.com/feed/json/eredivisie-2025",
	"por-primeira-liga": "https://fixturedownload.com/feed/json/primeira-liga-2025",
	"tur-super-lig": "https://fixturedownload.com/feed/json/super-lig-2025",
	"ita-league-1": "https://fixturedownload.com/feed/json/ligue-1-2025",
	"bundesliga": "https://fixturedownload.com/feed/json/bundesliga-2025",
	"mls": "https://fixturedownload.com/feed/json/mls-2025",
	"la-liga": "https://fixturedownload.com/feed/json/la-liga-2025",
	"europa-league": "https://fixturedownload.com/feed/json/la-liga-2025"	
	}

THESPORTSDB_LEAGUE_IDS = {
    "premier-league": 4328,
    "serie-a": 4332,
    "efl-championship": 4329,
    "uefa-champions-league": 4480,
    "eredivisie": 4337,
    "por-primeira-liga": 4344,
    "tur-super-lig": 4358,
    "ligue-1": 4334,  # Assuming "ita-league-1" was a typo for France's Ligue 1
    "bundesliga": 4331,
    "mls": 4346,
    "la-liga": 4335,
    "europa-league": 4481
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
            url = f"https://int.soccerway.com/national/france/ligue-1/2025-2026/regular-season/2d58bc25-77ec-4425-bed7-30f1839e3f8f/"
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
