Generato con assistenza AI (Claude Fable 5)
# Revisione adversariale S-185 — lente SEMANTICA

**Verdetto: REGGE CON RILIEVI.** Claim (7db3a0ec): L-MR1 e L-MC2 identici al cammino generale. Codice + tre sonde (oracle / pin 159eee40 / dev 7efc1151): nessuna divergenza pin→dev; un argomento del claim è incompleto e la fixture non presidia i due bit più delicati.

## Rilievi

1. **(Q1, regge)** `run.rs:4273-4306` vs `ret_slow` `run.rs:7214-7247`: per il frame ammesso la sequenza coincide: note slots→stack→this (`gc_note_frame` mod.rs:4612-4638), clear slots→stack, morte del Frame (`drop(frame)` in `recycle_frame` mod.rs:4698-4705 ≡ `truncate`; `this` è l'unico campo con Rc). Il take/rimessa di `gc_note_this` è sano: `gc_note_slow` (mod.rs:3963-4083) e `gc_cascade` (4584-4599) non leggono `frames` né eseguono codice utente; `strong_count` vede lo stesso holder. IN_DESTRUCTOR (bit 6) escluso da `flags==0`; `retired_main` escluso da `top>0`.
2. **(Q2, argomento incompleto)** «`decay_arg` senza codice utente ⇒ ordine inosservabile» non basta: `decay_arg` (calls.rs:312-329) lascia morire il Rc del `Ref`; se sole-holder di un oggetto → `Object::drop` (php-types/object.rs:365-387) → `free_object_id`, osservabile via LIFO degli handle. Storico: decay 0..n AVANTI dopo i pop (run.rs:7108-7111); nuovo: `(0..n).rev()` interleaved (run.rs:7060-7063). Caso raggiungibile non trovato (P1 `$o->m(d(1),d(2))`, `&d`: pin == dev), ma la prova va per NOME (Concilio WP-107, S-106-D-9: «operando mai last-ref»). Trace, `ip=1`, RET_DEREF: nessun osservatore tra push e `return` ✓; ricevitore mai ArgPlace (ammissione `Zval::Object` a `stack[len-n-1]`) ✓.
3. **(Q3, fixture)** fx-mc2 non presidia l'ORDINE slots→$this: serve locale ultimo-riferimento E ricevitore temporaneo (P2: `(new D('recv'))->k()` con `$x=new D('local')` in `k` → «dtor local» PRIMA di «dtor recv», identico su oracle/pin/dev). Un mutante «this prima di slots» passerebbe fx-mc2.
4. **(Q4, fixture)** fx-mc2.php:12 (`$this->m(1,1)` in `__destruct`) NON esercita la cascata: conteggio ≥2, oggetto ancora in `created`, e `gc_note_slow` esce su `destructed()` (mod.rs:3971): no-op per ogni mutante della nota; etichetta «cascata» errata. Il ramo `destructed ∧ ¬created ∧ count==1` lo esercita P3 (oggetto resuscitato in static, `D::take()->m(1)`): pin == dev.
5. **(fuori perimetro)** P1 e P3: divergenze PREESISTENTI pin≠oracle (ordine dtor/id di argomenti da funzione by-ref; dtor del ricevitore temporaneo DOPO l'echo = quesito «dtor-in-echo»). Non attribuibili alla leva.

## Azioni

A. Aggiungere a fx-mc2 le forme P2 e P3 (P3 in istruzione propria, `$r = D::take()->m(1);`, per restare byte-id) PRIMA di ratificare l'A/B; rieseguire il mutante M (atteso: morde anche sulla cascata).
B. Commento L-MC2 (run.rs:7035-7040): prova per nome del «mai last-ref» o dente handle-id LIFO con due argomenti by-ref.
C. Correggere fx-mc2.php:12.
D. Catalogare il rilievo 5 in PHPR_DIVERGENCES_FROM_PHP.md (REGOLE 9).
