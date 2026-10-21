import base64
import os
import html

SCRATCH_DIR = "/Users/egor/.gemini/antigravity/scratch/egorfm"
CARDS_DIR = os.path.join(SCRATCH_DIR, "assets/cards")
SPRITES_DIR = os.path.join(SCRATCH_DIR, "assets/sprites")

def get_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

rayquaza_b64 = get_b64(os.path.join(CARDS_DIR, "rayquaza.png"))
porygonz_b64 = get_b64(os.path.join(CARDS_DIR, "porygonz.png"))
mewtwo_b64 = get_b64(os.path.join(CARDS_DIR, "mewtwo.png"))

def xml_esc(s):
    if isinstance(s, list):
        return [xml_esc(item) for item in s]
    return html.escape(str(s))

# ==============================================================================
# 1. MINIMALIST HEADER BANNER SVG
# ==============================================================================
def create_header():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 140" width="920" height="140" fill="none">
  <defs>
    <linearGradient id="headerBorder" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#21262d"/>
      <stop offset="50%" stop-color="#30363d"/>
      <stop offset="100%" stop-color="#21262d"/>
    </linearGradient>
  </defs>

  <!-- Clean Dark Canvas -->
  <rect width="920" height="140" rx="14" fill="#0d1117"/>
  <rect x="1" y="1" width="918" height="138" rx="13" stroke="url(#headerBorder)" stroke-width="1.5"/>

  <!-- Centered Minimalist Typography -->
  <g transform="translate(460, 36)" text-anchor="middle">
    <!-- Subtitle / Role -->
    <text y="0" font-family="system-ui, -apple-system, sans-serif" font-weight="700" font-size="12" fill="#8b949e" letter-spacing="4">PYTHON DEVELOPER</text>
    
    <!-- Name -->
    <text y="36" font-family="system-ui, -apple-system, sans-serif" font-weight="900" font-size="34" fill="#f0f6fc" letter-spacing="1.5">EGOR</text>

    <!-- Domains Row -->
    <g transform="translate(0, 58)">
      <rect x="-240" y="0" width="150" height="24" rx="6" fill="#161b22" stroke="#30363d" stroke-width="1"/>
      <text x="-165" y="16" font-family="system-ui, -apple-system, sans-serif" font-weight="600" font-size="10.5" fill="#c9d1d9" letter-spacing="0.8">DATA ENGINEERING</text>

      <circle cx="-75" cy="12" r="2" fill="#484f58"/>

      <rect x="-60" y="0" width="120" height="24" rx="6" fill="#161b22" stroke="#30363d" stroke-width="1"/>
      <text x="0" y="16" font-family="system-ui, -apple-system, sans-serif" font-weight="600" font-size="10.5" fill="#c9d1d9" letter-spacing="0.8">DATA ANALYTICS</text>

      <circle cx="75" cy="12" r="2" fill="#484f58"/>

      <rect x="90" y="0" width="150" height="24" rx="6" fill="#161b22" stroke="#30363d" stroke-width="1"/>
      <text x="165" y="16" font-family="system-ui, -apple-system, sans-serif" font-weight="600" font-size="10.5" fill="#c9d1d9" letter-spacing="0.8">ARTIFICIAL INTEL</text>
    </g>
  </g>
