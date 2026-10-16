#!/usr/bin/env python3
# gen-promozione-s185.py — genera s185-promozione.sh e s185-lancio-promo.sh come COPIE DICHIARATE di
# ../wp184-harness/s184-promozione.sh e s184-lancio-promo.sh (ogni sostituzione con assert di unicità;
# manifest = diff dei due script). Eseguito una volta in S-185 diurna (16/10) dopo: A/B mc2 rc=0 (notte),
# azione B della revisione chiusa con prova per nome (criterio-mc2 p.8), CI verde su 84980b05.
# Generato con assistenza AI (Claude Fable 5).
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/..')

def rep(s, old, new, n=1):
    assert s.count(old) == n, (old[:70], s.count(old))
    return s.replace(old, new)

s = open('wp184-harness/s184-promozione.sh', encoding='utf-8').read()
head_old = s[:s.index('set -u\n')]
head_new = '''#!/bin/bash
# s185-promozione.sh — gate di PROMOZIONE COMPOSTA del tree «pin s182 + L-MR1 + L-MC2» (criterio s185-criterio-mc2.md p.5).
# COPIA DICHIARATA di ../wp184-harness/s184-promozione.sh (manifest s185-promozione-copia.diff, generatore
# gen-promozione-s185.py) coi SOLI adattamenti: (1) tag s183 (harness wp185: verdetto s185-promo-verdetto.out, promo-out);
# (2) CANDIDATO = braccio B dell'A/B mc2 (ab-out/s185-leva/phpr-B 7466bf61, commit 4176ea3a): precondizione A/B rc=0
# (ab-out/mc2.rc) e commit in HEAD; (3) REF = stash phpr-s182 (159eee40be506171) per i gate invarianti; (4) gate bilaterale
# NUOVO fx-mc2 di wp185 (FX-MC2 DONE, nome fxmc2s185: il nome fxmc2 è già del gate invariante §3.28 di wp172) accanto a
# fx-rt1/fx-rt2; (5) corpus: ZERO flip attesi (semantica identica per costruzione, prova per nome criterio-mc2 p.8, batteria
# CI 1748/0 su 4176ea3a..84980b05); (6) conferma post-pin = mcalls-dq R=5 pin s183 vs stash s182 (stessa toolchain 1.98.1:
# attesa D ≈ [+19,00;+19,17] dell'A/B) + calls-dq e prop-dq (guardie, attesa |D| < 1); (7) pin-server.sh s183.
# Testo S-184/S-181/S-180/S-177 conservato sotto:
'''
s = head_new + s[len(head_old):]
s = rep(s, 'H9="$SRC/wp184-harness"; H3="$SRC/wp182-harness"', 'H9="$SRC/wp184-harness"; H3="$SRC/wp182-harness"\nH10="$SRC/wp185-harness"')
s = rep(s, 'OUT="$H9/promo-out"; mkdir -p "$OUT"', 'OUT="$H10/promo-out"; mkdir -p "$OUT"')
s = rep(s, 'VERD="$H9/s184-promo-verdetto.out"', 'VERD="$H10/s185-promo-verdetto.out"')
s = rep(s, 'REF="$STASH/phpr-s181"; REF_EXP="19a2faa83a492745"', 'REF="$STASH/phpr-s182"; REF_EXP="159eee40be506171"')
s = rep(s, 'CAND="$H9/ab-out/s184-leva/phpr-B"; CAND_COMMIT="${CAND_COMMIT:-454a77c3}"', 'CAND="$H10/ab-out/s185-leva/phpr-B"; CAND_COMMIT="${CAND_COMMIT:-4176ea3a}"')
s = rep(s, '"$H3/fx-rt1.php" "$H9/fx-rt2.php" "$CAND" "$H9/ab-out/rt2.rc" \\',
        '"$H3/fx-rt1.php" "$H9/fx-rt2.php" "$H10/fx-mc2.php" "$H10/mcalls-dq.php" "$CAND" "$H10/ab-out/mc2.rc" \\')
s = rep(s, '|| stop "PRE: stash phpr-s181 hash != $REF_EXP — STOP"', '|| stop "PRE: stash phpr-s182 hash != $REF_EXP — STOP"')
s = rep(s, '[ "$(cat "$H9/ab-out/rt2.rc")" = 0 ] || stop "PRE: A/B rt2 rc=$(cat "$H9/ab-out/rt2.rc") ≠ 0 — nessuna promozione senza nomina — STOP"',
        '[ "$(cat "$H10/ab-out/mc2.rc")" = 0 ] || stop "PRE: A/B mc2 rc=$(cat "$H10/ab-out/mc2.rc") ≠ 0 — nessuna promozione senza nomina — STOP"')
