import pandas as pd
import matplotlib.pyplot as plt

# DATA:
#   Steph Curry
#   Field Goal Shots (2s and 3s)
#   Season 2014 - 2015
#   Only Regular Games

# GOALS:
#   Attempts Based On Distance
#   Accuracy Based On Distance
#   Accuracy Based On Period
#   Average Points Based On Period From FGs
#   Clutch Accuracy (Accuracy Based On Last 5 Minutes Where |Final Margin| <= 10)
#   3PT Accuracy Through Games
#   2PT Accuracy Through Games
#   3PT Accuracy Based On Defender Distance
#   Accuracy Based On Number Of Dribbles Before Shooting - Accuracy Based On Touch Time Before Shooting
#   2PT Accuracy For Home and Away Games - 3PT Accuracy For Home and Away Games

# NEW COLUMNS: (New Columns Will Be Created Containing Any Information That Will Be Commonly Used)
#   Distance Categories [0 - 8, 8 - 22, 22 - 30, 30+]

# NOTE: Some variables are repeated just for the independence of each code segment

# Load data from csv file
df = pd.read_csv('curry_shot_logs.csv')

# Create New Columns
distanceBins = [0, 8, 22, 30, float('inf')]
distanceLabels = ['Paint Area', 'Mid-Range 2PT', '3PT', 'Deep 3PT']
df['distance_category'] = pd.cut(df['SHOT_DIST'], bins=distanceBins, labels=distanceLabels)

# Plot Styling
gsw_gold = '#FDB927'
gsw_blue = '#006BB6'
white = '#FFFFFF'
plt.rcParams.update({
    'axes.facecolor': gsw_blue,        
    'figure.facecolor': gsw_blue,     
    'axes.edgecolor': white,          
    'axes.labelcolor': white,         
    'xtick.color': white,              
    'ytick.color': white,             
    'text.color': white,              
    'axes.titlecolor': white,         
    'axes.prop_cycle': plt.cycler('color', [gsw_gold]) 
})



# Start Goals

# Attempts Based On Distance
totalAttemptsByDistance = df.groupby('distance_category', observed=False).size().values
plt.figure(figsize=(10, 6))
bars = plt.bar(distanceLabels, totalAttemptsByDistance)
plt.title("Attempts Based On Distance", fontsize=16)
plt.xlabel("Distance Category", fontsize=14)
plt.ylabel("Number of Attempts", fontsize=14)
plt.ylim(0, 1.3*max(totalAttemptsByDistance))
plt.grid(axis='y', linestyle='--', alpha=0.3, color=white)
for bar in bars: # Annotating bars
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
             f'{bar.get_height()}', ha='center', va='bottom', fontsize=12)
#plt.show()

# Accuracy Based On Distance
totalAttemptsByDistanceDF = df.groupby('distance_category', observed=False).size().values
madeAttemptsByDistance = df[df['SHOT_RESULT'] == 'made'].groupby('distance_category', observed=False).size().values
accuracyByDistance = (madeAttemptsByDistance / totalAttemptsByDistance * 100)
plt.figure(figsize=(10, 6))
bars = plt.bar(distanceLabels, accuracyByDistance)
plt.title("Accuracy Based On Distance", fontsize=16)
plt.xlabel("Distance Category", fontsize=14)
plt.ylabel("Accuracy", fontsize=14)
plt.ylim(0, 100)
plt.grid(axis='y', linestyle='--', alpha=0.3, color=white)
for bar in bars: # Annotating bars
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
             f'{bar.get_height():.1f}%', ha='center', va='bottom', fontsize=12)
#plt.show()

# Accuracy Based On Period
totalAttemptsByPeriod = df.groupby('PERIOD', observed=False).size().values
madeAttemptsByPeriod = df[df['SHOT_RESULT'] == 'made'].groupby('PERIOD', observed=False).size().values
accuracyByPeriod = (madeAttemptsByPeriod / totalAttemptsByPeriod) * 100
periodLabels = ['1st', '2nd', '3rd', '4th', 'OTs']
plt.figure(figsize=(10, 6))
bars = plt.bar(periodLabels, accuracyByPeriod)
plt.title("Accuracy Based On Period", fontsize=16)
plt.xlabel("Period", fontsize=14)
plt.ylabel("Accuracy", fontsize=14)
plt.ylim(0, 100)
plt.grid(axis='y', linestyle='--', alpha=0.3, color=white)
for bar in bars: # Annotating bars
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
             f'{bar.get_height():.1f}%', ha='center', va='bottom', fontsize=12)
#plt.show()

