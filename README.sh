#!/bin/bash

cat <<EOF
# plot.ipanema

$(for f in $@
do
echo '*' "${f}" "[html](${f}.html)" "[pdf](${f}.pdf)"
done)
EOF
