#!/usr/bin/env python3
# gen-leva-build.py — genera s185-leva-build.sh come COPIA DICHIARATA di wp184-harness/s184-leva-build.sh (bracci Z/B/M della
# leva (a) L-MR1+L-MC2, criterio s185-criterio-mc2.md p.3/p.6). Ogni sostituzione e' asserita UNICA; manifest
# s185-leva-build-copia.diff. Adattamenti: token s185, tag s185-leva, pin atteso s182, fixture fx-mc2 (NUOVA) in riferimento +
# parita' + bersaglio del mutante (fx-rt2 resta a parita'), MUTANTE = «Ret fuso del metodo SENZA la nota GC di $this» (riga
# gc_note_this tolta dall'archivio; esito esatto: M diverge dall'oracle su fx-mc2 su >=1 riga e TUTTE le righe cambiate sono
# MC2-dtor*), DISASM come GATE vs il PIN s182 (non piu' vs tree-RT1): Δsp_refs <= +97 (soglia derivata S-184 az.rev. #3) e
# |Δbl| <= 2, altrimenti rc=5.
import os, subprocess
H = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(H, "..", "wp184-harness", "s184-leva-build.sh"); DST = os.path.join(H, "s185-leva-build.sh")
s = open(SRC).read()
def sub(old, new):
    global s
    assert s.count(old) == 1, f"NON unico ({s.count(old)}): {old[:70]!r}"
    s = s.replace(old, new)
sub("#!/bin/bash\n# s184-leva-build.sh — bracci Z (gemello del pin s181) e B (tree = L-RT1 + L-RT2) + MUTANTE",
    "#!/bin/bash\n# s185-leva-build.sh — bracci Z (gemello del pin s182) e B (tree = pin + L-MR1 + L-MC2, leva (a) «metodi») + MUTANTE\n"
    "# (criterio s185-criterio-mc2.md p.3/p.6): COPIA DICHIARATA di ../wp184-harness/s184-leva-build.sh (manifest s185-leva-build-copia.diff,\n"
    "# generatore gen-leva-build.py) coi SOLI adattamenti: token s185, tag s185-leva, pin atteso s182 159eee40be506171, fixture fx-mc2 (NUOVA)\n"
    "# in riferimento + parita' + bersaglio del mutante (fx-rt2 resta a parita'), MUTANTE = «Ret fuso del metodo SENZA la nota GC di $this»\n"
    "# (riga gc_note_this tolta dall'archivio con assert di unicita'; esito esatto: M diverge dall'oracle su fx-mc2 su >=1 riga e TUTTE le\n"
    "# righe cambiate sono MC2-dtor*), DISASM come GATE vs il PIN s182: Δsp_refs <= +97 e |Δbl| <= 2, altrimenti rc=5. Testo S-184 sotto:\n"
    "# s184-leva-build.sh — bracci Z (gemello del pin s181) e B (tree = L-RT1 + L-RT2) + MUTANTE")
sub('H="$REPO/php-rust/wp184-harness"; H1="$REPO/php-rust/wp181-harness"; H3="$REPO/php-rust/wp182-harness"; OUT="$H/ab-out/s184-leva"; mkdir -p "$OUT"\n'
    'VERD="$H/s184-leva-build-verdetto.out"; DONE="$H/ab-out/s184-leva.done"; rm -f "$DONE"',
    'H="$REPO/php-rust/wp185-harness"; H1="$REPO/php-rust/wp181-harness"; H3="$REPO/php-rust/wp182-harness"; H4="$REPO/php-rust/wp184-harness"; OUT="$H/ab-out/s185-leva"; mkdir -p "$OUT"\n'
    'VERD="$H/s185-leva-build-verdetto.out"; DONE="$H/ab-out/s185-leva.done"; rm -f "$DONE"')
