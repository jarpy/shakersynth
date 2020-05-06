## Shakersynth

Shakersynth is an alternative approach to driving tactile transducers (aka. bass
shakers) from DCS World. Existing solutions use pre-recorded sound samples as
their audio source. Shakersynth uses parametric real-time audio synthesis,
provided by [pyo](https://pypi.org/project/pyo/), enabling it to create sounds
that are dynamically derived from DCS telemetry data.

A nice example is helicopter rotor vibrations. Unlike with a pre-recorded
sample, Shakersynth continuously adjusts multiple properties of the vibration to
match the rotor in the simulator, so you can feel each blade as it passes
overhead.

### Development Status: Pre-alpha

Currently, Shakersynth provides _only_ rotor vibrations for the Mi-8 and
UH-1H. It's best to run it alongside SimShaker Sound Module, which does a good
job of handling a wide range of effects that don't benefit so much from the
real-time synthesis approach.

Shakersynth currently uses SimShaker's Lua export data, which is full of great
stuff. It requires a modified copy of the Lua script from SimShaker. If you are
interested in trying Shakersynth at this early stage, get in touch with me
(Jarpy#3445 on Discord). I won't distribute the modified file. Soon, I'll
develop a dedicated `export.lua` for Shakersynth, making it a stand-alone system
ready for alpha release.
