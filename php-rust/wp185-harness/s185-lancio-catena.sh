#!/bin/bash
# s185-lancio-catena.sh — S-185: CATENA NOTTURNA UNICA (criterio s185-criterio-istruttoria-orm.md p.6): gate di finestra
# EREDITATI (quiete CI, anti-flare 6x30 s, loadavg1 <3 x6, E2 <150 % x4, processo singolo >50 % x2, dichiarazione uptime+top)
# -> lock TOKEN s185 -> pin s182 E stash s181 per hash -> ISTRUTTORIA ORM 3 bracci (s185-orm-istruttoria.sh) -> se istr-out/e5.flag
# costanti E5 in env -> t27 dbal+ORM (s185-orm-coppia-t27.sh) -> lock rimosso; esiti SOLO in catena-out/catena-s185.done.
# COPIA DICHIARATA di wp184-harness/s184-lancio-orm-t26.sh (manifest s185-lancio-catena-copia.diff, generatore
# gen-lancio-catena.py) coi SOLI adattamenti: harness wp185/catena-out, TOKEN s185, watchdog disco su catena-s185.done, blocco
# finale (istruttoria + t27 al posto di archivio t25-raw + ORM t26; fine() a 3 argomenti). NESSUNA igiene FS qui.
# s184-lancio-orm-t26.sh — S-184 bis: t26 ORM-ONLY (dbal+ORM, s176-orm-coppia.sh emendato) @ pin s182, finestra PROPRIA dopo
# l'ORM t25 rc=8 NON GIUDICABILE (sentinella oracle fuori banda + ictx oracle1). COPIA DICHIARATA di s184-lancio-pair-t25.sh
# (manifest s184-lancio-orm-t26-copia.diff) coi SOLI adattamenti: log/esiti in orm-out (*-t26.*), lock TOKEN s184bis RIMOSSO
# dal lanciatore a ORM finito (finestra = il solo ORM), watchdog disco riferito a rimisura-t26.done (10 min dopo, max 3 h),
# e al posto del pair: archivio dei raw t25 di wp176-harness/orm-out in orm-out/t25-raw (verifica ls), pin == stash s182,
# s176-orm-coppia.sh con PIN_ATTESO/MAPPA_SP, copia verdetto+done in orm-out. Gate di finestra INVARIATI (quiete CI,
# anti-flare 6x30 s, loadavg1 <3 x6, E2 <150 % x4, processo singolo >50 % x2, dichiarazione uptime+top). NESSUNA igiene FS qui.
# s184-lancio-pair-t25.sh — COPPIA t25 @ pin s182 (criterio s184-criterio-coppia-t25.md p.3): COPIA DICHIARATA di
# ../wp182-harness/s182-lancio-pair-t24.sh (manifest s184-lancio-pair-copia.diff) coi SOLI adattamenti: nomi s184/t25/pair184,
# lock TOKEN s184, s184-pair.sh t25, PIÙ il gate sentinella «processo singolo >50 % CPU» ×2 (az.rev. S-183 #3, come
# s184-lancio-rt2.sh) dopo E2. Il resto INVARIATO (testo S-182 conservato sotto).
set -u
export PATH=/usr/bin:/bin:/usr/sbin:/opt/homebrew/bin
H="/Volumes/Extreme Pro/Claude/php-rust-experiment/php-rust/wp185-harness"
LOG="$H/catena-out/lancio-catena.log"; mkdir -p "$H/catena-out"
echo "$(date '+%F %T') attesa quiete CI" >> "$LOG"
while pgrep -qx cargo || pgrep -qx rustc || pgrep -qf phpt-runner; do sleep 60; done
sleep 60
if pgrep -qx cargo || pgrep -qx rustc || pgrep -qf phpt-runner; then
  while pgrep -qx cargo || pgrep -qx rustc || pgrep -qf phpt-runner; do sleep 60; done
  sleep 60
fi
# EMENDA t24 (i): LOCK col TOKEN s183 — apre la finestra multi-gamba (la CI si mette in mutex sul lock); rimosso a chiusura di sessione
MLOCK=/private/tmp/phpr-measure.lock
echo "s185 catena istruttoria+t27 @ pin s182 $(date '+%F %T') pid=$$" > "$MLOCK"
echo "$(date '+%F %T') lock scritto: $MLOCK (TOKEN s185)" >> "$LOG"
# predicato anti-flare PRE-registrato (criterio p.6b): quiete CONTINUA 6x30s
echo "$(date '+%F %T') CI quieta — attesa quiete continua anti-flare (6x30s <5%)" >> "$LOG"
calm=0
while [ "$calm" -lt 6 ]; do
  c=$(top -l 2 -stats pid,cpu,command 2>/dev/null | awk '/mediaanalysisd/ {v=$2} END {print (v==""?0:v)}')
  if awk -v c="$c" 'BEGIN{exit !(c<5.0)}'; then calm=$((calm+1)); else calm=0; fi
  echo "$(date '+%F %T') mediaanalysisd=$c calm=$calm" >> "$LOG"
  [ "$calm" -lt 6 ] && sleep 30
