ls = []
league = ["league_1","league_2"]
team = [{"test1":["team1","na","na","na"]},{"test2":["team2","na","na"]}]

for i ,j in zip(league,team):
    ls.append({i:j})

sob_match_dict = {"league":{
                    "home": {"0.8":"46816516"},
                    "away": {"0.8":"51351351"},
                    "over": {"0.8":"61351551"},
                    "under": {"0.8":"46546546"}
                           }
                 }