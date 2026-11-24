#!/bin/bash
# Double-click this file (or run `./start.command`) to start Interview Practice.
# It picks a Python that has pandas + numpy + statsmodels, starts the local server
# and opens http://127.0.0.1:8790 in your browser. Close the window or press Ctrl+C to stop.

cd "$(dirname "$0")" || exit 1

has_all()  { "$1" -c "import pandas, numpy, statsmodels" >/dev/null 2>&1; }
has_core() { "$1" -c "import pandas, numpy" >/dev/null 2>&1; }
is_py3()   { "$1" -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)" >/dev/null 2>&1; }

PY=""
CORE=""     # a Python with pandas + numpy but no statsmodels
FIRST=""    # any Python 3.8+

# 1. a private environment created by a previous run of this script
if [ -x ".venv/bin/python" ] && has_all ".venv/bin/python"; then
    PY=".venv/bin/python"
fi

# 2. any Python already on this Mac that has the three libraries
if [ -z "$PY" ]; then
    for candidate in python3 \
                     /opt/homebrew/bin/python3 \
                     /usr/local/bin/python3 \
                     /Library/Frameworks/Python.framework/Versions/Current/bin/python3 \
                     "$HOME/miniconda3/bin/python3" \
                     "$HOME/anaconda3/bin/python3" \
                     "$HOME/miniforge3/bin/python3" \
                     /usr/bin/python3; do
        path="$(command -v "$candidate" 2>/dev/null)" || continue
        is_py3 "$path" || continue
        [ -z "$FIRST" ] && FIRST="$path"
        if has_all "$path"; then PY="$path"; break; fi
        [ -z "$CORE" ] && has_core "$path" && CORE="$path"
    done
fi

# 3. otherwise offer to install them into a private .venv folder next to this file
if [ -z "$PY" ]; then
    if [ -z "$FIRST" ]; then
        echo "Python 3.8 or newer was not found. Install it from https://www.python.org/downloads/ and try again."
        read -r -p "Press Enter to close."
        exit 1
    fi
    echo "pandas, numpy and statsmodels were not all found."
    echo "(Millennium cases: pandas + numpy. Quantitative Methods: + statsmodels; matplotlib draws the charts.)"
    read -r -p "Install them into a private .venv folder here? Needs internet once. [Y/n] " answer
    FALLBACK="${CORE:-$FIRST}"
    case "$answer" in
        [nN]*) PY="$FALLBACK" ;;
        *)
            if "$FIRST" -m venv .venv && .venv/bin/python -m pip install --quiet --upgrade pip pandas numpy statsmodels matplotlib; then
                PY=".venv/bin/python"
            else
                echo "The installation failed; starting with what is available."
                PY="$FALLBACK"
            fi
            ;;
    esac
fi

exec "$PY" server.py "$@"
