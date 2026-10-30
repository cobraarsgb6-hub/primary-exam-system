import os

updater_script = '''
with open(r"C:\\Users\\co0ob\\Projects\\primary-exam-system\\build_flawless_cambridge_lab.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update comp-specimen
old_specimen_start = code.find('<!-- 4. COMPONENT D: SPECIMEN CLAMPING GAP')
old_specimen_end = code.find('<!-- ============================================================== -->\\n          <!-- 5. HARMONIC BALANCED SERIES CIRCUIT WIRING', old_specimen_start)

new_comp_specimen = """<!-- 4. COMPONENT D: SPECIMEN CLAMPING GAP (BOTTOM CENTER)          -->
          <!-- PHOTOREALISTIC LABORATORY CROCODILE CLAMPING & ZERO COLLISION  -->
          <!-- ============================================================== -->
          <g id="comp-specimen" transform="translate(300, 205)" filter="url(#compShadow)">
            <!-- Insulated Phenolic Stage Base -->
            <rect x="0" y="0" width="240" height="115" rx="14" fill="#1e293b" stroke="#334155" stroke-width="2"/>
            
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

            <!-- Single Clean Station Diagnostic Label (Completely below the clips!) -->
            <text id="specimen-station-label" x="120" y="98" fill="#f87171" font-size="9" font-weight="700" font-family="monospace" text-anchor="middle">
              Circuit Open: Air is an insulator (0.00 Amps)
            </text>
          </g>
"""

code = code[:old_specimen_start] + new_comp_specimen + code[old_specimen_end:]

# 2. Update electron-stream-group to NOT paint over rubber boots and text!
old_stream_start = code.find('<!-- REAL-TIME ELECTRON STREAM')
old_stream_end = code.find('</svg>', old_stream_start)

new_stream = """<!-- REAL-TIME ELECTRON STREAM (FLOWS PRECISELY THROUGH LOOP) -->
          <g id="electron-stream-group" display="none">
            <path d="M 170 90 Q 225 45 290 80" fill="none" stroke="#facc15" stroke-width="2.5" class="electron-flow-active"/>
            <path d="M 360 80 Q 510 40 670 144" fill="none" stroke="#facc15" stroke-width="2.5" class="electron-flow-active"/>
            <path d="M 670 144 L 730 144" fill="none" stroke="#facc15" stroke-width="3" class="electron-flow-active"/>
            <path d="M 730 144 Q 700 280 530 260" fill="none" stroke="#facc15" stroke-width="2.5" class="electron-flow-active"/>
            <!-- Electron flow through specimen gap ONLY (Between jaws, no boot overlap!) -->
            <path d="M 460 260 L 380 260" fill="none" stroke="#facc15" stroke-width="2.5" class="electron-flow-active"/>
            <path d="M 310 260 Q 220 270 170 180" fill="none" stroke="#facc15" stroke-width="2.5" class="electron-flow-active"/>
          </g>\\n        """

code = code[:old_stream_start] + new_stream + code[old_stream_end:]

with open(r"C:\\Users\\co0ob\\Projects\\primary-exam-system\\build_flawless_cambridge_lab.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Updated build_flawless_cambridge_lab.py!")
'''

with open(r"C:\Users\co0ob\Projects\primary-exam-system\do_precision_update.py", "w", encoding="utf-8") as f:
    f.write(updater_script)

print("do_precision_update.py created!")
