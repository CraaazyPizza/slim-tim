FROM mcr.microsoft.com/devcontainers/base:ubuntu-22.04

# ffmpeg is pinned by way of the base distro, not by apt version string.
# Ubuntu 22.04 ships ffmpeg 4.4.2, which is what decoded the reference frames.
# Do not move this base image without re-deriving every frame hash: the same
# decode command on a different ffmpeg can produce different bytes, and that
# difference is itself one of the findings this environment exists to check.
RUN apt-get update && apt-get install -y --no-install-recommends \
        ffmpeg \
        fontconfig \
        software-properties-common \
        curl ca-certificates \
    && add-apt-repository -y ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y --no-install-recommends \
        python3.12 \
        python3.12-venv \
        python3.12-dev \
        python3-pip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Everything analysis/ actually imports, at the versions that produced the
# published numbers. scipy is used in 132 places and matplotlib in 44, so a
# thinner install would leave most of analysis/ unable to run. fontconfig is here
# because the typeface work shells out to fc-list.
RUN python3.12 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir \
        numpy==2.4.6 \
        pillow==12.3.0 \
        scipy==1.18.0 \
        matplotlib==3.11.0 \
        opencv-python-headless==5.0.0.93 \
        scikit-image==0.26.0 \
        fonttools==4.63.0 \
        yt-dlp

# The GitHub CLI. The contribution path depends on it: "ask the AI to add this to
# the repo" means forking and opening a pull request, which needs the API and not
# just git. The devcontainers base image ships common-utils and git only, so gh is
# absent unless asked for — and it belongs here rather than in devcontainer.json
# "features" because a plain `docker build`, which is how the GHCR image is
# produced, ignores features entirely. In a Codespace gh picks up the injected
# token and is usually already authenticated; elsewhere, `gh auth login`.
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
        -o /usr/share/keyrings/githubcli-archive-keyring.gpg \
    && chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
        > /etc/apt/sources.list.d/github-cli.list \
    && apt-get update && apt-get install -y --no-install-recommends gh \
    && apt-get clean

# Node, then the three coding CLIs. Preinstalled so that "log in" is the entire
# setup step for a visitor — no npm, no PATH fiddling. Each still needs the
# visitor's own account; nothing here carries or implies credentials.
#
# gemini is included deliberately and not as an afterthought: it is the strongest
# of the three at actually looking at these images, and AGENTS.md treats a second
# opinion from a different model as part of the method rather than a nicety.
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && apt-get clean && rm -rf /var/lib/apt/lists/* \
    && npm install -g --no-fund --no-audit \
        @anthropic-ai/claude-code \
        @openai/codex \
        @google/gemini-cli \
    && npm cache clean --force

# Record what this image actually contains, so a mismatch between the environment
# a result was produced in and the one it is being checked in is visible rather
# than silent. frames/README.md explains why that distinction carried a finding.
RUN mkdir -p /opt/slim-tim \
    && ffmpeg -version | head -1 > /opt/slim-tim/built_ffmpeg.txt \
    && python3.12 --version > /opt/slim-tim/built_python.txt \
    && pip freeze > /opt/slim-tim/built_python_packages.txt \
    && { claude --version 2>/dev/null; codex --version 2>/dev/null; \
         gemini --version 2>/dev/null; gh --version 2>/dev/null | head -1; \
         yt-dlp --version 2>/dev/null; } > /opt/slim-tim/built_clis.txt || true
