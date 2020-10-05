## Shakersynth

Shakersynth is an alternative approach to driving tactile transducers (aka.
bass shakers) from DCS World. It uses parametric real-time audio synthesis,
provided by [pyo], enabling it to create sounds that are dynamically derived
from DCS telemetry data.

The canonical use-case is helicopter rotor vibrations. Shakersynth continuously
adjusts multiple properties of the vibration to match the rotor in the simulator,
so you can feel each blade as it passes overhead.

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

### Configuration
When first run, Shakersynth creates a default configuration file at:
```
%LOCALAPPDATA%\Shakersynth\shakersynth.yml
```

On my system, that becomes:
```
C:\Users\jarpy\AppData\Local\Shakersynth\shakersynth.yml
```

Edit this file to set some important options like the sample rate, output volume
and frequency of the sound sent to the bass shakers.

If you delete the file, it will be recreated with the current defaults.

#### Configuration Options
| Option          | Default  | Description                         |
| --------------- | -------- | ----------------------------------- |
| `audio_api`     | `wasapi` | Not currently working!              |
| `sample_rate`   | `44100`  | Sample rate of the sound card.      |
| `buffer_size`   | `2048`   | Audio buffer size in samples.       |
| `global_volume` | `0.90`   | Output volume from `0.0` to `1.0`.  |
| `rotor_hz`      | `35.0`   | This frequency of the rotor effect. |

### Upgrading to a new version
1. Open PowerShell and run:
   ```powershell
   pip install --upgrade shakersynth
   ```
2. Save the latest version of [Shakersynth.lua] to the folder:
   ```
   %UserProfile%\Saved Games\DCS\Scripts
   ```
   :point_up: This step is only needed after a major version change, like
   `0.6.0` -> `1.0.0`.

[pyo]: https://pypi.org/project/pyo/
[Python 3]: https://www.python.org/downloads/windows/
[Shakersynth.lua]: https://raw.githubusercontent.com/jarpy/shakersynth/main/Shakersynth.lua
