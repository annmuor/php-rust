#!/usr/bin/env python3
# gen-ab-mc2.py — genera s185-ab-mc2.sh come COPIA DICHIARATA di wp184-harness/s184-ab-rt2.sh (A/B della leva (a) L-MR1+L-MC2,
# criterio s185-criterio-mc2.md p.4-5). Ogni sostituzione e' asserita UNICA; manifest s185-ab-mc2-copia.diff. Adattamenti: token
# s185, GIUDICE mcalls-dq (driver $o->m($s,1)) al posto di calls-dq, GUARDIA calls-dq al posto di arith-dq (prop-dq resta), PREV
# prop-dq 31,60 (pin s182), attesa [4;9], promozione se D >= max(4, rumore, |A-Z|) con ENTRAMBI gli stimatori, rc=3 = sola
# direzione (tenuta a CI OK, senza sottocaso RT2), rc=4 kill, verdetto s185-<TAG>. Resto INVARIATO.
import os, subprocess
H = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(H, "..", "wp184-harness", "s184-ab-rt2.sh"); DST = os.path.join(H, "s185-ab-mc2.sh")
s = open(SRC).read()
def sub(old, new):
    global s
    assert s.count(old) == 1, f"NON unico ({s.count(old)}): {old[:70]!r}"
    s = s.replace(old, new)
sub("#!/bin/bash\n# s184-ab-rt2.sh — A/B della LEVA COMPOSTA L-RT1 (nel tree) + L-RT2 «Ret fuso»",
    "#!/bin/bash\n# s185-ab-mc2.sh — A/B della LEVA (a) «metodi» L-MR1 «Ret fuso dei metodi» + L-MC2 «MethodCall in pila» (criterio s185-criterio-mc2.md\n"
    "# p.4-5): COPIA DICHIARATA di ../wp184-harness/s184-ab-rt2.sh (manifest s185-ab-mc2-copia.diff, generatore gen-ab-mc2.py) coi SOLI\n"
    "# adattamenti: token s185, GIUDICE mcalls-dq ($o->m($s,1), N dal sorgente) al posto di calls-dq, GUARDIA calls-dq al posto di arith-dq\n"
    "# (prop-dq resta), PREV prop-dq 31,60 (pin s182), attesa [4;9], promozione se D ≥ max(4, rumore, |A−Z|) con ENTRAMBI gli stimatori,\n"
    "# rc=3 = sola direzione (leva tenuta a CI OK), rc=4 kill, verdetto s185-<TAG>. Testo S-184 sotto:\n"
    "# s184-ab-rt2.sh — A/B della LEVA COMPOSTA L-RT1 (nel tree) + L-RT2 «Ret fuso»")
sub('R="${8:-5}"; PREVPD="${9:-31.27}"', 'R="${8:-5}"; PREVPD="${9:-31.60}"')
sub('CD="$H/calls-dq.php"\nGD="$H/../wp164-harness/arith-dq.php"', 'CD="$H/mcalls-dq.php"\nGD="$H/calls-dq.php"')
sub('VERD="$H/s184-$TAG-verdetto.out"', 'VERD="$H/s185-$TAG-verdetto.out"')
sub('grep -qw s184 /private/tmp/phpr-measure.lock 2>/dev/null || { echo "lock s184 assente (per TOKEN)"', 'grep -qw s185 /private/tmp/phpr-measure.lock 2>/dev/null || { echo "lock s185 assente (per TOKEN)"')
sub('echo "N non leggibile dal driver (calls=\'$NCD\' dq=\'$NGD\' prop=\'$NPD\')"', 'echo "N non leggibile dal driver (mcalls=\'$NCD\' calls=\'$NGD\' prop=\'$NPD\')"')
sub('echo "== s184 LEVA COMPOSTA L-RT1+L-RT2 $TAG — A=$AM MISURATO ($A, pin s181) Z=$ZM MISURATO ($ZZ, gemello del pin ricostruito$( [ "$ZM" = "$AM" ] && echo \' — BYTE-ID col pin: |A−Z| = solo rumore, SL in-run NON stimabile\' )) B=$BM MISURATO ($BB, tree = L-RT1 + L-RT2) — R=$R, N: calls-dq=$NCD arith-dq=$NGD prop-dq=$NPD, PREV prop-dq A (stesso binario, S-183: 31,27): $PREVPD,',
    'echo "== s185 LEVA (a) L-MR1+L-MC2 $TAG — A=$AM MISURATO ($A, pin s182) Z=$ZM MISURATO ($ZZ, gemello del pin ricostruito$( [ "$ZM" = "$AM" ] && echo \' — BYTE-ID col pin: |A−Z| = solo rumore, SL in-run NON stimabile\' )) B=$BM MISURATO ($BB, tree = pin + L-MR1 + L-MC2) — R=$R, N: mcalls-dq=$NCD calls-dq=$NGD prop-dq=$NPD, PREV prop-dq A (stesso binario, S-184: 31,60): $PREVPD,')
