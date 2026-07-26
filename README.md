# Duddy's Crash Coarse in Rocketry

A public, open-source graduate-to-research rocketry tutorial built around derivation, numerical modeling, verification, validation, uncertainty, primary-source traceability, and expert technical defense.

> The word **Coarse** is intentional and preserves the requested project name.

## What Is Included

- 14 coupled technical modules, from mission architecture through reusable landing
- 84 research seminars with more than 43,000 words of instruction
- 14 interactive mission-analysis laboratories
- 56 governing equations with explicit validity boundaries
- System text-to-speech with Play, Pause, Resume, Stop, voice, speed, and per-section playback
- Search across modules and seminars
- An independent expert-review workspace prepared for John Eichner or another qualified reviewer
- Weighted technical scoring, local autosave, and portable JSON review export
- A first-line funding brief with milestone-based validation gates
- Direct links to NASA, NASA NTRS, NASA Software Catalog, NASA directives, and current eCFR primary sources

## Important Scope and Safety Notice

This project is independent. It is **not affiliated with, sponsored by, or endorsed by NASA, FAA, JPL, any launch provider, or any referenced organization**.

The software is educational screening software. It is not flight software, certified engineering analysis, regulatory guidance, range-safety software, or an operational launch tool. Do not use it to design, manufacture, test, license, launch, or operate real aerospace hardware.

## Download

### Option 1: Git Clone

```bash
git clone https://github.com/JohnDuddy/Duddys-Crash-Coarse-in-Rocketry.git
cd Duddys-Crash-Coarse-in-Rocketry
```

### Option 2: GitHub ZIP

1. Open [the public GitHub repository](https://github.com/JohnDuddy/Duddys-Crash-Coarse-in-Rocketry).
2. Select **Code**.
3. Select **Download ZIP**.
4. Extract the ZIP and open a terminal in the extracted folder.

## Run on Windows

Python 3.10 or later is recommended.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Then open <http://127.0.0.1:5080/>.

On the original development computer, double-click `start.bat` or the Desktop shortcut named **Duddy's Crash Coarse in Rocketry**.

## Run on macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Then open <http://127.0.0.1:5080/>.

## Run the Tests

```bash
python -m unittest discover -s tests -v
```

The `/health` route also reports curriculum integrity:

```text
http://127.0.0.1:5080/health
```

## Expert Evaluation

Open `/review` in the running application. The reviewer should:

1. Record the exact Git commit or release tag evaluated.
2. Inspect representative modules in every major discipline.
3. Exercise all 14 laboratories and challenge their conservation laws and limiting behavior.
4. Score only demonstrated evidence.
5. Record blocking technical defects and required corrective actions.
6. Export the review JSON and attach it to a GitHub issue or release record.

The prefilled reviewer name does not imply that John Eichner has reviewed or endorsed the project.

## Project Structure

```text
app.py                    Flask routes and health reporting
rocket_curriculum.py      Fourteen-module curriculum and seminar generator
rocket_sources.py         Authoritative primary-source registry
templates/                Application pages
static/css/app.css        Responsive mission-control visual system
static/js/simulators.js   Fourteen interactive screening laboratories
static/js/lecture-player.js
static/js/review.js
tests/                    Curriculum and route regression tests
REVIEW_PROTOCOL.md        Independent technical-review procedure
FUNDING_BRIEF.md          Milestone-based first-line funding case
```

## Primary References

The application provides direct links and publication metadata for all references. Core sources include:

- NASA Systems Engineering Handbook, Revision 2
- NASA SP-125, *Design of Liquid Propellant Rocket Engines*
- NASA Glenn thrust, nozzle, specific-impulse, and ideal-rocket-equation references
- NASA Chemical Equilibrium with Applications (CEA)
- NASA trajectory design, Copernicus, GN&C, cislunar astrodynamics, materials, thermal, TPS, and test references
- 14 CFR Part 450 launch and reentry license requirements
- NASA software engineering requirements and the Columbia Accident Investigation Board report

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md). Technical changes should include a primary-source basis, validity limits, tests, and an explanation of how the change affects the educational or review claim.

## License

MIT. See [LICENSE](LICENSE).
