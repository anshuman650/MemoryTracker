import tkinter as tk
from tkinter import ttk
import psutil
from tkinter import messagebox

class ProcessTracker:
    def __init__(self, parent):
        self.parent = parent
        self.selected_pid = None
        self.create_widgets()
        self.update_process_list()
    
    def create_widgets(self):
        # Process selection frame
        self.selection_frame = ttk.Frame(self.parent, style="Card.TFrame")
        self.selection_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Process list with scrollbars
        self.tree_frame = ttk.Frame(self.selection_frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)
        
        self.tree_scroll = ttk.Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.process_list = ttk.Treeview(
            self.tree_frame, 
            columns=('pid', 'name', 'memory'), 
            show='headings',
            yscrollcommand=self.tree_scroll.set
        )
        self.process_list.heading('pid', text='PID')
        self.process_list.heading('name', text='Name')
        self.process_list.heading('memory', text='Memory (MB)')
        self.process_list.pack(fill=tk.BOTH, expand=True)
        self.tree_scroll.config(command=self.process_list.yview)
        
        # Add refresh button
        self.refresh_btn = ttk.Button(
            self.selection_frame,
            text="Refresh",
            command=self.update_process_list
        )
        self.refresh_btn.pack(side=tk.BOTTOM, pady=5)
    
    def update_process_list(self):
        # Clear existing items
        for item in self.process_list.get_children():
            self.process_list.delete(item)
        
        # Get all processes
        try:
            for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
                try:
                    memory_mb = proc.info['memory_info'].rss / (1024 * 1024)
                    self.process_list.insert(
                        '', 
                        'end', 
                        values=(proc.info['pid'], proc.info['name'], f"{memory_mb:.2f}")
                    )
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get processes: {str(e)}")
        
        # Sort by memory usage
        self.sort_by_memory()
    
    def sort_by_memory(self):
        items = [(self.process_list.set(child, 'memory'), child) 
                for child in self.process_list.get_children()]
        try:
            items.sort(reverse=True, key=lambda x: float(x[0]))
        except ValueError:
            return
        
        for index, (val, child) in enumerate(items):
            self.process_list.move(child, '', index)