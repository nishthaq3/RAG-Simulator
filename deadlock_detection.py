import networkx as nx
import matplotlib.patches as patches
import openai

openai.api_key = "PLEASE GIVE YOUR API KEY"
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

def suggest_deadlock_resolution(deadlock_cycle, rag):
    if not deadlock_cycle:
        return "No deadlock detected."

    edges_in_cycle = [(deadlock_cycle[i], deadlock_cycle[(i + 1) % len(deadlock_cycle)]) for i in range(len(deadlock_cycle))]
    edge_to_break = edges_in_cycle[0]  # Default: Break the first edge

    # Simple AI: Prioritize breaking edges involving resources with more requests
    resource_counts = {}
    for u, v in rag.edges():
        if v.startswith("R"):  # If the edge points to a resource
            resource_counts[v] = resource_counts.get(v, 0) + 1

    best_edge = None
    best_count = 0
    for u, v in edges_in_cycle:
        if v.startswith("R") and resource_counts.get(v, 0) > best_count:
            best_edge = (u, v)
            best_count = resource_counts.get(v, 0)

    if best_edge:
        edge_to_break = best_edge

    # Use LLM to generate human-readable suggestion
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Given a deadlock cycle {deadlock_cycle} in a resource allocation graph, suggest a human-readable resolution. For example, 'To prevent deadlock, consider releasing resource R1, currently held by process P1, as this resource is requested by process P2, which is part of a cycle.'",
            max_tokens=100
        )
        llm_suggestion = response.choices[0].text.strip()
    except Exception as e:
        llm_suggestion = f"To resolve the deadlock, consider breaking the edge: {edge_to_break[0]} -> {edge_to_break[1]}"

    return llm_suggestion