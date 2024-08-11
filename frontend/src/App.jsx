import React, { useState, useEffect } from 'react';
import './App.css';
import PlayerList from './Playerlist';

function App() {
  const [players, setPlayers] = useState([]);
  const [sortedPlayers, setSortedPlayers] = useState([]);
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'ascending' });
  const[positionFilters, setPositionFilters] = useState({
    rb: true,
    wr: true,
    te: true,
    qb: true,
    k: true,
  })

  useEffect(() => {
    fetchPlayers();
  }, []);

  const fetchPlayers = async () => {
    const response = await fetch("http://127.0.0.1:5000/player");
    const data = await response.json();
    setPlayers(data.players);
    setSortedPlayers(data.players); // Initialize sortedPlayers with the fetched data
  }

  const handleSort = (key) => {
    let direction = 'ascending';
    if (sortConfig.key === key && sortConfig.direction === 'ascending') {
      direction = 'descending';
    }

    setSortConfig({ key, direction });

    const sorted = [...sortedPlayers].sort((a, b) => {
      if (a[key] > b[key]) return direction === 'ascending' ? -1 : 1;
      if (a[key] < b[key]) return direction === 'ascending' ? 1 : -1;
      return 0;
    });

    setSortedPlayers(sorted);
  }

  const handleCheckboxChange = (e) => {
    const {id, checked} = e.target;
    setPositionFilters(prevFilters => ({
      ...prevFilters,
      [id]: checked,
    }))
  }

  const filterPlayersByPosition = () => {
    let filteredPlayers = players.filter(player => {
      if (positionFilters.rb && player.position === 'RB') {
        return true;
      }
      if (positionFilters.wr && player.position === 'WR') {
        return true;
      }
      if (positionFilters.qb && player.position === 'QB'){
        return true;
      }
      if (positionFilters.te && player.position === 'TE'){
        return true;
      }
      if (positionFilters.k && player.position === 'K'){
        return true;
      }
      return false;
    });
  
    if (Object.values(positionFilters).every(val => !val)) {
      // If no filters are selected, show all players
      filteredPlayers = players;
    }
  
    setSortedPlayers(filteredPlayers);
  }
  useEffect(() => {
    filterPlayersByPosition();

  }, [positionFilters]);

  const fetchDataFromScraper = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/getdata");
      if (!response.ok) {
        throw new Error('Failed to fetch data from web scraper');
      }
      // Optionally, you can fetch players again after scraping
      // fetchPlayers();
      alert('Web scraper triggered successfully!');
    } catch (error) {
      console.error('Error triggering web scraper:', error);
      alert('Failed to trigger web scraper');
    }
  };
  return (
    <div className="App">
      <button onClick={fetchDataFromScraper} className="fantasy-button">Get Fantasy Data</button>
      <div id="filterOptions">
        <label><input type="checkbox" id="rb" checked={positionFilters.rb} onChange={handleCheckboxChange} /> RB</label>
        <label><input type="checkbox" id="wr" checked={positionFilters.wr} onChange={handleCheckboxChange} /> WR</label>
        <label><input type="checkbox" id="te" checked={positionFilters.te} onChange={handleCheckboxChange} /> TE</label>
        <label><input type="checkbox" id="qb" checked={positionFilters.qb} onChange={handleCheckboxChange} /> QB</label>
        <label><input type="checkbox" id="k" checked={positionFilters.k} onChange={handleCheckboxChange} /> K</label>
      </div>
      <PlayerList players={sortedPlayers} handleSort={handleSort} />
    </div>
  );
}

export default App;
