import streamlit as st, pandas as pd, random
from datetime import date,datetime,timedelta
import plotly.express as px
st.set_page_config(page_title="iConnect SA AI Automation",page_icon="🤖",layout="wide")
st.markdown("""<style>.stApp{background:linear-gradient(135deg,#080d1a,#101a32)} section[data-testid="stSidebar"]{background:#0b1224} div[data-testid="stMetric"]{background:#121c32;border:1px solid #263654;padding:14px;border-radius:12px}</style>""",unsafe_allow_html=True)
def init():
 for k,v in {"alerts":[],"approvals":[]}.items():
  if k not in st.session_state: st.session_state[k]=v
 if "campaigns" not in st.session_state: st.session_state.campaigns=pd.DataFrame([{"ID":"CMP-001","Campaign":"Fibre Upgrade Awareness","Objective":"Generate leads","Audience":"SME customers","Channel":"Email","Start date":date.today()+timedelta(days=3),"Budget (R)":5000,"Status":"Draft"}])
 if "results" not in st.session_state: st.session_state.results=pd.DataFrame([{"Campaign":"Fibre Upgrade Awareness","Impressions":12400,"Clicks":620,"Leads":48,"Spend (R)":2100},{"Campaign":"Connectivity Tips","Impressions":8900,"Clicks":410,"Leads":19,"Spend (R)":980}])
 if "tickets" not in st.session_state: st.session_state.tickets=pd.DataFrame([{"Ticket":"IC-1042","Issue":"Fibre down","Priority":"High","Status":"Open","Team":"Network Ops"},{"Ticket":"IC-1043","Issue":"Invoice copy","Priority":"Low","Status":"In progress","Team":"Billing"}])
init()
def classify(m):
 t=m.lower()
 for words,cat,p,team in [(("down","outage","offline"),"Connectivity","High","Network Ops"),(("slow","latency"),"Connectivity","Medium","Network Ops"),(("voip","call","phone"),"Voice","High","Voice Support"),(("invoice","billing","payment"),"Billing","Low","Billing"),(("password","login"),"Account access","Medium","Service Desk")]:
  if any(w in t for w in words): return cat,p,team
 return "General enquiry","Medium","Service Desk"
def makecopy(ch,aud,obj,offer,tone):
 extra=(" "+offer) if offer else ""
 if ch=="Email": return f"Subject: Stay connected with iConnect SA\\n\\nHi there,\\nDiscover solutions designed for {aud}. Objective: {obj}.{extra}\\nContact our team to explore your options.\\nThe iConnect SA Team"
 if ch=="Social": return f"Stay connected. Keep moving! For {aud}, discover solutions built around the way you work.{extra} Contact iConnect SA. #iConnectSA #StayConnected"
 if ch=="SMS": return f"iConnect SA: {offer or 'Explore connectivity options built for you.'} Contact our team. Reply STOP to opt out."
 return f"Campaign brief\\nAudience: {aud}\\nObjective: {obj}\\nMessage: Stay connected with iConnect SA.{extra}\\nTone: {tone}\\nCTA: Contact our team."
st.sidebar.title("🤖 iConnect SA")
st.sidebar.caption("AI Automation Control Room")
page=st.sidebar.radio("Navigation",["Overview","AI Customer Service","Ticket Queue","Alerts & Activity","Plan Campaigns","Generate Content","Schedule & Approvals","Report Results","Settings"])
st.sidebar.success("Demo environment online")
st.title("iConnect SA | AI Automation")
st.caption("Customer service · Campaign planning · Content generation · Approvals · Reporting")
camps=st.session_state.campaigns
if page=="Overview":
 a,b,c,d=st.columns(4); a.metric("Open tickets",sum(st.session_state.tickets.Status!="Resolved")); b.metric("Campaigns",len(camps)); c.metric("Awaiting approval",sum(x["Status"]=="Pending approval" for x in st.session_state.approvals)); d.metric("Reported leads",int(st.session_state.results.Leads.sum()))
 fig=px.bar(st.session_state.results,x="Campaign",y=["Impressions","Clicks","Leads"],barmode="group",template="plotly_dark"); st.plotly_chart(fig,use_container_width=True)
 st.dataframe(camps,use_container_width=True,hide_index=True)
elif page=="AI Customer Service":
 msg=st.text_area("Customer message")
 if st.button("Analyse enquiry",type="primary") and msg.strip(): st.session_state.triage={"msg":msg,"result":classify(msg)}
 if "triage" in st.session_state:
  x=st.session_state.triage; cat,p,team=x["result"]; a,b,c=st.columns(3); a.metric("Category",cat); b.metric("Priority",p); c.metric("Team",team)
  st.text_area("Suggested reply (review before use)",f"Thanks for contacting iConnect SA. Our {team} team will review your {cat.lower()} enquiry. Never send passwords or OTPs.")
  if st.button("Create ticket & alert"):
   tid=f"IC-{random.randint(2000,9999)}"; st.session_state.tickets.loc[len(st.session_state.tickets)]=[tid,x["msg"],p,"Open",team]
   st.session_state.alerts.insert(0,{"Time":str(datetime.now()),"Event":f"{tid} routed to {team}"}); st.success("Ticket created.")
elif page=="Ticket Queue":
 st.dataframe(st.session_state.tickets,use_container_width=True,hide_index=True)
