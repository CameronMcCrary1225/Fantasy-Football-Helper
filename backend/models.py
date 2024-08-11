from config import db
from sqlalchemy.dialects.sqlite import JSON
import numpy as np

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    team = db.Column(db.String(50))
    position = db.Column(db.String(20))
    games = db.Column(db.Integer)
    pass_yards = db.Column(db.Integer)
    pass_td = db.Column(db.Integer)
    pass_int = db.Column(db.Integer)
    rush_yards = db.Column(db.Integer)
    rush_td = db.Column(db.Integer)
    rec_rec = db.Column(db.Integer)
    rec_yards = db.Column(db.Integer)
    rec_td = db.Column(db.Integer)
    ppg = db.Column(db.Float)
    points = db.Column(db.Integer)
    targets = db.Column(JSON)
    attempts = db.Column(JSON)
    points_per_game = db.Column(JSON)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "rank": self.rank,
            "team": self.team,
            "position": self.position,
            "games": self.games,
            "passYards": self.pass_yards,
            "passTd": self.pass_td,
            "passInt": self.pass_int,
            "rushYards": self.rush_yards,
            "rushTd": self.rush_td,
            "recRec": self.rec_rec,
            "recYards": self.rec_yards,
            "recTd": self.rec_td,
            "ppg": self.ppg,
            "points": self.points,
            "targets": self.targets,
            "attempts": self.attempts,
            "pointsPerGame": self.points_per_game,
            "touchdownDependency": self.touchdown_dependency(),
            "consistency": self.consistency(),
            "gamesPlayed": self.injury(),
            "activity":self.activity()
        }
    
    def touchdown_dependency(self):
        if self.points == 0:
            return 0
        point_from_touchdowns = (self.pass_td * 4) + (self.rec_td * 6) + (self.rush_td * 6)
        touchdown_dependency_ratio = (point_from_touchdowns / self.points) * 100.0
        return round(touchdown_dependency_ratio, 1)

    def consistency(self):
        if not self.points_per_game:
            return 0.0
        points_list = [int(points) for points in self.points_per_game]
        if len(points_list) < 2:
            return 0/0
        std_dev = np.std(points_list)
        return round(std_dev, 2)
    
    def injury(self):
        if self.games is None or self.games == 0:
            return 0.0
        percentage = self.games / 17.0  # Assuming 17 weeks in a regular NFL season
        return round(percentage * 100, 1)
    
    def activity(self):
        if not self.targets or not self.attempts:
            return 0.0
        total_sum = 0
        num_items = min(len(self.targets), len(self.attempts))
        for i in range(num_items):
            total_sum += self.targets[i] + self.attempts[i]
        average_activity = total_sum / num_items
        return round(average_activity, 2)