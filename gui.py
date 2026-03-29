import tkinter as tk

def run_gui(engine):

    def search():
        query = entry.get()
        result = engine.process_query(query)

        listbox.delete(0, tk.END)

        for doc in sorted(result):
            listbox.insert(tk.END, doc)

        result_label.config(text=f"Results: {len(result)} documents found")

    def show_preview(event):
        selected = listbox.curselection()
        if not selected:
            return

        doc_id = listbox.get(selected[0])

        try:
            with open(f"documents/{doc_id}.txt", "r", encoding="utf-8") as f:
                content = f.read()
        except:
            content = "File not found"

        preview.delete("1.0", tk.END)
        preview.insert(tk.END, content[:1000])

    root = tk.Tk()
    root.title("Boolean IR System")

    example_frame = tk.Frame(root)
    example_frame.pack()

    def set_query(q):
        entry.delete(0, tk.END)
        entry.insert(0, q)

    tk.Button(example_frame, text="AND", command=lambda: set_query("trump AND america")).pack(side=tk.LEFT)
    tk.Button(example_frame, text="OR", command=lambda: set_query("trump OR america")).pack(side=tk.LEFT)
    tk.Button(example_frame, text="NOT", command=lambda: set_query("trump NOT america")).pack(side=tk.LEFT)
    tk.Button(example_frame, text="/5", command=lambda: set_query("trump /5 speech")).pack(side=tk.LEFT)

    entry = tk.Entry(root, width=50)
    entry.pack()

    btn = tk.Button(root, text="Search", command=search)
    btn.pack()
    result_label = tk.Label(root, text="Results: 0 documents found")
    result_label.pack()

    listbox = tk.Listbox(root, width=50, height=15)
    listbox.pack()
    listbox.bind("<<ListboxSelect>>", show_preview)

    preview = tk.Text(root, height=10, width=60)
    preview.pack()

    root.mainloop()