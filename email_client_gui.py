"""
Email Client GUI Application
A graphical interface for the email client using tkinter.
Course: Computer Networks - Fall 2025
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from email_client import send_email, receive_email, send_notification


def show_push_notification(title, message):
    """Show a desktop push notification using Plyer."""
    try:
        from plyer import notification
        notification.notify(title=title, message=message, app_name="Email Client", timeout=2)
    except ImportError:
        print("[!] Plyer not installed. Run: pip install plyer")
    except Exception as e:
        print(f"[!] Notification error: {e}")


class EmailClientGUI:
    """Main GUI class for the email client."""

    def __init__(self, root):
        self.root = root
        self.root.title("Email Client - Computer Networks")
        self.root.geometry("700x650")

        # Style
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)

        self.create_widgets()

    def create_widgets(self):
        """Create all GUI widgets."""
        # Credentials Section
        cred_frame = ttk.LabelFrame(self.main_frame, text="Credentials", padding="5")
        cred_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=5)
        cred_frame.columnconfigure(1, weight=1)

        ttk.Label(cred_frame, text="Email:").grid(row=0, column=0, sticky="w", padx=5)
        self.email_var = tk.StringVar()
        ttk.Entry(cred_frame, textvariable=self.email_var, width=50).grid(row=0, column=1, sticky="ew", padx=5)

        ttk.Label(cred_frame, text="Password:").grid(row=1, column=0, sticky="w", padx=5)
        self.password_var = tk.StringVar()
        ttk.Entry(cred_frame, textvariable=self.password_var, show="*", width=50).grid(row=1, column=1, sticky="ew", padx=5)

        # Server Settings Section
        server_frame = ttk.LabelFrame(self.main_frame, text="Server Settings", padding="5")
        server_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)

        ttk.Label(server_frame, text="SMTP:").grid(row=0, column=0, sticky="w", padx=5)
        self.smtp_server_var = tk.StringVar(value="mail.tm")
        ttk.Entry(server_frame, textvariable=self.smtp_server_var, width=20).grid(row=0, column=1, padx=5)
        ttk.Label(server_frame, text="Port:").grid(row=0, column=2, padx=5)
        self.smtp_port_var = tk.StringVar(value="465")
        ttk.Entry(server_frame, textvariable=self.smtp_port_var, width=8).grid(row=0, column=3, padx=5)

        ttk.Label(server_frame, text="IMAP:").grid(row=1, column=0, sticky="w", padx=5)
        self.imap_server_var = tk.StringVar(value="mail.tm")
        ttk.Entry(server_frame, textvariable=self.imap_server_var, width=20).grid(row=1, column=1, padx=5)
        ttk.Label(server_frame, text="Port:").grid(row=1, column=2, padx=5)
        self.imap_port_var = tk.StringVar(value="993")
        ttk.Entry(server_frame, textvariable=self.imap_port_var, width=8).grid(row=1, column=3, padx=5)

        # Compose Email Section
        compose_frame = ttk.LabelFrame(self.main_frame, text="Compose Email", padding="5")
        compose_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=5)
        compose_frame.columnconfigure(1, weight=1)

        ttk.Label(compose_frame, text="To:").grid(row=0, column=0, sticky="w", padx=5)
        self.recipient_var = tk.StringVar()
        ttk.Entry(compose_frame, textvariable=self.recipient_var, width=50).grid(row=0, column=1, sticky="ew", padx=5)

        ttk.Label(compose_frame, text="Subject:").grid(row=1, column=0, sticky="w", padx=5)
        self.subject_var = tk.StringVar()
        ttk.Entry(compose_frame, textvariable=self.subject_var, width=50).grid(row=1, column=1, sticky="ew", padx=5)

        ttk.Label(compose_frame, text="Body:").grid(row=2, column=0, sticky="nw", padx=5)
        self.body_text = scrolledtext.ScrolledText(compose_frame, height=4, width=50)
        self.body_text.grid(row=2, column=1, sticky="ew", padx=5, pady=2)

        # Buttons Section
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)

        self.send_btn = ttk.Button(btn_frame, text="Send Email", command=self.send_email_thread)
        self.send_btn.grid(row=0, column=0, padx=10)

        self.receive_btn = ttk.Button(btn_frame, text="Receive Email", command=self.receive_email_thread)
        self.receive_btn.grid(row=0, column=1, padx=10)

        ttk.Button(btn_frame, text="Clear", command=self.clear_output).grid(row=0, column=2, padx=10)

        # Output Section
        output_frame = ttk.LabelFrame(self.main_frame, text="Output", padding="5")
        output_frame.grid(row=4, column=0, columnspan=2, sticky="nsew", pady=5)
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(4, weight=1)

        self.output_text = scrolledtext.ScrolledText(output_frame, height=12)
        self.output_text.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    def log(self, msg):
        """Add message to output."""
        self.output_text.insert(tk.END, msg + "\n")
        self.output_text.see(tk.END)

    def clear_output(self):
        """Clear output area."""
        self.output_text.delete(1.0, tk.END)

    def validate(self, need_recipient=False):
        """Validate required inputs."""
        if not self.email_var.get().strip():
            messagebox.showerror("Error", "Enter your email.")
            return False
        if not self.password_var.get().strip():
            messagebox.showerror("Error", "Enter your password.")
            return False
        if need_recipient and not self.recipient_var.get().strip():
            messagebox.showerror("Error", "Enter recipient email.")
            return False
        return True

    def set_buttons(self, state):
        """Enable or disable buttons."""
        self.send_btn.config(state=state)
        self.receive_btn.config(state=state)

    def send_email_thread(self):
        """Start sending email in background thread."""
        if not self.validate(need_recipient=True):
            return
        self.set_buttons('disabled')
        threading.Thread(target=self.do_send_email, daemon=True).start()

    def do_send_email(self):
        """Perform email sending."""
        self.log("\n" + "="*40 + "\nSENDING EMAIL...\n" + "="*40)

        port = int(self.smtp_port_var.get() or "465")
        success, time_taken, bytes_sent, pkts_sent, pkts_recv = send_email(
            self.email_var.get().strip(),
            self.password_var.get().strip(),
            self.recipient_var.get().strip(),
            self.subject_var.get().strip(),
            self.body_text.get(1.0, tk.END).strip(),
            self.smtp_server_var.get().strip(),
            port
        )

        if success:
            self.log(f"SUCCESS! Time: {time_taken:.3f}s, Bytes: {bytes_sent}")
            self.log(f"Packets sent: {pkts_sent}, received: {pkts_recv}")
            show_push_notification("Email Sent", "Email sent successfully!")
            send_notification("Email Sent")
        else:
            self.log("FAILED to send email.")
            show_push_notification("Failed", "Could not send email.")

        self.root.after(0, lambda: self.set_buttons('normal'))

    def receive_email_thread(self):
        """Start receiving email in background thread."""
        if not self.validate():
            return
        self.set_buttons('disabled')
        threading.Thread(target=self.do_receive_email, daemon=True).start()

    def do_receive_email(self):
        """Perform email receiving."""
        self.log("\n" + "="*40 + "\nRECEIVING EMAIL...\n" + "="*40)

        port = int(self.imap_port_var.get() or "993")
        success, time_taken, bytes_received, pkts_sent, pkts_recv, email_data = receive_email(
            self.email_var.get().strip(),
            self.password_var.get().strip(),
            self.imap_server_var.get().strip(),
            port
        )

        if success:
            self.log(f"SUCCESS! Time: {time_taken:.3f}s, Bytes: {bytes_received}")
            self.log(f"Packets sent: {pkts_sent}, received: {pkts_recv}")
            
            # Display email content in GUI
            if email_data:
                self.log("\n" + "-"*40)
                self.log("LATEST EMAIL:")
                self.log("-"*40)
                self.log(f"From: {email_data['from']}")
                self.log(f"Subject: {email_data['subject']}")
                self.log("-"*40)
                self.log(f"Body:\n{email_data['body']}")
                self.log("-"*40)
            else:
                self.log("No emails in inbox.")
                
            show_push_notification("Email Received", "Email fetched successfully!")
            send_notification("Email Received")
        else:
            self.log("FAILED to receive email.")
            show_push_notification("Failed", "Could not fetch email.")

        self.root.after(0, lambda: self.set_buttons('normal'))


def main():
    """Start the GUI application."""
    root = tk.Tk()
    EmailClientGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
