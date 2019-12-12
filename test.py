import pandas as pd

colum1 = ['1', '', '3', '', '4']
colum2 = ['22', '', '22', '', '66']
colum3 = ['0.8', '0.7', '0.9', '0.3', '1.2']
colum4 = ['1.3', '1.1', '1.5', '1.4', '1.8']

df = pd.DataFrame({'team1': colum1,'team2': colum2,
                   'home_odds': colum3,'away_odds': colum4})
df


team_list = df.values.tolist()
en_ls = list(enumerate(team_list))

dit1 = {}
for e in en_ls:
    d1 = {e[0]: e[1]}
    dit1.update(d1)

print(dit1)


team_list = df.values.tolist()
en_ls = list(enumerate(team_list))

dit1 = {}
for e in en_ls:
    d1 = {e[0]: e[1]}
    dit1.update(d1)
    
new_ls = [i for i in en_ls if i[1][1] == '']

dit2 = {}
for e in new_ls:
    d2 = {e[0]: e[1]}
    dit2.update(d2)

correct_ls = []
for r in dit2:
    val1 = dit2.get(r)[2:]
    val2 = dit1.get(r-1)
    
    new_val = val2 + val1
    correct_ls += [new_val]
    
print(correct_ls) 