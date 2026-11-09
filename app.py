import streamlit as st
from datetime import date, timedelta

st.set_page_config(page_title="ORBIT | Productivity Command Center", page_icon="◈", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
:root{--bg:#090d19;--panel:#11182a;--line:#25314a;--text:#eef2ff;--muted:#8d9ab6;--violet:#9274ff;--cyan:#54d8e8}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif}
.stApp{background:radial-gradient(circle at 80% 0%,#1a1c3b 0%,var(--bg) 42%);color:var(--text)}
.block-container{padding-top:2rem;max-width:1400px}
h1,h2,h3{font-family:'Space Grotesk',sans-serif!important;color:var(--text)!important}
[data-testid="stSidebar"]{background:#0d1322;border-right:1px solid var(--line)}
.panel,.mission{background:linear-gradient(145deg,#151f35,#0f1728);border:1px solid var(--line);border-radius:16px;padding:1rem 1.2rem;margin-bottom:.8rem}
.eyebrow{color:var(--cyan);font-size:.72rem;font-weight:700;letter-spacing:2px}
.hero{font-family:'Space Grotesk';font-size:2.6rem;font-weight:700;line-height:1.1;margin:.5rem 0}
.muted{color:var(--muted);font-size:.85rem}
.metric{font-size:2rem;font-family:'Space Grotesk';font-weight:700}
.stButton>button{border-radius:10px;border:1px solid #51458c;background:linear-gradient(110deg,#7658e8,#4b6fc8);color:white;font-weight:700}
.stTextInput input,.stSelectbox div[data-baseweb="select"]{background:#111a2c;color:#eef2ff}
</style>
""", unsafe_allow_html=True)

if "missions" not in st.session_state:
    st.session_state.missions = [
        {"id":1,"title":"Review Python dictionaries","category":"Study","priority":"High","due":date.today(),"done":False},
        {"id":2,"title":"Sketch a landing page concept","category":"Creative","priority":"Medium","due":date.today()+timedelta(days=1),"done":False},
        {"id":3,"title":"Organise portfolio screenshots","category":"Personal","priority":"Low","due":date.today()+timedelta(days=2),"done":True}
    ]
if "focus" not in st.session_state: st.session_state.focus = []
if "xp" not in st.session_state: st.session_state.xp = 40
if "next_id" not in st.session_state: st.session_state.next_id = 4
if "page" not in st.session_state: st.session_state.page = "Dashboard"

missions=st.session_state.missions
done=[m for m in missions if m["done"]]
pending=[m for m in missions if not m["done"]]
level=st.session_state.xp//100+1

with st.sidebar:
    st.markdown("## ◈ ORBIT")
    st.caption("PRODUCTIVITY COMMAND CENTER")
    st.divider()
    for name in ["Dashboard","Missions","Focus","Achievements","Analytics"]:
        if st.button(name,use_container_width=True,key="nav_"+name): st.session_state.page=name
    st.divider()
    st.markdown(f"**LEVEL {level}** · {st.session_state.xp} XP")
    st.progress((st.session_state.xp%100)/100)
    st.caption("Small steps. Real progress.")

page=st.session_state.page
if page=="Dashboard":
    st.markdown('<div class="eyebrow">YOUR SPACE. YOUR PACE.</div><div class="hero">Make today<br>count.</div><p class="muted">A clear view of what matters, what is moving, and what comes next.</p>',unsafe_allow_html=True)
    a,b,c,d=st.columns(4)
    for col,label,value in [(a,"TOTAL MISSIONS",len(missions)),(b,"COMPLETED",len(done)),(c,"COMPLETION",f"{int(len(done)/len(missions)*100) if missions else 0}%"),(d,"FOCUS SESSIONS",len(st.session_state.focus))]:
        with col:
            st.markdown(f'<div class="panel"><div class="muted">{label}</div><div class="metric">{value}</div></div>',unsafe_allow_html=True)
    left,right=st.columns([1.3,1])
    with left:
        st.subheader("Today's missions")
        today=[m for m in missions if m["due"]==date.today()]
        if today:
            for m in today: st.markdown(f'<div class="mission"><b>{m["title"]}</b><div class="muted">{m["category"]} · {m["priority"]} priority · {"Completed" if m["done"] else "In progress"}</div></div>',unsafe_allow_html=True)
        else: st.info("No missions due today.")
        if st.button("＋ Create a mission"): st.session_state.page="Missions"; st.rerun()
    with right:
        st.subheader("Your current orbit")
        st.markdown(f'<div class="panel"><div class="eyebrow">EXPERIENCE POINTS</div><div class="metric">{st.session_state.xp} XP</div><p class="muted">Level {level} · {100-st.session_state.xp%100} XP to next level</p></div>',unsafe_allow_html=True)
        st.progress(len(done)/len(missions) if missions else 0)

elif page=="Missions":
    st.markdown('<div class="eyebrow">MISSION CONTROL</div><div class="hero">Turn plans into progress.</div>',unsafe_allow_html=True)
    with st.expander("＋ Add a new mission"):
        with st.form("add_mission",clear_on_submit=True):
            title=st.text_input("Mission name")
            x,y,z=st.columns(3)
            category=x.selectbox("Category",["Study","Creative","Personal","Work","Other"])
            priority=y.selectbox("Priority",["High","Medium","Low"])
            due=z.date_input("Due date",value=date.today())
            if st.form_submit_button("Add mission"):
                if title.strip():
                    missions.append({"id":st.session_state.next_id,"title":title.strip(),"category":category,"priority":priority,"due":due,"done":False})
                    st.session_state.next_id+=1; st.rerun()
                else: st.warning("Enter a mission name first.")
    f,g=st.columns(2)
    status=f.selectbox("Status",["All","In progress","Completed"])
    pr=g.selectbox("Priority",["Any priority","High","Medium","Low"])
    for m in missions:
        if (status=="All" or status=="Completed" and m["done"] or status=="In progress" and not m["done"]) and (pr=="Any priority" or m["priority"]==pr):
            st.markdown(f'<div class="mission"><b>{m["title"]}</b><div class="muted">{m["category"]} · Due {m["due"]:%d %b} · {m["priority"]} · {"Completed" if m["done"] else "In progress"}</div></div>',unsafe_allow_html=True)
            p,q=st.columns(2)
            if not m["done"] and p.button("Complete",key=f"complete{m['id']}"):
                m["done"]=True; st.session_state.xp+=20; st.rerun()
            if q.button("Delete",key=f"delete{m['id']}"):
                st.session_state.missions=[item for item in missions if item["id"]!=m["id"]]; st.rerun()

elif page=="Focus":
    st.markdown('<div class="eyebrow">FOCUS MODE</div><div class="hero">One thing at a time.</div>',unsafe_allow_html=True)
    options=["General focus"]+[m["title"] for m in pending]
    task=st.selectbox("What are you focusing on?",options)
    minutes=st.select_slider("Session length (minutes)",options=[10,15,20,25,30,45,60],value=25)
    st.markdown(f'<div class="panel"><div class="metric">{minutes}:00</div><p class="muted">Planned focus block. Use your own timer, then log the session.</p></div>',unsafe_allow_html=True)
    if st.button("Complete focus block"):
        st.session_state.focus.append({"task":task,"minutes":minutes,"date":date.today()})
        st.session_state.xp+=10; st.success("Session logged · +10 XP")
    st.subheader("Focus history")
    for s in st.session_state.focus[::-1][:5]: st.write(f"◷ {s['task']} · {s['minutes']} min · {s['date']}")

elif page=="Achievements":
    st.markdown('<div class="eyebrow">ACHIEVEMENT CENTER</div><div class="hero">Progress deserves a spotlight.</div>',unsafe_allow_html=True)
    achievements=[("First orbit","Complete your first mission",len(done)>=1),("Getting warmer","Complete 5 missions",len(done)>=5),("Mission master","Complete 10 missions",len(done)>=10),("Deep focus","Log 3 focus sessions",len(st.session_state.focus)>=3),("Time well spent","Log 100 focus minutes",sum(s["minutes"] for s in st.session_state.focus)>=100),("Consistent energy","Reach 200 XP",st.session_state.xp>=200)]
    cols=st.columns(3); unlocked=0
    for i,(name,desc,yes) in enumerate(achievements):
        if yes: unlocked+=1
        with cols[i%3]:
            st.markdown(f'<div class="panel"><div class="metric">{"✦" if yes else "◇"}</div><b>{name}</b><p class="muted">{desc}</p><div class="eyebrow">{"UNLOCKED" if yes else "LOCKED"}</div></div>',unsafe_allow_html=True)
    st.write(f"{unlocked} of {len(achievements)} achievements unlocked"); st.progress(unlocked/len(achievements))

elif page=="Analytics":
    st.markdown('<div class="eyebrow">YOUR ACTIVITY</div><div class="hero">See your momentum.</div>',unsafe_allow_html=True)
    x,y,z=st.columns(3)
    x.metric("Missions completed",len(done)); y.metric("Focus minutes",sum(s["minutes"] for s in st.session_state.focus)); z.metric("Completion rate",f"{int(len(done)/len(missions)*100) if missions else 0}%")
    st.subheader("Mission status"); st.bar_chart({"Completed":len(done),"In progress":len(pending)})
    st.subheader("Missions by category")
    categories={}
    for m in missions: categories[m["category"]]=categories.get(m["category"],0)+1
    if categories: st.bar_chart(categories)
    st.subheader("Focus sessions")
    if st.session_state.focus: st.bar_chart({"Minutes":[s["minutes"] for s in st.session_state.focus]})
    else: st.info("Log focus sessions to see activity here.")

st.divider()
st.caption("ORBIT · Build your momentum, one mission at a time.")
