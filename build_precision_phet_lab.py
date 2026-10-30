<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Cambridge Stage 6 Science | Precision Circuit Laboratory</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;600;700;800&family=Newsreader:ital,opsz,wght@0,6..72,400..700;1,6..72,400..600&family=Outfit:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <style>
    :root {
      --font-sans: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
      --font-serif: 'Newsreader', Georgia, serif;
      --font-mono: 'JetBrains Mono', monospace;
    }
    body {
      font-family: var(--font-sans);
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }
    h1 {
      font-family: var(--font-serif);
      font-size: 2.25rem !important;
      line-height: 2.5rem !important;
      letter-spacing: -0.025em !important;
    }
    h2 {
      font-family: var(--font-serif);
      font-size: 1.5rem !important;
      line-height: 2rem !important;
      letter-spacing: -0.02em !important;
    }
    h3 {
      font-size: 1.125rem !important;
      line-height: 1.5rem !important;
    }
    .font-serif { font-family: var(--font-serif); }
    .font-mono { font-family: var(--font-mono); font-variant-numeric: tabular-nums; }
    
    /* Tactile Micro-Interactions */
    .tactile-btn {
      transition: transform 0.12s cubic-bezier(0.2, 0, 0, 1), background-color 0.15s ease, border-color 0.15s ease;
    }
    .tactile-btn:active {
      transform: scale(0.97) !important;
    }
    
    /* Electron Stream Animation */
    @keyframes electronStream {
      from { stroke-dashoffset: 28; }
      to { stroke-dashoffset: 0; }
    }
    .electron-flow-active {
      stroke-dasharray: 6, 6;
      animation: electronStream 0.5s linear infinite;
    }

    /* Shelf Card Transitions */
    .shelf-card {
      transition: all 0.18s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .shelf-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 16px -4px rgba(15, 23, 42, 0.08);
    }
    .shelf-card.active-selected {
      border-color: #2563eb !important;
      background-color: #eff6ff !important;
      box-shadow: 0 4px 12px -2px rgba(15, 23, 42, 0.1) !important;
    }

    /* Full Dark Mode Overrides */
    body.dark-mode {
      background-color: #090d16;
      color: #f1f5f9;
    }
    body.dark-mode .theme-surface {
      background-color: #0f172a;
      border-color: #1e293b;
    }
    body.dark-mode .theme-text-title {
      color: #ffffff;
    }
    body.dark-mode .theme-text-muted {
      color: #94a3b8;
    }
    body.dark-mode .shelf-card {
      background-color: #1e293b;
      border-color: #334155;
    }
    body.dark-mode .shelf-card.active-selected {
      background-color: #172554 !important;
      border-color: #3b82f6 !important;
    }
    body.dark-mode #workbench-board {
      fill: #0b1120 !important;
      stroke: #1e293b !important;
    }
    body.dark-mode .board-grid-line {
      stroke: #1e293b !important;
    }
    body.dark-mode #wire-return {
      stroke: #94a3b8 !important;
    }
    body.dark-mode .quiz-opt-btn {
      background-color: #1e293b !important;
      border-color: #334155 !important;
      color: #f1f5f9 !important;
    }
    body.dark-mode .quiz-opt-btn:hover {
      background-color: #334155 !important;
    }
  </style>
