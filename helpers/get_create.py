from datetime import datetime,timezone
def get_creation_date(uid):
    try:
        ts=(uid-1376280044)//4096+1377543634
        if ts<0: return "قديم"
        return datetime.fromtimestamp(ts,tz=timezone.utc).strftime("%d/%m/%Y")
    except: return "غير معروف"
