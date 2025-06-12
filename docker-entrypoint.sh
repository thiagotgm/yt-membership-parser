#!/bin/bash

set -e

exec uvicorn yt_membership_parser.api:app --host 0.0.0.0 --port 8000 "${args[@]}"
