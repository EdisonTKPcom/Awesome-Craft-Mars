#!/usr/bin/env python3
"""Fetch live GitHub repo stats. Unauthenticated, respects rate limits."""
import csv
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
UA = "Awesome-Craft-Mars-stats (https://github.com/EdisonTKPcom/Awesome-Craft-Mars)"
API = "https://api.github.com"
OUT = ROOT / "stats.tsv"

REPOS = [
    "nyx-space/anise",
    "nasa/GMAT",
    "jorgepiloto/lamberthub",
    "nyx-space/nyx",
    "esa/pagmo2",
    "poliastro/poliastro",
    "esa/pykep",
    "AndrewAnnex/SpiceyPy",
    "tudat-team/tudatpy",
    "ericstoneking/42",
    "AVSLab/basilisk",
    "CDNoyes/EDL-Py",
    "nasa/trick",
    "nasa/cFS",
    "nasa/fprime",
    "agh-space-systems-rover/kalman_robot",
    "nasa-jpl/m2020-urdf-models",
    "nasa-jpl/open-source-rover",
    "nasa-jpl/osr-android-app",
    "nasa-jpl/osr-rover-code",
    "space-ros/demos",
    "space-ros/space-ros",
    "DOI-USGS/ale",
    "DOI-USGS/ISIS3",
    "NeoGeographyToolkit/StereoPipeline",
    "NASA-AMMOS/MMGIS",
    "MarsRaw/mars-raw-utils",
    "pro3d-space/PRo3D",
    "NASA-PDS/transform",
    "NASA-PDS/validate",
    "NASA-Planetary-Science/AmesCAP",
    "nasa/AmesGCM",
    "nasa/legacy-mars-global-climate-model",
    "nschorgh/Planetary-Code-Collection",
    "scottbell/biosim",
    "mars-sim/mars-sim",
    "CelestiaProject/Celestia",
    "eleanorlutz/mars_geology_atlas_of_space",
    "nasa/NASA-3D-Resources",
    "OpenSpace/OpenSpace",
]


def api(url, attempt=0):
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": UA,
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as res:
            data = json.load(res)
            remaining = res.headers.get("X-RateLimit-Remaining")
            reset = res.headers.get("X-RateLimit-Reset")
            return res.status, data, remaining, reset
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        remaining = e.headers.get("X-RateLimit-Remaining")
        reset = e.headers.get("X-RateLimit-Reset")
        if e.code in (429, 403) and attempt < 8:
            wait = 30
            if reset:
                wait = max(5, int(reset) - int(time.time()) + 3)
            wait = max(wait, min(120, 5 * (2 ** attempt)))
            print(f"rate limited ({e.code}) on {url}, sleeping {wait}s", flush=True)
            time.sleep(wait)
            return api(url, attempt + 1)
        if e.code in (500, 502, 503, 504) and attempt < 5:
            wait = min(60, 2 ** attempt)
            print(f"server error {e.code} on {url}, retry in {wait}s", flush=True)
            time.sleep(wait)
            return api(url, attempt + 1)
        return e.code, body, remaining, reset


def wait_for_budget(need):
    status, data, remaining, reset = api(f"{API}/rate_limit")
    if status != 200:
        print(f"rate_limit check failed: {status} {data}", flush=True)
        sys.exit(1)
    core = data["resources"]["core"]
    rem, rst = int(core["remaining"]), int(core["reset"])
    print(f"rate limit remaining={rem} reset={rst} need={need}", flush=True)
    if rem < need:
        wait = max(5, rst - int(time.time()) + 5)
        print(f"waiting {wait}s for rate limit reset", flush=True)
        time.sleep(wait)
        wait_for_budget(need)


def main():
    wait_for_budget(len(REPOS) + 2)
    rows = []
    missing = []
    for repo in REPOS:
        status, data, remaining, reset = api(f"{API}/repos/{repo}")
        if status == 404:
            print(f"MISSING {repo}", flush=True)
            missing.append(repo)
            continue
        if status != 200 or not isinstance(data, dict):
            print(f"ERROR {repo}: {status} {data}", flush=True)
            missing.append(repo)
            continue
        full = data.get("full_name") or repo
        stars = data["stargazers_count"]
        forks = data["forks_count"]
        lic_info = data.get("license")
        lic = lic_info["spdx_id"] if lic_info and lic_info.get("spdx_id") else "none"
        lang = data.get("language") or "none"
        pushed = (data.get("pushed_at") or "")[:10]
        archived = data.get("archived", False)
        print(
            f"{full}\t{stars}\t{forks}\t{lic}\t{lang}\t{pushed}\tarchived={archived}\trequested={repo}\tremaining={remaining}",
            flush=True,
        )
        rows.append(
            {
                "requested": repo,
                "full": full,
                "stars": stars,
                "forks": forks,
                "lic": lic,
                "lang": lang,
                "pushed": pushed,
                "archived": archived,
            }
        )
        time.sleep(0.15)

    with OUT.open("w", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        for row in rows:
            w.writerow(
                [row["requested"], row["stars"], row["forks"], row["lic"], row["lang"], row["pushed"]]
            )
    print(f"\nwrote {OUT} ({len(rows)} rows, {len(missing)} missing: {missing})", flush=True)
    (ROOT / "stats.json").write_text(
        json.dumps({"rows": rows, "missing": missing}, indent=2) + "\n"
    )


if __name__ == "__main__":
    main()
