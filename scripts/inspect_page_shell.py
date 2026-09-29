import re
import requests

html = requests.get("https://www.immobilien-experten.de/impressum.html", timeout=40).text
print("len", len(html))
for m in re.finditer(r"<script[^>]{0,200}>", html):
    tag = m.group(0)
    if "google" in tag or "gtm" in tag or "src=" in tag:
        print("SCRIPT", tag[:220])
print("gtag count", html.count("function gtag"))
print("doPoll", "var doPoll = true" in html)
print("iwf", "iwf-form" in html)
print("contact widget", "contact_widget" in html)
# style tag lengths
for i, m in enumerate(re.finditer(r"<style[^>]*>(.*?)</style>", html, re.S)):
    if i < 3 or len(m.group(1)) > 5000:
        print("style", i, len(m.group(1)), m.group(0)[:40])
