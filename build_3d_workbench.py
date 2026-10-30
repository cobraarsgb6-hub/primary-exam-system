import os
import shutil

html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Cambridge Stage 6 Science | 3D Electric Circuit Lab & Mastery Guide</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <style>
    body { font-family: 'Plus Jakarta Sans', sans-serif; }
    
    /* 3D Workbench Shadows & Perspective */
    .lab-stage-container {
      perspective: 1200px;
    }
    .workbench-card {
      transform-style: preserve-3d;
      box-shadow: 0 25px 50px -12px rgba(15, 23, 42, 0.25), 0 0 0 1px rgba(226, 232, 240, 0.8);
    }
    
    /* Current flow animation along realistic wires */
    @keyframes electronFlow {
      0% { stroke-dashoffset: 40; }
      100% { stroke-dashoffset: 0; }
    }
    .active-wire-flow {
      stroke-dasharray: 8, 8;
      animation: electronFlow 0.8s linear infinite;
    }
    
    /* Pulsing Glow Animation for the Lamp */
    @keyframes bulbRadiance {
      0%, 100% { opacity: 0.88; transform: scale(1); }
      50% { opacity: 0.98; transform: scale(1.04); }
    }
    .bulb-radiance {
      transform-origin: 640px 210px;
      animation: bulbRadiance 2s ease-in-out infinite;
    }

    /* Floating Student Speech Bubble Pulse */
    @keyframes gentleBounce {
      0%, 100% { transform: translateY(0); }
      50% { transform: translateY(-4px); }
    }
    .floating-bubble {
      animation: gentleBounce 3s ease-in-out infinite;
    }

    /* Interactive Tool Card 3D Lift */
    .tool-3d-card {
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .tool-3d-card:hover {
      transform: translateY(-4px) scale(1.02);
      box-shadow: 0 12px 24px -6px rgba(30, 41, 59, 0.15);
    }
    .tool-3d-card.active-selected {
      border-color: #3b82f6 !important;
      background: linear-gradient(145deg, #eff6ff 0%, #dbeafe 100%) !important;
      box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.35), 0 10px 20px -5px rgba(59, 130, 246, 0.3) !important;
    }
  </style>
</head>
<body class="bg-slate-100 text-slate-800 antialiased min-h-screen p-3 sm:p-8">

  <div class="max-w-4xl mx-auto space-y-6">

    <!-- HERO HEADER: MANARET EL-EMAN LEARNING HUB -->
    <header class="bg-gradient-to-r from-blue-700 via-indigo-700 to-indigo-900 text-white p-6 sm:p-8 rounded-3xl shadow-xl relative overflow-hidden">
      <div class="relative z-10 space-y-2">
        <div class="inline-flex items-center gap-2 bg-white/20 backdrop-blur-md px-3.5 py-1 rounded-full text-xs font-extrabold">
          <span>⚡ Cambridge Primary Stage 6</span>
          <span>•</span>
          <span>Manaret El-Eman British International School</span>
        </div>
        <h1 class="text-2xl sm:text-3xl font-black tracking-tight">Interactive 3D Physics Workbench: Electricity & Circuits</h1>
        <p class="text-indigo-100 text-xs sm:text-sm max-w-2xl font-medium leading-relaxed">
          Crafted specifically for <b>Mostafa Ahmed (Grade 6)</b>. Explore real-world physics hands-on: connect conductors and insulators on the lab table, watch current flow, and master Cambridge exam questions!
        </p>
      </div>
      <div class="absolute -right-10 -bottom-10 w-44 h-44 bg-white/10 rounded-full blur-2xl pointer-events-none"></div>
    </header>

    <!-- 1. MENTAL MODEL: WATER-PIPE ANALOGY -->
    <section class="bg-white border border-slate-200 rounded-3xl p-6 sm:p-7 shadow-sm space-y-4">
      <div class="flex items-center justify-between border-b border-slate-100 pb-3">
        <div class="flex items-center gap-2.5">
          <span class="w-8 h-8 rounded-xl bg-blue-100 text-blue-700 font-black flex items-center justify-center text-sm">1</span>
          <h2 class="text-base sm:text-lg font-black text-slate-900">The Water-Pipe Analogy: See Electricity in Your Mind</h2>
        </div>
        <span class="text-xs bg-blue-50 text-blue-700 font-bold px-3 py-1 rounded-full border border-blue-200">Mental Model</span>
      </div>
      <p class="text-xs sm:text-sm text-slate-600 font-medium leading-relaxed">
        Students often struggle with electricity because electrons are invisible. Imagine an electric circuit as a <b>closed loop of water pipes</b> with a pump and a water wheel:
      </p>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-3.5">
        <div class="p-4 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-1.5">
          <div class="text-xs font-black text-indigo-700 uppercase tracking-wide flex items-center gap-1.5">
            <span>🔋</span> The Battery = Water Pump
          </div>
          <p class="text-xs text-slate-600 font-medium leading-relaxed">
            The battery does <b>not</b> create electrons; it provides push/pressure (<b>Voltage</b>) to move existing electrons through the wire loop.
          </p>
        </div>
        <div class="p-4 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-1.5">
          <div class="text-xs font-black text-cyan-700 uppercase tracking-wide flex items-center gap-1.5">
            <span>🌊</span> Current = Water Flow Rate
          </div>
          <p class="text-xs text-slate-600 font-medium leading-relaxed">
            Current (Amperes) is the <b>number of electrons</b> passing a point every second, just like litres of water flowing past every minute.
          </p>
        </div>
        <div class="p-4 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-1.5">
          <div class="text-xs font-black text-amber-700 uppercase tracking-wide flex items-center gap-1.5">
            <span>💡</span> The Bulb = Water Wheel
          </div>
          <p class="text-xs text-slate-600 font-medium leading-relaxed">
            As flowing electrons squeeze through the thin tungsten filament, friction turns kinetic energy into brilliant heat and <b>radiant light</b>!
          </p>
        </div>
      </div>
    </section>

    <!-- 2. REALISTIC 3D PHYSICS WORKBENCH WITH MOSTAFA AVATAR -->
    <section class="workbench-card bg-white border border-slate-200 rounded-3xl p-5 sm:p-7 space-y-5">
      
      <!-- MISSION BAR -->
      <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-4">
        <div>
          <span class="text-xs font-black uppercase tracking-wider text-indigo-600">Cambridge Practical Investigation</span>
          <h2 class="text-lg font-black text-slate-900 mt-0.5">Mostafa's Circuit Lab: Conductor vs Insulator Test</h2>
          <p class="text-xs text-slate-500 font-medium mt-0.5">Pick an item from Mostafa's toolbox below to connect it between the golden crocodile clips on the table.</p>
        </div>
        <span id="circuit-badge" class="text-xs bg-rose-100 text-rose-800 font-extrabold px-3.5 py-1.5 rounded-full border border-rose-200">
          Circuit: OPEN (No Current)
        </span>
      </div>

      <!-- THE 3D LAB WORKBENCH STAGE (SVG 3D ISOMETRIC LAB) -->
      <div class="w-full bg-slate-900 rounded-2xl p-2 sm:p-4 shadow-inner overflow-hidden border border-slate-800">
        <svg viewBox="0 0 820 440" class="w-full h-auto select-none" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <!-- Room & Table Gradients -->
            <linearGradient id="wallGrad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stop-color="#1e293b"/>
              <stop offset="100%" stop-color="#0f172a"/>
            </linearGradient>
            
            <!-- Realistic Polished Wood Tabletop -->
            <linearGradient id="woodSurface" x1="0%" y1="0%" x2="100%" y2="80%">
              <stop offset="0%" stop-color="#a16207"/>
              <stop offset="40%" stop-color="#854d0e"/>
              <stop offset="80%" stop-color="#713f12"/>
              <stop offset="100%" stop-color="#582f09"/>
            </linearGradient>
            <linearGradient id="woodBevelFront" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stop-color="#713f12"/>
              <stop offset="100%" stop-color="#3f2005"/>
            </linearGradient>

            <!-- Tabletop Glow Overlay (When Lamp Lights Up) -->
            <radialGradient id="deskLampGlow" cx="75%" cy="50%" r="65%">
              <stop offset="0%" stop-color="#fde047" stop-opacity="0.45"/>
              <stop offset="45%" stop-color="#ca8a04" stop-opacity="0.18"/>
              <stop offset="100%" stop-color="#713f12" stop-opacity="0"/>
            </radialGradient>

            <!-- 3D Metallic Crocodile Clips -->
            <linearGradient id="goldClipGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#fef08a"/>
              <stop offset="30%" stop-color="#f59e0b"/>
              <stop offset="70%" stop-color="#b45309"/>
              <stop offset="100%" stop-color="#78350f"/>
            </linearGradient>

            <!-- Bulb Volumetric Glow -->
            <radialGradient id="bulbVolumetricGlow" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stop-color="#ffffff" stop-opacity="1"/>
              <stop offset="25%" stop-color="#fef08a" stop-opacity="0.9"/>
              <stop offset="60%" stop-color="#facc15" stop-opacity="0.4"/>
              <stop offset="100%" stop-color="#ca8a04" stop-opacity="0"/>
            </radialGradient>

            <!-- Specimen Gradients -->
            <linearGradient id="copperCoinGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#fed7aa"/>
              <stop offset="35%" stop-color="#f97316"/>
              <stop offset="75%" stop-color="#c2410c"/>
              <stop offset="100%" stop-color="#7c2d12"/>
            </linearGradient>

            <linearGradient id="pencilWoodGrad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stop-color="#fde047"/>
              <stop offset="50%" stop-color="#eab308"/>
              <stop offset="100%" stop-color="#ca8a04"/>
            </linearGradient>

            <linearGradient id="pencilLeadGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#64748b"/>
              <stop offset="50%" stop-color="#1e293b"/>
              <stop offset="100%" stop-color="#020617"/>
            </linearGradient>

            <!-- Soft Drop Shadows -->
            <filter id="deskShadow" x="-5%" y="-5%" width="120%" height="130%">
              <feDropShadow dx="0" dy="18" stdDeviation="15" flood-color="#000000" flood-opacity="0.6"/>
            </filter>
            <filter id="softCompShadow" x="-20%" y="-20%" width="140%" height="150%">
              <feDropShadow dx="3" dy="6" stdDeviation="4" flood-color="#000000" flood-opacity="0.45"/>
            </filter>
          </defs>

          <!-- 1. LAB ROOM BACKGROUND -->
          <rect x="0" y="0" width="820" height="440" fill="url(#wallGrad)"/>
          
          <!-- Subtle Lab Tile Grid Lines on Wall -->
          <line x1="0" y1="80" x2="820" y2="80" stroke="#334155" stroke-width="0.8" opacity="0.3"/>
          <line x1="0" y1="160" x2="820" y2="160" stroke="#334155" stroke-width="0.8" opacity="0.3"/>
          <line x1="280" y1="0" x2="280" y2="200" stroke="#334155" stroke-width="0.8" opacity="0.2"/>
          <line x1="560" y1="0" x2="560" y2="200" stroke="#334155" stroke-width="0.8" opacity="0.2"/>

          <!-- Lab Poster on Wall -->
          <rect x="490" y="25" width="130" height="70" rx="6" fill="#1e293b" stroke="#475569" stroke-width="1.5"/>
          <text x="502" y="44" fill="#38bdf8" font-size="9" font-weight="900" letter-spacing="0.5">OHM'S LAW: V = I × R</text>
          <text x="502" y="60" fill="#94a3b8" font-size="8" font-weight="700">Stage 6 Electricity Rule</text>
          <text x="502" y="76" fill="#cbd5e1" font-size="8">Conductors allow free electrons</text>
          <text x="502" y="86" fill="#cbd5e1" font-size="8">Insulators lock electrons tightly</text>

          <!-- 2. WOODEN WORKBENCH (ISOMETRIC PERSPECTIVE TABLETOP) -->
          <!-- Table Shadow on Floor -->
          <polygon points="120,400 790,400 740,430 80,430" fill="#000000" opacity="0.55"/>
          
          <!-- Front Bevel of Table (Thickness) -->
          <polygon points="140,360 770,360 770,388 140,388" fill="url(#woodBevelFront)"/>
          
          <!-- Main Table Surface (Polished Oak) -->
          <polygon points="210,185 750,185 770,360 140,360" fill="url(#woodSurface)" filter="url(#deskShadow)"/>

          <!-- Dynamic Light Glow on Wood Surface (Active when bulb is on) -->
          <polygon id="svg-wood-light-glow" points="210,185 750,185 770,360 140,360" fill="url(#deskLampGlow)" opacity="0" class="transition-opacity duration-300"/>

          <!-- Wood Grain Depth Lines -->
          <line x1="260" y1="210" x2="710" y2="210" stroke="#582f09" stroke-width="1" opacity="0.3"/>
          <line x1="200" y1="260" x2="730" y2="260" stroke="#582f09" stroke-width="1" opacity="0.3"/>
          <line x1="170" y1="310" x2="750" y2="310" stroke="#582f09" stroke-width="1" opacity="0.3"/>

          <!-- Table Metal Legs -->
          <rect x="155" y="388" width="18" height="42" fill="#1e293b" stroke="#334155" stroke-width="1"/>
          <rect x="745" y="388" width="18" height="42" fill="#1e293b" stroke="#334155" stroke-width="1"/>

          <!-- 3. STUDENT AVATAR: MOSTAFA (STANDING PROUDLY BESIDE THE TABLE) -->
          <g id="student-mostafa" transform="translate(45, 120)">
            <!-- Shadow under Mostafa -->
            <ellipse cx="65" cy="275" rx="42" ry="12" fill="#000000" opacity="0.5"/>

            <!-- Lab Coat Body -->
            <path d="M 35 155 L 20 270 L 110 270 L 95 155 Z" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>
            <!-- Inner Blue Shirt & Tie -->
            <polygon points="50,155 65,190 80,155" fill="#1d4ed8"/>
            <polygon points="62,165 68,165 66,200 64,200" fill="#dc2626"/> <!-- Red School Tie -->

            <!-- Lab Coat Lapels -->
            <path d="M 35 155 L 60 215 L 65 270" fill="none" stroke="#94a3b8" stroke-width="2"/>
            <path d="M 95 155 L 70 215 L 65 270" fill="none" stroke="#94a3b8" stroke-width="2"/>

            <!-- School ID Badge on Lab Coat -->
            <rect x="74" y="180" width="22" height="28" rx="2" fill="#ffffff" stroke="#3b82f6" stroke-width="1.5"/>
            <rect x="76" y="183" width="18" height="8" fill="#1e40af"/>
            <text x="78" y="189" fill="#ffffff" font-size="5" font-weight="900">STAGE 6</text>
            <text x="76" y="200" fill="#1e293b" font-size="6" font-weight="800">Mostafa</text>
            <text x="77" y="205" fill="#64748b" font-size="4">Scientist</text>

            <!-- Mostafa's Head & Face -->
            <!-- Neck -->
            <rect x="56" y="135" width="18" height="22" fill="#fbcfe8" rx="4"/>
            <!-- Head Sphere -->
            <ellipse id="avatar-head" cx="65" cy="115" rx="30" ry="32" fill="#fdd8b5" stroke="#f0a570" stroke-width="1.5"/>
            <!-- Hair (Modern Neat Cut) -->
            <path d="M 35 110 C 35 80, 95 80, 95 110 C 90 92, 40 92, 35 110 Z" fill="#1e1b4b"/>
            <path d="M 33 112 Q 40 90 65 85 Q 92 90 97 112 Q 85 96 65 96 Q 45 96 33 112 Z" fill="#0f172a"/>

            <!-- Eyes -->
            <circle cx="53" cy="114" r="3.5" fill="#1e293b"/>
            <circle cx="54" cy="113" r="1.2" fill="#ffffff"/> <!-- Sparkle -->
            <circle cx="75" cy="114" r="3.5" fill="#1e293b"/>
            <circle cx="76" cy="113" r="1.2" fill="#ffffff"/> <!-- Sparkle -->

            <!-- Eyebrows -->
            <path id="avatar-eyebrows" d="M 48 106 Q 54 103 60 106 M 68 106 Q 74 103 80 106" fill="none" stroke="#1e1b4b" stroke-width="2" stroke-linecap="round"/>

            <!-- Expressive Mouth (Changes dynamically in JS: Smile vs Thinking) -->
            <path id="avatar-mouth" d="M 56 128 Q 64 136 72 128" fill="none" stroke="#be123c" stroke-width="2.5" stroke-linecap="round"/>

            <!-- Cheeks Blush -->
            <circle cx="48" cy="122" r="4.5" fill="#fda4af" opacity="0.6"/>
            <circle cx="80" cy="122" r="4.5" fill="#fda4af" opacity="0.6"/>

            <!-- Right Arm Reaching to Table (Pointing to the Experiment) -->
            <path d="M 95 170 Q 120 185 140 210" fill="none" stroke="#f8fafc" stroke-width="14" stroke-linecap="round"/>
            <circle cx="140" cy="210" r="7" fill="#fdd8b5"/> <!-- Hand -->

            <!-- Left Arm at Side -->
            <path d="M 35 170 Q 22 210 25 240" fill="none" stroke="#f8fafc" stroke-width="12" stroke-linecap="round"/>
            <circle cx="25" cy="240" r="6" fill="#fdd8b5"/>
          </g>

          <!-- 4. MOSTAFA'S DYNAMIC SPEECH BUBBLE -->
          <g id="speech-bubble-group" class="floating-bubble" transform="translate(60, 22)">
            <!-- Bubble Box with Tail -->
            <path d="M 0 0 L 260 0 Q 272 0 272 12 L 272 65 Q 272 77 260 77 L 85 77 L 65 96 L 72 77 L 12 77 Q 0 77 0 65 Z" fill="#ffffff" filter="url(#softCompShadow)" stroke="#cbd5e1" stroke-width="1.5"/>
            <!-- Header -->
            <text x="14" y="22" fill="#2563eb" font-size="11" font-weight="900" letter-spacing="0.5">MOSTAFA (STUDENT GUIDE):</text>
            <!-- Dynamic Speech Line 1 -->
            <text id="speech-line-1" x="14" y="42" fill="#0f172a" font-size="12" font-weight="800">
              Pick an item from the toolbox!
            </text>
            <!-- Dynamic Speech Line 2 -->
            <text id="speech-line-2" x="14" y="60" fill="#475569" font-size="10.5" font-weight="600">
              Let's see if it lets electrons complete the loop!
            </text>
          </g>

          <!-- 5. 3D CIRCUIT COMPONENTS ON THE TABLETOP -->

          <!-- (A) 3D DUAL-CELL 3V BATTERY PACK (LEFT TABLE SURFACE) -->
          <g id="component-battery" transform="translate(230, 245)" filter="url(#softCompShadow)">
            <!-- Cast Shadow -->
            <ellipse cx="60" cy="50" rx="65" ry="16" fill="#000000" opacity="0.35"/>
            
            <!-- Battery Molded Casing (Black Plastic Tray) -->
            <rect x="0" y="8" width="120" height="45" rx="8" fill="#1e293b" stroke="#334155" stroke-width="2"/>
            
            <!-- AA Battery 1 (Top Blue Cylinder) -->
            <rect x="12" y="14" width="90" height="15" rx="4" fill="url(#wallGrad)" stroke="#38bdf8" stroke-width="1"/>
            <rect x="102" y="18" width="5" height="7" rx="2" fill="#cbd5e1"/> <!-- Nub (+) -->
            <text x="35" y="25" fill="#f8fafc" font-size="8" font-weight="900">1.5V ALKALINE</text>

            <!-- AA Battery 2 (Bottom Blue Cylinder) -->
            <rect x="18" y="32" width="90" height="15" rx="4" fill="url(#wallGrad)" stroke="#38bdf8" stroke-width="1"/>
            <rect x="13" y="36" width="5" height="7" rx="2" fill="#cbd5e1"/> <!-- Nub (+) reverse -->
            <text x="40" y="43" fill="#f8fafc" font-size="8" font-weight="900">1.5V ALKALINE</text>

            <!-- Red Positive Terminal Screw Post (Right) -->
            <circle cx="114" cy="20" r="6" fill="#ef4444" stroke="#b91c1c" stroke-width="1.5"/>
            <text x="111" y="24" fill="#ffffff" font-size="10" font-weight="900">+</text>

            <!-- Black Negative Terminal Screw Post (Left) -->
            <circle cx="6" cy="38" r="6" fill="#0f172a" stroke="#475569" stroke-width="1.5"/>
            <text x="4" y="41" fill="#ffffff" font-size="10" font-weight="900">&minus;</text>

            <!-- 3V Badge -->
            <rect x="42" y="55" width="42" height="14" rx="4" fill="#0f172a" stroke="#60a5fa" stroke-width="1"/>
            <text x="48" y="65" fill="#60a5fa" font-size="8.5" font-weight="900">3.0V DC</text>
          </g>

          <!-- (B) 3D PORCELAIN LAMP SOCKET & GLASS BULB (RIGHT TABLE SURFACE) -->
          <g id="component-lamp" transform="translate(630, 210)" filter="url(#softCompShadow)">
            <!-- Volumetric Light Beam Halo (Expands when on) -->
            <circle id="svg-bulb-glow" cx="24" cy="24" r="80" fill="url(#bulbVolumetricGlow)" opacity="0" class="bulb-radiance transition-opacity duration-300 pointer-events-none"/>
            
            <!-- Shadow of Socket Base -->
            <ellipse cx="24" cy="68" rx="38" ry="14" fill="#000000" opacity="0.4"/>
            
            <!-- White Ceramic Socket Base (Beveled Ring) -->
            <ellipse cx="24" cy="62" rx="34" ry="12" fill="#e2e8f0" stroke="#cbd5e1" stroke-width="1.5"/>
            <path d="M -10 62 Q 24 74 58 62 L 58 54 Q 24 66 -10 54 Z" fill="#94a3b8"/>
            <ellipse cx="24" cy="54" rx="34" ry="11" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1"/>

            <!-- Brass Screw Collar -->
            <rect x="12" y="38" width="24" height="16" rx="2" fill="#d97706" stroke="#b45309" stroke-width="1.2"/>
            <line x1="12" y1="42" x2="36" y2="42" stroke="#78350f" stroke-width="1"/>
            <line x1="12" y1="48" x2="36" y2="48" stroke="#78350f" stroke-width="1"/>

            <!-- Glass Bulb Sphere (3D Volume & Reflections) -->
            <circle id="svg-bulb-glass" cx="24" cy="20" r="26" fill="#334155" stroke="#94a3b8" stroke-width="2" opacity="0.85" class="transition-colors duration-300"/>
            <!-- Glass Specular Reflection Highlight -->
            <ellipse cx="16" cy="12" rx="8" ry="4" fill="#ffffff" opacity="0.35" transform="rotate(-30 16 12)"/>

            <!-- Tungsten Filament Coils -->
            <path id="svg-bulb-filament" d="M 16 28 L 20 16 L 24 22 L 28 16 L 32 28" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="transition-colors duration-300"/>

            <!-- Label -->
            <text x="0" y="86" fill="#f8fafc" font-size="10" font-weight="900" letter-spacing="0.5">STAGE 6 LAMP</text>
          </g>

          <!-- (C) CENTER SPECIMEN TESTING DISH & CROCODILE CLIPS -->
          <g id="component-testing-station" transform="translate(385, 270)">
            <!-- Specimen Dish Shadow -->
            <ellipse cx="65" cy="30" rx="85" ry="26" fill="#000000" opacity="0.35"/>
            
            <!-- Ceramic Petri Dish / Specimen Plate -->
            <ellipse cx="65" cy="24" rx="80" ry="22" fill="#0f172a" stroke="#334155" stroke-width="2"/>
            <ellipse cx="65" cy="22" rx="72" ry="18" fill="#1e293b" stroke="#475569" stroke-width="1"/>

            <!-- THE DYNAMIC SPECIMEN (OBJECTS SWAP CLEANLY INSIDE DISH) -->
            <g id="specimen-holder" transform="translate(20, 2)">
              
              <!-- State 0: Empty Gap (Default) -->
              <g id="item-empty">
                <text x="45" y="24" text-anchor="middle" font-size="20">❓</text>
                <text x="45" y="36" text-anchor="middle" fill="#94a3b8" font-size="9" font-weight="700">EMPTY TEST GAP</text>
              </g>

              <!-- State 1: Copper Coin (Conductor) -->
              <g id="item-coin" class="hidden">
                <ellipse cx="45" cy="20" rx="28" ry="16" fill="url(#copperCoinGrad)" stroke="#7c2d12" stroke-width="1.8"/>
                <ellipse cx="45" cy="19" rx="23" ry="12" fill="none" stroke="#fed7aa" stroke-width="1.2" stroke-dasharray="3,2"/>
                <text x="45" y="23" text-anchor="middle" fill="#fef3c7" font-size="10" font-weight="900">ONE POUND</text>
              </g>

              <!-- State 2: Rubber Eraser (Insulator) -->
              <g id="item-eraser" class="hidden">
                <!-- Beveled Angled Eraser Block -->
                <polygon points="15,16 65,10 75,25 25,31" fill="#f43f5e" stroke="#be123c" stroke-width="1.5"/>
                <polygon points="65,10 75,25 80,22 70,7" fill="#3b82f6" stroke="#1d4ed8" stroke-width="1.5"/>
                <text x="40" y="24" text-anchor="middle" fill="#ffffff" font-size="8.5" font-weight="900" transform="rotate(-6 40 24)">ERASER</text>
              </g>

              <!-- State 3: Pencil with Graphite Lead (Conductor) -->
              <g id="item-pencil" class="hidden">
                <!-- Hexagonal Yellow Pencil Body -->
                <polygon points="10,22 62,16 62,24 10,30" fill="url(#pencilWoodGrad)" stroke="#b45309" stroke-width="1.5"/>
                <!-- Sharpened Cedar Cone -->
                <polygon points="62,16 76,20 62,24" fill="#fed7aa"/>
                <!-- Exposed Pure Graphite Lead Point -->
                <polygon points="73,19 82,20 73,21" fill="url(#pencilLeadGrad)"/>
                <text x="35" y="26" text-anchor="middle" fill="#78350f" font-size="7" font-weight="900" transform="rotate(-6 35 26)">HB GRAPHITE</text>
              </g>

              <!-- State 4: Plastic Ruler (Insulator) -->
              <g id="item-ruler" class="hidden">
                <polygon points="10,14 78,14 74,27 6,27" fill="#38bdf8" fill-opacity="0.6" stroke="#0284c7" stroke-width="1.5"/>
                <!-- Tick Marks -->
                <line x1="20" y1="14" x2="20" y2="19" stroke="#0369a1" stroke-width="1"/>
                <line x1="30" y1="14" x2="30" y2="21" stroke="#0369a1" stroke-width="1"/>
                <line x1="40" y1="14" x2="40" y2="19" stroke="#0369a1" stroke-width="1"/>
                <line x1="50" y1="14" x2="50" y2="21" stroke="#0369a1" stroke-width="1"/>
                <line x1="60" y1="14" x2="60" y2="19" stroke="#0369a1" stroke-width="1"/>
                <text x="42" y="25" text-anchor="middle" fill="#0369a1" font-size="7" font-weight="900">PLASTIC cm</text>
              </g>

            </g>

            <!-- LEFT ALLIGATOR CLIP (CLAMPING ONTO SPECIMEN) -->
            <g id="clip-left" transform="translate(10, 12)">
              <rect x="-14" y="2" width="22" height="14" rx="3" fill="url(#goldClipGrad)" stroke="#78350f" stroke-width="1"/>
              <!-- Teeth Clamping -->
              <polygon points="8,4 18,9 8,14" fill="#b45309"/>
            </g>

            <!-- RIGHT ALLIGATOR CLIP (CLAMPING ONTO SPECIMEN) -->
            <g id="clip-right" transform="translate(108, 12)">
              <rect x="4" y="2" width="22" height="14" rx="3" fill="url(#goldClipGrad)" stroke="#78350f" stroke-width="1"/>
              <!-- Teeth Clamping -->
              <polygon points="4,4 -6,9 4,14" fill="#b45309"/>
            </g>

            <!-- Clean Station Title Beneath Dish -->
            <text x="65" y="58" text-anchor="middle" fill="#cbd5e1" font-size="10" font-weight="800">
              PHYSICAL GAP BRIDGE (CROCODILE CLIPS)
            </text>
          </g>

          <!-- 6. REALISTIC 3D FLEXIBLE JUMPER WIRES (CURVING ACROSS THE TABLE) -->
          
          <!-- (1) RED WIRE: From Battery (+) to Lamp Socket -->
          <!-- Shadow -->
          <path d="M 345 265 Q 490 200 642 260" fill="none" stroke="#000000" stroke-width="8" opacity="0.35"/>
          <!-- Outer Insulated Rubber -->
          <path d="M 345 265 Q 490 200 642 260" fill="none" stroke="#dc2626" stroke-width="6" stroke-linecap="round"/>
          <!-- 3D Highlight Line -->
          <path d="M 345 264 Q 490 199 642 259" fill="none" stroke="#fca5a5" stroke-width="1.8" stroke-linecap="round"/>

          <!-- (2) BLUE WIRE: From Lamp Socket to Right Alligator Clip -->
          <!-- Shadow -->
          <path d="M 642 274 Q 570 330 505 285" fill="none" stroke="#000000" stroke-width="8" opacity="0.35"/>
          <!-- Outer Insulated Rubber -->
          <path d="M 642 274 Q 570 330 505 285" fill="none" stroke="#2563eb" stroke-width="6" stroke-linecap="round"/>
          <!-- Highlight Line -->
          <path d="M 642 273 Q 570 329 505 284" fill="none" stroke="#93c5fd" stroke-width="1.8" stroke-linecap="round"/>

          <!-- (3) BLACK WIRE: From Battery (-) to Left Alligator Clip -->
          <!-- Shadow -->
          <path d="M 236 283 Q 290 350 395 285" fill="none" stroke="#000000" stroke-width="8" opacity="0.35"/>
          <!-- Outer Insulated Rubber -->
          <path d="M 236 283 Q 290 350 395 285" fill="none" stroke="#1e293b" stroke-width="6" stroke-linecap="round"/>
          <!-- Highlight Line -->
          <path d="M 236 282 Q 290 349 395 284" fill="none" stroke="#64748b" stroke-width="1.8" stroke-linecap="round"/>

          <!-- (4) DYNAMIC ELECTRON STREAM (ACTIVE ONLY WHEN CURRENT FLOWS) -->
          <g id="electron-stream" class="hidden">
            <!-- Full Loop Flow -->
            <path d="M 345 265 Q 490 200 642 260" fill="none" stroke="#fef08a" stroke-width="3" class="active-wire-flow"/>
            <path d="M 642 274 Q 570 330 505 285" fill="none" stroke="#fef08a" stroke-width="3" class="active-wire-flow"/>
            <path d="M 405 285 L 495 285" fill="none" stroke="#fef08a" stroke-width="3.5" class="active-wire-flow"/>
            <path d="M 395 285 Q 290 350 236 283" fill="none" stroke="#fef08a" stroke-width="3" class="active-wire-flow"/>
          </g>

          <!-- 7. DIGITAL MULTIMETER HUD (MOUNTED ON TABLE CORNER) -->
          <g id="multimeter-hud" transform="translate(620, 310)" filter="url(#softCompShadow)">
            <!-- Meter Body -->
            <rect x="0" y="0" width="135" height="52" rx="8" fill="#0f172a" stroke="#334155" stroke-width="2"/>
            <!-- LCD Screen -->
            <rect x="6" y="6" width="123" height="40" rx="4" fill="#020617" stroke="#1e293b" stroke-width="1"/>
            <!-- Readings -->
            <text x="12" y="20" fill="#64748b" font-size="7" font-weight="900">LAB SENSOR READINGS</text>
            <text id="meter-v" x="12" y="32" fill="#38bdf8" font-size="10" font-weight="900" font-family="monospace">VOLTS: 3.00 V</text>
            <text id="meter-i" x="12" y="43" fill="#ef4444" font-size="10" font-weight="900" font-family="monospace">CURRENT: 0.00 A</text>
          </g>

        </svg>
      </div>

      <!-- 3. REAL-TIME LAB STATUS & DIAGNOSTIC BAR -->
      <div id="result-card" class="bg-slate-900 border border-slate-700/80 rounded-2xl p-4 sm:p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs">
        <div class="flex items-start sm:items-center gap-3.5">
          <div id="result-icon-badge" class="w-9 h-9 rounded-xl bg-rose-950 border border-rose-800 text-rose-400 flex items-center justify-center font-black text-base shrink-0">
            ✕
          </div>
          <div>
            <div id="result-heading" class="font-black text-rose-300 text-sm sm:text-base">Circuit Open: Air Gap in Circuit</div>
            <p id="result-desc" class="text-slate-300 font-medium mt-0.5 leading-relaxed">
              Air is an electrical insulator. Electrons cannot jump across the crocodile clips, so current is 0 Amperes and the lamp remains off.
            </p>
          </div>
        </div>
        <div id="result-pill" class="self-start sm:self-center bg-slate-800 text-slate-400 px-4 py-1.5 rounded-full font-mono text-xs font-black border border-slate-700 whitespace-nowrap">
          CURRENT: 0.00 A (OFF)
        </div>
      </div>

      <!-- 4. MOSTAFA'S TOOLBOX (CLICKABLE SPECIMENS) -->
      <div class="space-y-3 pt-1">
        <div class="flex items-center justify-between text-xs font-bold text-slate-700">
          <span class="flex items-center gap-1.5">
            <span>🧰</span>
            <span>Click any material below to place it on the test plate:</span>
          </span>
          <span class="text-indigo-600 font-extrabold text-[11px]">Real-Time Reaction</span>
        </div>

        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3.5">
          
          <!-- Tool 1: Metal Coin -->
          <button onclick="selectMaterial('coin')" id="btn-mat-coin" class="tool-3d-card bg-white border-2 border-slate-200 rounded-2xl p-4 flex flex-col items-center justify-center text-center space-y-2 group cursor-pointer">
            <div class="w-14 h-14 rounded-2xl bg-amber-50 border border-amber-200 flex items-center justify-center text-3xl group-hover:scale-110 transition-transform">
              🪙
            </div>
            <div>
              <div class="font-black text-sm text-slate-900">Copper Coin</div>
              <div class="text-[11px] text-emerald-700 font-extrabold mt-0.5">Pure Metal (Conductor)</div>
            </div>
          </button>

          <!-- Tool 2: Rubber Eraser -->
          <button onclick="selectMaterial('eraser')" id="btn-mat-eraser" class="tool-3d-card bg-white border-2 border-slate-200 rounded-2xl p-4 flex flex-col items-center justify-center text-center space-y-2 group cursor-pointer">
            <div class="w-14 h-14 rounded-2xl bg-rose-50 border border-rose-200 flex items-center justify-center text-3xl group-hover:scale-110 transition-transform">
              🧹
            </div>
            <div>
              <div class="font-black text-sm text-slate-900">Rubber Eraser</div>
              <div class="text-[11px] text-rose-700 font-extrabold mt-0.5">Flexible Rubber (Insulator)</div>
            </div>
          </button>

          <!-- Tool 3: Pencil Graphite -->
          <button onclick="selectMaterial('pencil')" id="btn-mat-pencil" class="tool-3d-card bg-white border-2 border-slate-200 rounded-2xl p-4 flex flex-col items-center justify-center text-center space-y-2 group cursor-pointer">
            <div class="w-14 h-14 rounded-2xl bg-slate-100 border border-slate-300 flex items-center justify-center text-3xl group-hover:scale-110 transition-transform">
              ✏️
            </div>
            <div>
              <div class="font-black text-sm text-slate-900">Pencil Lead (Graphite)</div>
              <div class="text-[11px] text-indigo-700 font-extrabold mt-0.5">Special Non-Metal Conductor</div>
            </div>
          </button>

          <!-- Tool 4: Plastic Ruler -->
          <button onclick="selectMaterial('ruler')" id="btn-mat-ruler" class="tool-3d-card bg-white border-2 border-slate-200 rounded-2xl p-4 flex flex-col items-center justify-center text-center space-y-2 group cursor-pointer">
            <div class="w-14 h-14 rounded-2xl bg-sky-50 border border-sky-200 flex items-center justify-center text-3xl group-hover:scale-110 transition-transform">
              📏
            </div>
            <div>
              <div class="font-black text-sm text-slate-900">Plastic Ruler</div>
              <div class="text-[11px] text-rose-700 font-extrabold mt-0.5">Polymer Plastic (Insulator)</div>
            </div>
          </button>

        </div>
      </div>

    </section>

    <!-- 3. CHECKPOINT EXAM CHALLENGE (CAMBRIDGE MARK SCHEME) -->
    <section class="bg-white border border-slate-200 rounded-3xl p-6 sm:p-7 shadow-sm space-y-5">
      <div class="flex items-center justify-between border-b border-slate-100 pb-3">
        <div class="flex items-center gap-2.5">
          <span class="w-8 h-8 rounded-xl bg-indigo-100 text-indigo-700 font-black flex items-center justify-center text-sm">3</span>
          <h2 class="text-base sm:text-lg font-black text-slate-900">Cambridge Exam Checkpoint Questions</h2>
        </div>
        <span id="quiz-score-badge" class="text-xs bg-slate-100 text-slate-700 font-extrabold px-3 py-1 rounded-full border border-slate-300">
          Score: 0 / 3
        </span>
      </div>

      <div class="space-y-4">
        
        <!-- Q1 -->
        <div class="p-4 sm:p-5 rounded-2xl bg-slate-50 border border-slate-200 space-y-3">
          <div class="font-extrabold text-xs sm:text-sm text-slate-900">
            Q1. Mostafa sets up a circuit with a battery, a buzzer, and an unknown solid material in the gap. The buzzer buzzes loudly. What does this prove?
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
            <button onclick="answerQuestion(1, 'A', false)" class="q1-opt text-left p-3 rounded-xl border border-slate-200 bg-white hover:bg-slate-100 font-bold transition-colors">
              A) The material is an electrical insulator
            </button>
            <button onclick="answerQuestion(1, 'B', true)" class="q1-opt text-left p-3 rounded-xl border border-slate-200 bg-white hover:bg-slate-100 font-bold transition-colors">
              B) The material is an electrical conductor
            </button>
            <button onclick="answerQuestion(1, 'C', false)" class="q1-opt text-left p-3 rounded-xl border border-slate-200 bg-white hover:bg-slate-100 font-bold transition-colors">
              C) The circuit has an open air break
            </button>
            <button onclick="answerQuestion(1, 'D', false)" class="q1-opt text-left p-3 rounded-xl border border-slate-200 bg-white hover:bg-slate-100 font-bold transition-colors">
              D) The battery has run out of voltage
            </button>
          </div>
          <div id="feedback-1" class="hidden text-xs p-3 rounded-xl font-medium"></div>
        </div>

        <!-- Q2 -->
        <div class="p-4 sm:p-5 rounded-2xl bg-slate-50 border border-slate-200 space-y-3">
          <div class="font-extrabold text-xs sm:text-sm text-slate-900">
            Q2. Why is pencil lead (graphite) special compared to most non-metals like plastic or wood?
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
            <button onclick="answerQuestion(2, 'A', false)" class="q2-opt text-left p-3 rounded-xl border border-slate-200 bg-white hover:bg-slate-100 font-bold transition-colors">
              A) It is made of copper wire
            </button>
            <button onclick="answerQuestion(2, 'B', true)" class="q2-opt text-left p-3 rounded-xl border border-slate-200 bg-white hover:bg-slate-100 font-bold transition-colors">
              B) It is a form of carbon with free delocalized electrons
            </button>
            <button onclick="answerQuestion(2, 'C', false)" class="q2-opt text-left p-3 rounded-xl border border-slate-200 bg-white hover:bg-slate-100 font-bold transition-colors">
              C) It generates its own 3V electric charge
            </button>
            <button onclick="answerQuestion(2, 'D', false)" class="q2-opt text-left p-3 rounded-xl border border-slate-200 bg-white hover:bg-slate-100 font-bold transition-colors">
              D) It acts as an insulator at room temperature
            </button>
          </div>
          <div id="feedback-2" class="hidden text-xs p-3 rounded-xl font-medium"></div>
        </div>

        <!-- Q3 -->
        <div class="p-4 sm:p-5 rounded-2xl bg-slate-50 border border-slate-200 space-y-3">
          <div class="font-extrabold text-xs sm:text-sm text-slate-900">
            Q3. In a series circuit with two identical lamps, what happens if one bulb is unscrewed or breaks?
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
            <button onclick="answerQuestion(3, 'A', false)" class="q3-opt text-left p-3 rounded-xl border border-slate-200 bg-white hover:bg-slate-100 font-bold transition-colors">
              A) The other lamp gets twice as bright
            </button>
            <button onclick="answerQuestion(3, 'B', false)" class="q3-opt text-left p-3 rounded-xl border border-slate-200 bg-white hover:bg-slate-100 font-bold transition-colors">
              B) Nothing changes for the second lamp
            </button>
            <button onclick="answerQuestion(3, 'C', true)" class="q3-opt text-left p-3 rounded-xl border border-slate-200 bg-white hover:bg-slate-100 font-bold transition-colors">
              C) The second lamp goes off because the single loop is broken
            </button>
            <button onclick="answerQuestion(3, 'D', false)" class="q3-opt text-left p-3 rounded-xl border border-slate-200 bg-white hover:bg-slate-100 font-bold transition-colors">
              D) The battery explodes from excessive heat
            </button>
          </div>
          <div id="feedback-3" class="hidden text-xs p-3 rounded-xl font-medium"></div>
        </div>

      </div>

      <!-- SYNC TO PORTAL BUTTON -->
      <div class="pt-2 flex flex-col sm:flex-row items-center justify-between gap-3 border-t border-slate-100">
        <div class="text-xs text-slate-500 font-semibold flex items-center gap-1.5">
          <span>☁️</span> Auto-synced to Google Sheet & Parent Dashboard
        </div>
        <a href="../Index.html" class="w-full sm:w-auto inline-flex items-center justify-center gap-2 bg-gradient-to-r from-blue-600 to-indigo-700 hover:from-blue-700 hover:to-indigo-800 text-white font-extrabold px-6 py-2.5 rounded-xl shadow-md transition-all text-xs">
          <span>Return to Stage 6 Hub</span>
          <span>→</span>
        </a>
      </div>

    </section>

  </div>

  <script>
    let currentMaterial = null;
    let score = 0;
    const answered = {};

    function selectMaterial(mat) {
      currentMaterial = mat;

      // Update button visual styles
      ['coin', 'eraser', 'pencil', 'ruler'].forEach(id => {
        const btn = document.getElementById('btn-mat-' + id);
        if (id === mat) {
          btn.classList.add('active-selected');
        } else {
          btn.classList.remove('active-selected');
        }
      });

      // Hide all specimens inside the dish
      ['empty', 'coin', 'eraser', 'pencil', 'ruler'].forEach(id => {
        document.getElementById('item-' + id).classList.add('hidden');
      });
      // Show selected specimen
      document.getElementById('item-' + mat).classList.remove('hidden');

      // Elements to update
      const badge = document.getElementById('circuit-badge');
      const bulbGlow = document.getElementById('svg-bulb-glow');
      const bulbGlass = document.getElementById('svg-bulb-glass');
      const filament = document.getElementById('svg-bulb-filament');
      const deskLight = document.getElementById('svg-wood-light-glow');
      const electrons = document.getElementById('electron-stream');
      
      const speech1 = document.getElementById('speech-line-1');
      const speech2 = document.getElementById('speech-line-2');
      const avatarMouth = document.getElementById('avatar-mouth');
      const avatarBrows = document.getElementById('avatar-eyebrows');

      const meterV = document.getElementById('meter-v');
      const meterI = document.getElementById('meter-i');

      const iconBadge = document.getElementById('result-icon-badge');
      const heading = document.getElementById('result-heading');
      const desc = document.getElementById('result-desc');
      const pill = document.getElementById('result-pill');

      if (mat === 'coin') {
        // CONDUCTOR SUCCESS
        badge.className = "text-xs bg-emerald-100 text-emerald-800 font-extrabold px-3.5 py-1.5 rounded-full border border-emerald-300";
        badge.textContent = "Circuit: CLOSED (Current Flowing!)";

        // Light & Electrons
        bulbGlow.setAttribute('opacity', '0.9');
        bulbGlass.setAttribute('fill', '#fef08a');
        bulbGlass.setAttribute('stroke', '#eab308');
        filament.setAttribute('stroke', '#b45309');
        deskLight.setAttribute('opacity', '1');
        electrons.classList.remove('hidden');

        // Mostafa Cheering Expression & Speech
        avatarMouth.setAttribute('d', 'M 52 126 Q 64 142 76 126'); // Big smile
        avatarBrows.setAttribute('d', 'M 48 103 Q 54 99 60 103 M 68 103 Q 74 99 80 103'); // Excited high brows
        speech1.textContent = "Awesome! The copper coin conducts! 🌟💡";
        speech1.setAttribute('fill', '#059669');
        speech2.textContent = "Copper has millions of free electrons that complete the loop!";

        // Multimeter
        meterV.textContent = "VOLTS: 3.00 V";
        meterI.textContent = "CURRENT: 0.35 A";
        meterI.setAttribute('fill', '#10b981');

        // Diagnostic Bar
        iconBadge.className = "w-9 h-9 rounded-xl bg-emerald-950 border border-emerald-800 text-emerald-400 flex items-center justify-center font-black text-base shrink-0";
        iconBadge.textContent = "✓";
        heading.className = "font-black text-emerald-300 text-sm sm:text-base";
        heading.textContent = "SUCCESS: Copper is an Electrical Conductor!";
        desc.textContent = "Copper atoms share a sea of mobile valence electrons. The loop is 100% closed, powering the 3V lamp with radiant light!";
        pill.className = "self-start sm:self-center bg-emerald-900/60 text-emerald-300 px-4 py-1.5 rounded-full font-mono text-xs font-black border border-emerald-600";
        pill.textContent = "CURRENT: 0.35 A (ACTIVE)";

      } else if (mat === 'pencil') {
        // GRAPHITE CONDUCTOR SUCCESS
        badge.className = "text-xs bg-emerald-100 text-emerald-800 font-extrabold px-3.5 py-1.5 rounded-full border border-emerald-300";
        badge.textContent = "Circuit: CLOSED (Graphite Conducts!)";

        // Light & Electrons
        bulbGlow.setAttribute('opacity', '0.85');
        bulbGlass.setAttribute('fill', '#fef08a');
        bulbGlass.setAttribute('stroke', '#eab308');
        filament.setAttribute('stroke', '#b45309');
        deskLight.setAttribute('opacity', '0.8');
        electrons.classList.remove('hidden');

        // Mostafa Surprised & Happy Expression
        avatarMouth.setAttribute('d', 'M 54 126 Q 64 140 74 126');
        avatarBrows.setAttribute('d', 'M 48 102 Q 54 98 60 102 M 68 102 Q 74 98 80 102');
        speech1.textContent = "Surprise! Pencil lead conducts electricity! ✏️⚡";
        speech1.setAttribute('fill', '#059669');
        speech2.textContent = "Graphite is a non-metal, but its layered carbon has free electrons!";

        // Multimeter
        meterV.textContent = "VOLTS: 3.00 V";
        meterI.textContent = "CURRENT: 0.28 A";
        meterI.setAttribute('fill', '#10b981');

        // Diagnostic Bar
        iconBadge.className = "w-9 h-9 rounded-xl bg-emerald-950 border border-emerald-800 text-emerald-400 flex items-center justify-center font-black text-base shrink-0";
        iconBadge.textContent = "⭐";
        heading.className = "font-black text-emerald-300 text-sm sm:text-base";
        heading.textContent = "SURPRISE! Pencil Graphite is a Rare Non-Metal Conductor!";
        desc.textContent = "In graphite, each carbon atom bonds to 3 others, leaving one delocalized electron free to drift between layers. It powers the lamp!";
        pill.className = "self-start sm:self-center bg-emerald-900/60 text-emerald-300 px-4 py-1.5 rounded-full font-mono text-xs font-black border border-emerald-600";
        pill.textContent = "CURRENT: 0.28 A (ACTIVE)";

      } else if (mat === 'eraser') {
        // RUBBER INSULATOR
        badge.className = "text-xs bg-rose-100 text-rose-800 font-extrabold px-3.5 py-1.5 rounded-full border border-rose-300";
        badge.textContent = "Circuit: OPEN (Broken Gap)";

        // Light Off
        bulbGlow.setAttribute('opacity', '0');
        bulbGlass.setAttribute('fill', '#334155');
        bulbGlass.setAttribute('stroke', '#94a3b8');
        filament.setAttribute('stroke', '#64748b');
        deskLight.setAttribute('opacity', '0');
        electrons.classList.add('hidden');

        // Mostafa Thinking / Puzzled Expression
        avatarMouth.setAttribute('d', 'M 56 130 Q 64 126 72 130'); // Flat/thoughtful mouth
        avatarBrows.setAttribute('d', 'M 48 108 Q 54 105 60 108 M 68 104 Q 74 107 80 104'); // One raised brow
        speech1.textContent = "Hmm, the lamp is dark! Rubber is an insulator! 🛑";
        speech1.setAttribute('fill', '#e11d48');
        speech2.textContent = "Rubber atoms hold tightly to their electrons, blocking current.";

        // Multimeter
        meterV.textContent = "VOLTS: 3.00 V";
        meterI.textContent = "CURRENT: 0.00 A";
        meterI.setAttribute('fill', '#ef4444');

        // Diagnostic Bar
        iconBadge.className = "w-9 h-9 rounded-xl bg-rose-950 border border-rose-800 text-rose-400 flex items-center justify-center font-black text-base shrink-0";
        iconBadge.textContent = "✕";
        heading.className = "font-black text-rose-300 text-sm sm:text-base";
        heading.textContent = "NO CURRENT: Rubber is an Electrical Insulator!";
        desc.textContent = "Rubber has extremely high electrical resistance. It completely locks electrons in place, leaving the circuit broken and the lamp off.";
        pill.className = "self-start sm:self-center bg-rose-900/60 text-rose-300 px-4 py-1.5 rounded-full font-mono text-xs font-black border border-rose-600";
        pill.textContent = "CURRENT: 0.00 A (OFF)";

      } else if (mat === 'ruler') {
        // PLASTIC INSULATOR
        badge.className = "text-xs bg-rose-100 text-rose-800 font-extrabold px-3.5 py-1.5 rounded-full border border-rose-300";
        badge.textContent = "Circuit: OPEN (Broken Gap)";

        // Light Off
        bulbGlow.setAttribute('opacity', '0');
        bulbGlass.setAttribute('fill', '#334155');
        bulbGlass.setAttribute('stroke', '#94a3b8');
        filament.setAttribute('stroke', '#64748b');
        deskLight.setAttribute('opacity', '0');
        electrons.classList.add('hidden');

        // Mostafa Explaining Expression
        avatarMouth.setAttribute('d', 'M 58 131 Q 64 127 70 131');
        avatarBrows.setAttribute('d', 'M 48 107 Q 54 104 60 107 M 68 104 Q 74 107 80 104');
        speech1.textContent = "Plastic blocks the current completely! 🛑";
        speech1.setAttribute('fill', '#e11d48');
        speech2.textContent = "That's why wires are coated in plastic—for safety!";

        // Multimeter
        meterV.textContent = "VOLTS: 3.00 V";
        meterI.textContent = "CURRENT: 0.00 A";
        meterI.setAttribute('fill', '#ef4444');

        // Diagnostic Bar
        iconBadge.className = "w-9 h-9 rounded-xl bg-rose-950 border border-rose-800 text-rose-400 flex items-center justify-center font-black text-base shrink-0";
        iconBadge.textContent = "✕";
        heading.className = "font-black text-rose-300 text-sm sm:text-base";
        heading.textContent = "NO CURRENT: Plastic is an Electrical Insulator!";
        desc.textContent = "Synthetic polymers have tightly bound covalent electrons with no free charge carriers. Electricians use plastic to insulate live wires.";
        pill.className = "self-start sm:self-center bg-rose-900/60 text-rose-300 px-4 py-1.5 rounded-full font-mono text-xs font-black border border-rose-600";
        pill.textContent = "CURRENT: 0.00 A (OFF)";
      }
    }

    function answerQuestion(qNum, optLetter, isCorrect) {
      if (answered[qNum]) return;
      answered[qNum] = true;

      const buttons = document.querySelectorAll('.q' + qNum + '-opt');
      buttons.forEach(btn => {
        btn.disabled = true;
        if (btn.textContent.includes(optLetter + ')')) {
          btn.className = "text-left p-3 rounded-xl border font-bold " + (isCorrect ? "bg-emerald-50 border-emerald-500 text-emerald-800" : "bg-rose-50 border-rose-500 text-rose-800");
        }
      });

      const fb = document.getElementById('feedback-' + qNum);
      fb.classList.remove('hidden');

      if (isCorrect) {
        score++;
        fb.className = "text-xs p-3.5 rounded-xl font-medium bg-emerald-50 text-emerald-800 border border-emerald-200";
        fb.innerHTML = "<b>Correct! 🌟</b> " + (qNum === 1 ? "The buzzer sounds because the material conducts electricity and completes the circuit." : qNum === 2 ? "Graphite layers have free delocalized electrons that move under voltage." : "In a series circuit, there is only one pathway. Breaking any component stops current everywhere.");
      } else {
        fb.className = "text-xs p-3.5 rounded-xl font-medium bg-rose-50 text-rose-800 border border-rose-200";
        fb.innerHTML = "<b>Incorrect.</b> " + (qNum === 1 ? "Conducting materials complete the loop and allow current to sound the buzzer." : qNum === 2 ? "Graphite has free mobile electrons between its carbon layers, unlike other non-metals." : "In series, if one bulb goes off, the entire loop breaks and all other bulbs turn off.");
      }

      document.getElementById('quiz-score-badge').textContent = "Score: " + score + " / 3";
      if (score === 3) {
        document.getElementById('quiz-score-badge').className = "text-xs bg-emerald-100 text-emerald-800 font-extrabold px-3 py-1 rounded-full border border-emerald-300";
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
    print(f"Successfully written: {p} ({len(html_content)} bytes)")
