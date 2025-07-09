#!/bin/bash

# Redirect STDOUT to a file, overwrite old content.
curl https://google.com > google_source.html

# Redirect STDOUT to a file, append.
curl https://google.com >> google_source.html

# Redirect STDERR to a file, overwrite old content.
curl https://some-host-no-one-knows.com 2> error.txt

# Redirect STDERR to a file, append.
curl https://some-host-no-one-knows.com 2>> error.txt

# Redirect STDOUT and STDERR, only bash. Overwrite old content.
curl https://some-host-no-one-knows.com &> all_output.txt # Alternate 'curl https://google.com > all_output.txt 2>&1'

# Redirect STDOUT and STDERR, only bash. Append.
curl https://some-host-no-one-knows.com &>> all_output.txt # Alternate 'curl https://google.com >> all_output.txt 2>&1'