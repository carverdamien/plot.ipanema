#!/bin/bash

cat <<EOF
# plot.ipanema

$(for html in $@
do
echo '*' "[${html}](${html})"
done)
EOF
