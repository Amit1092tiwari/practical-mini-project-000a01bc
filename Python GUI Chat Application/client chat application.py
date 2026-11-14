import socket
import threading
import queue
import time
import tkinter as tk
from tkinter import scrolledtext

HOST = 'localhost'  # Change to server IP for LAN connections (e.g. 192.168.1.5)
PORT = 1234

class ClientChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Client Chat")
        self.root.geometry("420x500")
        self.root.minsize(360, 400)

        self.client_socket = None
        self.is_connected = False
        self.is_running = True
        self.msg_queue = queue.Queue()

        self._build_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Poll the queue on the Tkinter main thread
        self.root.after(100, self._process_queue)

        # Start connecting in a background thread so the GUI opens immediately
        threading.Thread(target=self._connect_to_server, daemon=True).start()

    def _build_ui(self):
        # Status Bar
        self.status_var = tk.StringVar(value="Status: Connecting to server...")
        self.status_label = tk.Label(
            self.root, textvariable=self.status_var,
            bg='#e0e0e0', anchor='w', padx=8, pady=4, font=('Helvetica', 9)
        )
        self.status_label.pack(side=tk.TOP, fill=tk.X)

        # Chat Log
        self.chatlog = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, state=tk.DISABLED, bg='#f9f9f9', font=('Helvetica', 10)
        )
        self.chatlog.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=(8, 4))

        # Input Frame
        input_frame = tk.Frame(self.root)
        input_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=8, pady=8)

        self.textbox = tk.Text(input_frame, height=3, font=('Helvetica', 10))
        self.textbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))
        self.textbox.bind("<Return>", self._on_enter_pressed)

        self.send_button = tk.Button(
            input_frame, text="SEND", bg="#2196F3", fg="white",
            font=('Helvetica', 10, 'bold'), width=8,
            command=self.send_message, state=tk.DISABLED
        )
        self.send_button.pack(side=tk.RIGHT, fill=tk.BOTH)

    def _connect_to_server(self):
        while self.is_running and not self.is_connected:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self._set_status(f"Attempting to connect to {HOST}:{PORT}...")
                s.connect((HOST, PORT))
                self.client_socket = s
                self.is_connected = True
                self._set_status(f"Connected to server at {HOST}:{PORT}")
                self.root.after(0, lambda: self.send_button.config(state=tk.NORMAL))
                self.msg_queue.put(('SYSTEM', f"Connected to server at {HOST}:{PORT}"))

                # Start receiver loop
                self._receive_loop()
                break
            except (ConnectionRefusedError, OSError):
                self._set_status("Server unavailable. Retrying in 3 seconds...")
                for _ in range(30):
                    if not self.is_running:
                        return
                    time.sleep(0.1)

    def _receive_loop(self):
        while self.is_running and self.is_connected:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                msg = data.decode('utf-8', errors='replace')
                self.msg_queue.put(('SERVER', msg))
            except (ConnectionResetError, ConnectionAbortedError, OSError):
                break

        self.is_connected = False
        if self.is_running:
            self._set_status("Disconnected from server.")
            self.msg_queue.put(('SYSTEM', 'Server disconnected.'))
            self.root.after(0, lambda: self.send_button.config(state=tk.DISABLED))

    def _process_queue(self):
        while not self.msg_queue.empty():
            sender, msg = self.msg_queue.get_nowait()
            self._append_to_chat(sender, msg)
        if self.is_running:
            self.root.after(100, self._process_queue)

    def _append_to_chat(self, sender, msg):
        self.chatlog.config(state=tk.NORMAL)
        if sender == 'SYSTEM':
            self.chatlog.insert(tk.END, f"--- {msg} ---\n")
        else:
            self.chatlog.insert(tk.END, f"{sender}: {msg}\n")
        self.chatlog.config(state=tk.DISABLED)
        self.chatlog.yview(tk.END)

    def _set_status(self, text):
        self.root.after(0, lambda: self.status_var.set(f"Status: {text}"))

    def _on_enter_pressed(self, event):
        if not (event.state & 0x1):
            self.send_message()
            return "break"

    def send_message(self):
        if not self.is_connected or not self.client_socket:
            return
        msg = self.textbox.get("1.0", "end-1c").strip()
        if not msg:
            return
        try:
            self.client_socket.sendall(msg.encode('utf-8'))
            self._append_to_chat("YOU", msg)
            self.textbox.delete("1.0", tk.END)
        except OSError as e:
            self._set_status(f"Send failed: {e}")

    def on_close(self):
        self.is_running = False
        self.is_connected = False
        if self.client_socket:
            try:
                self.client_socket.close()
            except OSError:
                pass
        self.root.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    app = ClientChatApp(root)
    root.mainloop()
