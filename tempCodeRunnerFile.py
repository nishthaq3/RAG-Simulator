def show_main_page():
#     global canvas, process_entry, resource_entry, edge_entry, input_text, output_text, resolution_text, graph_frame, deadlock_label

#     for widget in window.winfo_children():
#         widget.destroy()

#     ttk.Label(window, text="Number of Processes:").grid(row=0, column=0)
#     process_entry = tk.Entry(window, bd=2, relief="solid")
#     process_entry.grid(row=0, column=1)

#     ttk.Label(window, text="Number of Resources:").grid(row=1, column=0)
#     resource_entry = tk.Entry(window, bd=2, relief="solid")
#     resource_entry.grid(row=1, column=1)

#     ttk.Label(window, text="Number of Edges:").grid(row=2, column=0)
#     edge_entry = tk.Entry(window, bd=2, relief="solid")
#     edge_entry.grid(row=2, column=1)

#     ttk.Label(window, text="Process-Resource request:").grid(row=3, column=0)
#     input_text = scrolledtext.ScrolledText(window, height=5, width=30, bd=2, relief="solid")
#     input_text.grid(row=3, column=1)

#     ttk.Button(window, text="Generate Graph", command=run_deadlock_detection).grid(row=4, column=0, columnspan=2)

#     deadlock_label = ttk.Label(window, text="", font=("Arial", 12))
#     deadlock_label.grid(row=5, column=0, columnspan=2)

#     graph_frame = tk.Frame(window, bd=2, relief="solid")
#     graph_frame.grid(row=6, column=0, columnspan=2, sticky="nsew", pady=10)

#     output_text = scrolledtext.ScrolledText(window, height=10, width=50, bd=2, relief="solid")
#     output_text.grid(row=7, column=0, columnspan=2)

#     resolution_text = scrolledtext.ScrolledText(window, height=3, width=50, bd=2, relief="solid")
#     resolution_text.grid(row=8, column=0, columnspan=2)

#     style = ttk.Style()
#     style.theme_use("clam")
#     window.configure(bg="#E3F2FD")
#     style.configure("TLabel", font=("Arial", 12), background="#E3F2FD", foreground="#0D47A1")
#     style.configure("TButton", font=("Arial", 11), background="#1976D2", foreground="white", padding=5)
#     style.map("TButton", background=[("active", "#42A5F5")])
#     input_text.configure(bg="white", fg="black", insertbackground="black")
#     output_text.configure(bg="white", fg="black", insertbackground="black")
#     deadlock_label.configure(font=("Arial", 12, "bold"), background="#E3F2FD", foreground="#E53935")

# def show_start_page():
#     for widget in window.winfo_children():
#         widget.destroy()

#     start_label = ttk.Label(window, text="Welcome to the Deadlock Simulator", font=("Arial", 16, "bold"))
#     start_label.pack(pady=20)

#     start_button = ttk.Button(window, text="Start", command=show_main_page)
#     start_button.pack(pady=10)

# show_start_page()