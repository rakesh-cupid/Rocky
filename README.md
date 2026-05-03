# Rocky 😎

> Relax first. Then act clearly.

A super chill AI companion for the overstimulated generation. Not a meditation teacher, not a guru, not a productivity coach. Just an unbothered AI mate that helps you stop reacting to every thought, feeling, and notification.

**Core vibe:** No unnecessary response.

---

## Deploy to Streamlit Cloud (free, ~10 mins)

### 1. Get your Anthropic API key

- Go to https://console.anthropic.com/
- Sign up / log in → **API Keys** → **Create Key**
- Add a few dollars of credit (Haiku is super cheap — like $1 will get you thousands of conversations)
- Copy the key (starts with `sk-ant-...`)

### 2. Push these files to a public GitHub repo

You already know this flow from your calculator project. Just three files:

```
rocky-ai-relaxer/
├── streamlit_app.py
├── requirements.txt
└── README.md
```

```bash
# in the folder with the files
git init
git add .
git commit -m "Rocky is alive"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/rocky-ai-relaxer.git
git push -u origin main
```

### 3. Deploy on Streamlit Community Cloud

- Go to https://share.streamlit.io/
- Sign in with GitHub
- Click **New app** → pick the repo, branch `main`, main file `streamlit_app.py`
- **Before clicking Deploy**, click **Advanced settings**
- Under **Secrets**, paste:

  ```toml
  ANTHROPIC_API_KEY = "sk-ant-your-actual-key-here"
  ```

- Click **Deploy**

In about 60 seconds you'll have a public URL like `https://rocky-ai-relaxer.streamlit.app` you can share with anyone.

---

## Test it locally first (optional)

```bash
pip install -r requirements.txt

# Create a secrets file
mkdir -p .streamlit
echo 'ANTHROPIC_API_KEY = "sk-ant-your-key"' > .streamlit/secrets.toml

# Run it
streamlit run streamlit_app.py
```

Important: add `.streamlit/secrets.toml` to your `.gitignore` so the key never hits GitHub:

```bash
echo ".streamlit/secrets.toml" >> .gitignore
```

---

## Configuration knobs

In `streamlit_app.py`:

- **Model** — currently `claude-haiku-4-5-20251001` (fast + cheap, perfect for chill chatbot vibes). Swap for `claude-sonnet-4-6` if you want richer responses, or `claude-opus-4-7` for the most intelligent (and most expensive).
- **System prompt** — the whole `SYSTEM_PROMPT` string at the top is Rocky's personality. Tweak it freely.
- **Starter prompts** — the `starters` list in the file controls the suggested buttons.
- **Title / tagline** — `st.title()` and the `.tagline` markdown.

---

## Cost estimate

With Haiku:
- ~$0.001 per conversation turn
- $1 of credit = roughly 1,000 user messages
- Even if you share this with friends and they go nuts, you'll likely spend under $5/month

---

## What Rocky is *not*

Rocky is not a medical tool, therapist, counsellor, or crisis service. The system prompt explicitly handles this — if someone seems at risk, Rocky responds with care and points them toward real-world support.

Bro chill. Ship it. 😎
