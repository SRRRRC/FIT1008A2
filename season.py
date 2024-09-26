from __future__ import annotations
from data_structures.bset import BSet
from data_structures.referential_array import ArrayR
from data_structures.linked_list import LinkedList
from dataclasses import dataclass
from team import Team , TeamStats
from typing import Generator, Union
from game_simulator import GameSimulator




@dataclass
class Game:
    """
    Simple container for a game between two teams.
    Both teams must be team objects, there cannot be a game without two teams.

    Note: Python will automatically generate the init for you.
    Use Game(home_team: Team, away_team: Team) to use this class.
    See: https://docs.python.org/3/library/dataclasses.html
    """
    home_team: Team = None
    away_team: Team = None


class WeekOfGames:
    """
    Simple container for a week of games.

    A fixture must have at least one game.
    """

    def __init__(self, week: int, games: ArrayR[Game]) -> None:
        """
        Container for a week of games.

        Args:
            week (int): The week number.
            games (ArrayR[Game]): The games for this week.
        """
        self.games: ArrayR[Game] = games
        self.week: int = week
        self.num: int =0

    def get_games(self) -> ArrayR:
        """
        Returns the games in a given week.

        Returns:
            ArrayR: The games in a given week.

        Complexity:
        Best Case Complexity: O(1)
        Worst Case Complexity: O(1)
        """
        return self.games

    def get_week(self) -> int:
        """
        Returns the week number.

        Returns:
            int: The week number.

        Complexity:
        Best Case Complexity: O(1)
        Worst Case Complexity: O(1)
        """
        return self.week

    def __iter__(self):
        """
        Complexity:
        Best Case Complexity: O(1)
        Worst Case Complexity: O(1)
        """
        self.num =0 
        return self

    def __next__(self):
        """
        Complexity:
        Best Case Complexity: O(1)
        Worst Case Complexity: O(1)
        """
        if self.num < len(self.games):
            game = self.games[self.num]
            self.num +=1
            return game
        else:
            raise StopIteration


