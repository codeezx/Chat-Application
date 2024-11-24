import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

# Server Configuration
HOST = '127.0.0.1'  # Server's IP address
PORT = 12345        # Server's port


class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Application")

        # Connection to the server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((HOST, PORT))
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))
            self.root.destroy()
            return

        # GUI Layout
        self.chat_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state='disabled')
        self.chat_area.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        self.message_entry = tk.Entry(self.root, font=("Arial", 12))
        self.message_entry.pack(padx=10, pady=5, fill=tk.X, side=tk.LEFT, expand=True)
        self.message_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.root, text="Send", font=("Arial", 12), command=self.send_message)
        self.send_button.pack(padx=5, pady=5, side=tk.RIGHT)

        # Start the thread to receive messages
        self.running = True
        threading.Thread(target=self.receive_messages, daemon=True).start()

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.close_connection)

    def receive_messages(self):
        """Receive messages from the server."""
        while self.running:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    self.chat_area.config(state='normal')
                    self.chat_area.insert(tk.END, message + '\n')
                    self.chat_area.config(state='disabled')
                    self.chat_area.see(tk.END)
            except:
                break

    def send_message(self, event=None):
        """Send a message to the server."""
        message = self.message_entry.get().strip()
        if message:
            try:
                self.client_socket.send(message.encode('utf-8'))
                self.message_entry.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Error", f"Unable to send message: {e}")
                self.close_connection()

    def close_connection(self):
        """Close the connection and exit."""
        self.running = False
        self.client_socket.close()
        self.root.destroy()


# Start the GUI client
if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()

