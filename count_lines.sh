find src -name "*.py" -type f -exec wc -l {} \; | awk '{total += $1} END {print total}'

# Old command
# find . -name "*.py" -type f -exec wc -l {} \; | awk '{total += $1} END {print total}'