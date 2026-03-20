import streamlit as st
import requests
import datetime
import random
import io
import base64

st.set_page_config(page_title="Echo English", page_icon="🔊", layout="wide")

for key, default in {
    "chat_messages": [],
    "progress": {1: False, 2: False, 3: False, 4: False, 5: False},
    "scores": {1: None, 2: None, 3: None, 4: None, 5: None},
    "placement_done": False,
    "placement_result": None,
    "placement_answers": {},
    "streak": 0,
    "last_practice_date": None,
    "dark_mode": False,
    "flashcard_index": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
    "flashcard_flipped": False,
    "quick_review_questions": [],
    "quick_review_answers": {},
    "quick_review_done": False,
    "cert_name": "",
    "feedback_submitted": False,
    "xp": 0,
    "badges": [],
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

def award_xp(amount):
    st.session_state.xp += amount

def check_badges():
    badges = st.session_state.badges
    xp = st.session_state.xp
    completed = sum(st.session_state.progress.values())
    streak = st.session_state.streak
    new_badges = []
    all_possible = [
        ("🌱","First Steps","Complete your first quiz",lambda: completed>=1),
        ("📚","Scholar","Complete 3 levels",lambda: completed>=3),
        ("🏆","Graduate","Complete all 5 levels",lambda: completed>=5),
        ("🔥","On Fire","Reach a 3-day streak",lambda: streak>=3),
        ("⚡","Lightning Learner","Earn 100 XP",lambda: xp>=100),
        ("💎","Diamond Student","Earn 300 XP",lambda: xp>=300),
        ("🎯","Sharp Shooter","Score 6/6 on any quiz",lambda: any(s==6 for s in st.session_state.scores.values() if s)),
        ("🌟","All Star","Complete all levels with 6/6",lambda: all(st.session_state.scores.get(i)==6 for i in range(1,6))),
    ]
    for icon,name,desc,condition in all_possible:
        if name not in [b[1] for b in badges]:
            if condition():
                new_badges.append((icon,name,desc))
                st.session_state.badges.append((icon,name,desc))
    return new_badges

def xp_level(xp):
    if xp<50:   return 1,"Newcomer",50
    if xp<150:  return 2,"Explorer",150
    if xp<300:  return 3,"Learner",300
    if xp<500:  return 4,"Practitioner",500
    if xp<750:  return 5,"Achiever",750
    return 6,"Master",999999

def update_streak():
    today = datetime.date.today()
    last = st.session_state.last_practice_date
    if last is None: st.session_state.streak=1
    elif last==today: pass
    elif last==today-datetime.timedelta(days=1): st.session_state.streak+=1
    else: st.session_state.streak=1
    st.session_state.last_practice_date=today

WORD_OF_DAY_LIST=[
    ("Persevere","verb","To continue doing something despite difficulty.","She persevered through the hard exam and passed."),
    ("Eloquent","adjective","Fluent and persuasive in speaking or writing.","He gave an eloquent speech at the ceremony."),
    ("Negotiate","verb","To discuss something to reach an agreement.","They negotiated a better salary offer."),
    ("Resilient","adjective","Able to recover quickly from difficulties.","She was resilient after losing her job."),
    ("Collaborate","verb","To work jointly with others.","The two teams collaborated on the project."),
    ("Initiative","noun","The ability to take action independently.","She showed great initiative by solving the problem herself."),
    ("Concise","adjective","Giving a lot of information clearly in few words.","His email was concise and easy to understand."),
    ("Diligent","adjective","Showing careful and hard work.","He was diligent in studying every day."),
    ("Articulate","adjective","Able to express ideas clearly and effectively.","She was articulate during the job interview."),
    ("Versatile","adjective","Able to adapt or be used in many ways.","A versatile employee can do many different tasks."),
    ("Punctual","adjective","Happening or doing something at the agreed time.","Always be punctual to job interviews."),
    ("Empathy","noun","The ability to understand another person's feelings.","Good managers show empathy toward their team."),
    ("Proficient","adjective","Competent or skilled in doing something.","She is proficient in English and Spanish."),
    ("Ambiguous","adjective","Open to more than one interpretation.","The instructions were ambiguous so I asked for clarification."),
    ("Dedicate","verb","To devote time or effort to a task.","He dedicated himself to learning English every day."),
    ("Constructive","adjective","Serving a useful purpose; helpful.","Her feedback was constructive and helped me improve."),
    ("Fluent","adjective","Able to speak a language easily and accurately.","After two years of practice, she became fluent in English."),
    ("Persistent","adjective","Continuing firmly despite obstacles.","Being persistent is key to learning a new language."),
    ("Candidate","noun","A person applying for a job or position.","She was the strongest candidate for the role."),
    ("Impression","noun","An idea or feeling formed about someone.","Make a good impression in your first week at work."),
    ("Inquire","verb","To ask for information.","He inquired about the job opening at the front desk."),
    ("Clarify","verb","To make something less confusing.","Could you clarify what you mean by that?"),
    ("Acknowledge","verb","To accept or recognize something.","She acknowledged the mistake and apologized."),
    ("Delegate","verb","To give a task to someone else to do.","A good manager delegates work to the right people."),
    ("Optimistic","adjective","Hopeful and confident about the future.","Stay optimistic — learning a language takes time."),
    ("Adapt","verb","To adjust to new conditions.","It took time to adapt to life in a new country."),
    ("Efficient","adjective","Achieving results with little waste of effort.","She found an efficient way to study vocabulary."),
    ("Commitment","noun","The state of being dedicated to something.","Learning English requires commitment every day."),
    ("Opportunity","noun","A chance for advancement or progress.","Moving abroad was a great opportunity for her career."),
    ("Accomplish","verb","To achieve something successfully.","He accomplished his goal of speaking fluent English."),
    ("Confident","adjective","Feeling certain about your own abilities.","Practice until you feel confident speaking English."),
    ("Professional","adjective","Relating to a skilled occupation.","She dressed professionally for the interview."),
    ("Encourage","verb","To give someone support or confidence.","Her teacher encouraged her to keep practicing."),
    ("Introduce","verb","To present someone to another person.","Let me introduce you to my manager."),
    ("Recommend","verb","To suggest something as good or suitable.","Can you recommend a good English course?"),
    ("Resolve","verb","To settle or find a solution to a problem.","We quickly resolved the misunderstanding."),
    ("Maintain","verb","To keep something at the same level.","It is important to maintain a positive attitude."),
    ("Achieve","verb","To successfully reach a goal.","You will achieve fluency with consistent practice."),
    ("Demonstrate","verb","To show how something works.","She demonstrated her skills during the interview."),
    ("Suitable","adjective","Right or appropriate for a situation.","Make sure your clothes are suitable for the interview."),
    ("Genuine","adjective","Truly what it appears to be; sincere.","Give a genuine answer when asked about your strengths."),
    ("Summarize","verb","To give a brief statement of the main points.","Can you summarize what was discussed in the meeting?"),
    ("Flexible","adjective","Willing to change or adapt.","Employers value workers who are flexible."),
    ("Assertive","adjective","Confident and direct in expressing opinions.","Be assertive but polite in negotiations."),
    ("Network","verb","To interact with others to exchange information.","Networking is important for finding jobs."),
    ("Reliable","adjective","Consistently good in quality or performance.","She is reliable and always meets her deadlines."),
    ("Feedback","noun","Information about reactions to a product or performance.","Ask for feedback after your first week at work."),
    ("Navigate","verb","To find the way through a complex situation.","She learned to navigate life in a new country."),
    ("Contribute","verb","To give something to help achieve something.","Everyone can contribute ideas in the meeting."),
]
day_of_year=datetime.date.today().timetuple().tm_yday
wotd=WORD_OF_DAY_LIST[day_of_year%len(WORD_OF_DAY_LIST)]

def generate_certificate(name):
    from reportlab.lib.pagesizes import landscape,A4
    from reportlab.pdfgen import canvas
    from reportlab.lib import colors
    buf=io.BytesIO()
    w,h=landscape(A4)
    c=canvas.Canvas(buf,pagesize=landscape(A4))
    c.setFillColor(colors.HexColor("#f5f0e8"))
    c.rect(0,0,w,h,fill=1,stroke=0)
    c.setStrokeColor(colors.HexColor("#1a1a1a"))
    c.setLineWidth(8)
    c.rect(24,24,w-48,h-48,fill=0,stroke=1)
    c.setLineWidth(2)
    c.setStrokeColor(colors.HexColor("#e85d2f"))
    c.rect(34,34,w-68,h-68,fill=0,stroke=1)
    c.setFillColor(colors.HexColor("#e85d2f"))
    c.rect(34,h-90,w-68,10,fill=1,stroke=0)
    c.setFillColor(colors.HexColor("#1a1a1a"))
    c.setFont("Helvetica-Bold",13)
    c.drawCentredString(w/2,h-120,"ECHO ENGLISH")
    c.setFont("Helvetica",10)
    c.setFillColor(colors.HexColor("#e85d2f"))
    c.drawCentredString(w/2,h-140,"CERTIFICATE OF COMPLETION")
    c.setStrokeColor(colors.HexColor("#1a1a1a"))
    c.setLineWidth(1)
    c.line(w/2-180,h-155,w/2+180,h-155)
    c.setFillColor(colors.HexColor("#555555"))
    c.setFont("Helvetica",11)
    c.drawCentredString(w/2,h-185,"This is to certify that")
    c.setFillColor(colors.HexColor("#1a1a1a"))
    c.setFont("Helvetica-Bold",32)
    dn=name if name.strip() else "Your Name"
    c.drawCentredString(w/2,h-230,dn)
    nw=c.stringWidth(dn,"Helvetica-Bold",32)
    c.setStrokeColor(colors.HexColor("#e85d2f"))
    c.setLineWidth(2)
    c.line(w/2-nw/2,h-238,w/2+nw/2,h-238)
    c.setFillColor(colors.HexColor("#555555"))
    c.setFont("Helvetica",11)
    c.drawCentredString(w/2,h-265,"has successfully completed all 5 levels of the")
    c.setFont("Helvetica-Bold",13)
    c.setFillColor(colors.HexColor("#1a1a1a"))
    c.drawCentredString(w/2,h-288,"Echo English Language Program")
    c.setFont("Helvetica",10)
    c.setFillColor(colors.HexColor("#555555"))
    c.drawCentredString(w/2,h-308,"Demonstrating proficiency from Beginner through Advanced English")
    ll=["Level 1\nBeginner","Level 2\nElementary","Level 3\nIntermediate","Level 4\nUpper Int.","Level 5\nAdvanced"]
    lc=["#3b82f6","#22c55e","#f59e0b","#ef4444","#8b5cf6"]
    bw=90
    tw=len(ll)*bw+(len(ll)-1)*12
    sx=(w-tw)/2
    for i,(lbl,col) in enumerate(zip(ll,lc)):
        bx=sx+i*(bw+12)
        c.setFillColor(colors.HexColor(col))
        c.rect(bx,h-380,bw,44,fill=1,stroke=0)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold",8)
        lines=lbl.split("\n")
        c.drawCentredString(bx+bw/2,h-356,lines[0])
        c.setFont("Helvetica",7)
        c.drawCentredString(bx+bw/2,h-368,lines[1])
    c.setFillColor(colors.HexColor("#888888"))
    c.setFont("Helvetica",9)
    c.drawCentredString(w/2,h-408,f"Issued on {datetime.date.today().strftime('%B %d, %Y')}")
    c.setStrokeColor(colors.HexColor("#1a1a1a"))
    c.setLineWidth(1)
    c.line(w/2-100,h-440,w/2+100,h-440)
    c.setFont("Helvetica-Bold",9)
    c.setFillColor(colors.HexColor("#1a1a1a"))
    c.drawCentredString(w/2,h-454,"Connor Burdick")
    c.setFont("Helvetica",8)
    c.setFillColor(colors.HexColor("#888888"))
    c.drawCentredString(w/2,h-466,"Founder, Echo English")
    c.setFillColor(colors.HexColor("#e85d2f"))
    c.rect(34,34,w-68,10,fill=1,stroke=0)
    c.save()
    buf.seek(0)
    return buf.read()

dm=st.session_state.dark_mode
bg="#1a1a1a" if dm else "#f5f0e8"
fg="#f5f0e8" if dm else "#1a1a1a"
card_bg="#2a2a2a" if dm else "#ffffff"
sub_bg="#111111" if dm else "#f5f0e8"
border="#3a3a3a" if dm else "#1a1a1a"
muted="#aaaaaa" if dm else "#555555"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Karla:wght@300;400;500&display=swap');
html,body,[class*="css"]{{font-family:'Karla',sans-serif;}}
.stApp{{background:{bg};color:{fg};}}
[data-testid="stSidebar"]{{display:none;}}
[data-testid="collapsedControl"]{{display:none;}}
h1{{font-family:'Syne',sans-serif!important;font-weight:800!important;font-size:3rem!important;line-height:1.1!important;color:{fg}!important;}}
h2,h3{{font-family:'Syne',sans-serif!important;font-weight:700!important;color:{fg}!important;}}
.navbar{{position:sticky;top:0;z-index:999;background:#1a1a1a;padding:10px 32px;display:flex;align-items:center;gap:14px;flex-wrap:wrap;}}
.navbar a{{color:#f5f0e8;text-decoration:none;font-family:'Syne',sans-serif;font-weight:700;font-size:0.64rem;letter-spacing:1.5px;text-transform:uppercase;opacity:0.65;}}
.navbar a:hover{{opacity:1;}}
.navbar-brand{{color:#e85d2f!important;opacity:1!important;font-size:0.95rem!important;margin-right:8px;}}
.section-wrap{{padding:56px 40px;border-bottom:2px solid {border};}}
.hero-section{{background:#1a1a1a;color:#f5f0e8;padding:90px 48px 72px;}}
.hero-badge{{background:#e85d2f;color:white;display:inline-block;padding:6px 16px;font-family:'Syne',sans-serif;font-size:0.72rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;margin-bottom:20px;}}
.divider{{border:none;border-top:2px solid {border};margin:28px 0;}}
.step-card{{background:{card_bg};border-left:5px solid #e85d2f;padding:24px 28px;margin-bottom:20px;box-shadow:4px 4px 0px {border};}}
.step-label{{font-family:'Syne',sans-serif;font-size:0.68rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:#e85d2f;margin-bottom:6px;}}
.step-title{{font-family:'Syne',sans-serif;font-size:1.3rem;font-weight:800;color:{fg};margin-bottom:14px;}}
.vocab-word{{background:{border};color:{bg};display:inline-block;padding:5px 12px;font-family:'Syne',sans-serif;font-weight:700;font-size:0.85rem;margin:3px 3px 3px 0;}}
.phrase-box{{background:{sub_bg};border-left:4px solid #e85d2f;padding:10px 14px;margin:6px 0;font-size:0.92rem;line-height:1.5;color:{fg};}}
.lesson-card{{background:{card_bg};border:2px solid {border};padding:18px 22px;margin-bottom:14px;box-shadow:3px 3px 0px {border};}}
.chat-user{{background:#1a1a1a;color:#f5f0e8;padding:12px 16px;margin:6px 0;text-align:right;font-size:0.93rem;white-space:pre-wrap;}}
.chat-ai{{background:{card_bg};border:2px solid {border};color:{fg};padding:12px 16px;margin:6px 0;font-size:0.93rem;box-shadow:2px 2px 0px {border};white-space:pre-wrap;}}
.progress-bar-wrap{{background:{'#3a3a3a' if dm else '#d0c8b8'};height:12px;width:100%;margin:6px 0 2px;}}
.progress-bar-fill{{background:#e85d2f;height:12px;}}
.progress-level-card{{background:{card_bg};border:2px solid {border};padding:14px 18px;margin-bottom:8px;box-shadow:3px 3px 0px {border};display:flex;align-items:center;gap:14px;}}
.before-after{{display:grid;grid-template-columns:1fr 1fr;gap:0;border:2px solid {border};box-shadow:4px 4px 0px {border};margin-bottom:20px;}}
.before-col{{background:{card_bg};padding:20px;border-right:2px solid {border};}}
.after-col{{background:#1a1a1a;color:#f5f0e8;padding:20px;}}
.ba-label{{font-family:'Syne',sans-serif;font-size:0.68rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;margin-bottom:10px;}}
.wotd-card{{background:#e85d2f;color:white;padding:24px 32px;margin-bottom:0;}}
.flashcard{{background:{card_bg};border:3px solid {border};padding:48px 32px;text-align:center;box-shadow:6px 6px 0px {border};min-height:180px;display:flex;align-items:center;justify-content:center;flex-direction:column;}}
.streak-badge{{background:#f59e0b;color:white;display:inline-block;padding:6px 18px;font-family:'Syne',sans-serif;font-weight:800;font-size:0.9rem;letter-spacing:1px;}}
.xp-badge{{background:#8b5cf6;color:white;display:inline-block;padding:6px 18px;font-family:'Syne',sans-serif;font-weight:800;font-size:0.9rem;letter-spacing:1px;margin-left:8px;}}
.badge-card{{background:{card_bg};border:2px solid {border};padding:16px 20px;text-align:center;box-shadow:3px 3px 0px {border};}}
.mistake-card{{background:{card_bg};border-left:5px solid #ef4444;padding:18px 22px;margin-bottom:14px;box-shadow:3px 3px 0px {border};}}
.mistake-wrong{{background:#fef2f2;border-left:4px solid #ef4444;padding:10px 14px;margin:6px 0;font-size:0.92rem;color:#c0392b;}}
.mistake-right{{background:#f0fdf4;border-left:4px solid #22c55e;padding:10px 14px;margin:6px 0;font-size:0.92rem;color:#166534;}}
.job-pack-card{{background:{card_bg};border:2px solid {border};padding:20px 24px;margin-bottom:14px;box-shadow:3px 3px 0px {border};}}
.search-result{{background:{card_bg};border:2px solid {border};padding:14px 18px;margin-bottom:8px;box-shadow:2px 2px 0px {border};}}
div[data-testid="stButton"] button{{background:#e85d2f!important;color:white!important;border:none!important;border-radius:0!important;font-family:'Syne',sans-serif!important;font-weight:700!important;letter-spacing:1px!important;padding:10px 22px!important;box-shadow:3px 3px 0px {border}!important;}}
[data-testid="stMetricValue"]{{font-family:'Syne',sans-serif!important;font-weight:800!important;color:{fg}!important;}}
[data-testid="stMetricLabel"]{{color:{muted}!important;}}
p,li,span{{color:{fg};}}
.stRadio label{{color:{fg}!important;}}
.stTextInput input{{background:{card_bg}!important;color:{fg}!important;border:2px solid {border}!important;border-radius:0!important;}}
.stTabs [data-baseweb="tab-list"]{{background:{card_bg};border-bottom:2px solid {border};}}
.stTabs [data-baseweb="tab"]{{color:{muted}!important;font-family:'Syne',sans-serif!important;font-weight:700!important;}}
.stTabs [aria-selected="true"]{{color:#e85d2f!important;border-bottom:3px solid #e85d2f!important;}}
.stExpander{{background:{card_bg}!important;border:1px solid {border}!important;}}
</style>
""",unsafe_allow_html=True)

st.markdown("""
<div class="navbar">
  <a class="navbar-brand" href="#hero">🔊 Echo English</a>
  <a href="#placement">Placement</a>
  <a href="#progress">Progress</a>
  <a href="#xp">XP & Badges</a>
  <a href="#stories">Stories</a>
  <a href="#level-1">L1</a>
  <a href="#level-2">L2</a>
  <a href="#level-3">L3</a>
  <a href="#level-4">L4</a>
  <a href="#level-5">L5</a>
  <a href="#job-packs">Job Packs</a>
  <a href="#mistakes">Mistakes</a>
  <a href="#search">Search</a>
  <a href="#flashcards">Flashcards</a>
  <a href="#quick-review">Review</a>
  <a href="#ai-chat">AI Partner</a>
  <a href="#certificate">Certificate</a>
  <a href="#pronunciation">Pronunciation</a>
  <a href="#grammar">Grammar</a>
  <a href="#about">About</a>
</div>
""",unsafe_allow_html=True)

dm_col1,dm_col2=st.columns([9,1])
with dm_col2:
    if st.button("🌙" if not dm else "☀️",key="dm_toggle"):
        st.session_state.dark_mode=not st.session_state.dark_mode; st.rerun()

# HERO
st.markdown('<div id="hero" class="hero-section">',unsafe_allow_html=True)
st.markdown(f"""<div class="wotd-card"><span style="font-family:'Syne',sans-serif;font-size:0.68rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;opacity:0.8">📅 Word of the Day</span><br><span style="font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:800">{wotd[0]}</span> <span style="font-size:0.8rem;opacity:0.8">({wotd[1]})</span><br><span style="font-size:0.95rem;opacity:0.9">{wotd[2]}</span><br><span style="font-size:0.85rem;opacity:0.75;font-style:italic">"{wotd[3]}"</span></div>""",unsafe_allow_html=True)
st.markdown("<br>",unsafe_allow_html=True)
st.markdown('<div class="hero-badge">🔊 Echo English</div>',unsafe_allow_html=True)
st.markdown("""<div style="font-family:'Syne',sans-serif;font-size:4rem;font-weight:800;color:#f5f0e8;line-height:1.0;margin-bottom:18px">Speak English.<br>Get the Job.<br>Live Your Life.</div><div style="font-size:1.1rem;color:#a0a090;max-width:520px;line-height:1.7;margin-bottom:32px">A free, AI-powered English learning platform built for non-native speakers. No ads. No rigid schedules. Real conversations at your own pace — 24/7.</div>""",unsafe_allow_html=True)
streak=st.session_state.streak
xp=st.session_state.xp
xp_lvl,xp_title,xp_next=xp_level(xp)
if streak>0:
    st.markdown(f'<div class="streak-badge">🔥 {streak} Day Streak!</div><span class="xp-badge">⚡ {xp} XP — {xp_title}</span>',unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
hc1,hc2,_=st.columns([1,1,3])
with hc1:
    if st.button("🎯 Take Placement Quiz",key="hero_cta"): pass
with hc2:
    if st.button("📘 Start at Level 1",key="hero_l1"): pass
st.markdown('<hr style="border-color:#2a2a2a;margin:40px 0 28px">',unsafe_allow_html=True)
s1,s2,s3,s4=st.columns(4)
for col,num,label in [(s1,"5","Learning Levels"),(s2,"AI","Conversation Partner"),(s3,"0","Ads Ever"),(s4,"24/7","Available")]:
    col.markdown(f'<div style="text-align:center;padding:16px;border-left:1px solid #2a2a2a"><div style="font-family:\'Syne\',sans-serif;font-size:2.2rem;font-weight:800;color:#e85d2f">{num}</div><div style="font-size:0.82rem;color:#888;margin-top:2px">{label}</div></div>',unsafe_allow_html=True)
st.markdown('</div>',unsafe_allow_html=True)

# PLACEMENT
st.markdown('<div id="placement" class="section-wrap">',unsafe_allow_html=True)
st.markdown('<div class="hero-badge">Find Your Level</div>',unsafe_allow_html=True)
st.title("Placement Quiz")
st.markdown("##### Answer 5 quick questions and we'll tell you exactly which level to start at.")
st.markdown('<hr class="divider">',unsafe_allow_html=True)
pqs=[
    {"q":"1. Which sentence is correct?","options":["I no understand.","I don't understand.","I not understand.","I am not understanding."],"correct":"I don't understand.","level":1},
    {"q":"2. Choose the best response to: 'How do I get to the train station?'","options":["Yes, I am.","Turn left at the corner, then walk two blocks.","I am going.","No problem."],"correct":"Turn left at the corner, then walk two blocks.","level":2},
    {"q":"3. Fill in the blank: 'The job is great. ___, the commute is very long.'","options":["So","Because","However","Also"],"correct":"However","level":3},
    {"q":"4. Which is the most professional way to disagree with your manager?","options":["You're wrong.","I don't think so.","I see your point, though I'd like to suggest an alternative approach.","That's a bad idea."],"correct":"I see your point, though I'd like to suggest an alternative approach.","level":4},
    {"q":"5. What does 'hit the ground running' mean?","options":["To fall while jogging.","To start something and immediately work hard at it.","To be very tired.","To arrive somewhere quickly."],"correct":"To start something and immediately work hard at it.","level":5},
]
cq,ci=st.columns([3,1])
with ci:
    st.markdown(f'<div class="step-card" style="padding:18px 22px"><div class="step-label">How it works</div><div style="font-size:0.87rem;color:{muted};line-height:1.8">5 questions across all 5 levels. We will tell you exactly where to start.</div></div>',unsafe_allow_html=True)
with cq:
    if not st.session_state.placement_done:
        answers={}
        for pq in pqs:
            ans=st.radio(pq["q"],["— select —"]+pq["options"],key=f"pq_{pq['level']}")
            answers[pq["level"]]=(ans,pq["correct"])
        if st.button("Get My Level →",key="placement_submit"):
            if any(a=="— select —" for a,_ in answers.values()):
                st.warning("Please answer all 5 questions first.")
            else:
                score=sum(1 for a,c in answers.values() if a==c)
                if score<=1: result=(1,"Beginner","📘","#3b82f6","You are just getting started — Level 1 will build your foundation.")
                elif score==2: result=(2,"Elementary","📗","#22c55e","You know some basics! Level 2 will help you build real sentences.")
                elif score==3: result=(3,"Intermediate","📙","#f59e0b","Nice work! Level 3 focuses on real conversations.")
                elif score==4: result=(4,"Upper Intermediate","📕","#ef4444","Impressive! Level 4 will polish your professional English.")
                else: result=(5,"Advanced","📓","#8b5cf6","Excellent! Level 5 covers idioms, nuance, and professional mastery.")
                st.session_state.placement_result=result
                st.session_state.placement_answers=answers
                st.session_state.placement_done=True
                award_xp(10)
                st.rerun()
    else:
        ln,lname,icon,color,message=st.session_state.placement_result
        score=sum(1 for a,c in st.session_state.placement_answers.values() if a==c)
        st.markdown(f'<div style="background:{color}18;border:3px solid {color};padding:24px 28px;box-shadow:6px 6px 0px {border};margin-bottom:16px"><div style="font-family:\'Syne\',sans-serif;font-size:0.68rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:{color};margin-bottom:6px">Your Result</div><div style="font-family:\'Syne\',sans-serif;font-size:2rem;font-weight:800;color:{fg}">{icon} Level {ln} — {lname}</div><div style="font-size:0.88rem;color:{muted};margin-top:6px">Score: {score} / 5 correct</div><div style="margin-top:10px;font-size:0.97rem;color:{fg}">{message}</div></div>',unsafe_allow_html=True)
        for pq in pqs:
            chosen,correct=st.session_state.placement_answers[pq["level"]]
            if chosen==correct: st.success(f"✅ Q{pq['level']}: Correct!")
            else: st.error(f"❌ Q{pq['level']}: You chose '{chosen}'. Answer: **{correct}**")
        if st.button("Retake Quiz",key="retake"):
            st.session_state.placement_done=False; st.session_state.placement_result=None; st.session_state.placement_answers={}; st.rerun()
st.markdown('</div>',unsafe_allow_html=True)

# PROGRESS
st.markdown('<div id="progress" class="section-wrap">',unsafe_allow_html=True)
st.markdown('<div class="hero-badge">Your Progress</div>',unsafe_allow_html=True)
st.title("Progress Tracker")
st.markdown('<hr class="divider">',unsafe_allow_html=True)
completed=sum(1 for v in st.session_state.progress.values() if v)
pct=int((completed/5)*100)
avg_scores=[s for s in st.session_state.scores.values() if s is not None]
c1,c2,c3,c4=st.columns(4)
c1.metric("Levels Completed",f"{completed} / 5")
c2.metric("Overall Progress",f"{pct}%")
c3.metric("Avg Quiz Score",f"{round(sum(avg_scores)/len(avg_scores),1) if avg_scores else '—'}")
c4.metric("Day Streak",f"{'🔥 ' if streak>0 else ''}{streak}")
st.markdown(f'<div class="progress-bar-wrap"><div class="progress-bar-fill" style="width:{pct}%"></div></div><div style="font-size:0.78rem;color:{muted};margin-bottom:20px">{pct}% complete</div>',unsafe_allow_html=True)
for num,icon,label in [(1,"📘","Beginner"),(2,"📗","Elementary"),(3,"📙","Intermediate"),(4,"📕","Upper Intermediate"),(5,"📓","Advanced")]:
    done=st.session_state.progress[num]; score=st.session_state.scores[num]
    color="#22c55e" if done else ("#3a3a3a" if dm else "#d0c8b8")
    status=f"✅ Completed — Score: {score}/6" if done else "⬜ Not yet completed"
    st.markdown(f'<div class="progress-level-card"><span style="font-size:1.8rem">{icon}</span><div style="flex:1"><div style="font-family:\'Syne\',sans-serif;font-weight:800;color:{fg}">Level {num} — {label}</div><div style="color:{muted};font-size:0.83rem;margin-top:3px">{status}</div></div><div style="width:100px"><div style="background:{"#3a3a3a" if dm else "#d0c8b8"};height:7px"><div style="background:{color};height:7px;width:{"100%" if done else "0%"}"></div></div></div></div>',unsafe_allow_html=True)
if completed>0:
    if st.button("Reset All Progress",key="reset_progress"):
        st.session_state.progress={1:False,2:False,3:False,4:False,5:False}
        st.session_state.scores={1:None,2:None,3:None,4:None,5:None}
        st.session_state.xp=0; st.session_state.badges=[]; st.rerun()
st.markdown('</div>',unsafe_allow_html=True)

# XP & BADGES
st.markdown('<div id="xp" class="section-wrap">',unsafe_allow_html=True)
st.markdown('<div class="hero-badge">⚡ XP & Badges</div>',unsafe_allow_html=True)
st.title("XP & Badges")
st.markdown("##### Earn XP for every quiz. Unlock badges as you reach milestones.")
st.markdown('<hr class="divider">',unsafe_allow_html=True)
xp_lvl,xp_title,xp_next=xp_level(st.session_state.xp)
xp_pct=min(100,int((st.session_state.xp/xp_next)*100)) if xp_next<999999 else 100
x1,x2,x3=st.columns(3)
x1.metric("Total XP",f"⚡ {st.session_state.xp}")
x2.metric("XP Level",f"{xp_lvl} — {xp_title}")
x3.metric("Badges Earned",f"🏅 {len(st.session_state.badges)}")
st.markdown(f'<div style="font-size:0.82rem;color:{muted};margin-bottom:4px">Progress to next XP level ({xp_next} XP)</div><div class="progress-bar-wrap"><div class="progress-bar-fill" style="width:{xp_pct}%;background:#8b5cf6"></div></div><div style="font-size:0.78rem;color:{muted};margin-bottom:24px">{st.session_state.xp} / {xp_next} XP</div>',unsafe_allow_html=True)
st.markdown("### How to Earn XP")
xp_ways=[("🎯","Complete Placement Quiz","10 XP"),("📝","Submit a Level Quiz","20 XP"),("💯","Perfect Score Bonus","10 XP"),("⚡","Complete Quick Review","15 XP"),("🔥","Daily Practice","5 XP/day")]
cols=st.columns(len(xp_ways))
for col,(icon,action,reward) in zip(cols,xp_ways):
    col.markdown(f'<div class="badge-card"><div style="font-size:1.8rem">{icon}</div><div style="font-family:\'Syne\',sans-serif;font-weight:700;font-size:0.85rem;margin:6px 0;color:{fg}">{action}</div><div style="color:#8b5cf6;font-weight:700;font-size:0.9rem">{reward}</div></div>',unsafe_allow_html=True)
st.markdown("<br>### All Badges")
all_badges_def=[("🌱","First Steps","Complete your first quiz"),("📚","Scholar","Complete 3 levels"),("🏆","Graduate","Complete all 5 levels"),("🔥","On Fire","Reach a 3-day streak"),("⚡","Lightning Learner","Earn 100 XP"),("💎","Diamond Student","Earn 300 XP"),("🎯","Sharp Shooter","Score 6/6 on any quiz"),("🌟","All Star","Complete all levels with 6/6")]
earned_names=[b[1] for b in st.session_state.badges]
badge_cols=st.columns(4)
for i,(icon,name,desc) in enumerate(all_badges_def):
    earned=name in earned_names
    col=badge_cols[i%4]
    op="1" if earned else "0.3"
    bc="#e85d2f" if earned else border
    col.markdown(f'<div class="badge-card" style="opacity:{op};border:2px solid {bc}"><div style="font-size:2.2rem">{icon}</div><div style="font-family:\'Syne\',sans-serif;font-weight:800;font-size:0.9rem;margin:6px 0;color:{fg}">{name}</div><div style="color:{muted};font-size:0.78rem">{desc}</div>{"<div style=\'color:#22c55e;font-size:0.75rem;margin-top:4px;font-weight:700\'>✅ EARNED</div>" if earned else ""}</div>',unsafe_allow_html=True)
st.markdown('</div>',unsafe_allow_html=True)

# STORIES
st.markdown('<div id="stories" class="section-wrap">',unsafe_allow_html=True)
st.markdown('<div class="hero-badge">Real Results</div>',unsafe_allow_html=True)
st.title("Before & After Echo English")
st.markdown('<hr class="divider">',unsafe_allow_html=True)
stories=[
    {"name":"Maria, 28 — from Mexico City","context":"Moved to the US for work. Struggled to communicate with coworkers.","before":["😰 Avoided talking to coworkers","❌ 'I no understand the meeting today'","😶 Stayed quiet in team discussions","📉 Was passed over for promotion"],"after":["😊 Confidently joins conversations","✅ 'I didn't quite follow — could you clarify?'","🗣️ Regularly shares ideas in meetings","📈 Got promoted to team lead"],"time":"After 3 Months"},
    {"name":"Ahmed, 34 — from Egypt","context":"Arrived in the UK with engineering qualifications but couldn't land a job.","before":["😰 Froze up in job interviews","❌ 'I am very hardly worker and I do my best always'","😟 Rejected from 12 interviews","💸 Working below his skill level"],"after":["😎 Calm and prepared in interviews","✅ 'I am a highly motivated engineer with 8 years of experience'","🎉 Landed a job at a London tech firm","🏆 Now mentors other immigrants"],"time":"After 4 Months"},
    {"name":"Lin, 22 — from China","context":"Started university in Canada but couldn't follow lectures or make friends.","before":["😰 Sat in the back and said nothing","❌ 'Yesterday I go to the library and study very much'","😔 Ate lunch alone every day","📚 Was failing two classes"],"after":["✋ Raises her hand and asks questions","✅ 'Yesterday I went to the library and studied for a few hours'","👫 Has a group of close friends","🎓 Made the Dean's List"],"time":"After 2 Months"},
]
for story in stories:
    st.markdown(f"### {story['name']}")
    st.markdown(f"*{story['context']}*")
    ib="".join([f'<div style="padding:5px 0;border-bottom:1px solid {"#3a3a3a" if dm else "#f0ebe0"};font-size:0.88rem">{i}</div>' for i in story["before"]])
    ia="".join([f'<div style="padding:5px 0;border-bottom:1px solid #2a2a2a;font-size:0.88rem">{i}</div>' for i in story["after"]])
    st.markdown(f'<div class="before-after"><div class="before-col"><div class="ba-label" style="color:#c0392b">❌ Before Echo English</div>{ib}</div><div class="after-col"><div class="ba-label" style="color:#4ade80">✅ {story["time"]}</div>{ia}</div></div>',unsafe_allow_html=True)
st.markdown('</div>',unsafe_allow_html=True)

def render_practice(level_num,questions,correct_answers):
    max_score=len(questions)
    st.markdown("Answer all questions, then press **Submit** to see your score.")
    responses=[]
    for i,(q_label,opts) in enumerate(questions):
        val=st.radio(q_label,["— select —"]+opts,key=f"l{level_num}q{i+1}")
        responses.append(val)
    if st.button("Submit",key=f"l{level_num}_submit"):
        update_streak()
        score=sum(1 for r,c in zip(responses,correct_answers) if r==c)
        st.session_state.scores[level_num]=score
        st.session_state.progress[level_num]=True
        award_xp(20)
        if score==max_score: award_xp(10)
        new_badges=check_badges()
        st.markdown(f"### Your Score: {score} / {max_score}")
        for i,(r,c) in enumerate(zip(responses,correct_answers)):
            lbl=f"Q{i+1}"
            if r=="— select —": st.warning(f"⚠️ {lbl}: Not answered. Answer: **{c}**")
            elif r==c: st.success(f"✅ {lbl}: Correct!")
            else: st.error(f"❌ {lbl}: You chose '{r}'. Answer: **{c}**")
        if score==max_score: st.balloons(); st.success("🎉 Perfect score! +30 XP earned!")
        else: st.info(f"+20 XP earned!")
        for icon,name,desc in new_badges:
            st.success(f"🏅 New badge: {icon} **{name}** — {desc}")

LEVEL_DATA={
    1:{
        "vocab":[("Greetings",["Hello","Goodbye","Please","Thank you","Sorry","Yes","No","Excuse me"]),("Numbers",["One","Two","Three","Four","Five","Ten","Twenty","Hundred"]),("Colors",["Red","Blue","Green","White","Black","Yellow","Orange","Purple"]),("Family",["Mother","Father","Brother","Sister","Friend","Baby","Husband","Wife"]),("Places",["Home","School","Hospital","Store","Restaurant","Bank","Street","City"])],
        "phrases":[("Meeting people",[("Hello, my name is ___.", "Hola, me llamo ___."),("Nice to meet you.","Mucho gusto."),("How are you?","Como estas?"),("I'm fine, thank you.","Estoy bien, gracias."),("Where are you from?","De donde eres?")]),("Asking for help",[("Can you help me?","Me puede ayudar?"),("I don't understand.","No entiendo."),("Please speak slowly.","Por favor hable despacio."),("Where is the bathroom?","Donde esta el bano?"),("Can you repeat that?","Puede repetir eso?")]),("Shopping",[("How much does this cost?","Cuanto cuesta esto?"),("I would like this, please.","Quisiera esto, por favor."),("Do you accept cash?","Acepta efectivo?"),("Do you have this in a different size?","Tiene esto en otra talla?")])],
        "flashcards":[("Hello","A greeting used when you meet someone"),("Thank you","Words you say when someone helps you"),("Sorry","What you say when you make a mistake"),("Please","A polite word used when asking for something"),("Goodbye","What you say when you leave"),("Yes","Agreement — the opposite of No"),("No","Disagreement — the opposite of Yes"),("Excuse me","Used to get someones attention politely")],
        "questions":[("1. 'Hello, ___ name is Maria.' — which word fits?",["my","your","his","she"],"my"),("2. You want to say thank you. You say:",["Sorry","Goodbye","Thank you","No"],"Thank you"),("3. You don't understand something. You say:",["I am fine.","I don't understand.","Nice to meet you.","How much?"],"I don't understand."),("4. Someone says 'Nice to meet you.' You reply:",["Goodbye.","Nice to meet you too.","I am sorry.","Yes please."],"Nice to meet you too."),("5. You want someone to speak more slowly. You say:",["Please be quiet.","Please speak slowly.","I am speaking.","Thank you."],"Please speak slowly."),("6. You want to know the price. You ask:",["Where is it?","What color is it?","How much does this cost?","Can you help me?"],"How much does this cost?")],
    },
    2:{
        "vocab":[("At Work",["Job","Office","Manager","Meeting","Email","Schedule","Deadline","Team","Colleague","Report"]),("At the Store",["Price","Receipt","Change","Discount","Size","Aisle","Checkout","Return","Sale"]),("Directions",["Left","Right","Straight","Corner","Block","Near","Far","Across","Next to","Between"]),("Time",["Morning","Afternoon","Evening","Tonight","Yesterday","Tomorrow","Weekly","Monthly","Appointment","On time"])],
        "phrases":[("Asking directions",[("How do I get to ___?","Como llego a ___?"),("Is it far from here?","Esta lejos de aqui?"),("Turn left at the corner.","Gire a la izquierda en la esquina."),("It's next to the bank.","Esta al lado del banco.")]),("At work",[("When is the deadline?","Cuando es la fecha limite?"),("Can I ask a question?","Puedo hacer una pregunta?"),("I will send you an email.","Le enviare un correo electronico."),("I have a meeting at 3pm.","Tengo una reunion a las 3pm.")]),("Daily life",[("What time does it open?","A que hora abre?"),("I need to make an appointment.","Necesito hacer una cita."),("Can I pay by card?","Puedo pagar con tarjeta?"),("What time does the bus arrive?","A que hora llega el autobus?")])],
        "flashcards":[("Deadline","The latest time something must be finished"),("Receipt","A piece of paper showing what you bought and paid"),("Schedule","A plan showing when things will happen"),("Appointment","A planned meeting at a specific time"),("Colleague","A person you work with"),("Discount","A reduction in the price of something"),("Checkout","The place in a store where you pay"),("Aisle","A passage between rows of shelves in a store")],
        "questions":[("1. You want to know how to get somewhere. You ask:",["What time is it?","How do I get to the station?","Can I have the bill?","Where are you from?"],"How do I get to the station?"),("2. Your boss asks for the report. You say:",["I will send you an email.","I am hungry.","Turn left.","Good morning."],"I will send you an email."),("3. You want to pay. You ask:",["Is it far?","Can I pay by card?","What is your name?","I don't understand."],"Can I pay by card?"),("4. The supermarket is near. You say:",["Yes, it is next to the bank.","I am fine, thank you.","My name is Pedro.","Turn left."],"Yes, it is next to the bank."),("5. You need to cancel an appointment. You say:",["I need to cancel my appointment.","I am very hungry.","Where is the hospital?","Thank you goodbye."],"I need to cancel my appointment."),("6. Your colleague asks when the meeting is. You say:",["I have a meeting at 3pm.","The price is ten dollars.","Turn right at the corner.","I don't understand."],"I have a meeting at 3pm.")],
    },
    3:{
        "vocab":[("Opinions & Feelings",["Agree","Disagree","Prefer","Frustrated","Confident","Nervous","Excited","Disappointed","Overwhelmed","Motivated"]),("Work & Career",["Promotion","Salary","Interview","Colleague","Responsible","Experience","Qualification","Department","Deadline","Performance"]),("Connectors",["However","Therefore","Although","Meanwhile","Furthermore","As a result","On the other hand","In addition","Nevertheless","Consequently"])],
        "phrases":[("At Work",[("I think it's a good idea, however I'm concerned about the deadline.","Creo que es buena idea, sin embargo me preocupa el plazo."),("Could we discuss this further?","Podriamos discutir esto mas?"),("I'd like to suggest an alternative.","Me gustaria sugerir una alternativa."),("I'm not sure I agree with that approach.","No estoy seguro de estar de acuerdo con ese enfoque.")]),("Meeting someone",[("I moved here two years ago to find better work opportunities.","Me mude aqui hace dos anos para encontrar mejores oportunidades de trabajo."),("Although it was hard at first, I'm really enjoying it now.","Aunque fue dificil al principio, ahora lo estoy disfrutando mucho."),("What do you do for work?","A que te dedicas?"),("I've been living here for about a year.","Llevo viviendo aqui aproximadamente un ano.")])],
        "flashcards":[("However","Used to show contrast between two ideas"),("Therefore","Used to show a result or conclusion"),("Although","Used to introduce a contrasting idea"),("Furthermore","Used to add another point"),("Nevertheless","Despite that; used to continue after something negative"),("Promotion","A move to a higher position at work"),("Frustrated","Feeling upset because you cannot do something"),("Motivated","Feeling eager and ready to work hard")],
        "questions":[("1. 'The job pays well. ___, the hours are long.'",["Therefore","However","Although","Meanwhile"],"However"),("2. 'She studied hard. ___, she passed the exam.'",["However","Although","Therefore","Meanwhile"],"Therefore"),("3. '___ it was raining, they went for a walk.'",["Therefore","Furthermore","Although","As a result"],"Although"),("4. 'I enjoy my work. ___, I find the commute exhausting.'",["Therefore","Furthermore","On the other hand","Consequently"],"On the other hand"),("5. 'He missed the interview. ___, he didn't get the job.'",["However","Although","Nevertheless","As a result"],"As a result"),("6. Which word means you feel sure about yourself?",["Frustrated","Nervous","Confident","Disappointed"],"Confident")],
    },
    4:{
        "vocab":[("Professional English",["Demonstrate","Initiative","Collaborate","Negotiate","Implement","Facilitate","Prioritize","Delegate","Streamline","Leverage"]),("Soft Skills",["Adaptable","Proactive","Analytical","Detail-oriented","Goal-driven","Self-motivated","Team player","Problem-solver"]),("Tone Shifters",["I'd suggest...","It might be worth...","Have you considered...","One option could be...","I'd like to raise a concern...","With respect, ..."])],
        "phrases":[("Professional responses",[("I'd like to discuss my compensation given my recent contributions.","Me gustaria hablar sobre mi compensacion dados mis logros recientes."),("I understand your frustration and I'd like to help resolve this.","Entiendo su frustracion y me gustaria ayudar a resolverlo."),("I proactively identified a gap and implemented a solution.","Identifique proactivamente un problema e implemente una solucion."),("Could we schedule a time to revisit this?","Podriamos programar un momento para revisar esto?")]),("Interview phrases",[("I'm a highly motivated professional with X years of experience.","Soy un profesional altamente motivado con X anos de experiencia."),("One of my key strengths is my ability to adapt quickly.","Una de mis principales fortalezas es mi capacidad de adaptarme rapidamente."),("I'd like to learn more about the team's goals.","Me gustaria conocer mas sobre los objetivos del equipo."),("I thrive in collaborative environments.","Me desempeno bien en entornos colaborativos.")])],
        "flashcards":[("Proactive","Taking action before problems arise, not waiting to react"),("Delegate","To give a task to someone else to complete"),("Streamline","To make a process faster and more efficient"),("Leverage","To use something to maximum advantage"),("Facilitate","To make a process easier or smoother"),("Negotiate","To discuss terms to reach a mutual agreement"),("Demonstrate","To show or prove something clearly"),("Initiative","The ability to act independently without being told")],
        "questions":[("1. Your manager asks why you missed a deadline. You say:",["It's not my fault.","I apologize — I underestimated the time needed and I've already adjusted my approach.","I was busy.","Nobody told me."],"I apologize — I underestimated the time needed and I've already adjusted my approach."),("2. You disagree with a colleague in a meeting. You say:",["That's wrong.","I hear you, and I'd suggest we also consider the budget impact before deciding.","Whatever.","No."],"I hear you, and I'd suggest we also consider the budget impact before deciding."),("3. You want to ask for a raise. The best opening is:",["Give me more money.","I've been here 2 years, pay me more.","I'd like to discuss my compensation given my recent contributions.","I need a raise."],"I'd like to discuss my compensation given my recent contributions."),("4. A client is upset. You say:",["Not my problem.","Calm down.","I understand your frustration and I'd like to help resolve this as quickly as possible.","That's not what I said."],"I understand your frustration and I'd like to help resolve this as quickly as possible."),("5. Which shows initiative in an interview?",["I just do what I'm told.","I proactively identified a gap and implemented a solution that saved the team 3 hours a week.","I come to work on time.","I try my best."],"I proactively identified a gap and implemented a solution that saved the team 3 hours a week."),("6. Which word means to make a process more efficient?",["Delegate","Facilitate","Streamline","Negotiate"],"Streamline")],
    },
    5:{
        "vocab":[("Idioms",["Hit the ground running","Beat around the bush","On the fence","Bite the bullet","Ball is in your court","Under the weather","Burn bridges","Cut corners"]),("Advanced Register",["Presumably","Essentially","Relatively","Particularly","Consistently","Overwhelmingly","Inherently","Substantively"])],
        "phrases":[("Formal vs Casual",[("Could you send me that file when you get a chance?","Podrias enviarme ese archivo cuando tengas oportunidad?"),("I would greatly appreciate it if you could send the file at your earliest convenience.","Le agradeceria mucho que me enviara el archivo a la mayor brevedad posible."),("I'm not sure that's the best approach — what about...?","No estoy seguro de que sea el mejor enfoque."),("While I appreciate the suggestion, I have some concerns I'd like to raise.","Aunque valoro la sugerencia, me gustaria plantear algunas dudas.")]),("Idioms in context",[("She hit the ground running on her first day.","Ella empezo a trabajar intensamente desde el primer dia."),("Stop beating around the bush — just tell me what happened.","Deja de rodeos — dime que paso."),("The ball is in your court now.","Ahora te toca a ti."),("I didn't want to apologize but I bit the bullet and did it.","No queria disculparme pero lo hice de todas formas.")])],
        "flashcards":[("Hit the ground running","To start working hard immediately from the beginning"),("Beat around the bush","To avoid talking about the main topic"),("On the fence","Undecided — not sure which choice to make"),("Bite the bullet","To do something difficult or unpleasant that you have been avoiding"),("The ball is in your court","It is now your turn to take action or make a decision"),("Under the weather","Feeling sick or unwell"),("Burn bridges","To permanently damage a relationship or opportunity"),("Cut corners","To do something the quick or cheap way, sacrificing quality")],
        "questions":[("1. 'I'm on the fence about the new job.' What does this mean?",["He already accepted it.","He is undecided.","He doesn't like it.","He is sitting on something."],"He is undecided."),("2. 'The ball is in your court.' What should you do?",["Wait for your boss.","Take the next step yourself.","Go play basketball.","Ask someone else."],"Take the next step yourself."),("3. Which is the most formal way to say you're sick?",["I feel terrible.","I'm under the weather.","I am unwell and unable to attend.","I'm not feeling it today."],"I am unwell and unable to attend."),("4. Your colleague quit very angrily and insulted everyone. You say:",["Good for them.","They really burned their bridges there.","They hit the ground running.","They were on the fence."],"They really burned their bridges there."),("5. The team rushed the project and quality suffered. You say:",["They beat around the bush.","They cut corners.","They bit the bullet.","They burned bridges."],"They cut corners."),("6. 'Stop beating around the bush' means:",["Stop running.","Stop being nervous.","Get to the point.","Stop being lazy."],"Get to the point.")],
    },
}

ALL_VOCAB=[]
for lvl_num,data in LEVEL_DATA.items():
    for cat,words in data["vocab"]:
        for w in words: ALL_VOCAB.append((w,cat,lvl_num))
    for cw,cd in data["flashcards"]: ALL_VOCAB.append((cw,cd,lvl_num))

level_meta=[(1,"📘","Beginner","Start from zero. Learn the words and phrases you need every single day."),(2,"📗","Elementary","Build simple sentences and handle everyday situations with confidence."),(3,"📙","Intermediate","Hold real conversations, express opinions, and talk about your life and work."),(4,"📕","Upper Intermediate","Sound more natural, nail job interviews, and handle complex conversations."),(5,"📓","Advanced","Master idioms, nuance, tone, and fluency. Speak like you have always lived here.")]

for lvl_num,icon,lvl_name,lvl_sub in level_meta:
    data=LEVEL_DATA[lvl_num]
    st.markdown(f'<div id="level-{lvl_num}" class="section-wrap">',unsafe_allow_html=True)
    st.markdown(f'<div class="hero-badge">{icon} Level {lvl_num} — {lvl_name}</div>',unsafe_allow_html=True)
    st.title(f"Level {lvl_num} – {lvl_name}")
    st.markdown(f"##### {lvl_sub}")
    st.markdown('<hr class="divider">',unsafe_allow_html=True)
    tl=["📖 Vocabulary","💬 Phrases","🎯 Practice"]
    if lvl_num==4: tl[1]="💼 Job Interview"
    elif lvl_num==5: tl[0]="📖 Idioms"; tl[1]="🎭 Tone & Register"
    tabs=st.tabs(tl)
    with tabs[0]:
        st.markdown("### Vocabulary")
        for cat,words in data["vocab"]:
            st.markdown(f"**{cat}**")
            st.markdown("".join([f'<span class="vocab-word">{w}</span>' for w in words])+"<br><br>",unsafe_allow_html=True)
    with tabs[1]:
        if lvl_num==4:
            st.markdown("### Job Interview Prep")
            for q,tip in [("Tell me about yourself.","Start with your background, mention key experience, end with why you are here. Under 2 minutes."),("What are your strengths?","Pick 2-3 real strengths with examples."),("Why do you want this job?","Show you researched the company and connect your skills to their needs."),("Describe a challenge you overcame.","Use the STAR method: Situation, Task, Action, Result."),("Where do you see yourself in 5 years?","Show ambition but commitment."),("Do you have any questions for us?","Always say yes! Ask about the team or growth opportunities.")]:
                with st.expander(f"❓ {q}"):
                    st.markdown(f'<div class="phrase-box"><strong>Tip:</strong> {tip}</div>',unsafe_allow_html=True)
        elif lvl_num==5:
            st.markdown("### Tone & Register")
            for situation,casual,neutral,formal in [("Asking for something","Oi, send me that file.","Could you send me that file when you get a chance?","I would greatly appreciate it if you could send the file at your earliest convenience."),("Saying you are busy","I can't, I'm swamped.","I'm pretty tied up right now — can we reschedule?","Unfortunately, I have prior commitments that prevent me from attending."),("Disagreeing","That's a bad idea.","I'm not sure that's the best approach — what about...?","While I appreciate the suggestion, I have some concerns I'd like to raise.")]:
                st.markdown(f"**{situation}**")
                c1,c2,c3=st.columns(3)
                c1.markdown(f'<div class="phrase-box" style="border-left-color:#f59e0b"><strong>Casual</strong><br><em>"{casual}"</em></div>',unsafe_allow_html=True)
                c2.markdown(f'<div class="phrase-box" style="border-left-color:#22c55e"><strong>Neutral</strong><br><em>"{neutral}"</em></div>',unsafe_allow_html=True)
                c3.markdown(f'<div class="phrase-box" style="border-left-color:#3b82f6"><strong>Formal</strong><br><em>"{formal}"</em></div>',unsafe_allow_html=True)
                st.markdown("<br>",unsafe_allow_html=True)
        else:
            st.markdown("### Key Phrases")
            for section,items in data["phrases"]:
                st.markdown(f"**{section}**")
                for en,es in items:
                    st.markdown(f'<div class="phrase-box">🇺🇸 <strong>{en}</strong><br><span style="color:{muted};font-size:0.83rem">🇪🇸 {es}</span></div>',unsafe_allow_html=True)
                st.markdown("<br>",unsafe_allow_html=True)
    with tabs[2]:
        st.markdown(f"### Level {lvl_num} Quiz")
        qs=[(q,opts) for q,opts,_ in data["questions"]]
        ans=[a for _,_,a in data["questions"]]
        render_practice(lvl_num,qs,ans)
    st.markdown('</div>',unsafe_allow_html=True)

# JOB PACKS
st.markdown('<div id="job-packs" class="section-wrap">',unsafe_allow_html=True)
st.markdown('<div class="hero-badge">💼 Job Vocabulary Packs</div>',unsafe_allow_html=True)
st.title("Job-Specific Vocabulary")
st.markdown("##### Real English words and phrases used in specific jobs. Pick your industry.")
st.markdown('<hr class="divider">',unsafe_allow_html=True)
job_packs={
    "🏥 Healthcare":{"color":"#ef4444","intro":"Working in healthcare requires specific vocabulary for talking to patients, colleagues, and doctors.","vocab":["Patient","Appointment","Prescription","Diagnosis","Symptom","Medication","Emergency","Nurse","Doctor","Ward","Discharge","Vital signs","Blood pressure","Allergy","Insurance"],"phrases":[("Talking to a patient","How are you feeling today? Can you describe the pain on a scale of 1 to 10?"),("Explaining a procedure","I am going to take your blood pressure. Please roll up your sleeve."),("Asking about medication","Are you currently taking any medication? Do you have any allergies?"),("In an emergency","Call 911 immediately. The patient is not responding."),("End of shift handover","The patient in bed 3 has been given their medication and is stable.")],"mistakes":[("He is very sick (too vague)","The patient presents with a high fever and chest pain"),("I don't know","Let me check with the doctor and get back to you")]},
    "🍽️ Restaurant":{"color":"#f59e0b","intro":"Restaurant workers need to take orders, handle complaints, and make guests feel welcome.","vocab":["Reservation","Menu","Appetizer","Entree","Dessert","Bill","Tip","Table","Host","Server","Kitchen","Order","Allergies","Special","Refill"],"phrases":[("Greeting guests","Welcome! Do you have a reservation? How many are in your party?"),("Taking an order","Are you ready to order? What can I get for you?"),("Handling a complaint","I sincerely apologize for that. Let me fix this for you right away."),("Describing a dish","That dish contains nuts — would you like me to suggest an alternative?"),("Presenting the bill","Here is your bill. Was everything to your satisfaction today?")],"mistakes":[("What you want?","What can I get for you today?"),("We don't have it","Unfortunately that item is unavailable today. May I suggest...")]},
    "🏗️ Construction":{"color":"#78716c","intro":"Construction workers need to understand safety instructions, tools, and workplace communication.","vocab":["Blueprint","Foundation","Scaffold","Drill","Concrete","Safety helmet","High-vis","Crane","Foreman","Deadline","Inspection","Permit","Contractor","Materials","Site"],"phrases":[("Safety briefing","Always wear your safety helmet and high-vis vest on site."),("Asking about the plan","Can you show me the blueprint for this section?"),("Reporting a problem","There is a crack in the foundation — we need to stop work and inspect it."),("Requesting materials","We have run out of concrete. Can you order another delivery for tomorrow?"),("End of day","The inspection passed. We are on schedule for the deadline.")],"mistakes":[("I not understand drawing","Could you explain the blueprint for this section?"),("Too danger here","This area is unsafe — we need to stop work immediately")]},
    "🛒 Retail":{"color":"#3b82f6","intro":"Retail workers interact with customers all day. Clear, polite English makes a huge difference.","vocab":["Customer","Receipt","Refund","Exchange","Loyalty card","Discount","Sale","Stock","Register","Queue","Manager","Complaint","Policy","Warranty","Fitting room"],"phrases":[("Greeting a customer","Hello! Welcome. Is there anything I can help you with today?"),("Processing a return","Do you have your receipt? I can process a refund or exchange for you."),("Handling a complaint","I completely understand your frustration. Let me speak to a manager for you."),("Explaining a policy","Our return policy allows exchanges within 30 days with a receipt."),("Closing a sale","Great choice! Would you like to join our loyalty program to earn points?")],"mistakes":[("No refund","Unfortunately this item is outside our return period, but let me see what I can do"),("Not my problem","Let me find someone who can help you with that")]},
    "🚛 Delivery":{"color":"#22c55e","intro":"Delivery drivers and warehouse workers need English for navigation, deliveries, and workplace safety.","vocab":["Parcel","Signature","Route","Warehouse","Loading dock","Manifest","Tracking","Delivery window","Fragile","Dispatch","Inventory","Scan","Recipient","Delay","Proof of delivery"],"phrases":[("At the door","Hello, I have a delivery for this address. Could I get a signature please?"),("When nobody is home","I attempted delivery but no one was home. I have left a card with instructions."),("Reporting a delay","There is heavy traffic on the route. The delivery will be approximately 30 minutes late."),("In the warehouse","This pallet is marked fragile — handle with care and do not stack anything on top."),("Confirming a delivery","I need you to sign here to confirm you have received the package.")],"mistakes":[("You sign here","Could I get your signature here please?"),("Package broken, not my fault","I noticed the package was damaged on arrival. I will report this to dispatch")]},
}
pack_names=list(job_packs.keys())
selected_pack=st.selectbox("Choose your industry:",pack_names,key="job_pack_select")
pack=job_packs[selected_pack]
st.markdown(f'<div class="job-pack-card" style="border-left:5px solid {pack["color"]}"><div style="font-size:0.82rem;color:{muted}">{pack["intro"]}</div></div>',unsafe_allow_html=True)
jp1,jp2,jp3=st.tabs(["📖 Key Vocabulary","💬 Phrases","⚠️ Mistakes"])
with jp1:
    st.markdown("### Essential Words for This Job")
    st.markdown("".join([f'<span class="vocab-word">{w}</span>' for w in pack["vocab"]])+"<br>",unsafe_allow_html=True)
with jp2:
    st.markdown("### Real Phrases You Will Need")
    for situation,phrase in pack["phrases"]:
        st.markdown(f'<div class="phrase-box"><strong>{situation}:</strong><br>"{phrase}"</div>',unsafe_allow_html=True)
with jp3:
    st.markdown("### Common Mistakes in This Industry")
    for wrong,right in pack["mistakes"]:
        st.markdown(f'<div class="mistake-wrong">❌ "{wrong}"</div><div class="mistake-right">✅ "{right}"</div><br>',unsafe_allow_html=True)
st.markdown('</div>',unsafe_allow_html=True)

# COMMON MISTAKES
st.markdown('<div id="mistakes" class="section-wrap">',unsafe_allow_html=True)
st.markdown('<div class="hero-badge">⚠️ Common Mistakes</div>',unsafe_allow_html=True)
st.title("Common Mistakes Non-Native Speakers Make")
st.markdown("##### The most frequent English errors — and how to fix them.")
st.markdown('<hr class="divider">',unsafe_allow_html=True)
mistake_categories={
    "Grammar Mistakes":[("'I am agree'","'I agree'","'Agree' is a verb, not an adjective. You don't need 'am'."),("'She don't know'","'She doesn't know'","With he/she/it, use 'doesn't' not 'don't'."),("'Yesterday I go to work'","'Yesterday I went to work'","Use past tense for actions that already happened."),("'I have 25 years'","'I am 25 years old'","In English, you don't 'have' an age — you 'are' an age."),("'He is very success'","'He is very successful'","Use the adjective 'successful', not the noun 'success'."),("'I didn't went'","'I didn't go'","After 'didn't', always use the base form of the verb."),("'More better'","'Better'","'Better' is already comparative — don't add 'more'."),("'I am boring'","'I am bored'","'Boring' describes the thing. 'Bored' describes how you feel.")],
    "Preposition Mistakes":[("'I am married with her'","'I am married to her'","Use 'married to', not 'married with'."),("'Depends of the situation'","'Depends on the situation'","Use 'depends on', not 'depends of'."),("'I am interested on this'","'I am interested in this'","Use 'interested in', not 'interested on'."),("'She is good in English'","'She is good at English'","Use 'good at' for skills, not 'good in'."),("'I arrived to the airport'","'I arrived at the airport'","Use 'arrived at' for specific places.")],
    "Word Choice Mistakes":[("'I will call you on tomorrow'","'I will call you tomorrow'","Don't add 'on' before 'tomorrow' or 'yesterday'."),("'Can you borrow me your pen?'","'Can you lend me your pen?'","You borrow FROM someone. You lend TO someone."),("'I did a mistake'","'I made a mistake'","In English, mistakes are 'made', not 'done'."),("'It's depending on...'","'It depends on...'","'Depend' is not used in the continuous form."),("'I am coming from Spain'","'I am from Spain' or 'I come from Spain'","Use simple present for where you're from.")],
    "Politeness Mistakes":[("'Give me water'","'Could I have some water, please?'","Always add 'please' and soften requests."),("'I want to know...'","'I was wondering if you could tell me...'","Softer phrasing sounds more polite and professional."),("'You are wrong'","'I think there might be a misunderstanding'","Avoid direct accusations in professional settings."),("'This is bad'","'I have some concerns about this approach'","Use constructive language rather than blunt judgments.")],
}
for category,mistakes in mistake_categories.items():
    st.markdown(f"### {category}")
    for wrong,right,explanation in mistakes:
        st.markdown(f'<div class="mistake-card"><div class="mistake-wrong">❌ {wrong}</div><div class="mistake-right">✅ {right}</div><div style="font-size:0.85rem;color:{muted};margin-top:8px">💡 {explanation}</div></div>',unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
st.markdown('</div>',unsafe_allow_html=True)

# SEARCH
st.markdown('<div id="search" class="section-wrap">',unsafe_allow_html=True)
st.markdown('<div class="hero-badge">🔍 Search</div>',unsafe_allow_html=True)
st.title("Search Vocabulary")
st.markdown("##### Search any word across all 5 levels instantly.")
st.markdown('<hr class="divider">',unsafe_allow_html=True)
search_query=st.text_input("Search for a word...",placeholder="e.g. deadline, however, confident...",key="search_input")
if search_query.strip():
    results=list({w:(w,c,l) for w,c,l in ALL_VOCAB if search_query.lower() in w.lower() or search_query.lower() in c.lower()}.values())
    if results:
        st.markdown(f"**{len(results)} result(s) found for '{search_query}':**")
        lc_map={1:"#3b82f6",2:"#22c55e",3:"#f59e0b",4:"#ef4444",5:"#8b5cf6"}
        ln_map={1:"Beginner",2:"Elementary",3:"Intermediate",4:"Upper Intermediate",5:"Advanced"}
        for word,cat_or_def,lvl in sorted(results,key=lambda x:x[2]):
            color=lc_map[lvl]; lvl_name=ln_map[lvl]
            st.markdown(f'<div class="search-result"><div style="display:flex;align-items:center;gap:12px"><span style="font-family:\'Syne\',sans-serif;font-weight:800;font-size:1.1rem;color:{fg}">{word}</span><span style="background:{color};color:white;padding:2px 10px;font-size:0.7rem;font-family:\'Syne\',sans-serif;font-weight:700">Level {lvl} — {lvl_name}</span></div><div style="color:{muted};font-size:0.85rem;margin-top:4px">{cat_or_def}</div></div>',unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="step-card"><div style="color:{muted}">No results found for "{search_query}". Try a different word.</div></div>',unsafe_allow_html=True)
else:
    st.markdown(f'<div style="text-align:center;padding:32px;color:{muted};border:2px dashed {"#3a3a3a" if dm else "#d0c8b8"}"><div style="font-size:1.5rem;margin-bottom:8px">🔍</div><div>Type a word above to search all vocabulary across every level.</div></div>',unsafe_allow_html=True)
st.markdown('</div>',unsafe_allow_html=True)

# FLASHCARDS
st.markdown('<div id="flashcards" class="section-wrap">',unsafe_allow_html=True)
st.markdown('<div class="hero-badge">🃏 Flashcards</div>',unsafe_allow_html=True)
st.title("Flashcard Mode")
st.markdown("##### Flip cards to test your memory.")
st.markdown('<hr class="divider">',unsafe_allow_html=True)
fc_level=st.selectbox("Choose a level",[1,2,3,4,5],format_func=lambda x:f"Level {x} — {level_meta[x-1][2]}",key="fc_level_select")
cards=LEVEL_DATA[fc_level]["flashcards"]
idx=st.session_state.flashcard_index[fc_level]%len(cards)
flipped=st.session_state.flashcard_flipped
word,definition=cards[idx]
col_card,col_nav=st.columns([3,1])
with col_card:
    if not flipped:
        st.markdown(f'<div class="flashcard"><div style="font-family:\'Syne\',sans-serif;font-size:0.68rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:#e85d2f;margin-bottom:12px">WORD</div><div style="font-family:\'Syne\',sans-serif;font-size:2.2rem;font-weight:800;color:{fg}">{word}</div><div style="font-size:0.82rem;color:{muted};margin-top:12px">Click Flip to see the definition</div></div>',unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="flashcard" style="background:#e85d2f;border-color:#e85d2f;box-shadow:6px 6px 0px {border}"><div style="font-family:\'Syne\',sans-serif;font-size:0.68rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:rgba(255,255,255,0.7);margin-bottom:12px">DEFINITION</div><div style="font-family:\'Syne\',sans-serif;font-size:1.3rem;font-weight:700;color:white;text-align:center;line-height:1.4">{definition}</div><div style="font-size:0.78rem;color:rgba(255,255,255,0.6);margin-top:12px;font-style:italic">{word}</div></div>',unsafe_allow_html=True)
    st.markdown(f'<div style="color:{muted};font-size:0.8rem;margin-top:8px;text-align:center">Card {idx+1} of {len(cards)}</div>',unsafe_allow_html=True)
with col_nav:
    st.markdown("<br><br>",unsafe_allow_html=True)
    if st.button("🔄 Flip",key="fc_flip"): st.session_state.flashcard_flipped=not st.session_state.flashcard_flipped; st.rerun()
    if st.button("➡️ Next",key="fc_next"): st.session_state.flashcard_index[fc_level]=(idx+1)%len(cards); st.session_state.flashcard_flipped=False; st.rerun()
    if st.button("⬅️ Prev",key="fc_prev"): st.session_state.flashcard_index[fc_level]=(idx-1)%len(cards); st.session_state.flashcard_flipped=False; st.rerun()
    if st.button("🔀 Shuffle",key="fc_shuffle"): st.session_state.flashcard_index[fc_level]=random.randint(0,len(cards)-1); st.session_state.flashcard_flipped=False; st.rerun()
st.markdown('</div>',unsafe_allow_html=True)

# QUICK REVIEW
st.markdown('<div id="quick-review" class="section-wrap">',unsafe_allow_html=True)
st.markdown('<div class="hero-badge">⚡ Quick Review</div>',unsafe_allow_html=True)
st.title("Quick Review")
st.markdown("##### Randomly pulls 5 questions from completed levels to keep your knowledge sharp.")
st.markdown('<hr class="divider">',unsafe_allow_html=True)
completed_levels=[n for n,done in st.session_state.progress.items() if done]
if len(completed_levels)==0:
    st.markdown(f'<div class="step-card"><div class="step-label">Nothing to review yet</div><div style="color:{muted}">Complete at least one level quiz to unlock Quick Review.</div></div>',unsafe_allow_html=True)
else:
    if not st.session_state.quick_review_questions:
        all_questions=[]
        for lvl in completed_levels:
            for q,opts,ans in LEVEL_DATA[lvl]["questions"]: all_questions.append((lvl,q,opts,ans))
        sample=random.sample(all_questions,min(5,len(all_questions)))
        st.session_state.quick_review_questions=sample; st.session_state.quick_review_answers={}; st.session_state.quick_review_done=False
    if not st.session_state.quick_review_done:
        st.markdown("Answer these mixed questions, then press **Submit**.")
        review_responses={}
        for i,(lvl,q,opts,_) in enumerate(st.session_state.quick_review_questions):
            st.markdown(f'<span style="font-size:0.72rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#e85d2f">FROM LEVEL {lvl}</span>',unsafe_allow_html=True)
            val=st.radio(q,["— select —"]+opts,key=f"qr_{i}")
            review_responses[i]=val
        if st.button("Submit Review",key="qr_submit"):
            update_streak()
            correct=sum(1 for i,(_,_,_,ans) in enumerate(st.session_state.quick_review_questions) if review_responses.get(i)==ans)
            st.session_state.quick_review_answers=review_responses; st.session_state.quick_review_done=True
            award_xp(15); new_badges=check_badges()
            st.markdown(f"### Score: {correct} / {len(st.session_state.quick_review_questions)}")
            for i,(lvl,q,opts,ans) in enumerate(st.session_state.quick_review_questions):
                chosen=review_responses.get(i,"— select —")
                if chosen==ans: st.success(f"✅ Q{i+1}: Correct!")
                elif chosen=="— select —": st.warning(f"⚠️ Q{i+1}: Not answered. Answer: **{ans}**")
                else: st.error(f"❌ Q{i+1}: You chose '{chosen}'. Answer: **{ans}**")
            if correct==len(st.session_state.quick_review_questions): st.balloons()
            st.info("+15 XP earned!")
            for icon,name,desc in new_badges: st.success(f"🏅 New badge: {icon} **{name}** — {desc}")
    else:
        st.success("✅ Review complete!")
    if st.button("🔀 New Review Set",key="qr_new"): st.session_state.quick_review_questions=[]; st.session_state.quick_review_done=False; st.rerun()
st.markdown('</div>',unsafe_allow_html=True)

# AI CHAT
st.markdown('<div id="ai-chat" class="section-wrap">',unsafe_allow_html=True)
st.markdown('<div class="hero-badge">🤖 AI Conversation Partner</div>',unsafe_allow_html=True)
st.title("AI Conversation Partner")
st.markdown("##### Practice real English conversations. The AI corrects your mistakes and helps you improve.")
st.markdown('<hr class="divider">',unsafe_allow_html=True)
col_left,col_right=st.columns([2,1])
with col_right:
    st.markdown("### Settings")
    chat_level=st.selectbox("Your level",["Beginner (Level 1)","Elementary (Level 2)","Intermediate (Level 3)","Upper Intermediate (Level 4)","Advanced (Level 5)"],key="chat_level_select")
    scenario=st.selectbox("Practice scenario",["Free conversation","Job interview practice","Shopping at a store","Meeting someone new","Asking for directions","At a doctor's office","Calling customer service","Negotiating a salary","Resolving a complaint","Healthcare workplace","Restaurant service","Construction site"])
    st.markdown(f'<div class="step-card" style="padding:14px 18px"><div class="step-label">How it works</div><div style="font-size:0.86rem;color:{muted};line-height:1.8">Type in English and the AI will:<br>✅ Respond naturally<br>✅ Correct any mistakes<br>✅ Explain why something is wrong<br>✅ Match your level</div></div>',unsafe_allow_html=True)
    if st.button("Clear Chat",key="clear_chat"): st.session_state.chat_messages=[]; st.rerun()
with col_left:
    st.markdown("### Conversation")
    if not st.session_state.chat_messages:
        st.markdown(f'<div style="text-align:center;padding:40px;color:{muted};border:2px dashed {"#3a3a3a" if dm else "#d0c8b8"}"><div style="font-size:2rem;margin-bottom:8px">💬</div><div style="font-family:\'Syne\',sans-serif;font-weight:700;color:{fg}">Start the conversation!</div><div style="font-size:0.86rem;margin-top:4px">Type something below to begin practicing.</div></div>',unsafe_allow_html=True)
    else:
        for msg in st.session_state.chat_messages:
            if msg["role"]=="user": st.markdown(f'<div class="chat-user">🧑 {msg["content"]}</div>',unsafe_allow_html=True)
            else: st.markdown(f'<div class="chat-ai">🤖 {msg["content"]}</div>',unsafe_allow_html=True)
    user_input=st.text_input("Type your message in English...",key="chat_input",label_visibility="collapsed",placeholder="Type your message in English...")
    if st.button("Send →",key="chat_send") and user_input.strip():
        st.session_state.chat_messages.append({"role":"user","content":user_input.strip()})
        li={"Beginner (Level 1)":"Use very simple words and short sentences. Avoid complex grammar.","Elementary (Level 2)":"Use simple sentences. Introduce basic grammar. Be encouraging.","Intermediate (Level 3)":"Use normal conversational English. Correct major errors.","Upper Intermediate (Level 4)":"Use natural English. Correct subtle errors. Use professional vocabulary.","Advanced (Level 5)":"Use rich natural English including idioms. Correct any errors precisely."}
        sp=f"""You are Echo, a friendly English conversation tutor on Echo English.
Student level: {chat_level}
Scenario: {scenario}
Instructions:
1. Respond naturally within the scenario.
2. End every response with a "📝 Feedback:" section: point out grammar/vocabulary mistakes kindly, suggest better phrasing if needed, give one short tip.
3. {li.get(chat_level,"")}
Format: [Your conversational response]\n\n📝 Feedback:\n[Correction and tip — 2-3 lines max]"""
        try:
            api_key=st.secrets["ANTHROPIC_API_KEY"]
            history=[{"role":m["role"],"content":m["content"]} for m in st.session_state.chat_messages]
            response=requests.post("https://api.anthropic.com/v1/messages",headers={"Content-Type":"application/json","x-api-key":api_key,"anthropic-version":"2023-06-01"},json={"model":"claude-sonnet-4-20250514","max_tokens":1000,"system":sp,"messages":history})
            ai_text=response.json()["content"][0]["text"]
        except Exception as e:
            ai_text=f"Sorry, I couldn't connect right now. Please try again. (Error: {e})"
        st.session_state.chat_messages.append({"role":"assistant","content":ai_text}); st.rerun()
st.markdown('</div>',unsafe_allow_html=True)

# CERTIFICATE
st.markdown('<div id="certificate" class="section-wrap">',unsafe_allow_html=True)
st.markdown('<div class="hero-badge">🏆 Certificate</div>',unsafe_allow_html=True)
st.title("Certificate of Completion")
st.markdown("##### Complete all 5 levels to earn your official Echo English certificate.")
st.markdown('<hr class="divider">',unsafe_allow_html=True)
all_done=all(st.session_state.progress.values())
completed_count=sum(st.session_state.progress.values())
if not all_done:
    st.markdown(f'<div class="step-card"><div class="step-label">Progress</div><div class="step-title">{completed_count} / 5 Levels Complete</div><div style="color:{muted};font-size:0.93rem">Complete all 5 levels to unlock your certificate. Keep going!</div></div>',unsafe_allow_html=True)
    remaining=[f"Level {n}" for n,done in st.session_state.progress.items() if not done]
    st.markdown(f"**Still needed:** {', '.join(remaining)}")
    st.markdown(f'<div class="progress-bar-wrap"><div class="progress-bar-fill" style="width:{int(completed_count/5*100)}%"></div></div>',unsafe_allow_html=True)
else:
    st.success("🎉 You've completed all 5 levels! Your certificate is ready.")
    cc1,cc2=st.columns([2,1])
    with cc1: name_input=st.text_input("Enter your full name for the certificate:",key="cert_name_input",placeholder="e.g. Maria Rodriguez")
    with cc2:
        st.markdown("<br>",unsafe_allow_html=True)
        if st.button("📄 Generate Certificate",key="gen_cert") and name_input.strip():
            pdf_bytes=generate_certificate(name_input.strip())
            b64=base64.b64encode(pdf_bytes).decode()
            st.markdown(f'<a href="data:application/pdf;base64,{b64}" download="Echo_English_Certificate_{name_input.strip().replace(" ","_")}.pdf" style="background:#e85d2f;color:white;padding:12px 24px;font-family:Syne,sans-serif;font-weight:700;text-decoration:none;display:inline-block;box-shadow:3px 3px 0px #1a1a1a;letter-spacing:1px">⬇️ Download Certificate</a>',unsafe_allow_html=True)
st.markdown('</div>',unsafe_allow_html=True)

# PRONUNCIATION GUIDE
st.markdown('<div id="pronunciation" class="section-wrap">',unsafe_allow_html=True)
st.markdown('<div class="hero-badge">🔊 Pronunciation Guide</div>',unsafe_allow_html=True)
st.title("Pronunciation Guide")
st.markdown("##### Click any word to hear it spoken aloud. Practice until it sounds natural.")
st.markdown('<hr class="divider">',unsafe_allow_html=True)

st.markdown(f"""
<div class="step-card" style="padding:16px 20px;margin-bottom:24px">
  <div class="step-label">How it works</div>
  <div style="font-size:0.88rem;color:{muted};line-height:1.8">
    Click the <strong>🔊 Hear It</strong> button next to any word or phrase to hear it spoken aloud using your browser's built-in speech engine.
    Use the <strong>Speed</strong> slider to slow it down if needed. Works best in Chrome.
  </div>
</div>
""",unsafe_allow_html=True)

pronunciation_data = {
    "🔤 Commonly Mispronounced Words": [
        ("Comfortable",     "KUM-fer-tuh-bul",  "Many people say 'com-FOR-ta-ble' — drop the middle syllable."),
        ("Vegetable",       "VEJ-tuh-bul",      "3 syllables, not 4. Not 'veg-eh-TAH-bul'."),
        ("February",        "FEB-roo-eh-ree",   "The first 'r' is often dropped in natural speech: 'FEB-yoo-ery'."),
        ("Wednesday",       "WENZ-day",         "The 'd' is silent. Never say 'Wed-nes-day'."),
        ("Pronunciation",   "pruh-NUN-see-AY-shun", "Not 'pro-NOUN-ciation'. The root changes spelling."),
        ("Clothes",         "KLOHZ",            "The 'th' is silent. Sounds like 'close'."),
        ("Choir",           "KWY-er",           "The 'ch' sounds like 'k'. Not 'cho-EER'."),
        ("Colonel",         "KER-nel",          "Completely irregular — sounds like 'kernel'."),
        ("Especially",      "eh-SPESH-uh-lee",  "Not 'ex-specially'. There is no 'x' sound."),
        ("Probably",        "PROB-uh-blee",      "Often shortened to 'prob-lee' in fast natural speech."),
    ],
    "💼 Workplace Words": [
        ("Schedule",        "SKEJ-yool (US) / SHED-yool (UK)", "Both are correct — depends on which English you are learning."),
        ("Colleague",       "KOL-eeg",          "The 'ue' at the end is silent."),
        ("Negotiate",       "neh-GOH-shee-ayt", "5 syllables. Stress is on the second syllable."),
        ("Prioritize",      "pry-OR-ih-tyz",    "Stress on the second syllable, not the first."),
        ("Demonstrate",     "DEM-un-strayt",    "Stress on the first syllable."),
        ("Collaborate",     "kuh-LAB-uh-rayt",  "Stress on the second syllable."),
        ("Appreciate",      "uh-PREE-shee-ayt", "5 syllables. Commonly mispronounced as 4."),
        ("Enthusiastic",    "en-THYOO-zee-AS-tik", "6 syllables — take it slowly."),
    ],
    "🗣️ Tricky Sounds for Non-Native Speakers": [
        ("Think / Thing",   "th- sound",        "Put your tongue between your teeth. Not 'tink' or 'sink'."),
        ("This / That",     "voiced th- sound", "Same position but with voice. Not 'dis' or 'dat'."),
        ("World",           "WERLD",            "The 'or' makes a 'er' sound. Not 'WOLD' or 'WORLD' with two syllables."),
        ("Shirt / Sheet",   "short vs long 'ee'","'Shirt' has a short vowel. 'Sheet' is longer. Practice the difference."),
        ("Beach / Bitch",   "long vs short 'ee'","Very different vowel lengths. Stress the long 'ee' in 'beach'."),
        ("Vowel",           "VOW-ul",           "2 syllables. The 'w' is part of the first syllable."),
        ("Rural",           "ROOR-ul",          "One of the hardest words — two 'r' sounds close together."),
        ("Squirrel",        "SKWER-ul",         "Another tricky 'r' word. Practice slowly: sk-wer-ul."),
    ],
    "📞 Phrases for Work & Daily Life": [
        ("Could you repeat that?",      "kud yoo reh-PEET that",     "Natural and polite way to ask someone to say it again."),
        ("I'll get back to you.",        "yl get BAK too yoo",        "'I will' contracts to 'I'll' in natural speech."),
        ("Let me check on that.",        "let mee CHEK on that",      "A safe professional phrase when you are unsure."),
        ("What time works for you?",     "wut tym werks fer yoo",     "'For' reduces to 'fer' in fast natural speech."),
        ("Nice to meet you.",            "NYS too MEET yoo",          "The 't' in 'meet' is often a soft tap in American English."),
        ("How's it going?",              "howz it GOH-ing",           "Very common casual greeting. 'How is it' contracts to 'How's it'."),
    ],
}

speed_js = """
<script>
function speakText(text, speed) {
    window.speechSynthesis.cancel();
    var msg = new SpeechSynthesisUtterance(text);
    msg.rate = speed || 1.0;
    msg.lang = 'en-US';
    window.speechSynthesis.speak(msg);
}
</script>
"""
st.markdown(speed_js, unsafe_allow_html=True)

pron_speed = st.slider("🐢 Playback Speed", min_value=0.5, max_value=1.5, value=1.0, step=0.1, key="pron_speed", help="Lower = slower. Try 0.7 for difficult words.")

for category, words in pronunciation_data.items():
    st.markdown(f"### {category}")
    for word, phonetic, tip in words:
        col_word, col_btn = st.columns([5, 1])
        with col_word:
            st.markdown(f"""
            <div class="phrase-box" style="margin-bottom:4px">
              <div style="display:flex;align-items:baseline;gap:10px">
                <strong style="font-size:1.05rem;color:{fg}">{word}</strong>
                <span style="font-size:0.82rem;color:#e85d2f;font-family:'Syne',sans-serif;font-weight:700">{phonetic}</span>
              </div>
              <div style="font-size:0.83rem;color:{muted};margin-top:4px">💡 {tip}</div>
            </div>""", unsafe_allow_html=True)
        with col_btn:
            safe_word = word.replace("'", "\\'").replace('"', '\\"').split('/')[0].strip()
            st.markdown(f"""
            <div style="padding-top:8px">
              <button onclick="speakText('{safe_word}', {pron_speed})"
                style="background:#e85d2f;color:white;border:none;padding:8px 14px;
                font-family:'Syne',sans-serif;font-weight:700;font-size:0.78rem;
                cursor:pointer;box-shadow:2px 2px 0px {border};letter-spacing:1px">
                🔊 Hear It
              </button>
            </div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

st.markdown('</div>',unsafe_allow_html=True)

# GRAMMAR GUIDE
st.markdown('<div id="grammar" class="section-wrap">',unsafe_allow_html=True)
st.markdown('<div class="hero-badge">📚 Grammar Guide</div>',unsafe_allow_html=True)
st.title("Grammar Guide")
st.markdown("##### Clear explanations of the most important English grammar rules — no jargon.")
st.markdown('<hr class="divider">',unsafe_allow_html=True)

grammar_topics = {
    "⏰ Verb Tenses": [
        {
            "title": "Simple Present",
            "use": "For habits, facts, and routines.",
            "structure": "Subject + base verb (+ s/es for he/she/it)",
            "examples": [
                ("✅ I work every day.", "✅ She works at a hospital."),
                ("❌ I am work every day.", "❌ She work at a hospital."),
            ],
            "tip": "Add -s or -es when the subject is he, she, or it.",
        },
        {
            "title": "Simple Past",
            "use": "For actions that are completely finished.",
            "structure": "Subject + verb-ed (or irregular past form)",
            "examples": [
                ("✅ I worked yesterday.", "✅ She went to the store."),
                ("❌ I work yesterday.", "❌ She goed to the store."),
            ],
            "tip": "Many common verbs are irregular: go→went, buy→bought, have→had, say→said.",
        },
        {
            "title": "Present Continuous",
            "use": "For actions happening right now, or temporary situations.",
            "structure": "Subject + am/is/are + verb-ing",
            "examples": [
                ("✅ I am studying English.", "✅ She is working from home this week."),
                ("❌ I studying English.", "❌ She working from home."),
            ],
            "tip": "You must include am/is/are. You cannot just use the -ing form alone.",
        },
        {
            "title": "Present Perfect",
            "use": "For past actions that connect to now, or life experiences.",
            "structure": "Subject + have/has + past participle",
            "examples": [
                ("✅ I have lived here for 3 years.", "✅ She has finished the report."),
                ("❌ I live here since 3 years.", "❌ She finished the report already. (if it still affects now)"),
            ],
            "tip": "Use 'for' with a period of time (for 3 years). Use 'since' with a start point (since 2020).",
        },
        {
            "title": "Future: Will vs Going To",
            "use": "'Will' for decisions made now or promises. 'Going to' for plans already made.",
            "structure": "will + base verb / am-is-are + going to + base verb",
            "examples": [
                ("✅ I will help you. (decided just now)", "✅ I am going to visit my sister. (already planned)"),
                ("❌ I will to go.", "❌ I going to visit."),
            ],
            "tip": "Both are correct future forms — the difference is about when you decided.",
        },
    ],
    "📌 Articles: A, An, The": [
        {
            "title": "When to use 'A' and 'An'",
            "use": "Use before singular countable nouns when mentioned for the first time.",
            "structure": "A + consonant sound | An + vowel sound",
            "examples": [
                ("✅ I have a job.", "✅ She is an engineer."),
                ("❌ I have job.", "❌ She is a engineer."),
            ],
            "tip": "It depends on the SOUND, not the letter. 'A university' (yoo-sound), 'An hour' (silent h).",
        },
        {
            "title": "When to use 'The'",
            "use": "Use when both speaker and listener know which thing you mean.",
            "structure": "The + noun (singular or plural)",
            "examples": [
                ("✅ I saw a dog. The dog was friendly.", "✅ Please close the door."),
                ("❌ I saw dog.", "❌ Please close door."),
            ],
            "tip": "Use 'the' for second mention, unique things (the sun, the internet), and specific things you both know.",
        },
        {
            "title": "When to use NO article",
            "use": "No article before plural nouns in general, and uncountable nouns in general.",
            "structure": "No article + plural/uncountable noun",
            "examples": [
                ("✅ Dogs are friendly animals.", "✅ I drink coffee every morning."),
                ("❌ The dogs are friendly animals. (in general)", "❌ I drink the coffee every morning."),
            ],
            "tip": "No article for general statements: 'I love music.' But 'I love the music at this party.' (specific)",
        },
    ],
    "🔗 Prepositions of Time & Place": [
        {
            "title": "In / On / At — Time",
            "use": "These three prepositions cover almost all time expressions.",
            "structure": "IN (months, years, seasons) | ON (days, dates) | AT (specific times, holidays)",
            "examples": [
                ("✅ In January / in 2024 / in summer", "✅ On Monday / on March 5th"),
                ("✅ At 3pm / at night / at Christmas", "❌ On January / in Monday / in 3pm"),
            ],
            "tip": "Think: big→small. IN for big periods, ON for days, AT for exact points.",
        },
        {
            "title": "In / On / At — Place",
            "use": "Use for locations and positions.",
            "structure": "IN (enclosed spaces) | ON (surfaces, floors) | AT (specific points/addresses)",
            "examples": [
                ("✅ In the office / in a country", "✅ On the table / on the 3rd floor"),
                ("✅ At the bus stop / at 42 Main Street", "❌ In the bus stop / on the country"),
            ],
            "tip": "AT is for a point (I'm at the bank). IN is for inside. ON is for surfaces.",
        },
    ],
    "❓ Question Formation": [
        {
            "title": "Yes/No Questions",
            "use": "Questions that can be answered with yes or no.",
            "structure": "Auxiliary verb + subject + main verb",
            "examples": [
                ("✅ Do you work here?", "✅ Is she coming to the meeting?"),
                ("❌ You work here?", "❌ She is coming to the meeting?"),
            ],
            "tip": "In English, you must invert the subject and auxiliary. You cannot just use a rising tone alone.",
        },
        {
            "title": "Wh- Questions",
            "use": "Questions asking for specific information.",
            "structure": "Wh-word + auxiliary + subject + verb",
            "examples": [
                ("✅ Where do you work?", "✅ What time does it start?"),
                ("❌ Where you work?", "❌ What time it starts?"),
            ],
            "tip": "The auxiliary (do/does/did/is/are) must come before the subject in questions.",
        },
    ],
    "🔄 Countable vs Uncountable Nouns": [
        {
            "title": "Countable Nouns",
            "use": "Things you can count. They have singular and plural forms.",
            "structure": "1 job / 2 jobs | a mistake / mistakes",
            "examples": [
                ("✅ I made two mistakes.", "✅ Can I ask a question?"),
                ("❌ I made two mistake.", "❌ Can I ask question?"),
            ],
            "tip": "If you can put a number in front of it, it's countable.",
        },
        {
            "title": "Uncountable Nouns",
            "use": "Things you cannot count directly. No plural form.",
            "structure": "No article or 'some' | never 'a' or a number",
            "examples": [
                ("✅ I need some advice.", "✅ She gave me useful information."),
                ("❌ I need an advice.", "❌ She gave me three informations."),
            ],
            "tip": "Common uncountables: advice, information, news, furniture, luggage, money, traffic, weather.",
        },
    ],
}

for topic, rules in grammar_topics.items():
    st.markdown(f"### {topic}")
    for rule in rules:
        with st.expander(f"📖 {rule['title']}"):
            col_a, col_b = st.columns([1, 1])
            with col_a:
                st.markdown(f'<div class="phrase-box" style="border-left-color:#8b5cf6"><strong>When to use it:</strong><br>{rule["use"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="phrase-box" style="border-left-color:#3b82f6"><strong>Structure:</strong><br><code>{rule["structure"]}</code></div>', unsafe_allow_html=True)
            with col_b:
                st.markdown(f'<div class="phrase-box" style="border-left-color:#f59e0b"><strong>💡 Tip:</strong><br>{rule["tip"]}</div>', unsafe_allow_html=True)
            st.markdown("**Examples:**")
            for ex_good, ex_bad in rule["examples"]:
                ec1, ec2 = st.columns(2)
                ec1.markdown(f'<div class="mistake-right" style="font-size:0.88rem">{ex_good}</div>', unsafe_allow_html=True)
                ec2.markdown(f'<div class="mistake-wrong" style="font-size:0.88rem">{ex_bad}</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

st.markdown('</div>',unsafe_allow_html=True)

# ABOUT
st.markdown('<div id="about" class="section-wrap">',unsafe_allow_html=True)
st.markdown('<div class="hero-badge">👋 About</div>',unsafe_allow_html=True)
st.title("About the Creator")
st.markdown('<hr class="divider">',unsafe_allow_html=True)
ac1,ac2=st.columns([2,1])
with ac1:
    st.markdown(f'<div class="step-card"><div class="step-label">The Story</div><div class="step-title">Why I Built Echo English</div><div style="font-size:0.97rem;line-height:1.8;color:{fg}">My name is <strong>Connor Burdick</strong>, and I built Echo English because I saw a real problem that existing tools were not solving.<br><br>People who move to English-speaking countries face a massive barrier — they cannot hold a basic conversation, cannot get a job that matches their skills, and feel isolated every day. Apps like Duolingo gamify learning but do not teach real conversation. Classes are expensive and rigid.<br><br>Echo English is different. It is built around <strong>real-world English</strong> — the kind you need at work, at the doctor, in a job interview, at the store. No ads, no gimmicks. Just genuine learning at your own pace, powered by AI.</div></div>',unsafe_allow_html=True)
    st.markdown(f'<div class="step-card"><div class="step-label">The Mission</div><div class="step-title">What Echo English Is For</div><div style="font-size:0.97rem;line-height:1.8;color:{fg}">Echo English exists to close the language gap for immigrants, refugees, international students, and anyone navigating life in an English-speaking country.<br><br>The goal is simple: <strong>help people speak English confidently enough to get a job, make friends, and live the life they came here for.</strong></div></div>',unsafe_allow_html=True)
with ac2:
    st.markdown(f'<div class="step-card" style="padding:22px 24px"><div class="step-label">Quick Facts</div><div style="font-size:0.9rem;line-height:2;color:{fg}">👤 <strong>Creator:</strong> Connor Burdick<br>🏫 <strong>Type:</strong> School Business Project<br>🌍 <strong>Target Users:</strong> Non-native English speakers<br>💻 <strong>Built With:</strong> Python + Streamlit<br>🤖 <strong>AI:</strong> Claude by Anthropic<br>🚫 <strong>Ads:</strong> Zero. Never.<br>📅 <strong>Launched:</strong> 2026</div></div>',unsafe_allow_html=True)
    st.markdown(f'<div class="step-card" style="padding:22px 24px"><div class="step-label">What\'s Inside</div><div style="font-size:0.88rem;line-height:1.9;color:{fg}">📘 5 Learning Levels<br>🎯 Placement Quiz<br>🤖 AI Conversation Partner<br>🃏 Flashcard Mode<br>⚡ XP and Badge System<br>💼 5 Job Vocabulary Packs<br>⚠️ Common Mistakes Guide<br>🔍 Vocabulary Search<br>🔊 Pronunciation Guide<br>📚 Grammar Guide<br>📊 Progress Tracker<br>🏆 Certificate of Completion</div></div>',unsafe_allow_html=True)
st.markdown('</div>',unsafe_allow_html=True)

# FEEDBACK
st.markdown('<div id="feedback" class="section-wrap">',unsafe_allow_html=True)
st.markdown('<div class="hero-badge">💬 Feedback</div>',unsafe_allow_html=True)
st.title("Share Your Feedback")
st.markdown("##### Help make Echo English better.")
st.markdown('<hr class="divider">',unsafe_allow_html=True)
fb1,fb2=st.columns([2,1])
with fb1:
    if not st.session_state.feedback_submitted:
        st.selectbox("What kind of feedback?",["💡 Suggest a new word or phrase","🐛 Report a confusing question","⭐ General feedback / praise","🔧 Something isn't working"])
        st.selectbox("Which level is this about?",["General / All levels","Level 1 – Beginner","Level 2 – Elementary","Level 3 – Intermediate","Level 4 – Upper Intermediate","Level 5 – Advanced"])
        fb_text=st.text_area("Your feedback:",placeholder="Type your feedback here...",key="fb_text",height=120)
        if st.button("Submit Feedback",key="fb_submit"):
            if fb_text.strip(): st.session_state.feedback_submitted=True; st.rerun()
            else: st.warning("Please write your feedback before submitting.")
    else:
        st.success("Thank you! Your feedback helps make Echo English better for everyone.")
        if st.button("Submit More Feedback",key="fb_more"): st.session_state.feedback_submitted=False; st.rerun()
with fb2:
    st.markdown(f'<div class="step-card" style="padding:18px 22px"><div class="step-label">Why it matters</div><div style="font-size:0.87rem;color:{muted};line-height:1.8">Your feedback directly shapes Echo English. Every suggestion is read and considered.</div></div>',unsafe_allow_html=True)
st.markdown('</div>',unsafe_allow_html=True)

st.markdown(f"""
<div style="background:#1a1a1a;color:#f5f0e8;text-align:center;padding:40px">
  <div style="font-family:'Syne',sans-serif;font-weight:800;font-size:1.4rem;color:#e85d2f;margin-bottom:8px">🔊 Echo English</div>
  <div style="color:#888;font-size:0.85rem;margin-bottom:16px">Learn at your own pace · Zero ads · Powered by AI · Created by Connor Burdick</div>
  <div style="display:flex;justify-content:center;gap:20px;font-size:0.75rem;color:#555;flex-wrap:wrap">
    <span>5 Levels</span><span>·</span><span>AI Partner</span><span>·</span><span>Flashcards</span><span>·</span><span>XP and Badges</span><span>·</span><span>Job Packs</span><span>·</span><span>Pronunciation</span><span>·</span><span>Grammar Guide</span><span>·</span><span>Certificate</span>
  </div>
</div>
""",unsafe_allow_html=True)
