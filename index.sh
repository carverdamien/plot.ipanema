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
$(for html in $@
do
echo '<li>' "<a href='${html}'>${html}</a>" '</li>'
done)
</ul>
</body>
</html>
EOF