</svg>'''

# ==============================================================================
# 2. MINIMALIST TITANIUM POKEMON TCG CARDS
# ==============================================================================
def create_card(
    filename,
    stage_text,
    pokemon_name,
    hp_val,
    type_symbol,
    b64_art,
    role_badge,
    move1_cost,
    move1_name,
    move1_dmg,
    move1_desc,
    move2_cost,
    move2_name,
    move2_dmg,
    move2_desc,
    rule_desc,
    card_number
):
    stage_text = xml_esc(stage_text)
    pokemon_name = xml_esc(pokemon_name)
    move1_name = xml_esc(move1_name)
    move1_desc = xml_esc(move1_desc)
    move2_name = xml_esc(move2_name)
    move2_desc = xml_esc(move2_desc)
    rule_desc = xml_esc(rule_desc)
    role_badge = xml_esc(role_badge)

    cost1_svg = "".join([f'<circle cx="{28 + i*18}" cy="316" r="7" fill="#21262d" stroke="#30363d" stroke-width="1.2"/>' for i in range(move1_cost)])
    cost2_svg = "".join([f'<circle cx="{28 + i*18}" cy="404" r="7" fill="#21262d" stroke="#30363d" stroke-width="1.2"/>' for i in range(move2_cost)])

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 600" width="420" height="600" fill="none">
  <defs>
    <!-- Titanium Minimalist Border -->
    <linearGradient id="cardBorder" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#30363d"/>
      <stop offset="50%" stop-color="#484f58"/>
      <stop offset="100%" stop-color="#21262d"/>
    </linearGradient>

    <!-- Subtle Vignette -->
    <radialGradient id="artVignette" cx="50%" cy="50%" r="55%">
      <stop offset="0%" stop-color="#1c2128"/>
      <stop offset="100%" stop-color="#0d1117"/>
    </radialGradient>
  </defs>

  <!-- Card Base (Dark Matte Charcoal) -->
  <rect x="2" y="2" width="416" height="596" rx="20" fill="url(#cardBorder)"/>
  <rect x="3.5" y="3.5" width="413" height="593" rx="18.5" fill="#0d1117"/>

  <!-- ================= HEADER BAR ================= -->
  <!-- Stage Pill -->
  <rect x="22" y="20" width="56" height="20" rx="4" fill="#161b22" stroke="#30363d" stroke-width="1"/>
  <text x="50" y="34" font-family="system-ui, -apple-system, sans-serif" font-weight="800" font-size="10" fill="#8b949e" text-anchor="middle" letter-spacing="0.5">{stage_text}</text>

  <!-- Pokemon Name -->
  <text x="88" y="36" font-family="system-ui, -apple-system, sans-serif" font-weight="900" font-size="18" fill="#f0f6fc" letter-spacing="0.5">{pokemon_name}</text>
  
  <!-- "ex" Badge -->
  <rect x="220" y="21" width="28" height="18" rx="4" fill="#21262d" stroke="#30363d" stroke-width="1"/>
  <text x="234" y="34" font-family="system-ui, -apple-system, sans-serif" font-weight="900" font-style="italic" font-size="11.5" fill="#f0f6fc" text-anchor="middle">ex</text>

  <!-- HP & Type Orb -->
  <text x="340" y="35" font-family="system-ui, -apple-system, sans-serif" font-weight="700" font-size="11.5" fill="#8b949e" text-anchor="end">HP</text>
  <text x="372" y="36" font-family="system-ui, -apple-system, sans-serif" font-weight="900" font-size="20" fill="#f0f6fc" text-anchor="end">{hp_val}</text>
  
  <!-- Type Energy Orb -->
  <circle cx="388" cy="30" r="10" fill="#161b22" stroke="#30363d" stroke-width="1.2"/>
  <text x="388" y="34" font-family="system-ui, sans-serif" font-size="11" text-anchor="middle">{type_symbol}</text>

  <!-- ================= ARTWORK WINDOW ================= -->
  <g transform="translate(18, 50)">
    <!-- Art Frame -->
    <rect width="384" height="236" rx="10" fill="url(#artVignette)" stroke="#30363d" stroke-width="1.2"/>
    
    <!-- Pokemon Artwork Image -->
    <image href="data:image/png;base64,{b64_art}" x="77" y="3" width="230" height="230" preserveAspectRatio="xMidYMid meet"/>

    <!-- Role Badge across bottom of art -->
    <rect x="12" y="204" width="160" height="22" rx="4" fill="#0d1117" stroke="#30363d" stroke-width="1"/>
    <text x="92" y="219" font-family="system-ui, -apple-system, sans-serif" font-weight="700" font-size="10" fill="#c9d1d9" text-anchor="middle" letter-spacing="0.8">{role_badge}</text>
  </g>

  <!-- ================= ATTACK 1 SECTION ================= -->
  <g transform="translate(0, 0)">
    {cost1_svg}
    <text x="{38 + move1_cost*18}" y="322" font-family="system-ui, -apple-system, sans-serif" font-weight="800" font-size="15" fill="#f0f6fc">{move1_name}</text>
    <text x="392" y="323" font-family="system-ui, -apple-system, sans-serif" font-weight="900" font-size="19" fill="#f0f6fc" text-anchor="end">{move1_dmg}</text>
    <text x="24" y="344" font-family="system-ui, -apple-system, sans-serif" font-weight="500" font-size="11" fill="#c9d1d9">{move1_desc[0]}</text>
    <text x="24" y="360" font-family="system-ui, -apple-system, sans-serif" font-weight="500" font-size="11" fill="#8b949e">{move1_desc[1]}</text>
  </g>

  <!-- Separator Line -->
  <line x1="22" y1="378" x2="398" y2="378" stroke="#21262d" stroke-width="1"/>

  <!-- ================= ATTACK 2 SECTION ================= -->
  <g transform="translate(0, 0)">
    {cost2_svg}
    <text x="{38 + move2_cost*18}" y="410" font-family="system-ui, -apple-system, sans-serif" font-weight="800" font-size="15" fill="#f0f6fc">{move2_name}</text>
    <text x="392" y="411" font-family="system-ui, -apple-system, sans-serif" font-weight="900" font-size="19" fill="#f0f6fc" text-anchor="end">{move2_dmg}</text>
    <text x="24" y="432" font-family="system-ui, -apple-system, sans-serif" font-weight="500" font-size="11" fill="#c9d1d9">{move2_desc[0]}</text>
    <text x="24" y="448" font-family="system-ui, -apple-system, sans-serif" font-weight="500" font-size="11" fill="#8b949e">{move2_desc[1]}</text>
  </g>

  <!-- ================= STATS STRIP ================= -->
  <g transform="translate(22, 468)">
    <rect width="376" height="20" rx="4" fill="#161b22"/>
    <text x="12" y="14" font-family="system-ui, sans-serif" font-size="9" fill="#8b949e">weakness <tspan font-weight="bold" fill="#f0f6fc">⚡ ×2</tspan></text>
    <text x="145" y="14" font-family="system-ui, sans-serif" font-size="9" fill="#8b949e">resistance <tspan font-weight="bold" fill="#f0f6fc">🛡️ -30</tspan></text>
    <text x="290" y="14" font-family="system-ui, sans-serif" font-size="9" fill="#8b949e">retreat <tspan font-weight="bold" fill="#f0f6fc">⚪ ⚪</tspan></text>
  </g>

  <!-- ================= POKEMON EX RULE BOX ================= -->
  <g transform="translate(22, 498)">
    <rect width="376" height="56" rx="6" fill="#161b22" stroke="#30363d" stroke-width="1"/>
    <rect x="8" y="7" width="115" height="16" rx="3" fill="#21262d"/>
    <text x="65" y="19" font-family="system-ui, -apple-system, sans-serif" font-weight="700" font-size="9" fill="#c9d1d9" text-anchor="middle">Pokémon ex rule</text>
    <text x="130" y="19" font-family="system-ui, -apple-system, sans-serif" font-weight="500" font-size="9" fill="#8b949e">When this Dev enters the squad:</text>
    <text x="12" y="36" font-family="system-ui, -apple-system, sans-serif" font-size="10.5" fill="#e6edf3">{rule_desc[0]}</text>
    <text x="12" y="49" font-family="system-ui, -apple-system, sans-serif" font-size="10.5" fill="#8b949e">{rule_desc[1]}</text>
  </g>

  <!-- ================= FOOTER INFO ================= -->
  <g transform="translate(22, 575)">
    <text x="0" y="0" font-family="system-ui, sans-serif" font-size="9" fill="#484f58">Illus. Egor</text>
    <text x="188" y="0" font-family="system-ui, sans-serif" font-size="9" font-weight="700" fill="#8b949e" text-anchor="middle">OBSIDIAN PROMO {card_number} ★★★</text>
    <text x="376" y="0" font-family="system-ui, sans-serif" font-size="9" fill="#484f58" text-anchor="end">© 2026 Data &amp; AI Lab</text>
  </g>
</svg>'''
    with open(filename, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated {filename}")

# Generate Minimalist Header
with open(os.path.join(SCRATCH_DIR, "assets/header_banner.svg"), "w", encoding="utf-8") as f:
    f.write(create_header())
print("Generated minimalist header_banner.svg")

# Generate Minimalist Card 1: Data Engineering (Rayquaza)
create_card(
    filename=os.path.join(CARDS_DIR, "card_rayquaza_de.svg"),
    stage_text="BASIC",
    pokemon_name="RAYQUAZA",
    hp_val="280",
    type_symbol="🐉",
    b64_art=rayquaza_b64,
    role_badge="DATA ENGINEERING",
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
    card_number="001/2026"
)

# Generate Minimalist Card 2: Data Analytics (Porygon-Z)
create_card(
    filename=os.path.join(CARDS_DIR, "card_porygonz_analytics.svg"),
    stage_text="STAGE 2",
    pokemon_name="PORYGON-Z",
    hp_val="260",
    type_symbol="💾",
    b64_art=porygonz_b64,
    role_badge="DATA ANALYTICS",
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
    card_number="002/2026"
)

# Generate Minimalist Card 3: AI & Machine Learning (Mewtwo)
create_card(
    filename=os.path.join(CARDS_DIR, "card_mewtwo_ai.svg"),
    stage_text="BASIC",
    pokemon_name="MEWTWO",
    hp_val="310",
    type_symbol="🧠",
    b64_art=mewtwo_b64,
    role_badge="AI & MACHINE LEARNING",
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
    card_number="003/2026"
)
