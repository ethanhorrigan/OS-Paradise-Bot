participants = 10
playtime = 2

# osrs_bosses = [
#     {
#         "name": "Phantom Muspah",
#         "type": "Boss"
#     },
#     {
#         "name": "Zulrah",
#         "type": "Boss"
#     },
#     {
#         "name": "Vorkath",
#         "type": "Boss"
#     },
#     {
#         "name": "Grotesque Guardians",
#         "type": "Boss"
#     },
#     {
#         "name": "Alchemical Hydra",
#         "type": "Boss"
#     },
#     {
#         "name": "Cerberus",
#         "type": "Boss"
#     },
#     {
#         "name": "Barrows",
#         "type": "Minigame"
#     },
#     {
#         "name": "Sarachnis",
#         "type": "Minigame"
#     },
#     {
#         "name": "Callisto",
#         "type": "Boss"
#     },
#     {
#         "name": "Vetion",
#         "type": "Boss"
#     },
#     {
#         "name": "Venenatis",
#         "type": "Boss"
#     },
#     {
#         "name": "Corrupted Gauntlet",
#         "type": "Boss"
#     },
#     {
#         "name": "Corporeal Beast",
#         "type": "Boss"
#     },
#     {
#         "name": "General Graardor",
#         "type": "Boss"
#     },
#     {
#         "name": "Kree'arra",
#         "type": "Boss"
#     },
#     {
#         "name": "K'ril Tsutsaroth",
#         "type": "Boss"
#     },
#     {
#         "name": "Commander Zilyana",
#         "type": "Boss"
#     },
#     {
#         "name": "Nightmare",
#         "type": "Boss"
#     },
#     {
#         "name": "Nex",
#         "type": "Boss"
#     },
#     {
#         "name": "Kalphite Queen",
#         "type": "Boss"
#     },
#     {
#         "name": "King Black Dragon",
#         "type": "Boss"
#     },
#     {
#         "name": "Chambers of Xeric",
#         "type": "Raid"
#     },
#     {
#         "name": "Theatre of Blood",
#         "type": "Raid"
#     },
#     {
#         "name": "Tombs of Amascut",
#         "type": "Raid"
#     }
# ]

osrs_bosses = [
    {"name": "Phantom Muspah", "type": "Boss", "kph": 25},
    {"name": "Zulrah", "type": "Boss", "kph": 25},
    {"name": "Vorkath", "type": "Boss", "kph": 25},
    {"name": "Grotesque Guardians", "type": "Boss", "kph": 20},
    {"name": "Alchemical Hydra", "type": "Boss", "kph": 25},
    {"name": "Cerberus", "type": "Boss", "kph": 30},
    {"name": "Barrows", "type": "Minigame"},
    {"name": "Sarachnis", "type": "Minigame", "kph": 25},
    {"name": "Callisto", "type": "Boss", "kph": 25},
    {"name": "Vetion", "type": "Boss", "kph": 25},
    {"name": "Venenatis", "type": "Boss", "kph": 25},
    {"name": "Corrupted Gauntlet", "type": "Boss", "kph": 5},
    {"name": "General Graardor", "type": "Boss", "kph": 25},
    {"name": "Kree'arra", "type": "Boss", "kph": 25},
    {"name": "K'ril Tsutsaroth", "type": "Boss", "kph": 25},
    {"name": "Commander Zilyana", "type": "Boss", "kph": 25},
    {"name": "Nightmare", "type": "Boss", "kph": 12},
    {"name": "Nex", "type": "Boss", "kph": 12},
    {"name": "Kalphite Queen", "type": "Boss", "kph": 20},
    {"name": "King Black Dragon", "type": "Boss", "kph": 30},
    {"name": "Chambers of Xeric", "type": "Raid", "kph": 3},
    {"name": "Theatre of Blood", "type": "Raid", "kph": 3},
    {"name": "Tombs of Amascut", "type": "Raid", "kph": 3}
]
def get_total_kc(avg_kph):
    total_kc = (2 * avg_kph) * participants
    return total_kc

# loop through osrs bosses and print them out
for boss in osrs_bosses:
    if "kph" in boss:
        boss_name = boss["name"]
        boss_kph = boss.get("kph", "Unknown")
        total_kills = get_total_kc(boss_kph)
        print(f'{boss_name} KPH: {boss_kph} Total To Kill: {total_kills}\n')

