#!/bin/bash
set -euo pipefail

# Get download directory
source "$HOME/.config/user-dirs.dirs"

# Generates a random PDF for uploading to Tinman
tex_dir="$(mktemp -d /tmp/tex-XXXXXXXX)"
tex_file="$tex_dir/random.tex"
pdf_file="$tex_dir/random.pdf"
final_file="$XDG_DOWNLOAD_DIR/random-$RANDOM.pdf"

function on_exit() {
	rm -rf "$tex_dir"
}

trap on_exit EXIT SIGINT SIGTERM 

cat > "$tex_file" << EOF
\\documentclass{article}
\\usepackage[T1]{fontenc}
\\usepackage{amsmath}

\\begin{document}
\\title{Randomly generated PDF}

Some math problems for you: \\par
\$$RANDOM + $RANDOM\$ \\par
\$$RANDOM - $RANDOM\$ \\par
\$$RANDOM \\cdot $RANDOM\$ \\par
\$$RANDOM \\div $RANDOM\$ \\par
\$$RANDOM^{$RANDOM}\$ \\par

\\end{document}
EOF

pdflatex -output-directory "$tex_dir" "$tex_file"
cp "$pdf_file" "$final_file"
echo "Copied to $final_file!"
