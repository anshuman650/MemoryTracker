import tkinter as tk
from tkinter import ttk
import tracemalloc

class LeakDetector:
    def __init__(self, parent):
        self.parent = parent
        self.snapshots = []
        self.create_widgets()
    
    def create_widgets(self):
        # Control frame
        self.control_frame = ttk.Frame(self.parent, style="Card.TFrame")
        self.control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Buttons
        self.start_btn = ttk.Button(
            self.control_frame,
            text="Start Tracing",
            command=self.start_tracing
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.snapshot_btn = ttk.Button(
            self.control_frame,
            text="Take Snapshot",
            command=self.take_snapshot
        )
        self.snapshot_btn.pack(side=tk.LEFT, padx=5)
        
        self.compare_btn = ttk.Button(
            self.control_frame,
            text="Compare Snapshots",
            command=self.compare_snapshots
        )
        self.compare_btn.pack(side=tk.LEFT, padx=5)
        
        # Results frame
        self.results_frame = ttk.Frame(self.parent, style="Card.TFrame")
        self.results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Results text
        self.results_text = tk.Text(
            self.results_frame,
            wrap=tk.WORD,
            bg="#1e1e1e",
            fg="#ffffff",
            insertbackground="white"
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)
    
    def start_tracing(self):
        tracemalloc.start()
        self.results_text.insert(tk.END, "Memory tracing started\n")
    
    def take_snapshot(self):
        snapshot = tracemalloc.take_snapshot()
        self.snapshots.append(snapshot)
        self.results_text.insert(tk.END, f"Snapshot #{len(self.snapshots)} taken\n")
    
    def compare_snapshots(self):
        if len(self.snapshots) < 2:
            self.results_text.insert(tk.END, "Need at least 2 snapshots to compare\n")
            return
        
        stats = self.snapshots[-1].compare_to(self.snapshots[-2], 'lineno')
        self.results_text.insert(tk.END, "\nMemory allocation differences:\n")
        
        for stat in stats[:10]:  # Show top 10 differences
            self.results_text.insert(tk.END, f"{stat}\n")
