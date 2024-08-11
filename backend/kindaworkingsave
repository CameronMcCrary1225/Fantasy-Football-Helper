from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

website = 'https://fantasydata.com/nfl/fantasy-football-leaders?position=1&season=2023&seasontype=1&scope=1&subscope=1&scoringsystem=2&aggregatescope=1&range=3'
service = Service(executable_path="chromedriver.exe")

# Set Chrome options to run in headless mode
options = Options()
options.headless = True

driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 5)  # Adjust the timeout as needed

players_data = []  # List to store player data dictionaries

try:
    driver.get(website)
    
    # Fetch positions from the main page
    positions = []
    tabletwo = driver.find_element(By.XPATH, "//table[@id='stats_grid']")
    rows = tabletwo.find_elements(By.TAG_NAME, "tr")
    
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) == 14:
            position = cells[1].text.strip()  # Assuming position is in the second column
            positions.append(position)

    # Find all links to process
    a_tags = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'k-grid-content-locked')]//a")))
    
    for index in range(len(a_tags)):
        # Re-fetch a_tags inside the loop to avoid StaleElementReferenceException
        a_tags = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'k-grid-content-locked')]//a")))
        
        a_tag = a_tags[index]
        href = a_tag.get_attribute("href")
        player_data = {'targets': [], 'attempts': [], 'points': []}  # Dictionary to store player data
                
        a_tag.click()

        # Wait for the table to load (adjust sleep time as needed)
        time.sleep(2)  # Example wait time, you may need to adjust this
        
        # Find all rows within the second grid content div
        tablerows = wait.until(EC.presence_of_all_elements_located((By.XPATH, "(//div[@class='k-grid-content k-auto-scrollable'])[2]//table//tbody//tr")))
        
        for row in tablerows:
            tds = row.find_elements(By.XPATH, ".//td")
            if len(tds) >= 13:
                # Extract data based on position
                if positions[index] == "WR":
                    targets = int(tds[3].text.strip())
                    attempts = int(tds[9].text.strip())
                    points = float(tds[16].text.strip())
                elif positions[index] == "QB":
                    points = float(tds[15].text.strip())
                    attempts = int(tds[10].text.strip())  # Rushing attempts
                    targets = int(tds[3].text.strip())  # Passing attempts for qb
                elif positions[index] == "RB":
                    attempts = int(tds[2].text.strip())
                    targets = int(tds[7].text.strip())
                    points = float(tds[13].text.strip())
                elif positions[index] == "TE":
                    targets = int(tds[3].text.strip())
                    attempts = int(tds[9].text.strip())
                    points = float(tds[16].text.strip()) #check laters
                
                # Append data to player_data dictionary
                player_data['targets'].append(targets)
                player_data['attempts'].append(attempts)
                player_data['points'].append(points)
            
        players_data.append(player_data)  # Append player data to the list
        
        # Go back to the main page
        driver.back()
    
finally:
    driver.quit()

# Print out all player data collected
for idx, player_data in enumerate(players_data, start=1):
    print(f"Player {idx} Data:")
    print("Targets:", player_data['targets'])
    print("Attempts:", player_data['attempts'])
    print("Points:", player_data['points'])
    print()
