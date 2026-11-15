#!/usr/bin/env python3
"""Generate README.md and assets/dashboard.svg from stats.tsv."""
import csv
import html
import urllib.parse as U
from pathlib import Path

ROOT = Path(__file__).resolve().parent
AS = "2026-11-15"
ACTIVE_SINCE = "2026-10-16"
UNMAINTAINED_BEFORE = "2025-11-15"

S = {
    r[0]: dict(stars=int(r[1]), forks=int(r[2]), lic=r[3], lang=r[4], push=r[5])
    for r in csv.reader((ROOT / "stats.tsv").open(), delimiter="\t")
}

LIC_OVERRIDE = {
    "OpenSpace/OpenSpace": "MIT",
    "nasa/trick": "NOSA-1.3",
    "DOI-USGS/ISIS3": "CC0-1.0",
    "nasa/AmesGCM": "NOSA-1.3",
}
ARCHIVED = {"poliastro/poliastro"}
LICNAME = {"NOASSERTION": "Undeclared", "none": "Undeclared"}

C = [
    (
        "Mars trajectory and mission design",
        "Tools for Earth–Mars transfers, ephemerides and trajectory optimisation. Porkchop plots can be produced with poliastro (archived) and with Lambert solvers such as pykep and LambertHub.",
        [
            ("ANISE", "nyx-space/anise", "Rust toolkit for SPICE-style trajectory, orientation and ephemeris work, including Mars tours."),
            ("GMAT", "nasa/GMAT", "NASA's General Mission Analysis Tool for spacecraft trajectory design and optimisation, including Mars transfers."),
            ("LambertHub", "jorgepiloto/lamberthub", "Collection of Lambert-problem solvers used to compute interplanetary transfer legs."),
            ("Nyx", "nyx-space/nyx", "High-fidelity astrodynamics and mission-design toolkit written in Rust."),
            ("pagmo", "esa/pagmo2", "ESA's platform for massively parallel optimisation, often used for trajectory problems."),
            ("poliastro", "poliastro/poliastro", "Python astrodynamics library with porkchop-plot helpers. Archived (last push 2023-10-14)."),
            ("pykep", "esa/pykep", "ESA toolkit for interplanetary trajectory design, including Lambert and porkchop-style analyses."),
            ("SpiceyPy", "AndrewAnnex/SpiceyPy", "Pythonic wrapper for NASA's SPICE toolkit, used with official Mars ephemerides."),
            ("Tudat", "tudat-team/tudatpy", "TU Delft astrodynamics toolbox, with a Python interface around the C++ core."),
        ],
    ),
    (
        "EDL and landing simulation",
        "Open high-fidelity EDL codes used on flown Mars landers are scarce. The entries below are public research or multi-mission simulators that can model atmospheric flight, entry or landing. JPL's DSENDS is not included because it is not a public source repository.",
        [
            ("42", "ericstoneking/42", "General-purpose spacecraft attitude and orbit simulation, including atmospheric flight cases. No licence file was present at the repository HEAD on 2026-11-15."),
            ("Basilisk", "AVSLab/basilisk", "Modular astrodynamics and spacecraft simulation framework that can model atmospheric flight and landing scenarios."),
            ("EDL-Py", "CDNoyes/EDL-Py", "Research-grade entry, descent and landing software in Python. Unmaintained (last push 2023-12-01)."),
            ("Trick", "nasa/trick", "NASA simulation framework used for flight-software testbeds, including landing problems. Licensed under the NASA Open Source Agreement 1.3, which is not OSI-approved."),
        ],
    ),
    (
        "Rover and flight software",
        "Flight frameworks flown or used around Mars, plus public rover stacks. F Prime is the framework flown on Ingenuity; the helicopter's complete flight image is not a separate public repository.",
        [
            ("cFS", "nasa/cFS", "NASA Core Flight System, a reusable flight software framework used across many missions."),
            ("F Prime", "nasa/fprime", "NASA flight software and embedded systems framework, flown on the Ingenuity Mars helicopter."),
            ("Kalman", "agh-space-systems-rover/kalman_robot", "ROS 2 software stack for AGH Space Systems' planetary rover."),
            ("M2020 URDF models", "nasa-jpl/m2020-urdf-models", "Perseverance and Ingenuity URDF models used for operations visualisation. Unmaintained (last push 2023-06-07); no licence file was confirmed at the repository HEAD on 2026-11-15."),
            ("Open Source Rover", "nasa-jpl/open-source-rover", "JPL build-it-yourself six-wheel rover, modelled on Mars rover mobility, with open hardware instructions."),
            ("OSR Android app", "nasa-jpl/osr-android-app", "Android controller for the JPL Open Source Rover. Unmaintained (last push 2023-09-24)."),
            ("OSR rover code", "nasa-jpl/osr-rover-code", "Software that runs on the JPL Open Source Rover."),
            ("Space ROS", "space-ros/space-ros", "Meta operating system for space robotics, based on ROS 2. No licence file was detected by GitHub on 2026-11-15."),
            ("Space ROS demos", "space-ros/demos", "Example Space ROS applications and robot demonstrations."),
        ],
    ),
    (
        "Mars imagery and data",
        "Tools for PDS products, HiRISE and CTX processing, stereo terrain, and public rover raw images. NASA Mars Trek is a public web map rather than a public application repository, so it is cited here as a data service only: https://trek.nasa.gov/. The official PDS Search API client is released on PyPI; its GitHub repository holds generators rather than the installed library, so it is not listed as a separate entry.",
        [
            ("ALE", "DOI-USGS/ale", "USGS Abstraction Layer for Ephemerides, used to load camera geometry for planetary image processing. GitHub did not detect a standard SPDX licence."),
            ("Ames Stereo Pipeline", "NeoGeographyToolkit/StereoPipeline", "NASA Ames suite for automated stereogrammetry and digital terrain models from orbital and landed planetary imagery, including Mars."),
            ("ISIS3", "DOI-USGS/ISIS3", "USGS Integrated Software for Imagers and Spectrometers, the standard toolkit for HiRISE, CTX and other planetary mission imagery. Dedicated to the public domain under CC0 1.0."),
            ("Mars Raw Utils", "MarsRaw/mars-raw-utils", "Utilities that fetch and best-effort calibrate publicly posted raw images from Curiosity and Perseverance."),
            ("MMGIS", "NASA-AMMOS/MMGIS", "NASA AMMOS web-based geographic information system for planetary mapping, science planning and operations."),
            ("PDS Transform", "NASA-PDS/transform", "Official NASA PDS tool that converts PDS3 and PDS4 labels and data into other formats."),
            ("PDS Validate", "NASA-PDS/validate", "Official NASA PDS validator for PDS4 product labels, data and PDS3 volumes."),
            ("PRo3D", "pro3d-space/PRo3D", "Interactive 3D viewer for high-resolution reconstructions of planetary surfaces, including Mars rover workspaces."),
        ],
    ),
    (
        "Atmosphere and climate models",
        "Open Mars climate models and analysis tools. The LMD Mars Climate Database is widely used but is distributed under its own access terms rather than as a public application repository, so it is not listed as a software entry.",
        [
            ("AmesCAP", "NASA-Planetary-Science/AmesCAP", "Analysis pipeline for NASA Ames Mars GCM output, including helpers that can ingest other Mars model formats."),
            ("Ames GCM", "nasa/AmesGCM", "Current NASA Ames Mars Global Climate Model. Licensed under the NASA Open Source Agreement 1.3, which is not OSI-approved."),
            ("Legacy Ames GCM", "nasa/legacy-mars-global-climate-model", "End-of-life public release of the earlier NASA Ames Mars GCM. Unmaintained (last push 2023-04-12); no licence file was confirmed at the repository HEAD on 2026-11-15."),
            ("Planetary Code Collection", "nschorgh/Planetary-Code-Collection", "Thermal, ice-evolution and exosphere models for planetary surfaces, including Mars. No licence file was confirmed at the repository HEAD on 2026-11-15."),
        ],
    ),
    (
        "ISRU and life support",
        "Open habitat and ECLSS simulators that can be used in Mars settlement studies. No well-maintained public repository for MOXIE flight or plant software was verified for this list.",
        [
            ("BioSim", "scottbell/biosim", "Integrated advanced life-support simulator, originally developed at NASA Johnson Space Center, with a documented REST interface."),
        ],
    ),
    (
        "Settlement planning",
        "Only verified public repositories are listed. Concept sketches and unofficial city plans without a maintained open-source codebase are omitted.",
        [
            ("Mars Simulation Project", "mars-sim/mars-sim", "Detailed Java simulation of early human settlements on Mars, covering people, resources, vehicles and weather."),
        ],
    ),
    (
        "Games and education",
        "Open-source educational maps, models and simulators that feature Mars. Commercial Mars games are omitted.",
        [
            ("Celestia", "CelestiaProject/Celestia", "Real-time 3D space simulation that includes navigable models of Mars and its satellites."),
            ("Mars Geology Atlas", "eleanorlutz/mars_geology_atlas_of_space", "Code and instructions for making a geologic map of Mars. Unmaintained (last push 2022-11-28)."),
            ("NASA 3D Resources", "nasa/NASA-3D-Resources", "Collection of NASA 3D models, textures and images, including Mars mission hardware. Unmaintained (last push 2025-06-03); no licence file was confirmed at the repository HEAD on 2026-11-15."),
            ("OpenSpace", "OpenSpace/OpenSpace", "Interactive data visualisation software for the known universe, used in planetariums and research, including Mars datasets."),
        ],
    ),
]

