<?php
// FX-MC2 (S-185): presidio bilaterale della leva (a) «metodi»: Ret FUSO esteso al frame con $this (L-MR1) + MethodCall
// in pila nella forma di L-CR1 (a) (L-MC2) — oracle == phpr byte-id. Il rischio di L-MR1 è la NOTA GC di $this: il Ret
// fuso del metodo deve notare il ricevitore nello stesso ordine di gc_note_frame (slots, stack, $this) e con la stessa
// cascata per un ricevitore già distrutto (__destruct che chiama metodi su $this); il rischio di L-MC2 è l'ordine
// pop-args/recv/decay e il cammino ArgPlace (escluso dalla forma in pila). Ogni riga è etichettata «MC2-<bit>» = il bit
// di ammissione o il meccanismo che la presidia; il MUTANTE «Ret fuso del metodo SENZA la nota GC di $this» DEVE cambiare
// almeno una riga MC2-dtor* (distruttore ritardato) e nessun'altra.
class D {
    public function __construct(public string $n) {}
    function m($a, $b) { return $a + $b; }                       // forma 0 con $this: il Ret fuso del metodo (L-MR1)
    function __destruct() { echo "MC2-dtor: {$this->n} ", $this->m(1, 1), "\n"; } // IN_DESTRUCTOR + metodo su ricevitore distrutto (cascata)
}
class M {
    public $v = 7; public array $arr = [1, 2]; public static $cnt = 0;
    function plain($a, $b) { return $a + $b; }                    // MC2-plain: forma 0 (fuso)
    static function st($a) { return $a * 2; }                     // MC2-static: $this None (già fuso)
    function h(): int { return "5"; }                            // MC2-hint: RS_HINT, coercizione weak
    function hf(): int { return "x"; }                           // MC2-hint-fail: TypeError
    function &w() { static $s = 1; return $s; }                  // MC2-wrap: by-ref, alias
    function &d() { $a = [1, 2]; return $a; }                     // MC2-deref: by-ref in contesto di valore (RET_DEREF)
    function __toString(): string { return "tostr"; }            // MC2-tostr: RET_STRINGIFY
    function __get($k) { return "get:$k"; }                      // MC2-get: magic con guard (ext)
    function __set($k, $v) { echo "MC2-set: $k=$v\n"; }          // MC2-set: ritorno magic scartato (ret_cell)
    function __isset($k) { return $k === 'yes'; }                // MC2-isset: RET_ISSET
    function __clone() { $this->v++; }                           // MC2-clone: CLONE_INIT
    function fe() { foreach ($this->arr as $x) { if ($x == 2) return $x; } return 0; } // MC2-foreach: iters non vuoti al Ret
    function ext($a) { return $a + count(func_get_args()); }     // MC2-ext: argomenti in più (ext)
    function dyn($name) { $$name = 9; return $x ?? 0; }          // MC2-dyn: dyn_vars
    function gen() { yield 1; yield 2; }                         // MC2-gen: generatore
    function cl() { return function () { return $this->v; }; }  // MC2-closure: Closure legata a $this
    function mk($n) { $d = new D($n); return $d->m(2, 3); }       // MC2-dtor-local: ricevitore ultimo riferimento nel chiamante
    function nested($a) { return $this->plain($a, $this->plain($a, 1)); } // MC2-nested: fuso annidato
    function nul() { }                                           // MC2-null: stack vuoto, Null implicito
    function place(array $a, int $i) { return $a[$i] + 1; }       // MC2-place: argomenti ArgPlace ($arr[$i] di $this)
}
$o = new M;
echo "MC2-plain: ", $o->plain(1, 2), " ", $o->nested(3), "\n";
echo "MC2-static: ", M::st(4), "\n";
echo "MC2-hint: "; var_dump($o->h());
try { $o->hf(); echo "MC2-hint-fail: nessun errore\n"; } catch (TypeError $e) { echo "MC2-hint-fail: ", get_class($e), "\n"; }
$r = &$o->w(); $r++; echo "MC2-wrap: ", $o->w(), "\n";
$x = $o->d(); $x[] = 3; echo "MC2-deref: ", count($x), "\n";
echo "MC2-tostr: ", (string) $o, " ", strlen($o), "\n";
echo "MC2-get: ", $o->zz, "\n";
$o->k = 5;
echo "MC2-isset: ", var_export(isset($o->yes), true), " ", var_export(isset($o->no), true), "\n";
$c = clone $o; echo "MC2-clone: ", $c->v, " ", $o->v, "\n";
echo "MC2-foreach: ", $o->fe(), "\n";
echo "MC2-ext: ", $o->ext(1, 2, 3), "\n";
echo "MC2-dyn: ", $o->dyn('x'), " ", $o->dyn('y'), "\n";
echo "MC2-gen: "; foreach ($o->gen() as $g) echo $g; echo "\n";
echo "MC2-closure: ", ($o->cl())(), "\n";
echo "MC2-null: "; var_dump($o->nul());
echo "MC2-place: ", $o->place($o->arr, 1), " ", $o->place([5, 6], $o->v - 6), "\n";
echo "MC2-dtor-local: ", $o->mk('a'), "\n";
echo "MC2-dtor-temp: ", (new D('t'))->m(4, 5), "\n";
echo "MC2-dtor-after: fine\n";
$d = new D('z'); echo "MC2-dtor-unset: ", $d->m(6, 7), "\n"; unset($d); echo "MC2-dtor-unset-after\n";
echo "FX-MC2 DONE\n";
