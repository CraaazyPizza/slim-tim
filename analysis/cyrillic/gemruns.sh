#!/bin/zsh
cd /home/user/new-skinny-bob
OUT=analysis/agent_cyr4/gem/answers.txt
: > $OUT
run() {
  echo "### PROMPT: $1" >> $OUT
  echo "### IMAGE: $2" >> $OUT
  gemini --skip-trust -p "@$2 $1" 2>/dev/null | grep -v "GOOGLE_API_KEY\|Ripgrep\|IDEClient" >> $OUT
  echo "" >> $OUT
  echo "----------------------------------------" >> $OUT
}
run "Transcribe ALL text visible in this image exactly as it appears. Do not interpret or summarise. If part of it is illegible, write [?] for the illegible part." "figs/cyrillic/gem/A_line2_x3.png"
run "What characters can you see in this image? List them left to right. Mark any you are not sure about with a question mark." "figs/cyrillic/gem/A_line2_x3.png"
run "This is a low-contrast enhanced crop of a video frame. Read out whatever writing is in it. If you cannot read it, say so." "figs/cyrillic/gem/A_line2_x3.png"
run "Transcribe ALL text visible in this image exactly as it appears, line by line. Do not interpret or summarise." "figs/cyrillic/gem/B_both_x2.png"
run "How many characters are in the final word or token at the right-hand end of this image, and what are they? Answer only about the right-hand end." "figs/cyrillic/gem/C_tail_x5.png"
run "Describe the shapes at the right-hand end of this image purely as shapes, without guessing at any letters or words." "figs/cyrillic/gem/C_tail_x5.png"
run "Transcribe ALL text visible in this image exactly as it appears. Do not interpret or summarise." "figs/cyrillic/gem/D_line1_x2.png"