elif page=="Alerts & Activity":
 st.dataframe(pd.DataFrame(st.session_state.alerts),use_container_width=True,hide_index=True) if st.session_state.alerts else st.success("No new alerts.")
elif page=="Plan Campaigns":
 with st.form("plan"):
  name=st.text_input("Campaign name"); obj=st.selectbox("Objective",["Generate leads","Awareness","Conversions","Engagement","Retention"]); aud=st.text_input("Target audience"); ch=st.selectbox("Channel",["Email","Social","SMS","Website","Multi-channel"]); start=st.date_input("Start date",date.today()+timedelta(days=7),min_value=date.today()); budget=st.number_input("Budget (R)",min_value=0,step=500); save=st.form_submit_button("Create campaign plan",type="primary")
 if save:
  if name.strip() and aud.strip():
   st.session_state.campaigns.loc[len(st.session_state.campaigns)]=[f"CMP-{random.randint(100,999)}",name,obj,aud,ch,start,budget,"Draft"]; st.success("Campaign plan created.")
  else: st.error("Enter campaign name and audience.")
 st.dataframe(st.session_state.campaigns,use_container_width=True,hide_index=True)
elif page=="Generate Content":
 with st.form("content"):
  campaign=st.selectbox("Campaign",camps.Campaign.tolist()); aud=st.text_input("Audience","iConnect SA customers"); obj=st.selectbox("Objective",["Generate leads","Awareness","Conversions","Engagement"]); ch=st.selectbox("Format",["Email","Social","SMS","Campaign brief"]); offer=st.text_input("Offer / key detail"); tone=st.selectbox("Tone",["Professional","Friendly","Helpful","Energetic"]); go=st.form_submit_button("Generate content",type="primary")
 if go: st.session_state.generated={"Campaign":campaign,"Channel":ch,"Content":makecopy(ch,aud,obj,offer,tone)}
 if "generated" in st.session_state:
  g=st.session_state.generated; edited=st.text_area("Editable draft",g["Content"],height=200)
  if st.button("Submit for approval",type="primary"):
   st.session_state.approvals.insert(0,{"Submitted":str(datetime.now()),"Campaign":g["Campaign"],"Channel":g["Channel"],"Content":edited,"Status":"Pending approval","Reviewer":"Unassigned","Scheduled date":"—"})
   st.session_state.alerts.insert(0,{"Time":str(datetime.now()),"Event":f"{g['Campaign']} submitted for approval"}); st.success("Sent to approval queue.")
elif page=="Schedule & Approvals":
 if not st.session_state.approvals: st.info("Generate content and submit it for approval first.")
 for i,x in enumerate(st.session_state.approvals):
  with st.expander(f"{x['Campaign']} · {x['Status']}",expanded=True):
   st.write(x["Content"])
   if x["Status"]=="Pending approval":
    reviewer=st.text_input("Reviewer", "Campaign approver",key=f"r{i}"); day=st.date_input("Schedule date",date.today()+timedelta(days=1),min_value=date.today(),key=f"d{i}")
    c1,c2=st.columns(2)
    if c1.button("Approve & schedule",key=f"a{i}"):
     x["Status"]="Scheduled"; x["Reviewer"]=reviewer; x["Scheduled date"]=str(day); st.session_state.alerts.insert(0,{"Time":str(datetime.now()),"Event":f"{x['Campaign']} scheduled for {day}"}); st.rerun()
    if c2.button("Request changes",key=f"n{i}"):
     x["Status"]="Changes requested"; x["Reviewer"]=reviewer; st.rerun()
 if st.session_state.approvals: st.dataframe(pd.DataFrame([{k:v for k,v in x.items() if k!="Content"} for x in st.session_state.approvals]),use_container_width=True,hide_index=True)
 st.caption("Scheduling records a plan; it does not publish externally.")
elif page=="Report Results":
 r=st.session_state.results.copy(); r["CTR (%)"]=(r.Clicks/r.Impressions*100).round(2); r["Lead rate (%)"]=(r.Leads/r.Clicks*100).round(2); r["Cost per lead (R)"]=(r["Spend (R)"]/r.Leads.replace(0,pd.NA)).round(2)
 a,b,c,d=st.columns(4); a.metric("Impressions",f"{r.Impressions.sum():,}"); b.metric("Clicks",f"{r.Clicks.sum():,}"); c.metric("Leads",int(r.Leads.sum())); d.metric("Spend",f"R{r['Spend (R)'].sum():,.0f}")
 st.dataframe(r,use_container_width=True,hide_index=True); st.download_button("Download CSV report",r.to_csv(index=False).encode(),file_name="iconnect_campaign_report.csv",mime="text/csv")
 with st.form("results"):
  name=st.text_input("Campaign"); imp=st.number_input("Impressions",min_value=0); clicks=st.number_input("Clicks",min_value=0); leads=st.number_input("Leads",min_value=0); spend=st.number_input("Spend (R)",min_value=0.0); add=st.form_submit_button("Add results")
 if add and name.strip(): st.session_state.results.loc[len(st.session_state.results)]=[name,imp,clicks,leads,spend]; st.success("Results added.")
elif page=="Settings":
 st.warning("Prototype only. No live integrations are connected.")
 st.write("Production checklist: authorised CRM/email/social APIs, authentication, role permissions, audit logs, consent/privacy controls, secure secrets, and human approval before publishing.")
st.caption("iConnect SA AI Automation · Simulated demo data · Human approval required")
