import streamlit as st
import requests

st.set_page_config(page_title="Echo English", page_icon="🔊", layout="wide")

# ── Session state ──────────────────────────────────────────────────────────────
for key, default in {
    "chat_messages": [],
    "progress": {1: False, 2: False, 3: False, 4: False, 5: False},
    "scores": {1: None, 2: None, 3: None, 4: None, 5: None},
    "placement_done": False,
    "placement_result": None,
    "placement_answers": {},
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Karla:wght@300;400;500&display=swap');
html, body, [class*="css"] { font-family: 'Karla', sans-serif; }
.stApp { background: #f5f0e8; color: #1a1a1a; }
[data-testid="stSidebar"] { display: none; }
[data-testid="collapsedControl"] { display: none; }
h1 { font-family: 'Syne', sans-serif !important; font-weight: 800 !important; font-size: 3rem !important; line-height: 1.1 !important; color: #1a1a1a !important; }
h2, h3 { font-family: 'Syne', sans-serif !important; font-weight: 700 !important; color: #1a1a1a !important; }
.navbar { position: sticky; top: 0; z-index: 999; background: #1a1a1a; padding: 12px 40px; display: flex; align-items: center; gap: 20px; flex-wrap: wrap; }
.navbar a { color: #f5f0e8; text-decoration: none; font-family: 'Syne', sans-serif; font-weight: 700; font-size: 0.72rem; letter-spacing: 1.5px; text-transform: uppercase; opacity: 0.7; }
.navbar a:hover { opacity: 1; }
.navbar-brand { color: #e85d2f !important; opacity: 1 !important; font-size: 1rem !important; margin-right: 12px; }
.section-wrap { padding: 64px 48px; border-bottom: 2px solid #d0c8b8; }
.hero-section { background: #1a1a1a; color: #f5f0e8; padding: 100px 48px 80px; }
.hero-badge { background: #e85d2f; color: white; display: inline-block; padding: 6px 16px; font-family: 'Syne', sans-serif; font-size: 0.75rem; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 20px; }
.hero-title { font-family: 'Syne', sans-serif; font-size: 4.5rem; font-weight: 800; color: #f5f0e8; line-height: 1.0; margin-bottom: 20px; }
.hero-sub { font-size: 1.15rem; color: #a0a090; max-width: 560px; line-height: 1.7; margin-bottom: 36px; }
.hero-btn { background: #e85d2f; color: white; display: inline-block; padding: 16px 36px; font-family: 'Syne', sans-serif; font-weight: 800; font-size: 1rem; letter-spacing: 1px; text-transform: uppercase; text-decoration: none; box-shadow: 4px 4px 0px #f5f0e8; cursor: pointer; border: none; }
.hero-stat { text-align: center; padding: 20px; border-left: 1px solid #2a2a2a; }
.hero-stat-num { font-family: 'Syne', sans-serif; font-size: 2.5rem; font-weight: 800; color: #e85d2f; }
.hero-stat-label { font-size: 0.85rem; color: #888; margin-top: 4px; }
.divider { border: none; border-top: 2px solid #1a1a1a; margin: 32px 0; }
.step-card { background: #ffffff; border-left: 5px solid #e85d2f; padding: 28px 32px; margin-bottom: 24px; box-shadow: 4px 4px 0px #1a1a1a; }
.step-label { font-family: 'Syne', sans-serif; font-size: 0.7rem; font-weight: 700; letter-spacing: 3px; text-transform: uppercase; color: #e85d2f; margin-bottom: 6px; }
.step-title { font-family: 'Syne', sans-serif; font-size: 1.4rem; font-weight: 800; color: #1a1a1a; margin-bottom: 16px; }
.answer-block { background: #f5f0e8; padding: 14px 18px; margin: 10px 0; font-size: 0.95rem; line-height: 1.6; border-bottom: 2px solid #1a1a1a; }
.big-number { font-family: 'Syne', sans-serif; font-size: 5rem; font-weight: 800; color: #e85d2f; opacity: 0.15; line-height: 1; position: absolute; top: 10px; right: 20px; }
.vocab-word { background: #1a1a1a; color: #f5f0e8; display: inline-block; padding: 6px 14px; font-family: 'Syne', sans-serif; font-weight: 700; font-size: 0.9rem; margin: 4px 4px 4px 0; }
.phrase-box { background: #f5f0e8; border-left: 4px solid #e85d2f; padding: 12px 16px; margin: 8px 0; font-size: 0.95rem; line-height: 1.5; }
.lesson-card { background: #fff; border: 2px solid #1a1a1a; padding: 20px 24px; margin-bottom: 16px; box-shadow: 3px 3px 0px #1a1a1a; }
.competitor-card { background: #fff; border: 2px solid #1a1a1a; padding: 16px 20px; margin: 8px 0; box-shadow: 3px 3px 0px #1a1a1a; }
.chat-user { background: #1a1a1a; color: #f5f0e8; padding: 12px 16px; margin: 8px 0; text-align: right; font-size: 0.95rem; white-space: pre-wrap; }
.chat-ai { background: #fff; border: 2px solid #1a1a1a; color: #1a1a1a; padding: 12px 16px; margin: 8px 0; font-size: 0.95rem; box-shadow: 2px 2px 0px #1a1a1a; white-space: pre-wrap; }
.progress-bar-wrap { background: #d0c8b8; height: 14px; width: 100%; margin: 8px 0 4px; }
.progress-bar-fill { background: #e85d2f; height: 14px; }
.progress-level-card { background: #fff; border: 2px solid #1a1a1a; padding: 16px 20px; margin-bottom: 10px; box-shadow: 3px 3px 0px #1a1a1a; display: flex; align-items: center; gap: 16px; }
.before-after { display: grid; grid-template-columns: 1fr 1fr; gap: 0; border: 2px solid #1a1a1a; box-shadow: 4px 4px 0px #1a1a1a; margin-bottom: 24px; }
.before-col { background: #fff; padding: 24px; border-right: 2px solid #1a1a1a; }
.after-col { background: #1a1a1a; color: #f5f0e8; padding: 24px; }
.ba-label { font-family: 'Syne', sans-serif; font-size: 0.7rem; font-weight: 700; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 12px; }
.placement-card { background: #fff; border: 2px solid #1a1a1a; padding: 28px 32px; box-shadow: 4px 4px 0px #1a1a1a; margin-bottom: 16px; }
.result-banner { padding: 28px 32px; margin: 16px 0; border: 3px solid #1a1a1a; box-shadow: 6px 6px 0px #1a1a1a; }
div[data-testid="stButton"] button { background: #e85d2f !important; color: white !important; border: none !important; border-radius: 0 !important; font-family: 'Syne', sans-serif !important; font-weight: 700 !important; letter-spacing: 1px !important; padding: 10px 24px !important; box-shadow: 3px 3px 0px #1a1a1a !important; }
[data-testid="stMetricValue"] { font-family: 'Syne', sans-serif !important; font-weight: 800 !important; }
</style>
""", unsafe_allow_html=True)

# ── Nav ────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="navbar">
  <a class="navbar-brand" href="#hero">🔊 Echo English</a>
  <a href="#placement">Placement Quiz</a>
  <a href="#progress">Progress</a>
  <a href="#stories">Success Stories</a>
  <a href="#level-1">Level 1</a>
  <a href="#level-2">Level 2</a>
  <a href="#level-3">Level 3</a>
  <a href="#level-4">Level 4</a>
  <a href="#level-5">Level 5</a>
  <a href="#ai-chat">AI Partner</a>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div id="hero" class="hero-section">', unsafe_allow_html=True)
st.markdown('<div class="hero-badge">🔊 Echo English</div>', unsafe_allow_html=True)
st.markdown("""
<div class="hero-title">Speak English.<br>Get the Job.<br>Live Your Life.</div>
<div class="hero-sub">A free, AI-powered English learning platform built for non-native speakers. No ads. No rigid schedules. Just real conversation practice at your own pace — 24/7.</div>
""", unsafe_allow_html=True)

col_btn, col_space = st.columns([1, 3])
with col_btn:
    if st.button("🎯  Take the Placement Quiz", key="hero_cta"):
        st.markdown('<script>document.getElementById("placement").scrollIntoView();</script>', unsafe_allow_html=True)

st.markdown('<hr style="border-color:#2a2a2a;margin:48px 0 32px">', unsafe_allow_html=True)
s1, s2, s3, s4 = st.columns(4)
for col, num, label in [
    (s1, "5", "Learning Levels"),
    (s2, "AI", "Conversation Partner"),
    (s3, "0", "Ads Ever"),
    (s4, "24/7", "Available"),
]:
    col.markdown(f"""
    <div class="hero-stat">
      <div class="hero-stat-num">{num}</div>
      <div class="hero-stat-label">{label}</div>
    </div>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PLACEMENT QUIZ
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div id="placement" class="section-wrap">', unsafe_allow_html=True)
st.markdown('<div class="hero-badge">Find Your Level</div>', unsafe_allow_html=True)
st.title("Placement Quiz")
st.markdown("##### Answer 5 quick questions and we'll tell you exactly which level to start at.")
st.markdown('<hr class="divider">', unsafe_allow_html=True)

placement_questions = [
    {
        "q": "1. Which sentence is correct?",
        "options": ["I no understand.", "I don't understand.", "I not understand.", "I am not understanding."],
        "correct": "I don't understand.",
        "level": 1,
    },
    {
        "q": "2. Choose the best response: 'How do I get to the train station?'",
        "options": ["Yes, I am.", "Turn left at the corner, then walk two blocks.", "I am going.", "No problem."],
        "correct": "Turn left at the corner, then walk two blocks.",
        "level": 2,
    },
    {
        "q": "3. Fill in the blank: 'The job is great. ___, the commute is very long.'",
        "options": ["So", "Because", "However", "Also"],
        "correct": "However",
        "level": 3,
    },
    {
        "q": "4. Which is the most professional way to disagree with your manager?",
        "options": ["You're wrong.", "I don't think so.", "I see your point, though I'd like to suggest an alternative approach.", "That's a bad idea."],
        "correct": "I see your point, though I'd like to suggest an alternative approach.",
        "level": 4,
    },
    {
        "q": "5. What does 'hit the ground running' mean?",
        "options": ["To fall while jogging.", "To start something and immediately work hard at it.", "To be very tired.", "To arrive somewhere quickly."],
        "correct": "To start something and immediately work hard at it.",
        "level": 5,
    },
]

col_quiz, col_info = st.columns([3, 1])

with col_info:
    st.markdown("""
    <div class="step-card" style="padding:20px 24px">
      <div class="step-label">How it works</div>
      <div style="font-size:0.88rem;color:#555;line-height:1.8">
        5 questions covering all levels.<br><br>
        Your result tells you exactly which level to start at so you're not too bored or too confused.
      </div>
    </div>""", unsafe_allow_html=True)

with col_quiz:
    if not st.session_state.placement_done:
        answers = {}
        for pq in placement_questions:
            ans = st.radio(pq["q"], ["— select —"] + pq["options"], key=f"pq_{pq['level']}")
            answers[pq["level"]] = (ans, pq["correct"])

        if st.button("Get My Level →", key="placement_submit"):
            unanswered = [lvl for lvl, (ans, _) in answers.items() if ans == "— select —"]
            if unanswered:
                st.warning("Please answer all 5 questions first.")
            else:
                correct_levels = [lvl for lvl, (ans, correct) in answers.items() if ans == correct]
                score = len(correct_levels)
                if score <= 1:
                    result = (1, "Beginner", "📘", "#3b82f6", "You're just getting started — and that's great! Level 1 will teach you the essentials.")
                elif score == 2:
                    result = (2, "Elementary", "📗", "#22c55e", "You know some basics! Level 2 will help you build real sentences and handle everyday situations.")
                elif score == 3:
                    result = (3, "Intermediate", "📙", "#f59e0b", "Nice work! You can communicate but there's room to grow. Level 3 focuses on real conversations.")
                elif score == 4:
                    result = (4, "Upper Intermediate", "📕", "#ef4444", "Impressive! You're nearly fluent. Level 4 will polish your professional English.")
                else:
                    result = (5, "Advanced", "📓", "#8b5cf6", "Excellent! You're at an advanced level. Level 5 covers idioms, nuance, and professional mastery.")
                st.session_state.placement_result = result
                st.session_state.placement_answers = answers
                st.session_state.placement_done = True
                st.rerun()
    else:
        result = st.session_state.placement_result
        lvl_num, lvl_name, icon, color, message = result
        score = len([1 for ans, correct in st.session_state.placement_answers.values() if ans == correct])

        st.markdown(f"""
        <div class="result-banner" style="background:{color}15;border-color:{color}">
          <div style="font-family:'Syne',sans-serif;font-size:0.75rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:{color};margin-bottom:8px">Your Result</div>
          <div style="font-family:'Syne',sans-serif;font-size:2.2rem;font-weight:800;color:#1a1a1a">{icon} Level {lvl_num} — {lvl_name}</div>
          <div style="font-size:0.9rem;color:#555;margin-top:8px">Score: {score} / 5 correct</div>
          <div style="margin-top:12px;font-size:1rem;color:#333">{message}</div>
        </div>""", unsafe_allow_html=True)

        st.markdown("**How you did on each question:**")
        for pq in placement_questions:
            chosen, correct = st.session_state.placement_answers[pq["level"]]
            if chosen == correct:
                st.success(f"✅ Q{pq['level']}: Correct!")
            else:
                st.error(f"❌ Q{pq['level']}: You chose '{chosen}'. Answer: **{correct}**")

        if st.button("Retake Quiz", key="retake_placement"):
            st.session_state.placement_done = False
            st.session_state.placement_result = None
            st.session_state.placement_answers = {}
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PROGRESS TRACKER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div id="progress" class="section-wrap">', unsafe_allow_html=True)
st.markdown('<div class="hero-badge">Your Progress</div>', unsafe_allow_html=True)
st.title("Progress Tracker")
st.markdown("##### Your quiz scores and level completion all in one place.")
st.markdown('<hr class="divider">', unsafe_allow_html=True)

completed = sum(1 for v in st.session_state.progress.values() if v)
pct = int((completed / 5) * 100)
avg_scores = [s for s in st.session_state.scores.values() if s is not None]

c1, c2, c3 = st.columns(3)
c1.metric("Levels Completed", f"{completed} / 5")
c2.metric("Overall Progress", f"{pct}%")
c3.metric("Avg Quiz Score", f"{round(sum(avg_scores)/len(avg_scores),1) if avg_scores else '—'}")

st.markdown(f'<div class="progress-bar-wrap"><div class="progress-bar-fill" style="width:{pct}%"></div></div><div style="font-size:0.8rem;color:#888;margin-bottom:24px">{pct}% complete</div>', unsafe_allow_html=True)

for num, icon, label in [(1,"📘","Beginner"),(2,"📗","Elementary"),(3,"📙","Intermediate"),(4,"📕","Upper Intermediate"),(5,"📓","Advanced")]:
    done = st.session_state.progress[num]
    score = st.session_state.scores[num]
    max_s = 2 if num == 4 else 3
    color = "#22c55e" if done else "#d0c8b8"
    status = f"✅ Completed — Score: {score}/{max_s}" if done else "⬜ Not yet completed"
    st.markdown(f"""
    <div class="progress-level-card">
      <span style="font-size:2rem">{icon}</span>
      <div style="flex:1">
        <div style="font-family:'Syne',sans-serif;font-weight:800">Level {num} — {label}</div>
        <div style="color:#555;font-size:0.85rem;margin-top:4px">{status}</div>
      </div>
      <div style="width:120px"><div style="background:#d0c8b8;height:8px"><div style="background:{color};height:8px;width:{'100%' if done else '0%'}"></div></div></div>
    </div>""", unsafe_allow_html=True)

if completed > 0:
    if st.button("Reset All Progress", key="reset_progress"):
        st.session_state.progress = {1:False,2:False,3:False,4:False,5:False}
        st.session_state.scores = {1:None,2:None,3:None,4:None,5:None}
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# BEFORE / AFTER SUCCESS STORIES
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div id="stories" class="section-wrap">', unsafe_allow_html=True)
st.markdown('<div class="hero-badge">Real Results</div>', unsafe_allow_html=True)
st.title("Before & After Echo English")
st.markdown("##### See the difference real practice makes.")
st.markdown('<hr class="divider">', unsafe_allow_html=True)

stories = [
    {
        "name": "Maria, 28 — from Mexico City",
        "context": "Moved to the US for work. Struggled to communicate with her coworkers.",
        "before_title": "Before Echo English",
        "before": [
            "😰 Avoided talking to coworkers out of embarrassment",
            "❌ Said: 'I no understand the meeting today'",
            "😶 Stayed quiet during team discussions",
            "📉 Was passed over for a promotion",
        ],
        "after_title": "After 3 Months",
        "after": [
            "😊 Confidently joins conversations at work",
            "✅ Says: 'I didn't quite follow the meeting — could you clarify?'",
            "🗣️ Regularly shares ideas in team meetings",
            "📈 Got promoted to team lead",
        ],
    },
    {
        "name": "Ahmed, 34 — from Egypt",
        "context": "Arrived in the UK with engineering qualifications but couldn't land a job.",
        "before_title": "Before Echo English",
        "before": [
            "😰 Froze up in job interviews",
            "❌ Said: 'I am very hardly worker and I do my best always'",
            "😟 Rejected from 12 interviews in a row",
            "💸 Working in a warehouse below his skill level",
        ],
        "after_title": "After 4 Months",
        "after": [
            "😎 Calm and prepared in interviews",
            "✅ Says: 'I'm a highly motivated engineer with 8 years of experience'",
            "🎉 Landed a job at a London tech firm",
            "🏆 Now mentors other immigrants learning English",
        ],
    },
    {
        "name": "Lin, 22 — from China",
        "context": "Started university in Canada but couldn't follow lectures or make friends.",
        "before_title": "Before Echo English",
        "before": [
            "😰 Sat in the back of class and said nothing",
            "❌ Said: 'Yesterday I go to the library and study very much'",
            "😔 Ate lunch alone every day",
            "📚 Was failing two classes",
        ],
        "after_title": "After 2 Months",
        "after": [
            "✋ Raises her hand and asks questions in lectures",
            "✅ Says: 'Yesterday I went to the library and studied for a few hours'",
            "👫 Has a group of close friends from her course",
            "🎓 Made the Dean's List last semester",
        ],
    },
]

for story in stories:
    st.markdown(f"### {story['name']}")
    st.markdown(f"*{story['context']}*")
    st.markdown(f"""
    <div class="before-after">
      <div class="before-col">
        <div class="ba-label" style="color:#c0392b">❌ {story['before_title']}</div>
        {''.join([f'<div style="padding:6px 0;border-bottom:1px solid #f0ebe0;font-size:0.9rem">{item}</div>' for item in story['before']])}
      </div>
      <div class="after-col">
        <div class="ba-label" style="color:#4ade80">✅ {story['after_title']}</div>
        {''.join([f'<div style="padding:6px 0;border-bottom:1px solid #2a2a2a;font-size:0.9rem">{item}</div>' for item in story['after']])}
      </div>
    </div>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


# ── Helper: practice renderer ──────────────────────────────────────────────────
def render_practice(level_num, questions, correct_answers, max_score):
    st.markdown("Answer all questions, then press **Submit** to see your score.")
    responses = []
    for i, (q_label, opts) in enumerate(questions):
        val = st.radio(q_label, ["— select —"] + opts, key=f"l{level_num}q{i+1}")
        responses.append(val)
    if st.button("Submit", key=f"l{level_num}_submit"):
        score = sum(1 for r, c in zip(responses, correct_answers) if r == c)
        st.session_state.scores[level_num] = score
        st.session_state.progress[level_num] = True
        st.markdown(f"### Your Score: {score} / {max_score}")
        for i, (r, c) in enumerate(zip(responses, correct_answers)):
            lbl = f"Q{i+1}"
            if r == "— select —": st.warning(f"⚠️ {lbl}: Not answered. Answer: **{c}**")
            elif r == c: st.success(f"✅ {lbl}: Correct!")
            else: st.error(f"❌ {lbl}: You chose '{r}'. Answer: **{c}**")
        if score == max_score:
            st.balloons()
            st.success("🎉 Perfect score! Level marked as complete.")
        else:
            st.info("Level marked as attempted. Get a perfect score to fully complete it!")


# ══════════════════════════════════════════════════════════════════════════════
# LEVEL 1
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div id="level-1" class="section-wrap">', unsafe_allow_html=True)
st.markdown('<div class="hero-badge">📘 Level 1 — Beginner</div>', unsafe_allow_html=True)
st.title("Level 1 – Beginner")
st.markdown("##### Start from zero. Learn the words and phrases you need every single day.")
st.markdown('<hr class="divider">', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📖 Vocabulary", "💬 Phrases", "🎯 Practice"])
with tab1:
    for cat, words in [("Greetings",["Hello","Goodbye","Please","Thank you","Sorry","Yes","No","Excuse me"]),("Numbers",["One","Two","Three","Four","Five","Ten","Twenty","Hundred"]),("Colors",["Red","Blue","Green","White","Black","Yellow","Orange","Purple"]),("Family",["Mother","Father","Brother","Sister","Friend","Baby","Husband","Wife"]),("Places",["Home","School","Hospital","Store","Restaurant","Bank","Street","City"])]:
        st.markdown(f"**{cat}**")
        st.markdown("".join([f'<span class="vocab-word">{w}</span>' for w in words])+"<br><br>", unsafe_allow_html=True)

with tab2:
    for section, items in [
        ("Meeting people",[("Hello, my name is ___.", "Hola, me llamo ___."),("Nice to meet you.","Mucho gusto."),("How are you?","¿Cómo estás?"),("I'm fine, thank you.","Estoy bien, gracias."),("Where are you from?","¿De dónde eres?")]),
        ("Asking for help",[("Can you help me?","¿Me puede ayudar?"),("I don't understand.","No entiendo."),("Please speak slowly.","Por favor hable despacio."),("Where is the bathroom?","¿Dónde está el baño?"),("Can you repeat that?","¿Puede repetir eso?")]),
        ("Shopping",[("How much does this cost?","¿Cuánto cuesta esto?"),("I would like this, please.","Quisiera esto, por favor."),("Do you accept cash?","¿Acepta efectivo?"),("Do you have this in a different size?","¿Tiene esto en otra talla?")])
    ]:
        st.markdown(f"**{section}**")
        for en, es in items:
            st.markdown(f'<div class="phrase-box">🇺🇸 <strong>{en}</strong><br><span style="color:#888;font-size:0.85rem">🇪🇸 {es}</span></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

with tab3:
    render_practice(1, [
        ("1. 'Hello, ___ name is Maria.' — which word fits?", ["my","your","his","she"]),
        ("2. You want to say thank you. You say:", ["Sorry","Goodbye","Thank you","No"]),
        ("3. You don't understand something. You say:", ["I am fine.","I don't understand.","Nice to meet you.","How much?"]),
        ("4. Someone says 'Nice to meet you.' You reply:", ["Goodbye.","Nice to meet you too.","I am sorry.","Yes please."]),
        ("5. You want someone to speak more slowly. You say:", ["Please be quiet.","Please speak slowly.","I am speaking.","Thank you."]),
        ("6. You want to know the price of something. You ask:", ["Where is it?","What color is it?","How much does this cost?","Can you help me?"]),
    ], ["my","Thank you","I don't understand.","Nice to meet you too.","Please speak slowly.","How much does this cost?"], 6)

st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# LEVEL 2
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div id="level-2" class="section-wrap">', unsafe_allow_html=True)
st.markdown('<div class="hero-badge">📗 Level 2 — Elementary</div>', unsafe_allow_html=True)
st.title("Level 2 – Elementary")
st.markdown("##### Build simple sentences and handle everyday situations with confidence.")
st.markdown('<hr class="divider">', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📖 Vocabulary", "💬 Phrases", "🎯 Practice"])
with tab1:
    for cat, words in [("At Work",["Job","Office","Manager","Meeting","Email","Schedule","Deadline","Team","Colleague","Report"]),("At the Store",["Price","Receipt","Change","Discount","Size","Aisle","Checkout","Return","Sale"]),("Directions",["Left","Right","Straight","Corner","Block","Near","Far","Across","Next to","Between"]),("Time",["Morning","Afternoon","Evening","Tonight","Yesterday","Tomorrow","Weekly","Monthly","Appointment","On time"])]:
        st.markdown(f"**{cat}**")
        st.markdown("".join([f'<span class="vocab-word">{w}</span>' for w in words])+"<br><br>", unsafe_allow_html=True)

with tab2:
    for section, items in [
        ("Asking directions",[("How do I get to ___?","¿Cómo llego a ___?"),("Is it far from here?","¿Está lejos de aquí?"),("Turn left at the corner.","Gire a la izquierda en la esquina."),("It's next to the bank.","Está al lado del banco.")]),
        ("At work",[("When is the deadline?","¿Cuándo es la fecha límite?"),("Can I ask a question?","¿Puedo hacer una pregunta?"),("I will send you an email.","Le enviaré un correo electrónico."),("I have a meeting at 3pm.","Tengo una reunión a las 3pm.")]),
        ("Daily life",[("What time does it open?","¿A qué hora abre?"),("I need to make an appointment.","Necesito hacer una cita."),("Can I pay by card?","¿Puedo pagar con tarjeta?"),("What time does the bus arrive?","¿A qué hora llega el autobús?")])
    ]:
        st.markdown(f"**{section}**")
        for en, es in items:
            st.markdown(f'<div class="phrase-box">🇺🇸 <strong>{en}</strong><br><span style="color:#888;font-size:0.85rem">🇪🇸 {es}</span></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

with tab3:
    render_practice(2, [
        ("1. You want to know how to get somewhere. You ask:", ["What time is it?","How do I get to the station?","Can I have the bill?","Where are you from?"]),
        ("2. Your boss asks for the report. You say:", ["I will send you an email.","I am hungry.","Turn left.","Good morning."]),
        ("3. You want to pay. You ask:", ["Is it far?","Can I pay by card?","What is your name?","I don't understand."]),
        ("4. Someone asks 'Is the supermarket far?' You answer:", ["Yes, it is next to the bank.","I am fine, thank you.","My name is Pedro.","Turn left."]),
        ("5. You need to cancel a doctor's appointment. You say:", ["I need to cancel my appointment.","I am very hungry.","Where is the hospital?","Thank you goodbye."]),
        ("6. Your colleague asks when the meeting is. You say:", ["I have a meeting at 3pm.","The price is ten dollars.","Turn right at the corner.","I don't understand."]),
    ], ["How do I get to the station?","I will send you an email.","Can I pay by card?","Yes, it is next to the bank.","I need to cancel my appointment.","I have a meeting at 3pm."], 6)

st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# LEVEL 3
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div id="level-3" class="section-wrap">', unsafe_allow_html=True)
st.markdown('<div class="hero-badge">📙 Level 3 — Intermediate</div>', unsafe_allow_html=True)
st.title("Level 3 – Intermediate")
st.markdown("##### Hold real conversations, express opinions, and talk about your life and work.")
st.markdown('<hr class="divider">', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📖 Vocabulary", "💬 Conversations", "🎯 Practice"])
with tab1:
    for cat, words in [("Opinions & Feelings",["Agree","Disagree","Prefer","Frustrated","Confident","Nervous","Excited","Disappointed","Overwhelmed","Motivated"]),("Work & Career",["Promotion","Salary","Interview","Colleague","Responsible","Experience","Qualification","Department","Deadline","Performance"]),("Connectors",["However","Therefore","Although","Meanwhile","Furthermore","As a result","On the other hand","In addition","Nevertheless","Consequently"])]:
        st.markdown(f"**{cat}**")
        st.markdown("".join([f'<span class="vocab-word">{w}</span>' for w in words])+"<br><br>", unsafe_allow_html=True)

with tab2:
    st.markdown("""<div class="lesson-card"><div style="font-family:'Syne',sans-serif;font-weight:700;margin-bottom:12px">🏢 At Work — Expressing an Opinion</div><div class="phrase-box">👤 Boss: "What do you think about the new schedule?"</div><div class="phrase-box">🗣️ You: "I think it's a good idea, <strong>however</strong> I'm concerned about the Friday deadline."</div><div class="phrase-box">👤 Boss: "That's a fair point. What do you suggest?"</div><div class="phrase-box">🗣️ You: "Maybe we could move it to Monday? That would give everyone more time."</div></div>""", unsafe_allow_html=True)
    st.markdown("""<div class="lesson-card"><div style="font-family:'Syne',sans-serif;font-weight:700;margin-bottom:12px">🤝 Meeting Someone New — Telling Your Story</div><div class="phrase-box">👤 Person: "Where are you from originally?"</div><div class="phrase-box">🗣️ You: "I'm from Mexico. I moved here two years ago to find better work opportunities."</div><div class="phrase-box">👤 Person: "How are you finding it?"</div><div class="phrase-box">🗣️ You: "<strong>Although</strong> it was hard at first, I'm really enjoying it now. The language was the biggest challenge."</div></div>""", unsafe_allow_html=True)

with tab3:
    render_practice(3, [
        ("1. 'The job pays well. ___, the hours are long.'", ["Therefore","However","Although","Meanwhile"]),
        ("2. 'She studied hard. ___, she passed the exam.'", ["However","Although","Therefore","Meanwhile"]),
        ("3. '___ it was raining, they went for a walk.'", ["Therefore","Furthermore","Although","As a result"]),
        ("4. 'I enjoy my work. ___, I find the commute exhausting.'", ["Therefore","Furthermore","On the other hand","Consequently"]),
        ("5. 'He missed the interview. ___, he didn't get the job.'", ["However","Although","Nevertheless","As a result"]),
        ("6. Which word means you feel sure about yourself?", ["Frustrated","Nervous","Confident","Disappointed"]),
    ], ["However","Therefore","Although","On the other hand","As a result","Confident"], 6)

st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# LEVEL 4
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div id="level-4" class="section-wrap">', unsafe_allow_html=True)
st.markdown('<div class="hero-badge">📕 Level 4 — Upper Intermediate</div>', unsafe_allow_html=True)
st.title("Level 4 – Upper Intermediate")
st.markdown("##### Sound more natural, nail job interviews, and handle complex conversations.")
st.markdown('<hr class="divider">', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📖 Vocabulary", "💼 Job Interview", "🎯 Practice"])
with tab1:
    for cat, words in [("Professional English",["Demonstrate","Initiative","Collaborate","Negotiate","Implement","Facilitate","Prioritize","Delegate","Streamline","Leverage"]),("Soft skills",["Adaptable","Proactive","Analytical","Detail-oriented","Goal-driven","Self-motivated","Team player","Problem-solver"]),("Tone shifters",["I'd suggest...","It might be worth...","Have you considered...","One option could be...","I'd like to raise a concern...","With respect,..."])]:
        st.markdown(f"**{cat}**")
        st.markdown("".join([f'<span class="vocab-word">{w}</span>' for w in words])+"<br><br>", unsafe_allow_html=True)

with tab2:
    for q, tip in [("Tell me about yourself.","Start with your background, mention key experience, end with why you're here. Under 2 minutes."),("What are your strengths?","Pick 2–3 real strengths with examples: 'I'm very detail-oriented — for example...'"),("Why do you want this job?","Show you researched the company and connect your skills to their needs."),("Describe a challenge you overcame.","Use the STAR method: Situation, Task, Action, Result."),("Where do you see yourself in 5 years?","Show ambition but commitment: 'I'd like to grow within this company.'"),("Do you have any questions for us?","Always say yes! Ask about the team, the role, or growth opportunities.")]:
        with st.expander(f"❓ {q}"):
            st.markdown(f'<div class="phrase-box"><strong>💡 Tip:</strong> {tip}</div>', unsafe_allow_html=True)

with tab3:
    render_practice(4, [
        ("1. Your manager asks why you missed a deadline. You say:", ["It's not my fault.","I apologize — I underestimated the time needed and I've already adjusted my approach.","I was busy.","Nobody told me."]),
        ("2. You disagree with a colleague in a meeting. You say:", ["That's wrong.","I hear you, and I'd suggest we also consider the budget impact before deciding.","Whatever.","No."]),
        ("3. You want to ask for a raise. The best opening is:", ["Give me more money.","I've been here 2 years, pay me more.","I'd like to discuss my compensation given my recent contributions.","I need a raise."]),
        ("4. A client is upset. You say:", ["Not my problem.","Calm down.","I understand your frustration and I'd like to help resolve this as quickly as possible.","That's not what I said."]),
        ("5. Which phrase best shows initiative in a job interview?", ["I just do what I'm told.","I proactively identified a gap in our process and implemented a solution that saved the team 3 hours a week.","I come to work on time.","I try my best."]),
        ("6. Which word means to make a process more efficient?", ["Delegate","Facilitate","Streamline","Negotiate"]),
    ], [
        "I apologize — I underestimated the time needed and I've already adjusted my approach.",
        "I hear you, and I'd suggest we also consider the budget impact before deciding.",
        "I'd like to discuss my compensation given my recent contributions.",
        "I understand your frustration and I'd like to help resolve this as quickly as possible.",
        "I proactively identified a gap in our process and implemented a solution that saved the team 3 hours a week.",
        "Streamline",
    ], 6)

st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# LEVEL 5
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div id="level-5" class="section-wrap">', unsafe_allow_html=True)
st.markdown('<div class="hero-badge">📓 Level 5 — Advanced</div>', unsafe_allow_html=True)
st.title("Level 5 – Advanced")
st.markdown("##### Master idioms, nuance, tone, and fluency. Speak like you've always lived here.")
st.markdown('<hr class="divider">', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📖 Idioms", "🎭 Tone & Register", "🎯 Practice"])
with tab1:
    for idiom, meaning, example in [
        ("Hit the ground running","To start something and immediately work hard at it.","She hit the ground running on her first day."),
        ("Beat around the bush","To avoid talking about the main topic.","Stop beating around the bush — just tell me what happened."),
        ("On the fence","Undecided about something.","I'm still on the fence about whether to take the offer."),
        ("Bite the bullet","To endure a painful situation because it's necessary.","I didn't want to apologize, but I bit the bullet and did it."),
        ("The ball is in your court","It's your turn to take action.","I've sent the proposal — the ball is in their court now."),
        ("Under the weather","Feeling sick or unwell.","I can't come in today, I'm a bit under the weather."),
        ("Burn bridges","To permanently damage a relationship.","Don't quit like that — you'll burn bridges in this industry."),
        ("Cut corners","To do something the quick or cheap way, sacrificing quality.","We can't cut corners on safety procedures."),
    ]:
        st.markdown(f'<div class="lesson-card"><div style="font-family:\'Syne\',sans-serif;font-weight:800;color:#e85d2f">"{idiom}"</div><div style="margin:6px 0;font-size:0.9rem"><strong>Meaning:</strong> {meaning}</div><div class="phrase-box">💬 <em>"{example}"</em></div></div>', unsafe_allow_html=True)

with tab2:
    for situation, casual, neutral, formal in [
        ("Asking for something","Oi, send me that file.","Could you send me that file when you get a chance?","I would greatly appreciate it if you could send the file at your earliest convenience."),
        ("Saying you're busy","I can't, I'm swamped.","I'm pretty tied up right now — can we reschedule?","Unfortunately, I have prior commitments that prevent me from attending."),
        ("Disagreeing","That's a bad idea.","I'm not sure that's the best approach — what about...?","While I appreciate the suggestion, I have some concerns I'd like to raise."),
    ]:
        st.markdown(f"**{situation}**")
        c1, c2, c3 = st.columns(3)
        c1.markdown(f'<div class="phrase-box" style="border-left-color:#f59e0b"><strong>Casual</strong><br><em>"{casual}"</em></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="phrase-box" style="border-left-color:#22c55e"><strong>Neutral</strong><br><em>"{neutral}"</em></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="phrase-box" style="border-left-color:#3b82f6"><strong>Formal</strong><br><em>"{formal}"</em></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

with tab3:
    render_practice(5, [
        ("1. 'I'm on the fence about the new job.' What does this mean?", ["He already accepted it.","He is undecided.","He doesn't like it.","He is sitting on something."]),
        ("2. 'The ball is in your court.' What should you do?", ["Wait for your boss.","Take the next step yourself.","Go play basketball.","Ask someone else."]),
        ("3. Which is the most formal way to say you're sick?", ["I feel terrible.","I'm under the weather.","I am unwell and unable to attend.","I'm not feeling it today."]),
        ("4. Your colleague quit very angrily and insulted everyone. You say:", ["Good for them.","They really burned their bridges there.","They hit the ground running.","They were on the fence."]),
        ("5. The team rushed the project and the quality was poor. You say:", ["They beat around the bush.","They cut corners.","They bit the bullet.","They burned bridges."]),
        ("6. 'Stop beating around the bush' means:", ["Stop running.","Stop being nervous.","Get to the point.","Stop being lazy."]),
    ], ["He is undecided.","Take the next step yourself.","I am unwell and unable to attend.","They really burned their bridges there.","They cut corners.","Get to the point."], 6)

st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# AI CONVERSATION PARTNER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div id="ai-chat" class="section-wrap">', unsafe_allow_html=True)
st.markdown('<div class="hero-badge">🤖 AI Conversation Partner</div>', unsafe_allow_html=True)
st.title("AI Conversation Partner")
st.markdown("##### Practice real English conversations with an AI tutor. It will correct your mistakes and help you improve.")
st.markdown('<hr class="divider">', unsafe_allow_html=True)

col_left, col_right = st.columns([2, 1])

with col_right:
    st.markdown("### Settings")
    chat_level = st.selectbox("Your level", ["Beginner (Level 1)","Elementary (Level 2)","Intermediate (Level 3)","Upper Intermediate (Level 4)","Advanced (Level 5)"], key="chat_level_select")
    scenario = st.selectbox("Practice scenario", ["Free conversation","Job interview practice","Shopping at a store","Meeting someone new","Asking for directions","At a doctor's office","Calling customer service"])
    st.markdown("""<div class="step-card" style="padding:16px 20px"><div class="step-label">How it works</div><div style="font-size:0.88rem;color:#555;line-height:1.7">Type in English and the AI will:<br>✅ Respond naturally<br>✅ Correct any mistakes<br>✅ Explain why something is wrong<br>✅ Match your level</div></div>""", unsafe_allow_html=True)
    if st.button("Clear Chat", key="clear_chat"):
        st.session_state.chat_messages = []
        st.rerun()

with col_left:
    st.markdown("### Conversation")
    if not st.session_state.chat_messages:
        st.markdown("""<div style="text-align:center;padding:40px;color:#888;border:2px dashed #d0c8b8"><div style="font-size:2rem;margin-bottom:8px">💬</div><div style="font-family:'Syne',sans-serif;font-weight:700">Start the conversation!</div><div style="font-size:0.88rem;margin-top:4px">Type something below to begin practicing.</div></div>""", unsafe_allow_html=True)
    else:
        for msg in st.session_state.chat_messages:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-user">🧑 {msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-ai">🤖 {msg["content"]}</div>', unsafe_allow_html=True)

    user_input = st.text_input("Type your message in English...", key="chat_input", label_visibility="collapsed", placeholder="Type your message in English...")

    if st.button("Send →", key="chat_send") and user_input.strip():
        st.session_state.chat_messages.append({"role": "user", "content": user_input.strip()})
        level_instructions = {
            "Beginner (Level 1)": "Use very simple words and short sentences. Avoid complex grammar.",
            "Elementary (Level 2)": "Use simple sentences. Introduce basic grammar. Be encouraging.",
            "Intermediate (Level 3)": "Use normal conversational English. Correct major errors.",
            "Upper Intermediate (Level 4)": "Use natural English. Correct subtle errors. Introduce professional vocabulary.",
            "Advanced (Level 5)": "Use rich natural English including idioms. Correct any errors precisely.",
        }
        system_prompt = f"""You are Echo, a friendly English conversation tutor on Echo English — a platform for non-native English speakers.

Student level: {chat_level}
Scenario: {scenario}

Instructions:
1. Respond naturally within the scenario.
2. End every response with a "📝 Feedback:" section:
   - Point out grammar or vocabulary mistakes kindly
   - Suggest a better way to say it if needed
   - Give one short tip or encouragement
3. {level_instructions.get(chat_level, "")}

Format:
[Your conversational response]

📝 Feedback:
[Correction and tip — 2-3 lines max]"""

        try:
            api_key = st.secrets["ANTHROPIC_API_KEY"]
            history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_messages]
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers={"Content-Type": "application/json", "x-api-key": api_key, "anthropic-version": "2023-06-01"},
                json={"model": "claude-sonnet-4-20250514", "max_tokens": 1000, "system": system_prompt, "messages": history},
            )
            data = response.json()
            ai_text = data["content"][0]["text"]
        except Exception as e:
            ai_text = f"Sorry, I couldn't connect right now. Please try again. (Error: {e})"

        st.session_state.chat_messages.append({"role": "assistant", "content": ai_text})
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:#1a1a1a;color:#f5f0e8;text-align:center;padding:40px">
  <div style="font-family:'Syne',sans-serif;font-weight:800;font-size:1.4rem;color:#e85d2f;margin-bottom:8px">🔊 Echo English</div>
  <div style="color:#888;font-size:0.85rem;margin-bottom:16px">Learn at your own pace · Zero ads · Powered by AI · Created by Connor Burdick</div>
  <div style="display:flex;justify-content:center;gap:32px;font-size:0.8rem;color:#555">
    <span>5 Learning Levels</span><span>·</span><span>AI Conversation Partner</span><span>·</span><span>Progress Tracker</span><span>·</span><span>Placement Quiz</span>
  </div>
</div>
""", unsafe_allow_html=True)
