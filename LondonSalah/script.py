import json
from datetime import datetime
import time
from pydub import AudioSegment
from pydub.playback import play

# Open the JSON file and load the data
with open('London-json.json') as f:
    data = json.load(f)

# Get the current date
today = datetime.now()

# Convert today's date into the format used in your JSON file
day = str(today.day)
month = str(today.month)

# Find the correct entry for today
for entry in data:
    if (entry['Date'] == day and entry['Month'] == month):
        times = {k: v for k, v in entry.items() if k in ['Dawn', 'Noon', 'Maghrib']}

# For each prayer time
for prayer, prayer_time in times.items():
    # Convert prayer time to datetime object
    prayer_datetime = datetime.strptime(f'{day}-{month}-{today.year} {prayer_time}', '%d-%m-%Y %H:%M')

    # Calculate seconds until prayer time
    seconds_until_prayer = (prayer_datetime - datetime.now()).total_seconds()
    
    # If the prayer time is in the future
    if seconds_until_prayer > 0:
        # Sleep until prayer time
        time.sleep(seconds_until_prayer)
    
        # Play the Athaan
        song = AudioSegment.from_mp3("athaan-ghalwash-rast.mp3")
        play(song)
