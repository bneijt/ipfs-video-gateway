#!/bin/bash
./build.sh
docker run  --publish 4000:80 --volume /tmp/ipfs:/ipfs --rm -it ipfs-video-gateway