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

print True