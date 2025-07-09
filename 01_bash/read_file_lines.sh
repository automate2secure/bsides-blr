#!/bin/bash

# Set the Internal Field Separator to empty to avoid split on space
while IFS= read -r line
do
    echo $line
    echo "***"
done < $1
