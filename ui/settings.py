import tkinter as tk
from tkinter import ttk

class Settings:
    def __init__(self, parent):
        self.parent = parent
        self.create_widgets()
    
    def create_widgets(self):
        # Settings frame
        self.settings_frame = ttk.Frame(self.parent, style="Card.TFrame")
        self.settings_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Refresh interval setting
        self.refresh_label = ttk.Label(
            self.settings_frame,
            text="Refresh Interval (seconds):"
        )
        self.refresh_label.pack(pady=(10, 0))
        
        self.refresh_slider = ttk.Scale(
            self.settings_frame,
            from_=0.5,
            to=5,
            value=1
        )
        self.refresh_slider.pack(fill=tk.X, padx=20)
        
        # Alert threshold setting
        self.alert_label = ttk.Label(
            self.settings_frame,
            text="Memory Alert Threshold (%):"
        )
        self.alert_label.pack(pady=(20, 0))
        
        self.alert_slider = ttk.Scale(
            self.settings_frame,
            from_=70,
            to=95,
            value=85
        )
        self.alert_slider.pack(fill=tk.X, padx=20)
        
        # Save button
        self.save_btn = ttk.Button(
            self.settings_frame,
            text="Save Settings",
            command=self.save_settings
        )
        self.save_btn.pack(pady=20)
    
    def save_settings(self):
        # In a real implementation, this would save to a config file
        new_interval = round(self.refresh_slider.get(), 1)
        new_threshold = int(self.alert_slider.get())
        
        self.parent.master.refresh_interval = new_interval
        self.parent.master.status_label.config(text=f"Settings saved - Refresh: {new_interval}s, Alert: {new_threshold}%")
