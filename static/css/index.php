<?php
$cpu=exec("top -bn 1 | grep Cpu  | awk '{ print ($2)}'");
$cpu1=explode("%",$cpu);
echo $cpu1[0];

$cpu=exec("atop -bn 1 | grep CPU  | awk '{ print (100)}'");
$cpu1=explode("%",$cpu);
echo $cpu1[0];

?>