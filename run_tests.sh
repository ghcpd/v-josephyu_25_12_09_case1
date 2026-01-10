#!/usr/bin/env bash
source .venv/bin/activate
.venv/bin/pytest -q
exit $?