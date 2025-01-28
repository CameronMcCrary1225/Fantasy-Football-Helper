Fantasy Football Helper Website

This project is a Fantasy Football Helper website that helps users analyze player stats by scraping data from a website using Selenium, storing it in a Flask SQLAlchemy database, and providing custom statistics on the frontend. The data is for the 2023 season and is regularly updated through scraping, with additional custom stats calculated in the backend.

Features

- Web Scraping with Selenium: The backend uses Selenium to scrape fantasy football data for players, capturing stats from a dynamic website.
- Backend:
  - Uses Flask with SQLAlchemy to store scraped data in a database.
  - Calculates custom stats, such as touchdown dependency and game activity, based on player data.
- Frontend:
  - Built using React, JavaScript, HTML, and CSS.
  - Displays data in an easily sortable table that allows users to sort by position and various statistics.
  - Allows users to interactively view and analyze player data with custom stats calculated by the backend.

Installation

Prerequisites

- Ensure you have Node.js and Python installed on your system.
- For the frontend, npm should be installed via Node.js.
- For the backend, install the necessary Python libraries using pip.

Frontend Setup

1. Clone the repository to your local machine:

2. Navigate to the frontend directory:

3. Install dependencies:
   npm install

Backend Setup

1. Navigate to the backend directory:

2. Install the required Python dependencies:
   pip install numpy flask flask_sqlalchemy flask_cors selenium

3. Scrape the data using Selenium:
   - You may need to configure Selenium WebDriver depending on the browser you’re using (e.g., ChromeDriver for Chrome).
   - A set of data has been provided for your use so you dont need to webscrape as it might not work depending on the current date.
   
Run the program
- On the backend do python main.py
- On the frontend do npm run dev

Database Setup

The backend uses SQLAlchemy to store the scraped data in a database. A filled in database in provided but on the website pressing Get Fantasy data will create a new set of data.
If you create a new set of data the website might have updated so the webscraper might no tbe configured properly.

Custom Stats

The backend calculates custom statistics, such as touchdown dependency and game activity, and sends them to the frontend for display.

Usage

Once the frontend and backend are both running, you can access the website and view the sortable table of player stats. You can sort the table by clicking the top label. Here is an example of the some of them:
- Position
- Names alphabetically
- Rank
- Custom statistics like touchdown dependency, activity in the game, and others.

Technologies Used

Backend
- Flask: Web framework for serving the backend API.
- Flask SQLAlchemy: ORM to interact with the database.
- Flask CORS: Handle Cross-Origin Resource Sharing for frontend-backend communication.
- Selenium: Web scraping library for gathering live fantasy football data.
- Numpy: For any numerical calculations needed for custom statistics.

Frontend
- React: JavaScript library for building the user interface.
- JavaScript, HTML, CSS: For creating the dynamic and interactive frontend.
- npm: For managing frontend dependencies.

Future Plans
The project is completed and serves it purpose in aiding my fantasy football draft. I plan on returning next year and updating the webscraper so I can use it again with new data.

Acknowledgements

This project was created to help fantasy football players analyze data efficiently and was developed as a personal project to gain experience in web scraping, full-stack development, and creating interactive user interfaces.
