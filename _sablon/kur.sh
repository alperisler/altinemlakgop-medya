#!/usr/bin/env bash
# Bulut kurulumu: şablonları /home/claude/kit'e kurar (bilgisayar gerekmez).
# Kullanım: FONT_KEY=<anahtar> bash _sablon/kur.sh [hedef_klasör]
set -euo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)"
KIT="${1:-/home/claude/kit}"
: "${FONT_KEY:?FONT_KEY gerekli (görev talimatında yazılı)}"
rm -rf "$KIT"; mkdir -p "$KIT"
cp "$SRC"/*.py "$SRC"/*.json "$SRC"/*.png "$KIT"/
cp -r "$SRC"/logo "$SRC"/danisman "$KIT"/
openssl enc -d -aes-256-cbc -pbkdf2 -in "$SRC/fonts.tgz.enc" -pass "pass:$FONT_KEY" | tar -xz -C "$KIT"
mkdir -p "$KIT/foto"
echo "kit hazır: $KIT"; ls "$KIT/fonts"
