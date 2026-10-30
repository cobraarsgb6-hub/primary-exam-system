import re

with open(r"C:\Users\co0ob\Projects\primary-exam-system\build_flawless_cambridge_lab.py", "r", encoding="utf-8") as f:
    text = f.read()

# Replace the entire comp-specimen block with the perfected zero-collision version
old_comp_specimen = '''          <!-- ============================================================== -->
          <!-- 4. COMPONENT D: SPECIMEN CLAMPING GAP (BOTTOM CENTER)          -->
          <!-- FEATURING REALISTIC LAB CROCODILE CLIPS WITH SERRATED JAWS     -->
          <!-- ============================================================== -->
          <g id="comp-specimen" transform="translate(300, 205)" filter="url(#compShadow)">
            <!-- Insulated Phenolic Stage Base -->
            <rect x="0" y="0" width="240" height="115" rx="14" fill="#1e293b" stroke="#334155" stroke-width="2"/>
            
            <!-- In-Canvas Component Badge -->
            <rect x="45" y="-14" width="150" height="16" rx="4" fill="#0f172a" opacity="0.9"/>
            <text x="120" y="-2" fill="#34d399" font-size="8.5" font-weight="800" font-family="monospace" text-anchor="middle">🧲 SPECIMEN TEST GAP</text>

            <!-- Specimen Display Layer -->
            <g id="specimen-holder">
              <!-- Default: Empty Break (Air Gap) -->
              <g id="item-none" display="block">
                <text x="120" y="54" fill="#f87171" font-size="11" font-weight="800" text-anchor="middle" font-family="monospace">
                  ⚠ AIR GAP (OPEN)
                </text>
                <text x="120" y="74" fill="#94a3b8" font-size="8.5" font-weight="600" text-anchor="middle">
                  Clamp material between alligator jaws
                </text>
              </g>

              <!-- Item 1: British 1p Copper Penny (AUTHENTIC COIN - NO TEXT CUT THROUGH!) -->
              <!-- Center at cx=120, cy=55. Radius r=42 -> Spans 78 to 162. Jaws bite firmly onto edges! -->
              <g id="item-coin" display="none">
                <circle cx="120" cy="55" r="42" fill="url(#realCopper)" stroke="#7c2d12" stroke-width="2.5"/>
                <circle cx="120" cy="55" r="37" fill="none" stroke="#fed7aa" stroke-width="1.5" stroke-dasharray="3,3" opacity="0.8"/>
                <!-- Embossed Royal Crown Emblem -->
                <path d="M 108 48 L 112 42 L 120 46 L 128 42 L 132 48 L 130 52 L 110 52 Z" fill="#fed7aa" stroke="#c2410c" stroke-width="1"/>
                <circle cx="112" cy="40" r="1.5" fill="#fef08a"/>
                <circle cx="120" cy="38" r="1.5" fill="#fef08a"/>
                <circle cx="128" cy="40" r="1.5" fill="#fef08a"/>
                <!-- Embossed "1" Below Electron Path -->
                <text x="120" y="72" text-anchor="middle" fill="#fed7aa" font-size="16" font-weight="900" font-family="serif">1</text>
              </g>

              <!-- Item 2: Rubber Eraser -->
              <g id="item-eraser" display="none">
                <rect x="76" y="37" width="88" height="36" rx="4" fill="#fb7185" stroke="#e11d48" stroke-width="2"/>
                <path d="M 76 37 L 96 37 L 96 73 L 76 73 Z" fill="#38bdf8"/>
                <text x="126" y="60" text-anchor="middle" fill="#ffffff" font-size="9" font-weight="900" font-family="sans-serif">RUBBER</text>
              </g>

              <!-- Item 3: HB Graphite Pencil (Wood clamped at left; exposed graphite clamped at right) -->
              <g id="item-pencil" display="none">
                <!-- Hexagonal Wood Barrel (74 to 138) -->
                <rect x="74" y="49" width="64" height="12" rx="2" fill="#d97706" stroke="#b45309" stroke-width="1.5"/>
                <line x1="74" y1="55" x2="138" y2="55" stroke="#f59e0b" stroke-width="1.5"/>
                <!-- Sharpened Conical Wood (138 to 154) -->
                <polygon points="138,49 154,55 138,61" fill="#fed7aa" stroke="#d97706" stroke-width="1"/>
                <!-- Exposed Pure Graphite Tip (154 to 164 - Clamped directly by Right Crocodile Clip!) -->
                <polygon points="154,52 164,55 154,58" fill="#0f172a" stroke="#000000" stroke-width="1"/>
                <text x="106" y="58" text-anchor="middle" fill="#ffffff" font-size="7" font-weight="900" font-family="monospace">HB GRAPHITE</text>
              </g>

              <!-- Item 4: Acrylic Plastic Ruler -->
              <g id="item-ruler" display="none">
                <rect x="76" y="41" width="88" height="28" rx="3" fill="#e0f2fe" stroke="#0284c7" stroke-width="1.5" fill-opacity="0.85"/>
                <!-- Centimeter Hash Marks -->
                <line x1="85" y1="41" x2="85" y2="49" stroke="#0369a1" stroke-width="1.5"/>
                <line x1="100" y1="41" x2="100" y2="53" stroke="#0369a1" stroke-width="1.5"/>
                <line x1="115" y1="41" x2="115" y2="49" stroke="#0369a1" stroke-width="1.5"/>
                <line x1="130" y1="41" x2="130" y2="53" stroke="#0369a1" stroke-width="1.5"/>
                <line x1="145" y1="41" x2="145" y2="49" stroke="#0369a1" stroke-width="1.5"/>
                <text x="120" y="63" text-anchor="middle" fill="#0369a1" font-size="8" font-weight="900" font-family="monospace">PLASTIC</text>
              </g>
            </g>

            <!-- ============================================================== -->
            <!-- REALISTIC LAB ALLIGATOR CLIPS WITH STEEL SERRATED JAWS & BOOTS -->
            <!-- ============================================================== -->

            <!-- LEFT ALLIGATOR CLIP (BLACK RUBBER BOOT + STEEL CHROME TOOTHED JAW) -->
            <g id="clip-left">
              <!-- Black Rubber Boot / Sleeve where wire enters -->
              <rect x="10" y="44" width="40" height="22" rx="5" fill="url(#rubberBootLeft)" stroke="#334155" stroke-width="1.5"/>
              <!-- Boot Grip Ribs -->
              <line x1="18" y1="47" x2="18" y2="63" stroke="#475569" stroke-width="1.5"/>
              <line x1="25" y1="47" x2="25" y2="63" stroke="#475569" stroke-width="1.5"/>
              <line x1="32" y1="47" x2="32" y2="63" stroke="#475569" stroke-width="1.5"/>
              <!-- Squeeze Lever -->
              <path d="M 20 44 L 28 34 L 36 44 Z" fill="#1e293b" stroke="#475569" stroke-width="1"/>
              
              <!-- Steel Pivot Hinge -->
              <rect x="46" y="48" width="12" height="14" rx="2" fill="url(#chromeMetal)" stroke="#64748b" stroke-width="1"/>
              <circle cx="52" cy="55" r="3" fill="#cbd5e1" stroke="#475569" stroke-width="1"/>
              
              <!-- Silver Chrome Upper Jaw -->
              <path d="M 54 51 L 76 51 L 80 55 L 56 55 Z" fill="url(#chromeMetal)" stroke="#475569" stroke-width="1"/>
              <!-- Silver Chrome Lower Jaw -->
              <path d="M 56 55 L 80 55 L 76 59 L 54 59 Z" fill="url(#chromeMetal)" stroke="#475569" stroke-width="1"/>
              <!-- Serrated Alligator Teeth Biting Specimen at x=78 -->
              <polygon points="62,53 65,57 68,53 71,57 74,53 77,57" fill="#0f172a"/>
            </g>

            <!-- RIGHT ALLIGATOR CLIP (BLUE RUBBER BOOT + STEEL CHROME TOOTHED JAW) -->
            <g id="clip-right">
              <!-- Blue Rubber Boot / Sleeve where wire enters -->
              <rect x="190" y="44" width="40" height="22" rx="5" fill="url(#rubberBootRight)" stroke="#1e40af" stroke-width="1.5"/>
              <!-- Boot Grip Ribs -->
              <line x1="208" y1="47" x2="208" y2="63" stroke="#60a5fa" stroke-width="1.5"/>
              <line x1="215" y1="47" x2="215" y2="63" stroke="#60a5fa" stroke-width="1.5"/>
              <line x1="222" y1="47" x2="222" y2="63" stroke="#60a5fa" stroke-width="1.5"/>
              <!-- Squeeze Lever -->
              <path d="M 204 44 L 212 34 L 220 44 Z" fill="#1e3a8a" stroke="#2563eb" stroke-width="1"/>
              
              <!-- Steel Pivot Hinge -->
              <rect x="182" y="48" width="12" height="14" rx="2" fill="url(#chromeMetal)" stroke="#64748b" stroke-width="1"/>
              <circle cx="188" cy="55" r="3" fill="#cbd5e1" stroke="#475569" stroke-width="1"/>
              
              <!-- Silver Chrome Upper Jaw (Pointing Left) -->
              <path d="M 186 51 L 164 51 L 160 55 L 184 55 Z" fill="url(#chromeMetal)" stroke="#475569" stroke-width="1"/>
              <!-- Silver Chrome Lower Jaw (Pointing Left) -->
              <path d="M 184 55 L 160 55 L 164 59 L 186 59 Z" fill="url(#chromeMetal)" stroke="#475569" stroke-width="1"/>
              <!-- Serrated Alligator Teeth Biting Specimen at x=162 -->
              <polygon points="178,53 175,57 172,53 169,57 166,53 163,57" fill="#0f172a"/>
            </g>

            <!-- Station Label Below (Completely free from any wire crossing!) -->
            <text id="specimen-station-label" x="120" y="103" fill="#94a3b8" font-size="8.5" font-weight="700" font-family="monospace" text-anchor="middle">
              Awaiting specimen selection
            </text>
          </g>'''

