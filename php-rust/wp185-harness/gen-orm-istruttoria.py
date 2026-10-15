#!/usr/bin/env python3
# gen-orm-istruttoria.py — genera s185-orm-istruttoria.sh come COPIA DICHIARATA di wp176-harness/s176-orm-coppia.sh
# (istruttoria ORM a TRE BRACCI, criterio s185-criterio-istruttoria-orm.md). Ogni sostituzione e' asserita UNICA;
# manifest s185-orm-istruttoria-copia.diff. Adattamenti: harness wp185/istr-out, terzo motore phpr s181 (stash, hash
# atteso), watchdog = copia con hash wp184-harness, ORM-only (dbal rimosso), rodaggio x3, R=3 round O-A-B, parita' su
# entrambi i bracci phpr, giudice NUOVO (tre bracci, round VOID a >200 ictx/s, esiti E1-E4 pre-registrati, sentinella
# E4/E5 companion + e5.flag), verdetto s185-orm-istruttoria-verdetto.out. Tutto il resto INVARIATO.
import os, re, subprocess
H = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(H, "..", "wp176-harness", "s176-orm-coppia.sh"); DST = os.path.join(H, "s185-orm-istruttoria.sh")
s = open(SRC).read()
def sub(old, new):
    global s
    assert s.count(old) == 1, f"NON unico ({s.count(old)}): {old[:70]!r}"
    s = s.replace(old, new)
sub("#!/bin/bash\n# EMENDA S-184 bis",
    "#!/bin/bash\n# s185-orm-istruttoria.sh — S-185: ISTRUTTORIA ORM A TRE BRACCI (oracle / phpr s181 / phpr s182) R=3 interleaved,\n"
    "# criterio s185-criterio-istruttoria-orm.md. COPIA DICHIARATA di wp176-harness/s176-orm-coppia.sh (manifest\n"
    "# s185-orm-istruttoria-copia.diff, generatore gen-orm-istruttoria.py) coi SOLI adattamenti: harness wp185/istr-out, terzo\n"
    "# motore PHPR181 (stash phpr-s181, hash atteso PIN181_ATTESO), watchdog = wp184-harness/run-with-watchdog-s184bis.sh\n"
    "# (copia con hash dell'emendato S-184 bis), ORM-only (dbal RIMOSSO), rodaggio x3, R=3 round O-A-B con quiescenza per\n"
    "# round, parita' per NOME su entrambi i bracci phpr, GIUDICE NUOVO (round VOID a >200 ictx/s, esiti E1-E4, sentinella\n"
    "# E4/E5 companion, istr-out/e5.flag se mediana oracle <4,84). rc SOLO da istr-out/rimisura.done. Testo S-176 sotto.\n"
    "# EMENDA S-184 bis")
sub('H="$REPO/wp176-harness"', 'H="$REPO/wp185-harness"')
sub('WD="/Volumes/Extreme Pro/Claude/wp13-harness/run-with-watchdog.sh"', 'WD="$REPO/wp184-harness/run-with-watchdog-s184bis.sh"')
sub('PHPR="$HOME/Claude/php-rust-output/release/phpr"\n',
    'PHPR="$HOME/Claude/php-rust-output/release/phpr"\nPHPR181="/Volumes/Extreme Pro/Claude/phpr-old-target/release/phpr-s181"\n')
sub('OUT="$H/orm-out"; mkdir -p "$OUT"\nVERD="$H/s176-orm-coppia-verdetto.out"',
    'OUT="$H/istr-out"; mkdir -p "$OUT"\nVERD="$H/s185-orm-istruttoria-verdetto.out"')
sub('PIN_ATTESO="${PIN_ATTESO:-5de14d6856d760a8}"\n[ "$PINM" = "$PIN_ATTESO" ] || { echo "rc=9 pin!=$PIN_ATTESO" > "$OUT/rimisura.done"; exit 9; }',
    'PIN_ATTESO="${PIN_ATTESO:-159eee40be506171}"\n[ "$PINM" = "$PIN_ATTESO" ] || { echo "rc=9 pin!=$PIN_ATTESO" > "$OUT/rimisura.done"; exit 9; }\n'
    'PIN181M="$(shasum -a 256 "$PHPR181" | cut -c1-16)"\nPIN181_ATTESO="${PIN181_ATTESO:-19a2faa83a492745}"\n'
    '[ "$PIN181M" = "$PIN181_ATTESO" ] || { echo "rc=9 pin181!=$PIN181_ATTESO" > "$OUT/rimisura.done"; exit 9; }')
