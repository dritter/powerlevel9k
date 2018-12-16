# Pyenv

## Installation

To use this segment, you need to activate it by adding it to your
`P9K_LEFT_PROMPT_ELEMENTS` or `P9K_RIGHT_PROMPT_ELEMENTS` array, depending
where you want to show this segment.

## Configuration

This segment shows the version of Python being used when using `pyenv` to change your current Python stack.

The `PYENV_VERSION` environment variable will be used if specified. Otherwise it figures out the version being used by taking the output of the `pyenv version-name` command.

* If `pyenv` is not in $PATH, nothing will be shown.
* If the current Python version is the same as the global Python version, nothing will be shown.

| Variable | Default Value | Description |
|----------|---------------|-------------|
|`P9K_PYENV_PROMPT_ALWAYS_SHOW`|`false`|Set to true if you wish to show the pyenv segment even if the current Python version is the same as the global Python version|