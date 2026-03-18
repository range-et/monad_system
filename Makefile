.PHONY: build serve open dev clean

PYTHON := python3
SRC    := src/compile_color.py
JSON   := colors.json
OUT    := build
PORT   := 8000

## build   — compile colors.json → all artifacts in build/
build:
	$(PYTHON) $(SRC) --json_path $(JSON) --output_path $(OUT)/

## serve   — start a local server at localhost:8000
serve:
	$(PYTHON) -m http.server $(PORT)

## open    — open the site in your default browser (run after serve)
open:
	open http://localhost:$(PORT)

## dev     — build, then serve + open in one step
dev: build
	@$(PYTHON) -m http.server $(PORT) &
	@sleep 0.5 && open http://localhost:$(PORT)

## clean   — wipe build/ artifacts (keeps directory)
clean:
	find $(OUT) -type f ! -name '.gitkeep' -delete
	@echo "build/ cleared"

## help    — list available targets
help:
	@grep -E '^## ' Makefile | sed 's/## /  make /'

.DEFAULT_GOAL := build
