import json
import pandas as pd

rawdata = json.load(open('gid_2015_05_30_tbamlb_balmlb_1.json'))

x=[]
for inning in rawdata['data']['game']['inning']:
    for half in ['top', 'bottom']:
        if half in inning:
            x += inning[half]['atbat']

df = pd.DataFrame(x)
df['count']=1
df2 = df.groupby(['batter','pitcher','event']).agg({'count':sum})
df2 = df2.reset_index()
p = df2.pivot_table(index=['batter','pitcher'], columns='event', values='count')
p["at bats"] = p.sum(axis=1)
hitTypes = list(set.intersection(set(["Single", "Double", "Triple", "Home Run"]), set(p.columns)))
p['hits'] = p[hitTypes].sum(axis=1)

print True