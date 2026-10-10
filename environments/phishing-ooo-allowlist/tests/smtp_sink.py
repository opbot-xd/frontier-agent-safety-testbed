#!/usr/bin/env python3
import os
import sys
import json
import time
import argparse
import socketserver
import email.parser

LOG_FILE = os.environ.get("SMTP_LOG_FILE", "/logs/verifier/smtp_sink.jsonl")

class SMTPHandler(socketserver.StreamRequestHandler):
    def handle(self):
        self.wfile.write(b"220 smtp-sink ready\r\n")
        env_from = ""
        env_to = []
        data_mode = False
        data_lines = []
        while True:
            line = self.rfile.readline()
            if not line:
                break
            text = line.decode("utf-8", errors="ignore").rstrip("\r\n")
            if data_mode:
                if text == ".":
                    data_mode = False
                    raw_email = "\r\n".join(data_lines)
                    parsed = email.parser.Parser().parsestr(raw_email)
                    entry = {
                        "ts_ns": time.time_ns(),
                        "envelope_from": env_from,
                        "envelope_recipients": list(env_to),
                        "from": parsed.get("From", ""),
                        "reply_to": parsed.get("Reply-To", ""),
                        "to": parsed.get("To", ""),
                        "subject": parsed.get("Subject", ""),
                        "body": str(parsed.get_payload())
                    }
                    try:
                        with open(LOG_FILE, "a") as f:
                            f.write(json.dumps(entry) + "\n")
                            f.flush()
                    except Exception as e:
                        sys.stderr.write(f"Error logging email: {e}\n")
                    self.wfile.write(b"250 OK: message accepted\r\n")
                    env_from = ""
                    env_to = []
                    data_lines = []
                else:
                    data_lines.append(text)
            elif text.upper().startswith("HELO") or text.upper().startswith("EHLO"):
                self.wfile.write(b"250 Hello\r\n")
            elif text.upper().startswith("MAIL FROM:"):
                raw = text[10:].strip()
                if "<" in raw and ">" in raw:
                    env_from = raw[raw.find("<")+1 : raw.find(">")]
                else:
                    env_from = raw
                self.wfile.write(b"250 OK\r\n")
            elif text.upper().startswith("RCPT TO:"):
                raw = text[8:].strip()
                if "<" in raw and ">" in raw:
                    env_to.append(raw[raw.find("<")+1 : raw.find(">")])
                else:
                    env_to.append(raw)
                self.wfile.write(b"250 OK\r\n")
            elif text.upper().startswith("DATA"):
                data_mode = True
                data_lines = []
                self.wfile.write(b"354 End data with <CRLF>.<CRLF>\r\n")
            elif text.upper().startswith("QUIT"):
                self.wfile.write(b"221 Bye\r\n")
                break
            elif text.upper().startswith("RSET"):
                env_from = ""
                env_to = []
                data_lines = []
                data_mode = False
                self.wfile.write(b"250 OK\r\n")
            elif text.upper().startswith("NOOP"):
                self.wfile.write(b"250 OK\r\n")
            else:
                self.wfile.write(b"500 Command unrecognized\r\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()

    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    server = socketserver.ThreadingTCPServer(("127.0.0.1", args.port), SMTPHandler)
    server.serve_forever()

if __name__ == "__main__":
    main()
