#!/bin/bash
set -euo pipefail

# Get download directory
source "$HOME/.config/user-dirs.dirs"

# Generates a random PDF for uploading to Tinman
tex_dir="$(mktemp -d /tmp/tex-XXXXXXXX)"
tex_file="$tex_dir/random.tex"
pdf_file="$tex_dir/random.pdf"
final_file="$XDG_DOWNLOAD_DIR/random-$RANDOM$RANDOM.pdf"

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

This document is for STAGING or TESTING only. It allows the upload of files to fufill activities when the contents of the document is not relevant for the test at hand. \\par

Here's some random information to prevent Tinman from thinking the same file was reuploaded: \\par
\$$RANDOM^{$RANDOM} - $RANDOM \\cdot \\frac{$RANDOM + $RANDOM}{$RANDOM}\$ \\par

\\end{document}
EOF

chronic pdflatex -output-directory "$tex_dir" "$tex_file"
cp "$pdf_file" "$final_file"
echo "Copied to $final_file!"
