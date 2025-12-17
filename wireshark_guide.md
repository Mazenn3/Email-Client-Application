# Wireshark Packet Capture & Analysis Guide
## Email Client - Computer Networks Fall 2025

---

## 1. Wireshark Filters

Use these filters to capture specific protocol traffic:

| Protocol | Filter | Port |
|----------|--------|------|
| SMTP (SSL) | `tcp.port == 465` | 465 |
| SMTP (STARTTLS) | `tcp.port == 587` | 587 |
| IMAP (SSL) | `tcp.port == 993` | 993 |
| Notification Server | `tcp.port == 9999` | 9999 |

**Combined filter for all traffic:**
```
tcp.port == 465 or tcp.port == 993 or tcp.port == 9999
```

---

## 2. TCP 3-Way Handshake

Every TCP connection starts with a 3-way handshake:

```
Client                    Server
   |                         |
   |-------- SYN ----------->|   (1) Client sends SYN
   |                         |
   |<------ SYN/ACK ---------|   (2) Server responds SYN/ACK
   |                         |
   |-------- ACK ----------->|   (3) Client sends ACK
   |                         |
   |===== Connection Open ===|
```

**What to capture in Wireshark:**
- Look for packets with flags: `[SYN]`, `[SYN, ACK]`, `[ACK]`
- Filter: `tcp.flags.syn == 1`
- Note the sequence numbers changing

---

## 3. SMTP Packet Analysis (Port 465)

### Connection Flow:
```
1. TCP 3-way handshake
2. TLS/SSL handshake (encrypted)
3. AUTH LOGIN (encrypted)
4. MAIL FROM: <sender@email.com>
5. RCPT TO: <recipient@email.com>
6. DATA (email content)
7. QUIT
8. TCP connection close (FIN/ACK)
```

### What you'll see in Wireshark:
- **TLS encrypted**: Content shows as "Application Data"
- Cannot read actual email content (encryption)
- Can see packet sizes and timing

### Screenshot to capture:
1. TCP handshake packets (SYN, SYN/ACK, ACK)
2. TLS Client Hello / Server Hello
3. Application Data packets
4. Connection close (FIN/ACK)

---

## 4. IMAP Packet Analysis (Port 993)

### Connection Flow:
```
1. TCP 3-way handshake
2. TLS/SSL handshake (encrypted)
3. LOGIN username password
4. SELECT INBOX
5. SEARCH ALL
6. FETCH <id> (RFC822)
7. LOGOUT
8. TCP connection close
```

### What you'll see in Wireshark:
- Similar to SMTP - all encrypted with TLS
- "Application Data" packets contain IMAP commands
- Larger packets when fetching email content

### Screenshot to capture:
1. TCP handshake
2. TLS negotiation
3. Data transfer packets (larger ones = email fetch)
4. Connection termination

---

## 5. TCP Notification Analysis (Port 9999)

### Connection Flow:
```
1. TCP 3-way handshake
2. Data: "Email Sent" or "Email Received"
3. TCP connection close (FIN/ACK)
```

### What you'll see in Wireshark:
- **Plain text visible!** (No TLS encryption)
- Can see actual notification message in packet data
- Use "Follow TCP Stream" to see full message

### Screenshot to capture:
1. TCP handshake
2. Data packet with message visible
3. Right-click → Follow → TCP Stream (shows message)

---

## 6. Required Analysis Table

Fill this table for your report:

| Operation | Packets Sent | Packets Received | Bytes TX | Latency (ms) | TLS? |
|-----------|--------------|------------------|----------|--------------|------|
| SMTP Send | ___ | ___ | ___ | ___ | Yes |
| IMAP Fetch | ___ | ___ | ___ | ___ | Yes |
| TCP Notify | ___ | ___ | ___ | ___ | No |

### How to get these values:
1. **Packet count**: Filter by operation, count packets in each direction
2. **Bytes**: Look at "Length" column in Wireshark
3. **Latency**: Time between first SYN and operation complete
4. **TLS**: SMTP/IMAP use SSL, notification server is plain TCP

---

## 7. Step-by-Step Capture Instructions

1. **Start Wireshark** and select your network interface
2. **Start capture** (click shark fin icon)
3. **Apply filter**: `tcp.port == 465 or tcp.port == 993 or tcp.port == 9999`
4. **Start notification server**: `python notification_server.py`
5. **Run email client**: `python email_client.py` or `python email_client_gui.py`
6. **Perform operations** (send email, receive email)
7. **Stop capture** (red square icon)
8. **Analyze packets** and take screenshots

---

## 8. Key Observations for Report

### TLS Encryption:
- SMTP (port 465) and IMAP (port 993) use SSL/TLS
- Packet contents show as "Application Data" (encrypted)
- Cannot see email content, only packet sizes and timing

### Plain TCP:
- Notification server (port 9999) uses plain TCP
- Message content is visible in Wireshark
- Use "Follow TCP Stream" to see complete message

### Performance Metrics:
- Your program measures: time, bytes sent/received
- Wireshark shows: packet count, actual bytes on wire, timing
- Wire bytes > application bytes (due to protocol overhead)
