#!/bin/bash
# s185-orm-istruttoria.sh — S-185: ISTRUTTORIA ORM A TRE BRACCI (oracle / phpr s181 / phpr s182) R=3 interleaved,
# criterio s185-criterio-istruttoria-orm.md. COPIA DICHIARATA di wp176-harness/s176-orm-coppia.sh (manifest
# s185-orm-istruttoria-copia.diff, generatore gen-orm-istruttoria.py) coi SOLI adattamenti: harness wp185/istr-out, terzo
# motore PHPR181 (stash phpr-s181, hash atteso PIN181_ATTESO), watchdog = wp184-harness/run-with-watchdog-s184bis.sh
# (copia con hash dell'emendato S-184 bis), ORM-only (dbal RIMOSSO), rodaggio x3, R=3 round O-A-B con quiescenza per
# round, parita' per NOME su entrambi i bracci phpr, GIUDICE NUOVO (round VOID a >200 ictx/s, esiti E1-E4, sentinella
# E4/E5 companion, istr-out/e5.flag se mediana oracle <4,84). rc SOLO da istr-out/rimisura.done. Testo S-176 sotto.
# EMENDA S-184 bis (2026-10-08, dichiarata): giudice con guardia sui .time incompleti (exit 7 => RC=7, VERDETTO NON EMESSO); vedi blocco python.
# s176-orm-coppia.sh — coppia dbal+ORM col CANONE EMENDATO (S-176, istruttoria s176-istruttoria-sentinella-orm.md +
# criterio s176-criterio-orm.md): COPIA DICHIARATA di s175-orm-coppia.sh (manifest s176-orm-coppia-copia.diff) coi SOLI
# adattamenti: (E3) quiesce_gate = assestamento a STREAK di mediaanalysisd PRIMA di ogni tentativo del gate (blocco di
# s175-pair.sh, retry x3) al posto della pausa fissa 30 s; (E4) ORA_REF=4,94 (mediana 18 gambe pulite S-162..S-175; rilievo 6 rev. S-176),
# banda sentinella [4,84;5,04] = ORA_REF ±2 %, REF2 ri-normalizzata [34,73;34,81] = [34,27;34,35]×4,94/4,875 (4,875 =
# media oracle della finestra di riferimento s166-mattina 4,87/4,88); harness wp176, verdetto s176-orm-coppia-verdetto.out,
# PIN atteso passato via env PIN_ATTESO (default s175). Tutto il resto INVARIATO; testo S-175 conservato sotto per storia.
# s175-orm-coppia.sh — coppia dbal+ORM sul pin s175 (DOVUTA: pin nuovo, promozione Sweep-in-op C S-175).
# COPIA DICHIARATA di wp172-harness/s173-orm-coppia.sh (manifest s175-orm-coppia-copia.diff); adattamenti: harness
# wp174, pin s175 = 5de14d6856d760a8, nota t19 (rapporto net [6,988;7,012] RIENTRATO <7,05: regola 4 non scattata;
# se t20 torna >7,05 la voce si riapre), attesa Sweep-in-op (direzione ≤0, magnitudine NON pre-registrabile);
# RIF, E1, E2 (banda sentinella [4,83;4,94]: 4,94 = estremo osservato t19 — fuori banda ⇒ Delta_norm NON giudicante,
# voce riaperta) INVARIATI. Testo S-173 conservato sotto per storia.
# s173-orm-coppia.sh — coppia dbal+ORM sul pin s173 (DOVUTA: pin nuovo)
# (criterio s173-criterio-orm.md; copia DICHIARATA di s172-orm-coppia.sh,
# manifest s173-orm-coppia-copia.diff; adattamenti: pin s173 = placeholder
# da4921a52eba0187 (inserito DOPO la promozione; era 5f2dff7d17ebed79), nota t18
# sul rapporto registrato, attesa fetta 3; RIF AGGIORNATO (sanatura az.rev.4; era «INVARIATO», contraddiceva r.~188): ORA_REF=4,885 (REGGE per
# R=5 oracle-only S-165, mediana 4,860), rapporto registrato S-162
# [7,035;7,086]; DUE EMENDE dal verbale S-165 (entrambe PRE-registrate):
# (E1) segnalazione ictx PER MOTORE (istruttoria ictx CHIUSA: firma =
# denominatore su bracci 6-7x diversi); (E2) banda sentinella oracle
# [4,83;4,94] VINCOLANTE (gamba fuori => Delta_norm NON giudicante);
# attesa fetta 3 (P3 peephole + P4 borrow unico) su ORM: direzione <=0,
# magnitudine NON pre-registrabile; attesa-AF1 resta APERTA.
# NOTA t18 (S-172): rapporto net t18 [7,090;7,092] da rivedere; se in S-173 resta >7,05 scatta la regola 4.
# SENTINELLA CONTAMINAZIONE (lezione S-161): oracle net fuori dal SUO rif
# storico => cifra NULLA anche a flag per-gamba muti; parita' resta valida.
# TRE adattamenti NEL CANONE ereditati: rodaggio non giudicante, quiescenza
# per gamba (retry x3), scaletta a DUE estremi. rc SOLO da orm-out/rimisura.done.
set -u
export PATH=/usr/bin:/bin:/usr/sbin:/opt/homebrew/bin
REPO="/Volumes/Extreme Pro/Claude/php-rust-experiment/php-rust"
H="$REPO/wp185-harness"
GATES="/Volumes/Extreme Pro/Claude/wp9-harness/gates"
WD="$REPO/wp184-harness/run-with-watchdog-s184bis.sh"
ORACLE=/opt/homebrew/opt/php/bin/php
PHPR="$HOME/Claude/php-rust-output/release/phpr"
PHPR181="/Volumes/Extreme Pro/Claude/phpr-old-target/release/phpr-s181"
SP="${MAPPA_SP:?MAPPA_SP (workdir APFS) richiesto}"
OUT="$H/istr-out"; mkdir -p "$OUT"
VERD="$H/s185-orm-istruttoria-verdetto.out"
p(){ echo "$(date +%H:%M:%S) $1" >> "$OUT/progress.txt"; }
: > "$OUT/progress.txt"
rm -f "$OUT/rimisura.done"
PINM="$(shasum -a 256 "$PHPR" | cut -c1-16)"
PIN_ATTESO="${PIN_ATTESO:-159eee40be506171}"
[ "$PINM" = "$PIN_ATTESO" ] || { echo "rc=9 pin!=$PIN_ATTESO" > "$OUT/rimisura.done"; exit 9; }
PIN181M="$(shasum -a 256 "$PHPR181" | cut -c1-16)"
PIN181_ATTESO="${PIN181_ATTESO:-19a2faa83a492745}"
[ "$PIN181M" = "$PIN181_ATTESO" ] || { echo "rc=9 pin181!=$PIN181_ATTESO" > "$OUT/rimisura.done"; exit 9; }
# lock della SESSIONE: si VERIFICA soltanto (niente creazione né trap).
LOCK=/private/tmp/phpr-measure.lock
[ -e "$LOCK" ] || { echo "rc=6 measure-lock ASSENTE (finestra non aperta)" > "$OUT/rimisura.done"; exit 6; }

