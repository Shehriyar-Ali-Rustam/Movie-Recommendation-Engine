"""
Movie Recommendation System
A content-based movie recommender using TF-IDF and cosine similarity.
"""

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from PIL import Image
import base64
import os
import sys

st.set_page_config(
    page_title="Cinematic — AI Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# MODERN 2026 UI — Glassmorphism, gradient mesh, micro-interactions
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">

<style>
/* ───── Design tokens ───── */
:root {
    --bg-0: #07060c;
    --bg-1: #0d0b18;
    --bg-2: #14111f;
    --surface: rgba(20, 17, 31, 0.55);
    --surface-hi: rgba(30, 26, 46, 0.72);
    --border: rgba(255, 255, 255, 0.08);
    --border-hi: rgba(255, 255, 255, 0.16);

    --text: #f5f3ff;
    --text-dim: #b9b4d0;
    --text-mute: #7d7895;

    --accent: #a78bfa;          /* violet-400 */
    --accent-2: #f472b6;         /* pink-400 */
    --accent-3: #38bdf8;         /* sky-400 */
    --accent-warm: #fbbf24;      /* amber-400 */

    --gradient-primary: linear-gradient(135deg, #a78bfa 0%, #f472b6 50%, #fb923c 100%);
    --gradient-cool: linear-gradient(135deg, #38bdf8 0%, #a78bfa 100%);
    --gradient-glass: linear-gradient(135deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02));

    --shadow-lg: 0 24px 60px -12px rgba(0, 0, 0, 0.6), 0 0 0 1px rgba(255, 255, 255, 0.04);
    --shadow-glow: 0 0 30px rgba(167, 139, 250, 0.25);

    --radius-sm: 10px;
    --radius: 16px;
    --radius-lg: 22px;
    --radius-xl: 28px;
}

/* ───── App canvas ───── */
.stApp {
    background:
        radial-gradient(1200px 700px at 80% -10%, rgba(244, 114, 182, 0.18), transparent 60%),
        radial-gradient(900px 600px at -10% 20%, rgba(56, 189, 248, 0.16), transparent 55%),
        radial-gradient(800px 500px at 50% 110%, rgba(167, 139, 250, 0.22), transparent 60%),
        var(--bg-0) !important;
    color: var(--text) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* Animated noise/grain overlay for filmic texture */
.stApp::before {
    content: "";
    position: fixed; inset: 0;
    pointer-events: none;
    background-image: url("data:image/svg+xml;utf8,<svg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='3'/></filter><rect width='100%25' height='100%25' filter='url(%23n)' opacity='0.5'/></svg>");
    opacity: 0.035;
    z-index: 0;
    mix-blend-mode: overlay;
}

/* Main content above grain */
.block-container { position: relative; z-index: 1; padding-top: 2rem !important; max-width: 1280px !important;}

/* ───── Typography ───── */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Space Grotesk', 'Inter', sans-serif !important;
    color: var(--text) !important;
    letter-spacing: -0.02em !important;
    font-weight: 700 !important;
}

p, label, span, div, .stMarkdown {
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden !important; }

/* ───── Hero ───── */
.hero {
    position: relative;
    text-align: center;
    padding: 3.5rem 1.5rem 2.5rem;
    margin-bottom: 1.5rem;
    border-radius: var(--radius-xl);
    background: var(--gradient-glass);
    border: 1px solid var(--border);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    overflow: hidden;
}
.hero::before {
    content: "";
    position: absolute; inset: -2px;
    background: conic-gradient(from 180deg at 50% 50%, rgba(167,139,250,0.0), rgba(244,114,182,0.3), rgba(56,189,248,0.0), rgba(167,139,250,0.4), rgba(167,139,250,0.0));
    filter: blur(40px);
    opacity: 0.5;
    z-index: -1;
    animation: rotate 18s linear infinite;
}
@keyframes rotate { to { transform: rotate(360deg); } }

.hero-eyebrow {
    display: inline-flex; align-items: center; gap: 8px;
    padding: 6px 14px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid var(--border-hi);
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-dim) !important;
    margin-bottom: 1.25rem;
    backdrop-filter: blur(10px);
}
.hero-eyebrow .dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: #34d399;
    box-shadow: 0 0 8px #34d399;
    animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }

