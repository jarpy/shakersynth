## Shakersynth

Shakersynth is an alternative approach to driving tactile transducers (aka. bass
shakers) from DCS World. Existing solutions use pre-recorded sound samples as
their audio source. Shakersynth uses parametric real-time audio synthesis,
enabling it to create sounds that are dynamically derived from DCS telemetry
data.

A nice example is helicopter rotor vibrations. Unlike with a pre-recorded
sample, Shakersynth constantly adjusts the speed of the vibration to match
the rotor in the simulator, so you can feel each blade as it passes overhead.

Currently, Shakersynth provides _only_ rotor vibrations for the Mi-8 and UH-1H. It's best to run it alongside SimShaker Sound Module, which does a good job of handling a wide range of effects that don't benefit so much from the parametric approach.

Shakersynth currently uses SimShaker's Lua export data, which is full of great stuff. It requires a modified copy of the Lua script from SimShaker. If you are interested in trying Shakersynth, get in touch with me (Jarpy#3445 on Discord). I won't be posting the modified file here. Install SimShaker, and please support the authors of SimShaker and SimShaker Sound Module.
