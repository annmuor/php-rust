#!/usr/bin/env python3
# gen-lancio-catena.py — genera s185-lancio-catena.sh come COPIA DICHIARATA di wp184-harness/s184-lancio-orm-t26.sh
# (catena notturna UNICA S-185: gate di finestra EREDITATI -> lock TOKEN s185 -> istruttoria ORM 3 bracci -> t27 dbal+ORM
# -> lock rimosso; criterio s185-criterio-istruttoria-orm.md p.6). Ogni sostituzione e' asserita UNICA; manifest
# s185-lancio-catena-copia.diff. Adattamenti: harness wp185/catena-out, TOKEN s185, watchdog disco su catena-s185.done,
# al posto dell'archivio t25-raw + ORM t26: verifica pin s182 E stash s181 per hash, istruttoria, e5.flag -> costanti E5
# in env per t27, t27, .done con entrambi gli rc (fine() a 3 argomenti: messaggio, contenuto .done, exit code).
import os, subprocess
H = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(H, "..", "wp184-harness", "s184-lancio-orm-t26.sh"); DST = os.path.join(H, "s185-lancio-catena.sh")
s = open(SRC).read()
def sub(old, new):
    global s
    assert s.count(old) == 1, f"NON unico ({s.count(old)}): {old[:70]!r}"
    s = s.replace(old, new)
sub("#!/bin/bash\n# s184-lancio-orm-t26.sh — S-184 bis",
    "#!/bin/bash\n# s185-lancio-catena.sh — S-185: CATENA NOTTURNA UNICA (criterio s185-criterio-istruttoria-orm.md p.6): gate di finestra\n"
    "# EREDITATI (quiete CI, anti-flare 6x30 s, loadavg1 <3 x6, E2 <150 % x4, processo singolo >50 % x2, dichiarazione uptime+top)\n"
    "# -> lock TOKEN s185 -> pin s182 E stash s181 per hash -> ISTRUTTORIA ORM 3 bracci (s185-orm-istruttoria.sh) -> se istr-out/e5.flag\n"
    "# costanti E5 in env -> t27 dbal+ORM (s185-orm-coppia-t27.sh) -> lock rimosso; esiti SOLO in catena-out/catena-s185.done.\n"
    "# COPIA DICHIARATA di wp184-harness/s184-lancio-orm-t26.sh (manifest s185-lancio-catena-copia.diff, generatore\n"
    "# gen-lancio-catena.py) coi SOLI adattamenti: harness wp185/catena-out, TOKEN s185, watchdog disco su catena-s185.done, blocco\n"
    "# finale (istruttoria + t27 al posto di archivio t25-raw + ORM t26; fine() a 3 argomenti). NESSUNA igiene FS qui.\n"
    "# s184-lancio-orm-t26.sh — S-184 bis")
sub('H="/Volumes/Extreme Pro/Claude/php-rust-experiment/php-rust/wp184-harness"', 'H="/Volumes/Extreme Pro/Claude/php-rust-experiment/php-rust/wp185-harness"')
sub('LOG="$H/orm-out/lancio-t26.log"; mkdir -p "$H/orm-out"', 'LOG="$H/catena-out/lancio-catena.log"; mkdir -p "$H/catena-out"')
sub('echo "s184bis ORM t26 @ pin s182 $(date \'+%F %T\') pid=$$" > "$MLOCK"\necho "$(date \'+%F %T\') lock scritto: $MLOCK (TOKEN s184bis)" >> "$LOG"',
    'echo "s185 catena istruttoria+t27 @ pin s182 $(date \'+%F %T\') pid=$$" > "$MLOCK"\necho "$(date \'+%F %T\') lock scritto: $MLOCK (TOKEN s185)" >> "$LOG"')
sub('( WD="$H/orm-out/watchdog-t26.txt"; PD="$H/orm-out/rimisura-t26.done"; t0=$(date +%s); tdone=0',
    '( WD="$H/catena-out/watchdog-catena.txt"; PD="$H/catena-out/catena-s185.done"; t0=$(date +%s); tdone=0')
