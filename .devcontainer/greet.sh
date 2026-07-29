#!/usr/bin/env bash
# Printed every time someone attaches to the Codespace. Reports the actual state of
# frames/ rather than asserting it, because whether the frames are already on disk
# depends on whether this Codespace came from a prebuild.
cd "$(dirname "$0")/.." || exit 0

cat <<'EOF'

  Skinny Bob, 2026 — the whole stash, on a machine that isn't yours.

  Start with     FINDINGS.md              the writeup
                 CORRECTIONS.md           what turned out to be wrong
                 UNFINISHED_BUSINESS.md   things nobody has done yet

  Never coded before? Type  claude  or  codex  or  gemini  below and log in with a
  subscription you already have. All three are installed. Then paste one of the
  questions from README.md. gemini is the best of them at reading these images.
  Read AGENTS.md before trusting any AI about what is in an image here — this
  footage makes them hallucinate, and that is not a figure of speech.

EOF

have=$(ls -d frames/*/ 2>/dev/null | while read -r d; do
         [ "$(ls -1 "$d" 2>/dev/null | wc -l)" -gt 100 ] && echo "$d"; done | wc -l)
total=$(ls videos/2026/*.mkv videos/2011/*.mkv 2>/dev/null | wc -l)

if [ "$have" -ge "$total" ] && [ "$total" -gt 0 ]; then
  echo "  Frames for all $total videos are already extracted under frames/."
else
  cat <<'EOF'
  The seven source videos are here; extracted frames are not, and you almost
  certainly do not need all of them. To grab what you want:

      bin/frames OpSTlDJWFFI 2971 2974    a range, about ten seconds
      bin/frames OpSTlDJWFFI              one whole video, about a minute
      bin/frames                          all seven, about six minutes and 5 GB

  Or just ask the AI for "frames 2971 to 2974 of the May 2026 video" and let it
  run that for you.
EOF
fi
echo
