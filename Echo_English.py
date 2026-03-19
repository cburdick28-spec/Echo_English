import streamlit as st

st.set_page_config(
    page_title="Echo English",
    page_icon="🔊",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Karla:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'Karla', sans-serif; }

.stApp { background: #f5f0e8; color: #1a1a1a; }

/* Hide sidebar entirely */
[data-testid="stSidebar"] { display: none; }
[data-testid="collapsedControl"] { display: none; }

h1 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    font-size: 3rem !important;
    line-height: 1.1 !important;
    color: #1a1a1a !important;
}
h2, h3 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    color: #1a1a1a !important;
}

/* Sticky nav bar */
.navbar {
    position: sticky;
    top: 0;
    z-index: 999;
    background: #1a1a1a;
    padding: 12px 40px;
    display: flex;
    align-items: center;
    gap: 32px;
    margin-bottom: 0;
}
.navbar a {
    color: #f5f0e8;
    text-decoration: none;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.78rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    opacity: 0.7;
    transition: opacity 0.2s;
}
.navbar a:hover { opacity: 1; }
.navbar-brand {
    color: #e85d2f !important;
    opacity: 1 !important;
    font-size: 1rem !important;
    margin-right: 16px;
}

.section-wrap {
    padding: 64px 48px;
    border-bottom: 2px solid #d0c8b8;
}
.section-wrap:last-child { border-bottom: none; }

.hero-badge {
    background: #e85d2f;
    color: white;
    display: inline-block;
    padding: 6px 16px;
    font-family: 'Syne', sans-serif;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 16px;
}

.divider {
    border: none;
    border-top: 2px solid #1a1a1a;
    margin: 32px 0;
}

.step-card {
    background: #ffffff;
    border-left: 5px solid #e85d2f;
    padding: 28px 32px;
    margin-bottom: 24px;
    box-shadow: 4px 4px 0px #1a1a1a;
}

.step-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #e85d2f;
    margin-bottom: 6px;
}

.step-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 800;
    color: #1a1a1a;
    margin-bottom: 16px;
}

.answer-block {
    background: #f5f0e8;
    padding: 14px 18px;
    margin: 10px 0;
    font-size: 0.95rem;
    line-height: 1.6;
    border-bottom: 2px solid #1a1a1a;
}

.big-number {
    font-family: 'Syne', sans-serif;
    font-size: 5rem;
    font-weight: 800;
    color: #e85d2f;
    opacity: 0.15;
    line-height: 1;
    position: absolute;
    top: 10px;
    right: 20px;
}

.level-card {
    background: #fff;
    border: 2px solid #1a1a1a;
    padding: 24px 20px;
    box-shadow: 4px 4px 0px #1a1a1a;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 20px;
}

.vocab-word {
    background: #1a1a1a;
    color: #f5f0e8;
    display: inline-block;
    padding: 6px 14px;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.9rem;
    margin: 4px 4px 4px 0;
}

.phrase-box {
    background: #f5f0e8;
    border-left: 4px solid #e85d2f;
    padding: 12px 16px;
    margin: 8px 0;
    font-size: 0.95rem;
    line-height: 1.5;
}

.lesson-card {
    background: #fff;
    border: 2px solid #1a1a1a;
    padding: 20px 24px;
    margin-bottom: 16px;
    box-shadow: 3px 3px 0px #1a1a1a;
}

.competitor-card {
    background: #fff;
    border: 2px solid #1a1a1a;
    padding: 16px 20px;
    margin: 8px 0;
    box-shadow: 3px 3px 0px #1a1a1a;
}

.reflection-box {
    background: #1a1a1a;
    color: #f5f0e8;
    padding: 28px 32px;
    margin-top: 8px;
    font-size: 1rem;
    line-height: 1.7;
    font-style: italic;
}

div[data-testid="stButton"] button {
    background: #e85d2f !important;
    color: white !important;
    border: none !important;
    border-radius: 0 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    padding: 10px 24px !important;
    box-shadow: 3px 3px 0px #1a1a1a !important;
}