sub('rm -rf "$SP/dbal-work"; tar xzf "$GATES/dbal-work.tgz" -C "$SP" || { echo "rc=8 untar-dbal" > "$OUT/rimisura.done"; exit 8; }\n', '')
sub('FO=$(floor3 "$ORACLE" "$SP/orm-work/vendor/bin/phpunit"); FP=$(floor3 "$PHPR" "$SP/orm-work/vendor/bin/phpunit")\n'
    'DFO=$(floor3 "$ORACLE" "$SP/dbal-work/vendor/bin/phpunit"); DFP=$(floor3 "$PHPR" "$SP/dbal-work/vendor/bin/phpunit")\n'
    'echo "floor_user_med3 orm: oracle=$FO phpr=$FP · dbal: oracle=$DFO phpr=$DFP (phpunit --version, pavimento PARZIALE dichiarato)" > "$OUT/floors.txt"\n'
    'p "floors: orm o=$FO p=$FP · dbal o=$DFO p=$DFP"',
    'FO=$(floor3 "$ORACLE" "$SP/orm-work/vendor/bin/phpunit"); FP=$(floor3 "$PHPR" "$SP/orm-work/vendor/bin/phpunit")\n'
    'F181=$(floor3 "$PHPR181" "$SP/orm-work/vendor/bin/phpunit")\n'
    'echo "floor_user_med3 orm: oracle=$FO phpr_s182=$FP phpr_s181=$F181 (phpunit --version, pavimento PARZIALE dichiarato)" > "$OUT/floors.txt"\n'
    'p "floors: orm o=$FO s182=$FP s181=$F181"')
sub('WLS="${WORKLOADS:-orm dbal}"', 'WLS="orm"')
sub('  run_leg orm orm-work.tgz orm-work 3600 "$ORACLE" "rodaggio-oracle"\n  run_leg orm orm-work.tgz orm-work 3600 "$PHPR"   "rodaggio-phpr" ;;\nesac\n'
    'case " $WLS " in *" dbal "*)\n  run_leg dbal dbal-work.tgz dbal-work 3600 "$ORACLE" "rodaggio-oracle"\n  run_leg dbal dbal-work.tgz dbal-work 3600 "$PHPR"   "rodaggio-phpr" ;;\nesac\n',
    '  run_leg orm orm-work.tgz orm-work 3600 "$ORACLE"  "rodaggio-oracle"\n  run_leg orm orm-work.tgz orm-work 3600 "$PHPR181" "rodaggio-s181"\n'
    '  run_leg orm orm-work.tgz orm-work 3600 "$PHPR"    "rodaggio-phpr" ;;\nesac\n')
sub('for leg in 1 2; do\n  case " $WLS " in *" orm "*)\n    quiesce_gate "orm-leg$leg"\n'
    '    run_leg orm orm-work.tgz orm-work 3600 "$ORACLE" "oracle$leg"\n    run_leg orm orm-work.tgz orm-work 3600 "$PHPR"   "phpr$leg" ;;\n  esac\n'
    '  case " $WLS " in *" dbal "*)\n    quiesce_gate "dbal-leg$leg"\n'
    '    run_leg dbal dbal-work.tgz dbal-work 3600 "$ORACLE" "oracle$leg"\n    run_leg dbal dbal-work.tgz dbal-work 3600 "$PHPR"   "phpr$leg" ;;\n  esac\ndone\n',
    '# TRE BRACCI interleaved O-A-B, R=3 round (criterio p.1)\nfor leg in 1 2 3; do\n  case " $WLS " in *" orm "*)\n    quiesce_gate "orm-leg$leg"\n'
    '    run_leg orm orm-work.tgz orm-work 3600 "$ORACLE"  "oracle$leg"\n    run_leg orm orm-work.tgz orm-work 3600 "$PHPR181" "s181$leg"\n'
    '    run_leg orm orm-work.tgz orm-work 3600 "$PHPR"    "phpr$leg" ;;\n  esac\ndone\n')
