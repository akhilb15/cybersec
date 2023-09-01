<?php
$origdata = json_encode(array( "showpassword"=>"no", "bgcolor"=>"#ffffff"));
$newdata = json_encode(array( "showpassword"=>"yes", "bgcolor"=>"#ffffff"));

function xor_encrypt($in, $xorkey) {
    $key = $xorkey;
    $text = $in;
    $outText = '';

    // Iterate through each character
    for($i=0;$i<strlen($text);$i++) {
    $outText .= $text[$i] ^ $key[$i % strlen($key)];
    }

    return $outText;
}
$key = xor_encrypt($origdata, base64_decode("MGw7JCQ5OC04PT8jOSpqdmkgJ25nbCorKCEkIzlscm5oKC4qLSgubjY="));
echo $key . "\n"; // key = KNHL
echo base64_encode(xor_encrypt($newdata, 'KNHL'));
