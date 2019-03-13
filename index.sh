#!/bin/bash

cat <<EOF
<!doctype html>
<html lang=en>
<head>
<meta charset=utf-8>
<title>plot.ipanema</title>
</head>
<body>
<h1>plot.ipanema</h1>
<ul>
$(for f in $@
do
echo '<li>' "${f}" "[<a href='${f}.html'>html</a>]" "[<a href='${f}.pdf'>pdf</a>]" '</li>'
done)
</ul>
</body>
</html>
EOF
