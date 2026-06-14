# Social Risk Scanner
<img width="450" height="450" alt="image" src="https://github.com/user-attachments/assets/cf22926f-d202-4a2c-a030-cfa7461c33e4" />    <td align="center" style="font-size:1800px; font-weight:12000; padding:0 40px;"> ➜ </td><img width="450" height="450" alt="image" src="https://github.com/user-attachments/assets/a852b136-4528-4374-9560-28a32fc2f23d"  />



---

## Overview

Social Risk Scanner is a full-stack prototype that analyzes social media text and produces a **provisional risk signal** for manual review.

The system is composed of:
- Chrome Extension (data collection)
- Flask Backend (ML inference + decision layer)
- React Dashboard (review UI)

---

## Chrome Extension

<img width="438" height="302" alt="extension preview" src="https://github.com/user-attachments/assets/c9c4c433-76d8-45b6-8113-a8dec3d1b746" />

### Responsibilities
- Extract post content from Facebook DOM
- Capture username + metadata
- Send structured JSON to backend
- Trigger real-time analysis per post

---

## Backend (Flask + Hugging Face)

### Core Responsibilities
- REST API endpoint
- Run Hugging Face model (`sentinet/suicidality`)
- Convert raw output into structured risk signal
- Store only high-risk posts in SQLite

### Model Output
- `label` (LABEL_0 / LABEL_1)
- `score` (confidence)
---

## Client (React Dashboard)

<img width="1817" height="868" alt="client preview" src="https://github.com/user-attachments/assets/9378da01-0667-4b77-b195-63b2e755660b" />

### Features
- Fetch review items from backend
- Display risk score per post
- Color-coded risk levels
- Summary dashboard (total / flagged)

---

## Workflow

<img width="782" height="537" alt="image" src="https://github.com/user-attachments/assets/3424a89e-8925-4e56-ba7b-1c9b366dcde7" />

## How to run

### Server

```bash
cd server
pip install -r requirements.txt
python server.py
```

### Client

```bash
cd client
npm install
npm run dev -- --host 0.0.0.0
```

### Chrome extension

1. Open Chrome and go to chrome://extensions.
2. Enable Developer mode.
3. Click Load unpacked and select the [chrome extention](chrome%20extention) folder.
4. Open Facebook, click the extension icon, and run Scan now.

## Notes

- The current prototype stores posts in a local SQLite database.
- The threshold is intentionally conservative and only keeps entries that meet the high-risk criteria.
- The server uses the Hugging Face model `sentinet/suicidality`.