.hero h1 {
    font-size: clamp(2.5rem, 6vw, 4.5rem) !important;
    line-height: 1.05 !important;
    margin: 0 0 0.75rem 0 !important;
    font-weight: 800 !important;
}
.hero h1 .grad {
    background: var(--gradient-primary);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    display: inline-block;
}
.hero p.lede {
    font-size: clamp(1rem, 1.5vw, 1.2rem);
    color: var(--text-dim) !important;
    max-width: 640px;
    margin: 0 auto !important;
    line-height: 1.6;
}

/* ───── Section headings ───── */
.section-title {
    display: flex; align-items: center; gap: 12px;
    font-size: 1.35rem !important;
    font-weight: 700 !important;
    margin: 2.25rem 0 1rem 0 !important;
}
.section-title .bar {
    width: 4px; height: 22px;
    background: var(--gradient-primary);
    border-radius: 2px;
}
.section-title .count {
    margin-left: auto;
    font-size: 0.75rem;
    font-weight: 500;
    color: var(--text-mute) !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* ───── Glass card primitive ───── */
.glass {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    backdrop-filter: blur(20px) saturate(160%);
    -webkit-backdrop-filter: blur(20px) saturate(160%);
    transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}
.glass:hover {
    background: var(--surface-hi);
    border-color: var(--border-hi);
    transform: translateY(-2px);
}

/* ───── Movie poster cards (Top Rated) ───── */
.poster {
    position: relative;
    width: 100%;
    aspect-ratio: 2 / 3;
    border-radius: var(--radius-lg);
    overflow: hidden;
    cursor: pointer;
    isolation: isolate;
    transform-style: preserve-3d;
    perspective: 1000px;
    transition: transform 0.5s cubic-bezier(0.16, 1, 0.3, 1),
                box-shadow 0.5s cubic-bezier(0.16, 1, 0.3, 1);
    box-shadow:
        0 12px 40px -12px rgba(0, 0, 0, 0.7),
        0 0 0 1px rgba(255, 255, 255, 0.05) inset;
    margin-bottom: 1rem;
    animation: posterIn 0.7s cubic-bezier(0.16, 1, 0.3, 1) backwards;
}
@keyframes posterIn {
    from { opacity: 0; transform: translateY(20px) scale(0.96); }
    to   { opacity: 1; transform: translateY(0) scale(1); }
}

/* Color-tinted gradient base — title hash decides the palette */
.poster-bg {
    position: absolute; inset: 0;
    background: var(--p1, linear-gradient(135deg, #6366f1, #ec4899));
    z-index: 0;
}
/* Layered gradient mesh on top of base for richness */
.poster-bg::before {
    content: "";
    position: absolute; inset: 0;
    background:
        radial-gradient(circle at 20% 10%, rgba(255,255,255,0.35), transparent 45%),
        radial-gradient(circle at 80% 90%, rgba(0,0,0,0.4), transparent 50%);
    mix-blend-mode: overlay;
}
/* Film grain on top of gradient */
.poster-bg::after {
    content: "";
    position: absolute; inset: 0;
    background-image: url("data:image/svg+xml;utf8,<svg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/></filter><rect width='100%25' height='100%25' filter='url(%23n)' opacity='0.65'/></svg>");
    opacity: 0.18;
    mix-blend-mode: overlay;
}

/* Dark vignette so text reads cleanly */
.poster-vignette {
    position: absolute; inset: 0;
    background:
        linear-gradient(180deg, rgba(0,0,0,0.0) 35%, rgba(0,0,0,0.45) 70%, rgba(0,0,0,0.85) 100%),
        radial-gradient(ellipse at center, transparent 40%, rgba(0,0,0,0.45) 100%);
    z-index: 1;
}

/* Giant rank watermark — the visual hero */
.poster-rank {
    position: absolute;
    bottom: -22px;
    left: -10px;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 800;
    font-size: 11rem;
    line-height: 0.85;
    letter-spacing: -0.06em;
    color: rgba(255, 255, 255, 0.96);
    -webkit-text-stroke: 2px rgba(255, 255, 255, 0.6);
    text-shadow: 0 6px 30px rgba(0, 0, 0, 0.5);
    z-index: 2;
    pointer-events: none;
    transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}
.poster:hover .poster-rank {
    transform: translate(4px, -4px) scale(1.02);
}

/* Top-right floating rating */
.poster-rating {
    position: absolute;
    top: 12px;
    right: 12px;
    display: inline-flex; align-items: center; gap: 5px;
    padding: 6px 12px;
    background: rgba(0, 0, 0, 0.55);
    border: 1px solid rgba(251, 191, 36, 0.45);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border-radius: 999px;
    color: #fbbf24;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700;
    font-size: 0.85rem;
    z-index: 3;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.4);
}
.poster-rating .star { color: #fbbf24; filter: drop-shadow(0 0 4px rgba(251,191,36,0.6)); }

/* Top-left small genre eyebrow */
.poster-genre {
    position: absolute;
    top: 14px;
    left: 14px;
    padding: 4px 10px;
    background: rgba(0, 0, 0, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.18);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border-radius: 999px;
    color: rgba(255, 255, 255, 0.92) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    z-index: 3;
    max-width: calc(100% - 80px);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* Title block sitting at the bottom */
.poster-info {
    position: absolute;
    left: 0; right: 0; bottom: 0;
    padding: 1rem 1.1rem 1.05rem;
    z-index: 3;
    transform: translateY(0);
    transition: transform 0.45s cubic-bezier(0.16, 1, 0.3, 1);
}
.poster-info .title {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700;
    font-size: 1.1rem;
    color: white !important;
    line-height: 1.15;
    margin: 0 0 4px 0;
    text-shadow: 0 2px 12px rgba(0,0,0,0.6);
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.poster-info .meta {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem;
    color: rgba(255, 255, 255, 0.8) !important;
    letter-spacing: 0.06em;
    display: flex;
    align-items: center;
    gap: 8px;
}
.poster-info .meta .dot {
    width: 3px; height: 3px;
    background: rgba(255, 255, 255, 0.55);
    border-radius: 50%;
}

/* Hover overlay: reveals director + nudges info up */
.poster-overlay {
    position: absolute;
    inset: 0;
    z-index: 4;
    padding: 1.1rem;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    background: linear-gradient(180deg, rgba(0,0,0,0.1) 0%, rgba(10,8,16,0.92) 100%);
    opacity: 0;
    transition: opacity 0.45s cubic-bezier(0.16, 1, 0.3, 1);
    pointer-events: none;
}
.poster-overlay .director {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.82rem;
    color: rgba(255, 255, 255, 0.85) !important;
    margin-top: 4px;
    line-height: 1.4;
}
.poster-overlay .director .lbl {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.62rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.5) !important;
    display: block;
    margin-bottom: 2px;
}
.poster-overlay .play-btn {
    align-self: flex-start;
    margin-bottom: auto;
    margin-top: 0;
    padding: 8px 16px;
    background: rgba(255,255,255,0.92);
    color: #07060c !important;
    border-radius: 999px;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600;
    font-size: 0.8rem;
    box-shadow: 0 8px 24px rgba(0,0,0,0.4);
    display: inline-flex; align-items: center; gap: 6px;
}

/* Hover state — Netflix-style scale + lift + reveal */
.poster:hover {
    transform: translateY(-8px) scale(1.025);
    box-shadow:
        0 32px 70px -16px rgba(0, 0, 0, 0.85),
        0 0 0 1px rgba(167, 139, 250, 0.35) inset,
        0 0 50px -10px rgba(167, 139, 250, 0.5);
}
.poster:hover .poster-overlay { opacity: 1; }
.poster:hover .poster-info { transform: translateY(-4px); }

/* Top-3 medal accent */
.poster.top1 { box-shadow: 0 12px 40px -12px rgba(251,191,36,0.5), 0 0 0 1px rgba(251,191,36,0.35) inset; }
.poster.top2 { box-shadow: 0 12px 40px -12px rgba(209,213,219,0.4), 0 0 0 1px rgba(209,213,219,0.28) inset; }
.poster.top3 { box-shadow: 0 12px 40px -12px rgba(217,119,6,0.4),  0 0 0 1px rgba(217,119,6,0.28)  inset; }

/* ───── Recommendation cards ───── */
.rec-card {
    position: relative;
    padding: 1.4rem 1.5rem;
    margin: 0.7rem 0;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    backdrop-filter: blur(20px) saturate(160%);
    -webkit-backdrop-filter: blur(20px) saturate(160%);
    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    overflow: hidden;
    animation: slideUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) backwards;
}
@keyframes slideUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}
.rec-card::before {
    content: "";
    position: absolute; inset: 0;
    background: linear-gradient(120deg, rgba(167,139,250,0.0) 0%, rgba(167,139,250,0.06) 50%, rgba(244,114,182,0.0) 100%);
    opacity: 0;
    transition: opacity 0.4s;
    pointer-events: none;
}
.rec-card:hover {
    transform: translateX(4px);
    border-color: rgba(167, 139, 250, 0.4);
    box-shadow: var(--shadow-lg), var(--shadow-glow);
}
.rec-card:hover::before { opacity: 1; }

.rec-card .rec-title {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.25rem !important;
    font-weight: 700;
    color: var(--text) !important;
    margin-bottom: 0.5rem;
    letter-spacing: -0.01em;
}
.rec-card .rec-title .year {
    color: var(--text-mute) !important;
    font-weight: 500;
    font-size: 1rem;
}
.rec-card .rec-meta {
    display: flex; flex-wrap: wrap; gap: 8px;
    margin-top: 0.6rem;
}
.chip {
    display: inline-flex; align-items: center; gap: 5px;
    padding: 3px 11px;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 500;
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid var(--border);
    color: var(--text-dim) !important;
}
.chip.genre { background: rgba(167, 139, 250, 0.12); border-color: rgba(167, 139, 250, 0.28); color: #c4b5fd !important; }
.chip.rating { background: rgba(251, 191, 36, 0.12); border-color: rgba(251, 191, 36, 0.3); color: #fbbf24 !important; }
.chip.director { background: rgba(56, 189, 248, 0.1); border-color: rgba(56, 189, 248, 0.28); color: #7dd3fc !important; }
.chip.match { background: linear-gradient(135deg, rgba(244,114,182,0.15), rgba(167,139,250,0.15)); border-color: rgba(244, 114, 182, 0.35); color: #f9a8d4 !important; font-weight: 600; }

/* Score ring on the right */
.rec-row { display: flex; align-items: center; justify-content: space-between; gap: 1rem; }
.score-pill {
    flex-shrink: 0;
    display: inline-flex; align-items: baseline; gap: 4px;
    padding: 8px 14px;
    border-radius: var(--radius-sm);
    background: var(--gradient-primary);
    color: white !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 700;
    font-size: 0.95rem;
    box-shadow: 0 6px 20px rgba(167, 139, 250, 0.35);
}
.score-pill .pct { font-size: 0.7rem; opacity: 0.85; }

/* ───── Streamlit widget overrides ───── */
/* Selectbox */
div[data-baseweb="select"] > div {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    backdrop-filter: blur(20px) !important;
    color: var(--text) !important;
    transition: all 0.25s ease !important;
    min-height: 48px !important;
}
div[data-baseweb="select"] > div:hover {
    border-color: rgba(167, 139, 250, 0.5) !important;
}
div[data-baseweb="select"] > div:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(167, 139, 250, 0.15) !important;
}
div[data-baseweb="popover"] {
    background: var(--bg-2) !important;
    border: 1px solid var(--border-hi) !important;
    border-radius: var(--radius) !important;
    box-shadow: var(--shadow-lg) !important;
}
ul[role="listbox"] li:hover { background: rgba(167, 139, 250, 0.12) !important; }

/* Text input */
.stTextInput input {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text) !important;
    padding: 0.75rem 1rem !important;
    font-family: 'Inter', sans-serif !important;
    backdrop-filter: blur(20px);
    transition: all 0.25s ease !important;
    min-height: 48px !important;
}
.stTextInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(167, 139, 250, 0.15) !important;
}
.stTextInput input::placeholder { color: var(--text-mute) !important; }

/* Sliders */
.stSlider [data-baseweb="slider"] > div > div { background: var(--gradient-primary) !important; }
.stSlider [role="slider"] {
    background: white !important;
    border: 2px solid var(--accent) !important;
    box-shadow: 0 4px 12px rgba(167, 139, 250, 0.4) !important;
}

/* Buttons */
.stButton > button {
    background: var(--gradient-primary) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 0.85rem 1.5rem !important;
    letter-spacing: -0.01em !important;
    box-shadow: 0 10px 30px -8px rgba(167, 139, 250, 0.5), 0 0 0 1px rgba(255, 255, 255, 0.08) inset !important;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
    position: relative !important;
    overflow: hidden !important;
}
.stButton > button::before {
    content: ""; position: absolute; inset: 0;
    background: linear-gradient(120deg, transparent 30%, rgba(255,255,255,0.25) 50%, transparent 70%);
    transform: translateX(-100%);
    transition: transform 0.6s;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 16px 40px -8px rgba(167, 139, 250, 0.6), 0 0 0 1px rgba(255, 255, 255, 0.12) inset !important;
}
.stButton > button:hover::before { transform: translateX(100%); }
.stButton > button:active { transform: translateY(0); }

/* DataFrame */
.stDataFrame {
    border-radius: var(--radius) !important;
    overflow: hidden !important;
    border: 1px solid var(--border) !important;
    background: var(--surface) !important;
    backdrop-filter: blur(20px);
}
.stDataFrame [data-testid="stTable"] { background: transparent !important; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(13, 11, 24, 0.92), rgba(7, 6, 12, 0.92)) !important;
    border-right: 1px solid var(--border) !important;
    backdrop-filter: blur(30px) !important;
}
section[data-testid="stSidebar"] .block-container { padding-top: 1.5rem !important; }
section[data-testid="stSidebar"] h3, section[data-testid="stSidebar"] h4 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
}
section[data-testid="stSidebar"] hr {
    border-color: var(--border) !important;
    margin: 1.25rem 0 !important;
}

/* Sidebar metric chips */
.metric-chip {
    display: flex; justify-content: space-between; align-items: center;
    padding: 12px 14px;
    margin-bottom: 8px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    backdrop-filter: blur(10px);
    transition: all 0.25s ease;
}
.metric-chip:hover { border-color: var(--border-hi); }
.metric-chip .label {
    font-size: 0.78rem;
    color: var(--text-mute) !important;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    font-weight: 500;
}
.metric-chip .value {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.1rem;
    font-weight: 700;
    background: var(--gradient-primary);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Alerts */
div[data-baseweb="notification"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    backdrop-filter: blur(20px) !important;
}

/* Footer */
.app-footer {
    margin-top: 4rem;
    padding: 2rem;
    text-align: center;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-xl);
    backdrop-filter: blur(20px);
}
.app-footer .brand {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.15rem;
    font-weight: 700;
    background: var(--gradient-primary);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.4rem;
}
.app-footer .stack {
    display: inline-flex; flex-wrap: wrap; gap: 6px; justify-content: center;
    margin-top: 0.6rem;
}
.app-footer .tag {
    padding: 3px 10px;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid var(--border);
    border-radius: 999px;
    font-size: 0.72rem;
    color: var(--text-mute) !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* Subhead under selects */
.field-label {
    display: block;
    font-size: 0.8rem;
    font-weight: 500;
    color: var(--text-dim) !important;
    margin-bottom: 0.45rem;
    letter-spacing: 0.02em;
}

/* Recommend result intro */
.result-intro {
    margin: 1.5rem 0 0.5rem;
    padding: 1.1rem 1.25rem;
    background: var(--gradient-glass);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    backdrop-filter: blur(20px);
}
.result-intro .lbl {
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-mute) !important;
    font-weight: 500;
}
.result-intro .seed {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.4rem;
    font-weight: 700;
    background: var(--gradient-primary);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-top: 4px;
}

/* Scrollbar */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: var(--bg-0); }
::-webkit-scrollbar-thumb { background: rgba(167, 139, 250, 0.3); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: rgba(167, 139, 250, 0.5); }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_movies(csv_path="movies.csv"):
    """Load and preprocess the movie dataset."""
    if not os.path.exists(csv_path):
        st.error(f"Movie dataset not found at: {csv_path}")
        st.info("Please ensure 'movies.csv' is in the same directory as this script.")
        sys.exit(1)

    try:
        movies_df = pd.read_csv(csv_path)
        required_columns = ['title', 'description']
        if not all(col in movies_df.columns for col in required_columns):
            st.error(f"CSV file must contain columns: {required_columns}")
            sys.exit(1)

        movies_df['genres'] = movies_df['description'].str.split(',').apply(lambda x: [g.strip() for g in x])
        unique_genres_list = sorted({g for gl in movies_df['genres'] for g in gl})
        return movies_df, unique_genres_list
    except Exception as e:
        st.error(f"Error loading movie data: {str(e)}")
        sys.exit(1)


