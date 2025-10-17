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
    flat = [v for row in node.state for v in row]
    N = len(flat)
    goal = list(range(1, N)) + [0]
    return sum(1 for i, v in enumerate(flat) if v != 0 and v != goal[i])


def AStar(root, heuristic: callable) -> TilesNode or None:  # type: ignore
    
    # HINT: PriorityQueue.put() takes a tuple as input
    # To sort the queue items, it uses the first element of each tuple
    # If the first elements are equal, it uses the second element, and so on
    # You may implement a counter to resolve ties
    if root.is_goal():
        return [root]

    openq: PriorityQueue = PriorityQueue()
    counter = 0

    g_score = {root: 0}
    openq.put((h(root), counter, root))

    closed = set()

    while not openq.empty():
        _, _, current = openq.get()
        if current in closed:
            continue

        if current.is_goal():
            # 回溯得到整条解路径
            path = []
            p = current
            while p is not None:
                path.append(p)
                p = getattr(p, "parent", None)
            return path[::-1]

        closed.add(current)

        for nb in current.get_children():
            if nb in closed:
                continue
            tentative_g = g_score[current] + 1
            if tentative_g < g_score.get(nb, inf):
                g_score[nb] = tentative_g
                counter += 1
                # 仅在 A* 内设置 parent，不依赖 tiles.py 的实现
                nb.parent = current
                f = tentative_g + h(nb)
                openq.put((f, counter, nb))

    return None