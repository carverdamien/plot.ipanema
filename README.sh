#!/bin/bash

cat <<EOF
# plot.ipanema

Last update

$(date)

$(hostname)

$(for f in $@
do
echo '*' "${f}" "[html](${f}.html)" "[pdf](${f}.pdf)"
done)
EOF
