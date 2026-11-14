import socket
import threading
import queue
import tkinter as tk
from tkinter import scrolledtext

HOST = 'localhost'  # Use '0.0.0.0' or your LAN IP (e.g. 192.168.1.5) to accept remote connections
PORT = 1234

class ServerChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Server Chat")
        self.root.geometry("420x500")
        self.root.minsize(360, 400)

        self.server_socket = None
        self.conn = None
        self.is_connected = False
        self.is_running = True
        self.msg_queue = queue.Queue()

        self._build_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Poll the queue on the Tkinter main thread
        self.root.after(100, self._process_queue)

        # Start server listening on a background thread to keep the GUI responsive
        threading.Thread(target=self._start_server, daemon=True).start()

    def _build_ui(self):
        # Status Bar
        self.status_var = tk.StringVar(value="Status: Initializing server...")
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
            input_frame, text="SEND", bg="#4CAF50", fg="white",
            font=('Helvetica', 10, 'bold'), width=8,
            command=self.send_message, state=tk.DISABLED
        )
        self.send_button.pack(side=tk.RIGHT, fill=tk.BOTH)

    def _start_server(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((HOST, PORT))
            self.server_socket.listen(1)
            self._set_status(f"Listening on {HOST}:{PORT}... Waiting for client connection.")

            conn, addr = self.server_socket.accept()
            self.conn = conn
            self.is_connected = True
            self._set_status(f"Connected to client: {addr[0]}:{addr[1]}")
            self.root.after(0, lambda: self.send_button.config(state=tk.NORMAL))
            self.msg_queue.put(('SYSTEM', f"Client connected from {addr[0]}:{addr[1]}"))

            # Start receiver loop
            self._receive_loop()
        except OSError as e:
            if self.is_running:
                self._set_status(f"Server error: {e}")

    def _receive_loop(self):
        while self.is_running and self.is_connected:
            try:
                data = self.conn.recv(1024)
                if not data:
                    # Remote client closed connection
                    break
                msg = data.decode('utf-8', errors='replace')
                self.msg_queue.put(('CLIENT', msg))
            except (ConnectionResetError, ConnectionAbortedError, OSError):
                break

        self.is_connected = False
        if self.is_running:
            self._set_status("Client disconnected.")
            self.msg_queue.put(('SYSTEM', 'Client disconnected.'))
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
        if not (event.state & 0x1):  # If Shift key is not held down
            self.send_message()
            return "break"  # Prevent default newline

    def send_message(self):
        if not self.is_connected or not self.conn:
            return
        msg = self.textbox.get("1.0", "end-1c").strip()
        if not msg:
            return
        try:
            self.conn.sendall(msg.encode('utf-8'))
            self._append_to_chat("YOU", msg)
            self.textbox.delete("1.0", tk.END)
        except OSError as e:
            self._set_status(f"Send failed: {e}")

    def on_close(self):
        self.is_running = False
        self.is_connected = False
        if self.conn:
            try:
                self.conn.close()
            except OSError:
                pass
        if self.server_socket:
            try:
                self.server_socket.close()
            except OSError:
                pass
        self.root.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    app = ServerChatApp(root)
    root.mainloop()
