# Demo Guide

Run commands from the repository root after installing the project dependencies.

## CLI Demo

Use the module that contains the CLI entry point:

```bash
python -m minesweeper.cli
```

After editable install, the console script is also available:

```bash
minesweeper
```

Examples:

```bash
python -m minesweeper.cli --difficulty beginner --seed 7 --steps 30
python -m minesweeper.cli --evaluate --difficulty beginner --games 100
```

Do not run the package root as a module unless a package `__main__.py` is added.

## GUI Demo

Run the GUI module directly:

```bash
python -m minesweeper_gui.app
```

After editable install, the GUI script is also available:

```bash
minesweeper-gui
```
