import json
import random

SAVE_FILE = "saving_the_browns_save.json"

ATTRIBUTE_KEYS = [
    "Arm Strength",
    "Short Accuracy",
    "Deep Accuracy",
    "Awareness",
    "Composure",
    "Pocket Presence",
    "Mobility",
    "Leadership",
]

PASSING_ATTRS = [
    "Arm Strength",
    "Short Accuracy",
    "Deep Accuracy",
    "Awareness",
    "Composure",
    "Pocket Presence",
]

TRAITS = {
    "Sharp Shooter": {"Short Accuracy": 8},
    "Bomb Maker": {"Deep Accuracy": 8},
    "Lockdown Reader": {"Awareness": 10},
    "Clutch Performer": {"Composure": 10},
    "Leader of Men": {"Leadership": 10},
    "Escape Artist": {"Mobility": 10},
    "Franchise Talent": {
        "Arm Strength": 5,
        "Short Accuracy": 5,
        "Deep Accuracy": 5,
        "Awareness": 5,
        "Composure": 5,
        "Pocket Presence": 5,
    },
}

DIVISION_TEAMS = ["Pittsburgh", "Baltimore", "Cincinnati"]
OTHER_TEAMS = [
    "Kansas City",
    "Buffalo",
    "Miami",
    "New York Jets",
    "New England",
    "Las Vegas",
    "Denver",
    "Los Angeles Chargers",
    "Jacksonville",
    "Tennessee",
    "Indianapolis",
    "Houston",
]

KEY_SITUATIONS = [
    {
        "name": "3rd & 8 from your own 35",
        "options": [
            {
                "text": "Quick slant to slot WR",
                "weights": {"Short Accuracy": 0.45, "Awareness": 0.25, "Confidence": 0.2, "Coach Trust": 0.1},
                "difficulty": 52,
                "success": "first_down",
                "mid": "incomplete",
                "fail": "sack",
            },
            {
                "text": "Take deep shot outside",
                "weights": {"Deep Accuracy": 0.5, "Arm Strength": 0.3, "Confidence": 0.2},
                "difficulty": 60,
                "success": "touchdown",
                "mid": "incomplete",
                "fail": "interception",
            },
            {
                "text": "Scramble and improvise",
                "weights": {"Mobility": 0.45, "Pocket Presence": 0.3, "Composure": 0.25},
                "difficulty": 56,
                "success": "first_down",
                "mid": "short_gain",
                "fail": "sack",
            },
        ],
    },
    {
        "name": "Red Zone: 2nd & Goal from the 9",
        "options": [
            {
                "text": "Play-action cross route",
                "weights": {"Awareness": 0.3, "Short Accuracy": 0.35, "Composure": 0.35},
                "difficulty": 58,
                "success": "touchdown",
                "mid": "field_goal",
                "fail": "interception",
            },
            {
                "text": "Fade route to top WR",
                "weights": {"Deep Accuracy": 0.4, "Arm Strength": 0.35, "Confidence": 0.25},
                "difficulty": 61,
                "success": "touchdown",
                "mid": "incomplete",
                "fail": "turnover_downs",
            },
            {
                "text": "QB draw",
                "weights": {"Mobility": 0.5, "Composure": 0.3, "Leadership": 0.2},
                "difficulty": 55,
                "success": "touchdown",
                "mid": "short_gain",
                "fail": "turnover_downs",
            },
        ],
    },
    {
        "name": "2-minute drill at midfield",
        "options": [
            {
                "text": "No-huddle chain-moving outs",
                "weights": {"Short Accuracy": 0.35, "Awareness": 0.35, "Coach Trust": 0.3},
                "difficulty": 57,
                "success": "first_down",
                "mid": "field_goal",
                "fail": "interception",
            },
            {
                "text": "Attack seams aggressively",
                "weights": {"Deep Accuracy": 0.4, "Composure": 0.35, "Confidence": 0.25},
                "difficulty": 60,
                "success": "touchdown",
                "mid": "first_down",
                "fail": "interception",
            },
            {
                "text": "Checkdown rhythm offense",
                "weights": {"Short Accuracy": 0.4, "Pocket Presence": 0.35, "Awareness": 0.25},
                "difficulty": 53,
                "success": "field_goal",
                "mid": "first_down",
                "fail": "incomplete",
            },
        ],
    },
    {
        "name": "Blitz look on 3rd & long",
        "options": [
            {
                "text": "Audible to max protection",
                "weights": {"Awareness": 0.45, "Leadership": 0.3, "Coach Trust": 0.25},
                "difficulty": 54,
                "success": "first_down",
                "mid": "incomplete",
                "fail": "sack",
            },
            {
                "text": "Hot route instantly",
                "weights": {"Short Accuracy": 0.4, "Composure": 0.35, "Pocket Presence": 0.25},
                "difficulty": 56,
                "success": "first_down",
                "mid": "incomplete",
                "fail": "interception",
            },
            {
                "text": "Hold for deep post",
                "weights": {"Arm Strength": 0.35, "Deep Accuracy": 0.35, "Pocket Presence": 0.3},
                "difficulty": 62,
                "success": "touchdown",
                "mid": "incomplete",
                "fail": "sack",
            },
        ],
    },
]

