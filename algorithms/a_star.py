import heapq
from itertools import count 
from puzzle.base_search import BaseSearch
from puzzle.state import GOAL_STATE, State
from puzzle.result import SearchResult

GOAL_POSITIONS = {
    tile: divmod(index, 3)
    for index, tile in enumerate(GOAL_STATE)
    if tile != 0
}

class AStar(BaseSearch):

    def __init__(self, heuristic=None):
        self._custom_heuristic = heuristic

    def heuristic(self, state: State) -> int:
        distance = 0

        for index, tile in enumerate(state.tiles):
            if tile == 0:
                continue

            row, column = divmod(index, 3)
            goal_row, goal_column = GOAL_POSITIONS[tile]

            distance += abs(row - goal_row) + abs(column - goal_column)

        return distance

    def search(self, initial: State) -> SearchResult:
        estimate = self.heuristic
        if self._custom_heuristic is not None:
            estimate = self._custom_heuristic
            
        order = count()
        priority = initial.cost + estimate(initial)
        frontier = [(priority, next(order), initial)]
        best_cost = {initial: initial.cost}

        result = SearchResult(
            solution=None, 
            nodes_generated=1,
            max_frontier_size=1,
        )

        while frontier:
            _, _, current = heapq.heappop(frontier)

            if current.cost > best_cost[current]:
                continue 

            if current.is_goal:
                result.solution = current
                result.depth = current.cost - initial.cost
                return result

            result.nodes_expanded += 1 

            for child in current.neighbors():
                previous_cost = best_cost.get(child)

                if previous_cost is not None and previous_cost <= child.cost:
                    continue

                best_cost[child] = child.cost
                priority = child.cost + estimate(child)
                heapq.heappush(frontier, (priority, next(order), child))
                result.nodes_generated += 1

            result.max_frontier_size = max(result.max_frontier_size, len(frontier))

        return result
    
