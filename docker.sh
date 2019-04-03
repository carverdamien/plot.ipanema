#!/bin/bash
set -e -x

IMAGE=carverdamien/plot.ipanema

docker build -t ${IMAGE} .
docker run \
       -v ~/storage:/root/storage \
       -v ${PWD}/sysbench.csv:/workdir/sysbench.csv \
       -v ${PWD}/batch.csv:/workdir/batch.csv \
       -v ${PWD}/sysbench.json:/workdir/sysbench.json \
       -v ${PWD}/batch.json:/workdir/batch.json \
       -v ${PWD}/i80:/workdir/i80 \
       -v ${PWD}/README.md:/workdir/README.md \
       -v ${PWD}/index.html:/workdir/index.html \
       -ti --rm \
       -p 80${PORT:-:80} \
       ${IMAGE} \
       "$@"
