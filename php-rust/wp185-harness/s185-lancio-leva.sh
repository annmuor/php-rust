#!/bin/bash
# s185-lancio-leva.sh — S-185: COORDINATORE della leva (a) L-MR1+L-MC2 (criterio s185-criterio-mc2.md p.6-7): gate di finestra
# EREDITATI -> lock TOKEN s185 -> prerequisito catena ORM FINITA -> build bracci Z/B/M (s185-leva-build.sh, COMMIT=$1, ZCOMMIT
# 454a77c3 = sorgente del pin s182) -> A/B (s185-lancio-mc2.sh, gate propri) SOLO se l'istruttoria ORM non ha dato E1 (rc=10
# «A/B rinviato», bracci agli atti) -> lock rimosso; esiti SOLO in ab-out/lancio-leva.done. COPIA DICHIARATA di
# wp184-harness/s184-lancio-orm-t26.sh (manifest s185-lancio-leva-copia.diff, generatore gen-lancio-leva.py) coi SOLI adattamenti:
# harness wp185/ab-out, TOKEN s185, watchdog disco su lancio-leva.done, blocco finale (fine() a 3 argomenti). NESSUNA igiene FS qui.
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
COMMIT="${1:?COMMIT della leva (hash)}"
LOG="$H/ab-out/lancio-leva.log"; mkdir -p "$H/ab-out"
echo "$(date '+%F %T') attesa quiete CI" >> "$LOG"
while pgrep -qx cargo || pgrep -qx rustc || pgrep -qf phpt-runner; do sleep 60; done
sleep 60
if pgrep -qx cargo || pgrep -qx rustc || pgrep -qf phpt-runner; then
  while pgrep -qx cargo || pgrep -qx rustc || pgrep -qf phpt-runner; do sleep 60; done
  sleep 60
fi
# EMENDA t24 (i): LOCK col TOKEN s183 — apre la finestra multi-gamba (la CI si mette in mutex sul lock); rimosso a chiusura di sessione
MLOCK=/private/tmp/phpr-measure.lock
echo "s185 leva (a) bracci + A/B @ pin s182 $(date '+%F %T') pid=$$" > "$MLOCK"
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
( WD="$H/ab-out/watchdog-leva.txt"; PD="$H/ab-out/lancio-leva.done"; t0=$(date +%s); tdone=0
  while :; do
    f=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}'); a=""; [ "${f:-0}" -lt 8 ] && a=" ALLARME<8G"
    echo "$(date '+%F %T') Data=${f}G swap=$(sysctl -n vm.swapusage | awk '{print $6}')$a" >> "$WD"
    now=$(date +%s); [ -e "$PD" ] && [ "$tdone" = 0 ] && tdone=$now
    { [ "$tdone" != 0 ] && [ $((now-tdone)) -ge 600 ]; } && break
    [ $((now-t0)) -ge 10800 ] && break
    sleep 60
  done ) > /dev/null 2>&1 &
# dichiarazione finestra QUIETA (criterio p.6c): uptime + top
Q="$H/ab-out/quiet-decl-leva.txt"
{ echo "== dichiarazione finestra quieta leva (a) build + A/B $(date '+%F %T') =="
  uptime
  top -l 1 -n 8 -o cpu -stats pid,cpu,command 2>/dev/null | tail -12
} > "$Q" 2>&1
echo "$(date '+%F %T') quiete raggiunta — dichiarazione in quiet-decl-leva.txt — build bracci Z/B/M, poi A/B" >> "$LOG"
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