sub('SLc = layout("calls-dq", cA, cZ, None)', 'SLc = layout("mcalls-dq", cA, cZ, None)')
sub('SLg = layout("arith-dq", gA, gZ, None)', 'SLg = layout("calls-dq", gA, gZ, None)')
sub('print(f"|A−Z| SOPRA il pavimento 4 (calls {SLc:.2f}, prop {SLp:.2f}, arith {SLg:.2f})', 'print(f"|A−Z| SOPRA il pavimento 4 (mcalls {SLc:.2f}, prop {SLp:.2f}, calls {SLg:.2f})')
sub('print(f"GIUDICE calls-dq (BERSAGLIO, 1 Call+CheckArity+BinarySS+Ret per iter):', 'print(f"GIUDICE mcalls-dq (BERSAGLIO, 1 MethodCall+Ret di metodo+BinarySS per iter):')
sub('DCc, DCp, nC, nomC, regC, sgC = stat("GIUDICE calls-dq COMPOSTA L-RT1+L-RT2 (D = A−B, pin s181 → tree)", cA, cB, "B", "A", SLc)',
    'DCc, DCp, nC, nomC, regC, sgC = stat("GIUDICE mcalls-dq leva (a) L-MR1+L-MC2 (D = A−B, pin s182 → tree)", cA, cB, "B", "A", SLc)')
sub('print(f"ATTESA (criterio-rt2 p.4): D composta ∈ [3,5;6,5]: {\'CENTRATA\' if 3.5 <= DC <= 6.5 else \'FUORI\'} ({DCc:+.2f}/{DCp:+.2f}); quota propria di L-RT2 = D − [2,50;2,83] di L-RT1 = INDICATIVA (regola 3: non cifra)")',
    'print(f"ATTESA (criterio-mc2 p.4): D ∈ [4;9]: {\'CENTRATA\' if 4.0 <= DC <= 9.0 else \'FUORI\'} ({DCc:+.2f}/{DCp:+.2f}); ripartizione a1/a2 NON misurata (regola 4: direzione+meccanismo, magnitudine composta)")')
sub('print(f"GUARDIA prop-dq (sola regressione, nessun Call nel loop):', 'print(f"GUARDIA prop-dq (sola regressione, nessun Ret di metodo nel loop):')
sub('print(f"GUARDIA arith-dq (sola regressione, nessun Call nel loop): oracle={med(gO):.2f} ns/iter;', 'print(f"GUARDIA calls-dq (sola regressione, Ret fuso della funzione libera già ammesso): oracle={med(gO):.2f} ns/iter;')
sub('DGc, DGp, nG, nomG, regG, sgG = stat("GUARDIA arith-dq (attesa |D| < 1)", gA, gB, "B", "A", SLg)', 'DGc, DGp, nG, nomG, regG, sgG = stat("GUARDIA calls-dq (attesa |D| < 1)", gA, gB, "B", "A", SLg)')
sub('print(f"GUARDIA arith-dq ESITO attesa |D|<1:', 'print(f"GUARDIA calls-dq ESITO attesa |D|<1:')
sub('print(f"PREV per la prossima misura (same-binary pin s181): calls-dq A={med(cA):.2f} arith-dq A={med(gA):.2f} prop-dq A={med(pA):.2f} (PREV: {prevpd:.2f})")',
    'print(f"PREV per la prossima misura (same-binary pin s182): mcalls-dq A={med(cA):.2f} calls-dq A={med(gA):.2f} prop-dq A={med(pA):.2f} (PREV: {prevpd:.2f})")')