sub('PIN_ATTESO="19a2faa83a492745"', 'PIN_ATTESO="159eee40be506171"')
sub('FXRT="$H3/fx-rt1.php"; FXRT2="$H/fx-rt2.php"; TREE_RT1="$H3/ab-out/s183-leva/phpr-B"\nSRC="/Volumes/Extreme Pro/Claude/s184-leva"; BUNDLE_MP="$HOME/Claude/phpr-target"; TGT="$BUNDLE_MP/s184-leva-tgt"',
    'FXRT="$H3/fx-rt1.php"; FXRT2="$H4/fx-rt2.php"; FXMC2="$H/fx-mc2.php"\nSRC="/Volumes/Extreme Pro/Claude/s185-leva"; BUNDLE_MP="$HOME/Claude/phpr-target"; TGT="$BUNDLE_MP/s185-leva-tgt"')
sub('grep -qw s184 "$LOCK"', 'grep -qw s185 "$LOCK"')
sub('"$FXRT" "$FXRT2" "$TREE_RT1"; do', '"$FXRT" "$FXRT2" "$FXMC2"; do')
sub('note "== s184 bracci Z/B/M leva COMPOSTA L-RT1+L-RT2 — riferimento A = pin s181 $PH, tree-RT1 $(shasum -a 256 "$TREE_RT1" | cut -c1-8), sorgente B',
    'note "== s185 bracci Z/B/M leva (a) L-MR1+L-MC2 — riferimento A = pin s182 $PH, sorgente B')
sub('diff -q "$OUT/fxrt2-oracle.out" "$OUT/fxrt2-pin.out" > /dev/null || { note "rc=7 fx-rt2: pin ≠ oracle (fixture non bilaterale a monte)"; fin 7; }\n',
    'diff -q "$OUT/fxrt2-oracle.out" "$OUT/fxrt2-pin.out" > /dev/null || { note "rc=7 fx-rt2: pin ≠ oracle (fixture non bilaterale a monte)"; fin 7; }\n'
    '"$ORACLE" -d log_errors=0 -d display_errors=1 "$FXMC2" > "$OUT/fxmc2-oracle.out" 2>&1\n'
    'perl -e \'alarm 120; exec @ARGV or die\' -- "$PIN" "$FXMC2" > "$OUT/fxmc2-pin.out" 2>&1\n'
    'grep -q "FX-MC2 DONE" "$OUT/fxmc2-pin.out" || { note "rc=7 riferimento: marcatore FX-MC2 assente sul pin"; fin 7; }\n'
    'diff -q "$OUT/fxmc2-oracle.out" "$OUT/fxmc2-pin.out" > /dev/null || { note "rc=7 fx-mc2: pin ≠ oracle (fixture non bilaterale a monte)"; fin 7; }\n')
sub("· fx-rt1/fx-rt2 pin==oracle BYTE-ID\"", "· fx-rt1/fx-rt2/fx-mc2 pin==oracle BYTE-ID\"")
sub('note "rc=4 Z: build FALLITA (ab-out/s184-leva/build-Z.log)"', 'note "rc=4 Z: build FALLITA (ab-out/s185-leva/build-Z.log)"')
sub('note "rc=4 B: build FALLITA (ab-out/s184-leva/build-B.log)"', 'note "rc=4 B: build FALLITA (ab-out/s185-leva/build-B.log)"')
sub('note "rc=4 M: build FALLITA (ab-out/s184-leva/build-M.log)"', 'note "rc=4 M: build FALLITA (ab-out/s185-leva/build-M.log)"')
sub("# M = B + mutante: ammissione del Ret FUSO senza i bit di FORMA (shape/flags/ret_cell) — sostituzione sull'ARCHIVIO, mai sul tree — DEVE divergere su fx-rt2 (righe RT2-)\n"
    "python3 - \"$SRC/php-rust/crates/php-runtime/src/vm/run.rs\" <<'PY' || { echo \"mutante non applicato\" >> \"$OUT/mutante.err\"; }\n"
    "import sys\n"
    "p = sys.argv[1]; s = open(p).read()\n"
    "old = ('                        f.func.ret_shape == 0\\n'\n"
    "       '                            && f.flags.bits() == 0\\n'\n"
    "       '                            && f.ret_cell.is_none()\\n'\n"
    "       '                            && f.this.is_none()\\n')\n"
    "assert s.count(old) == 1, 'sito ammissione Ret fuso non unico'\n"
    "s = s.replace(old, '                        // MUTANTE s184: ammissione SENZA shape/flags/ret_cell\\n                        f.this.is_none()\\n')\n",
    "# M = B + mutante: Ret fuso del METODO senza la nota GC di $this (gc_note_this tolta) — sostituzione sull'ARCHIVIO, mai sul tree — DEVE divergere su fx-mc2 (righe MC2-dtor*)\n"
    "python3 - \"$SRC/php-rust/crates/php-runtime/src/vm/run.rs\" <<'PY' || { echo \"mutante non applicato\" >> \"$OUT/mutante.err\"; }\n"
    "import sys\n"
    "p = sys.argv[1]; s = open(p).read()\n"
    "old = ('                        if self.frames[top].this.is_some() {\\n'\n"
    "       '                            self.gc_note_this(top);\\n'\n"
    "       '                        }\\n')\n"
    "assert s.count(old) == 1, 'sito nota GC di $this nel Ret fuso non unico'\n"
    "s = s.replace(old, '                        // MUTANTE s185: Ret fuso del metodo SENZA la nota GC di $this\\n')\n")
