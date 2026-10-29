# -*- coding: utf-8 -*-
"""
Master Compiler for the Unified Cambridge Primary Stage 6 Science Mastery Guide
Combines:
1. Interactive Physics Workbench (Circuit Simulator with zero air-gap crocodile clips)
2. Live Atomic Lattice Simulation (Copper, Graphite, Insulators)
3. The 5 Core Concept Cards (Teacher's 36 Slides explained with analogies)
4. Cambridge Exam Traps & Step-by-Step Solved Examples
5. Video Lecture & School Homework Reference
6. Interactive 5-Question Cambridge Assessment Checkpoint
"""

import os

HTML_CONTENT = """<!-- impeccable-disable nested-cards -->
<!DOCTYPE html>
<html lang="en" dir="ltr" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Cambridge Stage 6 Science | Electricity & Circuits Complete Mastery Guide</title>
  
  <!-- Fonts: Academic British Science Pairing -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;700;800&family=Newsreader:ital,opsz,wght@0,6..72,600;0,6..72,700;1,6..72,400&family=Outfit:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  
  <!-- Tailwind CSS -->
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>

  <style>
    :root {
      --font-sans: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
      --font-serif: 'Newsreader', Georgia, serif;
      --font-mono: 'JetBrains Mono', monospace;
    }

    body {
      font-family: var(--font-sans);
      background-color: #f8fafc;
      color: #0f172a;
      transition: background-color 0.3s ease, color 0.3s ease;
    }

    .font-editorial { font-family: var(--font-serif); }
    .font-mono-val { font-family: var(--font-mono); }

    
    /* Impeccable Strict Typographic Scale (1.25x - 1.35x steps) */
    body { font-size: 16px; line-height: 1.6; }
    h1 { font-size: 36px; line-height: 1.2; font-weight: 800; }
    h2 { font-size: 26px; line-height: 1.3; font-weight: 800; }
    h3 { font-size: 20px; line-height: 1.4; font-weight: 700; }
    h4 { font-size: 16px; line-height: 1.4; font-weight: 700; }

    /* Custom Animation for Flowing Current */
    @keyframes electronFlow {
      from { stroke-dashoffset: 40; }
      to { stroke-dashoffset: 0; }
    }

    .electron-flow-active {
      stroke-dasharray: 6, 6;
      animation: electronFlow 0.8s linear infinite;
    }

    /* Tactile Buttons */
    .tactile-btn {
      transition: all 0.15s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .tactile-btn:active {
      transform: scale(0.97);
    }
    .tactile-btn:hover {
      transform: translateY(-2px);
    }

    /* Shelf Selection Card States */
    .shelf-card {
      transition: all 0.2s ease;
      cursor: pointer;
    }
    .shelf-card:hover {
      transform: translateY(-3px);
    }
    .shelf-card.active-selected {
      border-color: #2563eb !important;
      background-color: #eff6ff !important;
      box-shadow: 0 0 0 2px #3b82f6 !important;
    }

    /* Concept Card Tabs */
    .concept-chip.active {
      background: #4f46e5 !important;
      color: #ffffff !important;
      border-color: #4338ca !important;
    }

    /* Studio Modes */
    body.dark-mode {
      background-color: #0b1120;
      color: #f8fafc;
    }
    body.dark-mode #workbench-board {
      fill: #090d16;
      stroke: #1e293b;
    }
    body.dark-mode .board-grid-line {
      stroke: #1e293b;
    }
    body.dark-mode #wire-return {
      stroke: #64748b;
    }
    body.dark-mode .shelf-card.active-selected {
      background-color: #1e293b !important;
      border-color: #60a5fa !important;
      box-shadow: 0 0 0 2px #3b82f6 !important;
    }
    body.dark-mode .concept-card-body {
      background-color: #1e293b !important;
      border-color: #334155 !important;
      color: #f8fafc !important;
    }
  </style>
</head>
<body class="p-3 sm:p-6 md:p-10 antialiased selection:bg-blue-100 selection:text-blue-900">

  <div class="max-w-6xl mx-auto space-y-8">

    <!-- ============================================================== -->
    <!-- TOP NAVIGATION & STATUS BAR                                    -->
    <!-- ============================================================== -->
    <header class="flex flex-wrap items-center justify-between gap-4 pb-6 border-b border-slate-200 dark:border-slate-800">
      <div>
        <div class="flex items-center gap-2 mb-1.5">
          <a href="../../../index.html" class="inline-flex items-center gap-1.5 text-xs font-black text-indigo-600 dark:text-indigo-400 hover:underline">
            <span>&larr;</span>
            <span>All Subjects Portal</span>
          </a>
          <span class="text-slate-300 dark:text-slate-700">&bull;</span>
          <span class="text-xs font-extrabold uppercase tracking-wider text-slate-500 dark:text-slate-400">Cambridge Primary Stage 6</span>
          <span class="text-slate-300 dark:text-slate-700">&bull;</span>
          <span class="text-xs bg-purple-100 dark:bg-purple-950/70 text-purple-800 dark:text-purple-300 font-extrabold px-2.5 py-0.5 rounded-full">Science 106</span>
        </div>
        <h1 class="text-2xl sm:text-3xl md:text-4xl font-extrabold tracking-tight font-editorial text-slate-900 dark:text-white">
          Electricity &amp; Circuits Complete Mastery Guide
        </h1>
        <p class="text-xs sm:text-sm text-slate-500 dark:text-slate-400 mt-1 font-medium">
          Student Investigator: <b class="text-slate-900 dark:text-slate-200">Mostafa Ahmed (Grade 6A)</b> &bull; Manaret El-Eman British International School
        </p>
      </div>

      <!-- Action Controls -->
      <div class="flex items-center gap-2.5">
        <!-- Theme Mode Toggle -->
        <button onclick="toggleThemeMode()" id="theme-btn" class="tactile-btn flex items-center gap-2 px-3.5 py-2 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-xs font-bold text-slate-700 dark:text-slate-200 shadow-sm cursor-pointer">
          <span id="theme-icon">☀️</span>
          <span id="theme-text">Day (Studio)</span>
        </button>

        <!-- Audio Toggle -->
        <button onclick="toggleAudio()" id="audio-btn" class="tactile-btn flex items-center gap-2 px-3.5 py-2 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-xs font-bold text-slate-700 dark:text-slate-200 shadow-sm cursor-pointer">
          <span id="audio-icon">🔊</span>
          <span id="audio-text">Audio: ON</span>
        </button>

        <!-- Video Modal Button -->
        <a href="#video-section" class="tactile-btn flex items-center gap-2 px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-xs font-black text-white shadow-md shadow-indigo-200 dark:shadow-none cursor-pointer">
          <span>🎬</span>
          <span>Revision Video</span>
        </a>
      </div>
    </header>

    <!-- ============================================================== -->
    <!-- SECTION 1: INTERACTIVE PHYSICAL WORKBENCH (CIRCUIT LAB)        -->
    <!-- ============================================================== -->
    <section class="space-y-4">
      <div class="flex items-center justify-between">
        <div>
          <span class="text-[11px] font-black uppercase text-indigo-600 dark:text-indigo-400 tracking-wider">Experimental Physics Module 1</span>
          <h2 class="text-xl sm:text-2xl font-black text-slate-900 dark:text-white">1. Interactive Series Circuit Workbench</h2>
        </div>
        <div id="circuit-status-pill" class="text-[11px] font-mono-val font-bold uppercase px-3 py-1 rounded-full bg-rose-50 dark:bg-rose-950/60 border border-rose-300 dark:border-rose-800 text-rose-800 dark:text-rose-300">
          LOOP OPEN &bull; 0.00 A
        </div>
      </div>

      <!-- Workbench Surface Card -->
      <div class="relative bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-3 sm:p-5 shadow-sm overflow-hidden">
        
        <!-- Interactive Circuit SVG -->
        <svg id="circuit-svg" viewBox="0 0 840 370" class="w-full h-auto select-none overflow-visible">
          <defs>
            <linearGradient id="batteryBody" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stop-color="#1e3a8a"/>
              <stop offset="50%" stop-color="#2563eb"/>
              <stop offset="100%" stop-color="#1e40af"/>
            </linearGradient>
            <linearGradient id="copperCap" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stop-color="#f97316"/>
              <stop offset="50%" stop-color="#ea580c"/>
              <stop offset="100%" stop-color="#9a3412"/>
            </linearGradient>
            <linearGradient id="brassMetallic" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#fef08a"/>
              <stop offset="40%" stop-color="#eab308"/>
              <stop offset="70%" stop-color="#ca8a04"/>
              <stop offset="100%" stop-color="#713f12"/>
            </linearGradient>
            <radialGradient id="lampGlowLight" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stop-color="#fef08a" stop-opacity="0.95"/>
              <stop offset="40%" stop-color="#facc15" stop-opacity="0.5"/>
              <stop offset="80%" stop-color="#eab308" stop-opacity="0.15"/>
              <stop offset="100%" stop-color="#ca8a04" stop-opacity="0"/>
            </radialGradient>
            <linearGradient id="chromeMetal" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stop-color="#f1f5f9"/>
              <stop offset="35%" stop-color="#cbd5e1"/>
              <stop offset="70%" stop-color="#94a3b8"/>
              <stop offset="100%" stop-color="#64748b"/>
            </linearGradient>
            <linearGradient id="rubberBootLeft" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stop-color="#334155"/>
              <stop offset="50%" stop-color="#1e293b"/>
              <stop offset="100%" stop-color="#0f172a"/>
            </linearGradient>
            <linearGradient id="rubberBootRight" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stop-color="#3b82f6"/>
              <stop offset="50%" stop-color="#1d4ed8"/>
              <stop offset="100%" stop-color="#172554"/>
            </linearGradient>
            <radialGradient id="realCopper" cx="38%" cy="38%" r="62%">
              <stop offset="0%" stop-color="#fed7aa"/>
              <stop offset="25%" stop-color="#ea580c"/>
              <stop offset="70%" stop-color="#9a3412"/>
              <stop offset="100%" stop-color="#431407"/>
            </radialGradient>
            <filter id="compShadow" x="-10%" y="-10%" width="120%" height="130%">
              <feDropShadow dx="0" dy="3" stdDeviation="3" flood-color="#0f172a" flood-opacity="0.15"/>
            </filter>
          </defs>

          <!-- WORKBENCH BOARD -->
          <rect id="workbench-board" x="15" y="10" width="810" height="350" rx="16" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
          <line x1="220" y1="10" x2="220" y2="360" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="4,4" class="board-grid-line"/>
          <line x1="420" y1="10" x2="420" y2="360" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="4,4" class="board-grid-line"/>
          <line x1="620" y1="10" x2="620" y2="360" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="4,4" class="board-grid-line"/>

          <!-- 1. COMPONENT A: DUAL AA BATTERY PACK (LEFT) -->
          <g id="comp-battery" transform="translate(45, 45)" filter="url(#compShadow)">
            <rect x="0" y="0" width="145" height="200" rx="12" fill="#1e293b" stroke="#0f172a" stroke-width="2"/>
            <rect x="15" y="20" width="100" height="50" rx="6" fill="url(#batteryBody)"/>
            <rect x="85" y="20" width="30" height="50" fill="url(#copperCap)"/>
            <rect x="115" y="36" width="10" height="18" rx="2" fill="#cbd5e1" stroke="#94a3b8" stroke-width="1"/>
            <text x="60" y="50" fill="#ffffff" font-size="11" font-weight="900" font-family="monospace">1.5V AA</text>

            <rect x="15" y="110" width="100" height="50" rx="6" fill="url(#batteryBody)"/>
            <rect x="15" y="110" width="30" height="50" fill="url(#copperCap)"/>
            <path d="M 115 125 Q 123 135 115 145" stroke="#cbd5e1" stroke-width="2.5" fill="none"/>
            <text x="65" y="140" fill="#ffffff" font-size="11" font-weight="900" font-family="monospace">1.5V AA</text>

            <path d="M 15 45 L 8 45 L 8 135 L 15 135" fill="none" stroke="#e2e8f0" stroke-width="3.5" stroke-linecap="round"/>

            <circle cx="125" cy="45" r="9" fill="#ef4444" stroke="#b91c1c" stroke-width="2"/>
            <text x="125" y="48.5" fill="#ffffff" font-size="10" font-weight="900" text-anchor="middle">+</text>

            <circle cx="125" cy="135" r="9" fill="#0f172a" stroke="#475569" stroke-width="2"/>
            <text x="125" y="138" fill="#ffffff" font-size="10" font-weight="900" text-anchor="middle">&#8722;</text>

            <rect x="10" y="-14" width="125" height="16" rx="4" fill="#0f172a" opacity="0.9"/>
            <text x="72" y="-2" fill="#60a5fa" font-size="8.5" font-weight="800" font-family="monospace" text-anchor="middle">🔋 3.0V DC CELL PACK</text>
          </g>

          <!-- 2. COMPONENT B: BRASS KNIFE SWITCH (TOP CENTER) -->
          <g id="comp-switch" transform="translate(260, 50)" onclick="toggleKnifeSwitch()" class="cursor-pointer" filter="url(#compShadow)">
            <rect x="0" y="0" width="130" height="60" rx="10" fill="#f8fafc" stroke="#94a3b8" stroke-width="2"/>
            <circle cx="30" cy="30" r="12" fill="url(#brassMetallic)" stroke="#78350f" stroke-width="1.5"/>
            <circle cx="30" cy="30" r="4" fill="#78350f"/>
            <circle cx="100" cy="30" r="12" fill="url(#brassMetallic)" stroke="#78350f" stroke-width="1.5"/>
            <circle cx="100" cy="30" r="4" fill="#78350f"/>
            <path d="M 96 22 L 104 22 L 102 38 L 98 38 Z" fill="#92400e"/>

            <g id="knife-blade" transform="rotate(0, 30, 30)">
              <rect x="25" y="26" width="76" height="8" rx="3" fill="url(#brassMetallic)" stroke="#78350f" stroke-width="1"/>
              <rect x="75" y="23" width="30" height="14" rx="4" fill="#dc2626" stroke="#991b1b" stroke-width="1.5"/>
            </g>

            <rect x="15" y="-14" width="100" height="16" rx="4" fill="#0f172a" opacity="0.9"/>
            <text x="65" y="-2" fill="#fbbf24" font-size="8.5" font-weight="800" font-family="monospace" text-anchor="middle">🔌 KNIFE SWITCH</text>
          </g>

          <!-- 3. COMPONENT C: 3.0V SCREW LAMP SOCKET & BULB (TOP RIGHT) -->
          <g id="comp-lamp" transform="translate(650, 45)" filter="url(#compShadow)">
            <circle id="lamp-glow" cx="50" cy="45" r="75" fill="url(#lampGlowLight)" opacity="0" class="transition-opacity duration-300"/>
            <rect x="10" y="80" width="80" height="38" rx="8" fill="#e2e8f0" stroke="#94a3b8" stroke-width="2"/>
            <rect x="26" y="55" width="48" height="26" rx="4" fill="#94a3b8" stroke="#475569" stroke-width="1.5"/>
            <line x1="26" y1="62" x2="74" y2="62" stroke="#475569" stroke-width="1"/>
            <line x1="26" y1="70" x2="74" y2="70" stroke="#475569" stroke-width="1"/>
            <circle cx="50" cy="45" r="32" fill="#f8fafc" stroke="#94a3b8" stroke-width="2" fill-opacity="0.3"/>
            <line x1="42" y1="55" x2="44" y2="38" stroke="#64748b" stroke-width="1.5"/>
            <line x1="58" y1="55" x2="56" y2="38" stroke="#64748b" stroke-width="1.5"/>
            <path id="lamp-filament" d="M 44 38 Q 50 30 56 38" fill="none" stroke="#475569" stroke-width="2" stroke-linecap="round"/>
            <circle cx="20" cy="99" r="8" fill="url(#brassMetallic)" stroke="#78350f" stroke-width="1.5"/>
            <circle cx="20" cy="99" r="3" fill="#78350f"/>
            <circle cx="80" cy="99" r="8" fill="url(#brassMetallic)" stroke="#78350f" stroke-width="1.5"/>
            <circle cx="80" cy="99" r="3" fill="#78350f"/>

            <rect x="0" y="-14" width="100" height="16" rx="4" fill="#0f172a" opacity="0.9"/>
            <text x="50" y="-2" fill="#facc15" font-size="8.5" font-weight="800" font-family="monospace" text-anchor="middle">💡 3.0V LAMP</text>
          </g>

          <!-- 4. COMPONENT D: SPECIMEN CLAMPING GAP (BOTTOM CENTER) -->
          <g id="comp-specimen" transform="translate(300, 205)" filter="url(#compShadow)">
            <rect x="0" y="0" width="240" height="122" rx="14" fill="#1e293b" stroke="#334155" stroke-width="2"/>
            <rect x="45" y="-14" width="150" height="16" rx="4" fill="#0f172a" opacity="0.9"/>
            <text x="120" y="-2" fill="#34d399" font-size="8.5" font-weight="800" font-family="monospace" text-anchor="middle">🧲 SPECIMEN TEST GAP</text>

            <!-- Specimen Display Layer -->
            <g id="specimen-holder">
              <!-- Item 0: Empty Air Gap -->
              <g id="item-none" display="block">
                <rect x="86" y="42" width="68" height="26" rx="6" fill="#0f172a" stroke="#f87171" stroke-width="1.5" stroke-dasharray="4,4" fill-opacity="0.6"/>
                <text x="120" y="58" fill="#f87171" font-size="9" font-weight="900" font-family="monospace" text-anchor="middle">
                  AIR BREAK
                </text>
              </g>

              <!-- Item 1: 1p Copper Penny -->
              <g id="item-coin" display="none">
                <circle cx="120" cy="55" r="38" fill="url(#realCopper)" stroke="#7c2d12" stroke-width="2.5"/>
                <circle cx="120" cy="55" r="33" fill="none" stroke="#fed7aa" stroke-width="1.5" stroke-dasharray="3,3" opacity="0.8"/>
                <path d="M 110 47 L 113 41 L 120 45 L 127 41 L 130 47 L 128 51 L 112 51 Z" fill="#fed7aa" stroke="#c2410c" stroke-width="1"/>
                <circle cx="113" cy="39" r="1.5" fill="#fef08a"/>
                <circle cx="120" cy="37" r="1.5" fill="#fef08a"/>
                <circle cx="127" cy="39" r="1.5" fill="#fef08a"/>
                <text x="120" y="72" text-anchor="middle" fill="#fed7aa" font-size="16" font-weight="900" font-family="serif">1</text>
              </g>

              <!-- Item 2: Rubber Eraser -->
              <g id="item-eraser" display="none">
                <rect x="80" y="38" width="80" height="34" rx="4" fill="#fb7185" stroke="#e11d48" stroke-width="2"/>
                <path d="M 80 38 L 102 38 L 102 72 L 80 72 Z" fill="#38bdf8"/>
                <text x="131" y="59" text-anchor="middle" fill="#ffffff" font-size="9" font-weight="900" font-family="sans-serif">ERASER</text>
              </g>

              <!-- Item 3: HB Graphite Pencil (Zero Midline Text & Clamped Directly) -->
              <g id="item-pencil" display="none">
                <polygon points="76,46 136,46 136,50 76,50" fill="#f59e0b"/>
                <rect x="76" y="50" width="60" height="10" fill="#d97706"/>
                <polygon points="76,60 136,60 136,64 76,64" fill="#b45309"/>
                <polygon points="136,46 152,51 152,59 136,64" fill="#fed7aa" stroke="#d97706" stroke-width="0.8"/>
                <line x1="136" y1="52" x2="148" y2="53" stroke="#d97706" stroke-width="0.5" opacity="0.6"/>
                <line x1="136" y1="58" x2="148" y2="57" stroke="#d97706" stroke-width="0.5" opacity="0.6"/>
                <rect x="152" y="52" width="14" height="6" rx="1" fill="#0f172a" stroke="#000000" stroke-width="0.8"/>
                <line x1="152" y1="53.5" x2="166" y2="53.5" stroke="#64748b" stroke-width="1"/>
              </g>

              <!-- Item 4: Acrylic Plastic Ruler -->
              <g id="item-ruler" display="none">
                <rect x="80" y="41" width="80" height="28" rx="3" fill="#e0f2fe" stroke="#0284c7" stroke-width="1.5" fill-opacity="0.85"/>
                <line x1="90" y1="41" x2="90" y2="49" stroke="#0369a1" stroke-width="1.5"/>
                <line x1="105" y1="41" x2="105" y2="53" stroke="#0369a1" stroke-width="1.5"/>
                <line x1="120" y1="41" x2="120" y2="49" stroke="#0369a1" stroke-width="1.5"/>
                <line x1="135" y1="41" x2="135" y2="53" stroke="#0369a1" stroke-width="1.5"/>
                <line x1="150" y1="41" x2="150" y2="49" stroke="#0369a1" stroke-width="1.5"/>
                <text x="120" y="63" text-anchor="middle" fill="#0369a1" font-size="8.5" font-weight="900" font-family="monospace">PLASTIC</text>
              </g>
            </g>

            <!-- LEFT ALLIGATOR CLIP -->
            <g id="clip-left">
              <rect x="8" y="44" width="46" height="22" rx="6" fill="url(#rubberBootLeft)" stroke="#334155" stroke-width="1.5"/>
              <line x1="18" y1="46" x2="18" y2="64" stroke="#475569" stroke-width="1.5"/>
              <line x1="25" y1="46" x2="25" y2="64" stroke="#475569" stroke-width="1.5"/>
              <line x1="32" y1="46" x2="32" y2="64" stroke="#475569" stroke-width="1.5"/>
              
              <rect x="52" y="48" width="10" height="14" rx="2" fill="url(#chromeMetal)" stroke="#64748b" stroke-width="1"/>
              <circle cx="57" cy="55" r="3" fill="#cbd5e1" stroke="#475569" stroke-width="1"/>
              
              <path d="M 58 51 L 80 47 L 83 51 L 62 54 Z" fill="url(#chromeMetal)" stroke="#475569" stroke-width="1"/>
              <path d="M 62 56 L 83 59 L 80 63 L 58 59 Z" fill="url(#chromeMetal)" stroke="#475569" stroke-width="1"/>
              <polygon points="68,51 71,55 74,50 77,54 80,49 82,53" fill="#0f172a"/>
              <polygon points="68,59 71,55 74,60 77,56 80,61 82,57" fill="#0f172a"/>
            </g>

            <!-- RIGHT ALLIGATOR CLIP -->
            <g id="clip-right">
              <rect x="186" y="44" width="46" height="22" rx="6" fill="url(#rubberBootRight)" stroke="#1e40af" stroke-width="1.5"/>
              <line x1="208" y1="46" x2="208" y2="64" stroke="#60a5fa" stroke-width="1.5"/>
              <line x1="215" y1="46" x2="215" y2="64" stroke="#60a5fa" stroke-width="1.5"/>
              <line x1="222" y1="46" x2="222" y2="64" stroke="#60a5fa" stroke-width="1.5"/>
              
              <rect x="178" y="48" width="10" height="14" rx="2" fill="url(#chromeMetal)" stroke="#64748b" stroke-width="1"/>
              <circle cx="183" cy="55" r="3" fill="#cbd5e1" stroke="#475569" stroke-width="1"/>
              
              <path d="M 182 51 L 160 49 L 157 53 L 178 54 Z" fill="url(#chromeMetal)" stroke="#475569" stroke-width="1"/>
              <path d="M 178 56 L 157 57 L 160 61 L 182 59 Z" fill="url(#chromeMetal)" stroke="#475569" stroke-width="1"/>
              <polygon points="172,52 169,55 166,51 163,55 160,50 158,54" fill="#0f172a"/>
              <polygon points="172,58 169,55 166,59 163,55 160,60 158,56" fill="#0f172a"/>
            </g>

            <!-- OLED TELEMETRY READOUT PILL -->
            <rect x="12" y="88" width="216" height="24" rx="12" fill="#090d16" stroke="#334155" stroke-width="1.2"/>
            <text id="specimen-station-label" x="120" y="103" fill="#f87171" font-size="8.5" font-weight="700" font-family="monospace" text-anchor="middle">
              Circuit Open: Air is an insulator (0.00 Amps)
            </text>
          </g>

          <!-- 5. HARMONIC BALANCED SERIES CIRCUIT WIRING -->
          <path d="M 170 90 Q 225 45 290 80" fill="none" stroke="#dc2626" stroke-width="4.5" stroke-linecap="round"/>
          <path d="M 360 80 Q 510 40 670 144" fill="none" stroke="#dc2626" stroke-width="4.5" stroke-linecap="round"/>
          <path d="M 730 144 Q 700 280 530 260" fill="none" stroke="#2563eb" stroke-width="4.5" stroke-linecap="round"/>
          <path id="wire-return" d="M 310 260 Q 220 270 170 180" fill="none" stroke="#334155" stroke-width="4.5" stroke-linecap="round"/>

          <!-- REAL-TIME ELECTRON STREAM -->
          <g id="electron-stream-group" display="none">
            <path d="M 170 90 Q 225 45 290 80" fill="none" stroke="#facc15" stroke-width="2.5" class="electron-flow-active"/>
            <path d="M 360 80 Q 510 40 670 144" fill="none" stroke="#facc15" stroke-width="2.5" class="electron-flow-active"/>
            <path d="M 670 144 L 730 144" fill="none" stroke="#facc15" stroke-width="3" class="electron-flow-active"/>
            <path d="M 730 144 Q 700 280 530 260" fill="none" stroke="#facc15" stroke-width="2.5" class="electron-flow-active"/>
            <path d="M 460 260 L 380 260" fill="none" stroke="#facc15" stroke-width="2.5" class="electron-flow-active"/>
            <path d="M 310 260 Q 220 270 170 180" fill="none" stroke="#facc15" stroke-width="2.5" class="electron-flow-active"/>
          </g>
        </svg>

        <!-- Digital Multimeter Corner HUD -->
        <div id="meter-card" class="absolute bottom-4 right-4 bg-slate-900/90 text-white rounded-xl px-3.5 py-2 shadow-lg backdrop-blur-md border border-slate-700/50">
          <div class="text-[10px] font-mono-val font-bold text-slate-400 mb-0.5">DIGITAL MULTIMETER</div>
          <div class="flex items-center gap-3 font-mono-val font-black text-xs">
            <span id="meter-v-text" class="text-blue-400">VOLTS: 3.00 V</span>
            <span id="meter-i-text" class="text-rose-400">CURRENT: 0.00 A</span>
          </div>
        </div>
      </div>

      <!-- Specimen Selection Shelf -->
      <div class="space-y-3">
        <div class="flex items-center justify-between text-xs font-bold text-slate-500 dark:text-slate-400">
          <span>🧰 Student Specimen Shelf (Click to place in circuit gap):</span>
          <span class="text-blue-600 dark:text-blue-400 font-extrabold text-[11px]">Instant Reaction</span>
        </div>

        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3.5">
          <!-- Item 1: Copper Coin -->
          <button onclick="selectMaterial('coin')" id="btn-mat-coin" class="shelf-card tactile-btn bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl p-4 flex flex-col items-center justify-center text-center space-y-2 group shadow-sm">
            <div class="w-12 h-12 rounded-xl bg-amber-100/70 dark:bg-amber-950/40 flex items-center justify-center text-2xl group-hover:scale-110 transition-transform">
              🪙
            </div>
            <div>
              <div class="text-sm font-black text-slate-900 dark:text-white">1p Copper Coin</div>
              <div class="text-[11px] text-emerald-600 dark:text-emerald-400 font-bold">Metal Conductor</div>
            </div>
          </button>

          <!-- Item 2: Rubber Eraser -->
          <button onclick="selectMaterial('eraser')" id="btn-mat-eraser" class="shelf-card tactile-btn bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl p-4 flex flex-col items-center justify-center text-center space-y-2 group shadow-sm">
            <div class="w-12 h-12 rounded-xl bg-rose-100/70 dark:bg-rose-950/40 flex items-center justify-center text-2xl group-hover:scale-110 transition-transform">
              🧹
            </div>
            <div>
              <div class="text-sm font-black text-slate-900 dark:text-white">Rubber Eraser</div>
              <div class="text-[11px] text-rose-500 font-bold">Polymer Insulator</div>
            </div>
          </button>

          <!-- Item 3: Pencil Lead -->
          <button onclick="selectMaterial('pencil')" id="btn-mat-pencil" class="shelf-card tactile-btn bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl p-4 flex flex-col items-center justify-center text-center space-y-2 group shadow-sm">
            <div class="w-12 h-12 rounded-xl bg-blue-100/70 dark:bg-blue-950/40 flex items-center justify-center text-2xl group-hover:scale-110 transition-transform">
              ✏️
            </div>
            <div>
              <div class="text-sm font-black text-slate-900 dark:text-white">Pencil Lead (Graphite)</div>
              <div class="text-[11px] text-blue-600 dark:text-blue-400 font-bold">Non-Metal Conductor</div>
            </div>
          </button>

          <!-- Item 4: Plastic Ruler -->
          <button onclick="selectMaterial('ruler')" id="btn-mat-ruler" class="shelf-card tactile-btn bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl p-4 flex flex-col items-center justify-center text-center space-y-2 group shadow-sm">
            <div class="w-12 h-12 rounded-xl bg-cyan-100/70 dark:bg-cyan-950/40 flex items-center justify-center text-2xl group-hover:scale-110 transition-transform">
              📏
            </div>
            <div>
              <div class="text-sm font-black text-slate-900 dark:text-white">Plastic Ruler</div>
              <div class="text-[11px] text-rose-500 font-bold">Acrylic Insulator</div>
            </div>
          </button>
        </div>
      </div>
    </section>

    <!-- ============================================================== -->
    <!-- SECTION 2: MICROSCOPIC & ATOMIC CHARGE SIMULATION              -->
    <!-- ============================================================== -->
    <section class="space-y-4">
      <div>
        <span class="text-[11px] font-black uppercase text-indigo-600 dark:text-indigo-400 tracking-wider">Experimental Physics Module 2</span>
        <h2 class="text-xl sm:text-2xl font-black text-slate-900 dark:text-white">2. Microscopic &amp; Atomic Charge Carrier Inspection</h2>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <!-- Box A: Physical Macro Appearance -->
        <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-5 shadow-sm space-y-3">
          <div class="text-xs font-black uppercase text-slate-500 dark:text-slate-400">Box A: Physical Macro Inspection</div>
          <div class="flex items-center gap-4">
            <div id="inspector-icon" class="w-14 h-14 rounded-2xl bg-slate-100 dark:bg-slate-800 flex items-center justify-center text-3xl">
              🔍
            </div>
            <div>
              <h3 id="inspector-name" class="text-base font-black text-slate-900 dark:text-white">Awaiting Material Clamping</h3>
              <p id="inspector-meta" class="text-xs text-slate-500 dark:text-slate-400">Select any material from the tray above to see its physical and molecular makeup.</p>
            </div>
          </div>
          <div id="inspector-desc" class="text-xs text-slate-600 dark:text-slate-300 bg-slate-50 dark:bg-slate-800/60 p-3.5 rounded-xl border border-slate-200 dark:border-slate-700/60 leading-relaxed font-medium">
            Cambridge Stage 6 Standard: Metals are conductors because electrons are free to move. Most non-metals are insulators, except graphite.
          </div>
        </div>

        <!-- Box B: Live Canvas Atomic Simulation -->
        <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-5 shadow-sm space-y-3">
          <div class="flex items-center justify-between">
            <span class="text-xs font-black uppercase text-slate-500 dark:text-slate-400">Box B: Live Atomic Electron Drift</span>
            <span class="text-[11px] font-mono-val font-bold text-blue-600 dark:text-blue-400">HTML5 Canvas Engine</span>
          </div>
          <div class="rounded-2xl overflow-hidden border border-slate-800 bg-[#090d16]">
            <canvas id="atomic-canvas" width="400" height="144" class="w-full h-auto block"></canvas>
          </div>
        </div>
      </div>
    </section>

    <!-- ============================================================== -->
    <!-- SECTION 3: THE 5 CORE CONCEPT CARDS (TEACHER'S 36 SLIDES)      -->
    <!-- ============================================================== -->
    <section class="space-y-4">
      <div class="flex items-center justify-between">
        <div>
          <span class="text-[11px] font-black uppercase text-indigo-600 dark:text-indigo-400 tracking-wider">Cambridge Stage 6 Core Curriculum</span>
          <h2 class="text-xl sm:text-2xl font-black text-slate-900 dark:text-white">3. Teacher's 36 Slides &bull; Core Concept Mastery</h2>
        </div>
        <span class="text-xs bg-indigo-50 dark:bg-indigo-950/60 border border-indigo-200 dark:border-indigo-800 text-indigo-800 dark:text-indigo-300 font-extrabold px-3 py-1 rounded-full">
          Electricity_(1).pptx
        </span>
      </div>

      <!-- Slide Chips Navigator -->
      <div class="flex items-center gap-2 overflow-x-auto pb-1 text-xs font-bold">
        <button onclick="showSlideCard(1)" id="chip-1" class="concept-chip active px-4 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 shadow-sm transition-all whitespace-nowrap cursor-pointer">
          Card 1: Electric Energy &amp; Cell (Slides 1–5)
        </button>
        <button onclick="showSlideCard(2)" id="chip-2" class="concept-chip px-4 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300 shadow-sm transition-all whitespace-nowrap cursor-pointer">
          Card 2: Open vs Closed Circuits (Slides 6–8)
        </button>
        <button onclick="showSlideCard(3)" id="chip-3" class="concept-chip px-4 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300 shadow-sm transition-all whitespace-nowrap cursor-pointer">
          Card 3: Conductors &amp; Circuit Symbols (Slides 9–11)
        </button>
        <button onclick="showSlideCard(4)" id="chip-4" class="concept-chip px-4 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300 shadow-sm transition-all whitespace-nowrap cursor-pointer">
          Card 4: Series vs Parallel Circuits (Slides 14–30)
        </button>
        <button onclick="showSlideCard(5)" id="chip-5" class="concept-chip px-4 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300 shadow-sm transition-all whitespace-nowrap cursor-pointer">
          Card 5: Teacher's Review Quiz (Slides 32–34)
        </button>
      </div>

      <!-- CONCEPT CARDS CONTAINER -->
      <div class="space-y-4">
        
        <!-- CARD 1: ELECTRIC ENERGY & CELL (SLIDES 1-5) -->
        <div id="slide-card-1" class="concept-card-body bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-6 shadow-sm space-y-4">
          <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
            <span class="text-xs font-black uppercase text-indigo-600 dark:text-indigo-400 tracking-wider">Concept 1 &bull; Teacher's Slides 1 to 5</span>
            <span class="text-xs bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 font-bold px-2.5 py-0.5 rounded-full">Core Foundations</span>
          </div>
          <h3 class="text-lg font-extrabold text-slate-900 dark:text-white">What is Electrical Energy and an Electric Cell?</h3>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            <div class="bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700/60 rounded-2xl p-4 space-y-2">
              <div class="font-extrabold text-slate-900 dark:text-white flex items-center gap-2 text-sm">
                <span class="text-amber-500">⚡</span>
                <span>Electrical Energy (Slide 4)</span>
              </div>
              <p class="text-slate-600 dark:text-slate-300 leading-relaxed font-medium">
                "Electrical energy is caused by <b>moving electric charges called electrons</b>. The faster the electric charges move, the more electrical energy they carry."
              </p>
              <div class="bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-900/50 p-2.5 rounded-xl text-amber-900 dark:text-amber-300 font-bold">
                💡 Water Analogy: Think of wires as water pipes and electrons as drops of water. Voltage is the water pressure pushing them along!
              </div>
            </div>

            <div class="bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700/60 rounded-2xl p-4 space-y-2">
              <div class="font-extrabold text-slate-900 dark:text-white flex items-center gap-2 text-sm">
                <span class="text-emerald-500">🔋</span>
                <span>The Electric Cell (Slide 5)</span>
              </div>
              <p class="text-slate-600 dark:text-slate-300 leading-relaxed font-medium">
                "An electric cell is a device which <b>converts chemical energy into electrical energy</b>." It has two terminals: Positive (+) and Negative (-).
              </p>
              <div class="bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-900/50 p-2.5 rounded-xl text-emerald-900 dark:text-emerald-300 font-bold">
                🔋 Cell vs Battery: A single cylinder is a "cell" (1.5V). When two or more cells connect together in series, they form a "battery" (3.0V)!
              </div>
            </div>
          </div>
        </div>

        <!-- CARD 2: OPEN VS CLOSED CIRCUITS (SLIDES 6-8) -->
        <div id="slide-card-2" class="concept-card-body bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-6 shadow-sm space-y-4 hidden">
          <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
            <span class="text-xs font-black uppercase text-indigo-600 dark:text-indigo-400 tracking-wider">Concept 2 &bull; Teacher's Slides 6 to 8</span>
            <span class="text-xs bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 font-bold px-2.5 py-0.5 rounded-full">Circuit Continuity</span>
          </div>
          <h3 class="text-lg font-extrabold text-slate-900 dark:text-white">Electric Circuit &amp; The Role of the Switch</h3>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            <div class="bg-emerald-50/70 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-800 rounded-2xl p-4 space-y-2">
              <div class="font-extrabold text-emerald-950 dark:text-emerald-200 flex items-center gap-2 text-sm">
                <span>🟢 Closed Circuit (Switch Closed)</span>
              </div>
              <p class="text-emerald-800 dark:text-emerald-300 leading-relaxed font-medium">
                A closed, continuous loop with <b>no gaps or breaks</b>. Electric current flows freely from the cell, through the wire, heats the filament, and lights the bulb!
              </p>
            </div>

            <div class="bg-rose-50/70 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-800 rounded-2xl p-4 space-y-2">
              <div class="font-extrabold text-rose-950 dark:text-rose-200 flex items-center gap-2 text-sm">
                <span>🔴 Open Circuit (Switch Open)</span>
              </div>
              <p class="text-rose-800 dark:text-rose-300 leading-relaxed font-medium">
                Not a continuous path! There is an <b>air break or open switch</b>. Electric current CANNOT cross air, so the loop is incomplete and the bulb remains dark.
              </p>
            </div>
          </div>
        </div>

        <!-- CARD 3: CONDUCTORS & CIRCUIT SYMBOLS (SLIDES 9-11) -->
        <div id="slide-card-3" class="concept-card-body bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-6 shadow-sm space-y-4 hidden">
          <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
            <span class="text-xs font-black uppercase text-indigo-600 dark:text-indigo-400 tracking-wider">Concept 3 &bull; Teacher's Slides 9 to 11</span>
            <span class="text-xs bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 font-bold px-2.5 py-0.5 rounded-full">Materials &amp; Symbols</span>
          </div>
          <h3 class="text-lg font-extrabold text-slate-900 dark:text-white">Conductors, Insulators &amp; Official Cambridge Circuit Symbols</h3>
          
          <div class="space-y-4 text-xs">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700/60 p-4 rounded-2xl">
                <div class="font-bold text-slate-900 dark:text-white text-sm">⚡ Conductors (Slide 9):</div>
                <div class="text-slate-600 dark:text-slate-300 mt-1.5 leading-relaxed font-medium">
                  Substances that allow electricity to pass through easily. Examples: <b>Copper, Aluminium, Iron, and Graphite (pencil lead)</b>.
                </div>
              </div>
              <div class="bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700/60 p-4 rounded-2xl">
                <div class="font-bold text-slate-900 dark:text-white text-sm">🔒 Insulators (Slide 9):</div>
                <div class="text-slate-600 dark:text-slate-300 mt-1.5 leading-relaxed font-medium">
                  Substances that do NOT allow electricity to pass through. Examples: <b>Plastic, Rubber, Glass, and Dry Wood</b>.
                </div>
              </div>
            </div>

            <div class="bg-slate-100 dark:bg-slate-800/90 p-4 rounded-2xl border border-slate-200 dark:border-slate-700 font-mono-val text-xs space-y-2 text-slate-700 dark:text-slate-300">
              <div class="font-sans font-bold text-slate-900 dark:text-white text-sm">Official Cambridge Symbols:</div>
              <div>&bull; <b>Cell:</b> [ &plus; |--&#x22ee;-- &#8722; ] (Long thin line for &plus;, short thick line for &#8722;)</div>
              <div>&bull; <b>Battery:</b> Two or more cells coupled in series [ &plus; |--&#x22ee;----&#x22ee;-- &#8722; ]</div>
              <div>&bull; <b>Bulb / Lamp:</b> Circle with a diagonal cross &bigotimes;</div>
              <div>&bull; <b>Switch:</b> Two terminals with an angled movable bridge line</div>
            </div>
          </div>
        </div>

        <!-- CARD 4: SERIES VS PARALLEL (SLIDES 14-30) -->
        <div id="slide-card-4" class="concept-card-body bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-6 shadow-sm space-y-4 hidden">
          <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
            <span class="text-xs font-black uppercase text-indigo-600 dark:text-indigo-400 tracking-wider">Concept 4 &bull; Teacher's Slides 14 to 30</span>
            <span class="text-xs bg-purple-100 dark:bg-purple-950/70 text-purple-800 dark:text-purple-300 font-bold px-2.5 py-0.5 rounded-full">Primary Exam Topic</span>
          </div>
          <h3 class="text-lg font-extrabold text-slate-900 dark:text-white">Series vs Parallel Circuits: The Essential Comparison</h3>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            <!-- Series -->
            <div class="bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700/60 rounded-2xl p-4 space-y-2">
              <div class="font-extrabold text-indigo-700 dark:text-indigo-400 text-sm">Series Circuit (Slides 14–18)</div>
              <p class="text-slate-600 dark:text-slate-300 leading-relaxed font-medium">
                There is <b>only ONE single path</b> for electric current to flow. All components connect in a continuous chain.
              </p>
              <div class="bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-900/50 p-2.5 rounded-xl text-rose-900 dark:text-rose-300 font-bold">
                ⚠️ Major Disadvantage (Slide 26): If ONE bulb burns out or is removed, the entire loop breaks and ALL other lights go out!
              </div>
            </div>

            <!-- Parallel -->
            <div class="bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700/60 rounded-2xl p-4 space-y-2">
              <div class="font-extrabold text-indigo-700 dark:text-indigo-400 text-sm">Parallel Circuit (Slides 19–25)</div>
              <p class="text-slate-600 dark:text-slate-300 leading-relaxed font-medium">
                The circuit <b>branches into two or more separate paths</b>. Current has multiple independent routes.
              </p>
              <div class="bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-900/50 p-2.5 rounded-xl text-emerald-900 dark:text-emerald-300 font-bold">
                ⭐ Major Advantage (Slide 30): Used in homes! If your kitchen bulb burns out, the bedroom and living room lights stay ON!
              </div>
            </div>
          </div>
        </div>

        <!-- CARD 5: TEACHER'S REVIEW QUESTIONS (SLIDES 32-34) -->
        <div id="slide-card-5" class="concept-card-body bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-6 shadow-sm space-y-4 hidden">
          <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
            <span class="text-xs font-black uppercase text-emerald-600 dark:text-emerald-400 tracking-wider">Concept 5 &bull; Teacher's Review Slides 32 to 34</span>
            <span class="text-xs bg-emerald-100 dark:bg-emerald-950/70 text-emerald-800 dark:text-emerald-300 font-bold px-2.5 py-0.5 rounded-full">Self-Check Flashcards</span>
          </div>
          <h3 class="text-lg font-extrabold text-slate-900 dark:text-white">Authentic Teacher Review Flashcards</h3>
          
          <div class="space-y-3 text-xs">
            <div class="border border-slate-200 dark:border-slate-700/60 p-4 rounded-2xl bg-slate-50 dark:bg-slate-800/60 space-y-2">
              <div class="font-extrabold text-slate-900 dark:text-white">Slide 32 Review: "What is the name for a circuit that has only ONE path for current to flow?"</div>
              <button onclick="document.getElementById('ans-32').classList.toggle('hidden')" class="text-indigo-600 dark:text-indigo-400 hover:underline font-black text-xs flex items-center gap-1 cursor-pointer">
                <span>Reveal Teacher's Answer</span>
                <span>▼</span>
              </button>
              <div id="ans-32" class="hidden text-emerald-800 dark:text-emerald-300 font-bold bg-emerald-50 dark:bg-emerald-950/40 p-2.5 rounded-xl border border-emerald-200 dark:border-emerald-900/50">
                Answer: <b>Series Circuit</b>.
              </div>
            </div>

            <div class="border border-slate-200 dark:border-slate-700/60 p-4 rounded-2xl bg-slate-50 dark:bg-slate-800/60 space-y-2">
              <div class="font-extrabold text-slate-900 dark:text-white">Slide 33 Review: "What happens to the lights in a series circuit if one light goes off? And why?"</div>
              <button onclick="document.getElementById('ans-33').classList.toggle('hidden')" class="text-indigo-600 dark:text-indigo-400 hover:underline font-black text-xs flex items-center gap-1 cursor-pointer">
                <span>Reveal Teacher's Answer</span>
                <span>▼</span>
              </button>
              <div id="ans-33" class="hidden text-emerald-800 dark:text-emerald-300 font-bold bg-emerald-50 dark:bg-emerald-950/40 p-2.5 rounded-xl border border-emerald-200 dark:border-emerald-900/50">
                Answer: <b>All the lights go out</b> because the circuit is broken and there is no alternative path for current!
              </div>
            </div>

            <div class="border border-slate-200 dark:border-slate-700/60 p-4 rounded-2xl bg-slate-50 dark:bg-slate-800/60 space-y-2">
              <div class="font-extrabold text-slate-900 dark:text-white">Slide 34 Review: "What happens when one light goes out in a parallel circuit?"</div>
              <button onclick="document.getElementById('ans-34').classList.toggle('hidden')" class="text-indigo-600 dark:text-indigo-400 hover:underline font-black text-xs flex items-center gap-1 cursor-pointer">
                <span>Reveal Teacher's Answer</span>
                <span>▼</span>
              </button>
              <div id="ans-34" class="hidden text-emerald-800 dark:text-emerald-300 font-bold bg-emerald-50 dark:bg-emerald-950/40 p-2.5 rounded-xl border border-emerald-200 dark:border-emerald-900/50">
                Answer: <b>The other lights stay ON</b> because each branch forms its own independent complete loop!
              </div>
            </div>
          </div>
        </div>

      </div>
    </section>

    <!-- ============================================================== -->
    <!-- SECTION 4: CAMBRIDGE EXAM TRAPS & WORKED EXAMPLES              -->
    <!-- ============================================================== -->
    <section class="space-y-4">
      <div>
        <span class="text-[11px] font-black uppercase text-indigo-600 dark:text-indigo-400 tracking-wider">Cambridge Checkpoint Intelligence</span>
        <h2 class="text-xl sm:text-2xl font-black text-slate-900 dark:text-white">4. Cambridge Exam Traps &amp; Solved Step-by-Step Questions</h2>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
        
        <!-- Trap 1 -->
        <div class="bg-amber-50/70 dark:bg-amber-950/20 border border-amber-200 dark:border-amber-800/60 rounded-3xl p-5 space-y-2.5">
          <div class="flex items-center gap-2 text-amber-900 dark:text-amber-300 font-black text-sm">
            <span>⚠️</span>
            <span>Exam Trap 1: The Non-Metal Conductor</span>
          </div>
          <p class="text-slate-700 dark:text-slate-300 leading-relaxed font-medium">
            <b>The Common Mistake:</b> Students memorize that "all non-metals are insulators" and incorrectly label pencil lead as an insulator.
          </p>
          <div class="bg-white dark:bg-slate-900 p-3 rounded-xl border border-amber-200 dark:border-amber-800 text-slate-800 dark:text-slate-200 font-bold">
            🎯 Cambridge Rule: <b>Graphite is pure carbon (non-metal)</b>, but because carbon atoms bond in planar hexagonal sheets, free electrons slide between the layers, making it a true electrical conductor!
          </div>
        </div>

        <!-- Trap 2 -->
        <div class="bg-purple-50/70 dark:bg-purple-950/20 border border-purple-200 dark:border-purple-800/60 rounded-3xl p-5 space-y-2.5">
          <div class="flex items-center gap-2 text-purple-900 dark:text-purple-300 font-black text-sm">
            <span>🔋</span>
            <span>Exam Trap 2: Series Battery Cell Polarity</span>
          </div>
          <p class="text-slate-700 dark:text-slate-300 leading-relaxed font-medium">
            <b>The Common Mistake:</b> Connecting two cells with opposing terminals (+ to + or - to -) hoping for 3.0V.
          </p>
          <div class="bg-white dark:bg-slate-900 p-3 rounded-xl border border-purple-200 dark:border-purple-800 text-slate-800 dark:text-slate-200 font-bold">
            🎯 Cambridge Rule: Cells must be connected <b>Positive to Negative (+ to -)</b> in series so their electromotive forces add together ($1.5V + 1.5V = 3.0V$). Opposing cells cancel each other out ($1.5V - 1.5V = 0V$)!
          </div>
        </div>

      </div>
    </section>

    <!-- ============================================================== -->
    <!-- SECTION 5: VIDEO LECTURE & HOMEWORK REFERENCE                  -->
    <!-- ============================================================== -->
    <section id="video-section" class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-6 shadow-sm space-y-4">
      <div class="flex items-center justify-between">
        <div>
          <span class="text-[11px] font-black uppercase text-indigo-600 dark:text-indigo-400 tracking-wider">Multimedia Revision Lecture</span>
          <h2 class="text-xl font-black text-slate-900 dark:text-white">5. Cambridge Science PSLE Revision Video: Electricity in Series</h2>
        </div>
        <span class="text-xs bg-emerald-100 dark:bg-emerald-950/70 text-emerald-800 dark:text-emerald-300 font-bold px-3 py-1 rounded-full">
          Episode 18 &bull; Offline Ready
        </span>
      </div>

      <div class="relative w-full rounded-2xl overflow-hidden bg-black border border-slate-300 dark:border-slate-800 shadow-inner">
        <video 
          id="main-science-video" 
          controls 
          preload="metadata" 
          class="w-full aspect-video rounded-2xl bg-black"
          src="Primary%20Science%20PSLE%20Revision%20Guide%20EP%2018%20_%20Electricity%20_%20Electricity%20in%20Series.mp4">
          Your browser does not support video playback.
        </video>
      </div>

      <div class="flex flex-wrap items-center justify-between gap-3 pt-2 text-xs text-slate-500 dark:text-slate-400 border-t border-slate-100 dark:border-slate-800 font-medium">
        <span>Assigned Coligo Homework Worksheet: <b>FORCE_H.W..pdf</b></span>
        <span class="text-indigo-600 dark:text-indigo-400 font-bold">Manaret El-Eman British International School</span>
      </div>
    </section>

    <!-- ============================================================== -->
    <!-- SECTION 6: 5-QUESTION CAMBRIDGE CHECKPOINT CHALLENGE           -->
    <!-- ============================================================== -->
    <section class="space-y-4 pb-12">
      <div class="flex items-center justify-between">
        <div>
          <span class="text-[11px] font-black uppercase text-indigo-600 dark:text-indigo-400 tracking-wider">Formal Assessment</span>
          <h2 class="text-xl sm:text-2xl font-black text-slate-900 dark:text-white">6. Cambridge Checkpoint Challenge</h2>
        </div>
        <div id="checkpoint-score" class="text-xs font-mono-val font-black bg-indigo-50 dark:bg-indigo-950/60 border border-indigo-200 dark:border-indigo-800 text-indigo-800 dark:text-indigo-300 px-3.5 py-1.5 rounded-xl">
          Score: 0 / 5
        </div>
      </div>

      <div class="space-y-4">
        
        <!-- Q1 -->
        <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-5 shadow-sm space-y-3">
          <div class="text-xs font-black text-slate-500 dark:text-slate-400">Question 1 of 5 &bull; Circuit Continuity</div>
          <p class="text-sm font-extrabold text-slate-900 dark:text-white">
            Mostafa connects a battery, a buzzer, and an unknown test rod in series. The buzzer sounds loudly. What does this confirm about the test rod?
          </p>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
            <button onclick="checkAnswer(1, 0, false)" class="q-opt-1 tactile-btn text-left p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/60 text-slate-700 dark:text-slate-300 font-bold">
              A) The rod is an electrical insulator
            </button>
            <button onclick="checkAnswer(1, 1, true)" class="q-opt-1 tactile-btn text-left p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/60 text-slate-700 dark:text-slate-300 font-bold">
              B) The rod is an electrical conductor
            </button>
            <button onclick="checkAnswer(1, 2, false)" class="q-opt-1 tactile-btn text-left p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/60 text-slate-700 dark:text-slate-300 font-bold">
              C) The circuit has an open air break
            </button>
            <button onclick="checkAnswer(1, 3, false)" class="q-opt-1 tactile-btn text-left p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/60 text-slate-700 dark:text-slate-300 font-bold">
              D) The battery has run completely out of energy
            </button>
          </div>
          <div id="q-feedback-1" class="text-xs font-bold hidden p-3 rounded-xl"></div>
        </div>

        <!-- Q2 -->
        <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-5 shadow-sm space-y-3">
          <div class="text-xs font-black text-slate-500 dark:text-slate-400">Question 2 of 5 &bull; Real-World Engineering</div>
          <p class="text-sm font-extrabold text-slate-900 dark:text-white">
            Why are the ceiling lamps in your home wired in parallel rather than in series?
          </p>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
            <button onclick="checkAnswer(2, 0, false)" class="q-opt-2 tactile-btn text-left p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/60 text-slate-700 dark:text-slate-300 font-bold">
              A) Parallel circuits require no switches at all
            </button>
            <button onclick="checkAnswer(2, 1, false)" class="q-opt-2 tactile-btn text-left p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/60 text-slate-700 dark:text-slate-300 font-bold">
              B) Parallel circuits make all bulbs turn off when one burns out
            </button>
            <button onclick="checkAnswer(2, 2, true)" class="q-opt-2 tactile-btn text-left p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/60 text-slate-700 dark:text-slate-300 font-bold">
              C) If one bulb burns out, all remaining bulbs stay lit
            </button>
            <button onclick="checkAnswer(2, 3, false)" class="q-opt-2 tactile-btn text-left p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/60 text-slate-700 dark:text-slate-300 font-bold">
              D) Parallel circuits prevent any electrons from flowing
            </button>
          </div>
          <div id="q-feedback-2" class="text-xs font-bold hidden p-3 rounded-xl"></div>
        </div>

        <!-- Q3 -->
        <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-5 shadow-sm space-y-3">
          <div class="text-xs font-black text-slate-500 dark:text-slate-400">Question 3 of 5 &bull; Materials Science</div>
          <p class="text-sm font-extrabold text-slate-900 dark:text-white">
            When Mostafa clamps a pencil core into the testing gap, the lamp lights up. What Cambridge scientific principle explains this?
          </p>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
            <button onclick="checkAnswer(3, 0, false)" class="q-opt-3 tactile-btn text-left p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/60 text-slate-700 dark:text-slate-300 font-bold">
              A) Pencil wood conducts electricity through sap
            </button>
            <button onclick="checkAnswer(3, 1, true)" class="q-opt-3 tactile-btn text-left p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/60 text-slate-700 dark:text-slate-300 font-bold">
              B) Graphite is a non-metal conductor with delocalized electrons
            </button>
            <button onclick="checkAnswer(3, 2, false)" class="q-opt-3 tactile-btn text-left p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/60 text-slate-700 dark:text-slate-300 font-bold">
              C) The pencil core is made of poisonous metal lead
            </button>
            <button onclick="checkAnswer(3, 3, false)" class="q-opt-3 tactile-btn text-left p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/60 text-slate-700 dark:text-slate-300 font-bold">
              D) The circuit remains open because graphite is an insulator
            </button>
          </div>
          <div id="q-feedback-3" class="text-xs font-bold hidden p-3 rounded-xl"></div>
        </div>

        <!-- Q4 -->
        <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-5 shadow-sm space-y-3">
          <div class="text-xs font-black text-slate-500 dark:text-slate-400">Question 4 of 5 &bull; Series Voltage</div>
          <p class="text-sm font-extrabold text-slate-900 dark:text-white">
            Two identical 1.5V AA cells are wired correctly in series (+ connected to -). What is the total voltage delivered across the circuit?
          </p>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
            <button onclick="checkAnswer(4, 0, false)" class="q-opt-4 tactile-btn text-left p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/60 text-slate-700 dark:text-slate-300 font-bold">
              A) 0.00 Volts
            </button>
            <button onclick="checkAnswer(4, 1, false)" class="q-opt-4 tactile-btn text-left p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/60 text-slate-700 dark:text-slate-300 font-bold">
              B) 1.50 Volts
            </button>
            <button onclick="checkAnswer(4, 2, true)" class="q-opt-4 tactile-btn text-left p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/60 text-slate-700 dark:text-slate-300 font-bold">
              C) 3.00 Volts (1.5V + 1.5V)
            </button>
            <button onclick="checkAnswer(4, 3, false)" class="q-opt-4 tactile-btn text-left p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/60 text-slate-700 dark:text-slate-300 font-bold">
              D) 4.50 Volts
            </button>
          </div>
          <div id="q-feedback-4" class="text-xs font-bold hidden p-3 rounded-xl"></div>
        </div>

        <!-- Q5 -->
        <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-5 shadow-sm space-y-3">
          <div class="text-xs font-black text-slate-500 dark:text-slate-400">Question 5 of 5 &bull; Circuit Behavior</div>
          <p class="text-sm font-extrabold text-slate-900 dark:text-white">
            In a series circuit with one lamp, what happens to the brightness of the lamps if you add two more lamps into the same series loop?
          </p>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
            <button onclick="checkAnswer(5, 0, false)" class="q-opt-5 tactile-btn text-left p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/60 text-slate-700 dark:text-slate-300 font-bold">
              A) The lamps shine significantly brighter
            </button>
            <button onclick="checkAnswer(5, 1, true)" class="q-opt-5 tactile-btn text-left p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/60 text-slate-700 dark:text-slate-300 font-bold">
              B) All lamps shine dimmer because resistance increases and voltage is shared
            </button>
            <button onclick="checkAnswer(5, 2, false)" class="q-opt-5 tactile-btn text-left p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/60 text-slate-700 dark:text-slate-300 font-bold">
              C) The first lamp shines bright, the other two stay completely off
            </button>
            <button onclick="checkAnswer(5, 3, false)" class="q-opt-5 tactile-btn text-left p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/60 text-slate-700 dark:text-slate-300 font-bold">
              D) The circuit immediately shorts out
            </button>
          </div>
          <div id="q-feedback-5" class="text-xs font-bold hidden p-3 rounded-xl"></div>
        </div>

      </div>
    </section>

  </div>

  <!-- ============================================================== -->
  <!-- JAVASCRIPT LOGIC & SIMULATION ENGINE                           -->
  <!-- ============================================================== -->
  <script>
    let currentMaterial = null;
    let isKnifeSwitchClosed = true;
    let score = 0;
    let audioEnabled = true;
    let isDarkMode = false;
    const answered = {};

    // 1. Theme Mode Toggle
    function toggleThemeMode() {
      isDarkMode = !isDarkMode;
      document.body.classList.toggle('dark-mode', isDarkMode);
      document.getElementById('theme-icon').textContent = isDarkMode ? '🌙' : '☀️';
      document.getElementById('theme-text').textContent = isDarkMode ? 'Night (Dark)' : 'Day (Studio)';
      playTone(500, 'sine', 0.06);
    }

    // 2. Web Audio Synthesizer
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    let audioCtx = null;

    function playTone(freq, type = 'sine', duration = 0.12) {
      if (!audioEnabled) return;
      try {
        if (!audioCtx) audioCtx = new AudioContext();
        if (audioCtx.state === 'suspended') audioCtx.resume();
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = type;
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        gain.gain.setValueAtTime(0.12, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + duration);
      } catch (e) {}
    }

    function playSuccessChime() {
      playTone(523.25, 'sine', 0.1);
      setTimeout(() => playTone(659.25, 'sine', 0.15), 100);
      setTimeout(() => playTone(783.99, 'sine', 0.25), 220);
    }

    function toggleAudio() {
      audioEnabled = !audioEnabled;
      document.getElementById('audio-text').textContent = audioEnabled ? 'Audio: ON' : 'Audio: OFF';
      document.getElementById('audio-icon').textContent = audioEnabled ? '🔊' : '🔇';
    }

    // 3. Switch Lever Interaction
    function toggleKnifeSwitch() {
      isKnifeSwitchClosed = !isKnifeSwitchClosed;
      const blade = document.getElementById('knife-blade');
      
      if (isKnifeSwitchClosed) {
        blade.setAttribute('transform', 'rotate(0, 30, 30)');
        playTone(320, 'triangle', 0.08);
      } else {
        blade.setAttribute('transform', 'rotate(-38, 30, 30)');
        playTone(220, 'sawtooth', 0.08);
      }
      
      updateCircuitState();
    }

    // 4. HTML5 Canvas Atomic Lattice Simulation
    const canvas = document.getElementById('atomic-canvas');
    const ctx = canvas.getContext('2d');
    let particles = [];
    let animId = null;

    class ChargeParticle {
      constructor(type, x, y) {
        this.type = type;
        this.baseX = x;
        this.baseY = y;
        this.x = x;
        this.y = y;
        this.vx = type === 'coin' ? 2.0 + Math.random() * 0.8 : type === 'pencil' ? 1.5 + Math.random() * 0.5 : 0;
        this.radius = 3.5;
        this.phase = Math.random() * Math.PI * 2;
      }
      update(isConducting) {
        if (isConducting && (this.type === 'coin' || this.type === 'pencil')) {
          this.x += this.vx;
          if (this.x > 385) this.x = 15;
        } else {
          this.phase += 0.15;
          this.x = this.baseX + Math.sin(this.phase) * 1.5;
          this.y = this.baseY + Math.cos(this.phase) * 1.5;
        }
      }
      draw() {
        ctx.beginPath();
        if (this.type === 'coin') {
          ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
          ctx.fillStyle = '#38bdf8';
          ctx.shadowColor = '#0284c7';
          // ctx.shadowBlur = 4; (optimized for 60fps)
          ctx.fill();
          
        } else if (this.type === 'pencil') {
          ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
          ctx.fillStyle = '#60a5fa';
          ctx.shadowColor = '#2563eb';
          // ctx.shadowBlur = 4; (optimized for 60fps)
          ctx.fill();
          
        } else {
          ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
          ctx.fillStyle = '#f43f5e';
          ctx.fill();
        }
      }
    }

    function initParticles(type) {
      particles = [];
      if (type === 'coin') {
        for (let i = 0; i < 40; i++) {
          particles.push(new ChargeParticle('coin', Math.random() * 370 + 15, Math.random() * 110 + 16));
        }
      } else if (type === 'pencil') {
        for (let i = 0; i < 30; i++) {
          particles.push(new ChargeParticle('pencil', Math.random() * 370 + 15, 68 + (Math.random() - 0.5) * 16));
        }
      } else {
        for (let r = 0; r < 3; r++) {
          for (let c = 0; c < 8; c++) {
            particles.push(new ChargeParticle('insulator', c * 45 + 40, r * 38 + 35));
          }
        }
      }
    }

    function renderSimulation() {
      ctx.fillStyle = '#090d16';
      ctx.fillRect(0, 0, 400, 144);

      const isConducting = (currentMaterial === 'coin' || currentMaterial === 'pencil') && isKnifeSwitchClosed;

      if (!currentMaterial) {
        ctx.fillStyle = '#64748b';
        ctx.font = '12px JetBrains Mono';
        ctx.textAlign = 'center';
        ctx.fillText('Select a material above to observe electron movement', 200, 75);
      } else if (currentMaterial === 'coin') {
        ctx.fillStyle = '#1e293b';
        ctx.fillRect(10, 10, 380, 124);

        for (let r = 0; r < 3; r++) {
          for (let c = 0; c < 7; c++) {
            ctx.beginPath();
            ctx.arc(c * 54 + 40, r * 42 + 30, 9, 0, Math.PI * 2);
            ctx.fillStyle = '#b45309';
            ctx.fill();
            ctx.fillStyle = '#fed7aa';
            ctx.font = 'bold 8px monospace';
            ctx.textAlign = 'center';
            ctx.fillText('Cu', c * 54 + 40, r * 42 + 33);
          }
        }

        particles.forEach(p => {
          p.update(isConducting);
          p.draw();
        });

        ctx.fillStyle = isConducting ? '#38bdf8' : '#94a3b8';
        ctx.font = 'bold 10px JetBrains Mono';
        ctx.textAlign = 'left';
        ctx.fillText(isConducting ? '⚡ Delocalized Sea of Free Electrons Drifting' : '⏸ Switch Open: No Current Flow', 25, 124);

      } else if (currentMaterial === 'pencil') {
        ctx.fillStyle = '#1e293b';
        ctx.fillRect(10, 10, 380, 124);

        // Graphene sheets
        ctx.fillStyle = '#334155';
        ctx.fillRect(15, 26, 370, 14);
        ctx.fillRect(15, 96, 370, 14);

        ctx.fillStyle = '#94a3b8';
        ctx.font = '9px monospace';
        ctx.textAlign = 'center';
        ctx.fillText('--- Carbon Hexagonal Sheet 1 ---', 200, 36);
        ctx.fillText('--- Carbon Hexagonal Sheet 2 ---', 200, 106);

        particles.forEach(p => {
          p.update(isConducting);
          p.draw();
        });

        ctx.fillStyle = isConducting ? '#60a5fa' : '#94a3b8';
        ctx.font = 'bold 10px JetBrains Mono';
        ctx.textAlign = 'left';
        ctx.fillText(isConducting ? '⚡ Electrons Sliding Between Carbon Sheets' : '⏸ Switch Open: No Current Flow', 25, 72);

      } else {
        ctx.fillStyle = '#1e293b';
        ctx.fillRect(10, 10, 380, 124);

        for (let r = 0; r < 3; r++) {
          for (let c = 0; c < 8; c++) {
            const ix = c * 45 + 40;
            const iy = r * 38 + 35;
            ctx.beginPath();
            ctx.arc(ix, iy, 7, 0, Math.PI * 2);
            ctx.fillStyle = '#475569';
            ctx.fill();
            if (c < 7) {
              ctx.strokeStyle = '#334155';
              ctx.lineWidth = 2;
              ctx.beginPath();
              ctx.moveTo(ix + 7, iy); ctx.lineTo(ix + 38, iy);
              ctx.stroke();
            }
          }
        }

        particles.forEach(p => {
          p.update(false);
          p.draw();
        });

        ctx.fillStyle = '#f87171';
        ctx.font = 'bold 11px JetBrains Mono';
        ctx.textAlign = 'center';
        ctx.fillText('🔒 ELECTRONS ARE TRAPPED: ZERO CURRENT FLOW', 200, 122);
      }

      animId = requestAnimationFrame(renderSimulation);
    }

    renderSimulation();

    // 5. Specimen Selection
    function selectMaterial(mat) {
      currentMaterial = mat;

      document.querySelectorAll('.shelf-card').forEach(c => c.classList.remove('active-selected'));
      const activeBtn = document.getElementById('btn-mat-' + mat);
      if (activeBtn) activeBtn.classList.add('active-selected');

      ['none', 'coin', 'eraser', 'pencil', 'ruler'].forEach(k => {
        const el = document.getElementById('item-' + k);
        if (el) el.setAttribute('display', k === mat ? 'block' : 'none');
      });

      updateInspectorContent(mat);
      initParticles(mat);
      updateCircuitState();
    }

    function updateCircuitState() {
      const isConductor = currentMaterial === 'coin' || currentMaterial === 'pencil';
      const isComplete = isConductor && isKnifeSwitchClosed;

      const pill = document.getElementById('circuit-status-pill');
      const stream = document.getElementById('electron-stream-group');
      const glow = document.getElementById('lamp-glow');
      const fil = document.getElementById('lamp-filament');
      const meterV = document.getElementById('meter-v-text');
      const meterI = document.getElementById('meter-i-text');
      const stationLabel = document.getElementById('specimen-station-label');

      if (isComplete) {
        pill.textContent = 'CLOSED LOOP • 0.28 A (FLOWING)';
        pill.className = 'text-[11px] font-mono-val font-bold uppercase px-3 py-1 rounded-full bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-300 dark:border-emerald-800 text-emerald-800 dark:text-emerald-300';
        stationLabel.textContent = currentMaterial === 'coin' ? '1p Copper Coin: Conductor (Loop Closed)' : 'Pencil Lead: Non-Metal Conductor (Loop Closed)';
        stationLabel.setAttribute('fill', '#34d399');

        stream.setAttribute('display', 'block');
        glow.setAttribute('opacity', '1');
        fil.setAttribute('stroke', '#ffffff');
        meterV.textContent = 'VOLTS: 3.00 V';
        meterI.textContent = 'CURRENT: 0.28 A';
        meterI.className = 'text-emerald-400 font-black';

        playSuccessChime();
      } else {
        pill.textContent = 'LOOP OPEN • 0.00 A';
        pill.className = 'text-[11px] font-mono-val font-bold uppercase px-3 py-1 rounded-full bg-rose-50 dark:bg-rose-950/60 border border-rose-300 dark:border-rose-800 text-rose-800 dark:text-rose-300';
        stationLabel.textContent = !currentMaterial ? 'Air Gap: Insulator • 0.00 A' : currentMaterial === 'eraser' ? 'Rubber Eraser: Insulator (Circuit Broken)' : currentMaterial === 'ruler' ? 'Plastic Ruler: Insulator (Circuit Broken)' : 'Knife Switch Open: Current Halted';
        stationLabel.setAttribute('fill', '#f87171');

        stream.setAttribute('display', 'none');
        glow.setAttribute('opacity', '0');
        fil.setAttribute('stroke', '#475569');
        meterV.textContent = 'VOLTS: 3.00 V';
        meterI.textContent = 'CURRENT: 0.00 A';
        meterI.className = 'text-rose-400 font-black';

        if (currentMaterial && isKnifeSwitchClosed) {
          playTone(200, 'square', 0.1);
        }
      }
    }

    function updateInspectorContent(mat) {
      const icon = document.getElementById('inspector-icon');
      const name = document.getElementById('inspector-name');
      const meta = document.getElementById('inspector-meta');
      const desc = document.getElementById('inspector-desc');

      if (mat === 'coin') {
        icon.textContent = '🪙';
        name.textContent = 'British 1p Copper Penny';
        meta.textContent = 'Composition: 94% Steel core with pure electrolytic Copper coating (Cu).';
        desc.innerHTML = '<b class="text-emerald-700 dark:text-emerald-400">Electrical Conductor:</b> Copper atoms share an ocean of delocalized electrons that move with zero resistance under 3.0V electrical pressure.';
      } else if (mat === 'eraser') {
        icon.textContent = '🧹';
        name.textContent = 'Vulcanized Classroom Eraser';
        meta.textContent = 'Composition: Cross-linked isoprene synthetic polymer chains.';
        desc.innerHTML = '<b class="text-rose-700 dark:text-rose-400">Electrical Insulator:</b> Valence electrons are locked tight in covalent bonds. Electrons cannot move freely, blocking the loop completely.';
      } else if (mat === 'pencil') {
        icon.textContent = '✏️';
        name.textContent = 'HB Compressed Graphite Lead';
        meta.textContent = 'Composition: Layered crystalline carbon sheets bonded with fine clay.';
        desc.innerHTML = '<b class="text-blue-700 dark:text-blue-400">Non-Metal Conductor:</b> Carbon atoms form hexagonal planar rings leaving 1 free pi-electron per atom that slides effortlessly between layers!';
      } else if (mat === 'ruler') {
        icon.textContent = '📏';
        name.textContent = 'Extruded Acrylic Polymer Ruler';
        meta.textContent = 'Composition: Polymethyl methacrylate (PMMA) plastic resin.';
        desc.innerHTML = '<b class="text-rose-700 dark:text-rose-400">Electrical Insulator:</b> Highly stable polymer chains with zero mobile charge carriers, safely preventing electric shocks.';
      }
    }

    // 6. Concept Card Tabs
    function showSlideCard(num) {
      for (let i = 1; i <= 5; i++) {
        const c = document.getElementById('slide-card-' + i);
        const btn = document.getElementById('chip-' + i);
        if (c && btn) {
          if (i === num) {
            c.classList.remove('hidden');
            btn.classList.add('active');
            btn.className = "concept-chip active px-4 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 shadow-sm transition-all whitespace-nowrap cursor-pointer";
          } else {
            c.classList.add('hidden');
            btn.classList.remove('active');
            btn.className = "concept-chip px-4 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300 shadow-sm transition-all whitespace-nowrap cursor-pointer";
          }
        }
      }
      playTone(440, 'sine', 0.05);
    }

    // 7. Checkpoint Assessment Logic
    function checkAnswer(qNum, optIdx, isCorrect) {
      if (answered[qNum]) return;
      answered[qNum] = true;

      const opts = document.querySelectorAll('.q-opt-' + qNum);
      opts.forEach((btn, idx) => {
        btn.disabled = true;
        btn.classList.remove('tactile-btn', 'cursor-pointer');
        if (idx === optIdx) {
          if (isCorrect) {
            btn.className = "text-left p-3 rounded-xl border-2 border-emerald-500 bg-emerald-50 dark:bg-emerald-950/50 text-emerald-900 dark:text-emerald-200 font-extrabold";
          } else {
            btn.className = "text-left p-3 rounded-xl border-2 border-rose-500 bg-rose-50 dark:bg-rose-950/50 text-rose-900 dark:text-rose-200 font-extrabold";
          }
        }
      });

      const fb = document.getElementById('q-feedback-' + qNum);
      fb.classList.remove('hidden');

      if (isCorrect) {
        score++;
        document.getElementById('checkpoint-score').textContent = `Score: ${score} / 5`;
        fb.className = "text-xs font-bold p-3 rounded-xl bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-200 dark:border-emerald-800 text-emerald-800 dark:text-emerald-300";
        fb.innerHTML = "✅ <b>Correct!</b> Outstanding Cambridge scientific understanding!";
        playSuccessChime();
      } else {
        fb.className = "text-xs font-bold p-3 rounded-xl bg-rose-50 dark:bg-rose-950/60 border border-rose-200 dark:border-rose-800 text-rose-800 dark:text-rose-300";
        fb.innerHTML = "❌ <b>Incorrect.</b> Review the Core Concept Cards above to see why this rule holds true.";
        playTone(180, 'sawtooth', 0.15);
      }
    }
  </script>
</body>
</html>
"""

def main():
    target_path = r"C:\Users\co0ob\Projects\primary-exam-system\resources\coligo\Mostafa\Science 106\Electricity_Mastery_Guide_Stage6.html"
    brain_path = r"C:\Users\co0ob\.gemini\antigravity\brain\54d05bb7-093a-4520-bc55-e8fbc272480c\Electricity_Mastery_Guide_Stage6.html"

    with open(target_path, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)
    print(f"Updated primary target: {target_path} ({len(HTML_CONTENT)} bytes)")

    with open(brain_path, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)
    print(f"Updated brain mirror: {brain_path} ({len(HTML_CONTENT)} bytes)")

if __name__ == "__main__":
    main()
