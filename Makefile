.PHONY: venv bench-venv bench build serve open dev clean install install-vscode install-ghostty install-xcode install-unity install-zsh package-vscode publish-vscode

# Use the project venv (Python 3.15) when it exists. Create it with `make venv`.
PYTHON    := $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)
# The benchmark needs Python 3.13: TensorFlow 2.21 has no wheels for later versions.
BENCH_PY  := .venv-benchmark/bin/python
UV        := $(shell command -v /opt/homebrew/bin/uv || command -v uv)
SRC       := src/compile_color.py
JSON      := colors.json
OUT       := build
PORT      := 8000
PUBLISHER := monad-system

VSCODE_EXT_DIR    := $(HOME)/.vscode/extensions/monad-system.monad-system-theme-1.0.0
CURSOR_EXT_DIR    := $(HOME)/.cursor/extensions/monad-system.monad-system-theme-1.0.0
VSCODE_BUILD_DIR  := $(OUT)/themes/vscode
GHOSTTY_THEME_DIR := $(HOME)/.config/ghostty/themes
XCODE_THEME_DIR   := $(HOME)/Library/Developer/Xcode/UserData/FontAndColorThemes
XCODE_BUILD_DIR   := $(OUT)/themes/xcode
UNITY_GENERATED   := ../beta-bot_unity/Assets/Scripts/Generated/Monad
ZSH_PROFILE_DIR   := terminal/zsh

## build           — compile colors.json → all artifacts in build/
build:
	$(PYTHON) src/gen_icon.py
	$(PYTHON) $(SRC) --json_path $(JSON) --output_path $(OUT)/
	$(PYTHON) src/gen_motion_gifs.py
	@sips -z 128 128 assets/icon.png --out $(VSCODE_BUILD_DIR)/icon.png > /dev/null 2>&1 || true

## venv            — create .venv on uv-managed Python 3.15 and install requirements.txt
venv:
	$(UV) venv --python 3.15 .venv
	$(UV) pip install --python .venv/bin/python -r requirements.txt

## bench-venv      — create .venv-benchmark on uv-managed Python 3.13 for the perception benchmark
bench-venv:
	$(UV) venv --python 3.13 .venv-benchmark
	$(UV) pip install --python $(BENCH_PY) -r benchmark/requirements.txt

## bench           — build, then render, score and aggregate the perception benchmark
bench: build
	$(BENCH_PY) benchmark/render_layouts.py
	$(BENCH_PY) -m benchmark.score.run_batch
	$(BENCH_PY) -m benchmark.score.aggregate --write

## install         — build, then install VS Code + Ghostty + Xcode themes
install: build install-vscode install-ghostty install-xcode

## install-vscode  — copy built theme to VS Code + Cursor extensions
install-vscode:
	@for DIR in "$(VSCODE_EXT_DIR)" "$(CURSOR_EXT_DIR)"; do \
		rm -rf "$$DIR"; \
		mkdir -p "$$DIR"; \
		cp $(VSCODE_BUILD_DIR)/package.json "$$DIR/"; \
		cp $(VSCODE_BUILD_DIR)/monad-dark-color-theme.json "$$DIR/"; \
		cp $(VSCODE_BUILD_DIR)/monad-light-color-theme.json "$$DIR/"; \
		[ -f $(VSCODE_BUILD_DIR)/icon.png ] && cp $(VSCODE_BUILD_DIR)/icon.png "$$DIR/" || true; \
		echo "Installed → $$DIR"; \
	done
	@echo "Restart Cursor/VS Code, then: Cmd+K Cmd+T → Monad Dark / Monad Light"

## package-vscode  — package the VS Code extension as a .vsix file
## Requires: npm install -g @vscode/vsce  (run once, or: make vsce-install)
package-vscode:
	@which vsce > /dev/null 2>&1 || (echo "ERROR: vsce not found. Run: make vsce-install" && exit 1)
	@sips -z 128 128 assets/icon.png --out $(VSCODE_BUILD_DIR)/icon.png > /dev/null 2>&1 || true
	cd $(VSCODE_BUILD_DIR) && vsce package --out monad-system-theme.vsix --no-git-tag-version
	@echo ""
	@echo ".vsix ready → $(VSCODE_BUILD_DIR)/monad-system-theme.vsix"
	@echo "Install locally: code --install-extension $(VSCODE_BUILD_DIR)/monad-system-theme.vsix"