@st.cache_data
def compute_similarity_matrix(movies_df):
    """Pre-compute the TF-IDF similarity matrix for better performance."""
    tfidf = TfidfVectorizer(ngram_range=(1, 2), min_df=1, stop_words='english')
    tfidf_matrix = tfidf.fit_transform(movies_df['description'])
    similarity_matrix = cosine_similarity(tfidf_matrix)
    return similarity_matrix, tfidf


@st.cache_data
def get_hybrid_recommendations(movie_title, movies_df, similarity_matrix, top_n=5,
                               rating_weight=0.3, year_weight=0.1, genre_weight=0.6):
    """Get movie recommendations using hybrid approach (genre + rating + recency)."""
    try:
        idx = movies_df[movies_df['title'] == movie_title].index[0]
        genre_sim = similarity_matrix[idx]
        rating_sim = np.zeros(len(movies_df))
        year_sim = np.zeros(len(movies_df))

        if 'rating' in movies_df.columns and pd.notna(movies_df.iloc[idx]['rating']):
            selected_rating = movies_df.iloc[idx]['rating']
            ratings = movies_df['rating'].fillna(movies_df['rating'].mean())
            rating_diff = np.abs(ratings - selected_rating)
            rating_sim = 1 - (rating_diff / 10.0)

        if 'year' in movies_df.columns and pd.notna(movies_df.iloc[idx]['year']):
            selected_year = movies_df.iloc[idx]['year']
            years = movies_df['year'].fillna(movies_df['year'].median())
            year_diff = np.abs(years - selected_year)
            year_sim = 1 - (year_diff / 100.0)
            year_sim = np.clip(year_sim, 0, 1)

        combined_sim = (
            genre_weight * genre_sim +
            rating_weight * rating_sim +
            year_weight * year_sim
        )

        sim_scores = list(enumerate(combined_sim))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_idx = [i for i, score in sim_scores if i != idx][:top_n]
        sim_values = [score for i, score in sim_scores if i != idx][:top_n]

        result = movies_df.iloc[sim_idx].copy()
        result['similarity_score'] = [round(score * 100, 1) for score in sim_values]
        return result
    except IndexError:
        raise ValueError(f"Movie '{movie_title}' not found in database")


