from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from config import db, app
from models import Player

def web_scraper():
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    #website = 'https://fantasydata.com/nfl/fantasy-football-leaders?position=1&season=2023&seasontype=1&scope=1&subscope=1&scoringsystem=2&aggregatescope=1&range=3'
    website = 'https://fantasydata.com/nfl/fantasy-football-leaders?scope=season&scoring=fpts_ppr&order_by=fpts_ppr&sort_dir=desc&sp=2023_REG'
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 10)

    players_data = []

    try:
        driver.get(website)

        # Part 1: Scraping main page for player names, ranks, and initial stats
        tableone = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='k-grid-content-locked']//table")))
        for table in tableone:
            rows = table.find_elements(By.TAG_NAME, "tr")
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) >= 2:
                    rank = cells[0].text.strip()
                    name = cells[1].text.strip()
                    players_data.append({
                        'name': name,
                        'rank': int(rank),
                        'team': None,
                        'position': None,
                        'games': None,
                        'pass_yards': None,
                        'pass_td': None,
                        'pass_int': None,
                        'rush_yards': None,
                        'rush_td': None,
                        'rec_rec': None,
                        'rec_yards': None,
                        'rec_td': None,
                        'fumbles': None,
                        'ppg': None,
                        'points': None,
                        'targets': [],
                        'attempts': [],
                        'points_per_game': []
                    })

        # Part 2: Scraping individual player pages for detailed stats
        tabletwo = wait.until(EC.presence_of_element_located((By.XPATH, "//table[@id='stats_grid']")))
        rows = tabletwo.find_elements(By.TAG_NAME, "tr")
        positions = []
        player_index = 0
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) == 14:
                team = cells[0].text.strip()
                position = cells[1].text.strip()
                positions.append(position)
                games = cells[2].text.strip()
                pass_yards = cells[3].text.strip()
                pass_td = cells[4].text.strip()
                pass_int = cells[5].text.strip()
                rush_yards = cells[6].text.strip()
                rush_td = cells[7].text.strip()
                rec_rec = cells[8].text.strip()
                rec_yards = cells[9].text.strip()
                rec_td = cells[10].text.strip()
                fumbles = cells[11].text.strip()
                ppg = cells[12].text.strip()
                points = cells[13].text.strip()

                players_data[player_index].update({
                    'team': team,
                    'position': position,
                    'games': games,
                    'pass_yards': pass_yards,
                    'pass_td': pass_td,
                    'pass_int': pass_int,
                    'rush_yards': rush_yards,
                    'rush_td': rush_td,
                    'rec_rec': rec_rec,
                    'rec_yards': rec_yards,
                    'rec_td': rec_td,
                    'fumbles': fumbles,
                    'ppg': ppg,
                    'points': points
                })
                
                player_index += 1

        a_tags = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'k-grid-content-locked')]//a")))

        for index in range(len(a_tags)):
            a_tags = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'k-grid-content-locked')]//a")))
            a_tag = a_tags[index]
            href = a_tag.get_attribute("href")
            a_tag.click()


            tablerows = wait.until(EC.presence_of_all_elements_located((By.XPATH, "(//div[@class='k-grid-content k-auto-scrollable'])[2]//table//tbody//tr")))
            player_data = {'targets': [], 'attempts': [], 'points_per_game': []}

            for row in tablerows:
                tds = row.find_elements(By.XPATH, ".//td")
                if len(tds) >= 13:
                    if positions[index] == "WR":
                        targets = int(tds[3].text.strip())
                        attempts = int(tds[9].text.strip())
                        points_per_game = float(tds[16].text.strip())
                    elif positions[index] == "QB":
                        points_per_game = float(tds[15].text.strip())
                        attempts = int(tds[10].text.strip())  # Rushing attempts
                        targets = int(tds[3].text.strip())  # Passing attempts for QB
                    elif positions[index] == "RB":
                        attempts = int(tds[2].text.strip())
                        targets = int(tds[7].text.strip())
                        points_per_game = float(tds[13].text.strip())
                    elif positions[index] == "TE":
                        targets = int(tds[3].text.strip())
                        attempts = int(tds[9].text.strip())
                        points_per_game = float(tds[16].text.strip())

                    player_data['targets'].append(targets)
                    player_data['attempts'].append(attempts)
                    player_data['points_per_game'].append(points_per_game)

            # Update player_data in players_data list
            players_data[index].update(player_data)

            driver.back()  # Go back to the main page


        # Part 3: Print out collected player data
        for idx, player_data in enumerate(players_data, start=1):
            print(f"Player {idx} Data:")
            print(f"Name: {player_data['name']}")
            print(f"Rank: {player_data['rank']}")
            print(f"Team: {player_data['team']}")
            print(f"Position: {player_data['position']}")
            print(f"Games: {player_data['games']}")
            print(f"Pass Yards: {player_data['pass_yards']}")
            print(f"Pass TD: {player_data['pass_td']}")
            print(f"Pass Int: {player_data['pass_int']}")
            print(f"Rush Yards: {player_data['rush_yards']}")
            print(f"Rush TD: {player_data['rush_td']}")
            print(f"Receptions: {player_data['rec_rec']}")
            print(f"Receiving Yards: {player_data['rec_yards']}")
            print(f"Receiving TD: {player_data['rec_td']}")
            print(f"Fumbles: {player_data['fumbles']}")
            print(f"PPG: {player_data['ppg']}")
            print(f"Points: {player_data['points']}")
            print(f"Targets: {player_data['targets']}")
            print(f"Attempts: {player_data['attempts']}")
            print(f"Points per Game: {player_data['points_per_game']}")
            print()

        with app.app_context():
            for player_data in players_data:
                new_player = Player(
                    name=player_data['name'],
                    rank=player_data['rank'],
                    team=player_data['team'],
                    position=player_data['position'],
                    games=player_data['games'],
                    pass_yards=player_data['pass_yards'],
                    pass_td=player_data['pass_td'],
                    pass_int=player_data['pass_int'],
                    rush_yards=player_data['rush_yards'],
                    rush_td=player_data['rush_td'],
                    rec_rec=player_data['rec_rec'],
                    rec_yards=player_data['rec_yards'],
                    rec_td=player_data['rec_td'],
                    fumbles=player_data['fumbles'],
                    ppg=player_data['ppg'],
                    points=player_data['points'],
                    targets=player_data['targets'],
                    attempts=player_data['attempts'],
                    points_per_game=player_data['points_per_game']
                )
                db.session.add(new_player)

            db.session.commit()
    except Exception as e:
        print(f"Error occurred during scraping: {str(e)}")

    finally:
        driver.quit()

