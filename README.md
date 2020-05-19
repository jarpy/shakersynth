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

### Trying it out

Shakersynth is a basic, text-mode application with no GUI. Getting it running is
a bit fiddly, sorry about that.

1. Install [Python 3](https://www.python.org/downloads/windows/).
2. Open PowerShell and run:
   ```powershell
   pip install shakersynth
   ```
3. Save [Shakersynth.lua][] to the folder:
   ```
   %UserProfile%\Saved Games\DCS\Scripts
   ```
4. Edit this file:
   ```
   %UserProfile%\Saved Games\DCS\Scripts\Export.lua
   ```
   adding this line:
   ```lua
   dofile(require('lfs').writedir()..'Scripts/Shakersynth.lua')
   ```
5. Back in PowerShell, run `python -m shakersynth`
6. Shakersynth will show a list of audio outputs. Identify the number that
   corresponds to your bass shaker interface and enter that number at the
   prompt.
7. Run DCS.

### Upgrading to a new version
1. Open PowerShell and run:
   ```powershell
   pip install --upgrade shakersynth
   ```
2. Save the latest version of [Shakersynth.lua][] to the folder:
   ```
   %UserProfile%\Saved Games\DCS\Scripts
   ```

[Shakersynth.lua]: https://raw.githubusercontent.com/jarpy/shakersynth/master/Shakersynth.lua
