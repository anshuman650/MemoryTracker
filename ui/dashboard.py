import tkinter as tk
from tkinter import ttk
import psutil
import platform
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Dashboard:
    def __init__(self, parent):
        self.parent = parent
        self.running = True
        self.create_widgets()
        self.update_plot()
    
    def create_widgets(self):
        # Memory summary card
        self.summary_card = ttk.Frame(self.parent)
        self.summary_card.pack(fill=tk.X, padx=10, pady=10)
        
        # Memory usage graph
        self.graph_frame = ttk.Frame(self.parent)
        self.graph_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Create matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(6, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)
    
    def update_plot(self):
        if not self.parent.winfo_exists() or not self.running:
            return
            
        memory = psutil.virtual_memory()
        
        # Handle platform differences
        if platform.system() == 'Windows':
            labels = ['Used', 'Free']
            sizes = [memory.used, memory.free]
        else:
            labels = ['Used', 'Free', 'Cached']
            sizes = [memory.used, memory.free, memory.cached]
        
        self.ax.clear()
        self.ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        self.ax.axis('equal')
        self.canvas.draw()
        
        # Schedule next update
        self.parent.after(1000, self.update_plot)
    
    def stop(self):
        self.running = False
        plt.close(self.fig)