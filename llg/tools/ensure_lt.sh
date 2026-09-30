#!/bin/bash
# Start the LanguageTool server on 8081 if it is not answering.
# Needs Java 17+ and LanguageTool, which language_tool_python downloads on first use:
#   pip install language_tool_python && python3 -c "import language_tool_python as l; l.LanguageTool('en-US').close()"
if curl -s -o /dev/null -m 3 "http://127.0.0.1:8081/v2/languages"; then exit 0; fi
LT_DIR=$(ls -d "$HOME"/.cache/language_tool_python/LanguageTool-* 2>/dev/null | sort -V | tail -1)
[ -n "$LT_DIR" ] || { echo "LanguageTool is not downloaded yet, see the comment at the top of ensure_lt.sh" >&2; exit 1; }
cd "$LT_DIR" || exit 1
LOG="${TMPDIR:-/tmp}/lt-server.log"
(nohup java -Xmx2g -cp languagetool-server.jar org.languagetool.server.HTTPServer --port 8081 --allow-origin "*" > "$LOG" 2>&1 &)
for i in $(seq 1 30); do sleep 2; curl -s -o /dev/null -m 3 "http://127.0.0.1:8081/v2/languages" && exit 0; done
exit 1
