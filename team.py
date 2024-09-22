from __future__ import annotations
from data_structures.referential_array import ArrayR
from constants import GameResult, PlayerPosition, PlayerStats, TeamStats
from player import Player
from typing import Collection, Union, TypeVar
from data_structures.linked_list import LinkedList
from data_structures.hash_table import LinearProbeTable

T = TypeVar("T")


class Team:
    team_counter = 0
    def __init__(self, team_name: str, players: ArrayR[Player]) -> None:
        """
        Constructor for the Team class

        Args:
            team_name (str): The name of the team
            players (ArrayR[Player]): The players of the team

        Returns:
            None

        Complexity:
            Best Case Complexity:
            Worst Case Complexity:
        """
        Team.team_counter += 1
        self.number = Team.team_counter
        self.name = team_name

        self.statistics = LinearProbeTable()
        self.players = LinearProbeTable()

        #initialize statistics and player positions
        for statistic in TeamStats:
            if statistic == TeamStats.LAST_FIVE_RESULTS:
                self.statistics[statistic.value] = LinkedList()
            else:
                self.statistics[statistic.value] = 0

        for position in PlayerPosition:
            self.players[position.value] = LinkedList()

        #add initial players
        for player in players:
            self.add_player(player)
        
        

    def reset_stats(self) -> None:
        """
        Resets all the statistics of the team to the values they were during init.

        Complexity:
            Best Case Complexity:
            Worst Case Complexity:
        """
        for statistic in TeamStats:
            if statistic == TeamStats.LAST_FIVE_RESULTS:
                self.statistics[statistic.value] = LinkedList()
            else:
                self.statistics[statistic.value] = 0

    def add_player(self, player: Player) -> None:
        """
        Adds a player to the team.

        Args:
            player (Player): The player to add

        Returns:
            None

        Complexity:
            Best Case Complexity:
            Worst Case Complexity:
        """
        self.players[player.get_position().value].append(player)


    def remove_player(self, player: Player) -> None:
        """
        Removes a player from the team.

        Args:
            player (Player): The player to remove

        Returns:
            None

        Complexity:
            Best Case Complexity:
            Worst Case Complexity:
        """
        position_players = self.players[player.get_position().value]
        current = position_players.head
        prev = None
        while current:
            if current.item == player:
                if prev:
                    prev.link = current.link
                else:
                    position_players.head = current.link
                position_players.length -= 1
                return
            prev = current  #update prev to the current node
            current = current.link#move on to the next one


    def get_number(self) -> int:
        """
        Returns the number of the team.

        Complexity:
            Analysis not required.
        """
        return self.number
    
    def get_name(self) -> str:
        """
        Returns the name of the team.

        Complexity:
            Analysis not required.
        """
        return self.name
    
    def get_players(self, position: Union[PlayerPosition, None] = None) -> Union[Collection[Player], None]:
        """
        Returns the players of the team that play in the specified position.
        If position is None, it should return ALL players in the team.
        You may assume the position will always be valid.
        Args:
            position (Union[PlayerPosition, None]): The position of the players to return

        Returns:
            Collection[Player]: The players that play in the specified position
            held in a valid data structure provided to you within
            the data_structures folder this includes the ArrayR
            which was previously prohibited.

            None: When no players match the criteria / team has no players

        Complexity:
            Best Case Complexity:
            Worst Case Complexity:
        """
        all_players = LinkedList()
        if position is None:
            for position in PlayerPosition:
                current_position_players = self.players[position.value]
                current_node = current_position_players.head
                while current_node:
                    all_players.append(current_node.item)
                    current_node = current_node.link
            if len(all_players) > 0:
                return all_players
            else:
                return None
        if len(self.players[position.value]) > 0:
            return self.players[position.value]
        else:
            return None

       
    def get_statistics(self):
        """
        Get the statistics of the team

        Returns:
            statistics: The teams' statistics

        Complexity:
            Best Case Complexity:
            Worst Case Complexity:
        """
        return self.statistics

    def get_last_five_results(self) -> Union[Collection[GameResult], None]:
        """
        Returns the last five results of the team.
        If the team has played less than five games,
        return all the result of all the games played so far.

        For example:
        If a team has only played 4 games and they have:
        Won the first, lost the second and third, and drawn the last,
        the array should be an array of size 4
        [GameResult.WIN, GameResult.LOSS, GameResult.LOSS, GameResult.DRAW]

        **Important Note:**
        If this method is called before the team has played any games,
        return None the reason for this is explained in the specefication.

        Returns:
            Collection[GameResult]: The last five results of the team
            or
            None if the team has not played any games.

        Complexity:
            Best Case Complexity:
            Worst Case Complexity:
        """
        results = self.statistics[TeamStats.LAST_FIVE_RESULTS.value]
        if len(results) > 0:
            return results
        else:
            return None

    def get_top_x_players(self, player_stat: PlayerStats, num_players: int) -> list[tuple[int, str, Player]]:
        """
        Note: This method is only required for FIT1054 students only!

        Args:
            player_stat (PlayerStats): The player statistic to use to order the top players
            num_players (int): The number of players to return from this team

        Return:
            list[tuple[int, str, Player]]: The top x players from this team
        Complexity:
            Best Case Complexity:
            Worst Case Complexity:
        """
        raise NotImplementedError

    def __setitem__(self, statistic: TeamStats, value: int) -> None:
        """
        Updates the team's statistics.

        Args:
            statistic (TeamStats): The statistic to update
            value (int): The new value of the statistic

        Complexity:
            Best Case Complexity:
            Worst Case Complexity:
        """
        if statistic in {TeamStats.WINS, TeamStats.LOSSES, TeamStats.DRAWS}:
            if len(self.statistics[TeamStats.LAST_FIVE_RESULTS.value]) >= 5:
                self.statistics[TeamStats.LAST_FIVE_RESULTS.value].delete_at_index(0)

            if statistic == TeamStats.WINS:
                self.statistics[TeamStats.LAST_FIVE_RESULTS.value].append(GameResult.WIN)
            elif statistic == TeamStats.LOSSES:
                self.statistics[TeamStats.LAST_FIVE_RESULTS.value].append(GameResult.LOSS)
            elif statistic == TeamStats.DRAWS:
                self.statistics[TeamStats.LAST_FIVE_RESULTS.value].append(GameResult.DRAW)

        self.statistics[statistic.value] = value

        #update dependent statistics
        self.statistics[TeamStats.GAMES_PLAYED.value] = (
            self.statistics[TeamStats.WINS.value] +
            self.statistics[TeamStats.DRAWS.value] +
            self.statistics[TeamStats.LOSSES.value]
        )

        self.statistics[TeamStats.GOALS_DIFFERENCE.value] = (
            self.statistics[TeamStats.GOALS_FOR.value] -
            self.statistics[TeamStats.GOALS_AGAINST.value]
        )

        self.statistics[TeamStats.POINTS.value] = (
            GameResult.WIN.value * self.statistics[TeamStats.WINS.value] +
            self.statistics[TeamStats.DRAWS.value]
        )


    def __getitem__(self, statistic: TeamStats) -> int:
        """
        Returns the value of the specified statistic.

        Args:
            statistic (TeamStats): The statistic to return

        Returns:
            int: The value of the specified statistic

        Raises:
            ValueError: If the statistic is invalid

        Complexity:
            Best Case Complexity:
            Worst Case Complexity:
        """
        try:
            return self.statistics[statistic.value]
        except KeyError:
            return 0

    def __len__(self) -> int:
        """
        Returns the number of players in the team.

        Complexity:
            Best Case Complexity:
            Worst Case Complexity:
        """
        total_players = 0
        for position in PlayerPosition:
            player_list = self.players[position.value]
            total_players += len(player_list)
        return total_players

    def __str__(self) -> str:
        """
        Optional but highly recommended.

        You may choose to implement this method to help you debug.
        However your code must not rely on this method for its functionality.

        Returns:
            str: The string representation of the team object.

        Complexity:
            Analysis not required.
        """
        return f"Team {self.name} (Number: {self.number})"

    def __repr__(self) -> str:
        """Returns a string representation of the Team object.
        Useful for debugging or when the Team is held in another data structure."""
        return str(self)