# sentinella language-server (az.rev. S-157 #4): registrata nel verdetto,
# inizio e fine finestra; presenza != esclusione (misure a user-CPU), si dichiara.
ls_sentinel(){ pgrep -fl 'language[_-]server|Antigravity|rust-analyzer|intelephense|serena|gopls|pylsp|solargraph' 2>/dev/null | grep -v pgrep | awk '{print $2}' | sort -u | tr '\n' ' '; }
LS_START="$(ls_sentinel)"
p "sentinella LS inizio: ${LS_START:-nessuno}"

# ADATTAMENTO (ii) DICHIARATO (istruttoria p.1): quiescenza per gamba giudicata,
# stesso gate del pair (s129-quiescenza.sh), retry x3 con pausa 30 s.
QUIESCE="$REPO/wp129-harness/s129-quiescenza.sh"
# EMENDA E3 (S-176, lezione 3 S-175: budget 3x30 s battuto da flare di 2-3 min): assestamento a STREAK di
# mediaanalysisd (4 campioni consecutivi <5% a passo 5 s, tetto ~15 min) PRIMA di ogni tentativo del gate — blocco
# COPIATO da s175-pair.sh (emende S-136 t3/t4); il gate resta AUTORITATIVO e invariato.
quiesce_gate(){ local attempt q
  for attempt in 1 2 3; do
    local w=0 streak=0 c
    while :; do
      c=$(ps -Ao %cpu,comm | awk 'index($0,"mediaanalysisd"){s+=$1} END{printf "%.1f", s+0}')
      if awk -v a="$c" 'BEGIN{exit !(a<5.0)}'; then
        streak=$((streak+1))
        [ "$streak" -ge 4 ] && break
      else
        [ "$streak" -gt 0 ] && p "assestamento $1 (att.$attempt): streak rotta a $streak da $c%"
        streak=0
        w=$((w+1)); p "assestamento $1 (att.$attempt): mediaanalysisd $c% (attesa ~$((w*15))s)"
        [ "$w" -gt 90 ] && break
        /bin/sleep 10
      fi
      /bin/sleep 5
    done
    "$QUIESCE" "$OUT/quiesce-$1.rc" > "$OUT/quiesce-$1.log" 2>&1; q=$?
    p "quiescenza $1 rc=$q tentativo-gate=$attempt (file: orm-out/quiesce-$1.rc)"
    [ "$q" = 0 ] && return 0
  done
  echo "rc=8 quiescenza-fail su $1 (3 tentativi)" > "$OUT/rimisura.done"; exit 8
}

