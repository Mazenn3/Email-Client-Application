# Email Client Application

A Python-based Email Client Application for the Computer Networks course (Fall 2025).

## Features

- **Send Emails** using SMTP protocol (port 587 SSL)
- **Receive Emails** using IMAP protocol (port 993 SSL)
- **TCP Notification Server** for real-time notifications
- **Push Notifications** using Plyer library
- **Performance Metrics** (time, bytes, packet counts, throughput)
- **GUI Application** using Tkinter
- **Wireshark Analysis Guide** for packet capture

## Project Structure

```
EmailClientProject/
├── email_client.py        # Main email client (console version)
├── email_client_gui.py    # GUI version using Tkinter
├── notification_server.py # TCP notification server
├── wireshark_guide.md     # Wireshark packet analysis guide
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## Installation

1. **Install Python 3.8+** (if not already installed)

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 1. Start the Notification Server

```bash
python notification_server.py
```

The server will listen on `127.0.0.1:9999` for notifications.

### 2. Run the Email Client

**Console Version:**
```bash
python email_client.py
```

**GUI Version:**
```bash
python email_client_gui.py
```

### 3. Using the Application

1. Enter your email credentials (use a test email from mail.tm)
2. Configure server settings (defaults: mail.tm, ports 465/993)
3. Choose an option:
   - **Send Email**: Compose and send an email
   - **Receive Email**: Fetch the latest email from inbox
   - **View Performance**: See metrics for all operations

## Performance Metrics

The application tracks:
- **Time** - Duration of each operation (seconds)
- **Bytes** - Data sent/received
- **Packets** - Estimated packet count (sent/received)
- **Throughput** - Bytes per second

## Wireshark Packet Capture

See `wireshark_guide.md` for detailed instructions on:
- Wireshark filters for each protocol
- TCP 3-way handshake analysis
- SMTP/IMAP packet flow
- Screenshot guidance for your report

### Quick Filters

| Protocol | Filter |
|----------|--------|
| SMTP | `tcp.port == 465 or tcp.port == 587` |
| IMAP | `tcp.port == 993` |
| Notification | `tcp.port == 9999` |
| All | `tcp.port == 465 or tcp.port == 993 or tcp.port == 9999` |

## Technical Details

### Protocols Used

- **SMTP (Simple Mail Transfer Protocol)**: Port 465 (SSL)
- **IMAP (Internet Message Access Protocol)**: Port 993 (SSL)
- **TCP Sockets**: Port 9999 (notification server)

### Libraries Used

- `smtplib` - SMTP email sending
- `imaplib` - IMAP email receiving
- `socket` - TCP notification client/server
- `tkinter` - GUI framework
- `plyer` - Push notifications
- `email` - Email parsing

## Testing with Eathereal

1. Go to [Eathereal](https://Eathereal.email)
2. Create a temporary email account
3. Use the email and password in the application
4. Send emails to yourself or other mail.tm addresses

## Author

Mazen Mohamed Haseeb 2305607 ANU - Computer Networks Fall 2025