s = rep(s, 'note "PRE: candidato = braccio B $CH (commit $CAND_COMMIT, A/B rt2 rc=0, cifra composta [+12,50;+13,17]); REF = stash s181 $REF_EXP"',
        'note "PRE: candidato = braccio B $CH (commit $CAND_COMMIT, A/B mc2 rc=0, cifra composta [+19,00;+19,17]); REF = stash s182 $REF_EXP"')
s = rep(s, '"$SRC/scripts/pin-phpr.sh" s182 > "$OUT/pin.log" 2>&1', '"$SRC/scripts/pin-phpr.sh" s183 > "$OUT/pin.log" 2>&1')
s = rep(s, 'note "promozione corpus-gate: rc=0 — nomi==congelato (1412), CONTENUTO==golden, off-on zero (ZERO flip come atteso: L-RT1+L-RT2 a semantica identica per costruzione)"',
        'note "promozione corpus-gate: rc=0 — nomi==congelato (1412), CONTENUTO==golden, off-on zero (ZERO flip come atteso: L-MR1+L-MC2 a semantica identica per costruzione, prova per nome criterio-mc2 p.8)"')
s = rep(s, 'PHPR="$BIN" R=5 "$SRC/wp97-harness/micro/run-micro.sh" > "$OUT/micro-pin-s182.out" 2>&1\nnote "promozione micro pin s182: $(grep -E \'^rapporto_\' "$OUT/micro-pin-s182.out" | tr \'\\n\' \' \')"',
        'PHPR="$BIN" R=5 "$SRC/wp97-harness/micro/run-micro.sh" > "$OUT/micro-pin-s183.out" 2>&1\nnote "promozione micro pin s183: $(grep -E \'^rapporto_\' "$OUT/micro-pin-s183.out" | tr \'\\n\' \' \')"')
s = rep(s, '# ---- conferma POST-PIN: R=5 pin s182 vs stash s181 (STESSA toolchain 1.98.1) su calls-dq (bersaglio) e prop-dq (guardia) ----',
        '# ---- conferma POST-PIN: R=5 pin s183 vs stash s182 (STESSA toolchain 1.98.1) su mcalls-dq (bersaglio) e calls-dq/prop-dq (guardie) ----')
s = rep(s, 'note "conferma post-pin calls-dq (pin s182 vs stash s181, stessa toolchain): $(conferma "$H9/calls-dq.php" calls) (attesa: D ≈ cifra composta dell\'A/B rt2 [+12,50;+13,17])"',
        'note "conferma post-pin mcalls-dq (pin s183 vs stash s182, stessa toolchain): $(conferma "$H10/mcalls-dq.php" mcalls) (attesa: D ≈ cifra composta dell\'A/B mc2 [+19,00;+19,17])"\n'
        'note "conferma post-pin calls-dq (guardia, pin s183 vs stash s182): $(conferma "$H9/calls-dq.php" calls) (attesa |D| < 1: Ret fuso delle funzioni già ammesso)"')
s = rep(s, 'note "conferma post-pin prop-dq (guardia, pin s182 vs stash s181): $(conferma "$H/prop-dq.php" prop) (attesa |D| < 1: sola lettura)"',
        'note "conferma post-pin prop-dq (guardia, pin s183 vs stash s182): $(conferma "$H/prop-dq.php" prop) (attesa |D| < 1: sola lettura)"')