# Official plan citations. Targets are GOAL; the existence of a dated document can be described in the claim.
PLANS = [
    (
        "GOAL",
        "NASA's Moon to Mars Architecture is an evolving blueprint for crewed deep-space exploration. It currently comprises four segments: Human Lunar Return, Foundational Exploration, Sustained Lunar Evolution, and Humans to Mars. It is not a flight manifest or a set of fixed landing dates.",
        "NASA Moon to Mars Architecture; Architecture Components",
        "Cited 2026-11-15",
        "https://www.nasa.gov/moontomarsarchitecture/",
    ),
    (
        "GOAL",
        "Architecture Definition Document ESDMD-001 Revision C records the 2025 Architecture Concept Review, including added Mars use cases and functions. The revision was released on 12 December 2025. Calendar crew-landing dates are not treated as facts in this list.",
        "NASA ADD Rev C (ESDMD-001) and the Architecture Definition Documents page",
        "Released 2025-12-12",
        "https://www.nasa.gov/moontomarsarchitecture-architecturedefinitiondocuments/",
    ),
    (
        "GOAL",
        "SpaceX states that Starship cargo flights to the Martian surface for research, development and exploratory missions start no earlier than 2028. That is a published target, not a recorded result.",
        "SpaceX Mission: Mars",
        "Page fetched 2026-11-15",
        "https://www.spacex.com/mars/",
    ),
    (
        "GOAL",
        "SpaceX describes a long-term aim of a self-sufficient city on Mars, with crew and cargo moved during transfer windows that open about every 26 months. This list does not treat population or cargo totals as measured facts, and it does not repeat cost figures.",
        "SpaceX Mission: Mars",
        "Page fetched 2026-11-15",
        "https://www.spacex.com/mars/",
    ),
    (
        "GOAL",
        "On 28 May 2025 SpaceX published a Starship talk titled Mars 2026, in which the company presents plans to make life multiplanetary. Specific unofficial retellings of that talk are not cited here.",
        "SpaceX Starship Talks: Mars 2026",
        "Talk dated 2025-05-28; page fetched 2026-11-15",
        "https://www.spacex.com/content/starship-talks/mars-2026",
    ),
]


