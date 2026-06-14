# Shield Akaton

<img width="1688" height="385" alt="image" src="https://github.com/user-attachments/assets/b239b338-1cfc-4362-b299-b8696e1b9454" />
<img width="438" height="302" alt="image" src="https://github.com/user-attachments/assets/c9c4c433-76d8-45b6-8113-a8dec3d1b746" />
<img width="1817" height="868" alt="image" src="https://github.com/user-attachments/assets/9378da01-0667-4b77-b195-63b2e755660b" />

Shield Akaton is a lightweight prototype that combines a Chrome extension, a Flask API, and a React client to surface social posts that may warrant manual review as a generic risk signal.

## Role of the model

The model is not a medical or safety diagnostic tool. Its role is limited to:

- receiving short social text
- producing a generic risk-like score
- flagging content that may deserve human review

The system should be interpreted as an experimental screening aid, not as a definitive judgment about a person.

## Workflow

1. The Chrome extension scans visible post content on Facebook.
2. Each post is sent to the Flask server as JSON.
3. The server runs a Hugging Face-based classifier and returns a generic risk score.
4. The UI displays the result as a provisional signal.
5. Only posts that exceed the configured threshold are stored in SQLite for review.

## Components

- Extension: [chrome extention](chrome%20extention)
- Server: [server](server)
- Client: [client](client)

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
