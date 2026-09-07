// Render an AR replay HTML page to a full-height PNG screenshot.
// Expands the inner .viewer div so the entire SERP is visible (no inner
// scroll), keeps sparkline tracks rendered below, takes a full-page
// screenshot, then auto-crops to non-empty content via Python.
//
// Usage:
//   node render_replay.js <trial_id> [--max-y N]
//   --max-y N: cap rendered SERP height to N px (e.g., farthest user fixation)
//
// Output: figs/fig4_replay_<trial>.full.png (uncropped),
//         figs/fig4_replay_<trial>.png (auto-cropped via PIL).

const path = require('path');
const fs = require('fs');
// Resolve playwright from NODE_PATH (or PLAYWRIGHT_PATH) rather than one
// hard-coded checkout; e.g. NODE_PATH=~/Documents/dev/session-cartographer/node_modules
const { chromium } = require(process.env.PLAYWRIGHT_PATH || 'playwright');

const args = process.argv.slice(2);
const trial = args[0];
if (!trial) {
    console.error('usage: node render_replay.js <trial_id> [--max-y N]');
    process.exit(2);
}
const maxYFlag = args.find(a => a.startsWith('--max-y='));
const maxY = maxYFlag ? parseInt(maxYFlag.split('=')[1]) : null;

const REPLAY = `file://${path.resolve(`/Users/andyed/Documents/dev/approach-retreat/site/replay/trials/${trial}.html`)}`;
const FIGS_DIR = path.resolve(__dirname);
const OUT_FULL = path.join(FIGS_DIR, `fig4_replay_${trial}.full.png`);

(async () => {
    if (!fs.existsSync(REPLAY.replace('file://', ''))) {
        console.error(`replay HTML not found: ${REPLAY}`);
        process.exit(1);
    }

    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({
        viewport: { width: 1300, height: 4000 },
        deviceScaleFactor: 2,  // for crisp text
    });
    const page = await context.newPage();
    await page.goto(REPLAY, { waitUntil: 'networkidle', timeout: 30000 });

    // Wait for sparkline canvases to draw; they fire on DOMContentLoaded but
    // some tracks render lazily (gaze series, AOI presence) and can take several
    // seconds on a tall SERP.
    await page.waitForTimeout(8000);

    // Read the SERP image's natural height + apply the max-y cap if given.
    const dims = await page.evaluate((capY) => {
        const img = document.getElementById('serp-img');
        if (!img) return null;
        const naturalHeight = img.naturalHeight * (img.clientWidth / img.naturalWidth);
        const renderH = capY != null ? Math.min(capY, naturalHeight) : naturalHeight;
        const viewer = document.querySelector('.viewer');
        if (viewer) {
            viewer.style.height = `${renderH}px`;
            viewer.style.maxHeight = 'none';
            viewer.style.overflow = 'hidden';
        }
        return { naturalHeight, renderH };
    }, maxY);
    if (!dims) {
        console.error('SERP image not found in replay');
        process.exit(1);
    }
    console.log(`SERP natural height: ${Math.round(dims.naturalHeight)}px, render: ${Math.round(dims.renderH)}px`);

    // Give the page time to reflow + repaint canvases at the new size.
    await page.waitForTimeout(3000);

    // Full-page screenshot — captures header, expanded SERP viewer, sparkline timeline, and info-panel.
    await page.screenshot({ path: OUT_FULL, fullPage: true });
    console.log(`wrote ${OUT_FULL}`);

    await browser.close();
})();
