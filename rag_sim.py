import networkx as nx
import matplotlib.pyplot as plt 

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
pos = {}
x_pos = 0
y_gap = 2


for i, p in enumerate(process):
    pos[p] = (x_pos, -i * y_gap)

x_pos = 3 

for i, r in enumerate(resource):
    pos[r] = (x_pos, -i * y_gap)

colors = [rag.nodes[n]['color'] for n in rag.nodes]

plt.figure(figsize=(8, 6))
nx.draw_networkx_nodes(rag, pos, nodelist=process, node_color="blue", node_size=2000, node_shape="o")
nx.draw_networkx_nodes(rag, pos, nodelist=resource, node_color="red", node_size=2000, node_shape="s")

nx.draw_networkx_labels(rag, pos, font_size=12, font_color="black")

nx.draw_networkx_edges(
    rag, pos, edge_color="black", arrows=True, arrowsize=20, arrowstyle="-|>",
    width=2, min_source_margin=20, min_target_margin=30, connectionstyle="arc3,rad=0"
)

plt.title("Resource Allocation Graph (RAG)")
plt.axis("off")
plt.show()

