import base64
import os

SCRATCH_DIR = "/Users/egor/.gemini/antigravity/scratch/egorfm"
CARDS_DIR = os.path.join(SCRATCH_DIR, "assets/cards")
SPRITES_DIR = os.path.join(SCRATCH_DIR, "assets/sprites")

def get_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

rayquaza_b64 = get_b64(os.path.join(CARDS_DIR, "rayquaza.png"))
porygonz_b64 = get_b64(os.path.join(CARDS_DIR, "porygonz.png"))
mewtwo_b64 = get_b64(os.path.join(CARDS_DIR, "mewtwo.png"))
pikachu_b64 = get_b64(os.path.join(CARDS_DIR, "pikachu.png"))

# ==============================================================================
# 1. HEADER BANNER SVG
# ==============================================================================
def create_header():
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 220" width="920" height="220" fill="none">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0a0a14"/>
      <stop offset="50%" stop-color="#121124"/>
      <stop offset="100%" stop-color="#1a103c"/>
    </linearGradient>
    <linearGradient id="neonBorder" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#10b981"/>
      <stop offset="35%" stop-color="#06b6d4"/>
      <stop offset="70%" stop-color="#8b5cf6"/>
      <stop offset="100%" stop-color="#ec4899"/>
    </linearGradient>
    <linearGradient id="titleGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="70%" stop-color="#e0e7ff"/>
      <stop offset="100%" stop-color="#a5b4fc"/>
    </linearGradient>
    <radialGradient id="glowG" cx="20%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#10b981" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#10b981" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glowP" cx="80%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#8b5cf6" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#8b5cf6" stop-opacity="0"/>
    </radialGradient>
    <pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse">
      <path d="M 30 0 L 0 0 0 30" fill="none" stroke="#312e81" stroke-width="0.8" opacity="0.3"/>
    </pattern>
  </defs>

  <!-- Background Base -->
  <rect width="920" height="220" rx="18" fill="url(#bgGrad)"/>
  <rect width="920" height="220" rx="18" fill="url(#grid)"/>
  <circle cx="200" cy="110" r="180" fill="url(#glowG)"/>
  <circle cx="750" cy="110" r="200" fill="url(#glowP)"/>

  <!-- Border -->
  <rect x="1.5" y="1.5" width="917" height="217" rx="16.5" stroke="url(#neonBorder)" stroke-width="2.5"/>

  <!-- Left Pikachu Art -->
  <g transform="translate(30, 15)">
    <circle cx="95" cy="95" r="75" fill="#f59e0b" fill-opacity="0.12"/>
    <circle cx="95" cy="95" r="60" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="4 4" stroke-opacity="0.4"/>
    <image href="data:image/png;base64,{pikachu_b64}" x="15" y="15" width="160" height="160" preserveAspectRatio="xMidYMid meet"/>
  </g>

  <!-- Center Content -->
  <g transform="translate(240, 42)">
    <!-- Top Pill: Status -->
    <rect x="0" y="0" width="220" height="24" rx="12" fill="#1e1b4b" stroke="#6366f1" stroke-width="1.2"/>
    <circle cx="14" cy="12" r="4.5" fill="#10b981"/>
    <text x="28" y="16" font-family="system-ui, -apple-system, sans-serif" font-weight="700" font-size="11" fill="#38bdf8" letter-spacing="1.2">LEVEL 99 • DATA &amp; AI LAB</text>

    <!-- Main Title -->
    <text x="0" y="62" font-family="system-ui, -apple-system, sans-serif" font-weight="900" font-size="34" fill="url(#titleGrad)" letter-spacing="0.5">EGOR // PYTHON DEVELOPER</text>
    
    <!-- Subtitle: Specialization -->
    <text x="0" y="92" font-family="system-ui, -apple-system, sans-serif" font-weight="600" font-size="16" fill="#94a3b8">
      Building robust systems at the intersection of:
    </text>

    <!-- Tags Row -->
    <g transform="translate(0, 108)">
      <!-- Tag 1: Data Engineering -->
      <rect x="0" y="0" width="180" height="28" rx="6" fill="#064e3b" fill-opacity="0.6" stroke="#10b981" stroke-width="1.2"/>
      <text x="90" y="18" font-family="system-ui, -apple-system, sans-serif" font-weight="700" font-size="11" fill="#34d399" text-anchor="middle" letter-spacing="0.8">⚡ DATA ENGINEERING</text>

      <!-- Tag 2: Analytics -->
      <rect x="190" y="0" width="130" height="28" rx="6" fill="#0c4a6e" fill-opacity="0.6" stroke="#0ea5e9" stroke-width="1.2"/>
      <text x="255" y="18" font-family="system-ui, -apple-system, sans-serif" font-weight="700" font-size="11" fill="#38bdf8" text-anchor="middle" letter-spacing="0.8">📊 ANALYTICS</text>

      <!-- Tag 3: AI & Machine Learning -->
      <rect x="330" y="0" width="180" height="28" rx="6" fill="#4c1d95" fill-opacity="0.6" stroke="#8b5cf6" stroke-width="1.2"/>
      <text x="420" y="18" font-family="system-ui, -apple-system, sans-serif" font-weight="700" font-size="11" fill="#c084fc" text-anchor="middle" letter-spacing="0.8">🧠 ARTIFICIAL INTEL</text>
    </g>
  </g>

  <!-- Right Pixel Pokeball Accent -->
  <g transform="translate(805, 50)" opacity="0.75">
    <circle cx="45" cy="45" r="42" fill="#18182b" stroke="#6366f1" stroke-width="2.5"/>
    <path d="M 5 45 A 40 40 0 0 1 85 45 Z" fill="#ef4444"/>
    <path d="M 5 45 A 40 40 0 0 0 85 45 Z" fill="#ffffff"/>
    <line x1="5" y1="45" x2="85" y2="45" stroke="#18182b" stroke-width="6"/>
    <circle cx="45" cy="45" r="14" fill="#ffffff" stroke="#18182b" stroke-width="5"/>
    <circle cx="45" cy="45" r="6" fill="#ffffff"/>
  </g>