sub('print(f"GUARDIA: regressione su {\'prop-dq \' if regP else \'\'}{\'arith-dq\' if regG else \'\'}', 'print(f"GUARDIA: regressione su {\'prop-dq \' if regP else \'\'}{\'calls-dq\' if regG else \'\'}')
sub('print(f"PROMOZIONE: D calls-dq NOMINATA da entrambi gli stimatori [{min(DCc,DCp):+.2f};{max(DCc,DCp):+.2f}] (soglia max(4,rumore,SL)), guardie senza regressione ⇒ promozione COMPOSTA del TREE (L-RT1+L-RT2) con copia dichiarata di s181-promozione.sh (tag s182, CARGO_TARGET_DIR esplicito) + coppia t25 + ORM (rc=0)")',
    'print(f"PROMOZIONE: D mcalls-dq NOMINATA da entrambi gli stimatori [{min(DCc,DCp):+.2f};{max(DCc,DCp):+.2f}] (soglia max(4,rumore,SL)), guardie senza regressione ⇒ promozione del TREE (L-MR1+L-MC2) con copia dichiarata di s184-promozione.sh (tag s183, CARGO_TARGET_DIR esplicito) + coppia WP/ORM NOTTURNA (rc=0)")')
sub('''elif DC >= max(nC, SLc) and sgC == R:
    rt1hi = 2.83
    if DC >= rt1hi + max(nC, SLc):
        print(f"SOLO DIREZIONE composta: D {DCc:+.2f}/{DCp:+.2f} ≥ max(rumore {nC:.2f}, SL {SLc:.2f}) con segni {sgC}/{R} ma sotto la soglia; SOTTOCASO RT2 DIREZIONE (D ≥ 2,83 + max(rumore,SL) = {rt1hi + max(nC, SLc):.2f}) ⇒ L-RT2 TENUTA nel tree con L-RT1 SOLO a CI batteria+corpus OK sul commit (criterio-rt2 p.5; rc=3)")
    else:
        print(f"SOLO DIREZIONE composta: D {DCc:+.2f}/{DCp:+.2f} ≥ max(rumore {nC:.2f}, SL {SLc:.2f}) con segni {sgC}/{R} ma sotto la soglia; SOTTOCASO RT2 NULLA (D < 2,83 + max(rumore,SL) = {rt1hi + max(nC, SLc):.2f}: la composta non supera L-RT1 sola) ⇒ REVERT del commit L-RT2, il tree torna a L-RT1 sola (criterio-rt2 p.5; rc=3)")
    rc = 3
else:
    print(f"KILL L-RT2: D composta {DCc:+.2f}/{DCp:+.2f} < max(rumore {nC:.2f}, SL {SLc:.2f}) o segni misti ({sgC}/{R}) ⇒ revert al byte del commit L-RT2 (L-RT1 resta sul suo A/B S-183), meccanismo a verbale (rc=4)"); rc = 4''',
    '''elif DC >= max(nC, SLc) and sgC == R:
    print(f"SOLO DIREZIONE: D {DCc:+.2f}/{DCp:+.2f} ≥ max(rumore {nC:.2f}, SL {SLc:.2f}) con segni {sgC}/{R} ma sotto la soglia ⇒ leva (a) TENUTA nel tree SOLO a CI batteria+corpus OK sul commit, nessuna promozione (criterio-mc2 p.5; rc=3)")
    rc = 3
else:
    print(f"KILL leva (a): D {DCc:+.2f}/{DCp:+.2f} < max(rumore {nC:.2f}, SL {SLc:.2f}) o segni misti ({sgC}/{R}) ⇒ revert al byte del commit L-MR1+L-MC2, meccanismo a verbale (rc=4)"); rc = 4''')
open(DST, "w").write(s); os.chmod(DST, 0o755)
with open(os.path.join(H, "s185-ab-mc2-copia.diff"), "w") as mf:
    subprocess.run(["diff", SRC, DST], stdout=mf)
print("generato", DST)
