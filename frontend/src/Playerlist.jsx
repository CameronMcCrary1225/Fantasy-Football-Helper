import React, { useState, useEffect } from "react";
import './PlayerStatsPopup.css';
import PlayerStatsPopup from "./PlayerStatsPopup";

const PlayerList = ({ players, handleSort }) => {
    const [hoveredPlayer, setHoveredPlayer] = useState(null);
    const [popupPosition, setPopupPosition] = useState({ top: 0, left: 0 });
    const [thresholds, setThresholds] = useState({});

    useEffect(() => {
        const calculateThresholds = () => {
            const thresholds = {};
            const stats = [
                'activity',
                'gamesPlayed',
                'points',
                'touchdownDependency',
                'consistency',
            ];
            stats.forEach((stat) => {
                const sortedPlayers = [...players].sort((a, b) => b[stat] - a[stat]);
                const totalPlayers = sortedPlayers.length;
                const top30Threshold = sortedPlayers[Math.floor(totalPlayers * 0.3)][stat];
                const bottom30Threshold = sortedPlayers[Math.ceil(totalPlayers * 0.7)][stat];
                thresholds[stat] = { top30Threshold, bottom30Threshold };
            });
            return thresholds;
        };

        if (players.length > 0) {
            const thresholds = calculateThresholds();
            setThresholds(thresholds);
        }
    }, [players]);

    const handleMouseEnter = (player, event) => {
        setHoveredPlayer(player);
        const rect = event.target.getBoundingClientRect();
        setPopupPosition({
            top: rect.bottom + window.scrollY,
            left: rect.left + window.scrollX
        });
    };

    const handleMouseLeave = () => {
        setHoveredPlayer(null);
    };

    const getStatColor = (stat, value) => {
        if (!thresholds[stat]) return "";
        if (value >= thresholds[stat].top30Threshold) {
            return "green-text";
        } else if (value <= thresholds[stat].bottom30Threshold) {
            return "red-text";
        } else {
            return "";
        }
    };

    return (
        <div>
            <h2 className='titlename'>Top 100 Fantasy Football Player!</h2>
            <table className="statstable">
                <thead className="headers">
                    <tr>
                        <th onClick={() => handleSort('rank')}>Rank</th>
                        <th onClick={() => handleSort('name')}>Name</th>
                        <th onClick={() => handleSort('team')}>Team</th>
                        <th onClick={() => handleSort('position')}>Position</th>
                        <th onClick={() => handleSort('gamesPlayed')}>Percent Played</th>
                        <th onClick={() => handleSort('points')}>Points</th>
                        <th onClick={() => handleSort('touchdownDependency')}>Touchdown Dependency</th>
                        <th onClick={() => handleSort('consistency')}>Consistency</th>
                        <th onClick={() => handleSort('activity')}>Average Activity</th>
                    </tr>
                </thead>
                <tbody className="content">
                    {players.map((player) => (
                        <tr key={player.id}
                            onMouseEnter={(e) => handleMouseEnter(player, e)}
                            onMouseLeave={handleMouseLeave}>
                            <td>{player.rank}</td>
                            <td>{player.name}</td>
                            <td>{player.team}</td>
                            <td>{player.position}</td>
                            <td className={getStatColor("gamesPlayed", player.gamesPlayed)}>{player.gamesPlayed}%</td>
                            <td className={getStatColor("points", player.points)}>{player.points}</td>
                            <td className={getStatColor("touchdownDependency", player.touchdownDependency)}>{player.touchdownDependency}%</td>
                            <td className={getStatColor("consistency", player.consistency)}>{player.consistency}</td>
                            <td className={getStatColor("activity", player.activity)}>{player.activity}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
            {hoveredPlayer && (
                <PlayerStatsPopup player={hoveredPlayer} position={popupPosition} />
            )}
        </div>
    );
};

export default PlayerList;
