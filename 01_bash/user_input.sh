#!/bin/bash

# $@ contains the array of all values passed as command line args.
echo " Command line args: $@"

# User input with no prompts
# On a shell, $REPLY var can be used to echo the user input
read input_var
echo $input_var

# -p prompt to show it to user
read -p "Enter your name: " name
echo "Your name is $name"

# -s can be used to hide sensitive info.
read -p "Enter your password: " -s password

# -t timeout for user input
read -p "Enter secret code within 5 seconds." -t 5 code

# -n limits numbers of characters to accept from user
read -n 10 -p "Enter your phone (max 10 chars)" phone