sub('Q="$H/orm-out/quiet-decl-t26.txt"\n{ echo "== dichiarazione finestra quieta t26 ORM $(date \'+%F %T\') =="',
    'Q="$H/catena-out/quiet-decl-catena.txt"\n{ echo "== dichiarazione finestra quieta catena S-185 (istruttoria + t27) $(date \'+%F %T\') =="')
i = s.index('echo "$(date \'+%F %T\') quiete raggiunta — dichiarazione in quiet-decl-t26.txt')
assert s.count('quiete raggiunta — dichiarazione in quiet-decl-t26.txt') == 1
s = s[:i] + '''echo "$(date '+%F %T') quiete raggiunta — dichiarazione in quiet-decl-catena.txt — istruttoria 3 bracci, poi t27" >> "$LOG"
REPO="/Volumes/Extreme Pro/Claude/php-rust-experiment/php-rust"; STASH="/Volumes/Extreme Pro/Claude/phpr-old-target/release"
DONE="$H/catena-out/catena-s185.done"; rm -f "$DONE"
fine(){ echo "$(date '+%F %T') $1" >> "$LOG"; echo "$2" > "$DONE"; rm -f "$MLOCK"; exit "$3"; }
PIN_ATTESO=$(shasum -a 256 "$STASH/phpr-s182" | cut -c1-16); PC=$(shasum -a 256 "$HOME/Claude/php-rust-output/release/phpr" | cut -c1-16)
[ "$PC" = "$PIN_ATTESO" ] || fine "pin canonico $PC != stash s182 $PIN_ATTESO" "rc=9 pin" 9
PIN181_ATTESO=$(shasum -a 256 "$STASH/phpr-s181" | cut -c1-16)
[ "$PIN181_ATTESO" = "19a2faa83a492745" ] || fine "stash s181 $PIN181_ATTESO != 19a2faa83a492745" "rc=9 pin181" 9
SPD=/private/tmp/phpr-s185-orm; mkdir -p "$SPD"
echo "$(date '+%F %T') pin $PC == stash s182 · stash s181 $PIN181_ATTESO — ISTRUTTORIA 3 bracci (MAPPA_SP=$SPD)" >> "$LOG"
PIN_ATTESO="$PIN_ATTESO" PIN181_ATTESO="$PIN181_ATTESO" MAPPA_SP="$SPD" /bin/bash "$H/s185-orm-istruttoria.sh"
rc1=$?
IR="$(cat "$H/istr-out/rimisura.done" 2>/dev/null)"
echo "$(date '+%F %T') istruttoria fine rc=$rc1 ($IR) — verdetto s185-orm-istruttoria-verdetto.out" >> "$LOG"
# t27: costanti E5 SOLO se l'istruttoria ha scritto istr-out/e5.flag (criterio p.5); altrimenti canone E4
E5=0
if [ -f "$H/istr-out/e5.flag" ]; then E5=1; export ORA_REF2=4.870 SENT_LO=4.81 SENT_HI=4.93 REF2_MIN=34.23 REF2_MAX=34.31; fi
export E5
echo "$(date '+%F %T') t27 dbal+ORM con E5=$E5 ($(cat "$H/istr-out/e5.flag" 2>/dev/null || echo "canone E4"))" >> "$LOG"
PIN_ATTESO="$PIN_ATTESO" MAPPA_SP="$SPD" /bin/bash "$H/s185-orm-coppia-t27.sh"
rc2=$?
TR="$(cat "$H/orm-out/rimisura.done" 2>/dev/null)"
fine "t27 fine rc=$rc2 ($TR) — verdetto s185-orm-coppia-verdetto-t27.out; lock rimosso" "rc=$rc2 istruttoria=[$IR] t27=[$TR] E5=$E5" "$rc2"
'''
open(DST, "w").write(s); os.chmod(DST, 0o755)
with open(os.path.join(H, "s185-lancio-catena-copia.diff"), "w") as mf:
    subprocess.run(["diff", SRC, DST], stdout=mf)
print("generato", DST)
