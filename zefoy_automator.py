import tkinter as tk
import threading
import requests
import time

# Script with GUI interface for automated interaction control
# Requires 'requests' library: pip install requests

class ZefoyGui:
    def __init__(self, root):
        self.root = root
        self.root.title("Zefoy Controller")
        self.is_running = False
        self.target_url = "https://vt.tiktok.com/ZSCGxYSoC/"
        
        self.btn = tk.Button(root, text="OFF", bg="red", command=self.toggle)
        self.btn.pack(pady=20, padx=50)

    def toggle(self):
        if not self.is_running:
            self.is_running = True
            self.btn.config(text="ON", bg="green")
            self.thread = threading.Thread(target=self.run_automation)
            self.thread.start()
        else:
            self.is_running = False
            self.btn.config(text="OFF", bg="red")

    def run_automation(self):
        session = requests.Session()
        while self.is_running:
            try:
                # Target endpoint for interaction processing
                response = session.post("https://zefoy.com/c2VuZF9mb2xsb3dlcnNfdGlrdG9k", 
                                       data={"url": self.target_url})
                time.sleep(120) 
            except Exception:
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = ZefoyGui(root)
    root.mainloop()
