#!/bin/bash

# Bash test file with various issues

# Use of /tmp without proper safety
echo "data" > /tmp/unsafe_file

# eval executes arbitrary strings
eval "$1"

# Insecure HTTP download
curl http://example.com/file

# sudo usage (ensure least-privilege)
sudo rm -rf /tmp/*

# Consider 'set -euo pipefail' for safety
set -e

# Use xargs/find -print0 for performance/robustness
for file in $(find . -name "*.txt"); do
    echo "Processing $file"
done

# More issues
echo "Processing files..."
for item in $(ls); do
    echo "Found: $item"
done
