# Projeto/leaderboard_manager.py
import json
import os

class LeaderboardManager:
    def __init__(self, leaderboard_file="leaderboard.json"):
        """
        Initializes the LeaderboardManager.

        Args:
            leaderboard_file (str): The name of the file to store leaderboard data.
        """
        self._leaderboard_file = leaderboard_file

    def load_leaderboard(self):
        """
        Loads the leaderboard from the JSON file.
        If the file doesn't exist, it returns an empty list.
        """
        if not os.path.exists(self._leaderboard_file):
            return []
        
        try:
            with open(self._leaderboard_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Sort scores by time (elapsed_time) in ascending order
            return sorted(data, key=lambda x: x.get("elapsed_time", float('inf')))
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading leaderboard: {e}")
            return []

    def save_score(self, name, elapsed_time):
        """
        Saves a new score to the leaderboard.

        Args:
            name (str): The player's name.
            elapsed_time (float): The time taken to finish the game.
        """
        leaderboard = self.load_leaderboard()
        
        new_score = {
            "name": name,
            "elapsed_time": elapsed_time
        }
        leaderboard.append(new_score)
        
        try:
            with open(self._leaderboard_file, "w", encoding="utf-8") as f:
                json.dump(leaderboard, f, indent=4)
            print(f"Score for {name} saved successfully.")
        except IOError as e:
            print(f"Error saving leaderboard: {e}")