s = rep(s, '"$SRC/scripts/pin-server.sh" s182 > "$OUT/pin-server.log" 2>&1', '"$SRC/scripts/pin-server.sh" s183 > "$OUT/pin-server.log" 2>&1')
s = rep(s, 'note "PROMOZIONE COMPLETA rc=0 (da promo-out/rcb): pin s182 = $H2"', 'note "PROMOZIONE COMPLETA rc=0 (da promo-out/rcb): pin s183 = $H2"')
# gate invarianti: la REF ora è lo stash s182 — etichette dei file e dei messaggi
s = rep(s, '"$OUT/$n-s181.out"', '"$OUT/$n-s182.out"', 3)
s = rep(s, 'note "promozione gate $n: pin==stash s181 BYTE-ID ($d)"', 'note "promozione gate $n: pin==stash s182 BYTE-ID ($d)"')
s = rep(s, 'stop "gate $n: pin DIVERGE dallo stash s181 (promo-out/$n.diff)"', 'stop "gate $n: pin DIVERGE dallo stash s182 (promo-out/$n.diff)"')
s = rep(s, '# gate INVARIANTE: pin==stash s180 byte-id (+ marcatore quando preteso)', '# gate INVARIANTE: pin==stash s182 byte-id (+ marcatore quando preteso)')
# gate bilaterale nuovo dopo fx-rt2 (stesse opzioni oracle del gate dei bracci s185-leva-build.sh r.68; nessun `$nome` PHP nella stringa: veto S-185)
anchor = s[s.index('bilat fxrt2 "$H9/fx-rt2.php"'):]
anchor = anchor[:anchor.index('\n') + 1]
s = rep(s, anchor, anchor +
        'bilat fxmc2s185 "$H10/fx-mc2.php" "FX-MC2 DONE" "presidio DIRETTO L-MR1+L-MC2 (S-185): Ret fuso dei metodi (nota GC del ricevitore: dtor-late, ordine slots poi ricevitore, cascata del ricevitore risorto), MethodCall in pila (by-ref, default, ArgPlace sul cammino storico, dtor di temporanei in istruzione propria)" -d log_errors=0 -d display_errors=1\n')
assert '$this' not in s.split('bilat fxmc2s185')[1].split('\n')[0]
open('wp185-harness/s185-promozione.sh', 'w', encoding='utf-8').write(s)

l = open('wp184-harness/s184-lancio-promo.sh', encoding='utf-8').read()
l = rep(l, '# s184-lancio-promo.sh — lanciatore DETACHED della catena di promozione COMPOSTA s184 → pin s182 (s184-promozione.sh).\n# COPIA DICHIARATA di ../wp181-harness/s181-lancio-promo.sh (manifest s184-lancio-promo-copia.diff): soli path/tag.',
        '# s185-lancio-promo.sh — lanciatore DETACHED della catena di promozione COMPOSTA s185 → pin s183 (s185-promozione.sh).\n'
        '# COPIA DICHIARATA di ../wp184-harness/s184-lancio-promo.sh (manifest s185-lancio-promo-copia.diff): path/tag PIÙ\n'
        '# (i) attesa quiete CI (nessun cargo/rustc/phpt-runner, coda CI vuota; doppia verifica a 60 s, come s185-lancio-leva.sh) e\n'
        '# (ii) lock TOKEN s185-promo scritto dal lanciatore PRIMA della catena e rimosso a fine corsa (la CI si mette in mutex sul\n'
        '# lock e sul pattern harness/s1NN-): in S-184 il lock era della sessione, qui la catena corre di giorno con la CI attiva.')
l = rep(l, 'H="$SRC/wp184-harness"; O="$H/promo-out"; mkdir -p "$O"', 'H="$SRC/wp185-harness"; O="$H/promo-out"; mkdir -p "$O"')
l = rep(l, 'export PROMO_SP="/private/tmp/promo-s184-sp"', 'export PROMO_SP="/private/tmp/promo-s185-sp"')
l = rep(l, 'sentinelle inizio\n',
        'sentinelle inizio\n'
        'CIQ="/Volumes/Extreme Pro/Claude/phpr-ci/queue"\n'
        'ci_busy(){ pgrep -qx cargo || pgrep -qx rustc || pgrep -qf phpt-runner || [ -n "$(ls "$CIQ" 2>/dev/null)" ]; }\n'
        'l "attesa quiete CI (cargo/rustc/phpt-runner assenti, coda vuota)"\n'
        'while ci_busy; do sleep 60; done; sleep 60\n'
        'while ci_busy; do sleep 60; done\n'
        'MLOCK=/private/tmp/phpr-measure.lock\n'
        'echo "s185 promozione pin s183 $(date \'+%F %T\') pid=$$" > "$MLOCK"\n'
        'l "CI quieta — lock scritto: $MLOCK (TOKEN s185-promo)"\n')
l = rep(l, '"$H/s184-promozione.sh" >> "$LOG" 2>&1\nrc=$?', '"$H/s185-promozione.sh" >> "$LOG" 2>&1\nrc=$?\nrm -f "$MLOCK"; l "lock rimosso"')
open('wp185-harness/s185-lancio-promo.sh', 'w', encoding='utf-8').write(l)
print('ok')
