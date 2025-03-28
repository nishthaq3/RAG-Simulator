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
    for line in input_text.get("1.0", tk.END).splitlines():
        line = line.strip()
        if line:
            parts = line.split()
            if len(parts) == 2:
                p, r = parts
                edges.append((p, r))
            else:
                output_text.insert(tk.END, f"Invalid edge format: {line}\n")
                return

    # Create RAG and detect deadlock
    rag, process = dd.create_rag(num_processes, num_resources, edges)
    deadlock_cycle = dd.detect_deadlock(rag, process)

    # Clear previous output
    output_text.delete("1.0", tk.END)

    # Draw graph first
    fig, ax = plt.subplots(figsize=(8, 6))
    ax = dd.draw_rag(rag, process, deadlock_cycle, ax)

    plt.margins(0.3)
    ax.set_xlim(-2, 8)
    ax.set_ylim(-num_processes * 3 - 3, num_processes * 3)
    ax.set_title("Resource Allocation Graph (RAG)")
    ax.axis("off")

    # Create frame for graph with black border
    graph_frame = tk.Frame(window, bd=2, relief="solid")  # Black border
    graph_frame.grid(row=6, column=0, columnspan=2, sticky="nsew", pady=10)

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    # Display edges
    output_text.insert(tk.END, f"Edges in graph: {list(rag.edges())}\n\n")

    # System state message
    if deadlock_cycle:
        deadlock_label.config(text="⚠️ Deadlock detected!", fg="red")
        output_text.insert(tk.END, "⚠️ System is NOT in a safe state.\n")
        output_text.insert(tk.END, f"⚠️ Deadlock detected in cycle: {' → '.join(deadlock_cycle)}\n")
    else:
        deadlock_label.config(text="✅ No deadlock detected.", fg="green")
        output_text.insert(tk.END, "✅ System is in a safe state.\n")
        output_text.insert(tk.END, "✅ No deadlock detected.\n")

    # Deadlock resolution (if applicable)
    resolution_text.delete("1.0", tk.END)
    if deadlock_cycle:
        resolution_text.insert(tk.END, dd.suggest_deadlock_resolution(deadlock_cycle, rag))
    else:
        resolution_text.insert(tk.END, "No deadlock detected.")

window = tk.Tk()
window.title("Graphical Simulator")

# Configure row and column weights
window.grid_rowconfigure(6, weight=1)
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)

tk.Label(window, text="Number of Processes:").grid(row=0, column=0)
process_entry = tk.Entry(window, bd=2, relief="solid")  # Black border
process_entry.grid(row=0, column=1)

tk.Label(window, text="Number of Resources:").grid(row=1, column=0)
resource_entry = tk.Entry(window, bd=2, relief="solid")  # Black border
resource_entry.grid(row=1, column=1)

tk.Label(window, text="Number of Edges:").grid(row=2, column=0)
edge_entry = tk.Entry(window, bd=2, relief="solid")  # Black border
edge_entry.grid(row=2, column=1)

tk.Label(window, text="Process-Resource request:").grid(row=3, column=0)
input_text = scrolledtext.ScrolledText(window, height=5, width=30, bd=2, relief="solid")  # Black border
input_text.grid(row=3, column=1)

tk.Button(window, text="Generate Graph", command=run_deadlock_detection).grid(row=4, column=0, columnspan=2)

deadlock_label = tk.Label(window, text="", font=("Arial", 12))
deadlock_label.grid(row=5, column=0, columnspan=2)

output_text = scrolledtext.ScrolledText(window, height=10, width=50, bd=2, relief="solid")  # Black border
output_text.grid(row=7, column=0, columnspan=2)

resolution_text = scrolledtext.ScrolledText(window, height=3, width=50, bd=2, relief="solid")  # Black border
resolution_text.grid(row=8, column=0, columnspan=2)

style = ttk.Style()
style.theme_use("clam")

window.configure(bg="#E3F2FD")  # Soft sky blue background

style.configure("TLabel", font=("Arial", 12), background="#E3F2FD", foreground="#0D47A1")
style.configure("TButton", font=("Arial", 11), background="#1976D2", foreground="white", padding=5)
style.map("TButton", background=[("active", "#42A5F5")])  # Light blue hover

input_text.configure(bg="white", fg="black", insertbackground="black")
output_text.configure(bg="white", fg="black", insertbackground="black")

deadlock_label.configure(font=("Arial", 12, "bold"), background="#E3F2FD", foreground="#E53935")

window.mainloop()