</svg>'''

import html

def xml_esc(s):
    if isinstance(s, list):
        return [xml_esc(item) for item in s]
    return html.escape(str(s))

# ==============================================================================
# 2. POKEMON TCG EX CARDS
# ==============================================================================
def create_card(
    filename,
    stage_text,
    pokemon_name,
    hp_val,
    type_symbol,
    type_color,
    bg_start,
    bg_end,
    b64_art,
    role_badge,
    role_color,
    move1_cost,
    move1_name,
    move1_dmg,
    move1_desc,
    move2_cost,
    move2_name,
    move2_dmg,
    move2_desc,
    rule_desc,
    card_number,
    accent_glow
):
    stage_text = xml_esc(stage_text)
    pokemon_name = xml_esc(pokemon_name)
    move1_name = xml_esc(move1_name)
    move1_desc = xml_esc(move1_desc)
    move2_name = xml_esc(move2_name)
    move2_desc = xml_esc(move2_desc)
    rule_desc = xml_esc(rule_desc)
    role_badge = xml_esc(role_badge)

    cost1_svg = "".join([f'<circle cx="{28 + i*20}" cy="316" r="8" fill="{type_color}" stroke="#0f172a" stroke-width="1.5"/>' for i in range(move1_cost)])
    cost2_svg = "".join([f'<circle cx="{28 + i*20}" cy="404" r="8" fill="{type_color}" stroke="#0f172a" stroke-width="1.5"/>' for i in range(move2_cost)])

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 600" width="420" height="600" fill="none">
  <defs>
    <!-- Card Metallic Holographic Border -->
    <linearGradient id="holoBorder" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#cbd5e1"/>
      <stop offset="25%" stop-color="#94a3b8"/>
      <stop offset="50%" stop-color="#f8fafc"/>
      <stop offset="75%" stop-color="#64748b"/>
      <stop offset="100%" stop-color="#cbd5e1"/>
    </linearGradient>

    <!-- Card Background -->
    <linearGradient id="cardBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{bg_start}"/>
      <stop offset="100%" stop-color="{bg_end}"/>
    </linearGradient>

    <!-- EX Badge Gradient -->
    <linearGradient id="exGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0284c7"/>
      <stop offset="50%" stop-color="#38bdf8"/>
      <stop offset="100%" stop-color="#e0f2fe"/>
    </linearGradient>

    <!-- Art Frame Glow -->
    <radialGradient id="artGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{accent_glow}" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="{accent_glow}" stop-opacity="0"/>
    </radialGradient>

    <!-- Holo Shine Sheen -->
    <linearGradient id="holoSheen" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.3"/>
      <stop offset="50%" stop-color="#ffffff" stop-opacity="0.05"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0.25"/>
    </linearGradient>
  </defs>

  <!-- Outer Holographic Metallic Border (radius 24) -->
  <rect x="3" y="3" width="414" height="594" rx="22" fill="url(#holoBorder)"/>
  <rect x="7" y="7" width="406" height="586" rx="19" fill="#090d16"/>
  <rect x="10" y="10" width="400" height="580" rx="16" fill="url(#cardBg)"/>

  <!-- ================= HEADER BAR ================= -->
  <!-- Stage Pill -->
  <rect x="22" y="20" width="60" height="20" rx="5" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.2"/>
  <text x="52" y="34" font-family="system-ui, -apple-system, sans-serif" font-weight="900" font-size="10.5" fill="#0f172a" text-anchor="middle" letter-spacing="0.5">{stage_text}</text>

  <!-- Pokemon Name -->
  <text x="90" y="36" font-family="system-ui, -apple-system, sans-serif" font-weight="900" font-size="19" fill="#ffffff" letter-spacing="0.5">{pokemon_name}</text>
  
  <!-- "ex" Badge -->
  <rect x="222" y="21" width="30" height="19" rx="4" fill="url(#exGrad)" stroke="#ffffff" stroke-width="0.8"/>
  <text x="237" y="35" font-family="system-ui, -apple-system, sans-serif" font-weight="900" font-style="italic" font-size="13" fill="#0f172a" text-anchor="middle">ex</text>

  <!-- HP & Type Orb -->
  <text x="338" y="35" font-family="system-ui, -apple-system, sans-serif" font-weight="800" font-size="12" fill="#94a3b8" text-anchor="end">HP</text>
  <text x="374" y="36" font-family="system-ui, -apple-system, sans-serif" font-weight="900" font-size="21" fill="#ffffff" text-anchor="end">{hp_val}</text>
  
  <!-- Type Energy Orb -->
  <circle cx="390" cy="30" r="11" fill="{type_color}" stroke="#ffffff" stroke-width="1.5"/>
  <text x="390" y="35" font-family="system-ui, sans-serif" font-size="12" text-anchor="middle">{type_symbol}</text>

  <!-- ================= ARTWORK WINDOW ================= -->
  <g transform="translate(18, 50)">
    <!-- Art Frame with Shadow & Border -->
    <rect width="384" height="236" rx="12" fill="#060911" stroke="url(#holoBorder)" stroke-width="1.8"/>
    <!-- Scenic Glow -->
    <rect width="384" height="236" rx="12" fill="url(#artGlow)"/>
    
    <!-- Pokemon Artwork Image -->
    <image href="data:image/png;base64,{b64_art}" x="77" y="3" width="230" height="230" preserveAspectRatio="xMidYMid meet"/>
    
    <!-- Holo Shine Sheen overlay -->
    <polygon points="0,0 90,0 20,236 0,236" fill="url(#holoSheen)"/>
    <polygon points="130,0 220,0 150,236 60,236" fill="url(#holoSheen)" opacity="0.6"/>

    <!-- Role Banner Badge across bottom of art -->
    <rect x="12" y="204" width="160" height="22" rx="5" fill="#090d16" fill-opacity="0.85" stroke="{role_color}" stroke-width="1.2"/>
    <text x="92" y="219" font-family="system-ui, -apple-system, sans-serif" font-weight="800" font-size="10.5" fill="{role_color}" text-anchor="middle" letter-spacing="0.8">{role_badge}</text>
  </g>

  <!-- ================= ATTACK 1 SECTION ================= -->
  <g transform="translate(0, 0)">
    {cost1_svg}
    <text x="{38 + move1_cost*20}" y="322" font-family="system-ui, -apple-system, sans-serif" font-weight="800" font-size="16" fill="#ffffff">{move1_name}</text>
    <text x="392" y="323" font-family="system-ui, -apple-system, sans-serif" font-weight="900" font-size="20" fill="#ffffff" text-anchor="end">{move1_dmg}</text>
    <text x="24" y="344" font-family="system-ui, -apple-system, sans-serif" font-weight="500" font-size="11.5" fill="#cbd5e1">{move1_desc[0]}</text>
    <text x="24" y="360" font-family="system-ui, -apple-system, sans-serif" font-weight="500" font-size="11.5" fill="#94a3b8">{move1_desc[1]}</text>
  </g>

  <!-- Separator Line -->
  <line x1="22" y1="378" x2="398" y2="378" stroke="#334155" stroke-width="1" stroke-dasharray="3 3"/>

  <!-- ================= ATTACK 2 SECTION ================= -->
  <g transform="translate(0, 0)">
    {cost2_svg}
    <text x="{38 + move2_cost*20}" y="410" font-family="system-ui, -apple-system, sans-serif" font-weight="800" font-size="16" fill="#ffffff">{move2_name}</text>
    <text x="392" y="411" font-family="system-ui, -apple-system, sans-serif" font-weight="900" font-size="20" fill="#ffffff" text-anchor="end">{move2_dmg}</text>
    <text x="24" y="432" font-family="system-ui, -apple-system, sans-serif" font-weight="500" font-size="11.5" fill="#cbd5e1">{move2_desc[0]}</text>
    <text x="24" y="448" font-family="system-ui, -apple-system, sans-serif" font-weight="500" font-size="11.5" fill="#94a3b8">{move2_desc[1]}</text>
  </g>

  <!-- ================= STATS STRIP ================= -->
  <g transform="translate(22, 468)">
    <rect width="376" height="20" rx="4" fill="#090d16" fill-opacity="0.8"/>
    <text x="12" y="14" font-family="system-ui, sans-serif" font-size="9.5" fill="#94a3b8">weakness <tspan font-weight="bold" fill="#f87171">⚡ ×2</tspan></text>
    <text x="145" y="14" font-family="system-ui, sans-serif" font-size="9.5" fill="#94a3b8">resistance <tspan font-weight="bold" fill="#38bdf8">🛡️ -30</tspan></text>
    <text x="290" y="14" font-family="system-ui, sans-serif" font-size="9.5" fill="#94a3b8">retreat <tspan font-weight="bold" fill="#ffffff">⚪ ⚪</tspan></text>
  </g>

  <!-- ================= POKEMON EX RULE BOX ================= -->
  <g transform="translate(22, 498)">
    <rect width="376" height="56" rx="8" fill="#0b1120" stroke="url(#holoBorder)" stroke-width="1.2"/>
    <rect x="8" y="7" width="115" height="16" rx="4" fill="#1e293b"/>
    <text x="65" y="19" font-family="system-ui, -apple-system, sans-serif" font-weight="800" font-size="9.5" fill="#38bdf8" text-anchor="middle">Pokémon ex rule</text>
    <text x="130" y="19" font-family="system-ui, -apple-system, sans-serif" font-weight="600" font-size="9.5" fill="#94a3b8">When this Dev enters the squad:</text>
    <text x="12" y="36" font-family="system-ui, -apple-system, sans-serif" font-size="10.5" fill="#e2e8f0">{rule_desc[0]}</text>
    <text x="12" y="49" font-family="system-ui, -apple-system, sans-serif" font-size="10.5" fill="#cbd5e1">{rule_desc[1]}</text>
  </g>

  <!-- ================= FOOTER INFO ================= -->
  <g transform="translate(22, 575)">
    <text x="0" y="0" font-family="system-ui, sans-serif" font-size="9.5" fill="#64748b">Illus. Egor FM</text>
    <text x="188" y="0" font-family="system-ui, sans-serif" font-size="9.5" font-weight="700" fill="#cbd5e1" text-anchor="middle">PROMO {card_number} ★★★</text>
    <text x="376" y="0" font-family="system-ui, sans-serif" font-size="9.5" fill="#64748b" text-anchor="end">© 2026 Python Data &amp; AI Lab</text>
  </g>
</svg>'''
    with open(filename, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated {filename}")

# Generate Header
with open(os.path.join(SCRATCH_DIR, "assets/header_banner.svg"), "w", encoding="utf-8") as f:
    f.write(create_header())
print("Generated header_banner.svg")

# Generate Card 1: Data Engineering (Rayquaza)
create_card(
    filename=os.path.join(CARDS_DIR, "card_rayquaza_de.svg"),
    stage_text="BASIC",
    pokemon_name="RAYQUAZA",
    hp_val="280",
    type_symbol="🐉",
    type_color="#10b981",
    bg_start="#042017",
    bg_end="#020e0a",
    b64_art=rayquaza_b64,
    role_badge="DATA ENGINEERING",
    role_color="#34d399",
    move1_cost=2,
    move1_name="ETL Overdrive",
    move1_dmg="130",
    move1_desc=[
        "Extracts and transforms streaming datasets at scale.",
        "Python • DuckDB • Polars • PostgreSQL • Asyncio."
    ],
    move2_cost=3,
    move2_name="Distributed Stream",
    move2_dmg="260",
    move2_desc=[
        "Orchestrates fault-tolerant Airflow pipelines & Kafka topics",
        "with zero downtime and sub-second ingestion latency."
    ],
    rule_desc=[
        "All data pipelines achieve 99.99% uptime and queries run",
        "with optimal memory footprint across distributed clusters."
    ],
    card_number="001/2026",
    accent_glow="#10b981"
)

# Generate Card 2: Data Analytics (Porygon-Z)
create_card(
    filename=os.path.join(CARDS_DIR, "card_porygonz_analytics.svg"),
    stage_text="STAGE 2",
    pokemon_name="PORYGON-Z",
    hp_val="260",
    type_symbol="💾",
    type_color="#06b6d4",
    bg_start="#041829",
    bg_end="#020d17",
    b64_art=porygonz_b64,
    role_badge="DATA ANALYTICS",
    role_color="#38bdf8",
    move1_cost=2,
    move1_name="Pattern Synthesis",
    move1_dmg="120",
    move1_desc=[
        "Performs exploratory data analysis (EDA) & hypothesis testing.",
        "Pandas • NumPy • Statistics • Statistical Modeling."
    ],
    move2_cost=3,
    move2_name="Metric Ray",
    move2_dmg="240",
    move2_desc=[
        "Converts multi-dimensional chaotic logs into clear business",
        "KPIs, cohort analysis, and executive decision dashboards."
    ],
    rule_desc=[
        "Complex data mysteries are solved instantly, exposing hidden",
        "trends, anomalies, and high-impact revenue opportunities."
    ],
    card_number="002/2026",
    accent_glow="#06b6d4"
)

# Generate Card 3: AI & Machine Learning (Mewtwo)
create_card(
    filename=os.path.join(CARDS_DIR, "card_mewtwo_ai.svg"),
    stage_text="BASIC",
    pokemon_name="MEWTWO",
    hp_val="310",
    type_symbol="🧠",
    type_color="#a855f7",
    bg_start="#1a0b2e",
    bg_end="#0b0314",
    b64_art=mewtwo_b64,
    role_badge="AI & MACHINE LEARNING",
    role_color="#c084fc",
    move1_cost=2,
    move1_name="Vector Embeddings",
    move1_dmg="140",
    move1_desc=[
        "Projects high-dimensional latent spaces for semantic RAG,",
        "deep neural search, and multi-modal vector indexing."
    ],
    move2_cost=3,
    move2_name="Neural Inference Blast",
    move2_dmg="290",
    move2_desc=[
        "Fine-tunes LLMs, transformers, and autonomous agent workflows",
        "deployed directly into low-latency production APIs."
    ],
    rule_desc=[
        "Autonomous agent workflows resolve tasks end-to-end and",
        "models generalize seamlessly with near-perfect accuracy."
    ],
    card_number="003/2026",
    accent_glow="#a855f7"
)