# FIX az.rev. S-155 #4 (adattamento DICHIARATO): l'output dbal phpr contiene
# byte non-UTF-8 (latin1 a catalogo) — tr/sed/grep BSD in locale UTF-8 muoiono
# a metà stream e la summary/failnames escono tronche. LC_ALL=C + grep -a.
names(){ LC_ALL=C tr -d '\0' < "$1" | LC_ALL=C sed -n 's/^[0-9][0-9]*) \(.*\)$/\1/p' | LC_ALL=C sort -u; }
summ(){ LC_ALL=C tr -d '\0' < "$1" | LC_ALL=C grep -aE "^(Tests:|OK)" | tail -1; }

# pavimenti per-binario (med3 di `phpunit --version`) PER WORKSPACE — MISURATI
# su QUESTO pin (az.rev.4: mai ereditati).
rm -rf "$SP/orm-work"; tar xzf "$GATES/orm-work.tgz" -C "$SP" || { echo "rc=8 untar" > "$OUT/rimisura.done"; exit 8; }
floor3(){ local E="$1" P="$2" f1 f2 f3
  f1=$( { /usr/bin/time -l "$E" "$P" --version > /dev/null; } 2>&1 | awk '/[0-9.]+ *user/{for(i=1;i<=NF;i++) if($i=="user"){print $(i-1)}}' )
  f2=$( { /usr/bin/time -l "$E" "$P" --version > /dev/null; } 2>&1 | awk '/[0-9.]+ *user/{for(i=1;i<=NF;i++) if($i=="user"){print $(i-1)}}' )
  f3=$( { /usr/bin/time -l "$E" "$P" --version > /dev/null; } 2>&1 | awk '/[0-9.]+ *user/{for(i=1;i<=NF;i++) if($i=="user"){print $(i-1)}}' )
  printf '%s\n%s\n%s\n' "$f1" "$f2" "$f3" | sort -n | awk 'NR==2'
}
FO=$(floor3 "$ORACLE" "$SP/orm-work/vendor/bin/phpunit"); FP=$(floor3 "$PHPR" "$SP/orm-work/vendor/bin/phpunit")
F181=$(floor3 "$PHPR181" "$SP/orm-work/vendor/bin/phpunit")
echo "floor_user_med3 orm: oracle=$FO phpr_s182=$FP phpr_s181=$F181 (phpunit --version, pavimento PARZIALE dichiarato)" > "$OUT/floors.txt"
p "floors: orm o=$FO s182=$FP s181=$F181"

run_leg(){ # W TGZ DIR TIMEOUT ENGINE LABEL
  local W="$1" TGZ="$2" DIR="$3" T="$4" E="$5" L="$6"
  rm -rf "$SP/$DIR"; tar xzf "$GATES/$TGZ" -C "$SP" || return 7
  p "$W $L START"
  # EMENDA ereditata (s147 p.7): oracle con memory_limit=-1 (§3.14, parità
  # di condizioni).
  local ML=""
  [ "$E" = "$ORACLE" ] && ML="-d memory_limit=-1"
  ( cd "$SP/$DIR" && "$WD" -t "$T" -s 600 -p "$OUT/$W-$L.txt" -o "$OUT" -- \
      /usr/bin/time -l "$E" $ML vendor/bin/phpunit --no-coverage > "$OUT/$W-$L.txt" 2> "$OUT/$W-$L.time" )
  local rc=$?
  p "$W $L rc=$rc"
  return 0
}

WLS="orm"

# ADATTAMENTO (i) DICHIARATO (istruttoria p.1): RODAGGIO non giudicante — una
# gamba per motore e workload, scarica il transitorio primo-run (leg1 598/s ->
# leg2-3 ~120/s in isolamento, daemon scagionati). FUORI da ogni statistica;
# ictx/s a verbale come companion.
case " $WLS " in *" orm "*)
  run_leg orm orm-work.tgz orm-work 3600 "$ORACLE"  "rodaggio-oracle"
  run_leg orm orm-work.tgz orm-work 3600 "$PHPR181" "rodaggio-s181"
  run_leg orm orm-work.tgz orm-work 3600 "$PHPR"    "rodaggio-phpr" ;;