# ─────────────────────────────────────────────────────────────────────────────
# Load data
# ─────────────────────────────────────────────────────────────────────────────
movies, unique_genres = load_movies()
similarity_matrix, tfidf_vectorizer = compute_similarity_matrix(movies)

# ─────────────────────────────────────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero">
        <span class="hero-eyebrow"><span class="dot"></span> AI-Powered · TF-IDF + Hybrid Scoring</span>
        <h1>Discover your next<br/><span class="grad">favorite film.</span></h1>
        <p class="lede">An intelligent recommender that blends genre, rating, and era —
        crafted with modern machine learning to surface films you'll actually love.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙ Tuning")
    st.markdown('<span class="field-label">Adjust how the engine weighs each signal.</span>', unsafe_allow_html=True)

    genre_weight = st.slider("Genre match", 0.0, 1.0, 0.6, 0.1)
    rating_weight = st.slider("Rating similarity", 0.0, 1.0, 0.3, 0.1)
    year_weight = st.slider("Release era", 0.0, 1.0, 0.1, 0.1)
    num_recommendations = st.slider("Results", 3, 20, 5)

    st.markdown("---")
    st.markdown("### Library")

    year_range = ""
    if 'year' in movies.columns:
        year_range = f"{int(movies['year'].min())}–{int(movies['year'].max())}"

    st.markdown(
        f"""
        <div class="metric-chip"><span class="label">Movies</span><span class="value">{len(movies)}</span></div>
        <div class="metric-chip"><span class="label">Genres</span><span class="value">{len(unique_genres)}</span></div>
        {f'<div class="metric-chip"><span class="label">Era</span><span class="value">{year_range}</span></div>' if year_range else ''}
        """,
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────────────────────────────────────
# TOP RATED
# ─────────────────────────────────────────────────────────────────────────────
if 'rating' in movies.columns:
    st.markdown(
        '<div class="section-title"><span class="bar"></span>Top rated<span class="count">TOP 10</span></div>',
        unsafe_allow_html=True,
    )

    # Curated palette pairs — each title deterministically maps to one
    POSTER_PALETTES = [
        ("#6366f1", "#ec4899"),  # indigo → pink
        ("#0ea5e9", "#8b5cf6"),  # sky → violet
        ("#f43f5e", "#fb923c"),  # rose → orange
        ("#10b981", "#0ea5e9"),  # emerald → sky
        ("#a855f7", "#06b6d4"),  # purple → cyan
        ("#ef4444", "#7c3aed"),  # red → violet
        ("#f59e0b", "#dc2626"),  # amber → red
        ("#14b8a6", "#6366f1"),  # teal → indigo
        ("#db2777", "#7c3aed"),  # pink → violet
        ("#0891b2", "#f43f5e"),  # cyan → rose
        ("#84cc16", "#0ea5e9"),  # lime → sky
        ("#9333ea", "#f59e0b"),  # purple → amber
    ]

    def palette_for(title):
        """Deterministic palette per title — same movie always gets same look."""
        h = sum(ord(c) for c in title) if title else 0
        return POSTER_PALETTES[h % len(POSTER_PALETTES)]

    top_cols = ['title', 'rating']
    for opt in ('year', 'director', 'description'):
        if opt in movies.columns:
            top_cols.append(opt)

    top_rated = movies.nlargest(10, 'rating')[top_cols].reset_index(drop=True)

    poster_cols = st.columns(5, gap="small")

    for i, (_, m) in enumerate(top_rated.iterrows()):
        with poster_cols[i % 5]:
            c1, c2 = palette_for(m['title'])
            year_str = f"{int(m['year'])}" if 'year' in m and pd.notna(m['year']) else "—"
            director_str = m['director'] if 'director' in m and pd.notna(m.get('director')) else "Unknown"
            primary_genre = "Film"
            if 'description' in m and pd.notna(m.get('description')):
                primary_genre = str(m['description']).split(',')[0].strip().upper()

            tier_class = ""
            if i == 0: tier_class = "top1"
            elif i == 1: tier_class = "top2"
            elif i == 2: tier_class = "top3"

            st.markdown(
                f"""
                <div class="poster {tier_class}" style="animation-delay: {i * 0.05}s;">
                    <div class="poster-bg" style="--p1: linear-gradient(135deg, {c1} 0%, {c2} 100%);"></div>
                    <div class="poster-vignette"></div>
                    <div class="poster-rank">{i+1}</div>
                    <div class="poster-genre">{primary_genre}</div>
                    <div class="poster-rating"><span class="star">★</span> {m['rating']}</div>
                    <div class="poster-overlay">
                        <div class="play-btn">▶ View</div>
                        <div class="director">
                            <span class="lbl">Directed by</span>
                            {director_str}
                        </div>
                    </div>
                    <div class="poster-info">
                        <div class="title">{m['title']}</div>
                        <div class="meta">
                            <span>{year_str}</span>
                            <span class="dot"></span>
                            <span>#{i+1:02d} OF 10</span>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

# ─────────────────────────────────────────────────────────────────────────────
# SEARCH + GENRE
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="section-title"><span class="bar"></span>Explore the library</div>',
    unsafe_allow_html=True,
)

search_col, genre_col = st.columns([2, 1], gap="medium")

with search_col:
    st.markdown('<span class="field-label">Search</span>', unsafe_allow_html=True)
    search_term = st.text_input(
        "Search",
        "",
        placeholder="Search by title or director…",
        label_visibility="collapsed",
        key="search_input",
    )

with genre_col:
    st.markdown('<span class="field-label">Filter by genre</span>', unsafe_allow_html=True)
    genre = st.selectbox(
        "Genre",
        ["All"] + unique_genres,
        label_visibility="collapsed",
    )

if search_term:
    filtered_by_search = movies[
        movies['title'].str.contains(search_term, case=False, na=False) |
        (movies['director'].str.contains(search_term, case=False, na=False) if 'director' in movies.columns else False)
    ]
else:
    filtered_by_search = movies

filtered = filtered_by_search.copy()
if genre != "All":
    filtered = filtered[filtered['genres'].apply(lambda gs: genre in gs)]

# Status line
status_parts = []
if search_term:
    status_parts.append(f'matching <strong style="color:var(--accent)">"{search_term}"</strong>')
if genre != "All":
    status_parts.append(f'in <strong style="color:var(--accent)">{genre}</strong>')
status_text = " ".join(status_parts) if status_parts else "in the catalog"
st.markdown(
    f"""<div style="color: var(--text-mute); font-size: 0.85rem; margin: 0.5rem 0 1rem; font-family: 'JetBrains Mono', monospace;">
    → {len(filtered)} {'movie' if len(filtered) == 1 else 'movies'} {status_text}
    </div>""",
    unsafe_allow_html=True,
)

if not filtered.empty:
    display_cols = ['title', 'description']
    rename_dict = {'title': 'Title', 'description': 'Genres'}
    if 'year' in filtered.columns:
        display_cols.append('year'); rename_dict['year'] = 'Year'
    if 'rating' in filtered.columns:
        display_cols.append('rating'); rename_dict['rating'] = 'Rating'
    if 'director' in filtered.columns:
        display_cols.append('director'); rename_dict['director'] = 'Director'

    st.dataframe(
        filtered[display_cols].rename(columns=rename_dict),
        height=320,
        use_container_width=True,
        hide_index=True,
    )
else:
    st.warning("No movies match your filters. Try a broader search.")

# ─────────────────────────────────────────────────────────────────────────────
# RECOMMENDATIONS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="section-title"><span class="bar"></span>Personalized for you</div>',
    unsafe_allow_html=True,
)

pick_col, btn_col = st.columns([3, 1], gap="medium")

with pick_col:
    st.markdown('<span class="field-label">Pick a movie you love</span>', unsafe_allow_html=True)
    movie = st.selectbox(
        "Movie",
        filtered['title'].tolist() if not filtered.empty else [],
        index=0 if filtered.empty else None,
        label_visibility="collapsed",
        placeholder="Select a film…",
    )

with btn_col:
    st.markdown('<span class="field-label">&nbsp;</span>', unsafe_allow_html=True)
    get_recs = st.button("Get recommendations →", key="recommend_btn", use_container_width=True)

if get_recs:
    if movie:
        try:
            with st.spinner(""):
                recommendations = get_hybrid_recommendations(
                    movie, movies, similarity_matrix,
                    top_n=num_recommendations,
                    rating_weight=rating_weight,
                    year_weight=year_weight,
                    genre_weight=genre_weight,
                )

            st.markdown(
                f"""
                <div class="result-intro">
                    <div class="lbl">Because you liked</div>
                    <div class="seed">{movie}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            for offset, (_, row) in enumerate(recommendations.iterrows()):
                year_html = f' <span class="year">({int(row["year"])})</span>' if 'year' in row and pd.notna(row['year']) else ''

                chips = []
                if pd.notna(row.get('description')):
                    for g in [g.strip() for g in str(row['description']).split(',')][:4]:
                        chips.append(f'<span class="chip genre">{g}</span>')
                if 'rating' in row and pd.notna(row['rating']):
                    chips.append(f'<span class="chip rating">★ {row["rating"]}</span>')
                if 'director' in row and pd.notna(row['director']):
                    chips.append(f'<span class="chip director">🎬 {row["director"]}</span>')

                score_html = ""
                if 'similarity_score' in row:
                    score_html = f'<div class="score-pill">{row["similarity_score"]}<span class="pct">%</span></div>'

                st.markdown(
                    f"""
                    <div class="rec-card" style="animation-delay: {offset * 0.06}s;">
                        <div class="rec-row">
                            <div style="flex:1; min-width:0;">
                                <div class="rec-title">{row['title']}{year_html}</div>
                                <div class="rec-meta">{''.join(chips)}</div>
                            </div>
                            {score_html}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        except ValueError as e:
            st.error(f"Error: {str(e)}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
    else:
        st.warning("Please select a movie first.")

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    f"""
    <div class="app-footer">
        <div class="brand">CINEMATIC · AI MOVIE RECOMMENDER</div>
        <div style="color: var(--text-dim); font-size: 0.88rem;">
            Hybrid content-based filtering · TF-IDF with bigrams · Cosine similarity
        </div>
        <div class="stack">
            <span class="tag">{len(movies)} movies</span>
            <span class="tag">{len(unique_genres)} genres</span>
            <span class="tag">scikit-learn</span>
            <span class="tag">streamlit</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
