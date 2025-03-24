import tkinter as tk
from tkinter import ttk, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import deadlock_detection as dd

def run_deadlock_detection():
    num_processes = int(process_entry.get())
    num_resources = int(resource_entry.get())
    num_edges = int(edge_entry.get())

    edges = []
    for _ in range(num_edges):
        p, r = input_text.get("1.0", tk.END).splitlines()[_].split()
        edges.append((p, r))

    rag, process = dd.create_rag(num_processes, num_resources, edges)
    deadlock_cycle = dd.detect_deadlock(rag, process)

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, f"Edges in graph: {list(rag.edges())}\n")
    output_text.insert(tk.END, f"Detected Deadlock Cycle: {deadlock_cycle}\n")

    fig, ax = plt.subplots(figsize=(8, 6))
    ax = dd.draw_rag(rag, process, deadlock_cycle, ax)

    if deadlock_cycle:
        deadlock_label.config(text=f"⚠️ Deadlock detected! Involved cycle: {' → '.join(deadlock_cycle)}", fg="red")
    else:
        deadlock_label.config(text="✅ No deadlock detected.", fg="green")

    plt.margins(0.3)
    ax.set_xlim(-2, 8)
    ax.set_ylim(-num_processes * 3 - 3, num_processes * 3)
    ax.set_title("Resource Allocation Graph (RAG)")
    ax.axis("off")

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().grid(row=6, column=0, columnspan=2)  # Adjust row for graph

window = tk.Tk()
window.title("Deadlock Detection")

tk.Label(window, text="Number of Processes:").grid(row=0, column=0)
process_entry = tk.Entry(window)
process_entry.grid(row=0, column=1)

tk.Label(window, text="Number of Resources:").grid(row=1, column=0)
resource_entry = tk.Entry(window)
resource_entry.grid(row=1, column=1)

tk.Label(window, text="Number of Edges:").grid(row=2, column=0)
edge_entry = tk.Entry(window)
edge_entry.grid(row=2, column=1)

tk.Label(window, text="Edges (Process Resource):").grid(row=3, column=0)
input_text = scrolledtext.ScrolledText(window, height=5, width=30)
input_text.grid(row=3, column=1)

tk.Button(window, text="Run Detection", command=run_deadlock_detection).grid(row=4, column=0, columnspan=2)

deadlock_label = tk.Label(window, text="", font=("Arial", 12))
deadlock_label.grid(row=5, column=0, columnspan=2)  # Place above the graph

output_text = scrolledtext.ScrolledText(window, height=10, width=50)
output_text.grid(row=7, column=0, columnspan=2)  # Adjust row for output

window.mainloop()