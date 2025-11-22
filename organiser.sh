#!/user/bin/env bash
set -eou pipefail

LOGFILE="organiser.log"
ARCHIVE_DIR="archive"
if [ ! -d "$ARCHIVE_DIR" ]:then
    mkdir -p "$ARCHIVE_DIR"
fi
shopt -s nullglob
for f in *csv; do
[ -f "$f" ] || continue
ts=$(date +%Y%M%D-%H%M%S)
base= "${f%.csv}"
newname="${base}-${ts}.csv"
{
    echo "-----"
    echo "timestamp:$ (date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "Archiving: $f -> $ARCHIVE_DIR/$username"
    echo "contents."
    cat "$f"
    echo ""
} >> "$LOGFILE"

mv -- "$f" "ARCHIVE_DIR/$newname"
done
