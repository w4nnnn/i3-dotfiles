# ==========================================================
# ZSH Configuration - Catppuccin Mocha (HyDE Style)
# ==========================================================

# User environment & PATH
export PATH="$HOME/.local/bin:$HOME/.opencode/bin:$HOME/.npm-global/bin:$PATH"
export EDITOR="nano"
export VISUAL="nano"

# ---------------------------------------------------------
# History Settings
# ---------------------------------------------------------
HISTFILE="$HOME/.zsh_history"
HISTSIZE=10000
SAVEHIST=10000
setopt APPEND_HISTORY
setopt SHARE_HISTORY
setopt HIST_IGNORE_DUPS
setopt HIST_IGNORE_SPACE
setopt HIST_EXPIRE_DUPS_FIRST

# ---------------------------------------------------------
# Keybindings (Standard POSIX / Modern terminal)
# ---------------------------------------------------------
bindkey -e
bindkey '^[[H' beginning-of-line
bindkey '^[[F' end-of-line
bindkey '^[[3~' delete-char
bindkey '^[[1;5C' forward-word
bindkey '^[[1;5D' backward-word

# ---------------------------------------------------------
# Completion System
# ---------------------------------------------------------
autoload -Uz compinit
zstyle ':completion:*' menu select
zstyle ':completion:*' matcher-list 'm:{a-zA-Z}={A-Za-z}'
zstyle ':completion:*' list-colors "${(s.:.)LS_COLORS}"
compinit -d "$HOME/.cache/zcompdump"

# ---------------------------------------------------------
# Plugins & Tool Integrations
# ---------------------------------------------------------
# 1. FZF Integration
[ -f /usr/share/fzf/key-bindings.zsh ] && source /usr/share/fzf/key-bindings.zsh
[ -f /usr/share/fzf/completion.zsh ] && source /usr/share/fzf/completion.zsh

# 2. ZSH Autosuggestions (Catppuccin Surface2 color)
if [ -f /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh ]; then
    ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE='fg=#585b70'
    ZSH_AUTOSUGGEST_STRATEGY=(history completion)
    source /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh
fi

# 3. ZSH Syntax Highlighting (Must be loaded near the end)
if [ -f /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh ]; then
    source /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
fi

# ---------------------------------------------------------
# HyDE Style Aliases
# ---------------------------------------------------------
# Clear terminal
alias c='clear'

# Modern eza aliases (replacing ls)
if command -v eza >/dev/null 2>&1; then
    alias ls='eza --icons=auto'
    alias l='eza -lh --icons=auto'
    alias ll='eza -lha --icons=auto --sort=name --group-directories-first'
    alias la='eza -a --icons=auto'
    alias ld='eza -lhD --icons=auto'
    alias lt='eza --icons=auto --tree --level=2'
fi

# Modern bat alias (replacing cat)
if command -v bat >/dev/null 2>&1; then
    alias cat='bat --paging=never'
    alias b='bat'
fi

# Navigation shortcuts
alias ..='cd ..'
alias ...='cd ../..'
alias .3='cd ../../..'
alias .4='cd ../../../..'
alias .5='cd ../../../../..'

# Always create parent directories
alias mkdir='mkdir -p'

# Colored outputs
alias grep='grep --color=auto'
alias diff='diff --color=auto'
alias ip='ip -color=auto'

# Package manager shortcuts
alias update='sudo pacman -Syu'

# Git shortcuts
alias gs='git status'
alias ga='git add'
alias gc='git commit -m'
alias gp='git push'
alias gl='git log --oneline -10'

# ---------------------------------------------------------
# Starship Prompt Initialization
# ---------------------------------------------------------
if command -v starship >/dev/null 2>&1; then
    eval "$(starship init zsh)"
fi

# ---------------------------------------------------------
# Fastfetch Greeting on New Interactive Terminal
# ---------------------------------------------------------
if [[ -o interactive ]] && command -v fastfetch >/dev/null 2>&1; then
    fastfetch
fi