esac

# TRE BRACCI interleaved O-A-B, R=3 round (criterio p.1)
for leg in 1 2 3; do
  case " $WLS " in *" orm "*)
    quiesce_gate "orm-leg$leg"
    run_leg orm orm-work.tgz orm-work 3600 "$ORACLE"  "oracle$leg"
    run_leg orm orm-work.tgz orm-work 3600 "$PHPR181" "s181$leg"
    run_leg orm orm-work.tgz orm-work 3600 "$PHPR"    "phpr$leg" ;;
  esac
done

# parità: ORM per NOME vs baseline 16 su ENTRAMBI i bracci phpr (s181, s182), ogni round
RC=0
for leg in 1 2 3; do
  for arm in phpr s181; do
    names "$OUT/orm-$arm$leg.txt" > "$OUT/orm-$arm$leg.failnames"
    if ! diff -q "$REPO/wp125-harness/orm-baseline-failnames.txt" "$OUT/orm-$arm$leg.failnames" > /dev/null; then
      p "orm $arm$leg: fail-set DIVERGE — cifra NULLA"; RC=1
    fi
  done
done

python3 - "$OUT" "$FO" "$FP" "$F181" "$RC" > "$OUT/ratios.txt" <<'PY'
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
JRC=$?
[ "$JRC" = 0 ] || { RC=$JRC; p "giudice rc=$JRC — $([ "$JRC" = 8 ] && echo NON GIUDICABILE || echo "VERDETTO NON EMESSO (.time incompleto)")"; }

rod_ictx(){ # companion istruttoria: ictx/s delle gambe di rodaggio (FUORI dal gate)
  local f="$OUT/$1.time" r i
  [ -f "$f" ] || { echo "n/d"; return; }
  r=$(tr -d '\0' < "$f" | awk '/[0-9.]+ *real/{for(j=1;j<=NF;j++) if($j=="real"){print $(j-1)}}')
  i=$(tr -d '\0' < "$f" | awk '/involuntary/{print $1}')
  python3 -c "print(f'{$i/$r:.1f}')" 2>/dev/null || echo "n/d"
}

{ echo "== s185 ISTRUTTORIA ORM 3 bracci (oracle 8.5.7 / phpr s181 $PIN181M / phpr s182 $PINM; criterio s185-criterio-istruttoria-orm.md) =="
  echo "# estrazione summ/names con LC_ALL=C + grep -a (fix az.rev. S-155 #4); reperto conteggi dbal phpr vs oracle A VERBALE (companion, non arbitra)"
  echo "# ADATTAMENTI (i)-(iii) dall'istruttoria p.1 + az.rev. S-159 #1: rodaggio non giudicante, quiescenza per gamba, scaletta a due estremi"
  echo "sentinella language-server inizio finestra (az.rev. S-157 #4): ${LS_START:-nessuno}"
  LS_END="$(ls_sentinel)"
  echo "sentinella language-server fine finestra: ${LS_END:-nessuno}"
  echo "rodaggio (NON giudicato, companion istruttoria) ictx/s: orm_oracle=$(rod_ictx orm-rodaggio-oracle) orm_s181=$(rod_ictx orm-rodaggio-s181) orm_s182=$(rod_ictx orm-rodaggio-phpr)"
  for g in orm-leg1 orm-leg2 orm-leg3; do
    echo "quiescenza $g: rc=$(cat "$OUT/quiesce-$g.rc" 2>/dev/null || echo MANCANTE) (file: istr-out/quiesce-$g.rc)"
  done
  cat "$OUT/floors.txt"
  cat "$OUT/ratios.txt"
  [ -f "$OUT/e5.flag" ] && echo "e5.flag: $(cat "$OUT/e5.flag")"
  echo "parita': orm per NOME vs baseline 16 su s181 e s182, 3 round — rc=$RC (0=tutte valide)"
  for leg in 1 2 3; do
    echo "orm oracle$leg: $(summ "$OUT/orm-oracle$leg.txt")"
    echo "orm s181-$leg:  $(summ "$OUT/orm-s181$leg.txt")"
    echo "orm s182-$leg:  $(summ "$OUT/orm-phpr$leg.txt")"
  done
} > "$VERD"
echo "rc=$RC $(date +%T)" > "$OUT/rimisura.done"
p "DONE rc=$RC"
