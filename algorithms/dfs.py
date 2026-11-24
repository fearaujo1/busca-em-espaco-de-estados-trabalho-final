from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        frontier = [initial]
        shallowest_depth = {initial: 0}
        result = SearchResult(
            solution=None,
            nodes_generated=1,
            max_frontier_size=1,
        )

        while frontier:
            current = frontier.pop()
            depth = current.cost - initial.cost

            if depth > shallowest_depth[current]:
                continue

            if current.is_goal:
                result.solution = current
                result.depth = depth
                return result

            if depth >= self.depth_limit:
                continue

            result.nodes_expanded += 1
            next_depth = depth + 1

            for child in reversed(current.neighbors()):
                previous_depth = shallowest_depth.get(child)

                if previous_depth is not None and previous_depth <= next_depth: 
                    continue

                shallowest_depth[child] = next_depth
                frontier.append(child)
                result.nodes_generated += 1

            result.max_frontier_size = max(result.max_frontier_size, len(frontier))

        return result
