import numpy as np    #using numpy lib
import matplotlib.pyplot as plt    #matplotlib library used
import sqlite3    #importing sqlLite3

fig = plt.figure()
ax = fig.add_subplot(111)

con = sqlite3.connect('player_info.db')
cur = con.cursor()
cur.execute(
        'SELECT * FROM(SELECT user_name,points, RANK() OVER (ORDER BY points DESC) PRANK FROM players) WHERE '
        'PRANK <=3')
## the data
data = []
xTickMarks = []

for row in cur:
   data.append(int(row[1]))
   xTickMarks.append(str(row[0]))
con.commit()
con.close()

## necessary variables
ind = np.arange(len(data))                # the x locations for the groups
width = 0.35                      # the width of the bars

## the bars
rects1 = ax.bar(ind, data, width,
                color='black',
                error_kw=dict(elinewidth=2,ecolor='red'))


# axes and labels
ax.set_xlim(-width,len(ind)+width)
ax.set_ylim(0,45)


ax.set_ylabel('POINTS')
ax.set_xlabel('NAMES')
ax.set_title('TOP RATED PLAYERS (RANK WISE )')

ax.set_xticks(ind+width)
xtickNames = ax.set_xticklabels(xTickMarks)
plt.setp(xtickNames, rotation=45, fontsize=10)


plt.show()