new_comp_specimen = '''          <!-- ============================================================== -->
          <!-- 4. COMPONENT D: SPECIMEN CLAMPING GAP (BOTTOM CENTER)          -->
          <!-- ERGONOMIC ALLIGATOR CLIPS WITH ZERO TEXT COLLISIONS             -->
          <!-- ============================================================== -->
          <g id="comp-specimen" transform="translate(300, 205)" filter="url(#compShadow)">
            <!-- Insulated Phenolic Stage Base -->
            <rect x="0" y="0" width="240" height="115" rx="14" fill="#1e293b" stroke="#334155" stroke-width="2"/>
            
            <!-- In-Canvas Component Badge -->
            <rect x="45" y="-14" width="150" height="16" rx="4" fill="#0f172a" opacity="0.9"/>
            <text x="120" y="-2" fill="#34d399" font-size="8.5" font-weight="800" font-family="monospace" text-anchor="middle">🧲 SPECIMEN TEST GAP</text>

            <!-- Specimen Display Layer -->
            <g id="specimen-holder">
              <!-- Default: Empty Break (Clean air slot with zero text collisions) -->
              <g id="item-none" display="block">
                <!-- Visual Air Slot Target -->
                <rect x="86" y="42" width="68" height="26" rx="6" fill="#0f172a" stroke="#f87171" stroke-width="1.5" stroke-dasharray="4,4" fill-opacity="0.6"/>
                <text x="120" y="58" fill="#f87171" font-size="9" font-weight="900" font-family="monospace" text-anchor="middle">
                  AIR BREAK
                </text>
              </g>

              <!-- Item 1: British 1p Copper Penny (AUTHENTIC COIN - NO TEXT CUT THROUGH!) -->
              <!-- Center at cx=120, cy=55. Radius r=38 -> Spans 82 to 158. Jaws bite firmly onto edges! -->
              <g id="item-coin" display="none">
                <circle cx="120" cy="55" r="38" fill="url(#realCopper)" stroke="#7c2d12" stroke-width="2.5"/>
                <circle cx="120" cy="55" r="33" fill="none" stroke="#fed7aa" stroke-width="1.5" stroke-dasharray="3,3" opacity="0.8"/>
                <!-- Embossed Royal Crown Emblem -->
                <path d="M 110 47 L 113 41 L 120 45 L 127 41 L 130 47 L 128 51 L 112 51 Z" fill="#fed7aa" stroke="#c2410c" stroke-width="1"/>
                <circle cx="113" cy="39" r="1.5" fill="#fef08a"/>
                <circle cx="120" cy="37" r="1.5" fill="#fef08a"/>
                <circle cx="127" cy="39" r="1.5" fill="#fef08a"/>
                <!-- Embossed "1" Below Electron Path -->
                <text x="120" y="72" text-anchor="middle" fill="#fed7aa" font-size="16" font-weight="900" font-family="serif">1</text>
              </g>

              <!-- Item 2: Rubber Eraser -->
              <g id="item-eraser" display="none">
                <rect x="80" y="37" width="80" height="36" rx="4" fill="#fb7185" stroke="#e11d48" stroke-width="2"/>
                <path d="M 80 37 L 100 37 L 100 73 L 80 73 Z" fill="#38bdf8"/>
                <text x="130" y="60" text-anchor="middle" fill="#ffffff" font-size="9" font-weight="900" font-family="sans-serif">RUBBER</text>
              </g>

              <!-- Item 3: HB Graphite Pencil (Wood clamped at left; exposed graphite clamped at right) -->
              <g id="item-pencil" display="none">
                <!-- Hexagonal Wood Barrel (78 to 138) -->
                <rect x="78" y="49" width="60" height="12" rx="2" fill="#d97706" stroke="#b45309" stroke-width="1.5"/>
                <line x1="78" y1="55" x2="138" y2="55" stroke="#f59e0b" stroke-width="1.5"/>
                <!-- Sharpened Conical Wood (138 to 152) -->
                <polygon points="138,49 152,55 138,61" fill="#fed7aa" stroke="#d97706" stroke-width="1"/>
                <!-- Exposed Pure Graphite Tip (152 to 162 - Clamped directly by Right Crocodile Clip!) -->
                <polygon points="152,52 162,55 152,58" fill="#0f172a" stroke="#000000" stroke-width="1"/>
                <text x="108" y="58" text-anchor="middle" fill="#ffffff" font-size="7" font-weight="900" font-family="monospace">HB GRAPHITE</text>
              </g>

              <!-- Item 4: Acrylic Plastic Ruler -->
              <g id="item-ruler" display="none">
                <rect x="80" y="41" width="80" height="28" rx="3" fill="#e0f2fe" stroke="#0284c7" stroke-width="1.5" fill-opacity="0.85"/>
                <!-- Centimeter Hash Marks -->
                <line x1="90" y1="41" x2="90" y2="49" stroke="#0369a1" stroke-width="1.5"/>
                <line x1="105" y1="41" x2="105" y2="53" stroke="#0369a1" stroke-width="1.5"/>
                <line x1="120" y1="41" x2="120" y2="49" stroke="#0369a1" stroke-width="1.5"/>
                <line x1="135" y1="41" x2="135" y2="53" stroke="#0369a1" stroke-width="1.5"/>
                <line x1="150" y1="41" x2="150" y2="49" stroke="#0369a1" stroke-width="1.5"/>
                <text x="120" y="63" text-anchor="middle" fill="#0369a1" font-size="8" font-weight="900" font-family="monospace">PLASTIC</text>
              </g>
            </g>

            <!-- ============================================================== -->
            <!-- REALISTIC LAB ALLIGATOR CLIPS (CLEAN ERGONOMIC BOOTS & JAWS)   -->
            <!-- ============================================================== -->

            <!-- LEFT ALLIGATOR CLIP (BLACK RUBBER BOOT + STEEL CHROME TOOTHED JAW) -->
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
              
              <!-- Silver Chrome Upper Jaw -->
              <path d="M 58 51 L 78 51 L 82 55 L 60 55 Z" fill="url(#chromeMetal)" stroke="#475569" stroke-width="1"/>
              <!-- Silver Chrome Lower Jaw -->
              <path d="M 60 55 L 82 55 L 78 59 L 58 59 Z" fill="url(#chromeMetal)" stroke="#475569" stroke-width="1"/>
              <!-- Serrated Alligator Teeth Biting Specimen at x=82 -->
              <polygon points="66,53 69,57 72,53 75,57 78,53 81,57" fill="#0f172a"/>
            </g>

            <!-- RIGHT ALLIGATOR CLIP (BLUE RUBBER BOOT + STEEL CHROME TOOTHED JAW) -->
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
              
              <!-- Silver Chrome Upper Jaw (Pointing Left) -->
              <path d="M 182 51 L 162 51 L 158 55 L 180 55 Z" fill="url(#chromeMetal)" stroke="#475569" stroke-width="1"/>
              <!-- Silver Chrome Lower Jaw (Pointing Left) -->
              <path d="M 180 55 L 158 55 L 162 59 L 182 59 Z" fill="url(#chromeMetal)" stroke="#475569" stroke-width="1"/>
              <!-- Serrated Alligator Teeth Biting Specimen at x=158 -->
              <polygon points="174,53 171,57 168,53 165,57 162,53 159,57" fill="#0f172a"/>
            </g>

            <!-- Single Clean Station Diagnostic Label (Completely below the clips!) -->
            <text id="specimen-station-label" x="120" y="98" fill="#f87171" font-size="9" font-weight="700" font-family="monospace" text-anchor="middle">
              Circuit Open: Air is an insulator (0.00 Amps)
            </text>
          </g>'''

text = text.replace(old_comp_specimen, new_comp_specimen)

with open(r"C:\Users\co0ob\Projects\primary-exam-system\build_flawless_cambridge_lab.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Updated build_flawless_cambridge_lab.py!")
