import tkinter as tk
from tkinter import ttk
import psutil
import threading
import time
from ui.dashboard import Dashboard
from ui.process_tracker import ProcessTracker
from ui.leak_detector import LeakDetector
from ui.gc_monitor import GCMonitor
from ui.settings import Settings

class MemoryTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Memory Allocation Tracker")
        self.geometry("1200x800")
        self.configure(bg="#121212")
        
        # Initialize variables
        self.refresh_interval = 1  # seconds
        self.running = True
        self.dark_mode = True
        self.current_module = None
        
        # Setup UI
        self.create_widgets()
        self.apply_theme()
        
        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self.update_data, daemon=True)
        self.monitor_thread.start()
        
    def create_widgets(self):
        # Header
        self.header = ttk.Frame(self, style="Card.TFrame")
        self.header.pack(fill=tk.X, padx=10, pady=10)
        
        self.title_label = ttk.Label(
            self.header, 
            text="Memory Allocation Tracker", 
            style="Header.TLabel"
        )
        self.title_label.pack(side=tk.LEFT, padx=10)
        
        # Theme toggle button
        self.theme_btn = ttk.Button(
            self.header,
            text="Toggle Theme",
            command=self.toggle_theme
        )
        self.theme_btn.pack(side=tk.RIGHT, padx=10)
        
        # Main container
        self.main_container = ttk.Frame(self)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Left sidebar
        self.sidebar = ttk.Frame(self.main_container, width=200, style="Card.TFrame")
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 5), pady=5)
        
        # Add navigation buttons
        nav_buttons = [
            ("Dashboard", self.show_dashboard),
            ("Process Tracker", self.show_process_tracker),
            ("Leak Detector", self.show_leak_detector),
            ("GC Monitor", self.show_gc_monitor),
            ("Settings", self.show_settings)
        ]
        
        for text, command in nav_buttons:
            btn = ttk.Button(
                self.sidebar, 
                text=text, 
                command=command,
                style="Nav.TButton"
            )
            btn.pack(fill=tk.X, padx=5, pady=5)
        
        # Main content area
        self.content = ttk.Frame(self.main_container, style="Card.TFrame")
        self.content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 10), pady=5)
        
        # Footer
        self.footer = ttk.Frame(self, style="Card.TFrame")
        self.footer.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.status_label = ttk.Label(
            self.footer, 
            text="Ready", 
            style="Status.TLabel"
        )
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        self.last_update_label = ttk.Label(
            self.footer, 
            text="Last update: Never", 
            style="Status.TLabel"
        )
        self.last_update_label.pack(side=tk.RIGHT, padx=10)
        
        # Make status_label accessible to children
        self.content.status_label = self.status_label
        
        # Show dashboard by default
        self.show_dashboard()
    
    def apply_theme(self):
        style = ttk.Style()
        
        if self.dark_mode:
            style.theme_use('clam')
            style.configure('.', background="#121212", foreground="#ffffff")
            style.configure("TFrame", background="#121212")
            style.configure("Card.TFrame", background="#1e1e1e", relief=tk.RAISED)
            style.configure("Header.TLabel", font=('Arial', 14, 'bold'), background="#1e1e1e")
            style.configure("Nav.TButton", background="#2a2a2a", foreground="#ffffff")
            style.configure("Status.TLabel", background="#1e1e1e")
            self.configure(bg="#121212")
        else:
            style.theme_use('clam')
            style.configure('.', background="#f0f0f0", foreground="#000000")
            style.configure("TFrame", background="#f0f0f0")
            style.configure("Card.TFrame", background="#ffffff", relief=tk.RAISED)
            style.configure("Header.TLabel", font=('Arial', 14, 'bold'), background="#ffffff")
            style.configure("Nav.TButton", background="#e0e0e0", foreground="#000000")
            style.configure("Status.TLabel", background="#ffffff")
            self.configure(bg="#f0f0f0")
    
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()
    
    def update_data(self):
        while self.running:
            # Get system memory info
            memory = psutil.virtual_memory()
            
            # Update UI (must be done in main thread)
            self.after(0, self.update_ui, memory)
            
            time.sleep(self.refresh_interval)
    
    def update_ui(self, memory):
        self.last_update_label.config(text=f"Last update: {time.strftime('%H:%M:%S')}")
        # Update other UI elements with new memory data
    
    def show_dashboard(self):
        """Show dashboard view"""
        self.cleanup_current_module()
        self.current_module = Dashboard(self.content)
    
    def show_process_tracker(self):
        """Show process tracker view"""
        self.cleanup_current_module()
        self.current_module = ProcessTracker(self.content)
    
    def show_leak_detector(self):
        """Show leak detector view"""
        self.cleanup_current_module()
        self.current_module = LeakDetector(self.content)
    
    def show_gc_monitor(self):
        """Show GC monitor view"""
        self.cleanup_current_module()
        self.current_module = GCMonitor(self.content)
    
    def show_settings(self):
        """Show settings view"""
        self.cleanup_current_module()
        self.current_module = Settings(self.content)
    
    def cleanup_current_module(self):
        """Clean up the current module before switching views"""
        for widget in self.content.winfo_children():
            widget.destroy()
        
        if self.current_module and hasattr(self.current_module, 'stop'):
            self.current_module.stop()
    
    def on_closing(self):
        """Handle window closing event"""
        self.running = False
        
        # Clean up current module
        if hasattr(self, 'current_module') and hasattr(self.current_module, 'stop'):
            self.current_module.stop()
            
        # Wait for monitoring thread to finish
        if self.monitor_thread.is_alive():
            self.monitor_thread.join()
            
        self.destroy()

if __name__ == "__main__":
    app = MemoryTrackerApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()