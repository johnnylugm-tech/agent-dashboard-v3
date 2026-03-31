#!/bin/bash
# Heartbeat Cron Script
# Run: ./heartbeat_cron.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Run the tracker
python3 scripts/heartbeat_tracker.py

# Log output
echo "$(date): Heartbeat executed" >> logs/heartbeat.log