</head>
<body class="bg-[#f8fafc] text-slate-800 antialiased min-h-screen p-3 sm:p-6 lg:p-8 selection:bg-blue-600 selection:text-white transition-colors duration-300">

  <div class="max-w-5xl mx-auto space-y-6">

    <!-- 1. HEADER: BRAND & CONTROLS -->
    <header class="theme-surface flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white border border-slate-200/90 rounded-2xl p-5 sm:p-6 shadow-sm transition-colors duration-300">
      <div class="space-y-1.5">
        <div class="flex items-center gap-2">
          <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 inline-block"></span>
          <span class="text-[11px] font-mono font-bold uppercase tracking-wider text-blue-700 dark:text-blue-400">Cambridge Stage 6 • Physics Studio</span>
          <span class="text-slate-300 dark:text-slate-700">/</span>
          <span class="text-xs text-slate-500 dark:text-slate-400 font-medium">Manaret El-Eman British International School</span>
        </div>
        <h1 class="theme-text-title text-slate-950 font-bold">Precision Electric Circuit Laboratory</h1>
        <p class="theme-text-muted text-xs sm:text-sm text-slate-600 font-normal">
          Investigator: <strong class="text-slate-900 dark:text-white font-semibold">Mostafa Ahmed (Grade 6)</strong> • Verified physical contacts, zero-gap conductors, and dual studio modes.
        </p>
      </div>

      <!-- Quick Action Controls -->
      <div class="flex items-center gap-2 self-start sm:self-center">
        <!-- Day/Night Mode Toggle -->
        <button onclick="toggleThemeMode()" id="btn-theme" class="tactile-btn px-3.5 py-2 rounded-xl text-xs font-bold bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-200 flex items-center gap-1.5" title="Switch Day/Night View">
          <span id="theme-icon">☀️</span>
          <span id="theme-text">Day (Studio)</span>
        </button>

        <!-- Audio Toggle -->
        <button onclick="toggleAudio()" id="btn-audio" class="tactile-btn px-3 py-2 rounded-xl text-xs font-bold bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-200 flex items-center gap-1.5" title="Toggle Audio Feedback">
          <span id="audio-icon">🔊</span>
          <span id="audio-text">Audio: ON</span>
        </button>

        <!-- Video Lesson -->
        <button onclick="toggleVideoModal()" class="tactile-btn px-4 py-2 rounded-xl text-xs font-bold bg-blue-600 hover:bg-blue-700 text-white flex items-center gap-2">
          <span>🎬</span>
          <span>Cambridge Video</span>
        </button>
      </div>
    </header>

    <!-- 2. MAIN WORKBENCH SECTION -->
    <main class="theme-surface bg-white border border-slate-200/90 rounded-2xl p-5 sm:p-6 shadow-sm space-y-5 transition-colors duration-300">
      
      <!-- STATUS CONSOLE BAR -->
      <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 dark:border-slate-800 pb-4">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-blue-50 dark:bg-blue-950 border border-blue-200 dark:border-blue-800 text-blue-600 dark:text-blue-400 flex items-center justify-center font-bold text-lg">
            ⚡
          </div>
          <div>
            <div class="flex items-center gap-2">
              <span class="theme-text-title text-xs font-bold text-slate-900">Circuit Continuity Diagnostic</span>
              <span id="circuit-status-pill" class="text-[10px] font-mono font-bold uppercase px-2.5 py-0.5 rounded-full bg-rose-50 dark:bg-rose-950/50 border border-rose-200 dark:border-rose-900 text-rose-700 dark:text-rose-300">
                LOOP OPEN • 0.00 A
              </span>
            </div>
            <p id="assistant-hint" class="theme-text-muted text-xs text-slate-500 font-medium mt-0.5">
              Select an item from the shelf below. Real toothed crocodile clips will physically clamp onto it.
            </p>
          </div>
        </div>

        <!-- Knife Switch Control Button -->
        <div class="flex items-center gap-2">
          <button onclick="toggleKnifeSwitch()" id="btn-switch" class="tactile-btn px-3.5 py-2 rounded-xl text-xs font-extrabold bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-800 dark:text-slate-200 flex items-center gap-2">
            <span>🔌 Knife Switch:</span>
            <span id="switch-pill-text" class="text-emerald-700 dark:text-emerald-400 font-black">CLOSED (ON)</span>
          </button>
        </div>
      </div>

      <!-- WORKBENCH VISUAL CANVAS (HARMONIC RECTANGULAR SERIES LOOP) -->
      <div id="board-container" class="w-full bg-[#f1f5f9] dark:bg-[#020617] rounded-xl overflow-hidden relative p-3 sm:p-5 transition-colors duration-300">
        
        <!-- SVG Physics Canvas -->
        <svg viewBox="0 0 840 370" class="w-full h-auto select-none" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <!-- Realistic Component Gradients -->
            <linearGradient id="batteryBody" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#1e3a8a"/>
              <stop offset="30%" stop-color="#2563eb"/>
              <stop offset="70%" stop-color="#1d4ed8"/>
              <stop offset="100%" stop-color="#172554"/>
            </linearGradient>

            <linearGradient id="copperCap" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stop-color="#fed7aa"/>
              <stop offset="40%" stop-color="#f97316"/>
              <stop offset="100%" stop-color="#c2410c"/>
            </linearGradient>

            <!-- Lamp Volumetric Glow -->
            <radialGradient id="lampGlowLight" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stop-color="#ffffff" stop-opacity="1"/>
              <stop offset="25%" stop-color="#fef08a" stop-opacity="0.95"/>
              <stop offset="65%" stop-color="#facc15" stop-opacity="0.45"/>
              <stop offset="100%" stop-color="#ca8a04" stop-opacity="0"/>
            </radialGradient>

            <!-- Brass Binding Posts Gradient -->
            <linearGradient id="brassMetallic" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#fef08a"/>
              <stop offset="35%" stop-color="#f59e0b"/>
              <stop offset="75%" stop-color="#b45309"/>
              <stop offset="100%" stop-color="#78350f"/>
            </linearGradient>

            <!-- Steel Chrome Alligator Clip Jaws -->
            <linearGradient id="chromeMetal" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stop-color="#ffffff"/>
              <stop offset="30%" stop-color="#e2e8f0"/>
              <stop offset="65%" stop-color="#94a3b8"/>
              <stop offset="100%" stop-color="#475569"/>
            </linearGradient>

            <!-- Rubber Insulator Grip Sleeves -->
            <linearGradient id="rubberBootLeft" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stop-color="#334155"/>
              <stop offset="50%" stop-color="#0f172a"/>
              <stop offset="100%" stop-color="#020617"/>
            </linearGradient>
            <linearGradient id="rubberBootRight" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stop-color="#3b82f6"/>
              <stop offset="50%" stop-color="#1d4ed8"/>
              <stop offset="100%" stop-color="#172554"/>
            </linearGradient>

            <!-- Authentic British 1p Penny Gradient -->
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

          <!-- BOARD WORKBENCH SURFACE -->
          <rect id="workbench-board" x="15" y="10" width="810" height="350" rx="16" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
          
          <!-- Subtle Grid Ticks -->
          <line x1="220" y1="10" x2="220" y2="360" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="4,4" class="board-grid-line"/>
          <line x1="420" y1="10" x2="420" y2="360" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="4,4" class="board-grid-line"/>
          <line x1="620" y1="10" x2="620" y2="360" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="4,4" class="board-grid-line"/>

          <!-- ============================================================== -->
          <!-- 1. COMPONENT A: DUAL AA BATTERY PACK (LEFT SIDE)              -->
          <!-- Positive (+) Terminal Lug is at TOP: (170, 90)                 -->
          <!-- Negative (-) Terminal Lug is at BOTTOM: (170, 180)              -->
          <!-- ============================================================== -->
          <g id="comp-battery" transform="translate(45, 45)" filter="url(#compShadow)">
            <rect x="0" y="0" width="145" height="200" rx="12" fill="#1e293b" stroke="#0f172a" stroke-width="2"/>
            
            <!-- Battery 1 (Top cell): Positive (+) Nipple at Right -->
            <rect x="15" y="20" width="100" height="50" rx="6" fill="url(#batteryBody)"/>
            <rect x="85" y="20" width="30" height="50" fill="url(#copperCap)"/>
            <rect x="115" y="36" width="10" height="18" rx="2" fill="#cbd5e1" stroke="#94a3b8" stroke-width="1"/>
            <text x="60" y="50" fill="#ffffff" font-size="11" font-weight="900" font-family="monospace">1.5V AA</text>

            <!-- Battery 2 (Bottom cell): Series connection -->
            <rect x="15" y="110" width="100" height="50" rx="6" fill="url(#batteryBody)"/>
            <rect x="15" y="110" width="30" height="50" fill="url(#copperCap)"/>
            <!-- Spring coil at Right (-) -->
            <path d="M 115 125 Q 123 135 115 145" stroke="#cbd5e1" stroke-width="2.5" fill="none"/>
            <text x="65" y="140" fill="#ffffff" font-size="11" font-weight="900" font-family="monospace">1.5V AA</text>

            <!-- Series Jumper at Left connecting Bat1 (-) to Bat2 (+) -->
            <path d="M 15 45 L 8 45 L 8 135 L 15 135" fill="none" stroke="#e2e8f0" stroke-width="3.5" stroke-linecap="round"/>

            <!-- SOLDER TERMINALS -->
            <!-- RED TERMINAL LUG (+) AT TOP RIGHT (Global: 170, 90) -->
            <circle cx="125" cy="45" r="9" fill="#ef4444" stroke="#b91c1c" stroke-width="2"/>
            <text x="125" y="48.5" fill="#ffffff" font-size="10" font-weight="900" text-anchor="middle">+</text>

            <!-- BLACK TERMINAL LUG (-) AT BOTTOM RIGHT (Global: 170, 180) -->
            <circle cx="125" cy="135" r="9" fill="#0f172a" stroke="#475569" stroke-width="2"/>
            <text x="125" y="138" fill="#ffffff" font-size="10" font-weight="900" text-anchor="middle">&minus;</text>

            <!-- Badge -->
            <rect x="10" y="-14" width="125" height="16" rx="4" fill="#0f172a" opacity="0.9"/>
            <text x="72" y="-2" fill="#60a5fa" font-size="8.5" font-weight="800" font-family="monospace" text-anchor="middle">🔋 3.0V DC CELL PACK</text>
          </g>

          <!-- ============================================================== -->
          <!-- 2. COMPONENT B: BRASS KNIFE SWITCH (TOP CENTER)                -->
          <!-- Left Stud at (x=290, y=80), Right Stud at (x=370, y=80)        -->
          <!-- ============================================================== -->
          <g id="comp-switch" transform="translate(260, 50)" onclick="toggleKnifeSwitch()" class="cursor-pointer" filter="url(#compShadow)">
            <rect x="0" y="0" width="130" height="60" rx="10" fill="#f8fafc" stroke="#94a3b8" stroke-width="2"/>
            <!-- Left Screw Binding Post -->
            <circle cx="30" cy="30" r="12" fill="url(#brassMetallic)" stroke="#78350f" stroke-width="1.5"/>
            <circle cx="30" cy="30" r="4" fill="#78350f"/>
            
            <!-- Right Screw Binding Post -->
            <circle cx="100" cy="30" r="12" fill="url(#brassMetallic)" stroke="#78350f" stroke-width="1.5"/>
            <circle cx="100" cy="30" r="4" fill="#78350f"/>
            <path d="M 96 22 L 104 22 L 102 38 L 98 38 Z" fill="#92400e"/>

            <!-- Moving Knife Blade Pivot & Lever -->
            <g id="knife-blade" transform="rotate(0, 30, 30)">
              <rect x="25" y="26" width="76" height="8" rx="3" fill="url(#brassMetallic)" stroke="#78350f" stroke-width="1"/>
              <!-- Red Insulated Safety Handle -->
              <rect x="75" y="23" width="30" height="14" rx="4" fill="#dc2626" stroke="#991b1b" stroke-width="1.5"/>
            </g>

            <!-- Badge -->
            <rect x="15" y="-14" width="100" height="16" rx="4" fill="#0f172a" opacity="0.9"/>
            <text x="65" y="-2" fill="#fbbf24" font-size="8.5" font-weight="800" font-family="monospace" text-anchor="middle">🔌 KNIFE SWITCH</text>
          </g>

          <!-- ============================================================== -->
          <!-- 3. COMPONENT C: 3.0V SCREW LAMP SOCKET & BULB (TOP RIGHT)      -->
          <!-- Left Terminal at (x=670, y=144), Right Terminal at (x=730, y=144)-->
          <!-- ============================================================== -->
          <g id="comp-lamp" transform="translate(650, 45)" filter="url(#compShadow)">
            <!-- Volumetric Glow Halo -->
            <circle id="lamp-glow" cx="50" cy="45" r="75" fill="url(#lampGlowLight)" opacity="0" class="transition-opacity duration-300"/>
            
            <!-- Base Socket -->
            <rect x="10" y="80" width="80" height="38" rx="8" fill="#e2e8f0" stroke="#94a3b8" stroke-width="2"/>
            
            <!-- Metal Screw Shell -->
            <rect x="26" y="55" width="48" height="26" rx="4" fill="#94a3b8" stroke="#475569" stroke-width="1.5"/>
            <line x1="26" y1="62" x2="74" y2="62" stroke="#475569" stroke-width="1"/>
            <line x1="26" y1="70" x2="74" y2="70" stroke="#475569" stroke-width="1"/>

            <!-- Clear Glass Bulb Sphere -->
            <circle cx="50" cy="45" r="32" fill="#f8fafc" stroke="#94a3b8" stroke-width="2" fill-opacity="0.3"/>
            
            <!-- Filament Leads & Coil -->
            <line x1="42" y1="55" x2="44" y2="38" stroke="#64748b" stroke-width="1.5"/>
            <line x1="58" y1="55" x2="56" y2="38" stroke="#64748b" stroke-width="1.5"/>
            <path id="lamp-filament" d="M 44 38 Q 50 30 56 38" fill="none" stroke="#475569" stroke-width="2" stroke-linecap="round"/>

            <!-- Left Screw Terminal Binding Post -->
            <circle cx="20" cy="99" r="8" fill="url(#brassMetallic)" stroke="#78350f" stroke-width="1.5"/>
            <circle cx="20" cy="99" r="3" fill="#78350f"/>

            <!-- Right Screw Terminal Binding Post -->
            <circle cx="80" cy="99" r="8" fill="url(#brassMetallic)" stroke="#78350f" stroke-width="1.5"/>
            <circle cx="80" cy="99" r="3" fill="#78350f"/>

            <!-- Badge -->
            <rect x="0" y="-14" width="100" height="16" rx="4" fill="#0f172a" opacity="0.9"/>
            <text x="50" y="-2" fill="#facc15" font-size="8.5" font-weight="800" font-family="monospace" text-anchor="middle">💡 3.0V LAMP</text>
          </g>

          <!-- ============================================================== -->
          <!-- 4. COMPONENT D: SPECIMEN CLAMPING GAP (BOTTOM CENTER)          -->
          <!-- PHOTOREALISTIC LABORATORY CROCODILE CLAMPING & ZERO COLLISION  -->
          <!-- ============================================================== -->
          <g id="comp-specimen" transform="translate(300, 205)" filter="url(#compShadow)">
            <!-- Insulated Phenolic Stage Base -->
            <rect x="0" y="0" width="240" height="122" rx="14" fill="#1e293b" stroke="#334155" stroke-width="2"/>
            
            <!-- In-Canvas Component Badge -->
            <rect x="45" y="-14" width="150" height="16" rx="4" fill="#0f172a" opacity="0.9"/>
            <text x="120" y="-2" fill="#34d399" font-size="8.5" font-weight="800" font-family="monospace" text-anchor="middle">🧲 SPECIMEN TEST GAP</text>

            <!-- Specimen Display Layer (Drawn UNDER clips so clips visibly bite onto them!) -->
            <g id="specimen-holder">
              <!-- Default: Empty Break (Clean air slot with zero text collisions) -->
              <g id="item-none" display="block">
                <rect x="86" y="42" width="68" height="26" rx="6" fill="#0f172a" stroke="#f87171" stroke-width="1.5" stroke-dasharray="4,4" fill-opacity="0.6"/>
                <text x="120" y="58" fill="#f87171" font-size="9" font-weight="900" font-family="monospace" text-anchor="middle">
                  AIR BREAK
                </text>
              </g>

              <!-- Item 1: British 1p Copper Penny (Diameter 76px, centered at x=120, y=55) -->
              <g id="item-coin" display="none">
                <circle cx="120" cy="55" r="38" fill="url(#realCopper)" stroke="#7c2d12" stroke-width="2.5"/>
                <circle cx="120" cy="55" r="33" fill="none" stroke="#fed7aa" stroke-width="1.5" stroke-dasharray="3,3" opacity="0.8"/>
                <!-- Embossed Royal Crown Emblem -->
                <path d="M 110 47 L 113 41 L 120 45 L 127 41 L 130 47 L 128 51 L 112 51 Z" fill="#fed7aa" stroke="#c2410c" stroke-width="1"/>
                <circle cx="113" cy="39" r="1.5" fill="#fef08a"/>
                <circle cx="120" cy="37" r="1.5" fill="#fef08a"/>
                <circle cx="127" cy="39" r="1.5" fill="#fef08a"/>
                <text x="120" y="72" text-anchor="middle" fill="#fed7aa" font-size="16" font-weight="900" font-family="serif">1</text>
              </g>

              <!-- Item 2: Rubber Eraser (Beveled classroom eraser from x=80 to x=160) -->
              <g id="item-eraser" display="none">
                <rect x="80" y="38" width="80" height="34" rx="4" fill="#fb7185" stroke="#e11d48" stroke-width="2"/>
                <path d="M 80 38 L 102 38 L 102 72 L 80 72 Z" fill="#38bdf8"/>
                <text x="131" y="59" text-anchor="middle" fill="#ffffff" font-size="9" font-weight="900" font-family="sans-serif">ERASER</text>
              </g>

              <!-- Item 3: HB Graphite Pencil (Zero Midline Text! Exposed Lead Clamped Directly!) -->
              <g id="item-pencil" display="none">
                <!-- Hexagonal Wood Body (x=76 to 136, y=46 to 64) -->
                <polygon points="76,46 136,46 136,50 76,50" fill="#f59e0b"/>
                <rect x="76" y="50" width="60" height="10" fill="#d97706"/>
                <polygon points="76,60 136,60 136,64 76,64" fill="#b45309"/>
                
                <!-- Sharpened Cedar Wood Cone (x=136 to 152) -->
                <polygon points="136,46 152,51 152,59 136,64" fill="#fed7aa" stroke="#d97706" stroke-width="0.8"/>
                <line x1="136" y1="52" x2="148" y2="53" stroke="#d97706" stroke-width="0.5" opacity="0.6"/>
                <line x1="136" y1="58" x2="148" y2="57" stroke="#d97706" stroke-width="0.5" opacity="0.6"/>
                
                <!-- Cylindrical Pure Graphite Core (Extends from x=152 to 166, y=52 to 58) -->
                <!-- Firmly clamped inside right crocodile teeth! -->
                <rect x="152" y="52" width="14" height="6" rx="1" fill="#0f172a" stroke="#000000" stroke-width="0.8"/>
                <line x1="152" y1="53.5" x2="166" y2="53.5" stroke="#64748b" stroke-width="1"/>
              </g>

              <!-- Item 4: Acrylic Plastic Ruler (x=80 to x=160) -->
              <g id="item-ruler" display="none">
                <rect x="80" y="41" width="80" height="28" rx="3" fill="#e0f2fe" stroke="#0284c7" stroke-width="1.5" fill-opacity="0.85"/>
                <!-- Millimeter and Centimeter Marks -->
                <line x1="90" y1="41" x2="90" y2="49" stroke="#0369a1" stroke-width="1.5"/>
                <line x1="105" y1="41" x2="105" y2="53" stroke="#0369a1" stroke-width="1.5"/>
                <line x1="120" y1="41" x2="120" y2="49" stroke="#0369a1" stroke-width="1.5"/>
                <line x1="135" y1="41" x2="135" y2="53" stroke="#0369a1" stroke-width="1.5"/>
                <line x1="150" y1="41" x2="150" y2="49" stroke="#0369a1" stroke-width="1.5"/>
                <text x="120" y="63" text-anchor="middle" fill="#0369a1" font-size="8.5" font-weight="900" font-family="monospace">PLASTIC</text>
              </g>
            </g>

            <!-- ============================================================== -->
            <!-- REALISTIC ALLIGATOR CLIPS (DRAWN ON TOP - PHYSICAL CLAMPING)   -->
            <!-- ============================================================== -->

            <!-- LEFT ALLIGATOR CLIP (CLAMPING WOOD BODY AT x=76..82) -->
            <g id="clip-left">
              <!-- Black Rubber Boot Sleeve -->
              <rect x="8" y="44" width="46" height="22" rx="6" fill="url(#rubberBootLeft)" stroke="#334155" stroke-width="1.5"/>
              <!-- Boot Grip Rings -->
              <line x1="18" y1="46" x2="18" y2="64" stroke="#475569" stroke-width="1.5"/>
              <line x1="25" y1="46" x2="25" y2="64" stroke="#475569" stroke-width="1.5"/>
              <line x1="32" y1="46" x2="32" y2="64" stroke="#475569" stroke-width="1.5"/>
              
              <!-- Steel Pivot Hinge & Pin -->
              <rect x="52" y="48" width="10" height="14" rx="2" fill="url(#chromeMetal)" stroke="#64748b" stroke-width="1"/>
              <circle cx="57" cy="55" r="3" fill="#cbd5e1" stroke="#475569" stroke-width="1"/>
              
              <!-- Silver Chrome Upper Jaw (Slopes down to bite top of specimen at y=46) -->
              <path d="M 58 51 L 80 47 L 83 51 L 62 54 Z" fill="url(#chromeMetal)" stroke="#475569" stroke-width="1"/>
              <!-- Silver Chrome Lower Jaw (Slopes up to bite bottom of specimen at y=64) -->
              <path d="M 62 56 L 83 59 L 80 63 L 58 59 Z" fill="url(#chromeMetal)" stroke="#475569" stroke-width="1"/>
              <!-- Sharp Alligator Teeth biting into surface -->
              <polygon points="68,51 71,55 74,50 77,54 80,49 82,53" fill="#0f172a"/>
              <polygon points="68,59 71,55 74,60 77,56 80,61 82,57" fill="#0f172a"/>
            </g>

            <!-- RIGHT ALLIGATOR CLIP (CLAMPING GRAPHITE TIP DIRECTLY AT x=158..164) -->
            <g id="clip-right">
              <!-- Blue Rubber Boot Sleeve -->
              <rect x="186" y="44" width="46" height="22" rx="6" fill="url(#rubberBootRight)" stroke="#1e40af" stroke-width="1.5"/>
              <!-- Boot Grip Rings -->
              <line x1="208" y1="46" x2="208" y2="64" stroke="#60a5fa" stroke-width="1.5"/>
              <line x1="215" y1="46" x2="215" y2="64" stroke="#60a5fa" stroke-width="1.5"/>
              <line x1="222" y1="46" x2="222" y2="64" stroke="#60a5fa" stroke-width="1.5"/>
              
              <!-- Steel Pivot Hinge & Pin -->
              <rect x="178" y="48" width="10" height="14" rx="2" fill="url(#chromeMetal)" stroke="#64748b" stroke-width="1"/>
              <circle cx="183" cy="55" r="3" fill="#cbd5e1" stroke="#475569" stroke-width="1"/>
              
              <!-- Silver Chrome Upper Jaw (Slopes down to bite graphite core at y=52) -->
              <path d="M 182 51 L 160 49 L 157 53 L 178 54 Z" fill="url(#chromeMetal)" stroke="#475569" stroke-width="1"/>
              <!-- Silver Chrome Lower Jaw (Slopes up to bite graphite core at y=58) -->
              <path d="M 178 56 L 157 57 L 160 61 L 182 59 Z" fill="url(#chromeMetal)" stroke="#475569" stroke-width="1"/>
              <!-- Sharp Alligator Teeth gripping graphite tip -->
              <polygon points="172,52 169,55 166,51 163,55 160,50 158,54" fill="#0f172a"/>
              <polygon points="172,58 169,55 166,59 163,55 160,60 158,56" fill="#0f172a"/>
            </g>

            <!-- Single Clean Station Diagnostic Label inside OLED Pill -->
            <rect x="12" y="88" width="216" height="24" rx="12" fill="#090d16" stroke="#334155" stroke-width="1.2"/>
            <text id="specimen-station-label" x="120" y="103" fill="#f87171" font-size="8.5" font-weight="700" font-family="monospace" text-anchor="middle">
              Circuit Open: Air is an insulator (0.00 Amps)
            </text>
          </g>
