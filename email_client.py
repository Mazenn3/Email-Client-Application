"""
Email Client Application
A Python email client using SMTP (send) and IMAP (receive) protocols.
Course: Computer Networks - Fall 2025
"""

import smtplib
import imaplib
import socket
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import message_from_bytes


# ==================== Push Notification ====================

def show_push_notification(title, message):
    """Show a desktop push notification using Plyer."""
    try:
        from plyer import notification
        notification.notify(title=title, message=message, app_name="Email Client", timeout=2)
    except ImportError:
        print("[!] Plyer not installed. Run: pip install plyer")
    except Exception as e:
        print(f"[!] Notification error: {e}")


# ==================== SMTP - Send Email ====================

def send_email(sender_email, password, recipient_email, subject, body,
               smtp_server="mail.tm", smtp_port=465):
    """Send an email using SMTP. Returns (success, time, bytes, packets_sent, packets_recv)."""
    start_time = time.time()
    bytes_sent = 0
    # SMTP typical packet count: 3 (handshake) + ~8 (SMTP commands/responses) + 4 (close)
    packets_sent = 0
    packets_recv = 0

    try:
        # Create email message
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        msg_string = message.as_string()
        bytes_sent = len(msg_string.encode('utf-8'))

        # Connect to SMTP server
        print(f"[SMTP] Connecting to {smtp_server}:{smtp_port}...")
        
        if smtp_port == 465:
            server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=30)
        else:
            server = smtplib.SMTP(smtp_server, smtp_port, timeout=30)
            server.starttls()
        
        packets_sent += 2  # SYN, ACK
        packets_recv += 1  # SYN-ACK

        # Login and send
        print("[SMTP] Logging in...")
        server.login(sender_email, password)
        packets_sent += 2  # AUTH command + credentials
        packets_recv += 2  # AUTH responses
        
        print("[SMTP] Sending email...")
        server.sendmail(sender_email, recipient_email, msg_string)
        packets_sent += 4  # MAIL FROM, RCPT TO, DATA, message
        packets_recv += 4  # Responses
        
        server.quit()
        packets_sent += 2  # QUIT + FIN
        packets_recv += 2  # Response + FIN-ACK

        time_taken = time.time() - start_time
        print(f"[SMTP] SUCCESS! Time: {time_taken:.3f}s, Bytes: {bytes_sent}")
        print(f"[SMTP] Packets sent: {packets_sent}, received: {packets_recv}")
        return True, time_taken, bytes_sent, packets_sent, packets_recv

    except smtplib.SMTPAuthenticationError:
        print("[SMTP] ERROR: Authentication failed.")
        return False, time.time() - start_time, bytes_sent, packets_sent, packets_recv
    except Exception as e:
        print(f"[SMTP] ERROR: {e}")
        return False, time.time() - start_time, bytes_sent, packets_sent, packets_recv


# ==================== IMAP - Receive Email ====================

def receive_email(email_addr, password, imap_server="mail.tm", imap_port=993):
    """Receive latest email using IMAP. Returns (success, time, bytes, packets_sent, packets_recv, email_data)."""
    start_time = time.time()
    bytes_received = 0
    packets_sent = 0
    packets_recv = 0
    email_data = None

    try:
        # Connect to IMAP server
        print(f"[IMAP] Connecting to {imap_server}:{imap_port}...")
        mail = imaplib.IMAP4_SSL(imap_server, imap_port)
        packets_sent += 2  # SYN, ACK
        packets_recv += 1  # SYN-ACK

        # Login
        print("[IMAP] Logging in...")
        mail.login(email_addr, password)
        packets_sent += 1  # LOGIN command
        packets_recv += 1  # LOGIN response

        # Select inbox
        print("[IMAP] Selecting INBOX...")
        mail.select('INBOX')
        packets_sent += 1  # SELECT command
        packets_recv += 1  # SELECT response

        # Search for all emails
        status, messages = mail.search(None, 'ALL')
        packets_sent += 1  # SEARCH command
        packets_recv += 1  # SEARCH response

        if status != 'OK' or not messages[0]:
            print("[IMAP] No emails found.")
            mail.logout()
            return True, time.time() - start_time, 0, packets_sent, packets_recv, None

        # Get latest email
        email_ids = messages[0].split()
        latest_id = email_ids[-1]

        print("[IMAP] Fetching latest email...")
        status, msg_data = mail.fetch(latest_id, '(RFC822)')
        packets_sent += 1  # FETCH command
        packets_recv += 2  # FETCH response (may be multiple packets for large emails)

        if status != 'OK':
            print("[IMAP] ERROR: Failed to fetch email.")
            mail.logout()
            return False, time.time() - start_time, 0, packets_sent, packets_recv, None

        # Parse email
        raw_email = msg_data[0][1]
        bytes_received = len(raw_email)
        email_msg = message_from_bytes(raw_email)

        # Extract details
        subject = email_msg['Subject'] or "(No Subject)"
        sender = email_msg['From'] or "(Unknown)"

        # Extract body
        body = ""
        if email_msg.is_multipart():
            for part in email_msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    break
        else:
            body = email_msg.get_payload(decode=True).decode('utf-8', errors='ignore')

        # Store email data
        email_data = {"from": sender, "subject": subject, "body": body[:500]}

        mail.logout()
        packets_sent += 2  # LOGOUT + FIN
        packets_recv += 2  # Response + FIN-ACK
        
        time_taken = time.time() - start_time

        # Display email in console
        print("\n" + "="*50)
        print("LATEST EMAIL:")
        print("="*50)
        print(f"From: {sender}")
        print(f"Subject: {subject}")
        print("-"*50)
        print(f"Body: {body[:500]}")
        print("="*50 + "\n")

        print(f"[IMAP] SUCCESS! Time: {time_taken:.3f}s, Bytes: {bytes_received}")
        print(f"[IMAP] Packets sent: {packets_sent}, received: {packets_recv}")
        return True, time_taken, bytes_received, packets_sent, packets_recv, email_data

    except Exception as e:
        print(f"[IMAP] ERROR: {e}")
        return False, time.time() - start_time, bytes_received, packets_sent, packets_recv, None


