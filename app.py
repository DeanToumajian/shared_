import tkinter as tk
from tkinter import ttk
import requests
import threading

SERVER_URL = "https://your-app-name.onrender.com"  # <-- Replace with your actual hosted Flask URL

class StatusApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Shared Status")

        self.user = None
        self.partner = None

        self.setup_user_selection()

    def setup_user_selection(self):
        self.select_frame = tk.Frame(self.root)
        self.select_frame.pack(pady=30)

        tk.Label(self.select_frame, text="Who are you?").pack(pady=10)

        tk.Button(self.select_frame, text="Dean", font=("UnifrakturCook", 20), command=lambda: self.start_app("dean")).pack(pady=5)
        tk.Button(self.select_frame, text="Jenn", font=("Dancing Script", 20), command=lambda: self.start_app("jenn")).pack(pady=5)

    def start_app(self, user):
        self.user = user
        self.partner = "jenn" if user == "dean" else "dean"
        self.select_frame.destroy()
        self.build_main_ui()
        self.fetch_loop()

    def build_main_ui(self):
        self.status_var = tk.StringVar()
        self.message_var = tk.StringVar()

        # Status selection
        tk.Label(self.root, text="Your Status:").pack()
        status_options = ["Online", "Do not disturb", "Busy", "Away", "On phone", "Text me"]
        self.status_menu = ttk.Combobox(self.root, textvariable=self.status_var, values=status_options, state="readonly")
        self.status_menu.pack()
        self.status_menu.bind("<<ComboboxSelected>>", self.send_status_only)

        # Message box
        tk.Label(self.root, text="Your Message:").pack()
        self.message_entry = tk.Entry(self.root, textvariable=self.message_var, width=50)
        self.message_entry.pack(pady=5)

        tk.Button(self.root, text="Send", command=self.send_message).pack(pady=5)

        # Partner status
        self.partner_status_label = tk.Label(self.root, text=f"{self.partner.title()}'s Status: Loading...")
        self.partner_status_label.pack(pady=10)

        # Messages
        tk.Label(self.root, text=f"{self.partner.title()}'s Messages:").pack()
        self.message_box = tk.Text(self.root, height=15, width=60, state="disabled", bg="#f9f9f9")
        self.message_box.pack(pady=5)

    def send_message(self):
        status = self.status_var.get()
        message = self.message_var.get()

        if not message.strip():
            return

        try:
            requests.post(f"{SERVER_URL}/update/{self.user}", json={
                "status": status,
                "message": message
            })
        except Exception as e:
            print("Failed to send message:", e)

        self.message_var.set("")  # Clear input

    def send_status_only(self, event=None):
        status = self.status_var.get()

        try:
            requests.post(f"{SERVER_URL}/update/{self.user}", json={
                "status": status,
                "message": ""
            })
        except Exception as e:
            print("Failed to update status:", e)

    def fetch_loop(self):
        def loop():
            while True:
                try:
                    response = requests.get(f"{SERVER_URL}/get/{self.user}")
                    data = response.json()

                    # Update partner's status
                    self.partner_status_label.config(text=f"{self.partner.title()}'s Status: {data['status']}")

                    # Update messages
                    self.message_box.config(state="normal")
                    self.message_box.delete("1.0", tk.END)
                    for msg in data["messages"]:
                        self.message_box.insert(tk.END, f"{msg['timestamp']}: {msg['text']}\n")
                    self.message_box.config(state="disabled")
                except Exception as e:
                    print("Error fetching data:", e)

                self.root.after(3000, self.fetch_loop)
                break

        threading.Thread(target=loop).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = StatusApp(root)
    root.mainloop()