sub("grep -q 'MUTANTE s184'", "grep -q 'MUTANTE s185'")
sub('note "M: binario $MH (B + mutante: ammissione del Ret fuso senza shape/flags/ret_cell)"', 'note "M: binario $MH (B + mutante: Ret fuso del metodo senza la nota GC di $this)"')
sub('note "B: $n DIVERGE dall\'oracle ($(wc -l < "$OUT/$n.diff" | tr -d \' \') righe, ab-out/s184-leva/$n.diff) -> rc=2"',
    'note "B: $n DIVERGE dall\'oracle ($(wc -l < "$OUT/$n.diff" | tr -d \' \') righe, ab-out/s185-leva/$n.diff) -> rc=2"')
sub('bilat fxrt2 "$FXRT2" "FX-RT2 DONE" -d log_errors=0 -d display_errors=1\n',
    'bilat fxrt2 "$FXRT2" "FX-RT2 DONE" -d log_errors=0 -d display_errors=1\nbilat fxmc2 "$FXMC2" "FX-MC2 DONE" -d log_errors=0 -d display_errors=1\n')
sub("# mutante: DEVE divergere dall'oracle su fx-rt2 con ≥1 riga cambiata e TUTTE le righe cambiate etichettate RT2- (esito esatto, criterio-rt2 p.3)\n"
    "perl -e 'alarm 120; exec @ARGV or die' -- \"$OUT/phpr-M\" \"$FXRT2\" > \"$OUT/fxrt2-M.out\" 2>&1\n"
    "diff \"$OUT/fxrt2-oracle.out\" \"$OUT/fxrt2-M.out\" > \"$OUT/fxrt2-M.diff\" || true\n"
    "MCH=$(grep -c '^[<>]' \"$OUT/fxrt2-M.diff\"); MBAD=$(grep '^[<>]' \"$OUT/fxrt2-M.diff\" | grep -vcE '^[<>] (RT2-|FX-RT2 DONE|Fatal error|Stack trace|#[0-9]|  thrown)|^[<>] ?$')\n"
    "if [ \"$MCH\" -gt 0 ] && [ \"$MBAD\" -eq 0 ]; then\n"
    "  note \"MUTANTE: morde — fx-rt2 righe cambiate $MCH, tutte RT2- (non RT2- $MBAD): etichette $(grep '^[<>]' \"$OUT/fxrt2-M.diff\" | sed 's/^[<>] \\(RT2-[a-z-]*\\).*/\\1/' | sort -u | tr '\\n' ' ') — la fixture presidia l'ammissione\"\n"
    "else\n"
    "  note \"MUTANTE: NON morde nella forma attesa (fx-rt2 cambiate $MCH, non RT2- $MBAD; ab-out/s184-leva/fxrt2-M.diff) -> rc=3\"; [ \"$RC\" -eq 0 ] && RC=3\n"
    "fi\n",
    "# mutante: DEVE divergere dall'oracle su fx-mc2 con ≥1 riga cambiata e TUTTE le righe cambiate etichettate MC2-dtor (esito esatto, criterio-mc2 p.3)\n"
    "perl -e 'alarm 120; exec @ARGV or die' -- \"$OUT/phpr-M\" \"$FXMC2\" > \"$OUT/fxmc2-M.out\" 2>&1\n"
    "diff \"$OUT/fxmc2-oracle.out\" \"$OUT/fxmc2-M.out\" > \"$OUT/fxmc2-M.diff\" || true\n"
    "MCH=$(grep -c '^[<>]' \"$OUT/fxmc2-M.diff\"); MBAD=$(grep '^[<>]' \"$OUT/fxmc2-M.diff\" | grep -vcE '^[<>] MC2-dtor')\n"
    "if [ \"$MCH\" -gt 0 ] && [ \"$MBAD\" -eq 0 ]; then\n"
    "  note \"MUTANTE: morde — fx-mc2 righe cambiate $MCH, tutte MC2-dtor (non MC2-dtor $MBAD): etichette $(grep '^[<>]' \"$OUT/fxmc2-M.diff\" | sed 's/^[<>] \\(MC2-[a-z-]*\\).*/\\1/' | sort -u | tr '\\n' ' ') — la fixture presidia la nota GC di \\$this\"\n"
    "else\n"
    "  note \"MUTANTE: NON morde nella forma attesa (fx-mc2 cambiate $MCH, non MC2-dtor $MBAD; ab-out/s185-leva/fxmc2-M.diff) -> rc=3\"; [ \"$RC\" -eq 0 ] && RC=3\n"
    "fi\n")