[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Sticky Nav ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="navbar">
  <a class="navbar-brand" href="#home">🔊 Echo English</a>
  <a href="#about">About</a>
  <a href="#level-1">Level 1</a>
  <a href="#level-2">Level 2</a>
  <a href="#level-3">Level 3</a>
  <a href="#level-4">Level 4</a>
  <a href="#level-5">Level 5</a>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# HERO / HOME
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div id="home" class="section-wrap">', unsafe_allow_html=True)
st.markdown('<div class="hero-badge">Echo English — Learn at Your Pace</div>', unsafe_allow_html=True)
st.title("Echo English")
st.markdown("##### Helping non-English speakers hold conversations and land jobs — at their own pace, zero ads.")
st.markdown('<hr class="divider">', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="step-card" style="position:relative">
      <div class="big-number">1</div>
      <div class="step-label">The Problem</div>
      <div class="step-title">Language Barrier</div>
      Non-English speakers in English-speaking countries struggle to hold conversations and find employment.
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="step-card" style="position:relative">
      <div class="big-number">2</div>
      <div class="step-label">The Solution</div>
      <div class="step-title">AI-Driven Platform</div>
      A website with a built-in AI tutor — personalized lessons, 24/7 access, zero ads, your own pace.
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="step-card" style="position:relative">
      <div class="big-number">3</div>
      <div class="step-label">5 Levels</div>
      <div class="step-title">Your Learning Path</div>
      From complete beginner to advanced — structured levels so you always know where you stand.
    </div>""", unsafe_allow_html=True)

st.markdown("### Levels Overview")
levels_preview = [
    ("📘", "Level 1", "Beginner", "Basic greetings, numbers, everyday words", "#3b82f6"),
    ("📗", "Level 2", "Elementary", "Simple sentences, shopping, asking directions", "#22c55e"),
    ("📙", "Level 3", "Intermediate", "Work conversations, opinions, storytelling", "#f59e0b"),
    ("📕", "Level 4", "Upper Intermediate", "Job interviews, complex discussions", "#ef4444"),
    ("📓", "Level 5", "Advanced", "Fluency, idioms, professional English", "#8b5cf6"),
]
for icon, lvl, label, desc, color in levels_preview:
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:16px;padding:12px 0;border-bottom:1px solid #d0c8b8">
      <span style="font-size:1.4rem">{icon}</span>
      <span style="font-family:'Syne',sans-serif;font-weight:700;min-width:70px">{lvl}</span>
      <span style="color:{color};font-weight:600;min-width:150px">{label}</span>
      <span style="color:#555;font-size:0.88rem">{desc}</span>
    </div>""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ABOUT / BUSINESS CONCEPT
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div id="about" class="section-wrap">', unsafe_allow_html=True)
st.markdown('<div class="hero-badge">About Echo English</div>', unsafe_allow_html=True)
st.title("The Business Concept")
st.markdown('<hr class="divider">', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div class="step-card">
      <div class="step-label">The Problem</div>
      <div class="step-title">Language Barrier</div>
      <div class="answer-block">
        People living in English-speaking countries can't hold a conversation or get a job because of the language barrier.
        Existing solutions either have ads, cost too much, or simply don't build real conversational skills.
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("**Competitors & Their Flaws**")
    for name, flaw in [
        ("🦉 Duolingo", "Gamified streaks — not real conversation skills"),
        ("🏫 English Classes", "Expensive, rigid schedule, not self-paced"),
        ("📖 SpanishDict", "Dictionary only — no structured learning"),
    ]:
        st.markdown(f"""
        <div class="competitor-card">
          <strong>{name}</strong><br>
          <span style="color:#c0392b;font-size:0.9rem">❌ {flaw}</span>
        </div>""", unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="step-card">
      <div class="step-label">Our Solution</div>
      <div class="step-title">Echo English</div>
      <div class="answer-block">
        A fully personalized AI English platform. No ads. No rigid schedule. Just real conversation practice
        at your own pace, 24/7, with an AI tutor that adapts to you.
      </div>
    </div>""", unsafe_allow_html=True)

    for icon, title, desc in [
        ("🤖", "Built-in AI Tutor", "Adapts to your level and speed"),
        ("📋", "Custom Assignments", "Tailored to your specific goals"),
        ("🕐", "24/7 Availability", "Learn anytime, no schedule needed"),
        ("🚫", "Zero Ads", "Learning first, always"),
    ]:
        st.markdown(f"""
        <div style="display:flex;gap:14px;align-items:flex-start;padding:10px 0;border-bottom:1px solid #d0c8b8">
          <span style="font-size:1.3rem">{icon}</span>
          <div><strong>{title}</strong><br><span style="color:#555;font-size:0.88rem">{desc}</span></div>
        </div>""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
col1.metric("Problem Clarity", "9/10", "Well-defined & specific")
col2.metric("Solution Originality", "8/10", "AI personalization edge")
col3.metric("Market Potential", "10/10", "Massive global need")
st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# LEVEL 1 – BEGINNER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div id="level-1" class="section-wrap">', unsafe_allow_html=True)
st.markdown('<div class="hero-badge">📘 Level 1 — Beginner</div>', unsafe_allow_html=True)
st.title("Level 1 – Beginner")
st.markdown("##### Start from zero. Learn the words and phrases you need every single day.")
st.markdown('<hr class="divider">', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📖 Vocabulary", "💬 Phrases", "🎯 Practice"])
with tab1:
    st.markdown("### Essential Words")
    for cat, words in [
        ("Greetings", ["Hello", "Goodbye", "Please", "Thank you", "Sorry", "Yes", "No"]),
        ("Numbers", ["One", "Two", "Three", "Four", "Five", "Ten", "Twenty", "Hundred"]),
        ("Colors", ["Red", "Blue", "Green", "White", "Black", "Yellow"]),
        ("Family", ["Mother", "Father", "Brother", "Sister", "Friend", "Baby"]),
    ]:
        st.markdown(f"**{cat}**")
        st.markdown("".join([f'<span class="vocab-word">{w}</span>' for w in words]) + "<br><br>", unsafe_allow_html=True)

with tab2:
    st.markdown("### Key Phrases for Daily Life")
    for section, items in [
        ("Meeting people", [("Hello, my name is ___.", "Hola, me llamo ___."), ("Nice to meet you.", "Mucho gusto."), ("How are you?", "¿Cómo estás?"), ("I'm fine, thank you.", "Estoy bien, gracias.")]),
        ("Asking for help", [("Can you help me?", "¿Me puede ayudar?"), ("I don't understand.", "No entiendo."), ("Please speak slowly.", "Por favor hable despacio."), ("Where is the bathroom?", "¿Dónde está el baño?")]),
        ("Shopping", [("How much does this cost?", "¿Cuánto cuesta esto?"), ("I would like this, please.", "Quisiera esto, por favor."), ("Do you accept cash?", "¿Acepta efectivo?")]),
    ]:
        st.markdown(f"**{section}**")
        for en, es in items:
            st.markdown(f'<div class="phrase-box">🇺🇸 <strong>{en}</strong><br><span style="color:#888;font-size:0.85rem">🇪🇸 {es}</span></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

with tab3:
    st.markdown("### Quick Practice")
    st.markdown("Answer all questions, then press **Submit** to see your score.")
    l1q1 = st.radio("1. 'Hello, ___ name is Maria.' — which word fits?", ["— select —", "my", "your", "his", "she"], key="l1q1")
    l1q2 = st.radio("2. You want to say thank you. You say:", ["— select —", "Sorry", "Goodbye", "Thank you", "No"], key="l1q2")
    l1q3 = st.radio("3. You don't understand something. You say:", ["— select —", "I am fine.", "I don't understand.", "Nice to meet you.", "How much?"], key="l1q3")
    if st.button("Submit", key="l1_submit"):
        pairs = [("Q1", l1q1, "my"), ("Q2", l1q2, "Thank you"), ("Q3", l1q3, "I don't understand.")]
        score = sum(1 for _, chosen, correct in pairs if chosen == correct)
        st.markdown(f"### Your Score: {score} / 3")
        for label, chosen, correct in pairs:
            if chosen == "— select —":
                st.warning(f"⚠️ {label}: Not answered. Correct answer: **{correct}**")
            elif chosen == correct:
                st.success(f"✅ {label}: Correct!")
            else:
                st.error(f"❌ {label}: You chose '{chosen}'. Correct answer: **{correct}**")

st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# LEVEL 2 – ELEMENTARY
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div id="level-2" class="section-wrap">', unsafe_allow_html=True)
st.markdown('<div class="hero-badge">📗 Level 2 — Elementary</div>', unsafe_allow_html=True)
st.title("Level 2 – Elementary")
st.markdown("##### Build simple sentences and handle everyday situations with confidence.")
st.markdown('<hr class="divider">', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📖 Vocabulary", "💬 Phrases", "🎯 Practice"])
with tab1:
    st.markdown("### Expanding Your Word Bank")
    for cat, words in [
        ("At Work", ["Job", "Office", "Manager", "Meeting", "Email", "Schedule", "Deadline", "Team"]),
        ("At the Store", ["Price", "Receipt", "Change", "Discount", "Size", "Aisle", "Checkout"]),
        ("Directions", ["Left", "Right", "Straight", "Corner", "Block", "Near", "Far", "Across"]),
        ("Time", ["Morning", "Afternoon", "Evening", "Tonight", "Yesterday", "Tomorrow", "Weekly"]),
    ]:
        st.markdown(f"**{cat}**")
        st.markdown("".join([f'<span class="vocab-word">{w}</span>' for w in words]) + "<br><br>", unsafe_allow_html=True)

with tab2:
    st.markdown("### Useful Sentences")
    for section, items in [
        ("Asking directions", [("How do I get to ___?", "¿Cómo llego a ___?"), ("Is it far from here?", "¿Está lejos de aquí?"), ("Turn left at the corner.", "Gire a la izquierda en la esquina.")]),
        ("At work or school", [("When is the deadline?", "¿Cuándo es la fecha límite?"), ("Can I ask a question?", "¿Puedo hacer una pregunta?"), ("I will send you an email.", "Le enviaré un correo electrónico.")]),
        ("Daily life", [("What time does it open?", "¿A qué hora abre?"), ("I need to make an appointment.", "Necesito hacer una cita."), ("Can I pay by card?", "¿Puedo pagar con tarjeta?")]),
    ]:
        st.markdown(f"**{section}**")
        for en, es in items:
            st.markdown(f'<div class="phrase-box">🇺🇸 <strong>{en}</strong><br><span style="color:#888;font-size:0.85rem">🇪🇸 {es}</span></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

with tab3:
    st.markdown("### Practice Sentences")
    st.markdown("Answer all questions, then press **Submit** to see your score.")
    l2q1 = st.radio("1. You want to know how to get somewhere. You ask:", ["— select —", "What time is it?", "How do I get to the station?", "Can I have the bill?", "Where are you from?"], key="l2q1")
    l2q2 = st.radio("2. Your boss asks for the report. You say:", ["— select —", "I will send you an email.", "I am hungry.", "Turn left.", "Good morning."], key="l2q2")
    l2q3 = st.radio("3. You want to pay. You ask:", ["— select —", "Is it far?", "Can I pay by card?", "What is your name?", "I don't understand."], key="l2q3")
    if st.button("Submit", key="l2_submit"):
        pairs = [("Q1", l2q1, "How do I get to the station?"), ("Q2", l2q2, "I will send you an email."), ("Q3", l2q3, "Can I pay by card?")]
        score = sum(1 for _, chosen, correct in pairs if chosen == correct)
        st.markdown(f"### Your Score: {score} / 3")
        for label, chosen, correct in pairs:
            if chosen == "— select —":
                st.warning(f"⚠️ {label}: Not answered. Correct answer: **{correct}**")
            elif chosen == correct:
                st.success(f"✅ {label}: Correct!")
            else:
                st.error(f"❌ {label}: You chose '{chosen}'. Correct answer: **{correct}**")

st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# LEVEL 3 – INTERMEDIATE
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div id="level-3" class="section-wrap">', unsafe_allow_html=True)
st.markdown('<div class="hero-badge">📙 Level 3 — Intermediate</div>', unsafe_allow_html=True)
st.title("Level 3 – Intermediate")
st.markdown("##### Hold real conversations, express opinions, and talk about your life and work.")
st.markdown('<hr class="divider">', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📖 Vocabulary", "💬 Conversations", "🎯 Practice"])
with tab1:
    st.markdown("### Level Up Your Vocabulary")
    for cat, words in [
        ("Opinions & Feelings", ["Agree", "Disagree", "Prefer", "Frustrated", "Confident", "Nervous", "Excited", "Disappointed"]),
        ("Work & Career", ["Promotion", "Salary", "Interview", "Colleague", "Responsible", "Experience", "Qualification"]),
        ("Describing things", ["Complicated", "Efficient", "Reliable", "Flexible", "Obvious", "Detailed", "Urgent"]),
        ("Connectors", ["However", "Therefore", "Although", "Meanwhile", "Furthermore", "As a result"]),
    ]:
        st.markdown(f"**{cat}**")
        st.markdown("".join([f'<span class="vocab-word">{w}</span>' for w in words]) + "<br><br>", unsafe_allow_html=True)

with tab2:
    st.markdown("### Real Conversation Scenarios")
    st.markdown("""
    <div class="lesson-card">
      <div style="font-family:'Syne',sans-serif;font-weight:700;margin-bottom:12px">🏢 At Work — Expressing an Opinion</div>
      <div class="phrase-box">👤 Boss: "What do you think about the new schedule?"</div>
      <div class="phrase-box">🗣️ You: "I think it's a good idea, <strong>however</strong> I'm concerned about the Friday deadline."</div>
      <div class="phrase-box">👤 Boss: "That's a fair point. What do you suggest?"</div>
      <div class="phrase-box">🗣️ You: "Maybe we could move it to Monday? That would give everyone more time."</div>
    </div>
    <div class="lesson-card">
      <div style="font-family:'Syne',sans-serif;font-weight:700;margin-bottom:12px">🤝 Meeting Someone New — Telling Your Story</div>
      <div class="phrase-box">👤 Person: "Where are you from originally?"</div>
      <div class="phrase-box">🗣️ You: "I'm from Mexico. I moved here two years ago to find better work opportunities."</div>
      <div class="phrase-box">👤 Person: "How are you finding it?"</div>
      <div class="phrase-box">🗣️ You: "<strong>Although</strong> it was hard at first, I'm really enjoying it now."</div>
    </div>""", unsafe_allow_html=True)

with tab3:
    st.markdown("### Fill in the Connector")
    st.markdown("Answer all questions, then press **Submit** to see your score.")
    l3q1 = st.radio("1. 'The job pays well. ___, the hours are long.'", ["— select —", "Therefore", "However", "Although", "Meanwhile"], key="l3q1")
    l3q2 = st.radio("2. 'She studied hard. ___, she passed the exam.'", ["— select —", "However", "Although", "Therefore", "Meanwhile"], key="l3q2")
    l3q3 = st.radio("3. '___ it was raining, they went for a walk.'", ["— select —", "Therefore", "Furthermore", "Although", "As a result"], key="l3q3")
    if st.button("Submit", key="l3_submit"):
        pairs = [("Q1", l3q1, "However"), ("Q2", l3q2, "Therefore"), ("Q3", l3q3, "Although")]
        score = sum(1 for _, chosen, correct in pairs if chosen == correct)
        st.markdown(f"### Your Score: {score} / 3")
        for label, chosen, correct in pairs:
            if chosen == "— select —":
                st.warning(f"⚠️ {label}: Not answered. Correct answer: **{correct}**")
            elif chosen == correct:
                st.success(f"✅ {label}: Correct!")
            else:
                st.error(f"❌ {label}: You chose '{chosen}'. Correct answer: **{correct}**")

st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# LEVEL 4 – UPPER INTERMEDIATE
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div id="level-4" class="section-wrap">', unsafe_allow_html=True)
st.markdown('<div class="hero-badge">📕 Level 4 — Upper Intermediate</div>', unsafe_allow_html=True)
st.title("Level 4 – Upper Intermediate")
st.markdown("##### Sound more natural, nail job interviews, and handle complex conversations.")
st.markdown('<hr class="divider">', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📖 Vocabulary", "💼 Job Interview", "🎯 Practice"])
with tab1:
    st.markdown("### Professional & Nuanced Vocabulary")
    for cat, words in [
        ("Professional English", ["Demonstrate", "Initiative", "Collaborate", "Negotiate", "Implement", "Facilitate", "Prioritize"]),
        ("Expressing nuance", ["Presumably", "Technically", "Essentially", "Relatively", "Particularly", "Consistently"]),
        ("Soft skills", ["Adaptable", "Proactive", "Analytical", "Detail-oriented", "Goal-driven", "Self-motivated"]),
        ("Tone shifters", ["I'd suggest...", "It might be worth...", "Have you considered...", "One option could be..."]),
    ]:
        st.markdown(f"**{cat}**")
        st.markdown("".join([f'<span class="vocab-word">{w}</span>' for w in words]) + "<br><br>", unsafe_allow_html=True)

with tab2:
    st.markdown("### Job Interview Prep")
    for q, tip in [
        ("Tell me about yourself.", "Start with your background, mention key experience, end with why you're here. Under 2 minutes."),
        ("What are your strengths?", "Pick 2–3 real strengths with examples: 'I'm very detail-oriented — for example...'"),
        ("Why do you want this job?", "Show you researched the company and connect your skills to their needs."),
        ("Where do you see yourself in 5 years?", "Show ambition but also commitment: 'I'd like to grow within this company.'"),
        ("Do you have any questions for us?", "Always say yes! Ask about the team, the role, or growth opportunities."),
    ]:
        with st.expander(f"❓ {q}"):
            st.markdown(f'<div class="phrase-box"><strong>💡 Tip:</strong> {tip}</div>', unsafe_allow_html=True)

with tab3:
    st.markdown("### Choose the Most Professional Response")
    st.markdown("Answer all questions, then press **Submit** to see your score.")
    l4q1 = st.radio("1. Your manager asks why you missed a deadline. You say:", ["— select —", "It's not my fault.", "I apologize — I underestimated the time needed and I've already adjusted my approach.", "I was busy.", "Nobody told me."], key="l4q1")
    l4q2 = st.radio("2. You disagree with a colleague's idea in a meeting. You say:", ["— select —", "That's wrong.", "I hear you, and I'd suggest we also consider the budget impact before deciding.", "Whatever.", "No."], key="l4q2")
    if st.button("Submit", key="l4_submit"):
        pairs = [
            ("Q1", l4q1, "I apologize — I underestimated the time needed and I've already adjusted my approach."),
            ("Q2", l4q2, "I hear you, and I'd suggest we also consider the budget impact before deciding."),
        ]
        score = sum(1 for _, chosen, correct in pairs if chosen == correct)
        st.markdown(f"### Your Score: {score} / 2")
        for label, chosen, correct in pairs:
            if chosen == "— select —":
                st.warning(f"⚠️ {label}: Not answered. Correct answer: **{correct}**")
            elif chosen == correct:
                st.success(f"✅ {label}: Correct!")
            else:
                st.error(f"❌ {label}: You chose '{chosen}'. Correct answer: **{correct}**")

st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# LEVEL 5 – ADVANCED
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div id="level-5" class="section-wrap">', unsafe_allow_html=True)
st.markdown('<div class="hero-badge">📓 Level 5 — Advanced</div>', unsafe_allow_html=True)
st.title("Level 5 – Advanced")
st.markdown("##### Master idioms, nuance, tone, and fluency. Speak like you've always lived here.")
st.markdown('<hr class="divider">', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📖 Idioms", "🎭 Tone & Register", "🎯 Practice"])
with tab1:
    st.markdown("### Common English Idioms")
    st.markdown("Native speakers use these constantly. Learn them and you'll sound fluent.")
    for idiom, meaning, example in [
        ("Hit the ground running", "To start something and immediately work hard at it.", "She hit the ground running on her first day."),
        ("Beat around the bush", "To avoid talking about the main topic.", "Stop beating around the bush — just tell me what happened."),
        ("On the fence", "Undecided about something.", "I'm still on the fence about whether to take the offer."),
        ("Bite the bullet", "To endure a painful situation because it's necessary.", "I didn't want to apologize, but I bit the bullet and did it."),
        ("The ball is in your court", "It's your turn to take action.", "I've sent the proposal — the ball is in their court now."),
        ("Under the weather", "Feeling sick or unwell.", "I can't come in today, I'm feeling a bit under the weather."),
    ]:
        st.markdown(f"""
        <div class="lesson-card">
          <div style="font-family:'Syne',sans-serif;font-weight:800;color:#e85d2f">"{idiom}"</div>
          <div style="margin:6px 0;font-size:0.9rem"><strong>Meaning:</strong> {meaning}</div>
          <div class="phrase-box">💬 <em>"{example}"</em></div>
        </div>""", unsafe_allow_html=True)

with tab2:
    st.markdown("### Tone & Register")
    st.markdown("The same idea can sound very different depending on context. Compare:")
    for situation, casual, neutral, formal in [
        ("Asking for something", "Oi, send me that file.", "Could you send me that file when you get a chance?", "I would greatly appreciate it if you could send the file at your earliest convenience."),
        ("Saying you're busy", "I can't, I'm swamped.", "I'm pretty tied up right now — can we reschedule?", "Unfortunately, I have prior commitments that prevent me from attending."),
        ("Disagreeing", "That's a bad idea.", "I'm not sure that's the best approach — what about...?", "While I appreciate the suggestion, I have some concerns I'd like to raise."),
    ]:
        st.markdown(f"**{situation}**")
        c1, c2, c3 = st.columns(3)
        c1.markdown(f'<div class="phrase-box" style="border-left-color:#f59e0b"><strong>Casual</strong><br><em>"{casual}"</em></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="phrase-box" style="border-left-color:#22c55e"><strong>Neutral</strong><br><em>"{neutral}"</em></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="phrase-box" style="border-left-color:#3b82f6"><strong>Formal</strong><br><em>"{formal}"</em></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

with tab3:
    st.markdown("### Idiom Challenge")
    st.markdown("Answer all questions, then press **Submit** to see your score.")
    l5q1 = st.radio("1. 'I'm on the fence about the new job.' What does this mean?", ["— select —", "He already accepted it.", "He is undecided.", "He doesn't like it.", "He is sitting on something."], key="l5q1")
    l5q2 = st.radio("2. 'The ball is in your court.' What should you do?", ["— select —", "Wait for your boss.", "Take the next step yourself.", "Go play basketball.", "Ask someone else."], key="l5q2")
    l5q3 = st.radio("3. Which is the most formal way to say you're sick?", ["— select —", "I feel terrible.", "I'm under the weather.", "I am unwell and unable to attend.", "I'm not feeling it today."], key="l5q3")
    if st.button("Submit", key="l5_submit"):
        pairs = [("Q1", l5q1, "He is undecided."), ("Q2", l5q2, "Take the next step yourself."), ("Q3", l5q3, "I am unwell and unable to attend.")]
        score = sum(1 for _, chosen, correct in pairs if chosen == correct)
        st.markdown(f"### Your Score: {score} / 3")
        for label, chosen, correct in pairs:
            if chosen == "— select —":
                st.warning(f"⚠️ {label}: Not answered. Correct answer: **{correct}**")
            elif chosen == correct:
                st.success(f"✅ {label}: Correct!")
            else:
                st.error(f"❌ {label}: You chose '{chosen}'. Correct answer: **{correct}**")

st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:#1a1a1a;color:#f5f0e8;text-align:center;padding:32px;margin-top:0">
  <div style="font-family:'Syne',sans-serif;font-weight:800;font-size:1.2rem;color:#e85d2f;margin-bottom:8px">🔊 Echo English</div>
  <div style="color:#888;font-size:0.85rem">Learn at your own pace · Zero ads · Powered by AI · Created by Connor Burdick</div>
</div>
""", unsafe_allow_html=True)