EVENTS = [
    {
        "title": "Star WR complains about targets on local radio.",
        "choices": [
            {"text": "Publicly support him and promise more looks.", "effects": {"Leadership": 2, "Fan Support": 3, "Confidence": -1}},
            {"text": "Keep it internal and meet privately.", "effects": {"Coach Trust": 3, "Leadership": 1}},
            {"text": "Call him out for selfishness.", "effects": {"Coach Trust": 2, "Fan Support": -4, "Team Morale": -4}},
        ],
    },
    {
        "title": "Offensive coordinator wants extra film sessions.",
        "choices": [
            {"text": "Attend every session.", "effects": {"Awareness": 2, "Coach Trust": 4, "Confidence": 1}},
            {"text": "Attend selected sessions.", "effects": {"Coach Trust": 1, "Confidence": 1}},
            {"text": "Skip and trust your instincts.", "effects": {"Confidence": 2, "Coach Trust": -5}},
        ],
    },
    {
        "title": "Charity event request during a short week.",
        "choices": [
            {"text": "Attend and engage with fans.", "effects": {"Fan Support": 5, "Confidence": 1}},
            {"text": "Send donation instead.", "effects": {"Fan Support": 2}},
            {"text": "Decline and focus on prep.", "effects": {"Coach Trust": 1, "Fan Support": -3}},
        ],
    },
    {
        "title": "Veteran lineman asks you to back contract talks.",
        "choices": [
            {"text": "Back him publicly.", "effects": {"Leadership": 2, "Team Morale": 4, "Coach Trust": -2}},
            {"text": "Stay neutral.", "effects": {"Coach Trust": 1}},
            {"text": "Side with front office.", "effects": {"Coach Trust": 3, "Team Morale": -3}},
        ],
    },
    {
        "title": "You are offered a national TV interview.",
        "choices": [
            {"text": "Take it and hype the team.", "effects": {"Fan Support": 4, "Confidence": 2}},
            {"text": "Keep answers short and safe.", "effects": {"Coach Trust": 1, "Fan Support": 1}},
            {"text": "Decline media requests.", "effects": {"Confidence": -1, "Fan Support": -2}},
        ],
    },
    {
        "title": "Rookie backup asks for extra mentorship.",
        "choices": [
            {"text": "Mentor him daily.", "effects": {"Leadership": 3, "Team Morale": 2}},
            {"text": "Offer occasional tips.", "effects": {"Leadership": 1}},
            {"text": "Tell coaches to handle it.", "effects": {"Coach Trust": 1, "Team Morale": -2}},
        ],
    },
]


def clamp(value, low=0, high=100):
    return max(low, min(high, int(round(value))))


def divider():
    print("---------------------------------")


def get_choice(prompt, minimum, maximum):
    while True:
        value = input(prompt).strip()
        if value.isdigit():
            num = int(value)
            if minimum <= num <= maximum:
                return num
        print(f"Enter a number from {minimum} to {maximum}.")


def calculate_overall(player):
    total = sum(player["attributes"][k] for k in ATTRIBUTE_KEYS)
    return int(round(total / len(ATTRIBUTE_KEYS)))


