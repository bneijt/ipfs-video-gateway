#!/bin/bash
set -e
poetry install
poetry build
poetry run poetry-lock-package --build --no-root
docker build . -t ipfs-gateway