done
# EMENDA t23 EREDITATA + EMENDA t24 (ii): PRE-gate di carico PRIMA del pair — loadavg1 <3 (era <5) per 6 campioni consecutivi a 30 s
# (finestra NOTTURNA = conseguenza del gate, non un orario; il gate s129 per gamba resta INVARIATO)
lc=0
while [ "$lc" -lt 6 ]; do
  L1=$(sysctl -n vm.loadavg | awk '{print $2}')
  if awk -v l="$L1" 'BEGIN{exit !(l+0 < 3.0)}'; then lc=$((lc+1)); else lc=0; fi
  echo "$(date '+%F %T') loadavg1=$L1 lc=$lc" >> "$LOG"
  [ "$lc" -lt 6 ] && sleep 30
done
# EMENDA t24 (iii): E2 calma CPU TOTALE <150 % per 4 campioni a 30 s (predicato COPIATO da s181-promozione.sh:169-176; qui ripetuto finché passa)
cpu_tot(){ ps -Ao %cpu= | awk '{s+=$1} END{printf "%.0f", s}'; }
t=0
while :; do
  t=$((t+1)); ok=1; smp=""
  for k in 1 2 3 4; do c=$(cpu_tot); smp="$smp $c"; [ "$c" -lt 150 ] || ok=0; sleep 30; done
  if [ "$ok" = 1 ]; then echo "$(date '+%F %T') E2 calma CPU: PASS al tentativo $t (campioni:$smp %)" >> "$LOG"; break; fi
  echo "$(date '+%F %T') E2 calma CPU: tentativo $t FALLITO (campioni:$smp %)" >> "$LOG"
done
# GATE sentinella (az.rev. S-183 #3): nessun processo singolo > 50 % CPU al SECONDO campione di `top -l 2`, ×2 consecutivi
hog(){ /usr/bin/top -l 2 -n 1 -o cpu -stats cpu,command 2>/dev/null | tail -1 | awk '$1+0 > 50 {print}'; }
hc=0
while [ "$hc" -lt 2 ]; do hg=$(hog); if [ -z "$hg" ]; then hc=$((hc+1)); else hc=0; echo "$(date '+%F %T') processo singolo >50 % CPU: $hg — attesa" >> "$LOG"; fi; [ "$hc" -lt 2 ] && sleep 30; done
# EMENDA t24 (iv): watchdog disco Data (campione a 60 s in pair-out/watchdog-t24.txt; allarme <8G a verbale, NON abortisce: le misure sono a user-CPU);
# vive finché pair182-t24.done esiste da 4 h (copre l'ORM) o 14 h totali
( WD="$H/catena-out/watchdog-catena.txt"; PD="$H/catena-out/catena-s185.done"; t0=$(date +%s); tdone=0
  while :; do
    f=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}'); a=""; [ "${f:-0}" -lt 8 ] && a=" ALLARME<8G"
    echo "$(date '+%F %T') Data=${f}G swap=$(sysctl -n vm.swapusage | awk '{print $6}')$a" >> "$WD"
    now=$(date +%s); [ -e "$PD" ] && [ "$tdone" = 0 ] && tdone=$now
    { [ "$tdone" != 0 ] && [ $((now-tdone)) -ge 600 ]; } && break
    [ $((now-t0)) -ge 10800 ] && break
    sleep 60
  done ) > /dev/null 2>&1 &
# dichiarazione finestra QUIETA (criterio p.6c): uptime + top
Q="$H/catena-out/quiet-decl-catena.txt"
{ echo "== dichiarazione finestra quieta catena S-185 (istruttoria + t27) $(date '+%F %T') =="
  uptime
  top -l 1 -n 8 -o cpu -stats pid,cpu,command 2>/dev/null | tail -12
} > "$Q" 2>&1
echo "$(date '+%F %T') quiete raggiunta — dichiarazione in quiet-decl-catena.txt — istruttoria 3 bracci, poi t27" >> "$LOG"
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
