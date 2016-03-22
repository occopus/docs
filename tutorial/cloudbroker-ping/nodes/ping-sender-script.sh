#!/bin/bash

cat > /tmp/message.txt <<EOF
{{variables.message}}
EOF

ping {{getip(variables.targetnode)}} -c 5 > /tmp/ping-result.txt 2>&1