# ==================== TCP Notification Client ====================

def send_notification(message, host='127.0.0.1', port=9999):
    """Send notification to TCP server. Returns (success, time, bytes, packets_sent, packets_recv)."""
    start_time = time.time()
    bytes_sent = 0
    packets_sent = 0
    packets_recv = 0

    try:
        # Create TCP socket and connect
        print(f"[TCP] Connecting to {host}:{port}...")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        packets_sent += 2  # SYN, ACK
        packets_recv += 1  # SYN-ACK

        # Send message
        message_bytes = message.encode('utf-8')
        bytes_sent = len(message_bytes)
        client_socket.send(message_bytes)
        packets_sent += 1  # DATA packet
        
        client_socket.close()
        packets_sent += 1  # FIN
        packets_recv += 1  # FIN-ACK

        time_taken = time.time() - start_time
        print(f"[TCP] SUCCESS! Sent: '{message}'")
        print(f"[TCP] Packets sent: {packets_sent}, received: {packets_recv}")
        return True, time_taken, bytes_sent, packets_sent, packets_recv

    except ConnectionRefusedError:
        print("[TCP] ERROR: Server not running.")
        return False, time.time() - start_time, bytes_sent, packets_sent, packets_recv
    except Exception as e:
        print(f"[TCP] ERROR: {e}")
        return False, time.time() - start_time, bytes_sent, packets_sent, packets_recv


# ==================== Performance Summary ====================

def print_performance_summary(smtp_metrics, imap_metrics, tcp_metrics):
    """Print performance metrics for all operations."""
    print("\n" + "="*75)
    print("PERFORMANCE SUMMARY")
    print("="*75)
    print(f"{'Operation':<12} {'Time(s)':<9} {'Bytes':<10} {'Pkts Sent':<10} {'Pkts Recv':<10} {'Throughput':<12}")
    print("-"*75)

    metrics_list = [
        ("SMTP", smtp_metrics),
        ("IMAP", imap_metrics),
        ("TCP", tcp_metrics)
    ]

    for name, metrics in metrics_list:
        if metrics[0]:  # success
            time_taken = metrics[1]
            bytes_val = metrics[2]
            pkts_sent = metrics[3]
            pkts_recv = metrics[4]
            throughput = bytes_val / time_taken if time_taken > 0 else 0
            print(f"{name:<12} {time_taken:<9.3f} {bytes_val:<10} {pkts_sent:<10} {pkts_recv:<10} {throughput:<12.2f}")
        else:
            print(f"{name:<12} FAILED")
    
    print("="*75)
    print("\nWIRESHARK FILTERS:")
    print("-"*75)
    print("SMTP:         tcp.port == 465")
    print("IMAP:         tcp.port == 993")
    print("Notification: tcp.port == 9999")
    print("All traffic:  tcp.port == 465 or tcp.port == 993 or tcp.port == 9999")
    print("="*75 + "\n")


# ==================== Main Program ====================

def main():
    """Main function with menu interface."""
    print("\n" + "="*50)
    print("EMAIL CLIENT - Computer Networks")
    print("="*50 + "\n")

    # Initialize metrics: (success, time, bytes, packets_sent, packets_recv)
    smtp_metrics = (False, 0, 0, 0, 0)
    imap_metrics = (False, 0, 0, 0, 0)
    tcp_metrics = (False, 0, 0, 0, 0)

    # Get credentials
    print("Enter your credentials:")
    sender_email = input("Email: ").strip()
    password = input("Password: ").strip()

    # Server settings (use defaults if empty)
    smtp_server = input("SMTP Server [mail.tm]: ").strip() or "mail.tm"
    smtp_port = int(input("SMTP Port [465]: ").strip() or "465")
    imap_server = input("IMAP Server [mail.tm]: ").strip() or "mail.tm"
    imap_port = int(input("IMAP Port [993]: ").strip() or "993")

    while True:
        print("\n" + "="*30)
        print("1. Send Email")
        print("2. Receive Email")
        print("3. View Performance")
        print("4. Exit")
        print("="*30)

        choice = input("Choice: ").strip()

        if choice == '1':
            recipient = input("Recipient: ").strip()
            subject = input("Subject: ").strip()
            body = input("Body: ").strip()

            smtp_metrics = send_email(sender_email, password, recipient, subject, body,
                                       smtp_server, smtp_port)
            if smtp_metrics[0]:
                show_push_notification("Email Sent", "Your email was sent successfully!")
                tcp_metrics = send_notification("Email Sent")
            else:
                show_push_notification("Email Failed", "Failed to send email.")

        elif choice == '2':
            result = receive_email(sender_email, password, imap_server, imap_port)
            # Extract metrics without email_data for storage
            imap_metrics = (result[0], result[1], result[2], result[3], result[4])
            if imap_metrics[0]:
                show_push_notification("Email Received", "New email fetched successfully!")
                tcp_metrics = send_notification("Email Received")
            else:
                show_push_notification("Fetch Failed", "Failed to receive email.")

        elif choice == '3':
            print_performance_summary(smtp_metrics, imap_metrics, tcp_metrics)

        elif choice == '4':
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
