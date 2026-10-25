def ph(label, note, ms=None, **kw):
    phase = {"label": label, "note": note}
    if ms:
        phase["ms"] = ms
    phase.update(kw)
    return phase


def c(t, cls=None, n=None, v=None):
    chip = {"t": t}
    if cls:
        chip["c"] = cls
    if n is not None:
        chip["n"] = n
    if v is not None:
        chip["v"] = v
    return chip


def row(cap, chips, box=False):
    return {"cap": cap, "chips": chips, "box": box}


def flow(nodes, phases):
    return {"kind": "flow", "nodes": [{"t": t, "s": s} for t, s in nodes], "phases": phases}


def seq(lanes, msgs, phases):
    out = []
    for m in msgs:
        f, t, text = m[:3]
        opts = m[3] if len(m) > 3 else ""
        out.append({"f": f, "t": t, "text": text, "code": "code" in opts, "bad": "bad" in opts})
    return {"kind": "seq", "lanes": lanes, "msgs": out, "phases": phases}


def bars(items, phases, title=None, unit="%", max=100, div=None):
    cfg = {"kind": "bars", "items": items, "phases": phases, "unit": unit, "max": max}
    if title:
        cfg["title"] = title
    if div:
        cfg["div"] = div
    return cfg


def scatter(points, groups, phases):
    return {"kind": "scatter", "points": points, "groups": groups, "phases": phases}


def chips(phases):
    return {"kind": "chips", "phases": phases}


def cycle(steps, phases, log=None):
    cfg = {"kind": "cycle", "steps": steps, "phases": phases}
    if log:
        cfg["log"] = log
    return cfg


def stack(layers, phases):
    return {"kind": "stack", "layers": [{"t": t, "s": s} for t, s in layers], "phases": phases}


def compare(left, right, phases):
    return {"kind": "compare", "left": left, "right": right, "phases": phases}


def grid(rows, cols, phases, title=None):
    cfg = {"kind": "grid", "rows": rows, "cols": cols, "phases": phases}
    if title:
        cfg["title"] = title
    return cfg


def part(viz, cap, h, *paras):
    return {"viz": viz, "cap": cap, "h": h, "p": list(paras)}


def topic(slug, title, tag, summary, lede, plain, parts, take, keywords=""):
    return {
        "slug": slug,
        "title": title,
        "tag": tag,
        "summary": summary,
        "lede": lede,
        "plain": plain,
        "parts": parts,
        "take": take,
        "keywords": keywords,
    }