class Season:

    def __init__(self, teams: ArrayR[Team]) -> None:
        """
        Initializes the season with a schedule.

        Args:
            teams (ArrayR[Team]): The teams playing in this season.

        Complexity:
            Best Case Complexity: O(N^2) where N is the number of teams.
            Worst Case Complexity: O(N^2) where N is the number of teams.
        """
        self.teams = teams
        self.schedule = self._generate_schedule()
        self.leaderboard = LinkedList()

        #adding teams to the leaderboard
        #O(N^2) where N is the number of teams
        for team in teams:
            inserted = False
            #O(N) where N is number of teams
            for i in range(len(self.leaderboard)):
                if self._compare_teams(team, self.leaderboard[i]) < 0:
                    self.leaderboard.insert(i, team)#O(1)
                    inserted = True
                    break
            if not inserted:
                self.leaderboard.append(team)#O(1)



    def _generate_schedule(self) -> ArrayR[ArrayR[Game]]:
        """
        Generates a schedule by generating all possible games between the teams.

        Return:
            ArrayR[ArrayR[Game]]: The schedule of the season.
                The outer array is the weeks in the season.
                The inner array is the games for that given week.

        Complexity:
            Best Case Complexity: O(N^2) where N is the number of teams in the season.
            Worst Case Complexity: O(N^2) where N is the number of teams in the season.
        """
        num_teams: int = len(self.teams)
        weekly_games: list[ArrayR[Game]] = []
        flipped_weeks: list[ArrayR[Game]] = []
        games: list[Game] = []

        # Generate all possible matchups (team1 vs team2, team2 vs team1, etc.)
        for i in range(num_teams):
            for j in range(i + 1, num_teams):
                games.append(Game(self.teams[i], self.teams[j]))

        # Allocate games into each week ensuring no team plays more than once in a week
        week: int = 0
        while games:
            current_week: list[Game] = []
            flipped_week: list[Game] = []
            used_teams: BSet = BSet()

            week_game_no: int = 0
            for game in games[:]:  # Iterate over a copy of the list
                if game.home_team.get_number() not in used_teams and game.away_team.get_number() not in used_teams:
                    current_week.append(game)
                    used_teams.add(game.home_team.get_number())
                    used_teams.add(game.away_team.get_number())

                    flipped_week.append(Game(game.away_team, game.home_team))
                    games.remove(game)
                    week_game_no += 1

            weekly_games.append(ArrayR.from_list(current_week))
            flipped_weeks.append(ArrayR.from_list(flipped_week))
            week += 1

        return ArrayR.from_list(weekly_games + flipped_weeks)
    
    def _compare_teams(self, team1: Team, team2: Team) -> int:

        """
        Compares two teams based on their performance statistics.

        Args:
            team1 (Team): The first team to compare.
            team2 (Team): The second team to compare.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)

        """
        if team1[TeamStats.POINTS] != team2[TeamStats.POINTS]:
            return team2[TeamStats.POINTS] - team1[TeamStats.POINTS]
        elif team1[TeamStats.GOALS_DIFFERENCE] != team2[TeamStats.GOALS_DIFFERENCE]:
            return team2[TeamStats.GOALS_DIFFERENCE] - team1[TeamStats.GOALS_DIFFERENCE]
        elif team1[TeamStats.GOALS_FOR] != team2[TeamStats.GOALS_FOR]:
            return team2[TeamStats.GOALS_FOR] - team1[TeamStats.GOALS_FOR]
        else:
            if team1.get_name() < team2.get_name():
                return -1
            elif team1.get_name() > team2.get_name():
                return 1
            else:
                return 0

    
    def simulate_season(self) -> None:
        """
        Simulates the season.

        Complexity:
            Assume simulate_game is O(1)
            Remember to define your variables and their complexity.
            Best Case Complexity: O(N^4) where N is number of teams participating in the season.
            Worst Case Complexity: O(N^4) where N is number of teams participating in the season.
        """
        from constants import PlayerStats

        #iterate over each week in the schedule
        #O(N) where N is the number of weeks
        for week in self.schedule:
            #O(N) where N is the total number of games
            for game in week:
                result = GameSimulator.simulate(game.home_team, game.away_team)

                home_goals = result['Home Goals']
                away_goals = result['Away Goals']

                home_team = game.home_team
                away_team = game.away_team

                #update games played for all players
                #O(N) for each team, so O(2N) = O(N) per game
                for player in home_team.get_players():
                    player[PlayerStats.GAMES_PLAYED] += 1
                for player in away_team.get_players():
                    player[PlayerStats.GAMES_PLAYED] += 1

                #update goals for and against for the team
                #O(1) for each team
                home_team[TeamStats.GOALS_FOR] += home_goals
                home_team[TeamStats.GOALS_AGAINST] += away_goals

                away_team[TeamStats.GOALS_FOR] += away_goals
                away_team[TeamStats.GOALS_AGAINST] += home_goals

                #update wins, losses, draws, and points
                #O(1) for each team
                if home_goals > away_goals:
                    home_team[TeamStats.WINS] += 1
                    home_team[TeamStats.POINTS] += 3
                    away_team[TeamStats.LOSSES] += 1
                elif home_goals < away_goals:
                    away_team[TeamStats.WINS] += 1
                    away_team[TeamStats.POINTS] += 3
                    home_team[TeamStats.LOSSES] += 1
                else:
                    home_team[TeamStats.DRAWS] += 1
                    away_team[TeamStats.DRAWS] += 1
                    home_team[TeamStats.POINTS] += 1
                    away_team[TeamStats.POINTS] += 1

                #update goal difference
                home_team[TeamStats.GOALS_DIFFERENCE] = (
                    home_team[TeamStats.GOALS_FOR] - home_team[TeamStats.GOALS_AGAINST]
                )
                away_team[TeamStats.GOALS_DIFFERENCE] = (
                    away_team[TeamStats.GOALS_FOR] - away_team[TeamStats.GOALS_AGAINST]
                )

                goal_scorers = result['Goal Scorers']
                goal_assists = result['Goal Assists']
                tackles = result['Tackles']
                interceptions = result['Interceptions']

                #find player by name and update their stats
                def find_and_update_player_stat(player_name, stat_type):
                    #O(N * P) where N is the number of teams and P is the number of players per team
                    for team in self.teams:
                        for player in team.get_players():
                            if player.get_name() == player_name:
                                player[stat_type] += 1
                                return

                #update goals scored
                #O(M * N * P) where M is the number of goal scorers
                if goal_scorers:
                    for player_name in goal_scorers:
                        find_and_update_player_stat(player_name, PlayerStats.GOALS)

                #update assists
                #O(M * N * P) where M is the number of assists
                if goal_assists:
                    for player_name in goal_assists:
                        find_and_update_player_stat(player_name, PlayerStats.ASSISTS)

                #update tackles
                #O(M * N * P) where M is the number of tackles
                if tackles:
                    for player_name in tackles:
                        find_and_update_player_stat(player_name, PlayerStats.TACKLES)

                #update interceptions
                #O(M * N * P) where M is the number of interceptions
                if interceptions:
                    for player_name in interceptions:
                        find_and_update_player_stat(player_name, PlayerStats.INTERCEPTIONS)

        #sort teams using bubble sort
        #O(N^2) where N is the number of teams
        sorted_teams = self._bubble_sort_teams()

        #clear the current leaderboard and add sorted teams
        #O(N) where N is the number of teams
        self.leaderboard = LinkedList()
        for team in sorted_teams:
            self.leaderboard.append(team)



    def _bubble_sort_teams(self):
        """
        sorts teams using bubble sort based on points, goal difference, goals for, and name.

        Complexity:
            Best Case Complexity: O(N^2) where N is the number of teams.
            Worst Case Complexity: O(N^2) where N is the number of teams.
        """
        n = len(self.teams)  #O(N) where is the number of teams
        teams = self.teams

        #quter loop controls the number of passes over the list
        #O(N) where N is the number of teams
        for i in range(n):
            #inner loop goes through the unsorted part of the list and performs adjacent swaps if necessary
            #O(N) for each pass
            for j in range(0, n - i - 1):
                if self._compare_teams(teams[j], teams[j + 1]) > 0:
                    teams[j], teams[j + 1] = teams[j + 1], teams[j]
        return teams


    def delay_week_of_games(self, orig_week: int, new_week: Union[int, None] = None) -> None:
        """
        Delay a week of games from one week to another.

        Args:
            orig_week (int): The original week to move the games from.
            new_week (Union[int, None]): The new week to move the games to. If this is None, it moves the games to the end of the season.

        Complexity:
            Best Case Complexity: O(N) where N is the number of weeks in the schedule.
            Worst Case Complexity: O(N) where N is the number of weeks in the schedule.
        """
        orig_week_games = self.schedule[orig_week - 1]

        #manually remove the week from the schedule
        #O(N) where N is the number of weeks in the schedule
        for i in range(orig_week - 1, len(self.schedule) - 1):
            self.schedule[i] = self.schedule[i + 1]
        self.schedule[len(self.schedule) - 1] = None

        if new_week is None:
            #move games to the end of the season
            for i in range(len(self.schedule)):
                if self.schedule[i] is None:
                    self.schedule[i] = orig_week_games
                    break
        else:
            #insert the games into the specified new week
            #O(N) where N is the number of weeks
            for i in range(len(self.schedule) - 1, new_week - 1, -1):
                self.schedule[i] = self.schedule[i - 1]
            self.schedule[new_week - 1] = orig_week_games

    def get_next_game(self) -> Union[Generator[Game], None]:
        """
        Gets the next game in the season.

        Returns:
            Game: The next game in the season.
            or None if there are no more games left.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(N * G) where N is the number of weeks and G is the average number of games per week.
        """
        #iterate through each week and game
        #O(N * G) where N is the number of weeks and G is the average number of games per week.
        for week_of_games in self.schedule:
            for game in week_of_games:
                yield game  #O(1)
                #use of yield: https://www.geeksforgeeks.org/use-yield-keyword-instead-return-keyword-python/



    def get_leaderboard(self) -> ArrayR[ArrayR[Union[int, str]]]:
        """
        Generates the final season leaderboard.

        Returns:
            ArrayR(ArrayR[ArrayR[Union[int, str]]]):
                Outer array represents each team in the leaderboard
                Inner array consists of 10 elements:
                    - Team name (str)
                    - Games Played (int)
                    - Points (int)
                    - Wins (int)
                    - Draws (int)
                    - Losses (int)
                    - Goals For (int)
                    - Goals Against (int)
                    - Goal Difference (int)
                    - Previous Five Results (ArrayR(str)) where result should be WIN LOSS OR DRAW

        Complexity:
        Best Case Complexity: O(N) where N is the number of teams.
        Worst Case Complexity: O(N) where N is the number of teams.
        """
        leaderboard_array = ArrayR(len(self.leaderboard))

        #iterate over the leaderboard to generate the final array
        #O(N) where N is the number of teams in the leaderboard
        for i in range(len(self.leaderboard)):
            team = self.leaderboard[i]
            leaderboard_array[i] = ArrayR(10)
            leaderboard_array[i][0] = team.get_name()
            leaderboard_array[i][1] = team[TeamStats.GAMES_PLAYED]
            leaderboard_array[i][2] = team[TeamStats.POINTS]
            leaderboard_array[i][3] = team[TeamStats.WINS]
            leaderboard_array[i][4] = team[TeamStats.DRAWS]
            leaderboard_array[i][5] = team[TeamStats.LOSSES]
            leaderboard_array[i][6] = team[TeamStats.GOALS_FOR]
            leaderboard_array[i][7] = team[TeamStats.GOALS_AGAINST]
            leaderboard_array[i][8] = team[TeamStats.GOALS_DIFFERENCE]

            #extract the last five results
            #O(1)
            last_five_results = Team.get_last_five_results(team)
            leaderboard_array[i][9] = last_five_results

        return leaderboard_array

    
    def get_teams(self) -> ArrayR[Team]:
        """
        Returns:
            PlayerPosition (ArrayR(Team)): The teams participating in the season.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        return self.teams


    def __len__(self) -> int:
        """
        Returns the number of teams in the season.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        return len(self.teams)

    def __str__(self) -> str:
        """
        Optional but highly recommended.

        You may choose to implement this method to help you debug.
        However your code must not rely on this method for its functionality.

        Returns:
            str: The string representation of the season object.

        Complexity:
            Analysis not required.
        """
        return ""

    def __repr__(self) -> str:
        """Returns a string representation of the Season object.
        Useful for debugging or when the Season is held in another data structure."""
        return str(self)