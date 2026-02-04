# Annual Release Cadence for Sofia Core

**Applies to:** Sofia Core, EmeraldOrbit, Emerald Estates, EWF, and SEFAA

## Table of Contents

- [Overview](#-overview)
- [Badges](#-badges)
- [Release Types](#-release-types)
- [Annual Release Gantt Chart](#-annual-release-gantt-chart)
- [Visual Calendar Layout](#️-visual-calendar-layout)
- [Contributor Windows](#-contributor-windows)
- [Contributor Workflow Process](#-contributor-workflow-process)
- [Governance Sync Points](#-governance-sync-points)
- [Mermaid Timeline View](#-mermaid-timeline-view)
- [Release Intensity Heatmap](#-release-intensity-heatmap)
- [Purpose](#-purpose)
- [Quick Reference](#-quick-reference)

## 📅 Overview

This document defines the predictable annual rhythm for patch, minor, and major releases.

This cadence ensures:
- **Stability** — Consistent, reliable release patterns
- **Contributor clarity** — Predictable windows for contributions
- **Roadmap alignment** — Synchronized with architectural milestones
- **Unified‑field coherence** — Identity-preserving evolution
- **Zero‑surprise evolution** — Planned, ceremonial change management

All dates use a **Monday‑based cadence** for maximum contributor clarity.

---

## 🏷️ Badges

![Release Cadence](https://img.shields.io/badge/Releases-Weekly%20%7C%20Monthly%20%7C%20Quarterly-blue?style=flat-square)
![Version](https://img.shields.io/badge/version-1.0.2-green?style=flat-square)
![Contribution Status](https://img.shields.io/badge/contributions-welcome-brightgreen?style=flat-square)
![Governance](https://img.shields.io/badge/governance-unified%20field-purple?style=flat-square)

---

## 🔄 Release Types

### 1. Patch Releases — Weekly

**Schedule:** Every Monday

**Purpose:**
- Bug fixes
- Stability improvements
- Documentation updates
- Small internal refinements

This keeps the field clean and responsive without disrupting larger cycles.

### 2. Minor Releases — Monthly

**Schedule:** First Monday of every month

**Purpose:**
- New features
- New identity behaviors
- Non‑breaking enhancements
- Module‑level improvements

This gives contributors a predictable window to target.

### 3. Major Releases — Quarterly

**Schedule:** First Monday of January, April, July, October

**Purpose:**
- Breaking changes
- Structural shifts
- New identity layers
- Runtime redesigns
- Architectural evolution

This aligns with roadmap phases and ensures major changes land with ceremony and preparation.

### 4. Annual Meta‑Release — December

**Schedule:** Second Monday of December

**Purpose:**
- Year‑end consolidation
- Documentation harmonization
- Deprecations
- Long‑term roadmap reset
- Unified‑field alignment review

This is the "architectural audit" moment — the field's annual reset.

---

## 📊 Annual Release Gantt Chart

This Gantt chart visualizes the complete annual release schedule, showing the relationship between different release types and key windows throughout the year:

```mermaid
gantt
    title Sofia Core Annual Release Cadence Timeline
    dateFormat YYYY-MM-DD
    axisFormat %b
    
    section Q1 Releases
    Major Release Q1 (Jan 1st Mon)    :milestone, m1, 2026-01-05, 0d
    Minor Release (Feb 1st Mon)       :milestone, m2, 2026-02-02, 0d
    Minor Release (Mar 1st Mon)       :milestone, m3, 2026-03-02, 0d
    Q1 Freeze Window                  :crit, f1, 2026-03-23, 7d
    
    section Q2 Releases
    Major Release Q2 (Apr 1st Mon)    :milestone, m4, 2026-04-06, 0d
    Minor Release (May 1st Mon)       :milestone, m5, 2026-05-04, 0d
    Minor Release (Jun 1st Mon)       :milestone, m6, 2026-06-01, 0d
    Q2 Freeze Window                  :crit, f2, 2026-06-22, 7d
    
    section Q3 Releases
    Major Release Q3 (Jul 1st Mon)    :milestone, m7, 2026-07-06, 0d
    Minor Release (Aug 1st Mon)       :milestone, m8, 2026-08-03, 0d
    Minor Release (Sep 1st Mon)       :milestone, m9, 2026-09-07, 0d
    Q3 Freeze Window                  :crit, f3, 2026-09-21, 7d
    
    section Q4 Releases
    Major Release Q4 (Oct 1st Mon)    :milestone, m10, 2026-10-05, 0d
    Minor Release (Nov 1st Mon)       :milestone, m11, 2026-11-02, 0d
    Minor Release (Dec 1st Mon)       :milestone, m12, 2026-12-07, 0d
    Annual Meta-Release (Dec 2nd Mon) :milestone, meta, 2026-12-14, 0d
    Q4 Freeze Window                  :crit, f4, 2026-12-14, 14d
    
    section Weekly Cadence
    Patch Releases (Every Monday)     :active, patches, 2026-01-05, 360d
```

**Key Elements:**
- **Major Releases** (Milestones) — Quarterly on 1st Monday of Jan, Apr, Jul, Oct
- **Minor Releases** (Milestones) — Monthly on 1st Monday
- **Annual Meta‑Release** (Milestone) — 2nd Monday of December
- **Freeze Windows** (Red/Critical) — Last week of Q1-Q3, final 2 weeks of Q4
- **Patch Releases** (Active bar) — Continuous weekly rhythm every Monday

---

## 🗓️ Visual Calendar Layout

```
┌──────────────────────────────────────────────────────────────┐
│                        ANNUAL RELEASE MAP                     │
└──────────────────────────────────────────────────────────────┘

JANUARY
  ├─ Patch Releases: Every Monday
  ├─ Minor Release: 1st Monday
  └─ MAJOR RELEASE (Q1): 1st Monday

FEBRUARY
  ├─ Patch Releases: Every Monday
  └─ Minor Release: 1st Monday

MARCH
  ├─ Patch Releases: Every Monday
  ├─ Minor Release: 1st Monday
  └─ Freeze Window: Final week (Q1 end)

APRIL
  ├─ Patch Releases: Every Monday
  ├─ Minor Release: 1st Monday
  └─ MAJOR RELEASE (Q2): 1st Monday

MAY
  ├─ Patch Releases: Every Monday
  └─ Minor Release: 1st Monday

JUNE
  ├─ Patch Releases: Every Monday
  ├─ Minor Release: 1st Monday
  └─ Freeze Window: Final week (Q2 end)

JULY
  ├─ Patch Releases: Every Monday
  ├─ Minor Release: 1st Monday
  └─ MAJOR RELEASE (Q3): 1st Monday

AUGUST
  ├─ Patch Releases: Every Monday
  └─ Minor Release: 1st Monday

SEPTEMBER
  ├─ Patch Releases: Every Monday
  ├─ Minor Release: 1st Monday
  └─ Freeze Window: Final week (Q3 end)

OCTOBER
  ├─ Patch Releases: Every Monday
  ├─ Minor Release: 1st Monday
  └─ MAJOR RELEASE (Q4): 1st Monday

NOVEMBER
  ├─ Patch Releases: Every Monday
  └─ Minor Release: 1st Monday

DECEMBER
  ├─ Patch Releases: Every Monday (until freeze)
  ├─ Minor Release: 1st Monday
  ├─ Annual Meta‑Release: 2nd Monday
  └─ Freeze Window: Final 2 weeks (Q4 end)
```

---

## 🔁 Contributor Windows

To support the cadence, we define three key contributor windows:

### Open Window
- **When:** First 2 weeks after each major release
- **Activity:** High‑velocity feature intake
- **Focus:** New capabilities, experimental features, architectural proposals

### Stabilization Window
- **When:** Final week before each minor release
- **Activity:** Patch‑only
- **Focus:** Bug fixes, documentation, test coverage

### Freeze Window
- **When:** Last week of Q1-Q3 quarters; final 2 weeks of Q4/December
- **Activity:** No major merges
- **Focus:** Integration testing, release preparation, documentation finalization
- **Note:** December has a 2-week freeze to accommodate the annual meta-release and year-end consolidation

---

## 🔀 Contributor Workflow Process

This swimlane diagram illustrates the contributor workflow across different release phases, showing when and how to contribute throughout the release cycle:

```mermaid
flowchart TB
    subgraph "🚀 Major Release"
        MR[Major Release<br/>1st Monday of Quarter]
    end
    
    subgraph "⚡ Open Window Phase"
        direction LR
        OW1[High-Velocity<br/>Feature Intake]
        OW2[New Capabilities]
        OW3[Experimental Features]
        OW4[Architectural Proposals]
        OW1 --> OW2 --> OW3 --> OW4
    end
    
    subgraph "💻 Development Phase"
        direction LR
        DP1[Regular Contributions]
        DP2[Feature Development]
        DP3[Bug Fixes]
        DP4[Documentation]
        DP1 --> DP2 --> DP3 --> DP4
    end
    
    subgraph "🔧 Stabilization Window"
        direction LR
        SW1[Patch-Only Period]
        SW2[Bug Fixes]
        SW3[Documentation Updates]
        SW4[Test Coverage]
        SW1 --> SW2 --> SW3 --> SW4
    end
    
    subgraph "📦 Minor Release"
        MNR[Minor Release<br/>1st Monday of Month]
    end
    
    subgraph "🧊 Freeze Window Phase"
        direction LR
        FW1[No Major Merges]
        FW2[Integration Testing]
        FW3[Release Preparation]
        FW4[Documentation Finalization]
        FW1 --> FW2 --> FW3 --> FW4
    end
    
    subgraph "🎯 Release Phase"
        direction LR
        RP1[Tagged Release]
        RP2[Changelog Published]
        RP3[Artifacts Deployed]
        RP1 --> RP2 --> RP3
    end
    
    MR --> OW1
    OW4 --> DP1
    DP4 --> SW1
    SW4 --> MNR
    MNR --> DP1
    DP4 --> FW1
    FW4 --> RP1
    RP3 --> MR
    
    style MR fill:#ff6b6b
    style MNR fill:#4ecdc4
    style OW1 fill:#95e1d3
    style OW2 fill:#95e1d3
    style OW3 fill:#95e1d3
    style OW4 fill:#95e1d3
    style DP1 fill:#a8e6cf
    style DP2 fill:#a8e6cf
    style DP3 fill:#a8e6cf
    style DP4 fill:#a8e6cf
    style SW1 fill:#ffd93d
    style SW2 fill:#ffd93d
    style SW3 fill:#ffd93d
    style SW4 fill:#ffd93d
    style FW1 fill:#ffb347
    style FW2 fill:#ffb347
    style FW3 fill:#ffb347
    style FW4 fill:#ffb347
    style RP1 fill:#c7ceea
    style RP2 fill:#c7ceea
    style RP3 fill:#c7ceea
```

**Workflow Phases Explained:**

1. **Major Release** — Quarterly major release kicks off new cycle
2. **Open Window** (2 weeks) — High-velocity period for ambitious contributions
3. **Development Phase** — Regular contribution period with normal velocity
4. **Stabilization Window** (1 week) — Patch-only period before minor releases
5. **Minor Release** — Monthly feature release (or continue to freeze for quarter-end)
6. **Freeze Window** — Quarter-end integration testing and release prep
7. **Release Phase** — Tagged release with artifacts

**Contributor Guidance:**
- **Want to add major features?** → Target the Open Window after major releases
- **Want to contribute regularly?** → Development Phase is open for all contributions
- **Found a bug?** → Patches welcome anytime, especially in Stabilization Windows
- **Quarter ending soon?** → Be aware of Freeze Window—major work should wait

---

## 🧭 Governance Sync Points

### Monthly Maintainer Sync
- Review roadmap
- Triage issues
- Confirm next minor release
- Identity coherence check

### Quarterly Architecture Review
- Evaluate module boundaries
- Review runtime behavior
- Assess identity coherence
- Plan major release content

### Annual Unified‑Field Review
- Confirm long‑term direction
- Evolution phase confirmation
- Architectural audit
- Year‑end consolidation

---

## 📊 Mermaid Timeline View

```mermaid
timeline
    title Sofia Core Annual Release Cadence

    January
        : Patch Releases (Every Monday)
        : Minor Release (1st Monday)
        : MAJOR RELEASE — Q1 (1st Monday)

    February
        : Patch Releases (Every Monday)
        : Minor Release (1st Monday)

    March
        : Patch Releases (Every Monday)
        : Minor Release (1st Monday)
        : Freeze Window (Final week)

    April
        : Patch Releases (Every Monday)
        : Minor Release (1st Monday)
        : MAJOR RELEASE — Q2 (1st Monday)

    May
        : Patch Releases (Every Monday)
        : Minor Release (1st Monday)

    June
        : Patch Releases (Every Monday)
        : Minor Release (1st Monday)
        : Freeze Window (Final week)

    July
        : Patch Releases (Every Monday)
        : Minor Release (1st Monday)
        : MAJOR RELEASE — Q3 (1st Monday)

    August
        : Patch Releases (Every Monday)
        : Minor Release (1st Monday)

    September
        : Patch Releases (Every Monday)
        : Minor Release (1st Monday)
        : Freeze Window (Final week)

    October
        : Patch Releases (Every Monday)
        : Minor Release (1st Monday)
        : MAJOR RELEASE — Q4 (1st Monday)

    November
        : Patch Releases (Every Monday)
        : Minor Release (1st Monday)

    December
        : Patch Releases (Every Monday until freeze)
        : Minor Release (1st Monday)
        : Annual Meta‑Release (2nd Monday)
        : Freeze Window (Final 2 weeks)
```

---

## 🔥 Release Intensity Heatmap

This visualization shows the relative intensity of release activity throughout the year:

> **Note:** This heatmap uses emoji symbols for visual clarity. For best viewing, use a markdown viewer that supports emoji rendering.

| Release Type | Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec |
|--------------|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| **Patch**    | 🟦🟦🟦🟦 | 🟦🟦🟦🟦 | 🟦🟦🟦🟦 | 🟦🟦🟦🟦 | 🟦🟦🟦🟦 | 🟦🟦🟦🟦 | 🟦🟦🟦🟦 | 🟦🟦🟦🟦 | 🟦🟦🟦🟦 | 🟦🟦🟦🟦 | 🟦🟦🟦🟦 | 🟦🟦🟦🟦 |
| **Minor**    | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 | 🟩 |
| **Major**    | 🟧 | ⬜ | ⬜ | 🟧 | ⬜ | ⬜ | 🟧 | ⬜ | ⬜ | 🟧 | ⬜ | ⬜ |
| **Meta**     | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | 🟥 |
| **Freeze**   | ⬜ | ⬜ | 🟨 | ⬜ | ⬜ | 🟨 | ⬜ | ⬜ | 🟨 | ⬜ | ⬜ | 🟨🟨 |

**Legend:**
- 🟦 Patch releases (every Monday)
- 🟩 Minor release (1st Monday)
- 🟧 Major release (Quarterly, 1st Monday)
- 🟥 Annual Meta‑Release (2nd Monday of December)
- 🟨 Freeze Window (1 week at end of Q1-Q3, 2 weeks at end of Q4/December - note the double 🟨🟨 in December column)
- ⬜ No activity

### How to read this heatmap:
- **Patch (🟦🟦🟦🟦)** → Weekly cadence, always active
- **Minor (🟩)** → First Monday of the month
- **Major (🟧)** → First Monday of each quarter (Jan, Apr, Jul, Oct)
- **Meta (🟥)** → Second Monday of December
- **Freeze (🟨)** → Final week of Q1-Q3 quarters, final 2 weeks of Q4/December

The heatmap gives contributors and maintainers a single‑glance understanding of the entire year's rhythm.

---

## 🎯 Purpose

This calendar establishes a predictable, stable, identity‑aligned release rhythm across all systems governed by the unified field.

**Key Benefits:**
- **Predictable contributor flow** — Everyone knows when to contribute
- **Stable evolution** — Changes land at expected intervals
- **Coherent architectural progression** — Major shifts are planned and ceremonial
- **Unified‑field integrity** — All systems evolve together
- **Zero‑surprise governance** — Changes are telegraphed and prepared

This cadence is designed to support Sofia Core, EmeraldOrbit, Emerald Estates, EWF, and SEFAA governance structures while maintaining the unified field's identity coherence.

---

## 📝 Quick Reference

| Release Type | Frequency | Day | Purpose |
|--------------|-----------|-----|---------|
| Patch | Weekly | Every Monday | Bug fixes, stability |
| Minor | Monthly | 1st Monday | Features, enhancements |
| Major | Quarterly | 1st Monday (Jan, Apr, Jul, Oct) | Breaking changes, architectural shifts |
| Meta | Annually | 2nd Monday of December | Year‑end consolidation |

**Contributor Windows:**
- **Open:** 2 weeks after major releases
- **Stabilization:** 1 week before minor releases
- **Freeze:** Last week of Q1-Q3 quarters (2 weeks in Q4/December)

**Governance Sync:**
- **Monthly:** Maintainer sync
- **Quarterly:** Architecture review
- **Annually:** Unified‑field review