def k(n):
    if n >= 1e6:
        return f"{n/1e6:.2f}M"
    if n >= 1000:
        return f"{n/1000:.1f}k"
    return str(n)


def anchor(n):
    return n.lower().replace(",", "").replace(" ", "-").replace("/", "").replace("&", "")


def lic_of(repo):
    if repo in LIC_OVERRIDE:
        return LIC_OVERRIDE[repo]
    raw = S[repo]["lic"]
    return LICNAME.get(raw, raw)


def badge(tag):
    styles = {
        "FACT": "border:2px solid #0284c7;color:#0284c7;",
        "GOAL": "border:2px dashed #d97706;color:#d97706;",
        "ESTIMATE": "border:2px dotted #7c3aed;color:#7c3aed;",
    }
    return (
        f'<span style="display:inline-block;{styles[tag]}padding:0 7px;'
        f'border-radius:4px;font-weight:700;">{tag}</span>'
    )


def write_dashboard_svg(path, *, top, cat_stars, n_tools, n_cat, tot, forks, active, n_gh, langs):
    W, H = 880, 620
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="ui-sans-serif, system-ui, sans-serif">',
        f'<rect width="{W}" height="{H}" fill="#1a0a08"/>',
        '<text x="24" y="36" fill="#fde68a" font-size="20" font-weight="700">Evidence dashboard</text>',
        f'<text x="24" y="58" fill="#fbcfe8" font-size="12">Snapshot {AS}. Solid = FACT, dashed = GOAL, dotted = ESTIMATE.</text>',
        '<rect x="620" y="20" width="14" height="10" fill="#38bdf8" stroke="#38bdf8"/>',
        '<text x="640" y="30" fill="#e2e8f0" font-size="11">FACT</text>',
        '<rect x="690" y="20" width="22" height="10" fill="none" stroke="#f59e0b" stroke-width="2" stroke-dasharray="6 4"/>',
        '<text x="718" y="30" fill="#e2e8f0" font-size="11">GOAL</text>',
        '<rect x="770" y="20" width="22" height="10" fill="none" stroke="#a78bfa" stroke-width="2" stroke-dasharray="2 3"/>',
        '<text x="798" y="30" fill="#e2e8f0" font-size="11">ESTIMATE</text>',
        '<text x="24" y="92" fill="#e2e8f0" font-size="14" font-weight="700">Top projects by GitHub stars (FACT)</text>',
    ]
    mx = top[0][1] if top else 1
    y = 106
    bar_x, bar_w = 200, 220
    for name, stars in top:
        bw = max(2, int(stars / mx * bar_w))
        parts.append(f'<text x="24" y="{y+11}" fill="#fecaca" font-size="11">{html.escape(name)}</text>')
        parts.append(
            f'<rect x="{bar_x}" y="{y}" width="{bw}" height="14" fill="#38bdf8" stroke="#0284c7" stroke-width="1"/>'
        )
        parts.append(f'<text x="{bar_x+bw+8}" y="{y+11}" fill="#fde68a" font-size="11">{k(stars)}</text>')
        y += 22

    parts.append('<text x="470" y="92" fill="#e2e8f0" font-size="14" font-weight="700">Combined stars by category (ESTIMATE)</text>')
    cmax = max((s for _, s in cat_stars), default=1) or 1
    y = 106
    bar_x, bar_w = 690, 110
    for name, stars in cat_stars:
        bw = max(2, int(stars / cmax * bar_w)) if stars else 0
        label = name if len(name) <= 28 else name[:26] + "…"
        parts.append(f'<text x="470" y="{y+11}" fill="#fecaca" font-size="11">{html.escape(label)}</text>')
        if bw:
            parts.append(
                f'<rect x="{bar_x}" y="{y}" width="{bw}" height="14" fill="none" stroke="#a78bfa" stroke-width="2" stroke-dasharray="2 3"/>'
            )
        parts.append(f'<text x="{bar_x+max(bw,2)+8}" y="{y+11}" fill="#ddd6fe" font-size="11">{k(stars)}</text>')
        y += 26

    by = 490

    def card(x, title, value, tag, stroke, dash):
        parts.append(
            f'<rect x="{x}" y="{by}" width="200" height="110" rx="8" fill="#2a100c" stroke="{stroke}" stroke-width="2" stroke-dasharray="{dash}"/>'
        )
        parts.append(f'<text x="{x+14}" y="{by+24}" fill="{stroke}" font-size="11" font-weight="700">{tag}</text>')
        parts.append(f'<text x="{x+14}" y="{by+62}" fill="#f8fafc" font-size="26" font-weight="700">{html.escape(str(value))}</text>')
        parts.append(f'<text x="{x+14}" y="{by+86}" fill="#fbcfe8" font-size="12">{html.escape(title)}</text>')

    card(24, "combined GitHub stars", k(tot), "ESTIMATE", "#a78bfa", "2 3")
    card(236, "listed projects", n_tools, "ESTIMATE", "#a78bfa", "2 3")
    card(448, f"repos pushed since {ACTIVE_SINCE}", f"{active}/{n_gh}", "ESTIMATE", "#a78bfa", "2 3")
    card(660, "official plan rows (all GOAL)", str(len(PLANS)), "GOAL", "#f59e0b", "6 4")
    parts.append("</svg>")
    path.write_text("".join(parts))


