import re,os
URL_RE=re.compile(r"(?i)\b((?:https?://|www\d{0,3}[.])[^\s()<>]+((?:\([^\s()<>]+\))|[^\s!()]))")
def find_urls(t): return [m[0] for m in URL_RE.findall(t)]
def cleanup_file(p):
    try:
        if p and os.path.exists(p): os.remove(p)
    except: pass
def contains_persian(t): return any(c in "چپژگکیاٍبتثجحخدذرزسشصضطظعغفقلمنوهی" for c in t)
