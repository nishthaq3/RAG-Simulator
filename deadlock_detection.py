import networkx as nx
import matplotlib.patches as patches

def detect_deadlock(rag, process):
    def dfs(node, visited, stack, path):
        visited.add(node)
        stack.add(node)
        path.append(node)

        for neighbor in rag.neighbors(node):
            if neighbor not in visited:
                cycle = dfs(neighbor, visited, stack, path)
                if cycle:
                    return cycle
            elif neighbor in stack:
                cycle_start = path.index(neighbor)
                return path[cycle_start:]

        stack.remove(node)
        path.pop()
        return None

    visited = set()
    stack = set()

    for node in process:
        if node not in visited:
            cycle = dfs(node, visited, stack, [])
            if cycle:
                return cycle

    return None

def create_rag(num_processes, num_resources, edges):
    process = [f'P{i}' for i in range(1, num_processes + 1)]
    resource = [f'R{i}' for i in range(1, num_resources + 1)]

    rag = nx.DiGraph()
    rag.add_nodes_from(process, bipartite=0, color='blue')
    rag.add_nodes_from(resource, bipartite=1, color='red')
    rag.add_edges_from(edges)

    return rag, process

def draw_rag(rag, process, deadlock_cycle, ax):
    pos = {}
    x_pos_process = 0
    x_pos_resource = 5
    y_gap = 3

    for i, p in enumerate(process):
        pos[p] = (x_pos_process, -i * y_gap)

    resource = [node for node, data in rag.nodes(data=True) if data.get('bipartite') == 1]
    for i, r in enumerate(resource):
        pos[r] = (x_pos_resource, -i * y_gap)

    nx.draw_networkx_nodes(rag, pos, nodelist=[node for node, data in rag.nodes(data=True) if data.get('bipartite') == 0], node_color="blue", node_size=1200, node_shape="o", ax=ax)
    nx.draw_networkx_nodes(rag, pos, nodelist=[node for node, data in rag.nodes(data=True) if data.get('bipartite') == 1], node_color="red", node_size=700, node_shape="s", ax=ax)
    nx.draw_networkx_labels(rag, pos, font_size=12, font_color="white", ax=ax)

    for u, v in rag.edges():
        start_pos = pos[u]
        end_pos = pos[v]

        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        length = (dx**2 + dy**2)**0.5
        offset = 0.2
        end_x = end_pos[0] - (dx / length) * offset
        end_y = end_pos[1] - (dy / length) * offset

        if deadlock_cycle and (u, v) in [(deadlock_cycle[i], deadlock_cycle[(i + 1) % len(deadlock_cycle)]) for i in range(len(deadlock_cycle))]:
            arrow_color = "red"
        else:
            arrow_color = "black"

        arrow = patches.FancyArrowPatch(start_pos, (end_x, end_y), arrowstyle="-|>", mutation_scale=20, color=arrow_color, connectionstyle="arc3,rad=0.1")
        ax.add_patch(arrow)

    return ax