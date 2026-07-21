// Dashboard render-critique runner (WI-189) — META-ONLY dev tooling.
//
// Regenerates PROJECT_STATE.html, then screenshots it across a DECLARED matrix
// (widths x themes x tabs) into a gitignored dir so an agent session can Read
// the PNGs and critique *rendered pixels*, not ~790 KB of source markup. The
// command sequence here is also the artifact recipe a future
// Verification=Critique TC on dashboard quality would name (PROCESS_OPTIONS.md,
// "Critique verification").
//
// NOT shipped downstream: the kit's stdlib-only / install-nothing posture
// governs project-trajectory/scripts, never this dev-only tool (owner ruling at
// WI-189 filing; same meta-only scoping as WI-175 Rec 3).
//
// Prereqs (see scripts/dashboard-shots/README.md + the render-dashboard-critique
// skill):  npm ci  &&  npx playwright install chromium   (pinned in package.json)
// Run:     node scripts/dashboard-shots/shoot.mjs
//
// Pins (recorded so shots stay comparable across sessions):
//   playwright 1.61.1  ·  chromium build 1228 (Chrome 149.0.7827.55)

import { chromium } from "playwright";
import { spawnSync } from "node:child_process";
import { existsSync, mkdirSync, rmSync, readdirSync } from "node:fs";
import { fileURLToPath, pathToFileURL } from "node:url";
import { dirname, join, resolve } from "node:path";

const HERE = dirname(fileURLToPath(import.meta.url));
const REPO = resolve(HERE, "..", ".."); // scripts/dashboard-shots -> repo root
const DASHBOARD = join(REPO, "PROJECT_STATE.html");
const OUT = join(HERE, "shots"); // gitignored

// --- The declared matrix (edit here, never improvise per session) ------------
// Widths span the responsive breakpoints the dashboard's grid/layout react to.
const WIDTHS = { narrow: 390, laptop: 1280, wide: 1680 };
// Themes drive `prefers-color-scheme`; the dashboard is CSS-media-query themed,
// so emulating colorScheme is the whole toggle (no click needed).
const THEMES = ["light", "dark"];
// Every tab in nav.tabs (data-tab attributes), landing tab first.
const TABS = [
  ["arch", "What (SR breakdown)"],
  ["dag", "When (roadmap DAG)"],
  ["sw", "How (SW architecture)"],
  ["know", "Knowledge (OKF)"],
  ["process", "Process"],
];
// Full-page for every cell; above-the-fold (viewport clip) only for the landing
// tab, where "what you see first" is the critique that matters most.
const LANDING = "arch";
const SCALE = 2; // retina — legible text for an agent reading the PNG back

function pythonExe() {
  // Prefer the repo venv, which is a concrete path we can (and must) existence-
  // check; a bare PATH name can't be existsSync-vetted (it resolves at spawn),
  // so it is the final fallback, per platform.
  const venv =
    process.platform === "win32"
      ? join(REPO, ".venv", "Scripts", "python.exe")
      : join(REPO, ".venv", "bin", "python");
  if (existsSync(venv)) return venv;
  return process.platform === "win32" ? "python" : "python3";
}

function regenerateDashboard() {
  const py = pythonExe();
  const script = join(REPO, "project-trajectory", "scripts", "gen_trajectory.py");
  const r = spawnSync(py, [script], { cwd: REPO, encoding: "utf-8" });
  if (r.status !== 0) {
    console.error("gen_trajectory failed:\n" + (r.stderr || r.stdout || r.error));
    process.exit(1);
  }
  console.log((r.stdout || "").trim() || "gen_trajectory: (no output)");
}

async function main() {
  regenerateDashboard();
  if (!existsSync(DASHBOARD)) {
    console.error("no dashboard at " + DASHBOARD);
    process.exit(1);
  }
  // Fresh output dir so a run's shots are exactly the declared matrix.
  rmSync(OUT, { recursive: true, force: true });
  mkdirSync(OUT, { recursive: true });

  const url = pathToFileURL(DASHBOARD).href;
  const browser = await chromium.launch();
  const written = [];
  try {
    for (const theme of THEMES) {
      const context = await browser.newContext({
        colorScheme: theme,
        reducedMotion: "reduce",
        deviceScaleFactor: SCALE,
      });
      const page = await context.newPage();
      for (const [wname, w] of Object.entries(WIDTHS)) {
        await page.setViewportSize({ width: w, height: 900 });
        await page.goto(url, { waitUntil: "networkidle" });
        // Capture the landing fold before any click can scroll a narrow page to
        // bring an off-viewport tab button into view.
        const landingFold = join(OUT, `${w}px-${theme}-${LANDING}-fold.png`);
        await page.screenshot({ path: landingFold, fullPage: false });
        written.push(landingFold);
        for (const [tab, label] of TABS) {
          // The button's data-tab matches the panel's id; clicking it moves the
          // `active` class onto <section id="{tab}" class="panel active">.
          await page.click(`nav.tabs button[data-tab="${tab}"]`);
          await page.waitForSelector(`section#${tab}.panel.active`, {
            timeout: 5000,
          });
          const base = `${w}px-${theme}-${tab}`;
          const full = join(OUT, `${base}-full.png`);
          await page.screenshot({ path: full, fullPage: true });
          written.push(full);
        }
      }
      await context.close();
    }
  } finally {
    await browser.close();
  }

  console.log(`\nwrote ${written.length} screenshot(s) to ${OUT}`);
  for (const p of readdirSync(OUT).sort()) console.log("  " + join(OUT, p));
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
