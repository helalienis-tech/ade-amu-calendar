
import requests
import re

URL_A = "https://ade-web-consult.univ-amu.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?projectId=8&resources=163180&calType=ical&firstDate=2026-01-19&lastDate=2026-06-05"
URL_G = "https://ade-web-consult.univ-amu.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?projectId=8&resources=189063&calType=ical&firstDate=2026-01-19&lastDate=2026-06-04"

def load_ics(url):
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.text

ics_a = load_ics(URL_A)
ics_g = load_ics(URL_G)

events_a = re.findall(r"BEGIN:VEVENT.*?END:VEVENT", ics_a, re.S)
events_g = re.findall(r"BEGIN:VEVENT.*?END:VEVENT", ics_g, re.S)

header = ics_a.split("BEGIN:VEVENT")[0]

filtered_events = []

for ev in events_a:
    if "statistique inférentielle" in ev.lower():
        continue
    filtered_events.append(ev)

for ev in events_g:
    if "smi6u23_maths en jeans_td" in ev.lower():
        filtered_events.append(ev)

with open("filtered.ics", "w", encoding="utf-8") as f:
    f.write(header)
    for ev in filtered_events:
        f.write(ev + "\n")
    f.write("END:VCALENDAR\n")

print(f"Calendrier généré avec {len(filtered_events)} événements")
