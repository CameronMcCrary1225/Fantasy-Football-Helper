import React from 'react';
import './PlayerStatsPopup.css';

const PlayerStatsPopup = ({ player, position }) => {
    const { top, left } = position;

    return (
        <div className="player-stats-popup" style={{ top, left }}>
            <h3>{player.name} - Detailed Stats</h3>
            <p>Pass Yards: {player.passYards}</p>
            <p>Pass TD: {player.passTd}</p>
            <p>Pass Int: {player.passInt}</p>
            <p>Rush Yards: {player.rushYards}</p>
            <p>Rush TD: {player.rushTd}</p>
            <p>Receptions: {player.recRec}</p>
            <p>Receiving Yards: {player.recYards}</p>
            <p>Receiving TD: {player.recTd}</p>
            <p>Targets/Pass Attempts: {player.targets.join(', ')}</p>
            <p>Attempts: {player.attempts.join(', ')}</p>
            <p>PPG: {player.pointsPerGame.join(', ')}</p>
        </div>
    );
}

export default PlayerStatsPopup;
