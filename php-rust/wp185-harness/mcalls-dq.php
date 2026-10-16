<?php class O { function m($a,$b){ return $a+$b; } } $o=new O; $s=0;
for($i=0;$i<60000000;$i++){ $s = $o->m($s,1); } echo $s,"\n";
