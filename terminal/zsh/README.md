# Monad Terminal — Zsh / Oh My Zsh Profile

The unified shell profile so every machine shares the same terminal
experience: the same prompt, the same colors, the same "look."

Stack:

- **Oh My Zsh** — framework (`plugins=(git)`)
- **Powerlevel10k** — prompt theme. All the color codes and the prompt "look"
  live in [`.p10k.zsh`](.p10k.zsh) (lean, 1-line, transient prompt,
  nerdfont-v3 + powerline glyphs).

## Files

| File | Purpose |
|---|---|
| `.zshrc` | Oh My Zsh bootstrap, plugins, PATH/tooling setup (conda, nvm, pyenv, bun, …) |
| `.p10k.zsh` | Powerlevel10k prompt config — the colors and prompt layout |
| `.zprofile` | Login-shell Homebrew shellenv |

## Secrets

`.zshrc` does **not** contain API keys or tokens. Any machine-local secrets go
in `~/.zshrc.local` (untracked), which `.zshrc` sources automatically:

```sh
# ~/.zshrc.local
export DEEPSEEK_API_KEY="…"
```

## Prerequisites

```sh
# Oh My Zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# Powerlevel10k
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git \
  "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k"
```

A [Nerd Font](https://www.nerdfonts.com/) (e.g. MesloLGS NF) is required for the
prompt glyphs to render correctly.

## Install

From the repo root:

```sh
make install-zsh
```

This backs up any existing `~/.zshrc`, `~/.p10k.zsh`, and `~/.zprofile`
(as `*.bak`) and copies these versions into `$HOME`. Then:

```sh
exec zsh
```
