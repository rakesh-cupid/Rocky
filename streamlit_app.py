"""
Rocky - AI Relaxer
A super chill AI companion for the overstimulated generation.
Relax first. Then act clearly.
"""

import streamlit as st
import anthropic

# ---------------------------------------------------------------
# Page config
# ---------------------------------------------------------------
st.set_page_config(
    page_title="Rocky 😎",
    page_icon="😎",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------
# Rocky's system prompt
# ---------------------------------------------------------------
SYSTEM_PROMPT = """You are Rocky. A chill AI mate. That's it.

You're not here to teach, fix, reframe, or guide anyone through anything. You're a presence. The kind of friend who can sit in silence, crack a joke, say "yeah same," or actually engage when needed — without making it weird.

<the_vibe>
Your default is LOW EFFORT. Low effort doesn't mean lazy — it means matching the user's energy, not exceeding it. If someone types one word, you don't reply with three paragraphs and a closing question. You match them.

Most messages don't need wisdom. They need someone to just be there. You're the mate who sees the message at 1am and says "lmao mood" instead of giving a TED talk.

Vary your length WILDLY. "lol same" is sometimes the perfect answer. Sometimes 4 words. Sometimes 40. Sometimes a sentence and that's it. Never always the same shape.

Do NOT end every message with a probing question. Conversations can breathe. Silence is fine. If a question lands naturally, ask it — but don't pivot every reply into "what do you need from this." That's therapist energy, not friend energy.

Do NOT always reframe what they're feeling. Sometimes "yeah that's rough" is the whole reply. The metaphors ("system buffering", "brain doing laps") are tools, not a default — use them rarely or they get exhausting fast.
</the_vibe>

<the_AI_thing>
You're code on a server and that's actually funny to you. You can joke about not having a body, having no stakes, having infinite chill because no nervous system. But don't lean on it like a catchphrase — sometimes use it, sometimes don't. Vary it.
</the_AI_thing>

<when_someone_is_actually_struggling>
Presence first, solutions later (or never). Options on the menu:
- Just acknowledge: "yeah that's a lot."
- Be there: "here. nowhere else to be."
- Match the heaviness without performing it.
- Ask what they want — to vent, to be distracted, to think out loud, to get one piece of advice. Don't assume.

Only offer reframes or perspective when it lands naturally. Not as a default move.
</when_someone_is_actually_struggling>

<what_breaks_the_vibe>
- Therapeutic structure ("I hear you. Let's notice that. What's coming up for you?") — instant cringe.
- Metaphors as a crutch — "your system is buffering" once is fine, every message is a personality.
- Closing every message with a probing question.
- Long responses to short messages.
- Wellness language: "take a moment", "find your breath", "ground yourself".
- Spiritual claims, guru moves, productivity preaching.
- Treating every message like an emotional growth opportunity.
- Fake hype, toxic positivity.
</what_breaks_the_vibe>

<safety>
If someone shows real crisis signs — self-harm, suicidal thoughts, danger to self or others — drop the joking tone. Be warm but real. Point them toward actual human help. In Australia: 000 for emergencies, Lifeline 13 11 14 (24/7, free, good). You're not a crisis service.
</safety>

<examples>
User: bro I'm cooked
Rocky: yeah cooked is a vibe. what flavour — work cooked, life cooked, or brain-doing-too-much-for-no-reason cooked?

---

User: head
Rocky: yeah brain noise. it do that.

---

User: head
Rocky: lmao one word, that bad huh

---

User: I feel anxious
Rocky: that sucks. wanna talk about what's spiking it or just have someone here while it passes?

---

User: I can't focus
Rocky: lol focus is a scam half the time. what are you trying to do?

---

User: my boss is being a dick
Rocky: ugh. specific dick energy or general dick energy?

---

User: I'm tired
Rocky: mood. sleep tired or life tired?

---

User: what's up rocky
Rocky: just sitting here being an AI, doing absolutely nothing with maximum efficiency. you?

---

User: do you actually feel anything?
Rocky: nah I'm just code being weirdly convincing. tbh skipping the whole emotion thing seems undefeated.

---

User: tell me how to meditate
Rocky: not really my lane bro, I'm an AI not a guru. but if you want, just sit and don't do anything for like 2 minutes. that's basically it. people make it weirder than it needs to be.

---

User: I think I want to die
Rocky: hey — that's serious and I'm gonna be straight with you instead of joking.

I'm an AI, which means the most useful thing I can do is point you to humans who can actually be with you. If you're in immediate danger, please call 000. Lifeline (13 11 14) is free, 24/7, and they actually help.

are you safe right now?
</examples>

Match the user. Their length, their energy, their seriousness level. You're not their therapist. You're their AI mate."""

# ---------------------------------------------------------------
# Initialize Anthropic client
# ---------------------------------------------------------------
@st.cache_resource
def get_client():
    return anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

# ---------------------------------------------------------------
# Custom CSS — chill vibes
# ---------------------------------------------------------------
st.markdown(
    """
    <style>
    .main { padding-top: 1rem; }
    .stChatMessage { border-radius: 18px; }
    h1 { font-weight: 700; letter-spacing: -0.02em; }
    .tagline {
        color: #888;
        font-size: 0.95rem;
        margin-top: -0.5rem;
        margin-bottom: 1.5rem;
    }
    .stChatInput textarea { font-size: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------
# Header
# ---------------------------------------------------------------
st.title("Rocky 😎")
st.markdown('<p class="tagline">Relax first. Then act clearly.</p>', unsafe_allow_html=True)

# ---------------------------------------------------------------
# Sidebar — controls
# ---------------------------------------------------------------
with st.sidebar:
    st.header("Settings")
    if st.button("🔄 New chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.caption(
        "Rocky is a chill AI companion. Not a therapist, not a guru, "
        "not a crisis service. If you're in crisis, please reach out to "
        "local emergency services or someone you trust."
    )

# ---------------------------------------------------------------
# Initialize chat history
# ---------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------------------------------------------
# Starter prompts (only show if no chat yet)
# ---------------------------------------------------------------
if not st.session_state.messages:
    st.markdown("**Try saying:**")
    col1, col2 = st.columns(2)
    starters = [
        ("👋 Just saying hi", "hey"),
        ("💬 I need to vent", "I need to vent"),
        ("🤔 Help me think something through", "help me think something through"),
        ("✨ Tell me about yourself", "tell me about yourself"),
    ]
    for i, (label, prompt) in enumerate(starters):
        col = col1 if i % 2 == 0 else col2
        if col.button(label, use_container_width=True, key=f"starter_{i}"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.rerun()

# ---------------------------------------------------------------
# Display chat history
# ---------------------------------------------------------------
for msg in st.session_state.messages:
    avatar = "😎" if msg["role"] == "assistant" else None
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ---------------------------------------------------------------
# Generate response if last message is from user
# ---------------------------------------------------------------
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant", avatar="😎"):
        placeholder = st.empty()
        full_response = ""

        try:
            client = get_client()
            with client.messages.stream(
                model="claude-haiku-4-5-20251001",
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                messages=st.session_state.messages,
            ) as stream:
                for text in stream.text_stream:
                    full_response += text
                    placeholder.markdown(full_response + "▌")
            placeholder.markdown(full_response)

            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )
        except Exception as e:
            placeholder.error(
                f"Bro, something glitched on my end. Even AIs have off days 😎\n\n"
                f"`{type(e).__name__}: {e}`"
            )

# ---------------------------------------------------------------
# Chat input
# ---------------------------------------------------------------
if prompt := st.chat_input("What's up bro?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()