sub('# parità: ORM phpr per NOME vs baseline 16; dbal fail-set phpr STABILE tra gambe\nRC=0\nfor leg in 1 2; do\n'
    '  names "$OUT/orm-phpr$leg.txt" > "$OUT/orm-phpr$leg.failnames"\n'
    '  if ! diff -q "$REPO/wp125-harness/orm-baseline-failnames.txt" "$OUT/orm-phpr$leg.failnames" > /dev/null; then\n'
    '    p "orm phpr$leg: fail-set DIVERGE — cifra NULLA"; RC=1\n  fi\n'
    '  names "$OUT/dbal-phpr$leg.txt"   > "$OUT/dbal-phpr$leg.failnames"\n  names "$OUT/dbal-oracle$leg.txt" > "$OUT/dbal-oracle$leg.failnames"\ndone\n'
    'if ! diff -q "$OUT/dbal-phpr1.failnames" "$OUT/dbal-phpr2.failnames" > /dev/null; then\n'
    '  p "dbal: fail-set phpr NON stabile tra gambe — cifra NULLA"; RC=1\nfi\n',
    '# parità: ORM per NOME vs baseline 16 su ENTRAMBI i bracci phpr (s181, s182), ogni round\nRC=0\nfor leg in 1 2 3; do\n'
    '  for arm in phpr s181; do\n    names "$OUT/orm-$arm$leg.txt" > "$OUT/orm-$arm$leg.failnames"\n'
    '    if ! diff -q "$REPO/wp125-harness/orm-baseline-failnames.txt" "$OUT/orm-$arm$leg.failnames" > /dev/null; then\n'
    '      p "orm $arm$leg: fail-set DIVERGE — cifra NULLA"; RC=1\n    fi\n  done\ndone\n')