def base_player():
    return {
        "name": "Rookie QB",
        "age": 22,
        "season": 1,
        "attributes": {
            "Arm Strength": 78,
            "Short Accuracy": 70,
            "Deep Accuracy": 66,
            "Awareness": 64,
            "Composure": 67,
            "Pocket Presence": 65,
            "Mobility": 72,
            "Leadership": 68,
        },
        "dynamic": {"Confidence": 55, "Coach Trust": 45, "Fan Support": 50, "Team Morale": 50},
        "traits": [],
        "career": {
            "pass_yards": 0,
            "pass_td": 0,
            "interceptions": 0,
            "wins": 0,
            "losses": 0,
            "playoff_wins": 0,
            "playoff_losses": 0,
            "seasons_played": 0,
        },
        "team": {"Offensive Line": 66, "WR Group": 69, "Defense": 68, "Coach Rating": 64},
        "rivalry": {
            "ratings": {"Pittsburgh": 85, "Baltimore": 82, "Cincinnati": 75},
            "record": {
                "Pittsburgh": {"wins": 0, "losses": 0},
                "Baltimore": {"wins": 0, "losses": 0},
                "Cincinnati": {"wins": 0, "losses": 0},
            },
        },
        "unlock": {"draft_influence": False, "career_event_this_season": False},
    }


def to_jsonable(state):
    return state


def save_game(state):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(to_jsonable(state), f, indent=2)
    print(f"Game saved to {SAVE_FILE}.")


def load_game():
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("No save file found.")
    except json.JSONDecodeError:
        print("Save file is corrupted.")
    return None


def display_player(state):
    player = state["player"]
    divider()
    print(f"SEASON {player['season']} | AGE {player['age']} | OVR {calculate_overall(player)}")
    print("Attributes:")
    for k in ATTRIBUTE_KEYS:
        print(f"- {k}: {player['attributes'][k]}")
    print("Dynamic:")
    for k, v in player["dynamic"].items():
        print(f"- {k}: {v}")
    print(f"Traits ({len(player['traits'])}/5): {', '.join(player['traits']) if player['traits'] else 'None'}")
    divider()


def apply_trait(state):
    player = state["player"]
    if len(player["traits"]) >= 5:
        print("Trait cap reached (5 active traits).")
        return

    available = [t for t in TRAITS if t not in player["traits"]]
    if not available:
        print("No new traits available.")
        return

    print("Select one trait:")
    for i, trait in enumerate(available, 1):
        print(f"{i}. {trait}")
    choice = get_choice("Choice: ", 1, len(available))
    selected = available[choice - 1]
    player["traits"].append(selected)
    for attr, bonus in TRAITS[selected].items():
        player["attributes"][attr] = clamp(player["attributes"][attr] + bonus, 1, 100)
    print(f"Trait unlocked: {selected}")


def maybe_unlock_draft_influence(state):
    p = state["player"]
    if p["unlock"]["draft_influence"]:
        return
    if calculate_overall(p) > 85 and p["dynamic"]["Coach Trust"] > 75 and p["career"]["playoff_wins"] >= 1:
        p["unlock"]["draft_influence"] = True
        print("Franchise Draft Influence unlocked!")


def offseason_team_progression(state):
    team = state["player"]["team"]
    for key in team:
        team[key] = clamp(team[key] + random.randint(-3, 3), 50, 95)


def draft_influence(state):
    p = state["player"]
    if not p["unlock"]["draft_influence"]:
        return
    divider()
    print("Franchise Draft Influence:")
    print("1. Offensive Line")
    print("2. Wide Receiver")
    print("3. Defensive Star")
    print("4. Best Available Talent")
    c = get_choice("Draft focus: ", 1, 4)
    if c == 1:
        p["team"]["Offensive Line"] = clamp(p["team"]["Offensive Line"] + 8)
    elif c == 2:
        p["team"]["WR Group"] = clamp(p["team"]["WR Group"] + 8)
    elif c == 3:
        p["team"]["Defense"] = clamp(p["team"]["Defense"] + 8)
    else:
        for k in p["team"]:
            p["team"][k] = clamp(p["team"][k] + 4)
    print("Draft strategy applied.")


def pressure_modifier(state, opponent):
    p = state["player"]
    rival = opponent in DIVISION_TEAMS
    mod = 0
    if rival:
        rivalry = p["rivalry"]["ratings"][opponent]
        mod -= rivalry / 25
        mod += p["attributes"]["Composure"] / 100
    mod += (p["team"]["Offensive Line"] - 65) / 8
    mod += (p["team"]["WR Group"] - 65) / 10
    return mod, rival


