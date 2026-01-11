import requests
import re

URL_A = "https://ade-web-consult.univ-amu.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?projectId=8&resources=163180&calType=ical&firstDate=2026-01-19&lastDate=2026-06-05"
URL_G = "https://ade-web-consult.univ-amu.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?projectId=8&resources=189063&calType=ical&firstDate=2026-01-19&lastDate=2026-06-04"

def get_events(url):
    text = requests.get(url).text
    events = re.findall(r"BEGIN:VEVENT.*?END:VEVENT", text, re.S)
    header = text.split("BEGIN:VEVENT")[0]
    return header, events

header, events_A = get_events(URL_A)
_, events_G = get_events(URL_G)

filtered = []

for ev in events_A:
    low = ev.lower()
    if "statistique inférentielle" in low:
        continue
    filtered.append(ev)

for ev in events_G:
    if "smi6u23_maths en jeans_td".lower() in ev.lower():
        filtered.append(ev)

with open("filtered.ics", "w", encoding="utf-8") as f:
    f.write(header)
    for ev in filtered:
        f.write(ev + "\n")
    f.write("END:VCALENDAR\n")