# Average Points Based On Period From FGs
totalPeriodsPlayed = df.groupby('PERIOD', observed=False)['GAME_ID'].nunique()
totalPointsPerPeriod = df.groupby('PERIOD', observed=False)['PTS'].sum().values
averagePointsByPeriod = totalPointsPerPeriod / totalPeriodsPlayed
periodLabels = ['1st', '2nd', '3rd', '4th', 'OTs']
plt.figure(figsize=(10, 6))
bars = plt.bar(periodLabels, averagePointsByPeriod)
plt.title("Average Points Based On Period From Field Goals", fontsize=16)
plt.xlabel("Period", fontsize=14)
plt.ylabel("Average Points", fontsize=14)
plt.ylim(0, 1.3*max(averagePointsByPeriod))
plt.grid(axis='y', linestyle='--', alpha=0.3, color=white)
for bar in bars: # Annotating bars
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
             f'{bar.get_height():.1f}', ha='center', va='bottom', fontsize=12)
#plt.show()

# Accuracy Of Clutch 2PTs and 3PTs (Accuracy Based On Last 5 Minutes Where |Final Margin| <= 10)
clutchAttempts = df[
    (df['PERIOD'] == 4) & 
    (pd.to_datetime(df['GAME_CLOCK'], format='%M:%S') <= pd.to_datetime("5:00", format='%M:%S')) & 
    (df['FINAL_MARGIN'].abs() <= 10)
]
totalAttempts = clutchAttempts.groupby('PTS_TYPE').size()
madeAttempts = clutchAttempts[clutchAttempts['SHOT_RESULT'] == 'made'].groupby('PTS_TYPE').size()
clutchAccuracy = (madeAttempts / totalAttempts * 100).values
shotTypeLabels = ['2PTs', '3PTs']
plt.figure(figsize=(10, 6))
bars = plt.bar(shotTypeLabels, clutchAccuracy)
plt.title("Accuracy Of Clutch 2PTs and 3PTs", fontsize=16)
plt.xlabel("Shot Type", fontsize=14)
plt.ylabel("Accuracy", fontsize=14)
plt.ylim(0, 100)
plt.grid(axis='y', linestyle='--', alpha=0.3, color=white)
for bar in bars: # Annotating bars
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
             f'{bar.get_height():.1f}%', ha='center', va='bottom', fontsize=12)
#plt.show()

# 2PT Accuracy Through Games
twoPointsAttempted = df[df['PTS_TYPE'] == 2]
twoPointsMade = twoPointsAttempted[twoPointsAttempted['SHOT_RESULT'] == 'made']
twoPointsAttemptedPerGame = twoPointsAttempted.groupby("GAME_ID", observed=False).size()
twoPointsMadePerGame = twoPointsMade.groupby("GAME_ID", observed=False).size()
twoPointsAccuracyPerGame = twoPointsMadePerGame / twoPointsAttemptedPerGame * 100
games = list(range(1, len(twoPointsAttemptedPerGame)+1))
plt.figure(figsize=(10, 6))
plt.plot(games, twoPointsAccuracyPerGame, linestyle='-', marker='o')
plt.title('2PT Accuracy Through Games', fontsize=16)
plt.xlabel('Game', fontsize=14)
plt.ylabel('Accuracy', fontsize=14)
plt.ylim(0, 100)
#plt.show()

# 3PT Accuracy Through Games
threePointsAttempted = df[df['PTS_TYPE'] == 3]
threePointsMade = threePointsAttempted[threePointsAttempted['SHOT_RESULT'] == 'made']
threePointsAttemptedPerGame = threePointsAttempted.groupby("GAME_ID", observed=False).size()
threePointsMadePerGame = threePointsMade.groupby("GAME_ID", observed=False).size()
threePointsAccuracyPerGame = threePointsMadePerGame / threePointsAttemptedPerGame * 100
games = list(range(1, len(threePointsAttemptedPerGame)+1))
plt.figure(figsize=(10, 6))
plt.plot(games, threePointsAccuracyPerGame, linestyle='-', marker='o')
plt.title('3PT Accuracy Through Games', fontsize=16)
plt.xlabel('Game', fontsize=14)
plt.ylabel('Accuracy', fontsize=14)
plt.ylim(0, 100)
#plt.show()

