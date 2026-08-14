#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p build
javac -d build src/*.java
echo "Compiled to build/"
