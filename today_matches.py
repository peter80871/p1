import datetime
import db

def today_match():
    d = db.show_data_in_table('UPCOMING_MATCHES')
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    tomorrow = str(tomorrow).split('-')
    today_matches = [i for i in d if i[3].split('.')[0] == tomorrow[2] and i[3].split('.')[1] == tomorrow[1]]
    return today_matches
        