# GIUDICE: blocco python sostituito per intero (adattamento dichiarato)
m = re.search(r'python3 - "\$OUT" "\$FO" "\$FP" "\$DFO" "\$DFP" "\$RC" > "\$OUT/ratios\.txt" <<\'PY\'\n.*?\nPY\n', s, re.S)
assert m and s.count(m.group(0)) == 1
JUDGE = r'''python3 - "$OUT" "$FO" "$FP" "$F181" "$RC" > "$OUT/ratios.txt" <<'PY'
import re, sys, statistics, os
out = sys.argv[1]
fo, fp, f181 = map(float, sys.argv[2:5])
parita_rc = int(sys.argv[5])
def t(f):
    d = {}
    for l in open(f, errors="replace"):
        m = re.search(r'([\d.]+)\s+real', l)
        if m: d['real'] = float(m.group(1))
        m = re.search(r'([\d.]+)\s+user', l)
        if m: d['user'] = float(m.group(1))
        m = re.search(r'([\d.]+)\s+sys', l)
        if m: d['sys'] = float(m.group(1))
        m = re.search(r'^\s*(\d+)\s+involuntary context switches', l)
        if m: d['ictx'] = int(m.group(1))
    return d
# COSTANTI PRE-REGISTRATE (criterio s185-criterio-istruttoria-orm.md p.2-5)
ICTX_MAX = 200.0                      # tetto ASSOLUTO ictx/s per gamba (rev. S-184 bis #5)
RES = 0.293                           # risoluzione KS-146-1 (s)
ORA_REF_E4, SENT_E4 = 4.94, (4.84, 5.04)   # canone E4 (S-176)
ORA_REF_E5, SENT_E5 = 4.870, (4.81, 4.93)  # E5 (s185-banda-e5.out: 18 gambe pulite S-162..S-184)
SOGLIA_BASE = round(RES / ORA_REF_E5, 3)   # 0,06 sul rapporto
print("istruttoria ORM 3 bracci (user CPU; pavimenti PARZIALI phpunit --version: oracle=%.3f s182=%.3f s181=%.3f)" % (fo, fp, f181))
print("grade=VERDICT  # derivazione meccanica dai .time, criterio p.2-5")
A = []; B = []; O = []; valid = []
for leg in (1, 2, 3):
    o = t(f"{out}/orm-oracle{leg}.time"); a = t(f"{out}/orm-s181{leg}.time"); b = t(f"{out}/orm-phpr{leg}.time")
    incompleti = [f"orm-{k}{leg}.time" for k, d in (("oracle", o), ("s181", a), ("phpr", b)) if 'user' not in d or 'real' not in d]
    if incompleti:
        print(f"VERDETTO NON EMESSO: {incompleti} senza riga user/real (gamba incompleta o uccisa dal watchdog) — rc=7")
        sys.exit(7)
    rate = {k: (d['ictx']/d['real'] if ('ictx' in d and d['real'] > 0) else -1) for k, d in (("oracle", o), ("s181", a), ("phpr", b))}
    on = o['user'] - fo; an = a['user'] - f181; bn = b['user'] - fp
    ra, rb = an/on, bn/on
    void = [k for k, v in rate.items() if v > ICTX_MAX]
    print(f"orm_round{leg}: oracle_net={on:.2f} s181_net={an:.2f} s182_net={bn:.2f} a={ra:.3f} b={rb:.3f} ictx/s oracle={rate['oracle']:.1f} s181={rate['s181']:.1f} s182={rate['phpr']:.1f}" + (f"  ROUND VOID (>{ICTX_MAX:.0f}/s: {void})" if void else ""))
    if not void:
        A.append(ra); B.append(rb); O.append(on); valid.append(leg)
print(f"round validi: {valid} ({len(valid)}/3)")
if len(valid) < 2:
    print("ISTRUTTORIA NON GIUDICABILE: meno di 2 round validi (tetto ictx) — rc=8")
    sys.exit(8)
am, bm, om = statistics.median(A), statistics.median(B), statistics.median(O)
spread = max(max(A)-min(A), max(B)-min(B))
soglia = max(SOGLIA_BASE, spread)
D = bm - am
print(f"mediane: a(s181)={am:.3f} b(s182)={bm:.3f} oracle_net={om:.2f} · spread intra-braccio={spread:.3f} · soglia={soglia:.3f}" + ("  (SPREAD > 0,06: soglia dallo spread, dichiarato)" if spread > SOGLIA_BASE else ""))
print(f"D = b - a = {D:+.3f}")
if parita_rc != 0:
    esito = "CIFRA NULLA (parita' rotta su un braccio phpr) — nessun giudizio"
elif D > soglia:
    esito = "E1: s182 PIU' LENTO su ORM della leva composta (D > soglia) => REGOLA 4 sul pin s182 (quota Ret NON ammessi + costo bl ret_slow sui metodi) PRIMA della leva (a)"
elif D < -soglia:
    esito = "E4: s182 PIU' VELOCE su ORM (D < -soglia) — direzione firmata, magnitudine NON ripartita"
elif am > 7.05 and bm > 7.05:
    esito = "E2: rallentamento COMUNE ai due phpr (|D| <= soglia, entrambi >7,05) — macchina/oracle, NON la leva"
elif am <= 7.05 and bm <= 7.05:
    esito = "E3: t25/t26 = artefatti di contesa (|D| <= soglia, entrambi <=7,05); riferimento ORM @ s182 = t27"
else:
    esito = "NR: bracci a cavallo di 7,05 con |D| <= soglia — si dichiara"
print("ESITO: " + esito)
# sentinella oracle: companion, NON blocca; e5.flag per il t27
def banda(v, lo, hi): return "in banda" if lo <= v <= hi else ("SOTTO (lato veloce)" if v < lo else "SOPRA (lato lento)")
print(f"sentinella oracle (mediana net {om:.2f}): canone E4 [{SENT_E4[0]};{SENT_E4[1]}] => {banda(om, *SENT_E4)} · E5 [{SENT_E5[0]};{SENT_E5[1]}] => {banda(om, *SENT_E5)} · gambe {[round(x,2) for x in O]}")
flag = f"{out}/e5.flag"
if om < SENT_E4[0]:
    open(flag, "w").write(f"E5 oracle_med={om:.2f} < {SENT_E4[0]}\n")
    print(f"DRIFT CONFERMATO (mediana oracle < {SENT_E4[0]}): t27 corre con le costanti E5 (istr-out/e5.flag scritto)")
else:
    if os.path.exists(flag): os.remove(flag)
    print("drift NON confermato: t27 corre col canone E4")
PY
'''
s = s.replace(m.group(0), JUDGE)
sub('''  r=$(tr -d '\\0' < "$f" | awk '/[0-9.]+ *real/''', '''  r=$(tr -d '\\0' < "$f" | awk '/[0-9.]+ *real/''')  # invariato (ancora di contesto)
sub('{ echo "== s175 coppia dbal+ORM (pin s175 MISURATO $PINM vs oracle 8.5.7; criterio s175-criterio-orm.md) =="',
    '{ echo "== s185 ISTRUTTORIA ORM 3 bracci (oracle 8.5.7 / phpr s181 $PIN181M / phpr s182 $PINM; criterio s185-criterio-istruttoria-orm.md) =="')
