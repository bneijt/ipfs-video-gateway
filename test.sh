#!/bin/bash

docker build -t ipfs-gateway .
docker run  --publish 4000:80 --volume /tmp/ipfs:/ipfs --rm -it ipfs-gateway