## publish-vscode  — publish the extension to the VS Code Marketplace
## Requires: vsce login $(PUBLISHER)  (run once with your PAT)
## Get a PAT at: https://dev.azure.com → User Settings → Personal Access Tokens
##   Scope: Marketplace → Manage
## Create publisher at: https://marketplace.visualstudio.com/manage
publish-vscode: package-vscode
	cd $(VSCODE_BUILD_DIR) && vsce publish --packagePath monad-system-theme.vsix
	@echo "Published to https://marketplace.visualstudio.com/items?itemName=$(PUBLISHER).monad-system-theme"

## vsce-install    — install the vsce packaging tool (requires npm)
vsce-install:
	npm install -g @vscode/vsce
	@echo "vsce installed. Authenticate with: vsce login $(PUBLISHER)"

## install-ghostty — copy built Ghostty themes to ~/.config/ghostty/themes/
install-ghostty:
	@mkdir -p $(GHOSTTY_THEME_DIR)
	@cp "$(OUT)/themes/ghostty/Monad Dark" "$(GHOSTTY_THEME_DIR)/Monad Dark"
	@cp "$(OUT)/themes/ghostty/Monad Light" "$(GHOSTTY_THEME_DIR)/Monad Light"
	@echo "Ghostty themes installed → $(GHOSTTY_THEME_DIR)"
	@echo "Add to ~/.config/ghostty/config:  theme = light:Monad Light,dark:Monad Dark"

## install-xcode   — copy built Xcode themes to Xcode's FontAndColorThemes directory
install-xcode:
	@mkdir -p "$(XCODE_THEME_DIR)"
	@cp "$(XCODE_BUILD_DIR)/Monad Dark.xccolortheme" "$(XCODE_THEME_DIR)/"
	@cp "$(XCODE_BUILD_DIR)/Monad Light.xccolortheme" "$(XCODE_THEME_DIR)/"
	@echo "Xcode themes installed → $(XCODE_THEME_DIR)"
	@echo "Restart Xcode, then: Settings → Themes → Monad Dark / Monad Light"

## install-unity   — copy generated C# (palette + motion + textures) into beta-bot_unity
install-unity: build
	@mkdir -p $(UNITY_GENERATED)
	@cp $(OUT)/ColorPalette.cs      $(UNITY_GENERATED)/ColorPalette.cs
	@cp $(OUT)/ColorPaletteLight.cs $(UNITY_GENERATED)/ColorPaletteLight.cs
	@cp $(OUT)/MotionTokens.cs      $(UNITY_GENERATED)/MotionTokens.cs
	@cp $(OUT)/TexturePatterns.cs   $(UNITY_GENERATED)/TexturePatterns.cs
	@echo "Installed Monad C# artifacts → $(UNITY_GENERATED)"

## install-zsh     — install the shared Zsh / Powerlevel10k profile into $HOME
install-zsh:
	@for f in .zshrc .p10k.zsh .zprofile; do \
		if [ -f "$(HOME)/$$f" ] && [ ! -L "$(HOME)/$$f" ]; then \
			cp "$(HOME)/$$f" "$(HOME)/$$f.bak"; \
			echo "Backed up $(HOME)/$$f → $(HOME)/$$f.bak"; \
		fi; \
		cp "$(ZSH_PROFILE_DIR)/$$f" "$(HOME)/$$f"; \
		echo "Installed $$f → $(HOME)/$$f"; \
	done
	@echo "Done. Requires Oh My Zsh + Powerlevel10k + a Nerd Font. Then run: exec zsh"

## serve           — start a local server at localhost:8000
serve:
	$(PYTHON) -m http.server $(PORT)

## open            — open the site in your default browser (run after serve)
open:
	open http://localhost:$(PORT)

## dev             — build, then serve + open in one step
dev: build
	@$(PYTHON) -m http.server $(PORT) &
	@sleep 0.5 && open http://localhost:$(PORT)

## clean           — wipe build/ artifacts (keeps directory)
clean:
	find $(OUT) -type f ! -name '.gitkeep' -delete
	@echo "build/ cleared"

## help            — list available targets
help:
	@grep -E '^## ' Makefile | sed 's/## /  make /' | grep -v '^\s*make Requires\|^\s*make Get\|^\s*make Create\|^\s*make Scope'

.DEFAULT_GOAL := build
