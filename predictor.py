# predictor.py
import random
from typing import Dict, Any, Tuple

class AIModel:
    """Mock AI model for soccer predictions."""
    def predict_match_outcome(self, game: Dict[str, Any]) -> Tuple[str, float]:
        # Returns one of '1', 'X', '2' and a confidence
        # Mock: randomly choose with weights based on home form
        home_form = sum(game['team_forms']['home']) / (len(game['team_forms']['home']) * 3)  # normalized to [0,1]
        away_form = sum(game['team_forms']['away']) / (len(game['team_forms']['away']) * 3)
        # Home advantage factor
        home_adv = 0.1
        prob_home = (home_form + home_adv) / (home_form + away_form + home_adv)
        prob_draw = 0.2
        prob_away = 1 - prob_home - prob_draw
        # Normalize if needed
        total = prob_home + prob_draw + prob_away
        prob_home /= total
        prob_draw /= total
        prob_away /= total

        # Now choose the outcome with the highest probability
        if prob_home > prob_draw and prob_home > prob_away:
            return '1', prob_home
        elif prob_draw > prob_away:
            return 'X', prob_draw
        else:
            return '2', prob_away

    def predict_btts(self, game: Dict[str, Any]) -> Tuple[str, float]:
        # Returns 'Yes' or 'No' and confidence
        # Mock: based on average goals in h2h and current form
        total_goals = 0
        for match in game['h2h']:
            home_goals, away_goals = match['score'].split('-')
            total_goals += int(home_goals) + int(away_goals)
        avg_goals = total_goals / len(game['h2h']) if game['h2h'] else 2.5
        # If average goals > 2.5, then more likely both to score
        prob_yes = min(0.9, max(0.1, (avg_goals - 1) / 3))
        if random.random() < prob_yes:
            return 'Yes', prob_yes
        else:
            return 'No', 1 - prob_yes

    def predict_correct_score(self, game: Dict[str, Any]) -> Tuple[str, float]:
        # Returns a string like "2-1" and confidence
        # Mock: use form and h2h to generate a score
        home_avg = sum(game['team_forms']['home']) / len(game['team_forms']['home']) / 3 * 2  # scale to about 2 goals max
        away_avg = sum(game['team_forms']['away']) / len(game['team_forms']['away']) / 3 * 2
        home_goals = max(0, min(5, round(home_avg + random.normalvariate(0, 0.5))))
        away_goals = max(0, min(5, round(away_avg + random.normalvariate(0, 0.5))))
        score = f"{int(home_goals)}-{int(away_goals)}"
        # Confidence is arbitrary, we can use the inverse of the variance of the form? But we mock.
        confidence = random.uniform(0.1, 0.3)  # correct score is hard, so low confidence
        return score, confidence

class HollywoodbetsModel(AIModel):
    """Hollywoodbets model (mock) that might have a slight variation."""
    def predict_match_outcome(self, game: Dict[str, Any]) -> Tuple[str, float]:
        # We'll adjust the home advantage to be higher for Hollywoodbets
        # Copy the parent method but adjust the home_adv
        home_form = sum(game['team_forms']['home']) / (len(game['team_forms']['home']) * 3)
        away_form = sum(game['team_forms']['away']) / (len(game['team_forms']['away']) * 3)
        home_adv = 0.15  # slightly higher home advantage
        # ... same as parent but with home_adv=0.15
        prob_home = (home_form + home_adv) / (home_form + away_form + home_adv)
        # ... rest same
        # For brevity, we'll just call parent and then adjust randomly? Or we can override the entire logic differently.
        # Let's just call the parent and then flip a coin to change 10% of the time?
        pred, conf = super().predict_match_outcome(game)
        if random.random() < 0.1:
            # change the prediction to one of the other two
            options = ['1','X','2']
            options.remove(pred)
            pred = random.choice(options)
            conf = conf * 0.8  # reduce confidence
        return pred, conf

class BetwayModel(AIModel):
    """Betway model (mock) that might have a slight variation."""
    def predict_match_outcome(self, game: Dict[str, Any]) -> Tuple[str, float]:
        # We'll adjust the home advantage to be lower for Betway
        home_form = sum(game['team_forms']['home']) / (len(game['team_forms']['home']) * 3)
        away_form = sum(game['team_forms']['away']) / (len(game['team_forms']['away']) * 3)
        home_adv = 0.05  # lower home advantage
        # ... same as parent
        # Similarly, we can do as above but for simplicity we'll use the parent and then adjust 10% of the time
        pred, conf = super().predict_match_outcome(game)
        if random.random() < 0.1:
            options = ['1','X','2']
            options.remove(pred)
            pred = random.choice(options)
            conf = conf * 0.8
        return pred, conf

# We'll create a predictor that uses all three models
def predict_game(game: Dict[str, Any]) -> Dict[str, Any]:
    main_model = AIModel()
    hollywood_model = HollywoodbetsModel()
    betway_model = BetwayModel()

    # Predict match outcome
    main_1x2, main_1x2_conf = main_model.predict_match_outcome(game)
    holly_1x2, holly_1x2_conf = hollywood_model.predict_match_outcome(game)
    betway_1x2, betway_1x2_conf = betway_model.predict_match_outcome(game)

    # Predict BTTS
    main_btts, main_btts_conf = main_model.predict_btts(game)
    # For Hollywoodbets and Betway, we can use the same BTTS model? or have their own?
    # We'll use the same for BTTS for simplicity
    holly_btts, holly_btts_conf = hollywood_model.predict_btts(game)
    betway_btts, betway_btts_conf = betway_model.predict_btts(game)

    # Predict correct score
    main_cs, main_cs_conf = main_model.predict_correct_score(game)
    holly_cs, holly_cs_conf = hollywood_model.predict_correct_score(game)
    betway_cs, betway_cs_conf = betway_model.predict_correct_score(game)

    return {
        'main_model': {
            '1x2': (main_1x2, main_1x2_conf),
            'btts': (main_btts, main_btts_conf),
            'correct_score': (main_cs, main_cs_conf)
        },
        'hollywoodbets': {
            '1x2': (holly_1x2, holly_1x2_conf),
            'btts': (holly_btts, holly_btts_conf),
            'correct_score': (holly_cs, holly_cs_conf)
        },
        'betway': {
            '1x2': (betway_1x2, betway_1x2_conf),
            'btts': (betway_btts, betway_btts_conf),
            'correct_score': (betway_cs, betway_cs_conf)
        }
    }
