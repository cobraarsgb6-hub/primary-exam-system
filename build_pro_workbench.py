import os
import shutil

html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Cambridge Stage 6 Science | Professional 3D Physics Circuit Lab</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@600;700;800&display=swap" rel="stylesheet">
  <style>
    body {
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      -webkit-font-smoothing: antialiased;
    }
    .font-mono { font-family: 'JetBrains Mono', monospace; font-variant-numeric: tabular-nums; }
    
    /* Impeccable Smooth Camera Transition for SVG ViewBox */
    #lab-svg {
      transition: viewBox 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    /* Current Flow Animation */
    @keyframes electronStream {
      from { stroke-dashoffset: 48; }
      to { stroke-dashoffset: 0; }
    }
    .electron-flow-active {
      stroke-dasharray: 8, 8;
      animation: electronStream 0.65s linear infinite;
    }
    
    /* Lamp Filament & Bulb Radiance */
    @keyframes bulbPulse {
      0%, 100% { opacity: 0.92; filter: drop-shadow(0 0 25px rgba(250, 204, 21, 0.9)); }
      50% { opacity: 1; filter: drop-shadow(0 0 45px rgba(250, 204, 21, 1)); }
    }
    .bulb-radiance-active {
      animation: bulbPulse 1.8s ease-in-out infinite;
    }

    /* Tactile Micro-Interactions (Make Interfaces Feel Better) */
    .tactile-btn {
      transition: transform 0.15s cubic-bezier(0.2, 0, 0, 1), box-shadow 0.15s cubic-bezier(0.2, 0, 0, 1);
    }
    .tactile-btn:active {
      transform: scale(0.96) !important;
    }
    .material-card {
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .material-card:hover {
      transform: translateY(-3px);
      box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.12);
    }
    .material-card.active-selected {
      border-color: #2563eb !important;
      background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%) !important;
      box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.3), 0 10px 20px -5px rgba(37, 99, 235, 0.25) !important;
    }

    /* Glassmorphic Lab HUD */
    .lab-glass-hud {
      background: rgba(15, 23, 42, 0.75);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.12);
    }
  </style>