sub('DPIN=$(dis "$PIN" pin); DZ=$(dis "$OUT/phpr-Z" Z); DB=$(dis "$OUT/phpr-B" B); DT=$(dis "$TREE_RT1" treeRT1)\n'
    'note "DISASM run_loop: pin s181 $DPIN · Z $DZ · tree-RT1 9ef70777 $DT · B $DB"',
    'DPIN=$(dis "$PIN" pin); DZ=$(dis "$OUT/phpr-Z" Z); DB=$(dis "$OUT/phpr-B" B); DT="$DPIN"\n'
    'note "DISASM run_loop: pin s182 $DPIN · Z $DZ · B $DB (gate vs il PIN: Δsp_refs ≤ +97, |Δbl| ≤ 2 — criterio-mc2 p.6)"')
sub('  if [ "$DI" -lt 0 ] && [ "$DSP" -le 100 ]; then note "GATE disasm (criterio-rt2 p.7-8 forma 2): Δistr=$DI (<0) Δsp_refs=$DSP (≤100, emenda p.8) vs tree-RT1 ⇒ RISPETTATO · Δbl=$DBL a verbale"; else note "GATE disasm (forma 2): Δistr=$DI Δsp_refs=$DSP FUORI attesa (istr<0, sp_refs≤100 — emenda p.8) ⇒ meccanismo da rileggere, niente misura -> rc=5 · Δbl=$DBL"; [ "$RC" -eq 0 ] && RC=5; fi',
    '  if [ "$DSP" -le 97 ] && [ "$DBL" -ge -2 ] && [ "$DBL" -le 2 ]; then note "GATE disasm (criterio-mc2 p.6): Δsp_refs=$DSP (≤ +97) Δbl=$DBL (∈ [−2;+2]) vs pin s182 ⇒ RISPETTATO · Δistr=$DI a verbale"; else note "GATE disasm: Δsp_refs=$DSP Δbl=$DBL FUORI attesa (sp_refs ≤ +97, |bl| ≤ 2) vs pin s182 ⇒ meccanismo da rileggere, niente misura -> rc=5 · Δistr=$DI"; [ "$RC" -eq 0 ] && RC=5; fi')
open(DST, "w").write(s); os.chmod(DST, 0o755)
with open(os.path.join(H, "s185-leva-build-copia.diff"), "w") as mf:
    subprocess.run(["diff", SRC, DST], stdout=mf)
print("generato", DST)
