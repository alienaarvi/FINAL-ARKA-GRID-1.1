# ArkaGrid — Campus Energy Intelligence

Live campus energy simulation, a 3D digital twin and AI anomaly detection.
All data is synthetic and for demonstration only.

## Project layout

```
arkagrid/
├── index.html                    dashboard
├── style.css                     design system
├── app.js                        simulation, dispatch, forecast, anomaly UI
├── campus3d.js                   three.js digital twin
├── engine_a/anomaly_detection.py Isolation Forest engine + API + web server
├── data/campus_energy.csv        synthetic history (auto-generated)
├── package.json                  three.js dependency
├── requirements.txt              numpy, scikit-learn, pandas
├── server.py                     same engine at the repo root (used for hosting)
├── build_demo.py                 builds the single-file static demo
├── render.yaml / Procfile        hosting config
└── run.sh / run.bat              one-command launchers
```

## Quick start

One-command launch:

```bash
# macOS / Linux
chmod +x run.sh && ./run.sh

# Windows
run.bat
```

Or step by step (run in the project folder):

```bash
# 1. three.js for the 3D twin
npm install

# 2. Python dependencies (a virtual environment is recommended)
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. start the dashboard + API (one process, one port)
python engine_a/anomaly_detection.py --serve --open
```

Then open http://127.0.0.1:8000/ (the `--open` flag does it for you).

## Useful commands

| Command | What it does |
|---|---|
| `python engine_a/anomaly_detection.py` | Terminal report of historical anomalies, no server |
| `... --serve` | Dashboard + API on port 8000 |
| `... --serve --port 8080` | Use another port |
| `... --serve --host 0.0.0.0` | Allow other devices on your network |
| `... --regenerate` | Rebuild the synthetic dataset |
| `curl localhost:8000/api/health` | Check the engine is up |
| `curl localhost:8000/api/anomalies` | Raw JSON results |

## Demo it

1. Open the dashboard and let the simulation run (watch the clock and HUD).
2. Press **F** to inject a fault into the selected building.
3. Within ~5 seconds the building pulses red in the 3D twin and the event
   appears in the Anomaly Detection Monitor and in the terminal.
4. Try the dispatch modes (Balanced / Eco / Cost saver) in the Command Center.

## 3D campus controls

| Input | Action |
|---|---|
| Drag / scroll / click a building | Orbit, zoom, inspect (the camera flies to it) |
| `V` | Cycle camera: Isometric, Top-down, Cinematic, Energy hub |
| `C` | Guided tour through the buildings |
| `L` | **Energy lens**: dims the world so the power network glows |
| `B` | Toggle glow (bloom) effects |
| `H` | Hide / show labels |
| `F` | Inject a fault into the selected building |

The scene follows the simulation clock (sunrise, dusk, night, lit windows,
street lamps), shows weather from the simulated sky clearness, and animates
people and traffic. Glowing cables carry energy: solar and grid into the hub,
the hub out to every building (brightness and speed follow the live kW), and
battery charge/discharge in either direction.

## Deploy

**Option A - static demo (no Python engine), easiest.** Anomalies are detected in the
browser by the on-device detector.

```bash
python build_demo.py          # creates dist/arkagrid-demo.html (one self-contained file)
```

Rename it to `index.html`, put it in a folder, and upload that folder to any static
host (Netlify Drop, Cloudflare Pages, GitHub Pages, S3). three.js loads from a CDN.

**Option B - full version with the Python Isolation Forest engine.**

1. Put the project folder in a GitHub repository (`.gitignore` is included).
2. On https://render.com choose **New + > Blueprint** (it reads `render.yaml`), or
   **New + > Web Service** with:
   * Build command: `pip install -r requirements.txt`
   * Start command: `python engine_a/anomaly_detection.py --serve`
   * Health check path: `/api/health`
3. Open the `https://<your-service>.onrender.com` link when the deploy finishes.

Railway / Heroku also work (the included `Procfile` is picked up automatically).
The server reads the host's `PORT` variable and binds publicly by itself.

Notes: free tiers sleep when idle (the first visit can take about a minute), and on
the full version all visitors share one live anomaly feed.

## Troubleshooting

* **3D view shows a red message** - it explains the cause. three.js loads from
  `node_modules` if you ran `npm install`, otherwise from a CDN (needs internet).
  Fix: run `npm install`, then refresh.
* **3D view is slow** - press `B` to turn glow off; quality also lowers itself
  automatically on slow GPUs.

* **3D view stuck on "Initialising"** — run `npm install` (needs
  `node_modules/three`), then refresh. Open the browser console (F12) for errors.
* **"Engine offline" banner** — the dashboard still works in edge mode; start the
  server with the command above.
* **Port already in use** — add `--port 8001`.
* **`python` not found on Windows** — use `py` instead.
* Always open the site through the server (http://127.0.0.1:8000), not by
  double-clicking `index.html`; ES modules and the API need http.