<!-- ============================================================== -->
          <!-- 5. HARMONIC BALANCED SERIES CIRCUIT WIRING                     -->
          <!-- Wire 1: Battery (+) at (170, 90) -> Switch Left at (290, 80)    -->
          <!-- Wire 2: Switch Right at (360, 80) -> Lamp Left at (670, 144)   -->
          <!-- Wire 3: Lamp Right at (730, 144) -> Specimen Right at (530, 260)-->
          <!-- Wire 4: Specimen Left at (310, 260) -> Battery (-) at (170, 180)-->
          <!-- ============================================================== -->

          <!-- WIRE 1 (RED): Battery Top (+) -> Switch Left -->
          <path d="M 170 90 Q 225 45 290 80" fill="none" stroke="#dc2626" stroke-width="4.5" stroke-linecap="round"/>
          
          <!-- WIRE 2 (RED): Switch Right -> Lamp Left -->
          <path d="M 360 80 Q 510 40 670 144" fill="none" stroke="#dc2626" stroke-width="4.5" stroke-linecap="round"/>
          
          <!-- WIRE 3 (BLUE): Lamp Right -> Specimen Right Clip Boot -->
          <path d="M 730 144 Q 700 280 530 260" fill="none" stroke="#2563eb" stroke-width="4.5" stroke-linecap="round"/>
          
          <!-- WIRE 4 (RETURN): Specimen Left Clip Boot -> Battery Bottom (-) -->
          <path id="wire-return" d="M 310 260 Q 220 270 170 180" fill="none" stroke="#334155" stroke-width="4.5" stroke-linecap="round"/>

          <!-- REAL-TIME ELECTRON STREAM (FLOWS PRECISELY THROUGH LOOP) -->
          <g id="electron-stream-group" display="none">
            <path d="M 170 90 Q 225 45 290 80" fill="none" stroke="#facc15" stroke-width="2.5" class="electron-flow-active"/>
            <path d="M 360 80 Q 510 40 670 144" fill="none" stroke="#facc15" stroke-width="2.5" class="electron-flow-active"/>
            <path d="M 670 144 L 730 144" fill="none" stroke="#facc15" stroke-width="3" class="electron-flow-active"/>
            <path d="M 730 144 Q 700 280 530 260" fill="none" stroke="#facc15" stroke-width="2.5" class="electron-flow-active"/>
            <!-- Electron flow through specimen gap ONLY (Between jaws, no boot overlap!) -->
            <path d="M 460 260 L 380 260" fill="none" stroke="#facc15" stroke-width="2.5" class="electron-flow-active"/>
            <path d="M 310 260 Q 220 270 170 180" fill="none" stroke="#facc15" stroke-width="2.5" class="electron-flow-active"/>
          </g>
        </svg>

        <!-- Digital Multimeter HUD (Corner Card) -->
        <div id="meter-card" class="absolute bottom-4 right-4 bg-slate-900/90 text-white rounded-lg px-3.5 py-2 shadow backdrop-blur-md">
          <div class="text-[10px] font-mono font-bold text-slate-400 mb-0.5">DIGITAL MULTIMETER</div>
          <div class="flex items-center gap-3 font-mono font-black text-xs">
            <span id="meter-v-text" class="text-blue-400">VOLTS: 3.00 V</span>
            <span id="meter-i-text" class="text-rose-400">CURRENT: 0.00 A</span>
          </div>
        </div>
      </div>

      <!-- 3. SPECIMEN SELECTION SHELF -->
      <div class="space-y-3">
        <div class="flex items-center justify-between text-xs font-bold text-slate-500 dark:text-slate-400">
          <span>🧰 Student Specimen Shelf (Click to place in circuit gap):</span>
          <span class="text-blue-600 dark:text-blue-400 font-extrabold text-[11px]">Instant Reaction</span>
        </div>

        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3.5">
          
          <!-- Tool 1: 1p Copper Penny -->
          <button onclick="selectMaterial('coin')" id="btn-mat-coin" class="shelf-card tactile-btn bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl p-4 flex flex-col items-center justify-center text-center space-y-2 group cursor-pointer shadow-sm">
            <div class="w-12 h-12 rounded-xl bg-amber-100/70 dark:bg-amber-950/40 flex items-center justify-center text-2xl group-hover:scale-110 transition-transform">
              🪙
            </div>
            <div>
              <div class="font-bold text-sm text-slate-900 dark:text-white">Copper Coin (1p)</div>
              <div class="text-[11px] text-emerald-600 dark:text-emerald-400 font-bold mt-0.5">Pure Metal (Conductor)</div>
            </div>
          </button>

          <!-- Tool 2: Rubber Eraser -->
          <button onclick="selectMaterial('eraser')" id="btn-mat-eraser" class="shelf-card tactile-btn bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl p-4 flex flex-col items-center justify-center text-center space-y-2 group cursor-pointer shadow-sm">
            <div class="w-12 h-12 rounded-xl bg-rose-100/70 dark:bg-rose-950/40 flex items-center justify-center text-2xl group-hover:scale-110 transition-transform">
              🧹
            </div>
            <div>
              <div class="font-bold text-sm text-slate-900 dark:text-white">Rubber Eraser</div>
              <div class="text-[11px] text-rose-600 dark:text-rose-400 font-bold mt-0.5">Vulcanized Rubber (Insulator)</div>
            </div>
          </button>

          <!-- Tool 3: Pencil Graphite -->
          <button onclick="selectMaterial('pencil')" id="btn-mat-pencil" class="shelf-card tactile-btn bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl p-4 flex flex-col items-center justify-center text-center space-y-2 group cursor-pointer shadow-sm">
            <div class="w-12 h-12 rounded-xl bg-slate-100 dark:bg-slate-700 flex items-center justify-center text-2xl group-hover:scale-110 transition-transform">
              ✏️
            </div>
            <div>
              <div class="font-bold text-sm text-slate-900 dark:text-white">Pencil Lead (Graphite)</div>
              <div class="text-[11px] text-emerald-600 dark:text-emerald-400 font-bold mt-0.5">Non-Metal Conductor</div>
            </div>
          </button>

          <!-- Tool 4: Plastic Ruler -->
          <button onclick="selectMaterial('ruler')" id="btn-mat-ruler" class="shelf-card tactile-btn bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl p-4 flex flex-col items-center justify-center text-center space-y-2 group cursor-pointer shadow-sm">
            <div class="w-12 h-12 rounded-xl bg-cyan-100/70 dark:bg-cyan-950/40 flex items-center justify-center text-2xl group-hover:scale-110 transition-transform">
              📏
            </div>
            <div>
              <div class="font-bold text-sm text-slate-900 dark:text-white">Plastic Ruler</div>
              <div class="text-[11px] text-rose-600 dark:text-rose-400 font-bold mt-0.5">Synthetic Polymer (Insulator)</div>
            </div>
          </button>
        </div>
      </div>

      <!-- 4. REAL LIVE DYNAMIC INSPECTOR SHOWCASE (PLAIN-ENGLISH CAMBRIDGE MICROSCOPY) -->
      <div id="inspector-showcase" class="pt-5 border-t border-slate-200 dark:border-slate-800 space-y-4">
        
        <div class="flex items-center justify-between pb-1">
          <div class="flex items-center gap-2">
            <span class="text-sm">🔬</span>
            <span class="text-xs font-bold uppercase text-blue-700 dark:text-blue-400 tracking-wider">Cambridge Microscopic Inspector & Live Electron Flow</span>
          </div>
          <span id="showcase-badge" class="text-[10px] font-mono font-bold px-3 py-1 rounded-full bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300">
            AWAITING SELECTION
          </span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          
          <!-- Box A: Physical Macro Appearance -->
          <div class="space-y-2">
            <div class="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase font-mono">1. Physical Macro View</div>
            
            <div class="h-36 rounded-xl bg-slate-50 dark:bg-slate-950 flex items-center justify-center p-2 relative overflow-hidden">
              <svg id="macro-vector-stage" viewBox="0 0 320 120" class="w-full h-full">
                <text x="160" y="65" text-anchor="middle" fill="#94a3b8" font-size="12" font-weight="700">
                  Select an item above to inspect physical details
                </text>
              </svg>
            </div>
            
            <div id="macro-spec-meta" class="text-xs text-slate-700 dark:text-slate-300 font-medium"></div>
          </div>

          <!-- Box B: Live Canvas Atomic Charge Carrier Simulation -->
          <div class="space-y-2">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase font-mono">2. Microscopic Electron Flow (Live Simulation)</span>
              <span id="canvas-fps-badge" class="text-[10px] font-mono font-bold text-emerald-700 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/50 px-2 py-0.5 rounded">
                LIVE 60 FPS
              </span>
            </div>
            
            <div class="h-36 rounded-xl bg-[#090d16] relative overflow-hidden">
              <canvas id="atomic-canvas" width="400" height="144" class="w-full h-full block"></canvas>
            </div>
            
            <div id="atomic-spec-meta" class="text-xs text-slate-700 dark:text-slate-300 font-medium"></div>
          </div>

        </div>
      </div>

    </main>

    <!-- 5. CAMBRIDGE EXAM CHECKPOINT QUESTIONS -->
    <section class="theme-surface bg-white border border-slate-200/90 rounded-2xl p-6 sm:p-7 shadow-sm space-y-5 transition-colors duration-300">
      <div class="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-3">
        <div class="flex items-center gap-2.5">
          <span class="w-8 h-8 rounded-xl bg-blue-100 dark:bg-blue-950 text-blue-700 dark:text-blue-400 font-bold flex items-center justify-center text-sm">3</span>
          <h2 class="theme-text-title text-slate-900 font-bold">Cambridge Exam Checkpoint Challenge</h2>
        </div>
        <span id="quiz-score-badge" class="text-xs bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-bold px-3 py-1 rounded-full border border-slate-200 dark:border-slate-700">
          Score: 0 / 3
        </span>
      </div>

      <div class="space-y-5">
        
        <!-- Q1 -->
        <div class="pb-5 border-b border-slate-100 dark:border-slate-800 space-y-3">
          <div class="font-bold text-sm text-slate-900 dark:text-white">
            Q1. Mostafa sets up a circuit with a battery, a buzzer, and an unknown solid material in the gap. The buzzer buzzes loudly. What does this prove?
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
            <button onclick="answerQuestion(1, 'A', false)" class="q1-opt quiz-opt-btn tactile-btn text-left p-3 rounded-xl border border-slate-200 bg-white hover:bg-slate-100 text-slate-800 font-medium">
              A) The material is an electrical insulator
            </button>
            <button onclick="answerQuestion(1, 'B', true)" class="q1-opt quiz-opt-btn tactile-btn text-left p-3 rounded-xl border border-slate-200 bg-white hover:bg-slate-100 text-slate-800 font-medium">
              B) The material is an electrical conductor
            </button>
            <button onclick="answerQuestion(1, 'C', false)" class="q1-opt quiz-opt-btn tactile-btn text-left p-3 rounded-xl border border-slate-200 bg-white hover:bg-slate-100 text-slate-800 font-medium">
              C) The circuit has an open air break
            </button>
            <button onclick="answerQuestion(1, 'D', false)" class="q1-opt quiz-opt-btn tactile-btn text-left p-3 rounded-xl border border-slate-200 bg-white hover:bg-slate-100 text-slate-800 font-medium">
              D) The battery has run out of voltage
            </button>
          </div>
          <div id="feedback-1" class="hidden text-xs p-3 rounded-xl font-medium"></div>
        </div>

        <!-- Q2 -->
        <div class="pb-5 border-b border-slate-100 dark:border-slate-800 space-y-3">
          <div class="font-bold text-sm text-slate-900 dark:text-white">
            Q2. Why is pencil lead (graphite) special compared to most non-metals like plastic or wood?
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
            <button onclick="answerQuestion(2, 'A', false)" class="q2-opt quiz-opt-btn tactile-btn text-left p-3 rounded-xl border border-slate-200 bg-white hover:bg-slate-100 text-slate-800 font-medium">
              A) It is made of copper wire
            </button>
            <button onclick="answerQuestion(2, 'B', true)" class="q2-opt quiz-opt-btn tactile-btn text-left p-3 rounded-xl border border-slate-200 bg-white hover:bg-slate-100 text-slate-800 font-medium">
              B) It is a form of carbon with free delocalized electrons
            </button>
            <button onclick="answerQuestion(2, 'C', false)" class="q2-opt quiz-opt-btn tactile-btn text-left p-3 rounded-xl border border-slate-200 bg-white hover:bg-slate-100 text-slate-800 font-medium">
              C) It generates its own 3V electric charge
            </button>
            <button onclick="answerQuestion(2, 'D', false)" class="q2-opt quiz-opt-btn tactile-btn text-left p-3 rounded-xl border border-slate-200 bg-white hover:bg-slate-100 text-slate-800 font-medium">
              D) It acts as an insulator at room temperature
            </button>
          </div>
          <div id="feedback-2" class="hidden text-xs p-3 rounded-xl font-medium"></div>
        </div>

        <!-- Q3 -->
        <div class="space-y-3">
          <div class="font-bold text-sm text-slate-900 dark:text-white">
            Q3. In this series circuit, what happens to the entire circuit if one wire is detached from a battery terminal?
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
            <button onclick="answerQuestion(3, 'A', false)" class="q3-opt quiz-opt-btn tactile-btn text-left p-3 rounded-xl border border-slate-200 bg-white hover:bg-slate-100 text-slate-800 font-medium">
              A) Current doubles in the remaining parts
            </button>
            <button onclick="answerQuestion(3, 'B', false)" class="q3-opt quiz-opt-btn tactile-btn text-left p-3 rounded-xl border border-slate-200 bg-white hover:bg-slate-100 text-slate-800 font-medium">
              B) The lamp shines twice as bright
            </button>
            <button onclick="answerQuestion(3, 'C', true)" class="q3-opt quiz-opt-btn tactile-btn text-left p-3 rounded-xl border border-slate-200 bg-white hover:bg-slate-100 text-slate-800 font-medium">
              C) The circuit breaks and current drops immediately to 0.00 Amps
            </button>
            <button onclick="answerQuestion(3, 'D', false)" class="q3-opt quiz-opt-btn tactile-btn text-left p-3 rounded-xl border border-slate-200 bg-white hover:bg-slate-100 text-slate-800 font-medium">
              D) Voltage reverses direction
            </button>
          </div>
          <div id="feedback-3" class="hidden text-xs p-3 rounded-xl font-medium"></div>
        </div>

      </div>
    </section>

    <!-- 6. VIDEO LESSON MODAL -->
    <div id="videoModal" class="hidden fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
      <div class="theme-surface bg-white border border-slate-200 rounded-2xl max-w-3xl w-full p-5 space-y-4 shadow-2xl">
        <div class="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-3">
          <div class="flex items-center gap-2">
            <span class="text-xl">🎬</span>
            <span class="font-serif font-bold text-base text-slate-900 dark:text-white">Primary Science: Series Circuit Electricity</span>
          </div>
          <button onclick="toggleVideoModal()" class="w-8 h-8 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 font-bold hover:bg-slate-200 flex items-center justify-center">✕</button>
        </div>
        <div class="aspect-video w-full rounded-xl overflow-hidden bg-black shadow-inner">
          <video id="lessonVideo" controls class="w-full h-full object-contain">
            <source src="Primary Science PSLE Revision Guide EP 18 _ Electricity _ Electricity in Series.mp4" type="video/mp4">
            Your browser does not support HTML5 video.
          </video>
        </div>
      </div>
    </div>

  </div>

  <script>
    let currentMaterial = null;
    let isKnifeSwitchClosed = true;
    let score = 0;
    let audioEnabled = true;
    let isDarkMode = false;
    const answered = {};

    // Theme Mode Toggle (Day / Night)
    function toggleThemeMode() {
      isDarkMode = !isDarkMode;
      document.body.classList.toggle('dark-mode', isDarkMode);
      document.getElementById('theme-icon').textContent = isDarkMode ? '🌙' : '☀️';
      document.getElementById('theme-text').textContent = isDarkMode ? 'Night (Dark)' : 'Day (Studio)';
      playTone(500, 'sine', 0.06);
    }

    // Web Audio Synthesizer
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
      playTone(523.25, 'sine', 0.1); // C5
      setTimeout(() => playTone(659.25, 'sine', 0.15), 100); // E5
      setTimeout(() => playTone(783.99, 'sine', 0.25), 220); // G5
    }

    function toggleAudio() {
      audioEnabled = !audioEnabled;
      document.getElementById('audio-text').textContent = audioEnabled ? 'Audio: ON' : 'Audio: OFF';
      document.getElementById('audio-icon').textContent = audioEnabled ? '🔊' : '🔇';
    }

    function toggleVideoModal() {
      const modal = document.getElementById('videoModal');
      const vid = document.getElementById('lessonVideo');
      if (modal.classList.contains('hidden')) {
        modal.classList.remove('hidden');
        vid.play().catch(() => {});
      } else {
        modal.classList.add('hidden');
        vid.pause();
      }
    }

    function toggleKnifeSwitch() {
      isKnifeSwitchClosed = !isKnifeSwitchClosed;
      const blade = document.getElementById('knife-blade');
      const text = document.getElementById('switch-pill-text');
      
      if (isKnifeSwitchClosed) {
        blade.setAttribute('transform', 'rotate(0, 30, 30)');
        text.textContent = 'CLOSED (ON)';
        text.className = 'text-emerald-700 dark:text-emerald-400 font-black';
        playTone(320, 'triangle', 0.08);
      } else {
        blade.setAttribute('transform', 'rotate(-38, 30, 30)');
        text.textContent = 'OPEN (OFF)';
        text.className = 'text-rose-700 dark:text-rose-400 font-black';
        playTone(220, 'sawtooth', 0.08);
      }
      
      updateCircuitState();
    }

    // Live HTML5 Canvas Electron Particle Engine (Crystal Clear Visual Metaphors)
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
          // Jiggle in locked lattice
          this.phase += 0.15;
          this.x = this.baseX + Math.sin(this.phase) * 1.5;
          this.y = this.baseY + Math.cos(this.phase) * 1.5;
        }
      }
      draw() {
        ctx.beginPath();
        if (this.type === 'coin') {
          ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
          ctx.fillStyle = '#38bdf8'; // Free sea of copper conduction electrons
          ctx.shadowColor = '#0284c7';
          ctx.shadowBlur = 4;
          ctx.fill();
          ctx.shadowBlur = 0;
        } else if (this.type === 'pencil') {
          ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
          ctx.fillStyle = '#60a5fa'; // Delocalized pi electrons
          ctx.shadowColor = '#2563eb';
          ctx.shadowBlur = 4;
          ctx.fill();
          ctx.shadowBlur = 0;
        } else {
          ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
          ctx.fillStyle = '#f43f5e'; // Tightly bound valence electrons
          ctx.fill();
        }
      }
    }

    function initParticles(type) {
      particles = [];
      if (type === 'coin') {
        // Sea of free electrons drifting through copper atoms
        for (let i = 0; i < 40; i++) {
          particles.push(new ChargeParticle('coin', Math.random() * 370 + 15, Math.random() * 110 + 16));
        }
      } else if (type === 'pencil') {
        // Free electrons sliding between two carbon graphene sheets
        for (let i = 0; i < 30; i++) {
          particles.push(new ChargeParticle('pencil', Math.random() * 370 + 15, 68 + (Math.random() - 0.5) * 16));
        }
      } else {
        // Rigid bound lattice with locked electrons
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
        // Copper Metal Atoms Channel
        ctx.fillStyle = '#1e293b';
        ctx.fillRect(10, 10, 380, 124);
        
        // Copper Atom Cores
        for (let r = 0; r < 3; r++) {
          for (let c = 0; c < 7; c++) {
            const ix = c * 52 + 42;
            const iy = r * 38 + 32;
            ctx.beginPath();
            ctx.arc(ix, iy, 12, 0, Math.PI * 2);
            ctx.fillStyle = '#b45309';
            ctx.fill();
            ctx.strokeStyle = '#f59e0b';
            ctx.lineWidth = 1.5;
            ctx.stroke();
            ctx.fillStyle = '#ffffff';
            ctx.font = 'bold 9px Outfit';
            ctx.textAlign = 'center';
            ctx.fillText('Cu', ix, iy + 3);
          }
        }
        // Update and draw flowing electron sea
        particles.forEach(p => {
          p.update(isConducting);
          p.draw();
        });

        // Overlay status header
        ctx.fillStyle = isConducting ? '#38bdf8' : '#94a3b8';
        ctx.font = 'bold 10px JetBrains Mono';
        ctx.textAlign = 'left';
        ctx.fillText(isConducting ? '⚡ Free Electrons Flowing Through Metal (Conductor)' : '⏸ Circuit Open: Free Electrons at Rest', 20, 24);

      } else if (currentMaterial === 'pencil') {
        // Graphene Hexagonal Layers
        ctx.fillStyle = '#1e293b';
        ctx.fillRect(10, 10, 380, 124);

        // Carbon Sheet 1 (Top)
        ctx.strokeStyle = '#64748b';
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.moveTo(20, 45); ctx.lineTo(380, 45);
        ctx.stroke();
        ctx.fillStyle = '#cbd5e1';
        ctx.font = 'bold 9px JetBrains Mono';
        ctx.textAlign = 'left';
        ctx.fillText('CARBON ATOM SHEET 1 (GRAPHITE)', 25, 38);

        // Carbon Sheet 2 (Bottom)
        ctx.beginPath();
        ctx.moveTo(20, 95); ctx.lineTo(380, 95);
        ctx.stroke();
        ctx.fillText('CARBON ATOM SHEET 2 (GRAPHITE)', 25, 110);

        // Electrons drifting in between
        particles.forEach(p => {
          p.update(isConducting);
          p.draw();
        });

        ctx.fillStyle = isConducting ? '#60a5fa' : '#94a3b8';
        ctx.font = 'bold 10px JetBrains Mono';
        ctx.fillText(isConducting ? '⚡ Electrons Sliding Between Carbon Sheets' : '⏸ Switch Open: No Current Flow', 25, 72);

      } else {
        // Locked Insulator Lattice
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

    // Specimen Selection
    function selectMaterial(mat) {
      currentMaterial = mat;

      // Update button visual states
      document.querySelectorAll('.shelf-card').forEach(c => c.classList.remove('active-selected'));
      const activeBtn = document.getElementById('btn-mat-' + mat);
      if (activeBtn) activeBtn.classList.add('active-selected');

      // Update SVG Specimen Display
      ['none', 'coin', 'eraser', 'pencil', 'ruler'].forEach(k => {
        const el = document.getElementById('item-' + k);
        if (el) el.setAttribute('display', k === mat ? 'block' : 'none');
      });

      // Update Split Inspector
      updateInspectorContent(mat);
      initParticles(mat);
      updateCircuitState();
    }

    function updateCircuitState() {
      const isConductor = currentMaterial === 'coin' || currentMaterial === 'pencil';
      const isComplete = isConductor && isKnifeSwitchClosed;

      const pill = document.getElementById('circuit-status-pill');
      const hint = document.getElementById('assistant-hint');
      const stream = document.getElementById('electron-stream-group');
      const glow = document.getElementById('lamp-glow');
      const fil = document.getElementById('lamp-filament');
      const meterV = document.getElementById('meter-v-text');
      const meterI = document.getElementById('meter-i-text');
      const stationLabel = document.getElementById('specimen-station-label');

      if (isComplete) {
        pill.textContent = 'CLOSED LOOP • 0.28 A (FLOWING)';
        pill.className = 'text-[10px] font-mono font-bold uppercase px-2.5 py-0.5 rounded-full bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-300 dark:border-emerald-800 text-emerald-800 dark:text-emerald-300';
        hint.innerHTML = `<span class="text-emerald-700 dark:text-emerald-400 font-bold">SUCCESS!</span> <b>${currentMaterial === 'coin' ? '1p Copper Coin' : 'Pencil Graphite'}</b> is an electrical conductor. Electrons flow freely, completing the series loop!`;
        stationLabel.textContent = currentMaterial === 'coin' ? '1p Copper Coin: Conductor (Loop Closed)' : 'Pencil Lead: Non-Metal Conductor (Loop Closed)';
        stationLabel.setAttribute('fill', '#34d399');

        stream.setAttribute('display', 'block');
        glow.setAttribute('opacity', '1');
        fil.setAttribute('stroke', '#ffffff');
        meterV.textContent = 'VOLTS: 3.00 V';
        meterI.textContent = 'CURRENT: 0.28 A';
        meterI.className = 'text-emerald-600 dark:text-emerald-400 font-black';

        playSuccessChime();
      } else {
        const reason = !isKnifeSwitchClosed ? 'Knife switch is OPEN' : !currentMaterial ? 'Air gap break between clips' : 'Material is an INSULATOR';
        pill.textContent = 'LOOP OPEN • 0.00 A';
        pill.className = 'text-[10px] font-mono font-bold uppercase px-2.5 py-0.5 rounded-full bg-rose-50 dark:bg-rose-950/60 border border-rose-300 dark:border-rose-800 text-rose-800 dark:text-rose-300';
        hint.innerHTML = `<span class="text-rose-700 dark:text-rose-400 font-bold">CIRCUIT BROKEN:</span> ${reason}. Current cannot cross the gap; lamp remains OFF.`;
        stationLabel.textContent = !currentMaterial ? 'Awaiting specimen selection' : currentMaterial === 'eraser' ? 'Rubber Eraser: Insulator (Circuit Broken)' : currentMaterial === 'ruler' ? 'Plastic Ruler: Insulator (Circuit Broken)' : 'Knife Switch Open: Current Halted';
        stationLabel.setAttribute('fill', '#f87171');

        stream.setAttribute('display', 'none');
        glow.setAttribute('opacity', '0');
        fil.setAttribute('stroke', '#475569');
        meterV.textContent = 'VOLTS: 3.00 V';
        meterI.textContent = 'CURRENT: 0.00 A';
        meterI.className = 'text-rose-600 dark:text-rose-400 font-black';

        if (currentMaterial && isKnifeSwitchClosed) {
          playTone(200, 'square', 0.1);
        }
      }
    }

    function updateInspectorContent(mat) {
      const badge = document.getElementById('showcase-badge');
      const macroStage = document.getElementById('macro-vector-stage');
      const macroMeta = document.getElementById('macro-spec-meta');
      const atomicMeta = document.getElementById('atomic-spec-meta');

      if (mat === 'coin') {
        badge.textContent = 'COPPER COIN (ELECTRICAL CONDUCTOR)';
        badge.className = 'text-[10px] font-mono font-bold px-3 py-1 rounded-full bg-emerald-100 dark:bg-emerald-950 text-emerald-800 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-800';

        macroStage.innerHTML = `
          <g transform="translate(160, 60)">
            <circle r="46" fill="url(#realCopper)" stroke="#7c2d12" stroke-width="2.5"/>
            <circle r="40" fill="none" stroke="#fed7aa" stroke-width="1.5" stroke-dasharray="4,3"/>
            <path d="M -15 -14 L -9 -22 L 0 -16 L 9 -22 L 15 -14 L 12 -8 L -12 -8 Z" fill="#fed7aa" stroke="#c2410c" stroke-width="1"/>
            <text y="14" text-anchor="middle" fill="#fed7aa" font-size="24" font-weight="900" font-family="serif">1</text>
            <text y="28" text-anchor="middle" fill="#ffffff" font-size="9" font-weight="900" font-family="sans-serif">ONE PENNY</text>
          </g>
        `;
        macroMeta.innerHTML = "<b>Cambridge Key Fact:</b> British 1p and 2p coins are copper-plated steel. Copper is a metal with a sea of free electrons that carry electric current instantly.";
        atomicMeta.innerHTML = "<b class='text-blue-600 dark:text-blue-400'>Plain-English Science:</b> Free electrons flow through copper atoms like water through a pipe, lighting the bulb.";

        playTone(600, 'sine', 0.08);

      } else if (mat === 'pencil') {
        badge.textContent = 'GRAPHITE PENCIL (NON-METAL CONDUCTOR)';
        badge.className = 'text-[10px] font-mono font-bold px-3 py-1 rounded-full bg-emerald-100 dark:bg-emerald-950 text-emerald-800 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-800';

        macroStage.innerHTML = `
          <g transform="translate(40, 40)">
            <rect x="0" y="8" width="160" height="24" rx="4" fill="#d97706" stroke="#b45309" stroke-width="2"/>
            <line x1="0" y1="20" x2="160" y2="20" stroke="#f59e0b" stroke-width="2"/>
            <text x="80" y="24" fill="#ffffff" font-size="9" font-weight="900" font-family="monospace" text-anchor="middle">HB GRAPHITE CORE</text>
            <polygon points="160,8 210,20 160,32" fill="#fed7aa" stroke="#d97706" stroke-width="1.5"/>
            <polygon points="190,15 220,20 190,25" fill="#0f172a" stroke="#000000" stroke-width="1.5"/>
            <text x="210" y="44" fill="#64748b" font-size="9" font-weight="800" font-family="monospace">Exposed Carbon Tip</text>
          </g>
        `;
        macroMeta.innerHTML = "<b>Cambridge Key Fact:</b> Pencil lead contains <i>zero</i> toxic lead; it is pure layered carbon (graphite) mixed with clay.";
        atomicMeta.innerHTML = "<b class='text-blue-600 dark:text-blue-400'>Plain-English Science:</b> Carbon atoms bond in flat sheets, leaving loose electrons that slide between layers to conduct electricity.";

        playTone(550, 'sine', 0.08);

      } else if (mat === 'eraser') {
        badge.textContent = 'VULCANIZED RUBBER (ELECTRICAL INSULATOR)';
        badge.className = 'text-[10px] font-mono font-bold px-3 py-1 rounded-full bg-rose-100 dark:bg-rose-950 text-rose-800 dark:text-rose-300 border border-rose-300 dark:border-rose-800';

        macroStage.innerHTML = `
          <g transform="translate(80, 30)">
            <rect x="0" y="0" width="160" height="60" rx="8" fill="#fb7185" stroke="#e11d48" stroke-width="2"/>
            <rect x="0" y="0" width="45" height="60" rx="8" fill="#38bdf8" stroke="#0284c7" stroke-width="2"/>
            <text x="105" y="36" fill="#ffffff" font-size="14" font-weight="900" font-family="sans-serif" text-anchor="middle">CLASSIC RUBBER</text>
          </g>
        `;
        macroMeta.innerHTML = "<b>Cambridge Key Fact:</b> Rubber has tight chemical bonds that hold all electrons trapped in place so no electric current can pass.";
        atomicMeta.innerHTML = "<b class='text-rose-600 dark:text-rose-400'>Plain-English Science:</b> All electrons are locked in place. With zero free electrons, the circuit stays broken.";

        playTone(180, 'square', 0.08);

      } else if (mat === 'ruler') {
        badge.textContent = 'PLASTIC RULER (ELECTRICAL INSULATOR)';
        badge.className = 'text-[10px] font-mono font-bold px-3 py-1 rounded-full bg-rose-100 dark:bg-rose-950 text-rose-800 dark:text-rose-300 border border-rose-300 dark:border-rose-800';

        macroStage.innerHTML = `
          <g transform="translate(30, 35)">
            <rect x="0" y="0" width="260" height="50" rx="6" fill="#e0f2fe" stroke="#0284c7" stroke-width="2" fill-opacity="0.8"/>
            <line x1="20" y1="0" x2="20" y2="15" stroke="#0369a1" stroke-width="2"/>
            <line x1="50" y1="0" x2="50" y2="25" stroke="#0369a1" stroke-width="2"/>
            <text x="50" y="38" fill="#0369a1" font-size="10" font-weight="900">1 cm</text>
            <line x1="120" y1="0" x2="120" y2="25" stroke="#0369a1" stroke-width="2"/>
            <text x="120" y="38" fill="#0369a1" font-size="10" font-weight="900">2 cm</text>
            <line x1="190" y1="0" x2="190" y2="25" stroke="#0369a1" stroke-width="2"/>
            <text x="190" y="38" fill="#0369a1" font-size="10" font-weight="900">3 cm</text>
          </g>
        `;
        macroMeta.innerHTML = "<b>Cambridge Safety Application:</b> Electricians use plastic handles and rubber boots because plastic blocks electricity and prevents electric shocks.";
        atomicMeta.innerHTML = "<b class='text-rose-600 dark:text-rose-400'>Plain-English Science:</b> Plastic molecules bind electrons firmly. No electrons can move through the gap.";

        playTone(180, 'square', 0.08);
      }
    }

    function answerQuestion(qNum, optLetter, isCorrect) {
      if (answered[qNum]) return;
      answered[qNum] = true;

      const buttons = document.querySelectorAll('.q' + qNum + '-opt');
      buttons.forEach(btn => {
        btn.disabled = true;
        if (btn.textContent.includes(optLetter + ')')) {
          btn.className = "q" + qNum + "-opt quiz-opt-btn tactile-btn text-left p-3 rounded-xl border font-bold " + (isCorrect ? "bg-emerald-50 dark:bg-emerald-950/70 border-emerald-500 text-emerald-800 dark:text-emerald-200" : "bg-rose-50 dark:bg-rose-950/70 border-rose-500 text-rose-800 dark:text-rose-200");
        }
      });

      const fb = document.getElementById('feedback-' + qNum);
      fb.classList.remove('hidden');

      if (isCorrect) {
        score++;
        fb.className = "text-xs p-3.5 rounded-xl font-medium bg-emerald-50 dark:bg-emerald-950/50 text-emerald-800 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800";
        fb.innerHTML = "<b>Correct! 🌟</b> " + (qNum === 1 ? "The buzzer sounds because the material conducts electricity and completes the circuit." : qNum === 2 ? "Graphite layers have free delocalized electrons that move under voltage." : "In a series circuit, there is only one pathway. Breaking any component stops current everywhere.");
        playSuccessChime();
      } else {
        fb.className = "text-xs p-3.5 rounded-xl font-medium bg-rose-50 dark:bg-rose-950/50 text-rose-800 dark:text-rose-300 border border-rose-200 dark:border-rose-800";
        fb.innerHTML = "<b>Incorrect.</b> " + (qNum === 1 ? "Conducting materials complete the loop and allow current to sound the buzzer." : qNum === 2 ? "Graphite has free mobile electrons between its carbon layers, unlike other non-metals." : "In series, if one bulb goes off, the entire loop breaks and all other bulbs turn off.");
        playTone(180, 'square', 0.08);
      }

      document.getElementById('quiz-score-badge').textContent = "Score: " + score + " / 3";
      if (score === 3) {
        document.getElementById('quiz-score-badge').className = "text-xs bg-emerald-100 dark:bg-emerald-950 text-emerald-800 dark:text-emerald-300 font-extrabold px-3 py-1 rounded-full border border-emerald-300 dark:border-emerald-800";
      }
    }
  </script>
</body>
</html>