def option_score(player, weights, opponent, is_rival, quarter4=False):
    score = 0
    for key, weight in weights.items():
        if key in player["attributes"]:
            score += player["attributes"][key] * weight
        elif key in player["dynamic"]:
            score += player["dynamic"][key] * weight
    score += random.randint(-12, 12)
    if is_rival:
        score -= player["rivalry"]["ratings"][opponent] / 20
    if quarter4 and "Clutch Performer" in player["traits"]:
        score += 10
    score += (player["team"]["Offensive Line"] - 65) * 0.3
    score += (player["team"]["WR Group"] - 65) * 0.25
    return score


def apply_play_outcome(state, outcome, is_rival):
    p = state["player"]
    season = state["season_stats"]
    conf_swing = 0
    if outcome == "touchdown":
        season["yards"] += random.randint(18, 45)
        season["td"] += 1
        season["points"] += 7
        conf_swing = 4
        text = "Touchdown!"
    elif outcome == "first_down":
        season["yards"] += random.randint(8, 22)
        season["points"] += random.choice([0, 3])
        conf_swing = 2
        text = "Drive stays alive."
    elif outcome == "field_goal":
        season["yards"] += random.randint(5, 15)
        season["points"] += 3
        conf_swing = 1
        text = "Field goal range secured."
    elif outcome == "sack":
        season["yards"] -= random.randint(4, 10)
        conf_swing = -3
        text = "Sacked."
    elif outcome == "interception":
        season["ints"] += 1
        conf_swing = -6
        text = "Intercepted."
    elif outcome == "turnover_downs":
        conf_swing = -4
        text = "Turnover on downs."
    elif outcome == "short_gain":
        season["yards"] += random.randint(2, 7)
        conf_swing = 0
        text = "Small gain."
    else:
        conf_swing = -1
        text = "Incomplete pass."

    if is_rival:
        conf_swing = int(round(conf_swing * 1.5))
    p["dynamic"]["Confidence"] = clamp(p["dynamic"]["Confidence"] + conf_swing)
    print(text)


def play_game(state, opponent, playoffs=False):
    p = state["player"]
    divider()
    print(f"{'PLAYOFF' if playoffs else 'REGULAR'} GAME: Browns vs {opponent}")
    season = {"yards": 0, "td": 0, "ints": 0, "points": 0}
    state["season_stats"] = season

    pressure, is_rival = pressure_modifier(state, opponent)
    if is_rival:
        print("Rivalry intensity is high.")

    situations = random.choices(KEY_SITUATIONS, k=random.randint(5, 8))
    opp_points = 0

    for i, situation in enumerate(situations, 1):
        print(f"\nMoment {i}: {situation['name']}")
        for idx, option in enumerate(situation["options"], 1):
            print(f"{idx}. {option['text']}")
        choice = get_choice("Decision: ", 1, len(situation["options"]))
        option = situation["options"][choice - 1]

        q4 = i >= len(situations) - 1
        score = option_score(p, option["weights"], opponent, is_rival, quarter4=q4)
        score += pressure

        if score >= option["difficulty"] + 10:
            result = option["success"]
        elif score >= option["difficulty"] - 3:
            result = option["mid"]
        else:
            result = option["fail"]

        apply_play_outcome(state, result, is_rival)
        opp_points += random.randint(0, 7)

    team_factor = (p["team"]["Defense"] + p["team"]["Coach Rating"]) / 2
    opp_points += max(0, int((70 - team_factor) / 8))
    browns_points = season["points"] + random.randint(3, 10)

    win = browns_points >= opp_points
    print(f"Final: Browns {browns_points} - {opponent} {opp_points}")

    p["career"]["pass_yards"] += max(0, season["yards"])
    p["career"]["pass_td"] += season["td"]
    p["career"]["interceptions"] += season["ints"]

    if win:
        if playoffs:
            p["career"]["playoff_wins"] += 1
        else:
            p["career"]["wins"] += 1
        p["dynamic"]["Confidence"] = clamp(p["dynamic"]["Confidence"] + (6 if is_rival else 4))
        p["dynamic"]["Fan Support"] = clamp(p["dynamic"]["Fan Support"] + (5 if is_rival else 3))
        print("Result: WIN")
    else:
        if playoffs:
            p["career"]["playoff_losses"] += 1
        else:
            p["career"]["losses"] += 1
        p["dynamic"]["Confidence"] = clamp(p["dynamic"]["Confidence"] - (6 if is_rival else 4))
        p["dynamic"]["Fan Support"] = clamp(p["dynamic"]["Fan Support"] - (4 if is_rival else 2))
        print("Result: LOSS")

    if is_rival:
        rec = p["rivalry"]["record"][opponent]
        if win:
            rec["wins"] += 1
            p["rivalry"]["ratings"][opponent] = clamp(p["rivalry"]["ratings"][opponent] - 1, 40, 99)
        else:
            rec["losses"] += 1
            p["rivalry"]["ratings"][opponent] = clamp(p["rivalry"]["ratings"][opponent] + 1, 40, 99)


