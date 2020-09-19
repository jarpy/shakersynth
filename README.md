## Shakersynth

Shakersynth is an alternative approach to driving tactile transducers (aka.
bass shakers) from DCS World. It uses parametric real-time audio synthesis,
provided by [pyo], enabling it to create sounds that are dynamically derived
from DCS telemetry data.

The canonical use-case is helicopter rotor vibrations. Unlike with pre-recorded
samples, Shakersynth continuously adjusts multiple properties of the vibration
to match the rotor in the simulator, so you can feel each blade as it passes
overhead.

### Demo
Play these videos through your bass shakers to (literally) get a feel for what
Shakersynth can do.

  - [UH-1H Demo Video](https://youtu.be/CfWt1DQw7VE)
  - [Mi-8 Demo Video](https://youtu.be/9qU_9t4jrcw)

### Development Status

Currently, Shakersynth provides _only_ rotor vibrations for the Mi-8 and
UH-1H. It's best to run it alongside SimShaker Sound Module, which does a good
job of handling a wide range of effects that don't benefit so much from the
real-time synthesis approach.

Over time, Shakersynth could support more effects and more aircraft, but the
initial priority was to get a really good rotor effect for the Huey and the
Mi-8.

### Trying it out

Shakersynth is a basic, text-mode application with no GUI. Getting it running
is a little bit fiddly. Sorry about that.

1. Install [Python 3]<br>
   :point_right: Be sure to select options to add Python to the `PATH` environment variable.
2. Open PowerShell and run:
   ```powershell
   pip install shakersynth
   ```
3. Save [Shakersynth.lua] to the folder:
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
5. Back in PowerShell, run:
   ```
   shakersynth
   ```
6. Shakersynth will show a list of audio outputs. Find the number that
   corresponds to your bass shaker interface and enter that number at the
   prompt.
7. Run DCS.

### Upgrading to a new version
1. Open PowerShell and run:
   ```powershell
   pip install --upgrade shakersynth
   ```
2. Save the latest version of [Shakersynth.lua] to the folder:
   ```
   %UserProfile%\Saved Games\DCS\Scripts
   ```

[pyo]: https://pypi.org/project/pyo/
[Python 3]: https://www.python.org/downloads/windows/
[Shakersynth.lua]: https://raw.githubusercontent.com/jarpy/shakersynth/main/Shakersynth.lua
