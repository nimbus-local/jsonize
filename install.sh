#!/bin/sh
set -e

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
SRC="$SCRIPT_DIR/jsonize"
DEST_DIR="$HOME/.local/bin"
DEST="$DEST_DIR/jsonize"

if [ ! -f "$SRC" ]; then
    echo "install.sh: cannot find jsonize next to this script ($SRC)" >&2
    exit 1
fi

mkdir -p "$DEST_DIR"
cp "$SRC" "$DEST"
chmod +x "$DEST"
echo "Installed jsonize to $DEST"

case ":$PATH:" in
    *":$DEST_DIR:"*)
        echo "$DEST_DIR is already on PATH."
        ;;
    *)
        case "$SHELL" in
            */zsh) RC="$HOME/.zshrc" ;;
            */bash) RC="$HOME/.bashrc" ;;
            *) RC="$HOME/.profile" ;;
        esac
        if [ -f "$RC" ] && grep -qF "$DEST_DIR" "$RC" 2>/dev/null; then
            echo "$RC already references $DEST_DIR; skipping."
        else
            printf '\n# added by jsonize install.sh\nexport PATH="%s:$PATH"\n' "$DEST_DIR" >> "$RC"
            echo "Added $DEST_DIR to PATH in $RC. Restart your shell or run: . $RC"
        fi
        ;;
esac

echo "Run 'jsonize -v' (after restarting your shell, if PATH was just updated) to verify."
