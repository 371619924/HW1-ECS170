from tiles import TilesNode
from queue import PriorityQueue


def heuristic(node: TilesNode) -> int:
    """
    Evaluate the heuristic value of the current node.
    This implementation simply counts the number of misplaced tiles.

    Returns
    -------
    heuristic_value : int
        The heuristic value of the current node.
    """
    size = len(node.state)
    dist = 0
    for r in range(size):
        for c in range(size):
            val = node.state[r][c]
            if val == 0:
                continue
            goal_r = (val - 1) // size
            goal_c = (val - 1) % size
            dist += abs(goal_r - r) + abs(goal_c - c)
    return dist


def AStar(root, heuristic: callable) -> TilesNode or None:  # type: ignore
    
    # HINT: PriorityQueue.put() takes a tuple as input
    # To sort the queue items, it uses the first element of each tuple
    # If the first elements are equal, it uses the second element, and so on
    # You may implement a counter to resolve ties
    if root.is_goal():
        return [root]

    unexplored = PriorityQueue()
    counter = 0

    g_score = {root: 0}
    f0 = heuristic(root)
    unexplored.put((f0, counter, root))

    explored = set()

    while not unexplored.empty():
        f_curr, _, current = unexplored.get()

        # If this node has already been finalized with a better g, skip
        if current in explored:
            continue

        if current.is_goal():
            return current.get_path()

        explored.add(current)

        curr_g = g_score[current]

        for child in current.get_children():
            tentative_g = curr_g + 1  # each move costs 1

            # If we've already finalized a better path, skip
            if child in explored and tentative_g >= g_score.get(child, inf):
                continue

            # If this path to child is better, record it
            if tentative_g < g_score.get(child, inf):
                child.parent = current  # ensure path reconstruction works
                g_score[child] = tentative_g
                f = tentative_g + heuristic(child)
                counter += 1
                unexplored.put((f, counter, child))

    return None  # return None if no path was found