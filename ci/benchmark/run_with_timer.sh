#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 3 ]]; then
  echo "Usage: $0 <output_csv> <metric_name> <command_string>"
  exit 1
fi

OUTPUT_CSV="$1"
METRIC_NAME="$2"
COMMAND_STRING="$3"

mkdir -p "$(dirname "$OUTPUT_CSV")"

if [[ ! -f "$OUTPUT_CSV" ]]; then
  echo "metric,duration_seconds" > "$OUTPUT_CSV"
fi

START_TS="$(date +%s)"
bash -lc "$COMMAND_STRING"
END_TS="$(date +%s)"

DURATION="$((END_TS - START_TS))"
echo "${METRIC_NAME},${DURATION}" >> "$OUTPUT_CSV"
echo "Recorded ${METRIC_NAME}=${DURATION}s in ${OUTPUT_CSV}"
