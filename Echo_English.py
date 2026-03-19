import streamlit as st

st.set_page_config(
    page_title="Business Concept Builder",
    page_icon="💡",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Karla:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'Karla', sans-serif; }

.stApp {
    background: #f5f0e8;
    color: #1a1a1a;
}

[data-testid="stSidebar"] {
    background: #1a1a1a !important;
}
[data-testid="stSidebar"] * { color: #f5f0e8 !important; }
[data-testid="stSidebar"] .stRadio label { color: #f5f0e8 !important; }

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

.step-card {
    background: #ffffff;
    border-radius: 0px;
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
    border-radius: 0px;
    padding: 14px 18px;
    margin: 10px 0;
    font-size: 0.95rem;
    line-height: 1.6;
    border-bottom: 2px solid #1a1a1a;
}

.question-label {
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: #888;
    margin-bottom: 4px;
}

.pill {
    display: inline-block;
    background: #1a1a1a;
    color: #f5f0e8;
    border-radius: 0px;
    padding: 5px 14px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin: 4px 4px 4px 0;
}

.pill-outline {
    display: inline-block;
    border: 2px solid #1a1a1a;
    color: #1a1a1a;
    border-radius: 0px;
    padding: 4px 14px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin: 4px 4px 4px 0;
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

.competitor-card {
    background: #fff;
    border: 2px solid #1a1a1a;
    padding: 16px 20px;
    margin: 8px 0;
    box-shadow: 3px 3px 0px #1a1a1a;
}

.check-item {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    margin: 8px 0;
    font-size: 0.95rem;
}

.check-icon { color: #e85d2f; font-weight: 800; font-size: 1rem; margin-top: 1px; }

.reflection-box {
    background: #1a1a1a;
    color: #f5f0e8;
    padding: 28px 32px;
    margin-top: 8px;
    font-size: 1rem;
    line-height: 1.7;
    font-style: italic;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 💡 Business Concept")
    st.markdown("---")
    page = st.radio(
        "Navigate",
        [
            "🏠 Overview",
            "❗ Step 1 – Problem",
            "🔍 Step 2 – Existing Solutions",
            "✅ Step 3 – Your Solution",
            "⚡ Step 4 – Why Better",
            "🚀 Step 5 – Delivery Plan",
            "👤 Step 6 – First Customer",
            "💬 Reflection",
        ],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown("**Creator:** Connor Burdick")
    st.markdown("**Product:** AI English Learning Platform")


# ══════════════════════════════════════════════════════════════════════════════
# OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
if page == "🏠 Overview":
    st.markdown('<div class="hero-badge">Business Concept Builder — Part 1</div>', unsafe_allow_html=True)
    st.title("An AI-Powered English Learning Platform")
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
          <div class="step-label">The Gap</div>
          <div class="step-title">Existing Tools Fall Short</div>
          Duolingo is gamified fluff. Classes are expensive and rigid. No option is truly personalized and free.
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="step-card" style="position:relative">
          <div class="big-number">3</div>
          <div class="step-label">The Solution</div>
          <div class="step-title">AI-Driven Platform</div>
          A website with a built-in AI tutor — personalized lessons, 24/7 access, zero ads, your own pace.
        </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown("### All 6 Steps at a Glance")

    steps = [
        ("01", "Problem", "Language barrier for non-native English speakers"),
        ("02", "Existing Solutions", "Duolingo, paid classes, SpanishDict — all with flaws"),
        ("03", "Your Solution", "Personalized AI English platform, no ads"),
        ("04", "Why Better", "Fully personalized, goal-driven learning"),
        ("05", "Delivery Plan", "Online, on-demand — needs funding & domain"),
        ("06", "First Customer", "Non-English-speaking friends via free trial"),
    ]
    for num, title, desc in steps:
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:20px;padding:12px 0;border-bottom:1px solid #d0c8b8">
          <span style="font-family:'Syne',sans-serif;font-weight:800;font-size:1.2rem;color:#e85d2f;min-width:36px">{num}</span>
          <span style="font-family:'Syne',sans-serif;font-weight:700;min-width:180px">{title}</span>
          <span style="color:#555;font-size:0.9rem">{desc}</span>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# STEP 1 – PROBLEM
# ══════════════════════════════════════════════════════════════════════════════
elif page == "❗ Step 1 – Problem":
    st.markdown('<div class="hero-badge">Step 1</div>', unsafe_allow_html=True)
    st.title("The Problem")
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    st.markdown("""
    <div class="step-card">
      <div class="step-label">Core Problem</div>
      <div class="step-title">Language Barrier in English-Speaking Countries</div>
      <div class="answer-block">
        People living in English-speaking countries can't hold a conversation and/or get a job because of the language barrier.
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="step-card">
      <div class="step-label">Who Has This Problem?</div>
      <div class="step-title">The Target Population</div>
      <div class="answer-block">
        People whose <strong>first language isn't English</strong> and who are living in primarily English-speaking countries.
        This includes immigrants, refugees, international students, and expats navigating daily life and the job market.
      </div>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Why this matters")
        for item in [
            "Job opportunities require conversational English",
            "Daily life (shopping, healthcare, transport) demands it",
            "Social inclusion depends on communication",
            "Existing tools don't solve the real conversational gap",
        ]:
            st.markdown(f"""
            <div class="check-item">
              <span class="check-icon">→</span>
              <span>{item}</span>
            </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("#### Who specifically?")
        groups = ["Immigrants", "Refugees", "International Students", "Expats", "Foreign Workers"]
        for g in groups:
            st.markdown(f'<span class="pill">{g}</span>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# STEP 2 – EXISTING SOLUTIONS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🔍 Step 2 – Existing Solutions":
    st.markdown('<div class="hero-badge">Step 2</div>', unsafe_allow_html=True)
    st.title("Existing Solutions")
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    st.markdown("### Current Alternatives")
    competitors = [
        ("🦉 Duolingo", "Gamified language app", "Addictive streak mechanics, not real learning. Doesn't build true conversational ability."),
        ("🏫 English Classes", "In-person or group instruction", "Expensive, fixed schedule, doesn't go at your own pace. Hard to access for working adults."),
        ("📖 SpanishDict", "Translation & vocabulary tool", "Primarily a dictionary/translator — no conversational practice or structured learning path."),
    ]
    for icon_name, subtitle, flaw in competitors:
        st.markdown(f"""
        <div class="competitor-card">
          <div style="display:flex;justify-content:space-between;align-items:flex-start">
            <div>
              <div style="font-family:'Syne',sans-serif;font-weight:800;font-size:1.1rem">{icon_name}</div>
              <div style="color:#888;font-size:0.85rem;margin-bottom:8px">{subtitle}</div>
            </div>
            <span class="pill-outline">Competitor</span>
          </div>
          <div style="color:#c0392b;font-size:0.9rem"><strong>❌ Problem:</strong> {flaw}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown("### What's Frustrating or Missing?")
    st.markdown("""
    <div class="step-card">
      <div class="answer-block">
        Existing solutions either <strong>have ads</strong>, <strong>cost a lot of money</strong>, or simply <strong>don't work</strong> for real conversation.
        Classes don't go at your own pace. Duolingo is more of an adrenaline rush that keeps people hooked — it doesn't
        actually build the skills needed to hold a real English conversation or interview for a job.
      </div>
    </div>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Duolingo Ads", "Present (free tier)", "Major friction")
    col2.metric("Class Cost", "$50–200/mo", "Barrier to entry")
    col3.metric("Real Convo Prep", "Minimal", "Core gap")


# ══════════════════════════════════════════════════════════════════════════════
# STEP 3 – YOUR SOLUTION
# ══════════════════════════════════════════════════════════════════════════════
elif page == "✅ Step 3 – Your Solution":
    st.markdown('<div class="hero-badge">Step 3</div>', unsafe_allow_html=True)
    st.title("Your Solution Idea")
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    st.markdown("""
    <div class="step-card">
      <div class="step-label">Product / Service</div>
      <div class="step-title">AI-Powered English Learning Website</div>
      <div class="answer-block">
        A website similar to Duolingo, except it goes <strong>solely at your own pace</strong> and is focused entirely
        on helping people <strong>speak and listen to real English conversations</strong> — so they can understand
        what's going on in daily life, work, and social settings.
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("### What Does the Customer Receive?")
    features = [
        ("🤖", "Built-in AI Tutor", "A personal AI that adapts to your level and learning speed"),
        ("📋", "Customized Assignments", "Lessons tailored to your specific goals and weak areas"),
        ("🕐", "24/7 Availability", "Learn anytime — no schedule, no waiting for a teacher"),
        ("🚫", "Zero Ads", "Completely ad-free experience — learning first, always"),
        ("👤", "Personal Account", "Track your progress, revisit lessons, set goals"),
    ]
    col1, col2 = st.columns(2)
    for i, (icon, title, desc) in enumerate(features):
        col = col1 if i % 2 == 0 else col2
        col.markdown(f"""
        <div class="step-card" style="padding:20px 24px">
          <div style="font-size:1.5rem;margin-bottom:8px">{icon}</div>
          <div style="font-family:'Syne',sans-serif;font-weight:700;margin-bottom:4px">{title}</div>
          <div style="color:#555;font-size:0.9rem">{desc}</div>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# STEP 4 – WHY BETTER
# ══════════════════════════════════════════════════════════════════════════════
elif page == "⚡ Step 4 – Why Better":
    st.markdown('<div class="hero-badge">Step 4</div>', unsafe_allow_html=True)
    st.title("Why Is Your Solution Better?")
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    advantages = [
        ("More Personalized", True, "Fully adaptive AI — every lesson fits the individual learner's needs and pace"),
        ("Higher Quality", True, "Focus on real conversation and listening, not gamified streaks"),
        ("Faster / More Convenient", True, "On-demand, 24/7, no commute, no scheduling"),
        ("Easier to Use", True, "Clean interface, no distracting ads, no complexity"),
        ("Cheaper", False, "Pricing model still TBD — but goal is accessible pricing"),
    ]

    for label, checked, explanation in advantages:
        icon = "✅" if checked else "⬜"
        border = "#e85d2f" if checked else "#ccc"
        st.markdown(f"""
        <div class="step-card" style="border-left-color:{border};margin-bottom:12px;padding:18px 24px">
          <div style="display:flex;align-items:center;gap:12px">
            <span style="font-size:1.2rem">{icon}</span>
            <div>
              <div style="font-family:'Syne',sans-serif;font-weight:700">{label}</div>
              <div style="color:#555;font-size:0.9rem;margin-top:2px">{explanation}</div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown("""
    <div class="step-card">
      <div class="step-label">Core Explanation</div>
      <div class="step-title">Personalization Is the Goal</div>
      <div class="answer-block">
        Our main goal is allowing people to <strong>actually learn</strong> — and the best way to do that is with
        fully personalized lessons and achievable goals to reach. One-size-fits-all doesn't work for language learning.
      </div>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# STEP 5 – DELIVERY PLAN
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🚀 Step 5 – Delivery Plan":
    st.markdown('<div class="hero-badge">Step 5</div>', unsafe_allow_html=True)
    st.title("Delivery Plan")
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### How It's Delivered")
        delivery = [
            ("🌐", "Online", True),
            ("📲", "On Demand", True),
            ("📅", "Scheduled", False),
            ("🤝", "In Person", False),
        ]
        for icon, label, selected in delivery:
            bg = "#1a1a1a" if selected else "#fff"
            color = "#f5f0e8" if selected else "#1a1a1a"
            border = "#1a1a1a"
            st.markdown(f"""
            <div style="background:{bg};color:{color};border:2px solid {border};
                        padding:14px 20px;margin:8px 0;font-family:'Syne',sans-serif;
                        font-weight:700;display:flex;align-items:center;gap:12px">
              <span>{icon}</span> {label}
              {'<span style="margin-left:auto;font-size:0.7rem;letter-spacing:1px">SELECTED</span>' if selected else ''}
            </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("### Tools & Resources Needed")
        needs = [
            ("💰", "Funding / Money"),
            ("🌐", "Domain Name"),
            ("💻", "Website Development"),
            ("🤖", "Working AI Integration"),
            ("💳", "Payment Processing"),
            ("📢", "Advertising"),
            ("👥", "Consumers / Users"),
        ]
        for icon, item in needs:
            st.markdown(f"""
            <div class="check-item">
              <span style="font-size:1rem">{icon}</span>
              <span>{item}</span>
            </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown("### Could You Do This in a Week?")
    st.markdown("""
    <div class="step-card" style="border-left-color:#c0392b">
      <div style="display:flex;align-items:center;gap:12px">
        <span style="font-size:2rem">❌</span>
        <div>
          <div style="font-family:'Syne',sans-serif;font-weight:800">No — Not Without Funding</div>
          <div style="color:#555;font-size:0.9rem;margin-top:4px">
            Without significant funding or a donation, launching within a week isn't realistic.
            The main blocker is capital for development, AI integration, and infrastructure.
          </div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# STEP 6 – FIRST CUSTOMER
# ══════════════════════════════════════════════════════════════════════════════
elif page == "👤 Step 6 – First Customer":
    st.markdown('<div class="hero-badge">Step 6</div>', unsafe_allow_html=True)
    st.title("Your First Customer")
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="step-card">
          <div class="step-label">Who?</div>
          <div class="step-title">Non-English-Speaking Friends</div>
          <div class="answer-block">
            The very first customers would be <strong>friends who don't speak English as their first language</strong>.
            A known, trusted group — perfect for getting honest early feedback.
          </div>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="step-card">
          <div class="step-label">How to Reach Them?</div>
          <div class="step-title">Free Trial Offer</div>
          <div class="answer-block">
            Approach them directly and <strong>offer a free trial</strong> of the platform.
            Word-of-mouth from a trusted first group can spark organic growth.
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown("### Early Adoption Strategy")
    steps_go = [
        ("1", "Identify 5–10 non-English-speaking friends"),
        ("2", "Offer completely free access as beta testers"),
        ("3", "Collect feedback on what works and what doesn't"),
        ("4", "Iterate on the product based on real usage"),
        ("5", "Use their success stories as social proof"),
    ]
    for num, step in steps_go:
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:16px;padding:12px 0;border-bottom:1px solid #d0c8b8">
          <span style="background:#e85d2f;color:#fff;font-family:'Syne',sans-serif;font-weight:800;
                       width:32px;height:32px;display:flex;align-items:center;justify-content:center;
                       flex-shrink:0;font-size:0.9rem">{num}</span>
          <span>{step}</span>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# REFLECTION
# ══════════════════════════════════════════════════════════════════════════════
elif page == "💬 Reflection":
    st.markdown('<div class="hero-badge">Reflection</div>', unsafe_allow_html=True)
    st.title("Why This Idea Feels Realistic")
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    st.markdown("""
    <div class="reflection-box">
      "Because it can help anyone out."
    </div>""", unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown("### Breaking It Down")
    points = [
        ("🌍", "Universal Need", "Language barriers affect hundreds of millions of people worldwide — the market is enormous and real."),
        ("🧑‍💻", "Accessible Tech", "AI language tools already exist — this is about packaging them into something purposeful and user-first."),
        ("🎯", "Clear Focus", "Unlike competitors that try to teach many languages broadly, this is laser-focused: English conversation for non-native speakers."),
        ("💡", "Personal Connection", "The creator has real people in mind — friends who face this exact problem — making the idea grounded, not abstract."),
    ]
    for icon, title, desc in points:
        st.markdown(f"""
        <div class="step-card" style="padding:20px 24px">
          <div style="display:flex;gap:16px;align-items:flex-start">
            <span style="font-size:1.6rem">{icon}</span>
            <div>
              <div style="font-family:'Syne',sans-serif;font-weight:700;margin-bottom:4px">{title}</div>
              <div style="color:#555;font-size:0.9rem">{desc}</div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown("### Summary: Business Concept Scorecard")
    col1, col2, col3 = st.columns(3)
    col1.metric("Problem Clarity", "9/10", "Well-defined & specific")
    col2.metric("Solution Originality", "8/10", "AI personalization edge")
    col3.metric("Market Potential", "10/10", "Massive global need")

