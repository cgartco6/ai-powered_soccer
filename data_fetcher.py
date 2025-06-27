# data_fetcher.py
import datetime
from typing import List, Dict, Any

def fetch_todays_games() -> List[Dict[str, Any]]:
    # This function would normally call an API, but we mock 5 games for today.
    today = datetime.date.today()
    games = [
        {
            "home_team": "Team A",
            "away_team": "Team B",
            "date": today,
            # We would have more data in a real scenario
            "team_forms": {
                "home": [3, 3, 1, 0, 3],  # 3: win, 1: draw, 0: loss
                "away": [0, 1, 3, 3, 0]
            },
            "injuries": {
                "home": ["Player X"],
                "away": []
            },
            "transfers": {
                "home": {"in": ["Player Y"], "out": []},
                "away": {"in": [], "out": ["Player Z"]}
            },
            "weather": "Clear",
            "pitch": "Good",
            "referee": "John Smith",
            "h2h": [
                {"date": "2025-01-01", "home_team": "Team A", "away_team": "Team B", "score": "2-1"},
                {"date": "2024-08-15", "home_team": "Team B", "away_team": "Team A", "score": "0-0"}
            ]
        },
        # ... more games (up to 16)
    ]
    # Let's create 5 games for example
    games = games * (5 // len(games))  # if we want 5, but we have 1 example, so we duplicate 5 times
    # We'll create 5 distinct games for the example
    games = [
        {
            "home_team": f"Team {chr(65+i)}",
            "away_team": f"Team {chr(65+i+1)}",
            "date": today,
            "team_forms": {
                "home": [3] * (5-i) + [0]*i,  # varying form
                "away": [1] * 3 + [3] * 2
            },
            "injuries": {
                "home": [f"Player {j}" for j in range(i)],
                "away": []
            },
            "transfers": {
                "home": {"in": [f"New Player {i}"], "out": []},
                "away": {"in": [], "out": [f"Old Player {i}"]}
            },
            "weather": "Clear" if i % 2 == 0 else "Rainy",
            "pitch": "Good" if i % 2 == 0 else "Wet",
            "referee": f"Referee {i}",
            "h2h": [
                {"date": "2025-01-01", "home_team": f"Team {chr(65+i)}", "away_team": f"Team {chr(65+i+1)}", "score": f"{i}-0"},
                {"date": "2024-08-15", "home_team": f"Team {chr(65+i+1)}", "away_team": f"Team {chr(65+i)}", "score": f"1-{i}"}
            ]
        } for i in range(5)
    ]
    return games
