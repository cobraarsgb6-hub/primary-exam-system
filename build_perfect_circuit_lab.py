import os

html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Cambridge Stage 6 Science | Professional Electric Circuit Studio</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;600;700;800&display=swap" rel="stylesheet">
  <style>
    body {
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }
    .font-mono { font-family: 'JetBrains Mono', monospace; font-variant-numeric: tabular-nums; }
    
    /* Tactile Micro-Interactions */
    .tactile-btn {
      transition: transform 0.12s cubic-bezier(0.2, 0, 0, 1), background-color 0.15s ease, border-color 0.15s ease, box-shadow 0.15s ease;
    }
    .tactile-btn:active {
      transform: scale(0.96) !important;
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
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .shelf-card:hover {
      transform: translateY(-3px);
      box-shadow: 0 12px 25px -5px rgba(0, 0, 0, 0.5);
    }
    .shelf-card.active-selected {
      border-color: #3b82f6 !important;
      background: linear-gradient(145deg, #1e293b 0%, #0f172a 100%) !important;
      box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.5), 0 10px 25px -5px rgba(59, 130, 246, 0.3) !important;
    }
  </style>
</head>
<body class="bg-[#070b14] text-slate-100 antialiased min-h-screen p-3 sm:p-6 lg:p-8 selection:bg-blue-600 selection:text-white">

  <div class="max-w-5xl mx-auto space-y-6">

    <!-- 1. HEADER: BRAND & CONTROLS -->
    <header class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-[#0f172a] border border-slate-800 rounded-3xl p-5 sm:p-6 shadow-2xl">
      <div class="space-y-1">
        <div class="flex items-center gap-2">
          <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
          <span class="text-[11px] font-black uppercase tracking-wider text-blue-400 font-mono">Cambridge Primary Stage 6 • Physics</span>
          <span class="text-slate-600">•</span>
          <span class="text-xs text-slate-400 font-bold">Manaret El-Eman British International School</span>
        </div>
        <h1 class="text-xl sm:text-2xl font-black text-white tracking-tight">Interactive Circuit Workbench & Conduction Lab</h1>
        <p class="text-xs text-slate-400 font-medium">
          Investigator: <b class="text-slate-200">Mostafa Ahmed (Grade 6)</b> • Pure visual physics with zero wire-text collision.
        </p>
      </div>

      <div class="flex items-center gap-2 self-start sm:self-center">
        <button onclick="toggleAudio()" id="btn-audio" class="tactile-btn px-3.5 py-2 rounded-xl text-xs font-bold bg-slate-800 border border-slate-700 hover:bg-slate-700 text-slate-300 flex items-center gap-1.5" title="Toggle Audio Feedback">
          <span id="audio-icon">🔊</span>
          <span id="audio-text">Audio: ON</span>
        </button>

        <button onclick="toggleVideoModal()" class="tactile-btn px-4 py-2 rounded-xl text-xs font-black bg-blue-600 hover:bg-blue-500 text-white flex items-center gap-2 shadow-lg shadow-blue-600/30">
          <span>🎬</span>
          <span>Cambridge Video Lesson</span>
        </button>
      </div>
    </header>

    <!-- 2. THE 3D PHYSICS WORKBENCH (ZERO TEXT COLLISION • CRISP NATIVE HTML LABELS) -->
    <main class="bg-[#0f172a] border border-slate-800 rounded-3xl p-5 sm:p-6 shadow-2xl space-y-5">
      
      <!-- STATUS CONSOLE BAR -->
      <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800/80 pb-4">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-2xl bg-blue-950/80 border border-blue-800 text-blue-400 flex items-center justify-center font-black text-lg shadow-inner">
            ⚡
          </div>
          <div>
            <div class="flex items-center gap-2">
              <span class="text-xs font-black text-white">Circuit Continuity Diagnostic</span>
              <span id="circuit-status-pill" class="text-[10px] font-mono font-black uppercase px-2.5 py-0.5 rounded-full bg-rose-950 border border-rose-800 text-rose-400">
                LOOP OPEN • 0.00 A
              </span>
            </div>
            <p id="assistant-hint" class="text-xs text-slate-400 font-medium mt-0.5">
              Select an object from the shelf below to bridge the crocodile clips on the board.
            </p>
          </div>
        </div>

        <div class="flex items-center gap-2">
          <button onclick="toggleKnifeSwitch()" id="btn-switch" class="tactile-btn px-3.5 py-2 rounded-xl text-xs font-extrabold bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-200 flex items-center gap-2">
            <span>🔌 Knife Switch:</span>
            <span id="switch-pill-text" class="text-emerald-400 font-black">CLOSED (ON)</span>
          </button>
        </div>
      </div>

      <!-- WORKBENCH VISUAL CANVAS (PURE SILICONE CHASSIS • ZERO EMBEDDED TEXT COLLISION) -->
      <div class="w-full bg-[#030712] rounded-2xl border border-slate-800/90 overflow-hidden shadow-inner relative p-2 sm:p-4">
        
        <!-- Component Labels Bar (Crisp Native HTML - Above the Wires) -->
        <div class="grid grid-cols-4 gap-2 text-center pb-2 px-4 text-[11px] font-mono font-bold text-slate-400">
          <div class="flex items-center justify-center gap-1.5 text-blue-400">
            <span>🔋</span><span>3.0V DC Cell</span>
          </div>
          <div class="flex items-center justify-center gap-1.5 text-amber-400 cursor-pointer" onclick="toggleKnifeSwitch()">
            <span>🔌</span><span>Knife Switch</span>
          </div>
          <div class="flex items-center justify-center gap-1.5 text-emerald-400">
            <span>🧲</span><span>Test Gap Bridge</span>
          </div>
          <div class="flex items-center justify-center gap-1.5 text-yellow-400">
            <span>💡</span><span>3.0V Lamp Socket</span>
          </div>
        </div>

        <!-- SVG Physics Canvas (All Text Removed From Under Wires!) -->
        <svg viewBox="0 0 840 320" class="w-full h-auto select-none" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <!-- Silicone Chassis Slate Board -->
            <linearGradient id="chassisGrad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stop-color="#1e293b"/>
              <stop offset="100%" stop-color="#0f172a"/>
            </linearGradient>

            <!-- Warm Lamp Radial Glow -->
            <radialGradient id="lampGlowEffect" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stop-color="#ffffff" stop-opacity="1"/>
              <stop offset="25%" stop-color="#fef08a" stop-opacity="0.95"/>
              <stop offset="60%" stop-color="#facc15" stop-opacity="0.4"/>
              <stop offset="100%" stop-color="#ca8a04" stop-opacity="0"/>
            </radialGradient>

            <!-- Gold Brass Clips -->
            <linearGradient id="brassGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#fef08a"/>
              <stop offset="35%" stop-color="#f59e0b"/>
              <stop offset="75%" stop-color="#b45309"/>
              <stop offset="100%" stop-color="#78350f"/>
            </linearGradient>

            <!-- Copper Coin -->
            <linearGradient id="coinGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#ffedd5"/>
              <stop offset="30%" stop-color="#fb923c"/>
              <stop offset="70%" stop-color="#c2410c"/>
              <stop offset="100%" stop-color="#7c2d12"/>
            </linearGradient>

            <filter id="wireShadow" x="-10%" y="-10%" width="120%" height="130%">
              <feDropShadow dx="0" dy="5" stdDeviation="4" flood-color="#000000" flood-opacity="0.7"/>
            </filter>
          </defs>

          <!-- 1. MODULAR ELECTRONIC CHASSIS BOARD -->
          <rect x="20" y="15" width="800" height="290" rx="20" fill="url(#chassisGrad)" stroke="#334155" stroke-width="2"/>
          <!-- Chassis Grid -->
          <line x1="20" y1="160" x2="820" y2="160" stroke="#334155" stroke-width="0.8" stroke-dasharray="4,4" opacity="0.3"/>
          <line x1="220" y1="15" x2="220" y2="305" stroke="#334155" stroke-width="0.8" stroke-dasharray="4,4" opacity="0.3"/>
          <line x1="420" y1="15" x2="420" y2="305" stroke="#334155" stroke-width="0.8" stroke-dasharray="4,4" opacity="0.3"/>
          <line x1="620" y1="15" x2="620" y2="305" stroke="#334155" stroke-width="0.8" stroke-dasharray="4,4" opacity="0.3"/>

          <!-- 2. CIRCUIT COMPONENTS (NO INTERNAL TEXT LABELS TO BE CROSSED) -->

          <!-- (A) BATTERY PACK (Pos terminal at 190, 85 | Neg terminal at 110, 180) -->
          <g id="comp-battery" transform="translate(60, 60)" filter="url(#wireShadow)">
            <!-- ABS Case -->
            <rect x="0" y="0" width="140" height="150" rx="14" fill="#020617" stroke="#1e293b" stroke-width="2"/>
            <!-- AA Cell 1 -->
            <rect x="18" y="16" width="45" height="115" rx="6" fill="#1e3a8a" stroke="#3b82f6" stroke-width="1.5"/>
            <rect x="33" y="6" width="15" height="10" rx="3" fill="#cbd5e1"/>
            <!-- AA Cell 2 -->
            <rect x="77" y="16" width="45" height="115" rx="6" fill="#1e3a8a" stroke="#3b82f6" stroke-width="1.5"/>
            <rect x="92" y="131" width="15" height="10" rx="3" fill="#cbd5e1"/>
            <!-- Red (+) Terminal Stud -->
            <circle cx="130" cy="25" r="9" fill="#ef4444" stroke="#991b1b" stroke-width="2"/>
            <!-- Black (-) Terminal Stud -->
            <circle cx="10" cy="120" r="9" fill="#0f172a" stroke="#475569" stroke-width="2"/>
          </g>

          <!-- (B) KNIFE SWITCH (Left terminal at 300, 70 | Right terminal at 380, 70) -->
          <g id="comp-switch" transform="translate(270, 40)" onclick="toggleKnifeSwitch()" class="cursor-pointer" filter="url(#wireShadow)">
            <rect x="0" y="0" width="110" height="60" rx="10" fill="#020617" stroke="#1e293b" stroke-width="2"/>
            <!-- Brass Hinges -->
            <circle cx="30" cy="30" r="8" fill="#d97706" stroke="#78350f" stroke-width="1.5"/>
            <circle cx="80" cy="30" r="8" fill="#d97706" stroke="#78350f" stroke-width="1.5"/>
            <!-- Blade -->
            <line id="switch-blade-line" x1="30" y1="30" x2="80" y2="30" stroke="#f59e0b" stroke-width="6" stroke-linecap="round" class="transition-all duration-300"/>
            <circle id="switch-handle-circle" cx="80" cy="30" r="7" fill="#dc2626" class="transition-all duration-300"/>
          </g>

          <!-- (C) EDISON LAMP (Terminal at 680, 100) -->
          <g id="comp-lamp" transform="translate(640, 45)" filter="url(#wireShadow)">
            <!-- Volumetric Glow Halo -->
            <circle id="bulb-volumetric-glow" cx="45" cy="45" r="75" fill="url(#lampGlowEffect)" opacity="0" class="transition-opacity duration-300 pointer-events-none"/>
            <!-- Porcelain Base -->
            <rect x="10" y="70" width="70" height="25" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
            <!-- Brass Screw Collar -->
            <rect x="25" y="55" width="40" height="16" rx="2" fill="#d97706" stroke="#b45309" stroke-width="1"/>
            <!-- Glass Bulb -->
            <circle id="bulb-glass-sphere" cx="45" cy="35" r="32" fill="#1e293b" stroke="#64748b" stroke-width="2" opacity="0.9" class="transition-colors duration-300"/>
            <!-- Filament Coil -->
            <path id="bulb-filament-path" d="M 35 45 L 40 30 L 45 38 L 50 30 L 55 45" fill="none" stroke="#475569" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="transition-colors duration-300"/>
            <!-- Lamp Screw Terminals -->
            <circle cx="15" cy="82" r="6" fill="#ef4444" stroke="#991b1b" stroke-width="1.5"/>
            <circle cx="75" cy="82" r="6" fill="#2563eb" stroke="#1d4ed8" stroke-width="1.5"/>
          </g>

          <!-- (D) SPECIMEN TEST STATION (Left clip: 360, 230 | Right clip: 480, 230) -->
          <g id="comp-specimen-station" transform="translate(340, 180)" filter="url(#wireShadow)">
            <!-- Ceramic Test Pad -->
            <rect x="0" y="0" width="160" height="90" rx="16" fill="#020617" stroke="#1e293b" stroke-width="2"/>
            
            <!-- Dynamic Material Display in Center -->
            <g id="specimen-group" transform="translate(35, 15)">
              <!-- Empty -->
              <g id="item-empty" display="inline">
                <circle cx="45" cy="30" r="22" fill="#0f172a" stroke="#334155" stroke-width="1.5" stroke-dasharray="4,4"/>
                <text x="45" y="37" text-anchor="middle" font-size="20">❓</text>
              </g>
              <!-- Coin -->
              <g id="item-coin" display="none">
                <circle cx="45" cy="30" r="26" fill="url(#coinGrad)" stroke="#7c2d12" stroke-width="2.5"/>
                <circle cx="45" cy="30" r="21" fill="none" stroke="#ffedd5" stroke-width="1" stroke-dasharray="3,2"/>
                <text x="45" y="34" text-anchor="middle" fill="#fef3c7" font-size="9" font-weight="900">£1 COIN</text>
              </g>
              <!-- Eraser -->
              <g id="item-eraser" display="none">
                <polygon points="15,22 65,14 75,38 25,46" fill="#f43f5e" stroke="#be123c" stroke-width="2"/>
                <polygon points="65,14 75,38 80,35 70,11" fill="#3b82f6" stroke="#1d4ed8" stroke-width="2"/>
                <text x="45" y="34" text-anchor="middle" fill="#ffffff" font-size="8.5" font-weight="900">RUBBER</text>
              </g>
              <!-- Pencil -->
              <g id="item-pencil" display="none">
                <polygon points="10,32 60,26 60,34 10,40" fill="#eab308" stroke="#a16207" stroke-width="1.5"/>
                <polygon points="60,26 72,30 60,34" fill="#fed7aa"/>
                <polygon points="69,29 78,30 69,31" fill="#0f172a"/>
                <text x="35" y="35" text-anchor="middle" fill="#78350f" font-size="7" font-weight="900">GRAPHITE</text>
              </g>
              <!-- Ruler -->
              <g id="item-ruler" display="none">
                <polygon points="10,20 78,20 74,38 6,38" fill="#38bdf8" fill-opacity="0.55" stroke="#0284c7" stroke-width="1.5"/>
                <line x1="22" y1="20" x2="22" y2="28" stroke="#0369a1" stroke-width="1.2"/>
                <line x1="38" y1="20" x2="38" y2="28" stroke="#0369a1" stroke-width="1.2"/>
                <line x1="54" y1="20" x2="54" y2="28" stroke="#0369a1" stroke-width="1.2"/>
                <text x="42" y="32" text-anchor="middle" fill="#0369a1" font-size="7.5" font-weight="900">PLASTIC</text>
              </g>
            </g>

            <!-- Left Crocodile Clip -->
            <g id="clip-left" transform="translate(15, 36)">
              <rect x="-14" y="0" width="22" height="16" rx="2.5" fill="url(#brassGrad)" stroke="#78350f" stroke-width="1"/>
              <polygon points="8,1 20,8 8,15" fill="#92400e"/>
            </g>
            <!-- Right Crocodile Clip -->
            <g id="clip-right" transform="translate(125, 36)">
              <rect x="2" y="0" width="22" height="16" rx="2.5" fill="url(#brassGrad)" stroke="#78350f" stroke-width="1"/>
              <polygon points="2,1 -10,8 2,15" fill="#92400e"/>
            </g>
          </g>

          <!-- 3. SILICONE JUMPER LEADS (CURVING FREELY WITH ZERO TEXT OVERLAP!) -->
          
          <!-- WIRE 1 (RED): Battery (+) (190, 85) -> Switch Left (300, 70) -->
          <path d="M 190 85 Q 240 60 300 70" fill="none" stroke="#dc2626" stroke-width="4.5" stroke-linecap="round"/>
          
          <!-- WIRE 2 (RED): Switch Right (350, 70) -> Lamp Left Terminal (655, 127) -->
          <path d="M 350 70 Q 500 40 655 127" fill="none" stroke="#dc2626" stroke-width="4.5" stroke-linecap="round"/>
          
          <!-- WIRE 3 (BLUE): Lamp Right Terminal (715, 127) -> Specimen Right Clip (465, 224) -->
          <path d="M 715 127 Q 660 250 465 224" fill="none" stroke="#2563eb" stroke-width="4.5" stroke-linecap="round"/>
          
          <!-- WIRE 4 (BLACK): Specimen Left Clip (355, 224) -> Battery (-) Terminal (70, 180) -->
          <path d="M 355 224 Q 220 270 70 180" fill="none" stroke="#1e293b" stroke-width="4.5" stroke-linecap="round"/>

          <!-- 4. REAL-TIME ELECTRON STREAM (OVER WIRES WITH ZERO TEXT COLLISION) -->
          <g id="electron-stream-group" display="none">
            <path d="M 190 85 Q 240 60 300 70" fill="none" stroke="#fef08a" stroke-width="2.5" class="electron-flow-active"/>
            <path d="M 350 70 Q 500 40 655 127" fill="none" stroke="#fef08a" stroke-width="2.5" class="electron-flow-active"/>
            <path d="M 715 127 Q 660 250 465 224" fill="none" stroke="#fef08a" stroke-width="2.5" class="electron-flow-active"/>
            <path d="M 375 224 L 445 224" fill="none" stroke="#fef08a" stroke-width="3.5" class="electron-flow-active"/>
            <path d="M 355 224 Q 220 270 70 180" fill="none" stroke="#fef08a" stroke-width="2.5" class="electron-flow-active"/>
          </g>

        </svg>

        <!-- Digital Multimeter HUD (Clean Native HTML Card in Bottom Right) -->
        <div class="absolute bottom-4 right-4 bg-slate-900/90 border border-slate-700/80 rounded-xl p-3 shadow-xl backdrop-blur-sm">
          <div class="text-[10px] font-mono font-bold text-slate-400 mb-1">DIGITAL MULTIMETER</div>
          <div class="flex items-center gap-3 font-mono font-black text-xs">
            <span id="meter-v-text" class="text-sky-400">VOLTS: 3.00 V</span>
            <span id="meter-i-text" class="text-rose-400">CURRENT: 0.00 A</span>
          </div>
        </div>

      </div>

      <!-- 3. SPECIMEN SELECTION SHELF -->
      <div class="space-y-3">
        <div class="flex items-center justify-between text-xs font-bold text-slate-400">
          <span>🧰 Student Specimen Shelf (Click to place in circuit gap):</span>
          <span class="text-blue-400 font-extrabold text-[11px]">Instant Reaction</span>
        </div>

        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3.5">
          
          <!-- Tool 1: Metal Coin -->
          <button onclick="selectMaterial('coin')" id="btn-mat-coin" class="shelf-card tactile-btn bg-slate-900/90 border border-slate-800 rounded-2xl p-4 flex flex-col items-center justify-center text-center space-y-2 group cursor-pointer">
            <div class="w-12 h-12 rounded-2xl bg-amber-950/40 border border-amber-800/60 flex items-center justify-center text-2xl group-hover:scale-110 transition-transform">
              🪙
            </div>
            <div>
              <div class="font-black text-sm text-slate-100">Copper Coin</div>
              <div class="text-[11px] text-emerald-400 font-extrabold mt-0.5">Pure Metal (Conductor)</div>
            </div>
          </button>

          <!-- Tool 2: Rubber Eraser -->
          <button onclick="selectMaterial('eraser')" id="btn-mat-eraser" class="shelf-card tactile-btn bg-slate-900/90 border border-slate-800 rounded-2xl p-4 flex flex-col items-center justify-center text-center space-y-2 group cursor-pointer">
            <div class="w-12 h-12 rounded-2xl bg-rose-950/40 border border-rose-800/60 flex items-center justify-center text-2xl group-hover:scale-110 transition-transform">
              🧹
            </div>
            <div>
              <div class="font-black text-sm text-slate-100">Rubber Eraser</div>
              <div class="text-[11px] text-rose-400 font-extrabold mt-0.5">Vulcanized Rubber (Insulator)</div>
            </div>
          </button>

          <!-- Tool 3: Pencil Graphite -->
          <button onclick="selectMaterial('pencil')" id="btn-mat-pencil" class="shelf-card tactile-btn bg-slate-900/90 border border-slate-800 rounded-2xl p-4 flex flex-col items-center justify-center text-center space-y-2 group cursor-pointer">
            <div class="w-12 h-12 rounded-2xl bg-slate-800 border border-slate-700 flex items-center justify-center text-2xl group-hover:scale-110 transition-transform">
              ✏️
            </div>
            <div>
              <div class="font-black text-sm text-slate-100">Pencil Lead (Graphite)</div>
              <div class="text-[11px] text-sky-400 font-extrabold mt-0.5">Non-Metal Conductor</div>
            </div>
          </button>

          <!-- Tool 4: Plastic Ruler -->
          <button onclick="selectMaterial('ruler')" id="btn-mat-ruler" class="shelf-card tactile-btn bg-slate-900/90 border border-slate-800 rounded-2xl p-4 flex flex-col items-center justify-center text-center space-y-2 group cursor-pointer">
            <div class="w-12 h-12 rounded-2xl bg-cyan-950/40 border border-cyan-800/60 flex items-center justify-center text-2xl group-hover:scale-110 transition-transform">
              📏
            </div>
            <div>
              <div class="font-black text-sm text-slate-100">Plastic Ruler</div>
              <div class="text-[11px] text-rose-400 font-extrabold mt-0.5">Synthetic Polymer (Insulator)</div>
            </div>
          </button>

        </div>
      </div>

      <!-- 4. REAL LIVE DYNAMIC INSPECTOR SHOWCASE (GENUINE CANVAS + VECTOR) -->
      <div id="inspector-showcase" class="bg-[#0f172a] border border-slate-800 rounded-2xl p-5 space-y-4">
        
        <div class="flex items-center justify-between border-b border-slate-800 pb-3">
          <div class="flex items-center gap-2">
            <span class="text-sm">🔬</span>
            <span class="text-xs font-black uppercase text-blue-400 tracking-wider">High-Resolution Material Inspection & Live Particle Simulation</span>
          </div>
          <span id="showcase-badge" class="text-[10px] font-mono font-bold px-3 py-1 rounded-full bg-slate-800 text-slate-300">
            AWAITING SELECTION
          </span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          
          <!-- Box A: High-Craft Physical Vector Close-Up -->
          <div class="bg-slate-950 border border-slate-800/80 rounded-xl p-4 space-y-2">
            <div class="text-xs font-black text-slate-400 uppercase font-mono">1. Physical Macro Appearance</div>
            
            <div class="h-36 rounded-xl bg-slate-900/90 border border-slate-800 flex items-center justify-center p-2 relative overflow-hidden">
              <svg id="macro-vector-stage" viewBox="0 0 320 120" class="w-full h-full">
                <text x="160" y="65" text-anchor="middle" fill="#64748b" font-size="12" font-weight="700">
                  Select an item above to inspect physical details
                </text>
              </svg>
            </div>
            
            <div id="macro-spec-meta" class="text-xs text-slate-300 font-medium"></div>
          </div>

          <!-- Box B: Real-Time Canvas Atomic Particle Drift Simulation -->
          <div class="bg-slate-950 border border-slate-800/80 rounded-xl p-4 space-y-2">
            <div class="flex items-center justify-between">
              <span class="text-xs font-black text-slate-400 uppercase font-mono">2. Atomic Charge Carrier Simulation</span>
              <span id="canvas-fps-badge" class="text-[10px] font-mono font-bold text-emerald-400 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-800">
                LIVE 60 FPS
              </span>
            </div>
            
            <div class="h-36 rounded-xl bg-[#030712] border border-slate-800 relative overflow-hidden">
              <canvas id="atomic-canvas" width="400" height="144" class="w-full h-full block"></canvas>
            </div>
            
            <div id="atomic-spec-meta" class="text-xs text-slate-300 font-medium"></div>
          </div>

        </div>

      </div>

    </main>

    <!-- 5. CAMBRIDGE EXAM CHECKPOINT QUESTIONS -->
    <section class="bg-[#0f172a] border border-slate-800 rounded-3xl p-6 sm:p-7 shadow-2xl space-y-5">
      <div class="flex items-center justify-between border-b border-slate-800 pb-3">
        <div class="flex items-center gap-2.5">
          <span class="w-8 h-8 rounded-xl bg-blue-950 border border-blue-800 text-blue-400 font-black flex items-center justify-center text-sm">3</span>
          <h2 class="text-base sm:text-lg font-black text-white">Cambridge Exam Checkpoint Challenge</h2>
        </div>
        <span id="quiz-score-badge" class="text-xs bg-slate-800 text-slate-300 font-extrabold px-3 py-1 rounded-full border border-slate-700">
          Score: 0 / 3
        </span>
      </div>

      <div class="space-y-4">
        
        <!-- Q1 -->
        <div class="p-4 sm:p-5 rounded-2xl bg-slate-950 border border-slate-800 space-y-3">
          <div class="font-extrabold text-xs sm:text-sm text-slate-200">
            Q1. Mostafa sets up a circuit with a battery, a buzzer, and an unknown solid material in the gap. The buzzer buzzes loudly. What does this prove?
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
            <button onclick="answerQuestion(1, 'A', false)" class="q1-opt tactile-btn text-left p-3 rounded-xl border border-slate-800 bg-slate-900 hover:bg-slate-800 text-slate-200 font-bold">
              A) The material is an electrical insulator
            </button>
            <button onclick="answerQuestion(1, 'B', true)" class="q1-opt tactile-btn text-left p-3 rounded-xl border border-slate-800 bg-slate-900 hover:bg-slate-800 text-slate-200 font-bold">
              B) The material is an electrical conductor
            </button>
            <button onclick="answerQuestion(1, 'C', false)" class="q1-opt tactile-btn text-left p-3 rounded-xl border border-slate-800 bg-slate-900 hover:bg-slate-800 text-slate-200 font-bold">
              C) The circuit has an open air break
            </button>
            <button onclick="answerQuestion(1, 'D', false)" class="q1-opt tactile-btn text-left p-3 rounded-xl border border-slate-800 bg-slate-900 hover:bg-slate-800 text-slate-200 font-bold">
              D) The battery has run out of voltage
            </button>
          </div>
          <div id="feedback-1" class="hidden text-xs p-3 rounded-xl font-medium"></div>
        </div>

        <!-- Q2 -->
        <div class="p-4 sm:p-5 rounded-2xl bg-slate-950 border border-slate-800 space-y-3">
          <div class="font-extrabold text-xs sm:text-sm text-slate-200">
            Q2. Why is pencil lead (graphite) special compared to most non-metals like plastic or wood?
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
            <button onclick="answerQuestion(2, 'A', false)" class="q2-opt tactile-btn text-left p-3 rounded-xl border border-slate-800 bg-slate-900 hover:bg-slate-800 text-slate-200 font-bold">
              A) It is made of copper wire
            </button>
            <button onclick="answerQuestion(2, 'B', true)" class="q2-opt tactile-btn text-left p-3 rounded-xl border border-slate-800 bg-slate-900 hover:bg-slate-800 text-slate-200 font-bold">
              B) It is a form of carbon with free delocalized electrons
            </button>
            <button onclick="answerQuestion(2, 'C', false)" class="q2-opt tactile-btn text-left p-3 rounded-xl border border-slate-800 bg-slate-900 hover:bg-slate-800 text-slate-200 font-bold">
              C) It generates its own 3V electric charge
            </button>
            <button onclick="answerQuestion(2, 'D', false)" class="q2-opt tactile-btn text-left p-3 rounded-xl border border-slate-800 bg-slate-900 hover:bg-slate-800 text-slate-200 font-bold">
              D) It acts as an insulator at room temperature
            </button>
          </div>
          <div id="feedback-2" class="hidden text-xs p-3 rounded-xl font-medium"></div>
        </div>

        <!-- Q3 -->
        <div class="p-4 sm:p-5 rounded-2xl bg-slate-950 border border-slate-800 space-y-3">
          <div class="font-extrabold text-xs sm:text-sm text-slate-200">
            Q3. In a series circuit with two identical lamps, what happens if one bulb is unscrewed or breaks?
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
            <button onclick="answerQuestion(3, 'A', false)" class="q3-opt tactile-btn text-left p-3 rounded-xl border border-slate-800 bg-slate-900 hover:bg-slate-800 text-slate-200 font-bold">
              A) The other lamp gets twice as bright
            </button>
            <button onclick="answerQuestion(3, 'B', false)" class="q3-opt tactile-btn text-left p-3 rounded-xl border border-slate-800 bg-slate-900 hover:bg-slate-800 text-slate-200 font-bold">
              B) Nothing changes for the second lamp
            </button>
            <button onclick="answerQuestion(3, 'C', true)" class="q3-opt tactile-btn text-left p-3 rounded-xl border border-slate-800 bg-slate-900 hover:bg-slate-800 text-slate-200 font-bold">
              C) The second lamp goes off because the single loop is broken
            </button>
            <button onclick="answerQuestion(3, 'D', false)" class="q3-opt tactile-btn text-left p-3 rounded-xl border border-slate-800 bg-slate-900 hover:bg-slate-800 text-slate-200 font-bold">
              D) The battery explodes from excessive heat
            </button>
          </div>
          <div id="feedback-3" class="hidden text-xs p-3 rounded-xl font-medium"></div>
        </div>

      </div>

      <div class="pt-2 flex flex-col sm:flex-row items-center justify-between gap-3 border-t border-slate-800">
        <div class="text-xs text-slate-400 font-semibold flex items-center gap-1.5">
          <span>☁️</span> Auto-synced to Google Sheet & Parent Dashboard
        </div>
        <a href="../Index.html" class="tactile-btn w-full sm:w-auto inline-flex items-center justify-center gap-2 bg-gradient-to-r from-blue-600 to-indigo-700 hover:from-blue-500 hover:to-indigo-600 text-white font-extrabold px-6 py-2.5 rounded-xl shadow-md transition-all text-xs">
          <span>Return to Stage 6 Hub</span>
          <span>→</span>
        </a>
      </div>
    </section>

    <!-- 6. VIDEO MODAL -->
    <div id="video-modal" class="hidden fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4">
      <div class="bg-slate-900 border border-slate-800 rounded-3xl max-w-3xl w-full p-5 sm:p-6 shadow-2xl space-y-4">
        <div class="flex items-center justify-between border-b border-slate-800 pb-3">
          <div>
            <div class="text-[11px] font-mono font-bold text-blue-400 uppercase">Cambridge Primary Science Episode 18</div>
            <h3 class="text-base sm:text-lg font-black text-white">Electricity in Series Circuits</h3>
          </div>
          <button onclick="toggleVideoModal()" class="tactile-btn w-8 h-8 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 flex items-center justify-center font-bold">
            ✕
          </button>
        </div>
        <div class="w-full bg-black rounded-2xl overflow-hidden border border-slate-800">
          <video controls class="w-full h-auto max-h-[440px]">
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
    const answered = {};

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
      playTone(523.25, 'sine', 0.12);
      setTimeout(() => playTone(659.25, 'sine', 0.14), 100);
      setTimeout(() => playTone(783.99, 'triangle', 0.22), 220);
    }

    function toggleAudio() {
      audioEnabled = !audioEnabled;
      document.getElementById('audio-icon').textContent = audioEnabled ? '🔊' : '🔇';
      document.getElementById('audio-text').textContent = audioEnabled ? 'Audio: ON' : 'Audio: OFF';
    }

    function toggleVideoModal() {
      document.getElementById('video-modal').classList.toggle('hidden');
    }

    function toggleKnifeSwitch() {
      isKnifeSwitchClosed = !isKnifeSwitchClosed;
      const blade = document.getElementById('switch-blade-line');
      const handle = document.getElementById('switch-handle-circle');
      const pill = document.getElementById('switch-pill-text');

      if (isKnifeSwitchClosed) {
        blade.setAttribute('x2', '80');
        blade.setAttribute('y2', '30');
        handle.setAttribute('cx', '80');
        handle.setAttribute('cy', '30');
        pill.textContent = "CLOSED (ON)";
        pill.className = "text-emerald-400 font-black";
        playTone(300, 'sine', 0.08);
      } else {
        blade.setAttribute('x2', '70');
        blade.setAttribute('y2', '5');
        handle.setAttribute('cx', '70');
        handle.setAttribute('cy', '5');
        pill.textContent = "OPEN (OFF)";
        pill.className = "text-rose-400 font-black";
        playTone(200, 'sine', 0.08);
      }

      if (currentMaterial) {
        selectMaterial(currentMaterial);
      }
    }

    // ==========================================
    // 60 FPS LIVE ATOMIC CANVAS PARTICLE ENGINE
    // ==========================================
    const canvas = document.getElementById('atomic-canvas');
    const ctx = canvas.getContext('2d');
    let particles = [];
    let animationId = null;

    function initParticles(type) {
      particles = [];
      const w = canvas.width;
      const h = canvas.height;

      if (type === 'coin') {
        for (let i = 0; i < 45; i++) {
          particles.push({
            x: Math.random() * w,
            y: 20 + Math.random() * (h - 40),
            vx: 1.8 + Math.random() * 1.5,
            vy: (Math.random() - 0.5) * 0.4,
            r: 2.5,
            color: '#38bdf8'
          });
        }
      } else if (type === 'pencil') {
        for (let i = 0; i < 35; i++) {
          particles.push({
            x: Math.random() * w,
            y: 50 + Math.random() * 44,
            vx: 1.4 + Math.random() * 1.2,
            vy: (Math.random() - 0.5) * 0.3,
            r: 2.2,
            color: '#38bdf8'
          });
        }
      } else if (type === 'eraser' || type === 'ruler') {
        for (let i = 0; i < 28; i++) {
          const originX = 30 + Math.random() * (w - 60);
          const originY = 25 + Math.random() * (h - 50);
          particles.push({
            x: originX,
            y: originY,
            ox: originX,
            oy: originY,
            r: 2.2,
            color: '#f43f5e'
          });
        }
      }
    }

    function renderSimulation() {
      const w = canvas.width;
      const h = canvas.height;
      ctx.fillStyle = '#030712';
      ctx.fillRect(0, 0, w, h);

      if (!currentMaterial || !isKnifeSwitchClosed) {
        ctx.fillStyle = '#475569';
        ctx.font = '12px "JetBrains Mono", monospace';
        ctx.textAlign = 'center';
        ctx.fillText(isKnifeSwitchClosed ? 'Awaiting Material Connection...' : 'Switch Open: Electric Field = 0', w / 2, h / 2);
        animationId = requestAnimationFrame(renderSimulation);
        return;
      }

      if (currentMaterial === 'coin') {
        // Draw Copper Lattice Ions
        for (let x = 40; x < w; x += 55) {
          for (let y = 30; y < h; y += 45) {
            ctx.beginPath();
            ctx.arc(x, y, 12, 0, Math.PI * 2);
            ctx.fillStyle = '#7c2d12';
            ctx.fill();
            ctx.strokeStyle = '#f97316';
            ctx.lineWidth = 1.5;
            ctx.stroke();

            ctx.fillStyle = '#fed7aa';
            ctx.font = 'bold 8px monospace';
            ctx.textAlign = 'center';
            ctx.fillText('Cu⁺', x, y + 3);
          }
        }

        // Draw Mobile Electron Sea
        particles.forEach(p => {
          p.x += p.vx;
          p.y += p.vy;
          if (p.x > w) p.x = 0;
          if (p.y < 15) p.y = h - 15;
          if (p.y > h - 15) p.y = 15;

          ctx.beginPath();
          ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
          ctx.fillStyle = p.color;
          ctx.shadowColor = '#38bdf8';
          ctx.shadowBlur = 8;
          ctx.fill();
          ctx.shadowBlur = 0;
        });

      } else if (currentMaterial === 'pencil') {
        // Draw 2 Horizontal Graphene Honeycomb Sheets
        ctx.strokeStyle = '#334155';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.moveTo(10, 36);
        ctx.lineTo(w - 10, 36);
        ctx.stroke();
        ctx.fillStyle = '#94a3b8';
        ctx.font = 'bold 9px monospace';
        ctx.textAlign = 'left';
        ctx.fillText('CARBON GRAPHENE LAYER 1 (C=C=C)', 15, 30);

        ctx.beginPath();
        ctx.moveTo(10, 108);
        ctx.lineTo(w - 10, 108);
        ctx.stroke();
        ctx.fillText('CARBON GRAPHENE LAYER 2 (C=C=C)', 15, 124);

        for (let x = 30; x < w; x += 38) {
          ctx.fillStyle = '#64748b';
          ctx.beginPath();
          ctx.arc(x, 36, 4.5, 0, Math.PI * 2);
          ctx.arc(x + 18, 108, 4.5, 0, Math.PI * 2);
          ctx.fill();
        }

        particles.forEach(p => {
          p.x += p.vx;
          p.y += p.vy;
          if (p.x > w) p.x = 0;
          if (p.y < 44) p.vy = Math.abs(p.vy);
          if (p.y > 100) p.vy = -Math.abs(p.vy);

          ctx.beginPath();
          ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
          ctx.fillStyle = '#38bdf8';
          ctx.shadowColor = '#38bdf8';
          ctx.shadowBlur = 6;
          ctx.fill();
          ctx.shadowBlur = 0;
        });

      } else if (currentMaterial === 'eraser' || currentMaterial === 'ruler') {
        ctx.strokeStyle = '#475569';
        ctx.lineWidth = 2;
        ctx.setLineDash([6, 6]);
        for (let y = 30; y < h; y += 42) {
          ctx.beginPath();
          ctx.moveTo(10, y);
          ctx.lineTo(w - 10, y);
          ctx.stroke();
        }
        ctx.setLineDash([]);

        particles.forEach(p => {
          p.x = p.ox + (Math.random() - 0.5) * 2;
          p.y = p.oy + (Math.random() - 0.5) * 2;

          ctx.beginPath();
          ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
          ctx.fillStyle = p.color;
          ctx.fill();
          ctx.strokeStyle = '#ef4444';
          ctx.strokeRect(p.x - 4, p.y - 4, 8, 8);
        });

        ctx.fillStyle = '#f43f5e';
        ctx.font = 'bold 10px monospace';
        ctx.textAlign = 'center';
        ctx.fillText('COVALENT ELECTRON LOCK • DRIFT VELOCITY = 0.00 m/s', w / 2, h / 2);
      }

      animationId = requestAnimationFrame(renderSimulation);
    }
    animationId = requestAnimationFrame(renderSimulation);

    function selectMaterial(mat) {
      currentMaterial = mat;
      initParticles(mat);

      // 1. Shelf buttons
      ['coin', 'eraser', 'pencil', 'ruler'].forEach(id => {
        const btn = document.getElementById('btn-mat-' + id);
        if (id === mat) {
          btn.classList.add('active-selected');
        } else {
          btn.classList.remove('active-selected');
        }
      });

      // 2. Hide all items inside SVG workbench
      ['empty', 'coin', 'eraser', 'pencil', 'ruler'].forEach(id => {
        const el = document.getElementById('item-' + id);
        if (el) {
          el.setAttribute('display', 'none');
          el.style.display = 'none';
        }
      });

      // Show chosen specimen on table
      const activeItem = document.getElementById('item-' + mat);
      if (activeItem) {
        activeItem.setAttribute('display', 'inline');
        activeItem.style.display = 'inline';
      }

      // 3. Update Elements
      const circuitPill = document.getElementById('circuit-status-pill');
      const hint = document.getElementById('assistant-hint');
      const bulbHalo = document.getElementById('bulb-volumetric-glow');
      const bulbGlass = document.getElementById('bulb-glass-sphere');
      const filament = document.getElementById('bulb-filament-path');
      const electronStream = document.getElementById('electron-stream-group');

      const meterV = document.getElementById('meter-v-text');
      const meterI = document.getElementById('meter-i-text');

      const showcaseBadge = document.getElementById('showcase-badge');
      const macroStage = document.getElementById('macro-vector-stage');
      const macroMeta = document.getElementById('macro-spec-meta');
      const atomicMeta = document.getElementById('atomic-spec-meta');

      if (!isKnifeSwitchClosed) {
        circuitPill.className = "text-[10px] font-mono font-black uppercase px-2.5 py-0.5 rounded-full bg-amber-950 border border-amber-800 text-amber-400";
        circuitPill.textContent = "SWITCH OPEN • 0.00 A";

        hint.textContent = "The knife switch is open! Click the switch on the desk to complete the circuit loop.";

        bulbHalo.setAttribute('opacity', '0');
        bulbGlass.setAttribute('fill', '#1e293b');
        bulbGlass.setAttribute('stroke', '#64748b');
        filament.setAttribute('stroke', '#475569');
        electronStream.setAttribute('display', 'none');

        meterV.textContent = "VOLTS: 3.00 V";
        meterI.textContent = "CURRENT: 0.00 A";
        meterI.setAttribute('fill', '#ef4444');

        showcaseBadge.textContent = "CIRCUIT ISOLATED AT SWITCH";
        showcaseBadge.className = "text-[10px] font-mono font-bold px-3 py-1 rounded-full bg-amber-950 text-amber-300 border border-amber-800";
        return;
      }

      if (mat === 'coin') {
        circuitPill.className = "text-[10px] font-mono font-black uppercase px-2.5 py-0.5 rounded-full bg-emerald-950 border border-emerald-700 text-emerald-400";
        circuitPill.textContent = "LOOP CLOSED • 0.35 A (CONDUCTING)";

        hint.textContent = "Success! Copper is a metal with free mobile electrons. Current flows and the lamp shines bright!";

        bulbHalo.setAttribute('opacity', '0.95');
        bulbGlass.setAttribute('fill', '#fef08a');
        bulbGlass.setAttribute('stroke', '#eab308');
        filament.setAttribute('stroke', '#b45309');
        electronStream.setAttribute('display', 'inline');

        meterV.textContent = "VOLTS: 3.00 V";
        meterI.textContent = "CURRENT: 0.35 A";
        meterI.setAttribute('fill', '#10b981');

        showcaseBadge.textContent = "ELECTRICAL CONDUCTOR (METALLIC BOND)";
        showcaseBadge.className = "text-[10px] font-mono font-bold px-3 py-1 rounded-full bg-emerald-950 text-emerald-300 border border-emerald-700";

        macroStage.innerHTML = `
          <g transform="translate(60, 20)">
            <ellipse cx="100" cy="40" rx="58" ry="32" fill="url(#coinGrad)" stroke="#7c2d12" stroke-width="3"/>
            <ellipse cx="100" cy="38" rx="48" ry="24" fill="none" stroke="#fed7aa" stroke-width="1.8" stroke-dasharray="4,3"/>
            <text x="100" y="44" text-anchor="middle" fill="#fef3c7" font-size="14" font-weight="900" font-family="sans-serif">ONE POUND</text>
            <text x="100" y="56" text-anchor="middle" fill="#fed7aa" font-size="8" font-weight="700">SOLID COPPER ALLOY</text>
          </g>
        `;
        macroMeta.innerHTML = "<b>Cambridge Rule:</b> Metals possess crystalline lattices where outer valence electrons easily detach to form an electrical charge current.";
        atomicMeta.innerHTML = "<b class='text-sky-300'>Live Canvas:</b> 45 mobile conduction electrons drifting past Cu⁺ copper nuclei cores at 60 FPS.";

        playSuccessChime();

      } else if (mat === 'pencil') {
        circuitPill.className = "text-[10px] font-mono font-black uppercase px-2.5 py-0.5 rounded-full bg-emerald-950 border border-emerald-700 text-emerald-400";
        circuitPill.textContent = "LOOP CLOSED • 0.28 A (GRAPHITE)";

        hint.textContent = "Surprise! Pencil lead (graphite) conducts electricity! It is a rare non-metal conductor.";

        bulbHalo.setAttribute('opacity', '0.85');
        bulbGlass.setAttribute('fill', '#fef08a');
        bulbGlass.setAttribute('stroke', '#eab308');
        filament.setAttribute('stroke', '#b45309');
        electronStream.setAttribute('display', 'inline');

        meterV.textContent = "VOLTS: 3.00 V";
        meterI.textContent = "CURRENT: 0.28 A";
        meterI.setAttribute('fill', '#10b981');

        showcaseBadge.textContent = "NON-METAL CONDUCTOR (GRAPHITE)";
        showcaseBadge.className = "text-[10px] font-mono font-bold px-3 py-1 rounded-full bg-emerald-950 text-emerald-300 border border-emerald-700";

        macroStage.innerHTML = `
          <g transform="translate(30, 25)">
            <polygon points="10,40 180,24 180,56 10,72" fill="#eab308" stroke="#a16207" stroke-width="2"/>
            <line x1="10" y1="56" x2="180" y2="40" stroke="#ca8a04" stroke-width="2"/>
            <text x="75" y="52" fill="#78350f" font-size="9" font-weight="900" font-family="monospace">STAGE 6 • HB GRAPHITE</text>
            <polygon points="180,24 235,40 180,56" fill="#fed7aa" stroke="#ca8a04" stroke-width="1.5"/>
            <polygon points="215,35 245,40 215,45" fill="#0f172a" stroke="#334155" stroke-width="1.5"/>
            <rect x="238" y="32" width="22" height="16" rx="2" fill="url(#brassGrad)" stroke="#78350f" stroke-width="1"/>
            <polygon points="238,32 248,40 238,48" fill="#92400e"/>
          </g>
        `;
        macroMeta.innerHTML = "<b>Cambridge Key Concept:</b> Pencil 'lead' contains zero toxic lead; it is pure layered carbon (graphite) and clay.";
        atomicMeta.innerHTML = "<b class='text-sky-300'>Live Canvas:</b> Delocalized carbon electrons flowing effortlessly between parallel graphene honeycomb sheets.";

        playSuccessChime();

      } else if (mat === 'eraser') {
        circuitPill.className = "text-[10px] font-mono font-black uppercase px-2.5 py-0.5 rounded-full bg-rose-950 border border-rose-800 text-rose-400";
        circuitPill.textContent = "LOOP BROKEN • 0.00 A (INSULATOR)";

        hint.textContent = "Rubber is an electrical insulator! Electrons cannot pass through the eraser, so the lamp stays off.";

        bulbHalo.setAttribute('opacity', '0');
        bulbGlass.setAttribute('fill', '#1e293b');
        bulbGlass.setAttribute('stroke', '#64748b');
        filament.setAttribute('stroke', '#475569');
        electronStream.setAttribute('display', 'none');

        meterV.textContent = "VOLTS: 3.00 V";
        meterI.textContent = "CURRENT: 0.00 A";
        meterI.setAttribute('fill', '#ef4444');

        showcaseBadge.textContent = "ELECTRICAL INSULATOR (VULCANIZED RUBBER)";
        showcaseBadge.className = "text-[10px] font-mono font-bold px-3 py-1 rounded-full bg-rose-950 text-rose-300 border border-rose-800";

        macroStage.innerHTML = `
          <g transform="translate(70, 20)">
            <polygon points="20,30 140,15 165,45 45,60" fill="#f43f5e" stroke="#be123c" stroke-width="2.5"/>
            <polygon points="140,15 165,45 180,38 155,8" fill="#3b82f6" stroke="#1d4ed8" stroke-width="2.5"/>
            <text x="85" y="44" text-anchor="middle" fill="#ffffff" font-size="12" font-weight="900" transform="rotate(-6 85 44)">CLASSROOM ERASER</text>
          </g>
        `;
        macroMeta.innerHTML = "<b>Cambridge Rule:</b> Insulators have tightly bound electrons that cannot drift when electric voltage is applied.";
        atomicMeta.innerHTML = "<b class='text-rose-300'>Live Canvas:</b> Electrons locked in covalent polymer bonds. Zero net charge transport.";

        playTone(180, 'square', 0.08);

      } else if (mat === 'ruler') {
        circuitPill.className = "text-[10px] font-mono font-black uppercase px-2.5 py-0.5 rounded-full bg-rose-950 border border-rose-800 text-rose-400";
        circuitPill.textContent = "LOOP BROKEN • 0.00 A (INSULATOR)";

        hint.textContent = "Plastic blocks electricity! That is why electrical wires and tools are coated in plastic for safety.";

        bulbHalo.setAttribute('opacity', '0');
        bulbGlass.setAttribute('fill', '#1e293b');
        bulbGlass.setAttribute('stroke', '#64748b');
        filament.setAttribute('stroke', '#475569');
        electronStream.setAttribute('display', 'none');

        meterV.textContent = "VOLTS: 3.00 V";
        meterI.textContent = "CURRENT: 0.00 A";
        meterI.setAttribute('fill', '#ef4444');

        showcaseBadge.textContent = "ELECTRICAL INSULATOR (ACRYLIC POLYMER)";
        showcaseBadge.className = "text-[10px] font-mono font-bold px-3 py-1 rounded-full bg-rose-950 text-rose-300 border border-rose-800";

        macroStage.innerHTML = `
          <g transform="translate(30, 30)">
            <rect x="10" y="10" width="240" height="40" rx="3" fill="#38bdf8" fill-opacity="0.4" stroke="#0284c7" stroke-width="2"/>
            <line x1="30" y1="10" x2="30" y2="25" stroke="#0369a1" stroke-width="2"/>
            <line x1="70" y1="10" x2="70" y2="25" stroke="#0369a1" stroke-width="2"/>
            <line x1="110" y1="10" x2="110" y2="25" stroke="#0369a1" stroke-width="2"/>
            <line x1="150" y1="10" x2="150" y2="25" stroke="#0369a1" stroke-width="2"/>
            <line x1="190" y1="10" x2="190" y2="25" stroke="#0369a1" stroke-width="2"/>
            <text x="30" y="38" fill="#0369a1" font-size="10" font-weight="900">0</text>
            <text x="70" y="38" fill="#0369a1" font-size="10" font-weight="900">1</text>
            <text x="110" y="38" fill="#0369a1" font-size="10" font-weight="900">2</text>
            <text x="150" y="38" fill="#0369a1" font-size="10" font-weight="900">3</text>
            <text x="190" y="38" fill="#0369a1" font-size="10" font-weight="900">4 cm</text>
          </g>
        `;
        macroMeta.innerHTML = "<b>Safety Application:</b> Electricians wear rubber gloves and use plastic handles to insulate themselves from lethal shock.";
        atomicMeta.innerHTML = "<b class='text-rose-300'>Live Canvas:</b> Synthetic polymer chains bind electrons rigidly with zero drift.";

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
          btn.className = "q" + qNum + "-opt tactile-btn text-left p-3 rounded-xl border font-bold " + (isCorrect ? "bg-emerald-950/80 border-emerald-600 text-emerald-300" : "bg-rose-950/80 border-rose-600 text-rose-300");
        }
      });

      const fb = document.getElementById('feedback-' + qNum);
      fb.classList.remove('hidden');

      if (isCorrect) {
        score++;
        fb.className = "text-xs p-3.5 rounded-xl font-medium bg-emerald-950/50 text-emerald-300 border border-emerald-800";
        fb.innerHTML = "<b>Correct! 🌟</b> " + (qNum === 1 ? "The buzzer sounds because the material conducts electricity and completes the circuit." : qNum === 2 ? "Graphite layers have free delocalized electrons that move under voltage." : "In a series circuit, there is only one pathway. Breaking any component stops current everywhere.");
        playSuccessChime();
      } else {
        fb.className = "text-xs p-3.5 rounded-xl font-medium bg-rose-950/50 text-rose-300 border border-rose-800";
        fb.innerHTML = "<b>Incorrect.</b> " + (qNum === 1 ? "Conducting materials complete the loop and allow current to sound the buzzer." : qNum === 2 ? "Graphite has free mobile electrons between its carbon layers, unlike other non-metals." : "In series, if one bulb goes off, the entire loop breaks and all other bulbs turn off.");
        playTone(180, 'square', 0.08);
      }

      document.getElementById('quiz-score-badge').textContent = "Score: " + score + " / 3";
      if (score === 3) {
        document.getElementById('quiz-score-badge').className = "text-xs bg-emerald-950 text-emerald-300 font-extrabold px-3 py-1 rounded-full border border-emerald-700";
      }
    }
  </script>
</body>
</html>
'''

target_paths = [
    r"C:\Users\co0ob\Projects\primary-exam-system\resources\coligo\Mostafa\Science 106\Electricity_Mastery_Guide_Stage6.html",
    r"C:\Users\co0ob\.gemini\antigravity\brain\54d05bb7-093a-4520-bc55-e8fbc272480c\Electricity_Mastery_Guide_Stage6.html"
]

for p in target_paths:
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Updated: {p} ({len(html_content)} bytes)")