</head>
<body class="bg-slate-950 text-slate-100 antialiased min-h-screen p-3 sm:p-6 lg:p-8 selection:bg-blue-600 selection:text-white">

  <div class="max-w-5xl mx-auto space-y-6">

    <!-- 1. TOP BRAND & LAB CONTROL BAR -->
    <header class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-slate-900 border border-slate-800 rounded-3xl p-5 sm:p-6 shadow-2xl">
      <div class="space-y-1">
        <div class="flex items-center gap-2">
          <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
          <span class="text-[11px] font-black uppercase tracking-widest text-blue-400 font-mono">Cambridge Stage 6 • Physics Studio</span>
          <span class="text-slate-600">•</span>
          <span class="text-xs text-slate-400 font-bold">Manaret El-Eman British International School</span>
        </div>
        <h1 class="text-xl sm:text-2xl font-black text-white tracking-tight">Interactive Circuit Lab & Material Analyzer</h1>
        <p class="text-xs text-slate-400 font-medium">
          Dedicated learning hub for <b class="text-slate-200">Mostafa Ahmed</b> • Direct inquiry into electrical conduction, switch physics, and atomic charge carriers.
        </p>
      </div>

      <!-- Quick Action Controls -->
      <div class="flex items-center gap-2 self-start sm:self-center">
        <!-- Audio Mute Toggle -->
        <button onclick="toggleAudio()" id="btn-audio" class="tactile-btn px-3 py-2 rounded-xl text-xs font-bold bg-slate-800 border border-slate-700 hover:bg-slate-700 text-slate-300 flex items-center gap-1.5" title="Toggle Sound Feedback">
          <span id="audio-icon">🔊</span>
          <span id="audio-text">Audio: ON</span>
        </button>

        <!-- Video Modal Switch -->
        <button onclick="toggleVideoTab()" id="btn-video-tab" class="tactile-btn px-4 py-2 rounded-xl text-xs font-extrabold bg-blue-600 hover:bg-blue-500 text-white flex items-center gap-2 shadow-lg shadow-blue-600/30">
          <span>🎬</span>
          <span>Cambridge Video Lesson</span>
        </button>
      </div>
    </header>

    <!-- 2. MAIN INTERACTIVE LAB WORKBENCH STAGE -->
    <main class="bg-slate-900 border border-slate-800 rounded-3xl p-4 sm:p-6 shadow-2xl space-y-4 relative overflow-hidden">
      
      <!-- TOP STATUS & CAMERA ZOOM HUD -->
      <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800 pb-3">
        
        <!-- Left: Student Lab Status Badge -->
        <div class="flex items-center gap-3">
          <div id="status-avatar-badge" class="w-10 h-10 rounded-2xl bg-blue-950 border border-blue-800 text-blue-400 flex items-center justify-center font-black text-lg shadow-inner">
            👨‍🔬
          </div>
          <div>
            <div class="flex items-center gap-2">
              <span class="text-xs font-black text-white">Student Investigator: Mostafa Ahmed</span>
              <span id="circuit-state-pill" class="text-[10px] font-mono font-black uppercase px-2.5 py-0.5 rounded-full bg-rose-950 border border-rose-800 text-rose-400">
                LOOP OPEN • 0.00A
              </span>
            </div>
            <p id="assistant-speech-pill" class="text-xs text-slate-400 font-medium mt-0.5">
              Click any material from the tray below to clamp it between the golden clips.
            </p>
          </div>
        </div>

        <!-- Right: Real Optical Camera Controls (Ahmed's Direct Request!) -->
        <div class="flex items-center gap-1.5 bg-slate-950 border border-slate-800 p-1.5 rounded-2xl">
          <span class="text-[11px] font-mono font-bold text-slate-400 px-2 flex items-center gap-1">
            <span>📷</span>
            <span>CAMERA:</span>
          </span>
          <button onclick="setCameraZoom('wide')" id="btn-cam-wide" class="tactile-btn px-3 py-1.5 rounded-xl text-xs font-bold bg-blue-600 text-white transition-all shadow-sm">
            Full Table
          </button>
          <button onclick="setCameraZoom('macro')" id="btn-cam-macro" class="tactile-btn px-3 py-1.5 rounded-xl text-xs font-bold bg-slate-800 hover:bg-slate-700 text-slate-300 transition-all">
            🔍 5X Macro Zoom
          </button>
          <button onclick="setCameraZoom('atomic')" id="btn-cam-atomic" class="tactile-btn px-3 py-1.5 rounded-xl text-xs font-bold bg-slate-800 hover:bg-slate-700 text-slate-300 transition-all">
            🔬 10X Atomic
          </button>
        </div>

      </div>

      <!-- THE 3D PHYSICS WORKBENCH CANVAS (PURE SVG WITH REAL PERSPECTIVE) -->
      <div class="w-full bg-gradient-to-b from-slate-950 via-[#0a0f1d] to-slate-950 rounded-2xl border border-slate-800/80 overflow-hidden relative shadow-inner">
        
        <svg id="lab-svg" viewBox="0 0 840 450" class="w-full h-auto select-none" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <!-- Realistic Polished Wood Tabletop -->
            <linearGradient id="tableOakSurface" x1="0%" y1="0%" x2="100%" y2="80%">
              <stop offset="0%" stop-color="#b45309"/>
              <stop offset="40%" stop-color="#92400e"/>
              <stop offset="80%" stop-color="#78350f"/>
              <stop offset="100%" stop-color="#451a03"/>
            </linearGradient>
            <linearGradient id="tableBevel" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stop-color="#78350f"/>
              <stop offset="100%" stop-color="#270e02"/>
            </linearGradient>

            <!-- Dynamic Tabletop Illumination (Lights up when circuit closes) -->
            <radialGradient id="deskLampCone" cx="80%" cy="50%" r="65%">
              <stop offset="0%" stop-color="#fef08a" stop-opacity="0.55"/>
              <stop offset="35%" stop-color="#eab308" stop-opacity="0.25"/>
              <stop offset="80%" stop-color="#78350f" stop-opacity="0"/>
            </radialGradient>

            <!-- Metallic Golden Crocodile Clips -->
            <linearGradient id="goldBrassClip" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#fef08a"/>
              <stop offset="30%" stop-color="#f59e0b"/>
              <stop offset="70%" stop-color="#b45309"/>
              <stop offset="100%" stop-color="#78350f"/>
            </linearGradient>

            <!-- Bulb Volumetric Radiance -->
            <radialGradient id="volumetricBulbHalo" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stop-color="#ffffff" stop-opacity="1"/>
              <stop offset="25%" stop-color="#fef08a" stop-opacity="0.95"/>
              <stop offset="60%" stop-color="#facc15" stop-opacity="0.5"/>
              <stop offset="100%" stop-color="#ca8a04" stop-opacity="0"/>
            </radialGradient>

            <!-- Copper Coin Metallic Gradient -->
            <linearGradient id="coinCopperSheen" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#ffedd5"/>
              <stop offset="30%" stop-color="#fb923c"/>
              <stop offset="70%" stop-color="#c2410c"/>
              <stop offset="100%" stop-color="#7c2d12"/>
            </linearGradient>

            <!-- Pencil Wood & Graphite -->
            <linearGradient id="pencilWood" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stop-color="#fde047"/>
              <stop offset="50%" stop-color="#eab308"/>
              <stop offset="100%" stop-color="#a16207"/>
            </linearGradient>
            <linearGradient id="pencilGraphite" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#94a3b8"/>
              <stop offset="50%" stop-color="#334155"/>
              <stop offset="100%" stop-color="#0f172a"/>
            </linearGradient>

            <!-- Realistic Drop Shadows -->
            <filter id="shadowHeavy" x="-10%" y="-10%" width="130%" height="130%">
              <feDropShadow dx="0" dy="16" stdDeviation="12" flood-color="#000000" flood-opacity="0.65"/>
            </filter>
            <filter id="shadowComponent" x="-20%" y="-20%" width="140%" height="150%">
              <feDropShadow dx="2" dy="8" stdDeviation="5" flood-color="#000000" flood-opacity="0.55"/>
            </filter>
          </defs>

          <!-- 1. STUDIO WALL BACKGROUND & LAB SHELVING -->
          <rect x="0" y="0" width="840" height="450" fill="#090d16"/>
          <!-- Grid Lines on Wall -->
          <line x1="0" y1="90" x2="840" y2="90" stroke="#1e293b" stroke-width="1" opacity="0.4"/>
          <line x1="0" y1="180" x2="840" y2="180" stroke="#1e293b" stroke-width="1" opacity="0.4"/>
          <line x1="280" y1="0" x2="280" y2="200" stroke="#1e293b" stroke-width="1" opacity="0.3"/>
          <line x1="560" y1="0" x2="560" y2="200" stroke="#1e293b" stroke-width="1" opacity="0.3"/>

          <!-- Cambridge Scientific Safety Board on Wall -->
          <g transform="translate(480, 25)">
            <rect x="0" y="0" width="160" height="65" rx="8" fill="#0f172a" stroke="#334155" stroke-width="1.5"/>
            <text x="12" y="20" fill="#38bdf8" font-size="9" font-weight="900" font-family="monospace">CAMBRIDGE INQUIRY RULE</text>
            <text x="12" y="36" fill="#94a3b8" font-size="8.5" font-weight="700">Closed Loop = Free Charge Flow</text>
            <text x="12" y="50" fill="#cbd5e1" font-size="8">Conductors have delocalized e⁻</text>
          </g>

          <!-- 2. WOODEN WORKBENCH (ISOMETRIC POLISHED DESKTOP) -->
          <!-- Table Shadow on Floor -->
          <polygon points="60,410 800,410 750,445 30,445" fill="#000000" opacity="0.7"/>
          
          <!-- Front Table Skirt / Bevel Depth -->
          <polygon points="90,370 790,370 790,398 90,398" fill="url(#tableBevel)"/>
          
          <!-- Polished Oak Tabletop Surface -->
          <polygon points="170,185 770,185 790,370 90,370" fill="url(#tableOakSurface)" filter="url(#shadowHeavy)"/>

          <!-- Dynamic Radiance Reflection on Tabletop (Active when lamp is ON) -->
          <polygon id="svg-tabletop-glow" points="170,185 770,185 790,370 90,370" fill="url(#deskLampCone)" opacity="0" class="transition-opacity duration-300"/>

          <!-- Wood Grain Inlay Lines -->
          <line x1="220" y1="220" x2="740" y2="220" stroke="#582f09" stroke-width="1.2" opacity="0.35"/>
          <line x1="160" y1="270" x2="760" y2="270" stroke="#582f09" stroke-width="1.2" opacity="0.35"/>
          <line x1="120" y1="320" x2="780" y2="320" stroke="#582f09" stroke-width="1.2" opacity="0.35"/>

          <!-- Metal Bench Legs -->
          <rect x="110" y="398" width="18" height="42" fill="#0f172a" stroke="#1e293b" stroke-width="1"/>
          <rect x="765" y="398" width="18" height="42" fill="#0f172a" stroke="#1e293b" stroke-width="1"/>

          <!-- 3. REAL PHYSICAL CIRCUIT COMPONENTS ON THE TABLE -->

          <!-- (A) TWIN-CELL 3.0V BATTERY PACK (LEFT TABLE SURFACE) -->
          <g id="comp-battery" transform="translate(160, 245)" filter="url(#shadowComponent)">
            <ellipse cx="60" cy="50" rx="65" ry="16" fill="#000000" opacity="0.4"/>
            <!-- Molded ABS Battery Cradle -->
            <rect x="0" y="8" width="120" height="48" rx="8" fill="#0f172a" stroke="#334155" stroke-width="2"/>
            
            <!-- Cell 1 (Top) -->
            <rect x="14" y="14" width="88" height="16" rx="4" fill="#1e3a8a" stroke="#60a5fa" stroke-width="1"/>
            <rect x="102" y="18" width="6" height="8" rx="2" fill="#e2e8f0"/>
            <text x="32" y="26" fill="#ffffff" font-size="8" font-weight="900" font-family="monospace">1.5V ALKALINE</text>

            <!-- Cell 2 (Bottom) -->
            <rect x="20" y="34" width="88" height="16" rx="4" fill="#1e3a8a" stroke="#60a5fa" stroke-width="1"/>
            <rect x="14" y="38" width="6" height="8" rx="2" fill="#e2e8f0"/>
            <text x="38" y="46" fill="#ffffff" font-size="8" font-weight="900" font-family="monospace">1.5V ALKALINE</text>

            <!-- Brass Terminals -->
            <circle cx="114" cy="22" r="6" fill="#ef4444" stroke="#991b1b" stroke-width="1.5"/>
            <text x="111" y="26" fill="#ffffff" font-size="10" font-weight="900">+</text>
            <circle cx="6" cy="42" r="6" fill="#0f172a" stroke="#475569" stroke-width="1.5"/>
            <text x="4" y="45" fill="#ffffff" font-size="10" font-weight="900">&minus;</text>

            <!-- 3V Rating Plate -->
            <rect x="42" y="58" width="45" height="14" rx="4" fill="#020617" stroke="#3b82f6" stroke-width="1"/>
            <text x="48" y="68" fill="#38bdf8" font-size="8.5" font-weight="900" font-family="monospace">3.0V DC</text>
          </g>

          <!-- (B) HEAVY-DUTY BRASS KNIFE SWITCH (BETWEEN BATTERY & LAMP) -->
          <g id="comp-switch" transform="translate(305, 205)" onclick="toggleKnifeSwitch()" class="cursor-pointer" filter="url(#shadowComponent)">
            <!-- Slate Base -->
            <rect x="0" y="0" width="60" height="28" rx="6" fill="#1e293b" stroke="#475569" stroke-width="1.5"/>
            <circle cx="12" cy="14" r="5" fill="#d97706" stroke="#78350f" stroke-width="1.2"/>
            <circle cx="48" cy="14" r="5" fill="#d97706" stroke="#78350f" stroke-width="1.2"/>
            <!-- Switch Blade Lever -->
            <line id="switch-blade-line" x1="12" y1="14" x2="48" y2="14" stroke="#f59e0b" stroke-width="5" stroke-linecap="round" class="transition-all duration-300"/>
            <!-- Red Safety Handle -->
            <circle id="switch-handle-circle" cx="48" cy="14" r="5" fill="#dc2626" class="transition-all duration-300"/>
            <text x="7" y="38" fill="#94a3b8" font-size="7.5" font-weight="900" font-family="monospace">KNIFE SWITCH</text>
          </g>

          <!-- (C) EDISON SCREW-BASE CERAMIC LAMP & GLASS BULB (RIGHT TABLE SURFACE) -->
          <g id="comp-lamp" transform="translate(650, 205)" filter="url(#shadowComponent)">
            <!-- Volumetric Light Beam Halo -->
            <circle id="bulb-volumetric-glow" cx="26" cy="26" r="90" fill="url(#volumetricBulbHalo)" opacity="0" class="transition-opacity duration-300 pointer-events-none"/>

            <ellipse cx="26" cy="74" rx="42" ry="14" fill="#000000" opacity="0.45"/>
            
            <!-- Porcelain Base -->
            <ellipse cx="26" cy="68" rx="36" ry="13" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
            <path d="M -10 68 Q 26 80 62 68 L 62 58 Q 26 70 -10 58 Z" fill="#94a3b8"/>
            <ellipse cx="26" cy="58" rx="36" ry="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1"/>

            <!-- Brass Screw Base -->
            <rect x="13" y="42" width="26" height="16" rx="2" fill="#d97706" stroke="#b45309" stroke-width="1.2"/>
            <line x1="13" y1="46" x2="39" y2="46" stroke="#78350f" stroke-width="1"/>
            <line x1="13" y1="52" x2="39" y2="52" stroke="#78350f" stroke-width="1"/>

            <!-- Glass Bulb Sphere -->
            <circle id="bulb-glass-sphere" cx="26" cy="22" r="28" fill="#1e293b" stroke="#64748b" stroke-width="2" opacity="0.9" class="transition-colors duration-300"/>
            <!-- Glass Specular Reflection Highlight -->
            <ellipse cx="18" cy="14" rx="9" ry="4" fill="#ffffff" opacity="0.4" transform="rotate(-30 18 14)"/>

            <!-- Tungsten Filament Coil -->
            <path id="bulb-filament-path" d="M 18 30 L 22 18 L 26 24 L 30 18 L 34 30" fill="none" stroke="#475569" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" class="transition-colors duration-300"/>

            <text x="2" y="94" fill="#e2e8f0" font-size="10" font-weight="900" font-family="monospace">STAGE 6 LAMP</text>
          </g>

          <!-- (D) CENTER SPECIMEN TESTING DISH & CROCODILE CLIPS -->
          <!-- Clicking here or clicking zoom buttons will focus camera directly on this group! -->
          <g id="comp-specimen-station" transform="translate(420, 270)">
            <ellipse cx="65" cy="30" rx="95" ry="28" fill="#000000" opacity="0.4"/>
            
            <!-- Ceramic Petri Dish / Specimen Platform -->
            <ellipse cx="65" cy="24" rx="90" ry="24" fill="#0f172a" stroke="#334155" stroke-width="2.5"/>
            <ellipse cx="65" cy="22" rx="80" ry="20" fill="#1e293b" stroke="#475569" stroke-width="1.5"/>

            <!-- SPECIMEN RENDER (DISCRETE SVG NATIVE TOGGLES - ZERO OVERLAY) -->
            <g id="specimen-group" transform="translate(20, 2)">
              
              <!-- State 0: Empty Test Gap (Default) -->
              <g id="item-empty" display="inline">
                <text x="45" y="22" text-anchor="middle" font-size="22">❓</text>
                <text x="45" y="36" text-anchor="middle" fill="#94a3b8" font-size="9" font-weight="800" font-family="monospace">EMPTY TEST GAP</text>
              </g>

              <!-- State 1: 3D Copper Coin (Conductor) -->
              <g id="item-coin" display="none">
                <!-- Coin Drop Shadow inside dish -->
                <ellipse cx="45" cy="23" rx="34" ry="17" fill="#000000" opacity="0.3"/>
                <!-- Outer Ridged Copper Rim -->
                <ellipse cx="45" cy="20" rx="33" ry="18" fill="url(#coinCopperSheen)" stroke="#7c2d12" stroke-width="2.5"/>
                <!-- Inner Beaded Ring -->
                <ellipse cx="45" cy="19" rx="27" ry="14" fill="none" stroke="#ffedd5" stroke-width="1.2" stroke-dasharray="3,2"/>
                <text x="45" y="24" text-anchor="middle" fill="#fef3c7" font-size="11" font-weight="900" font-family="sans-serif">ONE POUND</text>
                
                <!-- Macro Sparkles when current flows -->
                <g id="coin-sparks" opacity="0" class="transition-opacity duration-300">
                  <circle cx="20" cy="18" r="2" fill="#fde047" class="animate-ping"/>
                  <circle cx="70" cy="18" r="2" fill="#fde047" class="animate-ping"/>
                </g>
              </g>

              <!-- State 2: 3D Rubber Classroom Eraser (Insulator) -->
              <g id="item-eraser" display="none">
                <ellipse cx="45" cy="26" rx="36" ry="16" fill="#000000" opacity="0.35"/>
                <!-- Angled Pink Eraser Block -->
                <polygon points="12,16 68,10 78,25 22,31" fill="#f43f5e" stroke="#be123c" stroke-width="2"/>
                <!-- Blue Beveled Grip Edge -->
                <polygon points="68,10 78,25 84,22 74,7" fill="#3b82f6" stroke="#1d4ed8" stroke-width="2"/>
                <text x="42" y="24" text-anchor="middle" fill="#ffffff" font-size="9.5" font-weight="900" transform="rotate(-6 42 24)">ERASER</text>
              </g>

              <!-- State 3: Hexagonal Pencil with Pure Graphite Core (Special Conductor) -->
              <g id="item-pencil" display="none">
                <ellipse cx="45" cy="26" rx="38" ry="14" fill="#000000" opacity="0.35"/>
                <!-- Yellow Hexagonal Pencil Shaft -->
                <polygon points="8,22 64,16 64,24 8,30" fill="url(#pencilWood)" stroke="#b45309" stroke-width="1.8"/>
                <!-- Sharpened Cedar Wood Cone -->
                <polygon points="64,16 78,20 64,24" fill="#fed7aa"/>
                <!-- Exposed Black Graphite Tip -->
                <polygon points="74,19 85,20 74,21" fill="url(#pencilGraphite)"/>
                <text x="34" y="26" text-anchor="middle" fill="#78350f" font-size="8" font-weight="900" transform="rotate(-6 34 26)">HB GRAPHITE</text>
              </g>

              <!-- State 4: Translucent Acrylic Plastic Ruler (Insulator) -->
              <g id="item-ruler" display="none">
                <ellipse cx="45" cy="26" rx="38" ry="14" fill="#000000" opacity="0.35"/>
                <!-- Transparent Cyan Acrylic Body -->
                <polygon points="8,14 82,14 76,27 2,27" fill="#38bdf8" fill-opacity="0.55" stroke="#0284c7" stroke-width="2"/>
                <!-- Millimeter Measurement Ticks -->
                <line x1="18" y1="14" x2="18" y2="19" stroke="#0369a1" stroke-width="1.2"/>
                <line x1="28" y1="14" x2="28" y2="22" stroke="#0369a1" stroke-width="1.2"/>
                <line x1="38" y1="14" x2="38" y2="19" stroke="#0369a1" stroke-width="1.2"/>
                <line x1="48" y1="14" x2="48" y2="22" stroke="#0369a1" stroke-width="1.2"/>
                <line x1="58" y1="14" x2="58" y2="19" stroke="#0369a1" stroke-width="1.2"/>
                <line x1="68" y1="14" x2="68" y2="22" stroke="#0369a1" stroke-width="1.2"/>
                <text x="42" y="25" text-anchor="middle" fill="#0369a1" font-size="8" font-weight="900" font-family="monospace">PLASTIC cm</text>
              </g>

            </g>

            <!-- LEFT ALLIGATOR JAW CLAMP -->
            <g id="clip-left" transform="translate(8, 12)">
              <rect x="-16" y="2" width="24" height="15" rx="3" fill="url(#goldBrassClip)" stroke="#78350f" stroke-width="1.2"/>
              <polygon points="8,3 20,9.5 8,16" fill="#92400e"/>
            </g>

            <!-- RIGHT ALLIGATOR JAW CLAMP -->
            <g id="clip-right" transform="translate(112, 12)">
              <rect x="2" y="2" width="24" height="15" rx="3" fill="url(#goldBrassClip)" stroke="#78350f" stroke-width="1.2"/>
              <polygon points="2,3 -10,9.5 2,16" fill="#92400e"/>
            </g>

            <text x="65" y="60" text-anchor="middle" fill="#94a3b8" font-size="9" font-weight="800" font-family="monospace">
              SPECIMEN TESTING BRIDGE (CROCODILE CLIPS)
            </text>
          </g>

          <!-- 4. THICK HEAVY-DUTY JUMPER CABLES (CURVED 3D BRAIDED WIRES) -->
          <!-- RED CABLE: Battery (+) -> Switch -> Lamp -->
          <path d="M 274 267 Q 310 240 317 219" fill="none" stroke="#dc2626" stroke-width="5.5" stroke-linecap="round"/>
          <path d="M 353 219 Q 500 175 662 255" fill="none" stroke="#dc2626" stroke-width="5.5" stroke-linecap="round"/>
          <!-- BLUE CABLE: Lamp -> Right Clip -->
          <path d="M 662 268 Q 600 330 552 285" fill="none" stroke="#2563eb" stroke-width="5.5" stroke-linecap="round"/>
          <!-- BLACK CABLE: Battery (-) -> Left Clip -->
          <path d="M 166 287 Q 240 350 428 285" fill="none" stroke="#1e293b" stroke-width="5.5" stroke-linecap="round"/>

          <!-- 5. REAL-TIME ELECTRON STREAM (FLOWS AROUND LOOP WHEN CLOSED) -->
          <g id="electron-stream-group" display="none">
            <path d="M 274 267 Q 310 240 317 219" fill="none" stroke="#fef08a" stroke-width="3" class="electron-flow-active"/>
            <path d="M 353 219 Q 500 175 662 255" fill="none" stroke="#fef08a" stroke-width="3" class="electron-flow-active"/>
            <path d="M 662 268 Q 600 330 552 285" fill="none" stroke="#fef08a" stroke-width="3" class="electron-flow-active"/>
            <path d="M 438 285 L 542 285" fill="none" stroke="#fef08a" stroke-width="3.5" class="electron-flow-active"/>
            <path d="M 428 285 Q 240 350 166 287" fill="none" stroke="#fef08a" stroke-width="3" class="electron-flow-active"/>
          </g>

          <!-- 6. HIGH-PRECISION DIGITAL MULTIMETER (TABLE CORNER) -->
          <g id="comp-multimeter" transform="translate(640, 310)" filter="url(#shadowComponent)">
            <rect x="0" y="0" width="145" height="56" rx="8" fill="#0f172a" stroke="#334155" stroke-width="2"/>
            <rect x="6" y="6" width="133" height="44" rx="4" fill="#020617" stroke="#1e293b" stroke-width="1.2"/>
            <text x="12" y="20" fill="#64748b" font-size="7.5" font-weight="900" font-family="monospace">DIGITAL MULTIMETER</text>
            <text id="meter-v-text" x="12" y="34" fill="#38bdf8" font-size="11" font-weight="900" class="font-mono">VOLTS: 3.00 V</text>
            <text id="meter-i-text" x="12" y="46" fill="#ef4444" font-size="11" font-weight="900" class="font-mono">CURRENT: 0.00 A</text>
          </g>

        </svg>

      </div>

      <!-- 3. REAL-TIME DIAGNOSTIC CARD (BELOW WORKBENCH - ZERO OVERLAP) -->
      <div id="diagnostic-card" class="bg-slate-950 border border-slate-800 rounded-2xl p-4 sm:p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div class="flex items-start sm:items-center gap-3.5">
          <div id="diagnostic-icon" class="w-10 h-10 rounded-2xl bg-rose-950 border border-rose-800 text-rose-400 flex items-center justify-center font-black text-lg shrink-0">
            ✕
          </div>
          <div>
            <div id="diagnostic-title" class="font-black text-rose-400 text-sm sm:text-base">
              Circuit Open: Air Gap Between Crocodile Clips
            </div>
            <p id="diagnostic-desc" class="text-xs text-slate-400 font-medium mt-0.5 leading-relaxed">
              Air is an electrical insulator. Electrons cannot jump the physical gap, so current is 0.00 Amperes and the lamp stays off.
            </p>
          </div>
        </div>
        <div id="diagnostic-pill" class="self-start sm:self-center bg-slate-900 text-slate-400 px-4 py-1.5 rounded-full font-mono text-xs font-black border border-slate-700 whitespace-nowrap">
          CURRENT: 0.00 A (OFF)
        </div>
      </div>

      <!-- 4. ATOMIC MACRO EXPLANATION DRAWER (CLEANLY STRUCTURED) -->
      <div id="atomic-inspector-panel" class="bg-slate-950/70 border border-slate-800 rounded-2xl p-4 sm:p-5 space-y-3">
        <div class="flex items-center justify-between border-b border-slate-800 pb-2.5">
          <span class="text-xs font-black text-blue-400 uppercase tracking-wider flex items-center gap-2">
            <span>🔬</span>
            <span>Microscopic / Atomic Breakdown: Why Does This Happen?</span>
          </span>
          <span id="atomic-badge" class="text-[10px] font-mono font-bold px-2.5 py-0.5 rounded-full bg-slate-800 text-slate-400">
            SELECT MATERIAL
          </span>
        </div>
        <div id="atomic-content" class="text-xs text-slate-300 leading-relaxed font-medium">
          Choose a material below (Copper Coin, Rubber Eraser, Pencil Lead, or Plastic Ruler) to reveal its molecular lattice and electron behavior under the microscope.
        </div>
      </div>

      <!-- 5. TACTILE TOOLBOX: CLICKABLE SPECIMENS -->
      <div class="space-y-3 pt-2">
        <div class="flex items-center justify-between text-xs font-bold text-slate-400">
          <span>🧰 Student Specimen Tray (Click to insert between crocodile clips):</span>
          <span class="text-blue-400 font-extrabold text-[11px]">Instant 3D Reaction</span>
        </div>

        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3.5">
          
          <!-- Tool 1: Metal Coin -->
          <button onclick="selectMaterial('coin')" id="btn-mat-coin" class="material-card tactile-btn bg-slate-900 border-2 border-slate-800 rounded-2xl p-4 flex flex-col items-center justify-center text-center space-y-2 group cursor-pointer">
            <div class="w-14 h-14 rounded-2xl bg-amber-950/40 border border-amber-800/60 flex items-center justify-center text-3xl group-hover:scale-110 transition-transform">
              🪙
            </div>
            <div>
              <div class="font-black text-sm text-slate-100">Copper Coin</div>
              <div class="text-[11px] text-emerald-400 font-extrabold mt-0.5">Pure Metal (Conductor)</div>
            </div>
          </button>

          <!-- Tool 2: Rubber Eraser -->
          <button onclick="selectMaterial('eraser')" id="btn-mat-eraser" class="material-card tactile-btn bg-slate-900 border-2 border-slate-800 rounded-2xl p-4 flex flex-col items-center justify-center text-center space-y-2 group cursor-pointer">
            <div class="w-14 h-14 rounded-2xl bg-rose-950/40 border border-rose-800/60 flex items-center justify-center text-3xl group-hover:scale-110 transition-transform">
              🧹
            </div>
            <div>
              <div class="font-black text-sm text-slate-100">Rubber Eraser</div>
              <div class="text-[11px] text-rose-400 font-extrabold mt-0.5">Vulcanized Rubber (Insulator)</div>
            </div>
          </button>

          <!-- Tool 3: Pencil Graphite -->
          <button onclick="selectMaterial('pencil')" id="btn-mat-pencil" class="material-card tactile-btn bg-slate-900 border-2 border-slate-800 rounded-2xl p-4 flex flex-col items-center justify-center text-center space-y-2 group cursor-pointer">
            <div class="w-14 h-14 rounded-2xl bg-slate-800 border border-slate-700 flex items-center justify-center text-3xl group-hover:scale-110 transition-transform">
              ✏️
            </div>
            <div>
              <div class="font-black text-sm text-slate-100">Pencil Lead (Graphite)</div>
              <div class="text-[11px] text-sky-400 font-extrabold mt-0.5">Non-Metal Conductor</div>
            </div>
          </button>

          <!-- Tool 4: Plastic Ruler -->
          <button onclick="selectMaterial('ruler')" id="btn-mat-ruler" class="material-card tactile-btn bg-slate-900 border-2 border-slate-800 rounded-2xl p-4 flex flex-col items-center justify-center text-center space-y-2 group cursor-pointer">
            <div class="w-14 h-14 rounded-2xl bg-cyan-950/40 border border-cyan-800/60 flex items-center justify-center text-3xl group-hover:scale-110 transition-transform">
              📏
            </div>
            <div>
              <div class="font-black text-sm text-slate-100">Plastic Ruler</div>
              <div class="text-[11px] text-rose-400 font-extrabold mt-0.5">Synthetic Polymer (Insulator)</div>
            </div>
          </button>

        </div>
      </div>

    </main>

    <!-- 3. CAMBRIDGE EXAM CHECKPOINT QUESTIONS -->
    <section class="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-7 shadow-2xl space-y-5">
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

    <!-- 4. MODAL OVERLAY: EMBEDDED CAMBRIDGE VIDEO LESSON -->
    <div id="video-modal" class="hidden fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4">
      <div class="bg-slate-900 border border-slate-800 rounded-3xl max-w-3xl w-full p-5 sm:p-6 shadow-2xl space-y-4">
        <div class="flex items-center justify-between border-b border-slate-800 pb-3">
          <div>
            <div class="text-[11px] font-mono font-bold text-blue-400 uppercase">Cambridge Primary Science Episode 18</div>
            <h3 class="text-base sm:text-lg font-black text-white">Electricity in Series Circuits</h3>
          </div>
          <button onclick="toggleVideoTab()" class="tactile-btn w-8 h-8 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 flex items-center justify-center font-bold">
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
    let currentCameraZoom = 'wide';
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

    function playSwitchClick() {
      playTone(190, 'square', 0.08);
    }

    function toggleAudio() {
      audioEnabled = !audioEnabled;
      document.getElementById('audio-icon').textContent = audioEnabled ? '🔊' : '🔇';
      document.getElementById('audio-text').textContent = audioEnabled ? 'Audio: ON' : 'Audio: OFF';
    }

    function toggleVideoTab() {
      const modal = document.getElementById('video-modal');
      modal.classList.toggle('hidden');
    }

    // REAL OPTICAL CAMERA ZOOM (AHMED'S DIRECT MANDATE)
    function setCameraZoom(mode) {
      currentCameraZoom = mode;
      const svg = document.getElementById('lab-svg');
      
      // Update camera button states
      ['wide', 'macro', 'atomic'].forEach(id => {
        const btn = document.getElementById('btn-cam-' + id);
        if (id === mode) {
          btn.className = "tactile-btn px-3 py-1.5 rounded-xl text-xs font-bold bg-blue-600 text-white transition-all shadow-sm";
        } else {
          btn.className = "tactile-btn px-3 py-1.5 rounded-xl text-xs font-bold bg-slate-800 hover:bg-slate-700 text-slate-300 transition-all";
        }
      });

      if (mode === 'wide') {
        // Full Workbench View
        svg.setAttribute('viewBox', '0 0 840 450');
      } else if (mode === 'macro') {
        // 5X Optical Zoom centered right on the Crocodile Clips & Specimen Dish
        svg.setAttribute('viewBox', '370 230 220 120');
      } else if (mode === 'atomic') {
        // 10X Ultra Zoom right into the Alligator Teeth Contact Point
        svg.setAttribute('viewBox', '420 255 120 70');
      }
      playTone(440, 'sine', 0.06);
    }

    function toggleKnifeSwitch() {
      isKnifeSwitchClosed = !isKnifeSwitchClosed;
      const blade = document.getElementById('switch-blade-line');
      const handle = document.getElementById('switch-handle-circle');

      if (isKnifeSwitchClosed) {
        blade.setAttribute('x2', '48');
        blade.setAttribute('y2', '14');
        handle.setAttribute('cx', '48');
        handle.setAttribute('cy', '14');
      } else {
        // Open upwards
        blade.setAttribute('x2', '40');
        blade.setAttribute('y2', '-2');
        handle.setAttribute('cx', '40');
        handle.setAttribute('cy', '-2');
      }

      playSwitchClick();
      if (currentMaterial) {
        selectMaterial(currentMaterial);
      }
    }

    function selectMaterial(mat) {
      currentMaterial = mat;

      // 1. Tool button active states
      ['coin', 'eraser', 'pencil', 'ruler'].forEach(id => {
        const btn = document.getElementById('btn-mat-' + id);
        if (id === mat) {
          btn.classList.add('active-selected');
        } else {
          btn.classList.remove('active-selected');
        }
      });

      // 2. Hide all specimens with bulletproof native SVG display attribute
      ['empty', 'coin', 'eraser', 'pencil', 'ruler'].forEach(id => {
        const el = document.getElementById('item-' + id);
        if (el) {
          el.setAttribute('display', 'none');
          el.style.display = 'none';
        }
      });

      // Show ONLY selected specimen
      const activeItem = document.getElementById('item-' + mat);
      if (activeItem) {
        activeItem.setAttribute('display', 'inline');
        activeItem.style.display = 'inline';
      }

      // 3. Elements to update
      const circuitPill = document.getElementById('circuit-state-pill');
      const speechPill = document.getElementById('assistant-speech-pill');
      const avatarBadge = document.getElementById('status-avatar-badge');

      const bulbHalo = document.getElementById('bulb-volumetric-glow');
      const bulbGlass = document.getElementById('bulb-glass-sphere');
      const filament = document.getElementById('bulb-filament-path');
      const tableGlow = document.getElementById('svg-tabletop-glow');
      const electronStream = document.getElementById('electron-stream-group');
      const sparks = document.getElementById('coin-sparks');

      const meterV = document.getElementById('meter-v-text');
      const meterI = document.getElementById('meter-i-text');

      const diagIcon = document.getElementById('diagnostic-icon');
      const diagTitle = document.getElementById('diagnostic-title');
      const diagDesc = document.getElementById('diagnostic-desc');
      const diagPill = document.getElementById('diagnostic-pill');

      const atomicBadge = document.getElementById('atomic-badge');
      const atomicContent = document.getElementById('atomic-content');

      // Check knife switch state first
      if (!isKnifeSwitchClosed) {
        circuitPill.className = "text-[10px] font-mono font-black uppercase px-2.5 py-0.5 rounded-full bg-amber-950 border border-amber-800 text-amber-400";
        circuitPill.textContent = "SWITCH OPEN • 0.00A";

        speechPill.textContent = "The knife switch is open! Click the switch on the desk to complete the circuit.";
        avatarBadge.textContent = "🔌";

        bulbHalo.setAttribute('opacity', '0');
        bulbGlass.setAttribute('fill', '#1e293b');
        bulbGlass.setAttribute('stroke', '#64748b');
        bulbGlass.classList.remove('bulb-radiance-active');
        filament.setAttribute('stroke', '#475569');
        tableGlow.setAttribute('opacity', '0');
        electronStream.setAttribute('display', 'none');
        if (sparks) sparks.setAttribute('opacity', '0');

        meterV.textContent = "VOLTS: 3.00 V";
        meterI.textContent = "CURRENT: 0.00 A";
        meterI.setAttribute('fill', '#ef4444');

        diagIcon.className = "w-10 h-10 rounded-2xl bg-amber-950 border border-amber-800 text-amber-400 flex items-center justify-center font-black text-lg shrink-0";
        diagIcon.textContent = "⚠️";
        diagTitle.className = "font-black text-amber-400 text-sm sm:text-base";
        diagTitle.textContent = "Break Detected at Switch: Lever is Raised (OFF)";
        diagDesc.textContent = "A circuit requires an unbroken loop. Even though a conductor may be present, the knife switch lever is open, blocking current.";
        diagPill.className = "self-start sm:self-center bg-amber-950 text-amber-400 px-4 py-1.5 rounded-full font-mono text-xs font-black border border-amber-800 whitespace-nowrap";
        diagPill.textContent = "SWITCH: OPEN (0.00 A)";

        atomicBadge.textContent = "SWITCH ISOLATION";
        atomicContent.innerHTML = "When the metallic switch lever is raised into the air, air molecules between the blade and contact act as an insulator with over 10<sup>14</sup> Ω of resistance.";
        return;
      }

      // Check materials
      if (mat === 'coin') {
        // COPPER CONDUCTION
        circuitPill.className = "text-[10px] font-mono font-black uppercase px-2.5 py-0.5 rounded-full bg-emerald-950 border border-emerald-700 text-emerald-400";
        circuitPill.textContent = "LOOP CLOSED • 0.35A (FLOWING)";

        speechPill.textContent = "Success! The copper coin conducts. Free electrons bridge the gap and power the lamp!";
        avatarBadge.textContent = "🌟";

        bulbHalo.setAttribute('opacity', '0.95');
        bulbGlass.setAttribute('fill', '#fef08a');
        bulbGlass.setAttribute('stroke', '#eab308');
        bulbGlass.classList.add('bulb-radiance-active');
        filament.setAttribute('stroke', '#b45309');
        tableGlow.setAttribute('opacity', '1');
        electronStream.setAttribute('display', 'inline');
        if (sparks) sparks.setAttribute('opacity', '1');

        meterV.textContent = "VOLTS: 3.00 V";
        meterI.textContent = "CURRENT: 0.35 A";
        meterI.setAttribute('fill', '#10b981');

        diagIcon.className = "w-10 h-10 rounded-2xl bg-emerald-950 border border-emerald-800 text-emerald-400 flex items-center justify-center font-black text-lg shrink-0";
        diagIcon.textContent = "✓";
        diagTitle.className = "font-black text-emerald-400 text-sm sm:text-base";
        diagTitle.textContent = "SUCCESS: Copper is an Electrical Conductor!";
        diagDesc.textContent = "The circuit is 100% complete. Electrons flow effortlessly across the copper coin, generating radiant illumination.";
        diagPill.className = "self-start sm:self-center bg-emerald-950 text-emerald-300 px-4 py-1.5 rounded-full font-mono text-xs font-black border border-emerald-700 whitespace-nowrap";
        diagPill.textContent = "CURRENT: 0.35 A (ACTIVE)";

        atomicBadge.textContent = "COPPER ATOMIC LATTICE";
        atomicContent.innerHTML = "<b class='text-amber-300'>Metallic Bonding:</b> Copper atoms share a giant 'sea' of mobile valence electrons (delocalized electrons). Applying 3V from the battery instantly pushes this sea of electrons through the wire loop.";

        playSuccessChime();

      } else if (mat === 'pencil') {
        // GRAPHITE CONDUCTION
        circuitPill.className = "text-[10px] font-mono font-black uppercase px-2.5 py-0.5 rounded-full bg-emerald-950 border border-emerald-700 text-emerald-400";
        circuitPill.textContent = "LOOP CLOSED • 0.28A (GRAPHITE)";

        speechPill.textContent = "Fascinating! Pencil lead (graphite) conducts electricity even though it's a non-metal!";
        avatarBadge.textContent = "⚡";

        bulbHalo.setAttribute('opacity', '0.85');
        bulbGlass.setAttribute('fill', '#fef08a');
        bulbGlass.setAttribute('stroke', '#eab308');
        bulbGlass.classList.add('bulb-radiance-active');
        filament.setAttribute('stroke', '#b45309');
        tableGlow.setAttribute('opacity', '0.8');
        electronStream.setAttribute('display', 'inline');

        meterV.textContent = "VOLTS: 3.00 V";
        meterI.textContent = "CURRENT: 0.28 A";
        meterI.setAttribute('fill', '#10b981');

        diagIcon.className = "w-10 h-10 rounded-2xl bg-emerald-950 border border-emerald-800 text-emerald-400 flex items-center justify-center font-black text-lg shrink-0";
        diagIcon.textContent = "⭐";
        diagTitle.className = "font-black text-emerald-400 text-sm sm:text-base";
        diagTitle.textContent = "SURPRISE! Pencil Graphite is a Rare Non-Metal Conductor!";
        diagDesc.textContent = "Carbon in graphite form conducts electricity. It completes the loop and lights up the lamp.";
        diagPill.className = "self-start sm:self-center bg-emerald-950 text-emerald-300 px-4 py-1.5 rounded-full font-mono text-xs font-black border border-emerald-700 whitespace-nowrap";
        diagPill.textContent = "CURRENT: 0.28 A (ACTIVE)";

        atomicBadge.textContent = "GRAPHENE HONEYCOMB SHEETS";
        atomicContent.innerHTML = "<b class='text-sky-300'>Delocalized Carbon Electrons:</b> Unlike diamond where all 4 carbon electrons are locked in bonds, graphite only bonds 3 carbon atoms, leaving 1 free electron per atom to slide effortlessly between layers!";

        playSuccessChime();

      } else if (mat === 'eraser') {
        // RUBBER INSULATOR
        circuitPill.className = "text-[10px] font-mono font-black uppercase px-2.5 py-0.5 rounded-full bg-rose-950 border border-rose-800 text-rose-400";
        circuitPill.textContent = "LOOP BROKEN • 0.00A (INSULATOR)";

        speechPill.textContent = "Rubber is an electrical insulator! Electrons cannot pass through the eraser.";
        avatarBadge.textContent = "🛑";

        bulbHalo.setAttribute('opacity', '0');
        bulbGlass.setAttribute('fill', '#1e293b');
        bulbGlass.setAttribute('stroke', '#64748b');
        bulbGlass.classList.remove('bulb-radiance-active');
        filament.setAttribute('stroke', '#475569');
        tableGlow.setAttribute('opacity', '0');
        electronStream.setAttribute('display', 'none');

        meterV.textContent = "VOLTS: 3.00 V";
        meterI.textContent = "CURRENT: 0.00 A";
        meterI.setAttribute('fill', '#ef4444');

        diagIcon.className = "w-10 h-10 rounded-2xl bg-rose-950 border border-rose-800 text-rose-400 flex items-center justify-center font-black text-lg shrink-0";
        diagIcon.textContent = "✕";
        diagTitle.className = "font-black text-rose-400 text-sm sm:text-base";
        diagTitle.textContent = "NO CURRENT: Rubber is an Electrical Insulator!";
        diagDesc.textContent = "Rubber atoms hold tightly to their valence electrons. No free electrons exist to carry electric current.";
        diagPill.className = "self-start sm:self-center bg-rose-950 text-rose-300 px-4 py-1.5 rounded-full font-mono text-xs font-black border border-rose-800 whitespace-nowrap";
        diagPill.textContent = "CURRENT: 0.00 A (OFF)";

        atomicBadge.textContent = "TIGHT POLYMER MATRIX";
        atomicContent.innerHTML = "<b class='text-rose-300'>Covalent Electron Locking:</b> Vulcanized rubber consists of long hydrocarbon polymer chains cross-linked by sulfur. Every electron is firmly pinned in place—none are free to flow.";

        playTone(180, 'square', 0.08);

      } else if (mat === 'ruler') {
        // PLASTIC INSULATOR
        circuitPill.className = "text-[10px] font-mono font-black uppercase px-2.5 py-0.5 rounded-full bg-rose-950 border border-rose-800 text-rose-400";
        circuitPill.textContent = "LOOP BROKEN • 0.00A (INSULATOR)";

        speechPill.textContent = "Plastic blocks electricity! That's why electricians wrap electrical cables in plastic.";
        avatarBadge.textContent = "🛑";

        bulbHalo.setAttribute('opacity', '0');
        bulbGlass.setAttribute('fill', '#1e293b');
        bulbGlass.setAttribute('stroke', '#64748b');
        bulbGlass.classList.remove('bulb-radiance-active');
        filament.setAttribute('stroke', '#475569');
        tableGlow.setAttribute('opacity', '0');
        electronStream.setAttribute('display', 'none');

        meterV.textContent = "VOLTS: 3.00 V";
        meterI.textContent = "CURRENT: 0.00 A";
        meterI.setAttribute('fill', '#ef4444');

        diagIcon.className = "w-10 h-10 rounded-2xl bg-rose-950 border border-rose-800 text-rose-400 flex items-center justify-center font-black text-lg shrink-0";
        diagIcon.textContent = "✕";
        diagTitle.className = "font-black text-rose-400 text-sm sm:text-base";
        diagTitle.textContent = "NO CURRENT: Plastic is an Electrical Insulator!";
        diagDesc.textContent = "Synthetic acrylic polymers possess extremely high resistance, completely halting electron flow.";
        diagPill.className = "self-start sm:self-center bg-rose-950 text-rose-300 px-4 py-1.5 rounded-full font-mono text-xs font-black border border-rose-800 whitespace-nowrap";
        diagPill.textContent = "CURRENT: 0.00 A (OFF)";

        atomicBadge.textContent = "SYNTHETIC ACRYLIC POLYMER";
        atomicContent.innerHTML = "<b class='text-rose-300'>Zero Free Charge Carriers:</b> Acrylic molecules bind their electrons in tight covalent pairs. Without free charge carriers, voltage cannot induce any measurable electric current.";

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