# 3PT Accuracy Based On Defender Distance
bins = [0, 2, 4, float('inf')]
labels = ['Contested', 'Semi-Contested', 'Wide Open']
threePoints = df[df['PTS_TYPE'] == 3]
threePointsAttemptsByDistance = threePoints.groupby(pd.cut(threePoints['CLOSE_DEF_DIST'], bins=bins, labels=labels), observed=False).size()
threePointsMadeByDistance = threePoints[threePoints['SHOT_RESULT'] == 'made'].groupby(pd.cut(threePoints['CLOSE_DEF_DIST'], bins=bins, labels=labels), observed=False).size()
threePointsAccuracyByDistance = threePointsMadeByDistance / threePointsAttemptsByDistance * 100
plt.figure(figsize=(10, 6))
bars = plt.bar(labels, threePointsAccuracyByDistance)
plt.title("3PT Accuracy Based On Defender Distance", fontsize=16)
plt.xlabel("Distance Type", fontsize=14)
plt.ylabel("Accuracy", fontsize=14)
plt.ylim(0, 100)
plt.grid(axis='y', linestyle='--', alpha=0.3, color=white)
for bar in bars: # Annotating bars
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
             f'{bar.get_height():.1f}%', ha='center', va='bottom', fontsize=12)
#plt.show()

# Accuracy Based On Number Of Dribbles Before Shooting -- Accuracy Based On Touch Time Before Shooting
totalAttemptsByDribbles = df.groupby('DRIBBLES', observed=False).size()
madeAttemptsByDribbles = df[df['SHOT_RESULT'] == 'made'].groupby('DRIBBLES', observed=False).size()
accuracyByDribbles = madeAttemptsByDribbles / totalAttemptsByDribbles * 100
dribbles = totalAttemptsByDribbles.index
bins = list(range(0, int(df['TOUCH_TIME'].max()+1)))
labels = [f"{x}-{x+1}" for x in bins[:-1]]
labels.append(str(max(bins))+'+')
bins.append(float('inf'))
totalAttemptsByTouchTime = df.groupby(pd.cut(threePoints['TOUCH_TIME'], bins=bins, labels=labels), observed=False).size()
madeAttemptsByTouchTime = df[df['SHOT_RESULT'] == 'made'].groupby(pd.cut(threePoints['TOUCH_TIME'], bins=bins, labels=labels), observed=False).size()
accuracyByTouchTime = madeAttemptsByTouchTime / totalAttemptsByTouchTime * 100
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
bars1 = ax1.bar(dribbles, accuracyByDribbles)
ax1.set_title("Accuracy Based On Number Of Dribbles Before Shooting", fontsize=16)
ax1.set_xlabel("Dribbles", fontsize=14)
ax1.set_ylabel("Accuracy (%)", fontsize=14)
for bar in bars1:
    ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
             f'{bar.get_height():.1f}%', ha='center', va='bottom', fontsize=8)
bars2 = ax2.bar(labels, accuracyByTouchTime)
ax2.set_title("Accuracy Based On Touch Time Before Shooting", fontsize=16)
ax2.set_xlabel("Touch Time (sec)", fontsize=14)
ax2.set_ylabel("Accuracy", fontsize=14)
for bar in bars2:
    ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
             f'{bar.get_height():.1f}%', ha='center', va='bottom', fontsize=8)
plt.tight_layout()
#plt.show()

# 2PT Accuracy For Home and Away Games - 3PT Accuracy For Home and Away Games
twoPoints = df[df['PTS_TYPE'] == 2]
threePoints = df[df['PTS_TYPE'] == 3]
totalTwoPoints = twoPoints.groupby('LOCATION')['SHOT_RESULT'].count()
madeTwoPoints = twoPoints[twoPoints['SHOT_RESULT'] == 'made'].groupby('LOCATION')['SHOT_RESULT'].count()
twoPointsAccuracy = (madeTwoPoints / totalTwoPoints * 100).fillna(0)
totalThreePoints = threePoints.groupby('LOCATION')['SHOT_RESULT'].count()
madeThreePoints = threePoints[threePoints['SHOT_RESULT'] == 'made'].groupby('LOCATION')['SHOT_RESULT'].count()
threePointsAccuracy = (madeThreePoints / totalThreePoints * 100).fillna(0)
accuracyByLocation = list(twoPointsAccuracy.values) + list(threePointsAccuracy.values)
labels = ['2PT Home', '2PT Away', '3PT Home', '3PT Away']
plt.figure(figsize=(10, 6))
bars = plt.bar(labels, accuracyByLocation)
plt.title("2PT and 3PT Accuracy For Home and Away Games", fontsize=16)
plt.xlabel("Shot Type", fontsize=14)
plt.ylabel("Accuracy", fontsize=14)
plt.ylim(0, 100)
plt.grid(axis='y', linestyle='--', alpha=0.3, color=white)
for bar in bars: # Annotating bars
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
             f'{bar.get_height():.1f}%', ha='center', va='bottom', fontsize=12)
#plt.show()

plt.show()