#!/usr/bin/env bash
# MATLAB Lab — yerel siteyi baslatir.
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORT="${PORT:-8787}"
HOST="${HOST:-127.0.0.1}"

# --- on kontroller -------------------------------------------------------
if ! command -v python3 >/dev/null 2>&1; then
  echo "HATA: python3 bulunamadi. Arch icin: sudo pacman -S python"
  exit 1
fi

if ! command -v octave-cli >/dev/null 2>&1 && ! command -v octave >/dev/null 2>&1; then
  echo "UYARI: GNU Octave bulunamadi."
  echo "       Kod calistirma ozelligi kapali olacak."
  echo "       Kurulum: sudo pacman -S octave"
  echo
  read -r -p "Devam edilsin mi? [e/H] " ans
  [[ "${ans:-h}" =~ ^[eE]$ ]] || exit 0
fi

# --- port bos mu ---------------------------------------------------------
if command -v ss >/dev/null 2>&1 && ss -ltn 2>/dev/null | grep -q ":${PORT} "; then
  echo "HATA: ${PORT} portu zaten kullanimda."
  echo "       Farkli port icin: PORT=8788 ./start.sh"
  exit 1
fi

echo "MATLAB Lab baslatiliyor..."
echo "Adres: http://${HOST}:${PORT}/"
echo "Durdurmak icin Ctrl+C"
echo

# tarayiciyi ac (arka planda, sunucu hazir olunca)
if command -v xdg-open >/dev/null 2>&1; then
  ( sleep 1.2; xdg-open "http://${HOST}:${PORT}/" >/dev/null 2>&1 || true ) &
fi

exec python3 "${DIR}/server.py" --port "${PORT}" --host "${HOST}"
