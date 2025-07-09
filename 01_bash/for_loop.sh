#!/bin/bash

for number in 1 2 3 4 5 6 7 8 9 10
do
	if [ $(($number%2)) -eq 0  ]
	then
		echo $number is even
	else
		echo $number is odd
	fi
done
