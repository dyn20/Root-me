<?php
function stringxor($o1, $o2) {
    $res = '';
    for($i=0;$i<strlen($o1);$i++)
        $res .= chr(ord($o1[$i]) ^ ord($o2[$i]));        
    return $res;
}
echo stringxor('c92fcd618967933ac463feb85ba00d5a7ae52842',base64_decode('VA5QA1cCVQgPXwEAXwZVVVsHBgtfUVBaV1QEAwIFVAJWAwBRC1tRVA==')); 
?>