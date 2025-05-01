import tkinter as tk
from tkinter import ttk
import gc

class GCMonitor:
    def __init__(self, parent):
        self.parent = parent
        self.running = True
        self.create_widgets()
        self.update_stats()
    
    def create_widgets(self):
        # Control frame
        self.control_frame = ttk.Frame(self.parent)
        self.control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Buttons
        self.collect_btn = ttk.Button(
            self.control_frame,
            text="Run GC",
            command=self.run_gc
        )
        self.collect_btn.pack(side=tk.LEFT, padx=5)
        
        # Stats frame
        self.stats_frame = ttk.Frame(self.parent)
        self.stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # GC stats labels
        self.gc_count_var = tk.StringVar(value="GC Count: 0")
        self.gc_count_label = ttk.Label(
            self.stats_frame,
            textvariable=self.gc_count_var
        )
        self.gc_count_label.pack(side=tk.LEFT, padx=10)
        
        self.gc_threshold_var = tk.StringVar(value="GC Threshold: ")
        self.gc_threshold_label = ttk.Label(
            self.stats_frame,
            textvariable=self.gc_threshold_var
        )
        self.gc_threshold_label.pack(side=tk.LEFT, padx=10)
    
    def run_gc(self):
        collected = gc.collect()
        root = self.parent.winfo_toplevel()
        if hasattr(root, 'status_label'):
            root.status_label.config(text=f"GC collected {collected} objects")
        self.update_stats()
    
    def update_stats(self):
        if not self.parent.winfo_exists() or not self.running:
            return
            
        counts = gc.get_count()
        thresholds = gc.get_threshold()
        
        self.gc_count_var.set(f"GC Count: Gen0={counts[0]}, Gen1={counts[1]}, Gen2={counts[2]}")
        self.gc_threshold_var.set(f"GC Threshold: Gen0={thresholds[0]}, Gen1={thresholds[1]}, Gen2={thresholds[2]}")
        
        # Schedule next update
        self.parent.after(1000, self.update_stats)
    
    def stop(self):
        self.running = False