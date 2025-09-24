from .config import SOURCE_WEIGHTS

def src_weight(src):
    for k, v in SOURCE_WEIGHTS.items():
        if k in src:
            return v
    return SOURCE_WEIGHTS.get("generic", 1.0)

def score(item):
    # abs move * source weight * simple volume flag
    base = abs(float(item.get("ret15", 0.0)))
    w = src_weight(item.get("source",""))
    volflag = 1.1 if float(item.get("vol1",0)) > float(item.get("vol0",0))*1.5 else 1.0
    return base * w * volflag
