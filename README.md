## Shakersynth

Shakersynth is an alternative approach to driving tactile transducers (aka. bass
shakers) from DCS World. Existing solutions use pre-recorded sound samples as
their audio source. Shakersynth uses parametric real-time audio synthesis,
provided by [pyo](https://pypi.org/project/pyo/), enabling it to create sounds
that are dynamically derived from DCS telemetry data.

A nice example is helicopter rotor vibrations. Unlike with pre-recorded samples,
Shakersynth continuously adjusts multiple properties of the vibration to match
the rotor in the simulator, so you can feel each blade as it passes overhead.

### Development Status: Pre-alpha

Currently, Shakersynth provides _only_ rotor vibrations for the Mi-8 and
UH-1H. It's best to run it alongside SimShaker Sound Module, which does a good
job of handling a wide range of effects that don't benefit so much from the
real-time synthesis approach.

Over time, Shakersynth should support more effects and more aircraft, but please
don't expect rapid development of this single-person hobby project. Of course,
this is free, open-source software, so if you'd like to contribute, then welcome
to Team Shakersynth!
