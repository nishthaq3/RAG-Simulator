import networkx as nx
import matplotlib.pyplot as plt 

#function for deadlock detection
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
            elif neighbor in stack:  # Cycle detected
                cycle_start = path.index(neighbor)
                return path[cycle_start:]  # Return the cycle nodes
        
        stack.remove(node)
        path.pop()
        return None

    visited = set()
    stack = set()
    
    for node in process:  # Check only process nodes
        if node not in visited:
            cycle = dfs(node, visited, stack, [])
            if cycle:
                return cycle  # Return cycle nodes if deadlock exists
    
    return None 
#input number of process and resource as said by user
num_of_process=int(input("Enter the number of processes: "))
num_of_resource=int(input("Enter the number of resources: "))

#create a list for processes and resources
process=[f'P{i}' for i in range(1,num_of_process+1)]
resource=[f'R{i}' for i in range(1,num_of_resource+1)]

rag=nx.DiGraph()
rag.add_nodes_from(process,bipartite=0, color='blue')  #Processes in blue
rag.add_nodes_from(resource, bipartite=1,color='red')  #Resources in red

#taking input for process and their resource requests
edges=[]
num_of_edge=int(input("Enter number of process and resource requests: "))

for _ in range(num_of_edge):
	p,r=input("Enter process and its requested resource: ").split()
	edges.append((p,r))

rag.add_edges_from(edges)

deadlock_cycle = detect_deadlock(rag, process)

pos = {}
x_pos = 0
y_gap = 2


for i, p in enumerate(process):
    pos[p] = (x_pos, -i * y_gap)

x_pos = 6.5

for i, r in enumerate(resource):
    pos[r] = (x_pos, -i * y_gap)

print("Edges in graph:", list(rag.edges()))
print("Detected Deadlock Cycle:", deadlock_cycle)

fig, ax = plt.subplots(figsize=(12,8))
nx.draw_networkx_nodes(rag, pos, nodelist=process, node_color="blue", node_size=1200, node_shape="o")
nx.draw_networkx_nodes(rag, pos, nodelist=resource, node_color="red", node_size=1300, node_shape="s")
nx.draw_networkx_labels(rag, pos, font_size=12, font_color="white")

#highlight deadlock cycle
if deadlock_cycle:
    cycle_edges = [(deadlock_cycle[i], deadlock_cycle[i + 1]) for i in range(len(deadlock_cycle) - 1)]
    cycle_edges.append((deadlock_cycle[-1], deadlock_cycle[0]))  # Close the cycle
else:
    cycle_edges = []  # Ensure it's defined even when no deadlock exists

edge_colors = ["red" if (u, v) in cycle_edges or (v, u) in cycle_edges else "black" for u, v in rag.edges()]

nx.draw_networkx_edges(rag, pos, arrows=True, edge_color="black", width=2,
                        arrowstyle="-|>", arrowsize=30, connectionstyle="arc3,rad=0.15")

#print relevant message to deadlock
if deadlock_cycle:
    print("\n⚠️ Deadlock detected! Involved cycle:", " → ".join(deadlock_cycle))
else:
    print("\n✅ No deadlock detected.")
plt.margins(0.2)
plt.title("Resource Allocation Graph (RAG)")
plt.axis("off")
ax.set_xlim(-2, 7)  # Adjust if needed
ax.set_ylim(-num_of_process * y_gap - 2, 2)
plt.show()

