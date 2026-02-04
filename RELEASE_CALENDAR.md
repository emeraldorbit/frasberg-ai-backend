# Annual Release Cadence for Sofia Core

**Applies to:** Sofia Core, EmeraldOrbit, Emerald Estates, EWF, and SEFAA

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

## 📖 Table of Contents

- [Overview](#-overview)
- [Badges](#-badges)
- [Release Types](#-release-types)
- [Visual Calendar Layout](#️-visual-calendar-layout)
- [Annual Release Timeline (Gantt Chart)](#-annual-release-timeline-gantt-chart)
- [Contributor Workflow Process](#-contributor-workflow-process)
- [Contributor Windows](#-contributor-windows)
- [Governance Sync Points](#-governance-sync-points)
- [Mermaid Timeline View](#-mermaid-timeline-view)
- [Release Intensity Heatmap](#-release-intensity-heatmap)
- [Purpose](#-purpose)
- [Quick Reference](#-quick-reference)

---

## 🏷️ Badges

![Release Cadence](https://img.shields.io/badge/Releases-Weekly%20%7C%20Monthly%20%7C%20Quarterly-blue?style=flat-square)
![Contribution Status](https://img.shields.io/badge/Contributions-Welcome-brightgreen?style=flat-square)
![Version](https://img.shields.io/badge/Version-1.0.0-informational?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

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

## 📊 Annual Release Timeline (Gantt Chart)

This Gantt chart visualizes the entire year's release schedule, showing the flow and overlap of different release types, freeze windows, and key milestones.

```mermaid
gantt
    title Sofia Core Annual Release Cadence
    dateFormat YYYY-MM-DD
    
    section Q1 Major Release
    Major Release Q1 (Jan 1st Mon)    :milestone, m1, 2024-01-01, 0d
    Open Window (2 weeks)             :active, ow1, 2024-01-01, 14d
    Development Phase                 :dev1, after ow1, 60d
    Freeze Window (Final week)        :crit, freeze1, 2024-03-25, 7d
    
    section Q2 Major Release
    Major Release Q2 (Apr 1st Mon)    :milestone, m2, 2024-04-01, 0d
    Open Window (2 weeks)             :active, ow2, 2024-04-01, 14d
    Development Phase                 :dev2, after ow2, 60d
    Freeze Window (Final week)        :crit, freeze2, 2024-06-24, 7d
    
    section Q3 Major Release
    Major Release Q3 (Jul 1st Mon)    :milestone, m3, 2024-07-01, 0d
    Open Window (2 weeks)             :active, ow3, 2024-07-01, 14d
    Development Phase                 :dev3, after ow3, 60d
    Freeze Window (Final week)        :crit, freeze3, 2024-09-23, 7d
    
    section Q4 Major Release
    Major Release Q4 (Oct 1st Mon)    :milestone, m4, 2024-10-01, 0d
    Open Window (2 weeks)             :active, ow4, 2024-10-01, 14d
    Development Phase                 :dev4, after ow4, 43d
    Annual Meta-Release (Dec 2nd Mon) :milestone, meta, 2024-12-09, 0d
    Freeze Window (Final 2 weeks)     :crit, freeze4, 2024-12-16, 14d
    
    section Monthly Minor Releases
    Minor Release (Every 1st Mon)     :done, minor, 2024-01-01, 365d
    
    section Weekly Patch Releases
    Patch Releases (Every Monday)     :patch, 2024-01-01, 365d
```

**Chart Legend:**
- **Milestones (diamonds):** Major releases (quarterly) and Annual Meta-Release
- **Active (green):** Open Windows for high-velocity feature intake
- **Development (blue):** Regular development phases
- **Critical (red):** Freeze Windows - no major merges, integration testing only
- **Done (gray):** Monthly minor releases (1st Monday of each month)
- **Patch (light blue):** Weekly patch releases (every Monday)

---

## 🌊 Contributor Workflow Process

This swimlane diagram shows how contributors should engage with the project across different release phases:

```mermaid
flowchart TD
    subgraph "Release Cycle Phases"
        direction TB
        
        subgraph "🟢 Open Window (2 weeks after Major Release)"
            A[High-Velocity Feature Intake]
            A1[Submit Major Features]
            A2[Propose Architectural Changes]
            A3[Experimental Contributions]
            A --> A1
            A --> A2
            A --> A3
        end
        
        subgraph "🔵 Development Phase (Regular Contributions)"
            B[Active Development]
            B1[Feature Development]
            B2[Bug Fixes]
            B3[Documentation]
            B4[Test Coverage]
            B --> B1
            B --> B2
            B --> B3
            B --> B4
        end
        
        subgraph "🟡 Stabilization Window (1 week before Minor Release)"
            C[Patch-Only Contributions]
            C1[Critical Bug Fixes]
            C2[Documentation Updates]
            C3[Test Improvements]
            C --> C1
            C --> C2
            C --> C3
        end
        
        subgraph "🔴 Freeze Window (End of Quarter)"
            D[Integration Testing Only]
            D1[No Major Merges]
            D2[Release Preparation]
            D3[Documentation Finalization]
            D --> D1
            D --> D2
            D --> D3
        end
        
        subgraph "🎯 Release Phase"
            E[Tagged Release]
            E1[Version Tagged]
            E2[Release Notes Published]
            E3[Artifacts Published]
            E --> E1
            E --> E2
            E --> E3
        end
    end
    
    A3 --> B1
    B4 --> C3
    C3 --> D1
    D3 --> E
    E3 --> A
    
    style "🟢 Open Window (2 weeks after Major Release)" fill:#90EE90
    style "🔵 Development Phase (Regular Contributions)" fill:#87CEEB
    style "🟡 Stabilization Window (1 week before Minor Release)" fill:#FFD700
    style "🔴 Freeze Window (End of Quarter)" fill:#FF6B6B
    style "🎯 Release Phase" fill:#9370DB
```

**Workflow Guide for Contributors:**

| Phase | Duration | What to Contribute | What to Avoid |
|-------|----------|-------------------|---------------|
| **🟢 Open Window** | 2 weeks after major release | Major features, architectural proposals, experimental work | Rushing incomplete features |
| **🔵 Development** | Between open and stabilization | Features, enhancements, bug fixes, docs | Breaking changes late in cycle |
| **🟡 Stabilization** | 1 week before minor release | Critical fixes, documentation, tests | New features, refactoring |
| **🔴 Freeze** | Last week of quarter (2 weeks in Dec) | Emergency patches only | Any non-critical changes |
| **🎯 Release** | Release day (Monday) | Monitor for issues, prepare next cycle | Last-minute changes |

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
