#!/usr/bin/env python3
# s185-banda-e5.py — EMENDA E5 (rev. S-184 bis azione B): banda sentinella oracle ORM ri-fondata UNA volta su TUTTE le
# gambe oracle PULITE S-162..S-184 (ORM, 2 gambe giudicate per coppia; rodaggio escluso per canone).
# Gamba PULITA = coppia con parita' rc=0, verdetto NON dichiarato contaminato/tronco, gamba oracle NON segnalata ictx
# nel blocco orm_ictx/s. Net = user - floor oracle (riga floor_user_med3 del verdetto; 0.06 se assente).
# Esito: s185-banda-e5.out (ORA_REF = mediana, SENT_LO = min pulito [lato veloce = SEGNALAZIONE], SENT_HI = max pulito
# [lato lento = BLOCCO], tetto ictx ASSOLUTO 200/s per gamba (rev. #5; storico: pulite ≤148/s, contaminate ≥214/s), REF2 ri-normalizzata = [34,27;34,35] x ORA_REF/4,875 come in E4). Aritmetica meccanica.
import glob, os, re, statistics, sys
ICTX_MAX = 200.0
REPO = "/Volumes/Extreme Pro/Claude/php-rust-experiment/php-rust"
files = sorted(glob.glob(f"{REPO}/wp1[6-8]*-harness/*orm*verdetto*.out") +
               glob.glob(f"{REPO}/wp1[6-8]*-harness/orm-out/*verdetto*.out"))
rows = []; excl = []
for f in files:
    b = os.path.basename(f)
    m = re.match(r"s(\d+)-orm", b)
    if not m or int(m.group(1)) < 162: excl.append((b, "fuori S-162..S-184")); continue
    if "contaminata" in b or "oracle-r5" in b: excl.append((b, "dichiarato contaminato / oracle-only")); continue
    if b == "s176-orm-coppia-verdetto.out": excl.append((b, "file VIVO di s176, sovrascritto = duplicato del t26")); continue
    txt = open(f, errors="replace").read()
    if not re.search(r"^parita'.*rc=0", txt, re.M): excl.append((b, "parita' rc!=0 o verdetto tronco")); continue
    legs = re.findall(r"^orm_leg(\d): oracle_user=([\d.]+)", txt, re.M)
    if len(legs) < 2: excl.append((b, "gambe ORM mancanti (tronco)")); continue
    fm = re.search(r"floor_user_med3 orm: oracle=([\d.]+)", txt) or re.search(r"floor_user_med3 oracle=([\d.]+)", txt)
    floor = float(fm.group(1)) if fm else 0.06
    fl = re.search(r"^orm_ictx/s.*SEGNALATE\(>1,5x med\): \[([^\]]*)\]", txt, re.M)
    flagged = set(re.findall(r"'(oracle\d)'", fl.group(1))) if fl else set()
    rates = dict(re.findall(r"(oracle\d)=([\d.]+)", (re.search(r"^orm_ictx/s.*$", txt, re.M) or re.match(r"", "")).group(0)))
    for leg, user in legs:
        k = f"oracle{leg}"
        if k in flagged: excl.append((f"{b}:{k}", "ictx segnalata")); continue
        # TETTO ASSOLUTO (rev. S-184 bis #5): 200 ictx/s per gamba — gambe storiche non segnalate max 148/s, contaminate min 214/s
        if float(rates.get(k, -1)) > ICTX_MAX: excl.append((f"{b}:{k}", f"ictx {rates[k]}/s > tetto {ICTX_MAX}")); continue
        rows.append((b, k, float(user) - floor))
vals = sorted(v for _, _, v in rows)
med = statistics.median(vals); lo, hi = vals[0], vals[-1]
ref2 = (round(34.27 * med / 4.875, 2), round(34.35 * med / 4.875, 2))
out = [f"== E5 banda sentinella oracle ORM — {len(vals)} gambe pulite da {len(set(b for b,_,_ in rows))} verdetti S-162..S-184 ==",
       f"ORA_REF={med:.3f} (mediana) SENT_LO={lo:.2f} (min pulito, lato veloce = SEGNALAZIONE) SENT_HI={hi:.2f} (max pulito, lato lento = BLOCCO)",
       f"REF2 ri-normalizzata = [34,27;34,35] x {med:.3f}/4,875 = [{ref2[0]}; {ref2[1]}]",
       f"canone E4 corrente: ORA_REF=4.94 banda [4.84;5.04] — gambe pulite sotto 4.84: {sum(1 for v in vals if v < 4.84)}, sopra 5.04: {sum(1 for v in vals if v > 5.04)}",
       "gambe (net): " + " ".join(f"{b.replace('-orm-coppia-verdetto','').replace('.out','')}/{k}={v:.2f}" for b, k, v in rows),
       "escluse: " + " · ".join(f"{b} ({why})" for b, why in excl)]
print("\n".join(out))
