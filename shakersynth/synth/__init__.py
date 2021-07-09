"""This module contains individual synthesizers for different effects.

A valid synth must take a module name as the sole argument to its constructor.
It must also implement the `update`, `start`, and `stop` methods.

`update` must accept a telemetry dictionary.
`start` and `stop` take no arguments.

Refer to `RotorSynth` for an example.
"""