def trigger_offfield_event(state):
    p = state["player"]
    event = random.choice(EVENTS)
    divider()
    print(f"OFF-FIELD: {event['title']}")
    for i, choice in enumerate(event["choices"], 1):
        print(f"{i}. {choice['text']}")
    c = get_choice("Choice: ", 1, len(event["choices"]))
    picked = event["choices"][c - 1]["effects"]

    for key, value in picked.items():
        if key in p["attributes"]:
            p["attributes"][key] = clamp(p["attributes"][key] + value, 1, 100)
        elif key in p["dynamic"]:
            p["dynamic"][key] = clamp(p["dynamic"][key] + value)

    print("Event outcome applied.")


def career_altering_event(state):
    p = state["player"]
    if p["unlock"]["career_event_this_season"]:
        return
    if random.random() > 0.05:
        return

    p["unlock"]["career_event_this_season"] = True
    divider()
    event_type = random.choice(["injury", "extension", "miracle", "takeover"])

    if event_type == "injury":
        print("CAREER EVENT: Major injury scare.")
        p["attributes"]["Mobility"] = clamp(p["attributes"]["Mobility"] - 10, 1, 100)
        p["attributes"]["Composure"] = clamp(p["attributes"]["Composure"] + 4, 1, 100)
        p["dynamic"]["Confidence"] = clamp(p["dynamic"]["Confidence"] - 8)
    elif event_type == "extension":
        print("CAREER EVENT: Franchise extension signed.")
        p["dynamic"]["Coach Trust"] = clamp(p["dynamic"]["Coach Trust"] + 12)
        p["dynamic"]["Fan Support"] = clamp(p["dynamic"]["Fan Support"] + 10)
        p["unlock"]["draft_influence"] = True
    elif event_type == "miracle":
        print("CAREER EVENT: Miracle comeback becomes league legend.")
        p["dynamic"]["Confidence"] = clamp(p["dynamic"]["Confidence"] + 15)
        p["attributes"]["Leadership"] = clamp(p["attributes"]["Leadership"] + 6, 1, 100)
    else:
        print("CAREER EVENT: You take over the locker room.")
        p["attributes"]["Leadership"] = clamp(p["attributes"]["Leadership"] + 8, 1, 100)
        p["dynamic"]["Team Morale"] = clamp(p["dynamic"]["Team Morale"] + 12)
        p["dynamic"]["Coach Trust"] = clamp(p["dynamic"]["Coach Trust"] + 5)


def play_regular_season(state):
    opponents = DIVISION_TEAMS * 2 + random.sample(OTHER_TEAMS, 11)
    random.shuffle(opponents)
    for opponent in opponents:
        play_game(state, opponent)


def playoffs(state):
    p = state["player"]
    wins_this_year = p["career"]["wins"] + p["career"]["losses"]
    if wins_this_year == 0:
        return

    season_wins = state["season_wins"]
    if season_wins < 10:
        print("No playoff berth this season.")
        return

    divider()
    print("PLAYOFFS BEGIN")
    rounds = ["Wild Card", "Divisional", "Conference", "Super Bowl"]
    playoff_opponents = random.sample(OTHER_TEAMS, 3) + ["NFC Champion"]

    for rnd, opponent in zip(rounds, playoff_opponents):
        print(f"\n{rnd} Round")
        pre_w = p["career"]["playoff_wins"]
        play_game(state, opponent, playoffs=True)
        if p["career"]["playoff_wins"] == pre_w:
            print("Eliminated from playoffs.")
            return

    print("You won the Super Bowl!")
    p["dynamic"]["Fan Support"] = clamp(p["dynamic"]["Fan Support"] + 15)
    p["dynamic"]["Coach Trust"] = clamp(p["dynamic"]["Coach Trust"] + 10)


