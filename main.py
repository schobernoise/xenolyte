# __main__.py
import sys
from .myapp_cli import main as cli_main
from .myapp_gui import launch_gui

def entrypoint():
    """
    Decide which mode to run:

    * No arguments → launch the GUI (default behavior)
    * Any recognized CLI option → run the CLI path
    """
    # If the first token looks like a known CLI flag or a positional argument,
    # we treat it as CLI mode. Otherwise we fall back to GUI.
    # This simple heuristic works for most cases; feel free to tighten it.
    if len(sys.argv) > 1:
        # Example: allow `--help` or any non‑empty argument to trigger CLI.
        # You could also check for a special flag like `--gui` to force GUI.
        cli_main(sys.argv[1:])
    else:
        launch_gui()


if __name__ == "__main__":
    entrypoint()