def emit():
    tools = [(n, r, d) for _, _, ts in C for (n, r, d) in ts]
    missing = [t[1] for t in tools if t[1] not in S]
    if missing:
        raise SystemExit(f"missing stats for: {missing}")

    tot = sum(S[t[1]]["stars"] for t in tools)
    forks = sum(S[t[1]]["forks"] for t in tools)
    langs = sorted({S[t[1]]["lang"] for t in tools if S[t[1]]["lang"] not in ("", "none")})
    active = sum(1 for t in tools if S[t[1]]["push"] >= ACTIVE_SINCE)
    unmaintained = [t for t in tools if S[t[1]]["push"] < UNMAINTAINED_BEFORE]
    archived = [t for t in tools if t[1] in ARCHIVED]

    cat_stars = [(heading, sum(S[t[1]]["stars"] for t in ts)) for heading, _, ts in C]
    top = sorted(((t[0], S[t[1]]["stars"]) for t in tools), key=lambda x: -x[1])[:10]

    write_dashboard_svg(
        ROOT / "assets" / "dashboard.svg",
        top=top,
        cat_stars=cat_stars,
        n_tools=len(tools),
        n_cat=len(C),
        tot=tot,
        forks=forks,
        active=active,
        n_gh=len(tools),
        langs=langs,
    )

    o = []
    o.append(
        f"""<div align="center">

# Awesome Craft Mars [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> A curated list of open-source tools and open data for Mars missions and settlement planning.

<img src="assets/craft-mars.svg" alt="Pixel-art Mars surface with habitat domes, a generic six-wheel rover and a rust-coloured sky" width="100%">

![Tools](https://img.shields.io/badge/tools-{len(tools)}-6366f1?style=for-the-badge)
[![Categories](https://img.shields.io/badge/categories-{len(C)}-0ea5e9?style=for-the-badge)](#contents)
![Combined stars](https://img.shields.io/badge/combined_stars-{k(tot)}-f59e0b?style=for-the-badge)
[![Stars](https://img.shields.io/github/stars/EdisonTKPcom/Awesome-Craft-Mars?style=for-the-badge&color=22c55e)](https://github.com/EdisonTKPcom/Awesome-Craft-Mars/stargazers)
[![Last commit](https://img.shields.io/github/last-commit/EdisonTKPcom/Awesome-Craft-Mars?style=for-the-badge&color=ec4899)](https://github.com/EdisonTKPcom/Awesome-Craft-Mars/commits/main)

</div>

Open-source software for getting to Mars, landing, driving rovers, reading imagery and thinking through settlement. Every project has a public repository that was checked on {AS}. Figures on the dashboard are tagged FACT (measured, with a cited source and date), GOAL (a stated plan, not a result) or ESTIMATE (a sum or count computed here). NASA and SpaceX roadmaps in the Plans table are GOAL. This list does not present target dates as facts, does not include unverified cost claims, and the pixel banner is an original scene without company logos or wordmarks.

Related lists: [Awesome Craft](https://github.com/EdisonTKPcom/Awesome-Craft), a family of curated open-source lists, and [Awesome Craft Space](https://github.com/EdisonTKPcom/Awesome-Craft-Space), open-source tools for spaceflight and rockets.

## Contents
"""
    )
    o += ["- [Dashboard](#dashboard)"] + [f"- [{n}](#{anchor(n)})" for n, _, _ in C] + ["- [Plans](#plans)"]
    o.append("\n## Dashboard\n")
    o.append(
        f"""<table>
<tr>
<td align="center"><h2>{len(tools)}</h2>{badge("ESTIMATE")} listed projects</td>
<td align="center"><h2>{len(C)}</h2>{badge("ESTIMATE")} software categories</td>
<td align="center"><h2>{k(tot)}</h2>{badge("ESTIMATE")} combined GitHub stars</td>
<td align="center"><h2>{k(forks)}</h2>{badge("ESTIMATE")} combined GitHub forks</td>
<td align="center"><h2>{active}/{len(tools)}</h2>{badge("ESTIMATE")} repos pushed in the last 30 days</td>
<td align="center"><h2>{len(langs)}</h2>{badge("ESTIMATE")} languages among GitHub repos</td>
</tr>
</table>

<img src="assets/dashboard.svg" alt="Evidence dashboard: FACT star counts, ESTIMATE category totals and GOAL plan-row count" width="100%">

### How the figures are tagged

<table>
<tr><th>Tag</th><th>Claim</th></tr>
<tr><td>{badge("FACT")}</td><td>Individual GitHub star, fork and last-push values come from the GitHub API, snapshot {AS}, stored in stats.tsv.</td></tr>
<tr><td>{badge("ESTIMATE")}</td><td>Combined GitHub stars ({k(tot)}, or {tot:,}) are the arithmetic sum of stargazers_count for the {len(tools)} GitHub-hosted entries in this list.</td></tr>
<tr><td>{badge("ESTIMATE")}</td><td>Combined forks ({k(forks)}), unique languages ({len(langs)}) and the {active}/{len(tools)} repos pushed on or after {ACTIVE_SINCE} are counts computed from that same snapshot.</td></tr>
<tr><td>{badge("GOAL")}</td><td>Every row in the Plans table is a stated architecture or timeline, cited from an official NASA or SpaceX page, not a measured outcome.</td></tr>
</table>

Announced landing windows, city scales and architecture segments are GOAL. This list does not invent unofficial dates or cost figures.

### Leaderboard

Individual star counts below are FACT values from the {AS} GitHub API snapshot.

<table>
<tr><th>Rank</th><th>Project</th><th align="right">Stars</th><th></th></tr>
"""
    )
    mx = top[0][1]
    for i, (name, stars) in enumerate(top, 1):
        bar = "█" * max(1, round(stars / mx * 20))
        medal = ["🥇", "🥈", "🥉"][i - 1] if i < 4 else i
        o.append(
            f'<tr><td align="center">{medal}</td><td><b>{html.escape(name)}</b></td>'
            f'<td align="right">{k(stars)}</td><td><code>{bar}</code></td></tr>'
        )
    o.append("</table>\n")

    lc = {}
    for t in tools:
        L = lic_of(t[1])
        lc[L] = lc.get(L, 0) + 1
    o.append("### Licences\n")
    o.append(
        " ".join(
            f"![{U.quote(L, safe='')}](https://img.shields.io/badge/{U.quote(L.replace('-', '--'))}-{c}-64748b?style=flat-square)"
            for L, c in sorted(lc.items(), key=lambda x: -x[1])
        )
    )
    o.append("")
    o.append(
        "Licence badges use the project's SPDX identifier when GitHub detects one, or the text of the licence file when that identifier is missing. "
        '"Undeclared" means no licence file was confirmed at the repository HEAD on the snapshot date. '
        "The NASA Open Source Agreement 1.3 is not OSI-approved; read it before you use those projects. "
        "ISIS3 is dedicated to the public domain under CC0 1.0. Archived and unmaintained projects stay in the star sum and are flagged in their entries.\n"
    )
    o.append("### Sources\n")
    o.append(
        f"""<table>
<tr><th>Source</th><th>What it supports</th></tr>
<tr><td>GitHub API, snapshot {AS} (Asia/Kuala_Lumpur calendar date), stored in <code>stats.tsv</code></td><td>stargazers_count, forks_count, license, language and pushed_at for {len(tools)} repositories.</td></tr>
<tr><td>Project licence files read on 2026-11-15</td><td>ISIS3 CC0-1.0, OpenSpace MIT, Trick and Ames GCM NASA Open Source Agreement 1.3.</td></tr>
<tr><td>NASA Moon to Mars Architecture pages and ADD Rev C, fetched 2026-11-15</td><td>Plans table rows tagged GOAL.</td></tr>
<tr><td>SpaceX Mission: Mars and Starship Talks pages, fetched 2026-11-15</td><td>Plans table rows tagged GOAL. Cost figures on those pages are omitted.</td></tr>
</table>
"""
    )

    for heading, intro, ts in C:
        o.append(f"## {heading}\n")
        if intro:
            o.append(intro + "\n")
        for t in sorted(ts, key=lambda t: t[0].lower()):
            name, repo, desc = t
            o.append(
                f"- [{name}](https://github.com/{repo}) - {desc} "
                f"![Stars](https://img.shields.io/github/stars/{repo}?style=flat-square&label=%E2%AD%90)"
            )
        o.append("")

    o.append("## Plans\n")
    o.append(
        "Official architecture and timeline statements. Every row is tagged GOAL. "
        "A published target is not a result. This table does not include unverified cost figures, "
        "and it does not treat unofficial interviews or secondary recaps as primary sources.\n"
    )
    o.append(
        "<table>\n<tr><th>Tag</th><th>Statement</th><th>Official source</th><th>Date</th></tr>"
    )
    # Link each official source once. First NASA architecture URL used in row 1;
    # ADD page in row 2; spacex.com/mars in row 3 only (row 4 same source, no second link);
    # talks page in row 5.
    linked = set()
    for tag, statement, source, date, url in PLANS:
        if url in linked:
            src_html = html.escape(source)
        else:
            src_html = f'<a href="{html.escape(url)}">{html.escape(source)}</a>'
            linked.add(url)
        o.append(
            "<tr>"
            f"<td>{badge(tag)}</td>"
            f"<td>{html.escape(statement)}</td>"
            f"<td>{src_html}</td>"
            f"<td>{html.escape(date)}</td>"
            "</tr>"
        )
    o.append("</table>\n")

    o.append(
        "## Contributing\n\nContributions welcome! Read the [contribution guidelines](contributing.md) first.\n\n"
        '<div align="center">\n\n'
        "If this list helped you, give it a ⭐ so others can find it.\n\n"
        "</div>\n"
    )
    (ROOT / "README.md").write_text("\n".join(o) + "\n")
    print(
        f"wrote README.md tools={len(tools)} stars={tot} forks={forks} "
        f"langs={len(langs)} active={active}/{len(tools)} "
        f"archived={len(archived)} unmaintained={len(unmaintained)} plans={len(PLANS)}"
    )
    for heading, _, ts in C:
        print(f"  {heading}: {len(ts)}")


if __name__ == "__main__":
    emit()
