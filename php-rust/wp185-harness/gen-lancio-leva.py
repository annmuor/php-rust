#!/usr/bin/env python3
# gen-lancio-leva.py — genera s185-lancio-leva.sh come COPIA DICHIARATA di wp184-harness/s184-lancio-orm-t26.sh (coordinatore
# della leva (a) L-MR1+L-MC2, criterio s185-criterio-mc2.md p.6-7): gate di finestra EREDITATI (quiete CI -> lock TOKEN s185 ->
# anti-flare -> loadavg -> E2 -> processo singolo -> dichiarazione) poi, al posto dell'ORM t26: prerequisito catena ORM FINITA
# (catena-out/catena-s185.done), build dei bracci Z/B/M (s185-leva-build.sh, COMMIT da argv $1, ZCOMMIT 454a77c3 = ultimo commit
# su crates = sorgente del pin s182), A/B (s185-lancio-mc2.sh) SOLO se l'istruttoria ORM non ha dato E1 (altrimenti rc=10
# «A/B rinviato», bracci agli atti), lock rimosso, esiti in ab-out/lancio-leva.done. Ogni sostituzione e' asserita UNICA;
# manifest s185-lancio-leva-copia.diff.
import os, subprocess
H = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(H, "..", "wp184-harness", "s184-lancio-orm-t26.sh"); DST = os.path.join(H, "s185-lancio-leva.sh")
s = open(SRC).read()
def sub(old, new):
    global s
    assert s.count(old) == 1, f"NON unico ({s.count(old)}): {old[:70]!r}"
    s = s.replace(old, new)
sub("#!/bin/bash\n# s184-lancio-orm-t26.sh — S-184 bis",
    "#!/bin/bash\n# s185-lancio-leva.sh — S-185: COORDINATORE della leva (a) L-MR1+L-MC2 (criterio s185-criterio-mc2.md p.6-7): gate di finestra\n"
    "# EREDITATI -> lock TOKEN s185 -> prerequisito catena ORM FINITA -> build bracci Z/B/M (s185-leva-build.sh, COMMIT=$1, ZCOMMIT\n"
    "# 454a77c3 = sorgente del pin s182) -> A/B (s185-lancio-mc2.sh, gate propri) SOLO se l'istruttoria ORM non ha dato E1 (rc=10\n"
    "# «A/B rinviato», bracci agli atti) -> lock rimosso; esiti SOLO in ab-out/lancio-leva.done. COPIA DICHIARATA di\n"
    "# wp184-harness/s184-lancio-orm-t26.sh (manifest s185-lancio-leva-copia.diff, generatore gen-lancio-leva.py) coi SOLI adattamenti:\n"
    "# harness wp185/ab-out, TOKEN s185, watchdog disco su lancio-leva.done, blocco finale (fine() a 3 argomenti). NESSUNA igiene FS qui.\n"
    "# s184-lancio-orm-t26.sh — S-184 bis")
sub('H="/Volumes/Extreme Pro/Claude/php-rust-experiment/php-rust/wp184-harness"', 'H="/Volumes/Extreme Pro/Claude/php-rust-experiment/php-rust/wp185-harness"\nCOMMIT="${1:?COMMIT della leva (hash)}"')
sub('LOG="$H/orm-out/lancio-t26.log"; mkdir -p "$H/orm-out"', 'LOG="$H/ab-out/lancio-leva.log"; mkdir -p "$H/ab-out"')
sub('echo "s184bis ORM t26 @ pin s182 $(date \'+%F %T\') pid=$$" > "$MLOCK"\necho "$(date \'+%F %T\') lock scritto: $MLOCK (TOKEN s184bis)" >> "$LOG"',
    'echo "s185 leva (a) bracci + A/B @ pin s182 $(date \'+%F %T\') pid=$$" > "$MLOCK"\necho "$(date \'+%F %T\') lock scritto: $MLOCK (TOKEN s185)" >> "$LOG"')
sub('( WD="$H/orm-out/watchdog-t26.txt"; PD="$H/orm-out/rimisura-t26.done"; t0=$(date +%s); tdone=0',
    '( WD="$H/ab-out/watchdog-leva.txt"; PD="$H/ab-out/lancio-leva.done"; t0=$(date +%s); tdone=0')
sub('Q="$H/orm-out/quiet-decl-t26.txt"\n{ echo "== dichiarazione finestra quieta t26 ORM $(date \'+%F %T\') =="',
    'Q="$H/ab-out/quiet-decl-leva.txt"\n{ echo "== dichiarazione finestra quieta leva (a) build + A/B $(date \'+%F %T\') =="')
i = s.index('echo "$(date \'+%F %T\') quiete raggiunta — dichiarazione in quiet-decl-t26.txt')
assert s.count('quiete raggiunta — dichiarazione in quiet-decl-t26.txt') == 1
s = s[:i] + '''echo "$(date '+%F %T') quiete raggiunta — dichiarazione in quiet-decl-leva.txt — build bracci Z/B/M, poi A/B" >> "$LOG"
DONE="$H/ab-out/lancio-leva.done"; rm -f "$DONE"
fine(){ echo "$(date '+%F %T') $1" >> "$LOG"; echo "$2" > "$DONE"; rm -f "$MLOCK"; exit "$3"; }
[ -e "$H/catena-out/catena-s185.done" ] || fine "catena ORM NON finita (catena-s185.done assente)" "rc=9 catena-orm" 9
IV="$H/s185-orm-istruttoria-verdetto.out"; E1=0; grep -q "^ESITO: E1" "$IV" 2>/dev/null && E1=1
echo "$(date '+%F %T') istruttoria ORM: $(grep '^ESITO:' "$IV" 2>/dev/null | cut -c1-80) (E1=$E1) — build bracci (COMMIT=$COMMIT ZCOMMIT=454a77c3)" >> "$LOG"
COMMIT="$COMMIT" ZCOMMIT=454a77c3 /bin/bash "$H/s185-leva-build.sh"
rcb=$?
BD="$(cat "$H/ab-out/s185-leva.done" 2>/dev/null)"
echo "$(date '+%F %T') bracci fine rc=$rcb ($BD) — verdetto s185-leva-build-verdetto.out" >> "$LOG"
grep -q '^rc=0' "$H/ab-out/s185-leva.done" 2>/dev/null || fine "bracci rc≠0: niente A/B" "rc=$rcb build=[$BD] ab=NON-ESEGUITO" "$rcb"
[ "$E1" = 0 ] || fine "istruttoria ORM E1 (s182 più lento): A/B della leva RINVIATO (criterio-mc2 p.7), bracci agli atti" "rc=10 build=[$BD] ab=RINVIATO-E1" 10
/bin/bash "$H/s185-lancio-mc2.sh"
rca=$?
LD="$(cat "$H/ab-out/lancio-mc2.done" 2>/dev/null)"; AR="$(cat "$H/ab-out/mc2.rc" 2>/dev/null)"
fine "A/B fine rc=$rca (lancio=[$LD] criterio rc=${AR:-n/d}) — verdetto s185-mc2-verdetto.out; lock rimosso" "rc=${AR:-$rca} build=[$BD] lancio=[$LD] criterio=${AR:-n/d}" "${AR:-$rca}"
'''
open(DST, "w").write(s); os.chmod(DST, 0o755)
with open(os.path.join(H, "s185-lancio-leva-copia.diff"), "w") as mf:
    subprocess.run(["diff", SRC, DST], stdout=mf)
print("generato", DST)