sub('  echo "rodaggio (NON giudicato, companion istruttoria) ictx/s: orm_oracle=$(rod_ictx orm-rodaggio-oracle) orm_phpr=$(rod_ictx orm-rodaggio-phpr) dbal_oracle=$(rod_ictx dbal-rodaggio-oracle) dbal_phpr=$(rod_ictx dbal-rodaggio-phpr)"\n'
    '  for g in orm-leg1 dbal-leg1 orm-leg2 dbal-leg2; do',
    '  echo "rodaggio (NON giudicato, companion istruttoria) ictx/s: orm_oracle=$(rod_ictx orm-rodaggio-oracle) orm_s181=$(rod_ictx orm-rodaggio-s181) orm_s182=$(rod_ictx orm-rodaggio-phpr)"\n'
    '  for g in orm-leg1 orm-leg2 orm-leg3; do')
sub('''    echo "quiescenza $g: rc=$(cat "$OUT/quiesce-$g.rc" 2>/dev/null || echo MANCANTE) (file: orm-out/quiesce-$g.rc)"''',
    '''    echo "quiescenza $g: rc=$(cat "$OUT/quiesce-$g.rc" 2>/dev/null || echo MANCANTE) (file: istr-out/quiesce-$g.rc)"''')
sub('''  echo "parita': orm phpr per NOME vs baseline 16 · dbal fail-set stabile tra gambe — rc=$RC (0=tutte valide)"\n  for leg in 1 2; do\n'''
    '''    echo "orm  oracle$leg: $(summ "$OUT/orm-oracle$leg.txt")"\n    echo "orm  phpr$leg:   $(summ "$OUT/orm-phpr$leg.txt")"\n'''
    '''    echo "dbal oracle$leg: $(summ "$OUT/dbal-oracle$leg.txt")"\n    echo "dbal phpr$leg:   $(summ "$OUT/dbal-phpr$leg.txt")"\n  done\n''',
    '''  echo "parita': orm per NOME vs baseline 16 su s181 e s182, 3 round — rc=$RC (0=tutte valide)"\n  for leg in 1 2 3; do\n'''
    '''    echo "orm oracle$leg: $(summ "$OUT/orm-oracle$leg.txt")"\n    echo "orm s181-$leg:  $(summ "$OUT/orm-s181$leg.txt")"\n'''
    '''    echo "orm s182-$leg:  $(summ "$OUT/orm-phpr$leg.txt")"\n  done\n''')
sub('''    echo "quiescenza $g: rc=$(cat "$OUT/quiesce-$g.rc" 2>/dev/null || echo MANCANTE) (file: istr-out/quiesce-$g.rc)"\n  done\n  cat "$OUT/floors.txt"\n  cat "$OUT/ratios.txt"''',
    '''    echo "quiescenza $g: rc=$(cat "$OUT/quiesce-$g.rc" 2>/dev/null || echo MANCANTE) (file: istr-out/quiesce-$g.rc)"\n  done\n  cat "$OUT/floors.txt"\n  cat "$OUT/ratios.txt"\n  [ -f "$OUT/e5.flag" ] && echo "e5.flag: $(cat "$OUT/e5.flag")"''')
# rc finale: 8 se il giudice ha dichiarato NON GIUDICABILE (round validi <2)
sub('JRC=$?\n[ "$JRC" = 0 ] || { RC=7; p "giudice rc=$JRC — VERDETTO NON EMESSO (.time incompleto)"; }',
    'JRC=$?\n[ "$JRC" = 0 ] || { RC=$JRC; p "giudice rc=$JRC — $([ "$JRC" = 8 ] && echo NON GIUDICABILE || echo "VERDETTO NON EMESSO (.time incompleto)")"; }')
open(DST, "w").write(s); os.chmod(DST, 0o755)
with open(os.path.join(H, "s185-orm-istruttoria-copia.diff"), "w") as mf:
    subprocess.run(["diff", SRC, DST], stdout=mf)
print("generato", DST)
