import argparse
import datetime
import dateutil.parser
import json
import pprint
import urllib2


FEED_URL = "http://gd2.mlb.com/components/game/mlb/{:year_%Y/month_%m/day_%d}/master_scoreboard.json"

class Team:
  def __init__(self):
    self.name = ''
    self.code = ''
    self.team_id = 0
    self.wins = 0
    self.losses = 0
    self.league = ''
    self.division = ''

  def __repr__(self):
    return str(self.__dict__)

class Pitcher:
  def __init__(self):
    self.first_name = ''
    self.last_name = ''
    self.player_id = 0
    self.era = 0.
    self.wins = 0
    self.losses = 0
    self.throwing_hand = ''

  def __repr__(self):
    return str(self.__dict__)

class Park:
  def __init__(self):
    self.city = ''
    self.venue = ''
    self.venue_id = 0
    self.weather_code = ''

  def __repr__(self):
    return str(self.__dict__)


class GameInfo:
  def __init__(self):
    self.home_team = Team()
    self.away_team = Team()
    self.park = Park()
    self.time = None
    self.home_pitcher = None
    self.away_pitcher = None
    self.scheduled_innings = 9
    self.game_data_dir = ''

  def __repr__(self):
    return str(self.__dict__)

def deunicode(input):
  if isinstance(input, dict):
    return {deunicode(key): deunicode(value)
        for key, value in input.iteritems()}
  elif isinstance(input, list):
    return [deunicode(element) for element in input]
  elif isinstance(input, unicode):
    return input.encode('utf-8')
  else:
    return input

def FetchGames(year, month, day):
  date = datetime.datetime(year, month, day)
  url = FEED_URL.format(date)
  response = urllib2.urlopen(url)
  txt_response = response.read()
  json_response = deunicode(json.loads(txt_response))
  games = []
  for game in json_response['data']['games']['game']:
    game_info = GameInfo()

    game_info.home_team.name = game['home_team_name']
    game_info.home_team.code = game['home_code']
    game_info.home_team.team_id = int(game['home_team_id'])
    game_info.home_team.wins = int(game['home_win'])
    game_info.home_team.losses = int(game['home_loss'])
    game_info.home_team.league = "AL" if game['home_league_id'] == "103" else "NL"
    game_info.home_team.division = game['home_division']

    game_info.away_team.name = game['away_team_name']
    game_info.away_team.code = game['away_code']
    game_info.away_team.team_id = int(game['away_team_id'])
    game_info.away_team.wins = int(game['away_win'])
    game_info.away_team.losses = int(game['away_loss'])
    game_info.away_team.league = "AL" if game['away_league_id'] == "103" else  "NL"
    game_info.away_team.division = game['away_division']

    game_info.park.city = game['location']
    game_info.park.venue = game['venue']
    game_info.park.venue_id = int(game['venue_id'])
    game_info.park.weather_code = game['venue_w_chan_loc']

    if 'home_probable_pitcher' in game and game['home_probable_pitcher']['id'] != '':
      game_info.home_pitcher = Pitcher()
      game_info.home_pitcher.first_name = game['home_probable_pitcher']['first_name']
      game_info.home_pitcher.last_name = game['home_probable_pitcher']['last_name']
      game_info.home_pitcher.player_id = int(game['home_probable_pitcher']['id'])
      era = game['home_probable_pitcher']['s_era']
      game_info.home_pitcher.era = float(era) if era != '-.--' else float('inf')
      game_info.home_pitcher.wins = int(game['home_probable_pitcher']['s_wins'])
      game_info.home_pitcher.losses = int(game['home_probable_pitcher']['s_losses'])
      game_info.home_pitcher.throwing_hand = game['home_probable_pitcher']['throwinghand']

    if 'away_probable_pitcher' in game and game['away_probable_pitcher']['id'] != '':
      game_info.away_pitcher = Pitcher()
      game_info.away_pitcher.first_name = game['away_probable_pitcher']['first_name']
      game_info.away_pitcher.last_name = game['away_probable_pitcher']['last_name']
      game_info.away_pitcher.player_id = int(game['away_probable_pitcher']['id'])
      era = game['away_probable_pitcher']['s_era']
      game_info.away_pitcher.era = float(era) if era != '-.--' else float('inf')
      game_info.away_pitcher.wins = int(game['away_probable_pitcher']['s_wins'])
      game_info.away_pitcher.losses = int(game['away_probable_pitcher']['s_losses'])
      game_info.away_pitcher.throwing_hand = game['away_probable_pitcher']['throwinghand']

    if 'media' in game['game_media']:
      start_time = ''
      if isinstance(game['game_media']['media'], list):
        start_time = game['game_media']['media'][0]['start']
      else:
        start_time = game['game_media']['media']['start']
      game_info.time = dateutil.parser.parse(start_time)
    else:
      # This version lacks timezone.
      game_info.time = dateutil.parser.parse('%s %s %s' % (game['time_date'],
                                                           game['ampm'],
                                                           game['time_zone']))
    game_info.scheduled_innings = int(game['scheduled_innings'])
    game_info.game_data_dir = game['game_data_directory']

    games.append(game_info)

  return games

if __name__ == "__main__":
  today = datetime.date.today()
  parser = argparse.ArgumentParser()
  parser.add_argument('--year', type=int, default=today.year)
  parser.add_argument('--month', type=int, default=today.month)
  parser.add_argument('--day', type=int, default=today.day)
  args = parser.parse_args()

  games = FetchGames(args.year, args.month, args.day)

  pp = pprint.PrettyPrinter(indent=2)
  pp.pprint(games)