def season_summary(state, start_wins, start_losses):
    p = state["player"]
    divider()
    wins = p["career"]["wins"] - start_wins
    losses = p["career"]["losses"] - start_losses
    state["season_wins"] = wins
    print(f"Season {p['season']} Summary")
    print(f"Record: {wins}-{losses}")
    print(f"Career Record: {p['career']['wins']}-{p['career']['losses']}")
    print(f"Career Passing: {p['career']['pass_yards']} yards | {p['career']['pass_td']} TD | {p['career']['interceptions']} INT")
    print(f"Playoff Record: {p['career']['playoff_wins']}-{p['career']['playoff_losses']}")
    print("Rivalry Records:")
    for team in DIVISION_TEAMS:
        rec = p["rivalry"]["record"][team]
        print(f"- vs {team}: {rec['wins']}-{rec['losses']}")
    print(f"Overall Rating: {calculate_overall(p)}")


def offseason(state):
    p = state["player"]
    p["unlock"]["career_event_this_season"] = False
    divider()
    print(f"OFFSEASON: Year {p['season']}")

    offseason_team_progression(state)
    p["dynamic"]["Confidence"] = clamp(p["dynamic"]["Confidence"] + random.randint(-3, 6))
    p["dynamic"]["Coach Trust"] = clamp(p["dynamic"]["Coach Trust"] + random.randint(-2, 4))
    p["dynamic"]["Fan Support"] = clamp(p["dynamic"]["Fan Support"] + random.randint(-4, 5))
    p["dynamic"]["Team Morale"] = clamp(p["dynamic"]["Team Morale"] + random.randint(-3, 4))

    display_player(state)
    print("1. Continue")
    print("2. Manual Save")
    c = get_choice("Choice: ", 1, 2)
    if c == 2:
        save_game(state)

    apply_trait(state)
    maybe_unlock_draft_influence(state)
    draft_influence(state)


def hall_of_fame_likelihood(player):
    score = 0
    score += player["career"]["pass_td"] * 0.08
    score += player["career"]["pass_yards"] * 0.002
    score += player["career"]["wins"] * 1.8
    score += player["career"]["playoff_wins"] * 4
    score += calculate_overall(player) * 0.6

    if score >= 300:
        return "Lock"
    if score >= 220:
        return "Very High"
    if score >= 160:
        return "Possible"
    return "Unlikely"


def retirement_summary(state):
    p = state["player"]
    divider()
    print("CAREER COMPLETE")
    print(f"Age: {p['age']}")
    print(f"Seasons: {p['career']['seasons_played']}")
    print(f"Career Record: {p['career']['wins']}-{p['career']['losses']}")
    print(f"Passing Yards: {p['career']['pass_yards']}")
    print(f"Passing TD: {p['career']['pass_td']}")
    print(f"INT: {p['career']['interceptions']}")
    print(f"Playoff Record: {p['career']['playoff_wins']}-{p['career']['playoff_losses']}")
    print(f"Hall of Fame Likelihood: {hall_of_fame_likelihood(p)}")
    divider()


def run_career(state):
    while True:
        p = state["player"]
        if p["age"] >= 40:
            print("You reached age 40 and retire.")
            break

        offseason(state)

        start_wins = p["career"]["wins"]
        start_losses = p["career"]["losses"]

        play_regular_season(state)

        for _ in range(random.randint(3, 6)):
            trigger_offfield_event(state)

        career_altering_event(state)
        season_summary(state, start_wins, start_losses)
        playoffs(state)

        p["career"]["seasons_played"] += 1
        p["season"] += 1
        p["age"] += 1

        save_game(state)

        divider()
        print("1. Next Season")
        print("2. Retire")
        print("3. Manual Save")
        next_action = get_choice("Choice: ", 1, 3)
        if next_action == 2:
            break
        if next_action == 3:
            save_game(state)

    retirement_summary(state)


def new_game():
    state = {"player": base_player(), "season_stats": {}, "season_wins": 0}
    run_career(state)


def main_menu():
    while True:
        divider()
        print("SAVING THE BROWNS")
        divider()
        print("1. New Game")
        print("2. Load Game")
        print("3. Exit")
        choice = get_choice("Choice: ", 1, 3)

        if choice == 1:
            new_game()
        elif choice == 2:
            state = load_game()
            if state:
                run_career(state)
        else:
            print("Goodbye.")
            return


if __name__ == "__main__":
    main_menu()
