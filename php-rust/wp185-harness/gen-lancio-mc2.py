#!/usr/bin/env python3
# gen-lancio-mc2.py — genera s185-lancio-mc2.sh come COPIA DICHIARATA di wp184-harness/s184-lancio-rt2.sh (lanciatore dell'A/B
# della leva (a), criterio s185-criterio-mc2.md p.6). Ogni sostituzione e' asserita UNICA; manifest s185-lancio-mc2-copia.diff.
# Adattamenti: harness wp185, tag mc2, token s185, bracci ab-out/s185-leva, pin s182 159eee40, PREV prop-dq 31,60, s185-ab-mc2.sh.
import os, subprocess
H = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(H, "..", "wp184-harness", "s184-lancio-rt2.sh"); DST = os.path.join(H, "s185-lancio-mc2.sh")
s = open(SRC).read()
def sub(old, new):
    global s
    assert s.count(old) == 1, f"NON unico ({s.count(old)}): {old[:70]!r}"
    s = s.replace(old, new)
sub("#!/bin/bash\n# s184-lancio-rt2.sh — LEVA COMPOSTA L-RT1+L-RT2 (criterio s184-criterio-rt2.md p.6):",
    "#!/bin/bash\n# s185-lancio-mc2.sh — LEVA (a) L-MR1+L-MC2 (criterio s185-criterio-mc2.md p.6): COPIA DICHIARATA di ../wp184-harness/s184-lancio-rt2.sh\n"
    "# (manifest s185-lancio-mc2-copia.diff, generatore gen-lancio-mc2.py) coi SOLI adattamenti: harness wp185, tag mc2, token s185, bracci\n"
    "# ab-out/s185-leva, pin s182 159eee40, PREV prop-dq 31,60, s185-ab-mc2.sh. Gate INVARIATI. Testo S-184 sotto:\n"
    "# s184-lancio-rt2.sh — LEVA COMPOSTA L-RT1+L-RT2 (criterio s184-criterio-rt2.md p.6):")
sub('H="$SRC/wp184-harness"; O="$H/ab-out"; mkdir -p "$O"', 'H="$SRC/wp185-harness"; O="$H/ab-out"; mkdir -p "$O"')
sub('LOG="$O/lancio-rt2.log"; LRC="$O/lancio-rt2.rc"; LDONE="$O/lancio-rt2.done"; WDL="$O/watchdog-rt2.log"; ALARM="$O/watchdog-rt2.alarm"\nDECL="$O/finestra-rt2.txt"',
    'LOG="$O/lancio-mc2.log"; LRC="$O/lancio-mc2.rc"; LDONE="$O/lancio-mc2.done"; WDL="$O/watchdog-mc2.log"; ALARM="$O/watchdog-mc2.alarm"\nDECL="$O/finestra-mc2.txt"')
sub('PIN8=19a2faa8\nAB="$O/s184-leva"', 'PIN8=159eee40\nAB="$O/s185-leva"')
sub('BD="$O/s184-leva.done"', 'BD="$O/s185-leva.done"')
sub('grep -qw s184 /private/tmp/phpr-measure.lock 2>/dev/null || fine 9 "lock senza token s184"', 'grep -qw s185 /private/tmp/phpr-measure.lock 2>/dev/null || fine 9 "lock senza token s185"')
sub('"$O/quiesce-rt2.rc" > "$O/quiesce-rt2-$i.log"', '"$O/quiesce-mc2.rc" > "$O/quiesce-mc2-$i.log"')
sub('if [ "$(cat "$O/quiesce-rt2.rc" 2>/dev/null)" = 0 ]', 'if [ "$(cat "$O/quiesce-mc2.rc" 2>/dev/null)" = 0 ]')
sub('l "quiescenza tentativo $i FAIL: $(tail -1 "$O/quiesce-rt2-$i.log")"', 'l "quiescenza tentativo $i FAIL: $(tail -1 "$O/quiesce-mc2-$i.log")"')
sub('{ echo "== finestra A/B COMPOSTA L-RT1+L-RT2: quiescenza PASS', '{ echo "== finestra A/B leva (a) L-MR1+L-MC2: quiescenza PASS')
sub('l "finestra aperta (quiescenza t$Q, Data ${D0}G, B=$B8) — s184-ab-rt2.sh rt2 R=5"\n/bin/bash "$H/s184-ab-rt2.sh" "$O/arm-A" "$PIN8" "$O/arm-Z" "$Z8" "$O/arm-B" "$B8" rt2 5 31.27',
    'l "finestra aperta (quiescenza t$Q, Data ${D0}G, B=$B8) — s185-ab-mc2.sh mc2 R=5"\n/bin/bash "$H/s185-ab-mc2.sh" "$O/arm-A" "$PIN8" "$O/arm-Z" "$Z8" "$O/arm-B" "$B8" mc2 5 31.60')
sub('cat "$DECL" >> "$H/s184-rt2-verdetto.out" 2>/dev/null\nl "s184-ab-rt2.sh rc=$R1"', 'cat "$DECL" >> "$H/s185-mc2-verdetto.out" 2>/dev/null\nl "s185-ab-mc2.sh rc=$R1"')
open(DST, "w").write(s); os.chmod(DST, 0o755)
with open(os.path.join(H, "s185-lancio-mc2-copia.diff"), "w") as mf:
    subprocess.run(["diff", SRC, DST], stdout=mf)
print("generato", DST)
