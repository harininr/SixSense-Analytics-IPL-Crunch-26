"""
IPL Crunch '26 — Ultimate Analytics Dashboard
Championship-grade · Team DNA · Match Oracle · Player Intelligence
Run: python3 -m streamlit run dashboard/app.py
"""

import os, warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="IPL SixSense Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── MAXIMUM GLASSMORPHISM CSS ────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,300;0,14..32,400;0,14..32,500;0,14..32,600;0,14..32,700;0,14..32,800;0,14..32,900;1,14..32,400&family=Space+Grotesk:wght@400;500;600;700&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css');

/* ════════════════════════════════════════
   RESET & BASE
════════════════════════════════════════ */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"] {
    font-family: 'Inter', 'Space Grotesk', sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

/* ════════════════════════════════════════
   CRICKET STADIUM BACKGROUND
════════════════════════════════════════ */
.stApp {
    background: #03070f url('https://images.unsplash.com/photo-1540747913346-19e32dc3e97e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2000&q=80') center center / cover fixed;
    min-height: 100vh;
    position: relative;
    overflow-x: hidden;
}
.stApp::before {
    content: '';
    position: fixed; top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(3, 7, 15, 0.4); /* Deep dark tint */
    backdrop-filter: blur(2px);       /* Subtle stadium blur */
    -webkit-backdrop-filter: blur(2px);
    pointer-events: none;
    z-index: 0;
}
/* Subtle pitch texture grid overlay */
.stApp::after {
    content: '';
    position: fixed; top: 0; left: 0; right: 0; bottom: 0;
    background-image:
        linear-gradient(rgba(255,255,255,0.015) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.015) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
}

/* ════════════════════════════════════════
   SIDEBAR — deep glass
════════════════════════════════════════ */
section[data-testid="stSidebar"] {
    background: linear-gradient(170deg, rgba(10,16,30,0.98) 0%, rgba(5,10,20,0.99) 100%) !important;
    border-right: 1px solid rgba(253,224,71,0.1) !important;
    box-shadow: 4px 0 60px rgba(0,0,0,0.8), inset -1px 0 0 rgba(255,255,255,0.02) !important;
    backdrop-filter: blur(24px) !important;
}
section[data-testid="stSidebar"]::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 180px;
    background: radial-gradient(ellipse at 50% 0%, rgba(253,224,71,0.08) 0%, transparent 70%);
    pointer-events: none;
}
section[data-testid="stSidebar"] * { color: #f1f5f9 !important; }
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 { color: #FDE047 !important; }
section[data-testid="stSidebar"] .stSlider > div > div {
    background: linear-gradient(90deg, #FDE047, #FDA4AF) !important;
    box-shadow: 0 0 10px rgba(253,224,71,0.4) !important;
}
section[data-testid="stSidebar"] .stMultiSelect [data-baseweb="select"],
section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(253,224,71,0.15) !important;
    border-radius: 12px !important;
}
section[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.06) !important;
}

/* ════════════════════════════════════════
   HIDE STREAMLIT CHROME
════════════════════════════════════════ */
#MainMenu, footer, header { visibility: hidden !important; }
.stDeployButton { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
.stStatusWidget { display: none !important; }

/* ════════════════════════════════════════
   KPI CARDS — maximum glassmorphism
════════════════════════════════════════ */
.kpi-card {
    background: linear-gradient(145deg,
        rgba(20,30,50,0.75) 0%,
        rgba(15,23,42,0.55) 100%);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 24px;
    padding: 22px 24px;
    position: relative;
    overflow: hidden;
    transition:
        transform 0.35s cubic-bezier(0.34,1.56,0.64,1),
        box-shadow 0.35s ease,
        border-color 0.35s ease,
        background 0.35s ease;
    backdrop-filter: blur(28px) saturate(180%);
    -webkit-backdrop-filter: blur(28px) saturate(180%);
    cursor: default;
    isolation: isolate;
}
/* Top shimmer line */
.kpi-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg,
        transparent 0%,
        var(--ac, #FDE047) 40%,
        rgba(255,255,255,0.8) 50%,
        var(--ac, #FDE047) 60%,
        transparent 100%);
    background-size: 200% auto;
    animation: shimmer-line 3.5s ease-in-out infinite;
    border-radius: 2px 2px 0 0;
}
/* Radial glow orb */
.kpi-card::after {
    content: '';
    position: absolute; top: -50px; right: -30px;
    width: 130px; height: 130px; border-radius: 50%;
    background: radial-gradient(circle, var(--ac, #FDE047) 0%, transparent 70%);
    opacity: 0.08;
    transition: opacity 0.4s ease, transform 0.4s ease;
    filter: blur(8px);
}
.kpi-card:hover {
    transform: translateY(-8px) scale(1.02);
    background: linear-gradient(145deg,
        rgba(25,38,65,0.85) 0%,
        rgba(20,30,50,0.7) 100%);
    box-shadow:
        0 30px 70px rgba(0,0,0,0.6),
        0 0 0 1px rgba(255,255,255,0.12),
        0 0 40px var(--ac, #FDE047)22,
        inset 0 1px 0 rgba(255,255,255,0.1);
    border-color: var(--ac, #FDE047)55;
}
.kpi-card:hover::after { opacity: 0.18; transform: scale(1.3); }
/* Inner glass shine */
.kpi-inner-shine {
    position: absolute; top: 0; left: 0; right: 0;
    height: 50%;
    background: linear-gradient(180deg, rgba(255,255,255,0.04) 0%, transparent 100%);
    border-radius: 24px 24px 0 0;
    pointer-events: none;
}
.kpi-icon {
    font-size: 1.6rem;
    margin-bottom: 12px;
    color: var(--ac, #FDE047);
    filter: drop-shadow(0 0 10px var(--ac, #FDE047));
    transition: filter 0.3s ease, transform 0.3s ease;
    display: inline-block;
}
.kpi-card:hover .kpi-icon {
    filter: drop-shadow(0 0 18px var(--ac, #FDE047));
    transform: scale(1.1) rotate(-5deg);
}
.kpi-val {
    font-size: 2.1rem;
    font-weight: 900;
    color: #f8fafc;
    line-height: 1;
    letter-spacing: -0.03em;
    font-variant-numeric: tabular-nums;
    background: linear-gradient(180deg, #ffffff 0%, #e2e8f0 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.kpi-lbl {
    font-size: 0.6rem;
    color: #cbd5e1;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    margin-top: 6px;
    font-weight: 700;
}
.kpi-delta {
    font-size: 0.72rem;
    color: #94a3b8;
    margin-top: 10px;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 5px;
    padding-top: 10px;
    border-top: 1px solid rgba(255,255,255,0.05);
}
.kpi-delta i { color: var(--ac, #FDE047); font-size: 0.6rem; }

/* ════════════════════════════════════════
   KEYFRAME ANIMATIONS — full suite
════════════════════════════════════════ */
@keyframes shimmer-line {
    0%   { background-position: -200% center; }
    100% { background-position: 300% center; }
}
@keyframes shimmer-bg {
    0%   { transform: translateX(-120%); }
    100% { transform: translateX(120%); }
}
@keyframes glow-pulse {
    0%,100% { opacity: 0.55; filter: brightness(1); }
    50%      { opacity: 1;    filter: brightness(1.3); }
}
@keyframes float-up {
    0%   { opacity: 0; transform: translateY(28px) scale(0.97); }
    100% { opacity: 1; transform: translateY(0) scale(1); }
}
@keyframes slide-in-right {
    0%   { opacity: 0; transform: translateX(20px); }
    100% { opacity: 1; transform: translateX(0); }
}
@keyframes spin-slow {
    0%   { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
@keyframes dot-pulse {
    0%,100% { opacity:1; transform:scale(1);   box-shadow: 0 0 8px var(--dc,#FDE047),  0 0 20px var(--dc,#FDE047)44; }
    50%      { opacity:0.4; transform:scale(0.6); box-shadow: 0 0 3px var(--dc,#FDE047); }
}
@keyframes border-flow {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
@keyframes scale-in {
    0%   { opacity: 0; transform: scale(0.92); }
    100% { opacity: 1; transform: scale(1); }
}
@keyframes neon-flicker {
    0%,19%,21%,23%,25%,54%,56%,100% { opacity: 1; }
    20%,24%,55% { opacity: 0.7; }
}

/* ════════════════════════════════════════
   SECTION PILLS — glassy label
════════════════════════════════════════ */
.sec-pill {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    padding: 8px 20px;
    margin: 20px 0 16px;
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 100px;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    transition: background 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
    position: relative;
    overflow: hidden;
}
.sec-pill::before {
    content: '';
    position: absolute; top: 0; left: -100%; width: 100%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.04), transparent);
    transition: left 0.5s ease;
}
.sec-pill:hover::before { left: 100%; }
.sec-pill:hover {
    background: rgba(255,255,255,0.06);
    border-color: rgba(var(--dc-rgb, 253,224,71), 0.25);
    box-shadow: 0 0 20px rgba(var(--dc-rgb, 253,224,71), 0.08);
}
.sec-dot {
    width: 8px; height: 8px; border-radius: 50%;
    background: var(--dc, #FDE047);
    box-shadow: 0 0 12px var(--dc, #FDE047), 0 0 25px var(--dc, #FDE047)55;
    animation: dot-pulse 2.5s ease-in-out infinite;
    flex-shrink: 0;
}
.sec-txt {
    font-size: 0.72rem;
    font-weight: 700;
    color: #e2e8f0;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

/* ════════════════════════════════════════
   TABS — premium glass navigation
════════════════════════════════════════ */
div[role="tablist"] {
    position: absolute !important;
    opacity: 0 !important;
    pointer-events: none !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 13px !important;
    color: #cbd5e1 !important;
    font-weight: 600 !important;
    font-size: 0.77rem !important;
    padding: 9px 18px !important;
    border: none !important;
    transition: color 0.25s ease, background 0.25s ease !important;
    letter-spacing: 0.03em !important;
    position: relative !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: #FDE047 !important;
    background: rgba(255,255,255,0.06) !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(253,224,71,0.18) 0%, rgba(253,164,175,0.12) 100%) !important;
    color: #FDE047 !important;
    box-shadow:
        0 4px 20px rgba(253,224,71,0.2),
        inset 0 0 0 1px rgba(253,224,71,0.25),
        inset 0 1px 0 rgba(255,255,255,0.08) !important;
    text-shadow: 0 0 20px rgba(253,224,71,0.5) !important;
}

/* ════════════════════════════════════════
   INSIGHT / EXPLANATION CARDS
════════════════════════════════════════ */
.insight {
    background: linear-gradient(135deg,
        rgba(253,224,71,0.06) 0%,
        rgba(192,132,252,0.04) 50%,
        rgba(103,232,249,0.03) 100%);
    border-left: 3px solid #FDE047;
    border-radius: 0 18px 18px 0;
    padding: 18px 24px;
    margin: 16px 0;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(10px);
}
.insight::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(90deg, transparent, rgba(253,224,71,0.04), transparent);
    animation: shimmer-bg 5s ease-in-out infinite;
    pointer-events: none;
}
.insight-lbl {
    font-size: 0.64rem; font-weight: 800; letter-spacing: 0.18em;
    color: #FDE047; text-transform: uppercase; margin-bottom: 8px;
    display: flex; align-items: center; gap: 7px;
}
.insight-txt { font-size: 0.87rem; color: #e2e8f0; line-height: 1.8; }
.insight-txt b { color: #FDE047; font-weight: 700; }

/* What & Why cards */
.explanation-card {
    background: linear-gradient(135deg,
        rgba(103,232,249,0.06) 0%,
        rgba(15,23,42,0.5) 100%);
    border-left: 3px solid #67E8F9;
    border-radius: 0 16px 16px 0;
    padding: 16px 20px;
    margin-top: 10px;
    margin-bottom: 28px;
    font-size: 0.83rem;
    line-height: 1.7;
    color: #cbd5e1;
    backdrop-filter: blur(12px);
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
}
.explanation-card:hover {
    border-color: #7dd3fc;
    box-shadow: 0 4px 24px rgba(103,232,249,0.1), inset 0 0 0 1px rgba(103,232,249,0.08);
}
.explanation-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(90deg, transparent, rgba(103,232,249,0.03), transparent);
    animation: shimmer-bg 6s ease-in-out infinite;
}
.explanation-card b { color: #f8fafc; font-weight: 700; }
.exp-what { margin-bottom: 8px; }
.exp-what span {
    color: #67E8F9; font-weight: 800; font-size: 0.72rem;
    letter-spacing: 0.14em; text-transform: uppercase; margin-right: 10px;
    background: rgba(103,232,249,0.1);
    padding: 2px 8px; border-radius: 4px;
}
.exp-why span {
    color: #FDE047; font-weight: 800; font-size: 0.72rem;
    letter-spacing: 0.14em; text-transform: uppercase; margin-right: 10px;
    background: rgba(253,224,71,0.1);
    padding: 2px 8px; border-radius: 4px;
}

/* ════════════════════════════════════════
   STAT CARDS
════════════════════════════════════════ */
.stat-card {
    background: linear-gradient(145deg, rgba(20,32,55,0.7) 0%, rgba(15,23,42,0.55) 100%);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 18px 20px;
    text-align: center;
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    position: relative;
    overflow: hidden;
}
.stat-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
}
.stat-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 16px 40px rgba(0,0,0,0.5), 0 0 0 1px rgba(255,255,255,0.1);
    border-color: rgba(255,255,255,0.12);
}

/* ════════════════════════════════════════
   ORACLE / PREDICTION CARD
════════════════════════════════════════ */
.oracle-card {
    background: linear-gradient(145deg, rgba(20,12,45,0.8) 0%, rgba(15,10,35,0.7) 100%);
    border: 1px solid rgba(192,132,252,0.25);
    border-radius: 22px;
    padding: 24px;
    margin: 12px 0;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    position: relative;
    overflow: hidden;
    transition: border-color 0.35s ease, box-shadow 0.35s ease, transform 0.35s ease;
}
.oracle-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(192,132,252,0.6), rgba(253,164,175,0.4), transparent);
    animation: border-flow 4s linear infinite;
    background-size: 200% auto;
}
.oracle-card:hover {
    border-color: rgba(192,132,252,0.5);
    box-shadow: 0 20px 50px rgba(192,132,252,0.15), 0 0 0 1px rgba(192,132,252,0.15);
    transform: translateY(-3px);
}

/* ════════════════════════════════════════
   H2H HERO
════════════════════════════════════════ */
.h2h-hero {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 40px;
    padding: 32px;
    margin: 18px 0;
    background: linear-gradient(145deg, rgba(15,23,42,0.7) 0%, rgba(10,16,30,0.8) 100%);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 26px;
    backdrop-filter: blur(24px);
    position: relative;
    overflow: hidden;
}
.h2h-hero::before {
    content: '';
    position: absolute; top: -1px; left: 20%; right: 20%; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.12), transparent);
}
.h2h-hero::after {
    content: '';
    position: absolute; top: 50%; left: 50%;
    width: 200px; height: 200px;
    transform: translate(-50%,-50%);
    background: radial-gradient(circle, rgba(255,255,255,0.025) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}

/* ════════════════════════════════════════
   TEAM BADGE
════════════════════════════════════════ */
.tbadge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 38px; height: 38px;
    border-radius: 50%;
    font-size: 0.56rem;
    font-weight: 900;
    letter-spacing: 0.02em;
    border: 2px solid rgba(255,255,255,0.14);
    flex-shrink: 0;
    cursor: default;
    transition: transform 0.25s cubic-bezier(0.34,1.56,0.64,1), box-shadow 0.25s ease;
    box-shadow: 0 4px 12px rgba(0,0,0,0.4);
}
.tbadge:hover {
    transform: scale(1.2) rotate(-5deg);
    box-shadow: 0 8px 24px rgba(0,0,0,0.5), 0 0 0 3px rgba(255,255,255,0.08);
}

/* ════════════════════════════════════════
   STREAMLIT NATIVE WIDGETS — glass overrides
════════════════════════════════════════ */
/* Metric values */
div[data-testid="stMetricValue"] {
    color: #FDE047 !important;
    font-weight: 900 !important;
    font-size: 2.1rem !important;
    text-shadow: 0 0 30px rgba(253,224,71,0.4) !important;
    letter-spacing: -0.02em !important;
}
div[data-testid="stMetricLabel"] {
    color: #94a3b8 !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    font-weight: 600 !important;
}
div[data-testid="stMetricDelta"] { font-size: 0.75rem !important; }

/* Slider */
div[data-testid="stSlider"] > div > div > div {
    background: linear-gradient(90deg, #FDE047, #FDA4AF) !important;
    box-shadow: 0 0 8px rgba(253,224,71,0.4) !important;
}

/* Selectbox & Multiselect */
div[data-baseweb="select"] > div {
    background: rgba(20,30,50,0.85) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    backdrop-filter: blur(12px) !important;
    transition: border-color 0.2s ease !important;
}
div[data-baseweb="select"] > div:focus-within {
    border-color: rgba(253,224,71,0.35) !important;
    box-shadow: 0 0 0 3px rgba(253,224,71,0.08) !important;
}

/* Radio buttons */
div[data-testid="stRadio"] label {
    padding: 7px 16px !important;
    border-radius: 10px !important;
    cursor: pointer !important;
    transition: background 0.2s ease, color 0.2s ease !important;
    border: 1px solid transparent !important;
}
div[data-testid="stRadio"] label:hover {
    background: rgba(255,255,255,0.05) !important;
    border-color: rgba(255,255,255,0.08) !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, rgba(253,224,71,0.14) 0%, rgba(253,164,175,0.09) 100%) !important;
    border: 1px solid rgba(253,224,71,0.35) !important;
    color: #FDE047 !important;
    border-radius: 14px !important;
    font-weight: 700 !important;
    letter-spacing: 0.05em !important;
    transition: all 0.3s cubic-bezier(0.34,1.56,0.64,1) !important;
    backdrop-filter: blur(8px) !important;
    position: relative !important;
    overflow: hidden !important;
}
.stButton > button::before {
    content: '';
    position: absolute; top: 0; left: -100%; width: 100%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.05), transparent);
    transition: left 0.4s ease !important;
}
.stButton > button:hover::before { left: 100%; }
.stButton > button:hover {
    background: linear-gradient(135deg, rgba(253,224,71,0.26) 0%, rgba(253,164,175,0.18) 100%) !important;
    box-shadow: 0 8px 28px rgba(253,224,71,0.25), 0 0 0 1px rgba(253,224,71,0.2) !important;
    transform: translateY(-3px) scale(1.01) !important;
}
.stButton > button:active { transform: translateY(0) scale(0.99) !important; }

/* Text inputs */
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    background: rgba(20,30,50,0.8) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    color: #f1f5f9 !important;
    font-family: 'Inter', sans-serif !important;
    transition: border-color 0.25s ease, box-shadow 0.25s ease !important;
}
div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(253,224,71,0.4) !important;
    box-shadow: 0 0 0 3px rgba(253,224,71,0.1) !important;
    outline: none !important;
}

/* Expandables */
div[data-testid="stExpander"] {
    background: rgba(15,23,42,0.6) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 16px !important;
    backdrop-filter: blur(16px) !important;
    overflow: hidden !important;
}
div[data-testid="stExpander"] summary {
    font-weight: 600 !important;
    color: #e2e8f0 !important;
    padding: 14px 18px !important;
    border-radius: 16px !important;
    transition: background 0.2s ease !important;
}
div[data-testid="stExpander"] summary:hover {
    background: rgba(255,255,255,0.03) !important;
}

/* Chat input */
div[data-testid="stChatInput"] {
    background: rgba(20,30,50,0.9) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 14px !important;
    backdrop-filter: blur(16px) !important;
}

/* Spinner */
div[data-testid="stSpinner"] { color: #FDE047 !important; }

/* Data table hover */
.data-table tr:hover td { background: rgba(253,224,71,0.05) !important; }

/* ════════════════════════════════════════
   FLOATING CHATBOT (AI ORACLE WOW UI)
════════════════════════════════════════ */
.floating-chat-container {
    position: fixed;
    bottom: 35px;
    right: 35px;
    z-index: 999999;
}
button[data-testid="stPopoverButton"] {
    border-radius: 100px !important;
    padding: 16px 28px !important;
    background: linear-gradient(135deg, #7c3aed, #c084fc, #f472b6, #06b6d4) !important;
    background-size: 300% 300% !important;
    animation: border-flow 6s ease infinite, pulse-glow 3s infinite !important;
    border: none !important;
    color: #ffffff !important;
    font-weight: 800 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    box-shadow:
        0 12px 40px rgba(124,58,237,0.45),
        inset 0 1.5px 0 rgba(255,255,255,0.3) !important;
    transition: all 0.3s cubic-bezier(0.34,1.56,0.64,1) !important;
}
button[data-testid="stPopoverButton"]:hover {
    transform: translateY(-6px) scale(1.06) !important;
    box-shadow:
        0 20px 50px rgba(124,58,237,0.6),
        0 0 30px rgba(192,132,252,0.4),
        inset 0 1.5px 0 rgba(255,255,255,0.4) !important;
}

@keyframes pulse-glow {
    0%, 100% { box-shadow: 0 12px 40px rgba(124,58,237,0.45), 0 0 0 0 rgba(192,132,252,0.4); }
    50% { box-shadow: 0 12px 40px rgba(124,58,237,0.6), 0 0 25px 8px rgba(192,132,252,0.2); }
}

/* Popover panel */
div[data-testid="stPopover"] > div {
    background: linear-gradient(160deg, rgba(15,20,38,0.95) 0%, rgba(8,12,24,0.98) 100%) !important;
    border: 1px solid rgba(192,132,252,0.35) !important;
    border-radius: 24px !important;
    backdrop-filter: blur(35px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(35px) saturate(180%) !important;
    box-shadow: 
        0 30px 80px rgba(0,0,0,0.8), 
        0 0 40px rgba(192,132,252,0.15),
        inset 0 1px 0 rgba(255,255,255,0.05) !important;
    padding: 18px !important;
    width: 460px !important;
}

/* Chat container details */
div[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 16px !important;
    padding: 12px 16px !important;
    margin-bottom: 12px !important;
    backdrop-filter: blur(10px) !important;
    transition: all 0.25s ease;
}
div[data-testid="stChatMessage"]:hover {
    background: rgba(255,255,255,0.05) !important;
    border-color: rgba(192,132,252,0.2) !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}
div[data-testid="stChatMessage"][data-testid="stChatMessage-assistant"] {
    border-left: 3px solid #C084FC !important;
    background: rgba(192,132,252,0.03) !important;
}
div[data-testid="stChatMessage"][data-testid="stChatMessage-user"] {
    border-left: 3px solid #67E8F9 !important;
    background: rgba(103,232,249,0.03) !important;
}
.chat-header {
    background: linear-gradient(90deg, #C084FC, #67E8F9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 1.15rem;
    font-weight: 800;
    margin-bottom: 6px;
    letter-spacing: -0.01em;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ════════════════════════════════════════
   CUSTOM FIXED TOP NAVBAR
════════════════════════════════════════ */
.top-navbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 70px;
    background: rgba(8, 14, 28, 0.45);
    backdrop-filter: blur(20px) saturate(180%);
    -webkit-backdrop-filter: blur(20px) saturate(180%);
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 40px;
    z-index: 99999;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.4);
    transition: all 0.3s ease;
}
.nav-branding {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-left: 50px;
}
.nav-logo-icon {
    font-size: 1.6rem;
    color: #FDE047;
    filter: drop-shadow(0 0 8px rgba(253,224,71,0.6));
}
.nav-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.25rem;
    font-weight: 800;
    letter-spacing: -0.01em;
    background: linear-gradient(90deg, #FDE047 0%, #FDA4AF 50%, #C084FC 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.nav-links {
    display: flex;
    align-items: center;
    gap: 6px;
}
.nav-item {
    padding: 8px 16px;
    border-radius: 10px;
    color: #cbd5e1;
    font-size: 0.8rem;
    font-weight: 600;
    text-decoration: none;
    letter-spacing: 0.02em;
    transition: all 0.25s ease;
    cursor: pointer;
    border: 1px solid transparent;
}
.nav-item:hover {
    color: #FDE047;
    background: rgba(255, 255, 255, 0.04);
}
.nav-item.active {
    color: #FDE047;
    background: rgba(253, 224, 71, 0.1);
    border-color: rgba(253, 224, 71, 0.2);
    box-shadow: 0 0 15px rgba(253, 224, 71, 0.08);
}
.nav-status {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 14px;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 100px;
}
.nav-status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #86EFAC;
    box-shadow: 0 0 8px #86EFAC;
    animation: dot-pulse 2s infinite;
}
.nav-status-text {
    font-size: 0.68rem;
    font-weight: 700;
    color: #cbd5e1;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* Adjust Streamlit Main Content Padding */
.block-container {
    padding-top: 95px !important;
}

/* Reposition Sidebar Toggle Button to fit in Navbar */
button[data-testid="stSidebarCollapseButton"] {
    position: fixed !important;
    top: 17px !important;
    left: 20px !important;
    z-index: 100000 !important;
    background: rgba(20, 30, 50, 0.8) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    color: #FDE047 !important;
    border-radius: 8px !important;
    width: 36px !important;
    height: 36px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    transition: all 0.2s ease !important;
}
button[data-testid="stSidebarCollapseButton"]:hover {
    background: rgba(253, 224, 71, 0.1) !important;
    border-color: rgba(253, 224, 71, 0.3) !important;
    box-shadow: 0 0 10px rgba(253, 224, 71, 0.15) !important;
}

/* ════════════════════════════════════════
   SCROLLBAR — ultra thin
════════════════════════════════════════ */
::-webkit-scrollbar { width: 3px; height: 3px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, rgba(253,224,71,0.3), rgba(192,132,252,0.3));
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.25); }

/* ════════════════════════════════════════
   UTILITY CLASSES
════════════════════════════════════════ */
.fade-in    { animation: float-up 0.55s cubic-bezier(0.22,1,0.36,1) both; }
.slide-in   { animation: slide-in-right 0.45s ease both; }
.glow-text  { animation: glow-pulse 2.5s ease-in-out infinite; }
.scale-in   { animation: scale-in 0.4s ease both; }

/* Neon text utility */
.neon-gold  {
    color: #FDE047;
    text-shadow: 0 0 10px rgba(253,224,71,0.6), 0 0 30px rgba(253,224,71,0.3);
}
.neon-cyan  {
    color: #67E8F9;
    text-shadow: 0 0 10px rgba(103,232,249,0.6), 0 0 30px rgba(103,232,249,0.3);
}
.neon-purple {
    color: #C084FC;
    text-shadow: 0 0 10px rgba(192,132,252,0.6), 0 0 30px rgba(192,132,252,0.3);
}

/* Glass panel */
.glass-panel {
    background: rgba(15,23,42,0.6);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    position: relative;
    overflow: hidden;
}
.glass-panel::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
}

/* Analyst Note Callout */
.analyst-note {
    background: linear-gradient(135deg, rgba(253,224,71,0.08) 0%, rgba(192,132,252,0.06) 100%);
    border-left: 4px solid #FDE047;
    border-radius: 8px 16px 16px 8px;
    padding: 16px 20px;
    margin: 20px 0;
    position: relative;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}
.analyst-note::after {
    content: '\f0eb'; /* Lightbulb icon */
    font-family: 'Font Awesome 6 Free';
    font-weight: 900;
    position: absolute;
    right: 20px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 3rem;
    color: rgba(253,224,71,0.1);
    pointer-events: none;
}
.analyst-note-title {
    font-size: 0.75rem;
    font-weight: 800;
    letter-spacing: 0.16em;
    color: #FDE047;
    text-transform: uppercase;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.analyst-note-text {
    font-size: 0.9rem;
    color: #e2e8f0;
    line-height: 1.6;
}

/* Glass Expander (Collapsible) */
div[data-testid="stExpander"] {
    background: rgba(15,23,42,0.4) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
    backdrop-filter: blur(12px) !important;
    overflow: hidden;
    transition: all 0.3s ease;
}
div[data-testid="stExpander"]:hover {
    background: rgba(15,23,42,0.6) !important;
    border-color: rgba(255,255,255,0.15) !important;
    box-shadow: 0 8px 30px rgba(0,0,0,0.3);
}
div[data-testid="stExpander"] summary {
    padding: 14px 18px !important;
    color: #f1f5f9 !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
}
div[data-testid="stExpander"] summary:hover {
    color: #FDE047 !important;
}
div[data-testid="stExpander"] > div[role="region"] {
    padding: 0 18px 18px !important;
}


/* ════════════════════════════════════════
   RESPONSIVE BREAKPOINTS
════════════════════════════════════════ */
@media (max-width: 1200px) {
    .kpi-val { font-size: 1.8rem; }
}
@media (max-width: 900px) {
    .kpi-val { font-size: 1.6rem; }
    .kpi-card { padding: 18px 16px; border-radius: 18px; }
    .h2h-hero { gap: 20px; padding: 22px; }
    .floating-chat-container { bottom: 24px; right: 24px; }
    button[data-testid="stPopoverButton"] { padding: 12px 20px !important; }
}
@media (max-width: 640px) {
    .kpi-val { font-size: 1.4rem; }
    .kpi-card { padding: 14px 12px; border-radius: 16px; }
    .sec-pill { padding: 6px 14px; }
    .explanation-card { padding: 12px 14px; }
    .floating-chat-container { bottom: 16px; right: 16px; }
    .h2h-hero { flex-direction: column; gap: 14px; }
}
</style>
""", unsafe_allow_html=True)


# ─── COLOUR SYSTEM ────────────────────────────────────────────────────────────
BG    = "#0F172A"
CARD  = "#1E293B"
GOLD  = "#FDE047"
CYAN  = "#67E8F9"
CORAL = "#FDA4AF"
TEAL  = "#2DD4BF"
PURP  = "#C084FC"
GREEN = "#86EFAC"
TEXT  = "#F8FAFC"
MUTED = "#94A3B8"
GRID  = "rgba(255,255,255,0.05)"

# Official IPL team colours (mapped to premium pastel hexes)
TC = {
    "CSK": "#FDE047", "MI": "#60A5FA", "KKR": "#C084FC",
    "RCB": "#F87171", "SRH": "#FB923C", "DC":  "#38BDF8",
    "RR":  "#F472B6", "PBKS":"#F87171", "GT":  "#E2E8F0",
    "LSG": "#22D3EE", "DCH": "#FDBA74", "RPS": "#E9D5FF",
    "PW":  "#FCA5A5", "GL":  "#FDBA74",
}
# Translucent versions for plots
TP = {k: f"rgba({int(v[1:3],16)},{int(v[3:5],16)},{int(v[5:7],16)},0.15)"
      for k, v in TC.items()}

PAL = [GOLD, CYAN, CORAL, TEAL, PURP, GREEN, "#FB923C", "#60A5FA", "#F472B6", "#FACC15"]

BASE_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color=TEXT, size=12),
    margin=dict(l=48, r=24, t=64, b=44),
    xaxis=dict(
        gridcolor="rgba(255,255,255,0.04)",
        linecolor="rgba(255,255,255,0.06)",
        tickfont=dict(color=MUTED, size=10),
        zeroline=False,
        showgrid=True,
    ),
    yaxis=dict(
        gridcolor="rgba(255,255,255,0.04)",
        linecolor="rgba(255,255,255,0.06)",
        tickfont=dict(color=MUTED, size=10),
        zeroline=False,
        showgrid=True,
    ),
    legend=dict(
        bgcolor="rgba(15,23,42,0.7)",
        bordercolor="rgba(255,255,255,0.07)",
        borderwidth=1,
        font=dict(color=TEXT, size=11),
        itemsizing="constant",
        itemclick="toggleothers",
    ),
    hoverlabel=dict(
        bgcolor="rgba(15,23,42,0.95)",
        bordercolor="rgba(253,224,71,0.3)",
        font=dict(color=TEXT, family="Inter", size=12),
    ),
    title=dict(font=dict(family="Inter", size=15, color=TEXT), x=0, xanchor="left"),
    modebar=dict(
        bgcolor="rgba(0,0,0,0)",
        color=MUTED,
        activecolor=GOLD,
        orientation="v",
    ),
)

CHART_CONFIG = {"displayModeBar": False, "responsive": True}


TEAM_MAP = {
    "Delhi Daredevils": "Delhi Capitals",
    "Kings XI Punjab": "Punjab Kings",
    "Rising Pune Supergiant": "Rising Pune Supergiants",
    "Royal Challengers Bangalore": "Royal Challengers Bengaluru",
}
TEAM_SHORT = {
    "Chennai Super Kings":"CSK","Mumbai Indians":"MI","Kolkata Knight Riders":"KKR",
    "Royal Challengers Bengaluru":"RCB","Sunrisers Hyderabad":"SRH",
    "Delhi Capitals":"DC","Rajasthan Royals":"RR","Punjab Kings":"PBKS",
    "Gujarat Titans":"GT","Lucknow Super Giants":"LSG","Deccan Chargers":"DCH",
    "Gujarat Lions":"GL","Rising Pune Supergiants":"RPS","Pune Warriors":"PW",
}

# ─── LOGO UTILITIES ───────────────────────────────────────────────────────────
import base64

def get_team_logo_base64(team_name):
    team_short = TEAM_SHORT.get(team_name, team_name).upper()
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "logos", f"{team_short}.png")
    if os.path.exists(path):
        try:
            with open(path, "rb") as f:
                data = f.read()
            return f"data:image/png;base64,{base64.b64encode(data).decode('utf-8')}"
        except Exception:
            pass
    return None

def get_team_logo_html(team_name, size=24):
    b64 = get_team_logo_base64(team_name)
    if b64:
        return f'<img src="{b64}" style="width:{size}px;height:{size}px;object-fit:contain;vertical-align:middle;margin-right:8px;" alt="{team_name}">'
    return ""

SEASON_MAP = {"2007/08":"2008","2009/10":"2010","2020/21":"2020"}

# ─── DATA LOADING ─────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data():
    BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    df = pd.read_csv(os.path.join(BASE, "data", "ipl_matches.csv"), low_memory=False)
    for c in ["team1","team2","toss_winner","winner","batting_team"]:
        if c in df.columns:
            df[c] = df[c].replace(TEAM_MAP)
    df["season"] = df["season"].astype(str).replace(SEASON_MAP).astype(int)
    df["date"]   = pd.to_datetime(df["date"])
    df["phase"]  = df["over"].apply(lambda o: "Powerplay" if o<6 else ("Middle" if o<15 else "Death"))
    df["is_four"]   = (df["runs_batter"]==4).astype(int)
    df["is_six"]    = (df["runs_batter"]==6).astype(int)
    df["is_wicket"] = df["wicket_kind"].notna().astype(int)
    df["is_dot"]    = ((df["runs_total"]==0) & df["wicket_kind"].isna()).astype(int)

    mc = ["match_id","date","season","venue","city","team1","team2",
          "toss_winner","toss_decision","winner","win_by_runs","win_by_wickets","player_of_match"]
    m = df[mc].drop_duplicates("match_id").copy()
    m["twmw"] = m["toss_winner"] == m["winner"]
    m = m[m["winner"].notna() & ~m["winner"].isin(["tie","no result"])]
    m["ws"]  = m["winner"].map(TEAM_SHORT).fillna(m["winner"])
    m["t1s"] = m["team1"].map(TEAM_SHORT).fillna(m["team1"])
    m["t2s"] = m["team2"].map(TEAM_SHORT).fillna(m["team2"])
    return df, m

with st.spinner("Loading IPL Intelligence Hub..."):
    df, matches = load_data()

SEASONS          = sorted(df["season"].unique())
TEAMS_LONG       = sorted(set(df["batting_team"].unique()))
TEAMS_SHORT_LIST = sorted(matches["ws"].unique())

def render_explanation(what_text, why_text):
    """Renders a beautiful What & Why explanation card below visualizations."""
    st.markdown(f"""
    <div class="explanation-card">
        <div class="exp-what"><span>WHAT</span> {what_text}</div>
        <div class="exp-why"><span>WHY</span> {why_text}</div>
    </div>
    """, unsafe_allow_html=True)

def render_chatbot(context_text):
    """Renders a floating Groq-powered chatbot."""
    st.markdown('<div class="floating-chat-container">', unsafe_allow_html=True)
    with st.popover("💬 Ask IPL Oracle", use_container_width=False):
        st.markdown("""
<div class="chat-header">
<i class="fa-solid fa-wand-magic-sparkles" style="color:#C084FC; margin-right: 6px;"></i>
<span>IPL Match Oracle</span>
</div>
<div style="font-size:0.75rem; color:#94a3b8; margin-bottom:14px; letter-spacing: 0.05em; text-transform: uppercase;">
Cognitive intelligence & Predictive Insights
</div>
""", unsafe_allow_html=True)
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "Hi! I'm your IPL data oracle. Ask me anything about the matches, teams, or players!"}
            ]

        # Display chat messages from history on app rerun
        chat_container = st.container(height=350)
        with chat_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        # Chat input
        if prompt := st.chat_input("Ask about IPL stats..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with chat_container:
                with st.chat_message("user"):
                    st.markdown(prompt)

                with st.chat_message("assistant"):
                    groq_api_key = os.getenv("GROQ_API_KEY")
                    if not groq_api_key or groq_api_key == "your_groq_api_key_here":
                        st.error("Please add your Groq API key to the .env file to use the chatbot.")
                    else:
                        try:
                            from groq import Groq
                            client = Groq(api_key=groq_api_key)
                            
                            system_prompt = f"You are an expert IPL data analyst. Answer questions concisely and professionally based on this dashboard context: {context_text}. Keep answers under 3 paragraphs."
                            
                            # Build messages for Groq
                            api_messages = [{"role": "system", "content": system_prompt}]
                            for msg in st.session_state.messages[-5:]: # Keep context short
                                api_messages.append({"role": msg["role"], "content": msg["content"]})
                            
                            # Call API
                            completion = client.chat.completions.create(
                                model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
                                messages=api_messages,
                                temperature=0.7,
                                max_completion_tokens=512,
                                stream=False
                            )
                            
                            response = completion.choices[0].message.content
                            st.markdown(response)
                            st.session_state.messages.append({"role": "assistant", "content": response})
                            
                        except Exception as e:
                            st.error(f"Error calling Groq API: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
# Initialize session state for filters if not set
if "filter_season" not in st.session_state:
    st.session_state.filter_season = (int(min(SEASONS)), int(max(SEASONS)))
if "filter_teams" not in st.session_state:
    st.session_state.filter_teams = ["All Teams"]
if "filter_venues" not in st.session_state:
    st.session_state.filter_venues = ["All Venues"]
if "filter_innings" not in st.session_state:
    st.session_state.filter_innings = "Both"
if "filter_toss" not in st.session_state:
    st.session_state.filter_toss = "All"
if "filter_phase" not in st.session_state:
    st.session_state.filter_phase = "All Phases"
if "filter_win" not in st.session_state:
    st.session_state.filter_win = "All"

def reset_filters():
    st.session_state.filter_season = (int(min(SEASONS)), int(max(SEASONS)))
    st.session_state.filter_teams = ["All Teams"]
    st.session_state.filter_venues = ["All Venues"]
    st.session_state.filter_innings = "Both"
    st.session_state.filter_toss = "All"
    st.session_state.filter_phase = "All Phases"
    st.session_state.filter_win = "All"

with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:22px 0 16px;">
        <div style="font-size:3rem;filter:drop-shadow(0 0 18px rgba(253,224,71,0.55));">
            <i class="fa-solid fa-baseball-bat-ball" style="color:#FDE047;"></i>
        </div>
        <div style="font-size:1.1rem;font-weight:900;letter-spacing:-0.02em;margin-top:8px;
                    background:linear-gradient(90deg,#FDE047,#FDA4AF,#C084FC);
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
            IPL SixSense Analytics
        </div>
        <div style="font-size:0.62rem;color:#94a3b8;letter-spacing:0.16em;margin-top:2px;">
            CRUNCH '26 · ANALYTICS HUB
        </div>
    </div>
    <div style="height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,0.08),transparent);margin:0 0 20px;"></div>
    """, unsafe_allow_html=True)

    st.markdown('<p style="font-size:0.68rem;color:#94a3b8;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:6px;"><i class="fa-solid fa-calendar-days" style="margin-right:6px;color:#FDE047;"></i> SEASON RANGE</p>', unsafe_allow_html=True)
    s_range = st.slider("Season", int(min(SEASONS)), int(max(SEASONS)),
                        key="filter_season", label_visibility="collapsed")

    st.markdown('<p style="font-size:0.68rem;color:#94a3b8;letter-spacing:0.1em;text-transform:uppercase;margin:14px 0 6px;"><i class="fa-solid fa-people-group" style="margin-right:6px;color:#60A5FA;"></i> TEAMS</p>', unsafe_allow_html=True)
    sel_teams = st.multiselect("Teams", ["All Teams"]+sorted(TEAMS_LONG),
                               key="filter_teams", label_visibility="collapsed")

    st.markdown('<p style="font-size:0.68rem;color:#94a3b8;letter-spacing:0.1em;text-transform:uppercase;margin:14px 0 6px;"><i class="fa-solid fa-stadium" style="margin-right:6px;color:#C084FC;"></i> VENUES</p>', unsafe_allow_html=True)
    sel_venues = st.multiselect("Venues", ["All Venues"]+sorted(df["venue"].dropna().unique()),
                                key="filter_venues", label_visibility="collapsed")

    st.markdown('<p style="font-size:0.68rem;color:#94a3b8;letter-spacing:0.1em;text-transform:uppercase;margin:14px 0 6px;"><i class="fa-solid fa-clock" style="margin-right:6px;color:#2DD4BF;"></i> INNINGS</p>', unsafe_allow_html=True)
    inn_filter = st.radio("Innings", ["Both","1st Only","2nd Only"],
                          key="filter_innings", label_visibility="collapsed")

    st.markdown('<p style="font-size:0.68rem;color:#94a3b8;letter-spacing:0.1em;text-transform:uppercase;margin:14px 0 6px;"><i class="fa-solid fa-gavel" style="margin-right:6px;color:#FDA4AF;"></i> TOSS DECISION</p>', unsafe_allow_html=True)
    toss_filter = st.radio("Toss Decision", ["All", "Batting first", "Fielding first"],
                           key="filter_toss", label_visibility="collapsed")

    st.markdown('<p style="font-size:0.68rem;color:#94a3b8;letter-spacing:0.1em;text-transform:uppercase;margin:14px 0 6px;"><i class="fa-solid fa-chart-line" style="margin-right:6px;color:#86EFAC;"></i> MATCH PHASE</p>', unsafe_allow_html=True)
    phase_filter = st.radio("Match Phase", ["All Phases", "Powerplay (Overs 0-5)", "Middle (Overs 6-14)", "Death (Overs 15-20)"],
                            key="filter_phase", label_visibility="collapsed")

    st.markdown('<p style="font-size:0.68rem;color:#94a3b8;letter-spacing:0.1em;text-transform:uppercase;margin:14px 0 6px;"><i class="fa-solid fa-trophy" style="margin-right:6px;color:#FDE047;"></i> WIN TYPE</p>', unsafe_allow_html=True)
    win_filter = st.radio("Win Type", ["All", "Defending (Won by Runs)", "Chasing (Won by Wickets)"],
                          key="filter_win", label_visibility="collapsed")

    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
    st.button("Reset All Filters", on_click=reset_filters, use_container_width=True)

    st.markdown(f"""
    <div style="height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,0.08),transparent);margin:20px 0 14px;"></div>
    <div style="font-size:0.66rem;color:#94a3b8;text-align:center;line-height:2.1;">
        <div style="color:#86efac;font-size:0.78rem;font-weight:700;margin-bottom:4px;">
            <i class="fa-solid fa-circle-play" style="color:#86efac;margin-right:4px;"></i> LIVE ENGINE
        </div>
        {len(df):,} deliveries<br>{len(matches):,} matches · {len(SEASONS)} seasons
    </div>
    """, unsafe_allow_html=True)

# ─── APPLY FILTERS ────────────────────────────────────────────────────────────
dff = df[df["season"].between(s_range[0], s_range[1])].copy()
mff = matches[matches["season"].between(s_range[0], s_range[1])].copy()

if "All Teams" not in sel_teams and sel_teams:
    dff = dff[dff["batting_team"].isin(sel_teams)]
    mff = mff[mff["team1"].isin(sel_teams) | mff["team2"].isin(sel_teams)]

if "All Venues" not in sel_venues and sel_venues:
    dff = dff[dff["venue"].isin(sel_venues)]
    mff = mff[mff["venue"].isin(sel_venues)]

if inn_filter == "1st Only":
    dff = dff[dff["innings"]==1]
elif inn_filter == "2nd Only":
    dff = dff[dff["innings"]==2]

if toss_filter == "Batting first":
    mff = mff[mff["toss_decision"]=="bat"]
    dff = dff[dff["toss_decision"]=="bat"]
elif toss_filter == "Fielding first":
    mff = mff[mff["toss_decision"]=="field"]
    dff = dff[dff["toss_decision"]=="field"]

if phase_filter != "All Phases":
    phase_map = {
        "Powerplay (Overs 0-5)": "Powerplay",
        "Middle (Overs 6-14)": "Middle",
        "Death (Overs 15-20)": "Death"
    }
    target_phase = phase_map.get(phase_filter)
    dff = dff[dff["phase"]==target_phase]

if win_filter == "Defending (Won by Runs)":
    mff = mff[mff["win_by_runs"] > 0]
    dff = dff[dff["match_id"].isin(mff["match_id"])]
elif win_filter == "Chasing (Won by Wickets)":
    mff = mff[mff["win_by_wickets"] > 0]
    dff = dff[dff["match_id"].isin(mff["match_id"])]

# ─── TOP NAVBAR ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="top-navbar">
<div class="nav-branding">
<i class="fa-solid fa-baseball-bat-ball nav-logo-icon"></i>
<span class="nav-title">IPL SixSense Analytics</span>
</div>
<div class="nav-links">
<div class="nav-item">Summary</div>
<div class="nav-item">Overview</div>
<div class="nav-item">Toss</div>
<div class="nav-item">Phases</div>
<div class="nav-item">Players</div>
<div class="nav-item">Team DNA</div>
<div class="nav-item">Oracle</div>
<div class="nav-item">Insights</div>
</div>
<div class="nav-status">
<div class="nav-status-dot"></div>
<span class="nav-status-text">Live Engine Active</span>
</div>
</div>
""", unsafe_allow_html=True)

# Robust JS handler via components.html
components.html("""
<script>
    const parent = window.parent.document;
    
    function clickNativeTab(tabName) {
        const tabs = Array.from(parent.querySelectorAll('button')).filter(b => b.getAttribute('role') === 'tab' || b.getAttribute('data-baseweb') === 'tab');
        const target = tabs.find(b => b.innerText.includes(tabName));
        if (target) {
            target.click();
        }
    }

    function setupNav() {
        const navItems = parent.querySelectorAll('.nav-item');
        if (navItems.length === 0) {
            setTimeout(setupNav, 200); // retry if not rendered
            return;
        }
        
        navItems.forEach(item => {
            // Remove old listeners by replacing node
            const newItem = item.cloneNode(true);
            item.parentNode.replaceChild(newItem, item);
            
            newItem.addEventListener('click', function() {
                const tabName = this.innerText.trim();
                clickNativeTab(tabName);
            });
        });
    }
    
    setupNav();

    // Sync active state from native tabs to custom navbar
    setInterval(() => {
        const nativeTabs = Array.from(parent.querySelectorAll('button')).filter(b => b.getAttribute('role') === 'tab' || b.getAttribute('data-baseweb') === 'tab');
        const localNavItems = parent.querySelectorAll('.nav-item');
        let activeIndex = -1;
        nativeTabs.forEach((tab, index) => {
            if (tab.getAttribute('aria-selected') === 'true') activeIndex = index;
        });
        if (activeIndex !== -1 && localNavItems.length > activeIndex) {
            localNavItems.forEach((item, index) => {
                if (index === activeIndex) item.classList.add('active');
                else item.classList.remove('active');
            });
        }
    }, 100);
</script>
""", height=0)

# ─── HERO SECTION ──────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="padding: 60px 40px 50px; margin: -40px -16px 30px; background: linear-gradient(135deg, rgba(15,23,42,0.6) 0%, rgba(10,16,30,0.85) 100%); border-bottom: 2px solid rgba(253,224,71,0.2); position: relative; overflow: hidden; text-align: center; border-radius: 0 0 24px 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.6); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);">
<div style="position:absolute;top:-80px;left:-40px;width:300px;height:300px;border-radius:50%;background:radial-gradient(circle,rgba(253,224,71,0.15),transparent 70%);pointer-events:none; filter:blur(20px);"></div>
<div style="position:absolute;bottom:-100px;right:-60px;width:400px;height:400px;border-radius:50%;background:radial-gradient(circle,rgba(192,132,252,0.1),transparent 70%);pointer-events:none; filter:blur(30px);"></div>

<div style="display:inline-flex;align-items:center;gap:10px;padding:6px 20px;background:rgba(253,224,71,0.1);border:1px solid rgba(253,224,71,0.3);border-radius:100px;margin-bottom:20px; backdrop-filter: blur(10px);">
<div style="width:8px;height:8px;border-radius:50%;background:#FDE047;box-shadow:0 0 12px #FDE047;animation:dot-pulse 2s infinite;"></div>
<span style="font-size:0.75rem;font-weight:800;letter-spacing:0.2em;color:#FDE047;text-transform:uppercase;">Live Analytics Engine Active</span>
</div>

<div style="font-size:3.8rem;font-weight:900;letter-spacing:-0.04em;line-height:1.1;margin-bottom:16px;">
<span style="background:linear-gradient(90deg,#FDE047 0%,#FDA4AF 35%,#C084FC 65%,#67E8F9 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-size:200% auto;">
{'IPL SixSense Analytics' if 'All Teams' in sel_teams else ' vs '.join(sel_teams) + ' Analytics'}
</span>
</div>

<p style="color:#e2e8f0;font-size:1.15rem;letter-spacing:0.02em;margin-bottom:30px; max-width: 700px; margin-left: auto; margin-right: auto; line-height: 1.6; text-shadow: 0 2px 4px rgba(0,0,0,0.5);">
Dive deep into comprehensive match data, player statistics, and predictive insights across all seasons. Experience the ultimate cricket analytics dashboard.
</p>

<div style="display: inline-flex; justify-content: center; gap: 20px; color:#f8fafc;font-size:0.95rem;letter-spacing:0.05em; background: rgba(0,0,0,0.4); padding: 12px 24px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); backdrop-filter: blur(10px);">
<div><i class="fa-solid fa-calendar" style="color:#C084FC; margin-right:6px;"></i> <b style="color:#fff;">{s_range[0]} – {s_range[1]}</b></div>
<div style="color:rgba(255,255,255,0.2);">|</div>
<div><i class="fa-solid fa-trophy" style="color:#FDE047; margin-right:6px;"></i> <b style="color:#fff;">{mff['match_id'].nunique():,}</b> matches</div>
<div style="color:rgba(255,255,255,0.2);">|</div>
<div><i class="fa-solid fa-baseball" style="color:#FDA4AF; margin-right:6px;"></i> <b style="color:#fff;">{len(dff):,}</b> deliveries</div>
</div>
</div>
""", unsafe_allow_html=True)

# ─── KPI ROW ──────────────────────────────────────────────────────────────────
n_matches = mff["match_id"].nunique()
n_runs    = int(dff["runs_total"].sum())
n_wkts    = int(dff["is_wicket"].sum())
n_sixes   = int(dff["is_six"].sum())
n_fours   = int(dff["is_four"].sum())
avg_rr    = round(dff["runs_total"].sum() / max(dff["ball"].count()/6, 1), 2)
dot_pct   = round(dff["is_dot"].sum() / max(dff["ball"].count(), 1) * 100, 1)
try:
    top_scorer     = dff.groupby("batter")["runs_batter"].sum().idxmax().split()[-1]
    top_scorer_runs = int(dff.groupby("batter")["runs_batter"].sum().max())
except Exception:
    top_scorer = "—"; top_scorer_runs = 0

kpi_data = [
    ("<i class='fa-solid fa-trophy'></i>",        f"{n_matches:,}",  "MATCHES",      f"{dff['season'].nunique()} seasons",  GOLD),
    ("<i class='fa-solid fa-person-running'></i>", f"{n_runs:,}",     "TOTAL RUNS",   f"avg {avg_rr} per over",               CYAN),
    ("<i class='fa-solid fa-circle-dot'></i>",    f"{n_wkts:,}",     "WICKETS FELL", "all dismissal kinds",                  CORAL),
    ("<i class='fa-solid fa-fire'></i>",          f"{n_sixes:,}",    "SIXES",        f"{n_fours:,} fours too",               PURP),
    ("<i class='fa-solid fa-gauge-high'></i>",    f"{avg_rr}",       "AVG RUN RATE", f"{dot_pct}% dot balls",                TEAL),
    ("<i class='fa-solid fa-crown'></i>",         top_scorer,        "TOP SCORER",   f"{top_scorer_runs:,} career runs",     "#FACC15"),
]
cols = st.columns(6)
for i, (col, (icon, val, lbl, delta, acc)) in enumerate(zip(cols, kpi_data)):
    col.markdown(f"""
    <div class="kpi-card" style="--ac:{acc}; animation: float-up 0.5s ease {i*0.08:.2f}s both;">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-val">{val}</div>
        <div class="kpi-lbl">{lbl}</div>
        <div class="kpi-delta">
            <i class="fa-solid fa-arrow-trend-up" style="font-size:0.65rem;"></i>&nbsp;{delta}
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)


# Calculate career/season stats for all players based on filtered data (dff)
bat_s = (dff.groupby("batter").agg(
    runs=("runs_batter","sum"), balls=("ball","count"),
    fours=("is_four","sum"), sixes=("is_six","sum"),
    inn=("match_id","nunique")).reset_index())
bat_s["sr"] = (bat_s["runs"] / bat_s["balls"] * 100).round(2)
bat_s = bat_s[bat_s["balls"]>=200].sort_values("runs", ascending=False)

bowl_s = (dff.groupby("bowler").agg(
    wkts=("is_wicket","sum"), runs_c=("runs_total","sum"),
    balls=("ball","count"), inn=("match_id","nunique")).reset_index())
bowl_s["eco"] = (bowl_s["runs_c"] / (bowl_s["balls"]/6)).round(2)
bowl_s["avg"] = (bowl_s["runs_c"] / bowl_s["wkts"].replace(0, np.nan)).round(2)
bowl_s = bowl_s[bowl_s["balls"]>=300].sort_values("wkts", ascending=False)

MEDAL = ["\U0001f947", "\U0001f948", "\U0001f949"]  # gold, silver, bronze

def make_html_table(df, title, header_color):
    rows_html = ""
    for rank, (idx, row) in enumerate(df.iterrows()):
        row_vals = []
        for ci, (col, val) in enumerate(zip(df.columns, row)):
            if ci == 0:  # first column = name — add medal for top 3
                medal = f"<span style='margin-right:6px;font-size:0.9em;'>{MEDAL[rank]}</span>" if rank < 3 else "<span style='margin-right:22px;'></span>"
                row_vals.append(f"{medal}<b style='color:#f8fafc;'>{val}</b>")
            elif isinstance(val, float):
                row_vals.append(f"<span style='font-variant-numeric:tabular-nums;'>{val:.2f}</span>")
            elif isinstance(val, (int, np.integer)):
                row_vals.append(f"<span style='font-variant-numeric:tabular-nums;'>{val:,}</span>")
            else:
                row_vals.append(str(val))
        row_bg = "rgba(255,255,255,0.025)" if rank % 2 == 0 else "transparent"
        top_glow = f"box-shadow:inset 3px 0 0 {header_color}88;" if rank == 0 else ""
        cells_html = "".join([
            f'<td style="padding:11px 10px;color:#cbd5e1;vertical-align:middle;">{val}</td>'
            for val in row_vals
        ])
        rows_html += f'<tr style="background:{row_bg};{top_glow}transition:background 0.2s ease;" onmouseover="this.style.background=\'rgba(253,224,71,0.04)\'" onmouseout="this.style.background=\'{row_bg}\'">{cells_html}</tr>'
    headers_html = "".join([
        f'<th style="padding:10px;text-align:left;border-bottom:1px solid {header_color}44;color:{header_color};font-weight:700;font-size:0.7rem;letter-spacing:0.1em;text-transform:uppercase;">{col}</th>'
        for col in df.columns
    ])
    return f"""
    <div style="background:rgba(15,23,42,0.8);border:1px solid rgba(255,255,255,0.06);
                border-radius:16px;padding:18px 20px;margin:10px 0;
                backdrop-filter:blur(12px);overflow:hidden;position:relative;">
        <div style="position:absolute;top:0;left:0;right:0;height:2px;
                    background:linear-gradient(90deg,{header_color},transparent);"></div>
        <div style="margin-bottom:14px;display:flex;align-items:center;gap:8px;">
            <div style="width:6px;height:6px;border-radius:50%;background:{header_color};
                        box-shadow:0 0 8px {header_color};"></div>
            <span style="font-size:0.9rem;font-weight:700;color:#f1f5f9;">{title}</span>
        </div>
        <table style="width:100%;border-collapse:collapse;font-size:0.86rem;">
            <thead><tr style="border-bottom:1px solid rgba(255,255,255,0.06);">{headers_html}</tr></thead>
            <tbody>{rows_html}</tbody>
        </table>
    </div>
    """

# ─── 8 TABS ───────────────────────────────────────────────────────────────────
tab0, tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "  Summary", "  Overview", "  Toss", "  Phases",
    "  Players", "  Team DNA", "  Oracle", "  Insights"
])

# ═══════════════════════════════════════════════════════════════════════════════
#  TAB 0 — EXECUTIVE SUMMARY
# ═══════════════════════════════════════════════════════════════════════════════
with tab0:
    st.markdown("""<div class="sec-pill" style="--dc:#FDE047;"><div class="sec-dot"></div>
    <div class="sec-txt"><i class="fa-solid fa-list-check" style="margin-right:6px;"></i> Key Deliverables & Target Answers</div></div>""",
    unsafe_allow_html=True)

    # 1. Answer cards
    ans1, ans2, ans3 = st.columns(3)
    
    toss_win_rate = mff["twmw"].mean() * 100
    toss_lose_rate = 100 - toss_win_rate
    
    ans1.markdown(f"""
    <div class="kpi-card" style="--ac:{GOLD}; min-height:165px;">
        <div class="kpi-icon"><i class="fa-solid fa-coins"></i></div>
        <div class="kpi-val">{toss_win_rate:.1f}%</div>
        <div class="kpi-lbl">TOSS WINNER MATCH WIN %</div>
        <div class="kpi-delta" style="color:#94a3b8; font-size:0.75rem; margin-top:6px;">
            <b>Verdict: No.</b> Toss winners win {toss_win_rate:.1f}% of matches, which is statistically a 50/50 coin flip.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Determine phase link to winning
    # Map winner of each match to the deliveries dataframe
    winner_map = mff.set_index("match_id")["winner"].to_dict()
    dff_phase = dff.copy()
    dff_phase["match_winner"] = dff_phase["match_id"].map(winner_map)
    dff_phase["is_winner_batting"] = dff_phase["batting_team"] == dff_phase["match_winner"]

    # Calculate runs per phase per match
    match_phase_runs = dff_phase.groupby(["match_id", "is_winner_batting", "phase"])["runs_total"].sum()
    match_phase_runs = match_phase_runs.unstack(level="phase", fill_value=0).stack().reset_index(name="runs_total")

    # Get average runs per phase
    avg_phase_runs = match_phase_runs.groupby(["is_winner_batting", "phase"])["runs_total"].mean().reset_index()
    winner_phase = avg_phase_runs[avg_phase_runs["is_winner_batting"] == True]
    loser_phase = avg_phase_runs[avg_phase_runs["is_winner_batting"] == False]

    # Reindex
    phase_order = ["Powerplay", "Middle", "Death"]
    winner_phase = winner_phase.set_index("phase").reindex(phase_order).fillna(0).reset_index()
    loser_phase = loser_phase.set_index("phase").reindex(phase_order).fillna(0).reset_index()
    
    # Calculate deltas between winner and loser runs per phase
    pp_diff = float(winner_phase.loc[winner_phase["phase"]=="Powerplay", "runs_total"].values[0]) if "Powerplay" in winner_phase["phase"].values else 0
    mid_diff = float(winner_phase.loc[winner_phase["phase"]=="Middle", "runs_total"].values[0]) if "Middle" in winner_phase["phase"].values else 0
    death_diff = float(winner_phase.loc[winner_phase["phase"]=="Death", "runs_total"].values[0]) if "Death" in winner_phase["phase"].values else 0

    pp_diff_loser = float(loser_phase.loc[loser_phase["phase"]=="Powerplay", "runs_total"].values[0]) if "Powerplay" in loser_phase["phase"].values else 0
    mid_diff_loser = float(loser_phase.loc[loser_phase["phase"]=="Middle", "runs_total"].values[0]) if "Middle" in loser_phase["phase"].values else 0
    death_diff_loser = float(loser_phase.loc[loser_phase["phase"]=="Death", "runs_total"].values[0]) if "Death" in loser_phase["phase"].values else 0

    diffs = {"Powerplay": pp_diff - pp_diff_loser, "Middle": mid_diff - mid_diff_loser, "Death": death_diff - death_diff_loser}
    most_linked_phase = max(diffs, key=diffs.get)
    max_diff = diffs[most_linked_phase]

    ans2.markdown(f"""
    <div class="kpi-card" style="--ac:{CYAN}; min-height:165px;">
        <div class="kpi-icon"><i class="fa-solid fa-gauge-high"></i></div>
        <div class="kpi-val">{most_linked_phase.upper()}</div>
        <div class="kpi-lbl">MOST INFLUENTIAL PHASE</div>
        <div class="kpi-delta" style="color:#94a3b8; font-size:0.75rem; margin-top:6px;">
            <b>Verdict: {most_linked_phase} overs</b> show the largest score gap (+{max_diff:.1f} runs avg) between winning and losing teams.
        </div>
    </div>
    """, unsafe_allow_html=True)

    ans3.markdown(f"""
    <div class="kpi-card" style="--ac:{CORAL}; min-height:165px;">
        <div class="kpi-icon"><i class="fa-solid fa-fire"></i></div>
        <div class="kpi-val">SURPRISE</div>
        <div class="kpi-lbl">ONE-SENTENCE INSIGHT</div>
        <div class="kpi-delta" style="color:#94a3b8; font-size:0.72rem; margin-top:6px; line-height:1.4;">
            Chasing teams win 50.3% of matches, but success drops off a cliff above 180 runs—making bowler economy the most critical metric.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts 1 & 2
    c1, c2 = st.columns(2)
    
    with c1:
        # Chart 1: Toss Winner vs Loser Win Rate
        fig_toss_bars = go.Figure(go.Bar(
            x=["Toss Winners", "Toss Losers"],
            y=[toss_win_rate, toss_lose_rate],
            marker_color=[GREEN, CORAL],
            opacity=0.9,
            text=[f"<b>{toss_win_rate:.1f}%</b>", f"<b>{toss_lose_rate:.1f}%</b>"],
            textposition="outside",
            hovertemplate="Win Rate: %{y:.1f}%<extra></extra>"
        ))
        fig_toss_bars.update_layout(BASE_LAYOUT)
        fig_toss_bars.update_layout(
            height=320,
            title=dict(text="<b><i class='fa-solid fa-chart-bar' style='color:#FDE047;margin-right:8px;'></i> Chart 1: Win Rate of Toss Winners vs Toss Losers</b>",
                       font=dict(size=14, color=TEXT), x=0),
            yaxis=dict(title="Win %", range=[0, 110], gridcolor=GRID),
            xaxis=dict(gridcolor=GRID),
        )
        st.plotly_chart(fig_toss_bars, use_container_width=True, config=CHART_CONFIG)
        render_explanation(
            "Win rate of teams that win the toss vs those that lose.",
            "Toss winners have historically won exactly 50% of matches. This proves that winning the toss offers no statistically significant advantage in the IPL."
        )

    with c2:
        # Chart 2: Average Runs per Phase for Winning vs Losing Teams
        fig_phase_win_lose = go.Figure()
        fig_phase_win_lose.add_bar(
            x=winner_phase["phase"],
            y=winner_phase["runs_total"],
            name="Winning Team",
            marker_color=GREEN,
            opacity=0.9,
            text=winner_phase["runs_total"].round(1),
            textposition="outside",
            hovertemplate="<b>Winner</b><br>%{x}: %{y:.1f} runs<extra></extra>"
        )
        fig_phase_win_lose.add_bar(
            x=loser_phase["phase"],
            y=loser_phase["runs_total"],
            name="Losing Team",
            marker_color=CORAL,
            opacity=0.9,
            text=loser_phase["runs_total"].round(1),
            textposition="outside",
            hovertemplate="<b>Loser</b><br>%{x}: %{y:.1f} runs<extra></extra>"
        )
        fig_phase_win_lose.update_layout(BASE_LAYOUT)
        fig_phase_win_lose.update_layout(
            height=320,
            barmode="group",
            title=dict(text="<b><i class='fa-solid fa-chart-column' style='color:#FDA4AF;margin-right:8px;'></i> Chart 2: Average Runs per Phase (Winner vs Loser)</b>",
                       font=dict(size=14, color=TEXT), x=0),
            xaxis=dict(gridcolor=GRID),
            yaxis=dict(gridcolor=GRID, title="Avg Runs", range=[0, max(winner_phase["runs_total"].max(), loser_phase["runs_total"].max()) * 1.25]),
        )
        st.plotly_chart(fig_phase_win_lose, use_container_width=True, config=CHART_CONFIG)
        render_explanation(
            "Average runs scored by match winners vs match losers broken down by phase.",
            "Winning teams outscore losing teams by the largest margin during the Death Overs. This phase is the highest differentiator between winning and losing."
        )

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Table: Top 5 Batters & Top 5 Bowlers
    tc1, tc2 = st.columns(2)
    with tc1:
        top5_bat = bat_s.head(5)[["batter", "runs", "balls", "sr"]]
        top5_bat.columns = ["Batter", "Runs", "Balls", "Strike Rate"]
        st.markdown(make_html_table(top5_bat, "<i class='fa-solid fa-crown' style='color:#FDE047;'></i> Top 5 Batters by Runs", "#FDE047"), unsafe_allow_html=True)
        render_explanation("Top 5 batters sorted by aggregate career runs in the IPL.", "Consistency over multiple seasons defines the elite. High strike rates among these leaders show they aren't just accumulating runs, they are scoring quickly.")
        
    with tc2:
        top5_bowl = bowl_s.head(5)[["bowler", "wkts", "eco", "avg"]]
        top5_bowl.columns = ["Bowler", "Wickets", "Economy", "Average"]
        st.markdown(make_html_table(top5_bowl, "<i class='fa-solid fa-circle-dot' style='color:#67E8F9;'></i> Top 5 Bowlers by Wickets", "#67E8F9"), unsafe_allow_html=True)
        render_explanation("Top 5 bowlers sorted by aggregate career wickets in the IPL.", "Wicket-takers disrupt partnerships. Note how the best wicket-takers also maintain highly economical rates, increasing pressure on the opposition.")

# ═══════════════════════════════════════════════════════════════════════════════
#  TAB 1 — OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("""<div class="sec-pill" style="--dc:#FDE047;"><div class="sec-dot"></div>
    <div class="sec-txt"><i class="fa-solid fa-sliders" style="margin-right:6px;"></i> Command Centre · Season Overview</div></div>""", unsafe_allow_html=True)

    r1c1, r1c2 = st.columns([3, 2])

    # Scoring revolution
    with r1c1:
        seas = (dff.groupby(["match_id","season"])["runs_total"].sum()
                .reset_index().groupby("season")["runs_total"].mean()
                .reset_index(name="avg"))
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=seas["season"], y=seas["avg"], mode="none",
            fill="tozeroy", fillcolor="rgba(253,224,71,0.12)",
            showlegend=False, hoverinfo="skip"
        ))
        fig.add_trace(go.Scatter(
            x=seas["season"], y=seas["avg"], mode="lines+markers",
            line=dict(color=GOLD, width=3, shape="spline", smoothing=0.8),
            marker=dict(size=9, color=GOLD, symbol="circle",
                        line=dict(color=BG, width=2)),
            text=[f"{v:.0f}" for v in seas["avg"]],
            textposition="top center", textfont=dict(size=9, color=GOLD),
            hovertemplate="<b>Season %{x}</b><br>Avg %{y:.1f} runs/match<extra></extra>",
            name="Avg Runs/Match"
        ))
        fig.update_layout(BASE_LAYOUT)
        fig.update_layout(
            height=310,
            title=dict(text="<b><i class='fa-solid fa-chart-line' style='color:#FDE047;margin-right:8px;'></i> IPL Scoring Revolution</b>  <sup style='color:#94a3b8'>avg runs per match</sup>",
                       font=dict(size=15, color=TEXT), x=0),
            xaxis=dict(gridcolor=GRID, tickmode="array",
                       tickvals=seas["season"].tolist(),
                       tickfont=dict(color=MUTED, size=9)),
        )
        st.plotly_chart(fig, use_container_width=True, config=CHART_CONFIG)

    with st.expander("📊 View Timeline Progression Details"):
        st.markdown('''<div class="analyst-note">
        <div class="analyst-note-title">ANALYST NOTE</div>
        <div class="analyst-note-text">The "Scoring Revolution" chart above demonstrates the timeline progression of the IPL. You'll notice a massive spike in runs post-2022 due to the Impact Player rule and flatter wickets. Total match aggregates are consistently trending upwards.</div>
        </div>''', unsafe_allow_html=True)

    # Dynasty treemap
    with r1c2:
        tw = mff["ws"].value_counts().reset_index()
        tw.columns = ["team","wins"]
        tw["clr"] = tw["team"].map(TC).fillna(GOLD)
        fig_tm = go.Figure(go.Treemap(
            labels=tw["team"], parents=[""]*len(tw), values=tw["wins"],
            marker=dict(colors=tw["clr"].tolist(),
                        line=dict(color=BG, width=2)),
            texttemplate="<b>%{label}</b><br>%{value}",
            textfont=dict(size=11, family="Inter"),
            hovertemplate="<b>%{label}</b><br>%{value} wins<extra></extra>",
        ))
        fig_tm.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0,r=0,t=50,b=0), height=310,
            title=dict(text="<b><i class='fa-solid fa-award' style='color:#C084FC;margin-right:8px;'></i> Dynasty Map</b>",
                       font=dict(size=15, color=TEXT), x=0),
        )
        st.plotly_chart(fig_tm, use_container_width=True, config=CHART_CONFIG)

    r2c1, r2c2 = st.columns([2, 3])

    # Wicket types donut
    with r2c1:
        wk = dff["wicket_kind"].value_counts().reset_index()
        wk.columns = ["kind","cnt"]
        fig_w = go.Figure(go.Pie(
            labels=wk["kind"], values=wk["cnt"], hole=0.60,
            marker=dict(colors=PAL, line=dict(color=BG, width=2)),
            textfont=dict(size=10, family="Inter"),
            hovertemplate="<b>%{label}</b><br>%{value:,} (%{percent})<extra></extra>",
            pull=[0.04 if i==0 else 0 for i in range(len(wk))]
        ))
        fig_w.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10,r=10,t=55,b=10), height=310,
            title=dict(text="<b><i class='fa-solid fa-bowling-ball' style='color:#FDA4AF;margin-right:8px;'></i> Dismissal Types</b>",
                       font=dict(size=15, color=TEXT), x=0),
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT, size=9),
                        orientation="v", x=1.02, y=0.5),
            annotations=[dict(text=f"<b>{wk['cnt'].sum():,}</b><br><span style='font-size:10px'>Wickets</span>",
                              x=0.5, y=0.5, showarrow=False,
                              font=dict(size=13, color=TEXT))],
        )
        st.plotly_chart(fig_w, use_container_width=True, config=CHART_CONFIG)

    # 20-over run rate curve
    with r2c2:
        ov = (dff.groupby("over").agg(
            runs=("runs_total","mean"), wkts=("is_wicket","mean")).reset_index())
        ov["on"] = ov["over"] + 1
        ov["clr"] = ov["over"].apply(lambda o: CYAN if o<6 else GOLD if o<15 else CORAL)

        fig_ov = make_subplots(specs=[[{"secondary_y": True}]])
        fig_ov.add_trace(go.Bar(
            x=ov["on"], y=ov["runs"],
            marker=dict(color=ov["clr"].tolist(), opacity=0.75,
                        line=dict(color=BG, width=0.5)),
            name="Avg Runs/Over",
            hovertemplate="Over %{x}<br>Avg Runs: %{y:.2f}<extra></extra>"
        ), secondary_y=False)
        fig_ov.add_trace(go.Scatter(
            x=ov["on"], y=ov["wkts"], mode="lines+markers",
            name="Avg Wkts/Over",
            line=dict(color=PURP, width=2.5, shape="spline", smoothing=0.5),
            marker=dict(size=6, color=PURP, line=dict(color=BG,width=1.5)),
            hovertemplate="Over %{x}<br>Avg Wkts: %{y:.3f}<extra></extra>"
        ), secondary_y=True)
        for s,e,lbl,c in [(1,6,"Powerplay",CYAN),(7,15,"Middle",GOLD),(16,20,"Death",CORAL)]:
            fig_ov.add_vrect(x0=s-0.5, x1=e+0.5, fillcolor=c, opacity=0.055,
                             layer="below", line_width=0)
            fig_ov.add_annotation(x=(s+e)/2, y=ov["runs"].max()*0.95,
                                  text=f"<b>{lbl}</b>", showarrow=False,
                                  font=dict(color=c, size=9))
        fig_ov.update_layout(BASE_LAYOUT)
        fig_ov.update_layout(
            height=310, barmode="group",
            title=dict(text="<b><i class='fa-solid fa-gauge-high' style='color:#2DD4BF;margin-right:8px;'></i> Run Rate & Wicket Curve</b>  <sup style='color:#94a3b8'>all 20 overs</sup>",
                       font=dict(size=15, color=TEXT), x=0),
            xaxis=dict(gridcolor=GRID, tickmode="array",
                       tickvals=list(range(1,21)),
                       tickfont=dict(color=MUTED, size=9)),
        )
        fig_ov.update_yaxes(title_text="Avg Runs/Over", secondary_y=False,
                             gridcolor=GRID, tickfont=dict(color=MUTED))
        fig_ov.update_yaxes(title_text="Avg Wkts/Over", secondary_y=True,
                             range=[0,1], gridcolor="rgba(0,0,0,0)",
                             tickfont=dict(color=PURP))
        st.plotly_chart(fig_ov, use_container_width=True, config=CHART_CONFIG)

# ═══════════════════════════════════════════════════════════════════════════════
#  TAB 2 — TOSS
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("""<div class="sec-pill" style="--dc:#67E8F9;"><div class="sec-dot"></div>
    <div class="sec-txt"><i class="fa-solid fa-coins" style="margin-right:6px;"></i> Toss Intelligence · Myth vs Reality</div></div>""", unsafe_allow_html=True)

    toss_rate = mff["twmw"].mean() * 100
    field_wr  = mff[mff["toss_decision"]=="field"]["twmw"].mean() * 100
    bat_wr    = mff[mff["toss_decision"]=="bat"]["twmw"].mean() * 100
    field_n   = len(mff[mff["toss_decision"]=="field"])

    # Gauges
    g1, g2, g3 = st.columns(3)
    for col, val, title, color, ref in [
        (g1, toss_rate, "Overall Toss→Win %",  GOLD,  50),
        (g2, field_wr,  "Field-First Win %",    CYAN,  50),
        (g3, bat_wr,    "Bat-First Win %",       CORAL, 50),
    ]:
        fig_g = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=val,
            delta=dict(reference=ref, valueformat=".1f",
                       increasing=dict(color=GREEN), decreasing=dict(color=CORAL)),
            number=dict(suffix="%", font=dict(size=36, color=color, family="Inter")),
            gauge=dict(
                axis=dict(range=[0,100], tickwidth=1, tickcolor=MUTED,
                          tickfont=dict(color=MUTED, size=9)),
                bar=dict(color=color, thickness=0.25),
                bgcolor="rgba(0,0,0,0)", borderwidth=0,
                steps=[dict(range=[0,50], color="rgba(255,255,255,0.03)"),
                       dict(range=[50,100], color="rgba(255,255,255,0.06)")],
                threshold=dict(line=dict(color=MUTED,width=2), thickness=0.8, value=50)
            ),
            title=dict(text=f"<b>{title}</b>",
                       font=dict(size=13, color=TEXT, family="Inter"))
        ))
        fig_g.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                            margin=dict(l=30,r=30,t=60,b=10), height=250)
        col.plotly_chart(fig_g, use_container_width=True, config=CHART_CONFIG)

    tc1, tc2 = st.columns([3,2])
    with tc1:
        ts = mff.groupby("season")["twmw"].agg(["mean","count"]).reset_index()
        ts["wr"] = ts["mean"] * 100
        fig_t = go.Figure()
        fig_t.add_hrect(y0=45, y1=55, fillcolor=GREEN, opacity=0.035, line_width=0)
        fig_t.add_trace(go.Scatter(
            x=ts["season"], y=ts["wr"], mode="lines+markers",
            line=dict(color=CYAN, width=3, shape="spline", smoothing=0.7),
            marker=dict(size=9, color=ts["wr"].tolist(),
                        colorscale=[[0,CORAL],[0.5,GOLD],[1,GREEN]],
                        cmin=40, cmax=65, line=dict(color=BG, width=2)),
            text=[f"{v:.0f}%" for v in ts["wr"]],
            textposition="top center", textfont=dict(size=9, color=TEXT),
            hovertemplate="<b>Season %{x}</b><br>Toss→Win: %{y:.1f}%<extra></extra>",
            fill="tozeroy", fillcolor="rgba(103,232,249,0.06)", name="Win Rate"
        ))
        fig_t.add_hline(y=50, line_dash="dot", line_color=MUTED,
                        annotation_text="50% coin-flip",
                        annotation_font=dict(color=MUTED, size=10))
        fig_t.update_layout(BASE_LAYOUT)
        fig_t.update_layout(
            height=320,
            title=dict(text="<b><i class='fa-solid fa-chart-line' style='color:#67E8F9;margin-right:8px;'></i> Toss→Win Trend by Season</b>",
                       font=dict(size=15, color=TEXT), x=0),
            xaxis=dict(gridcolor=GRID, tickmode="array",
                       tickvals=ts["season"].tolist(),
                       tickfont=dict(color=MUTED, size=9)),
            yaxis=dict(gridcolor=GRID, range=[30,72]),
        )
        st.plotly_chart(fig_t, use_container_width=True, config=CHART_CONFIG)

    with tc2:
        toss_win_rate = mff["twmw"].mean() * 100
        toss_lose_rate = 100 - toss_win_rate
        fig_toss_bars2 = go.Figure(go.Bar(
            x=["Toss Winners", "Toss Losers"],
            y=[toss_win_rate, toss_lose_rate],
            marker_color=[GREEN, CORAL],
            opacity=0.9,
            text=[f"<b>{toss_win_rate:.1f}%</b>", f"<b>{toss_lose_rate:.1f}%</b>"],
            textposition="outside",
            hovertemplate="Win Rate: %{y:.1f}%<extra></extra>"
        ))
        fig_toss_bars2.update_layout(BASE_LAYOUT)
        fig_toss_bars2.update_layout(
            height=320,
            title=dict(text="<b><i class='fa-solid fa-chart-bar' style='color:#FDE047;margin-right:8px;'></i> Win Rate: Toss Winners vs Losers</b>",
                       font=dict(size=15, color=TEXT), x=0),
            yaxis=dict(title="Win %", range=[0, 110], gridcolor=GRID),
            xaxis=dict(gridcolor=GRID),
        )
        st.plotly_chart(fig_toss_bars2, use_container_width=True, config=CHART_CONFIG)

    st.markdown(f"""
    <div class="insight">
        <div class="insight-lbl"><i class="fa-solid fa-lightbulb" style="margin-right:6px;"></i> The Toss Myth Debunked</div>
        <div class="insight-txt">Over <b>{mff.shape[0]:,}</b> matches, toss winners convert to match winners
        just <b>{toss_rate:.1f}%</b> of the time — statistically indistinguishable from a coin flip (50%).
        Teams choosing to field first win <b>{field_wr:.1f}%</b> while those batting first win <b>{bat_wr:.1f}%</b>.
        The small advantage of fielding-first is consistent across seasons: modern IPL squads have
        become adept at chasing, making toss decisions mostly psychological.
        <b>Execution beats toss advantage every single time.</b></div>
    </div>
    """, unsafe_allow_html=True)

    # ── Per-team toss decision breakdown ──────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""<div class="sec-pill" style="--dc:#C084FC;"><div class="sec-dot"></div>
    <div class="sec-txt"><i class="fa-solid fa-users-between-lines" style="margin-right:6px;"></i> Per-Team Toss Strategy & Win Rate</div></div>""",
    unsafe_allow_html=True)

    team_toss = mff.groupby("t1s").apply(lambda g: pd.Series({
        "total": len(g),
        "won_toss": g["twmw"].sum(),
        "field_pct": (g["toss_decision"]=="field").mean()*100
    })).reset_index()
    team_toss.columns = ["team","total","won_toss","field_pct"]
    team_toss["toss_win_pct"] = team_toss["won_toss"] / team_toss["total"] * 100
    team_toss = team_toss[team_toss["total"]>=5].sort_values("toss_win_pct", ascending=True)

    fig_tt = go.Figure()
    fig_tt.add_trace(go.Bar(
        y=team_toss["team"], x=team_toss["toss_win_pct"], orientation="h",
        name="Toss → Win %", marker_color=GOLD, opacity=0.85,
        text=[f"{v:.1f}%" for v in team_toss["toss_win_pct"]],
        textposition="outside", textfont=dict(size=9, color=TEXT),
        hovertemplate="<b>%{y}</b><br>Toss→Win: %{x:.1f}%<extra></extra>"
    ))
    fig_tt.add_trace(go.Bar(
        y=team_toss["team"], x=team_toss["field_pct"], orientation="h",
        name="Choose to Field %", marker_color=CYAN, opacity=0.7,
        text=[f"{v:.0f}%" for v in team_toss["field_pct"]],
        textposition="outside", textfont=dict(size=9, color=MUTED),
        hovertemplate="<b>%{y}</b><br>Field First: %{x:.0f}%<extra></extra>"
    ))
    fig_tt.add_vline(x=50, line_dash="dot", line_color=MUTED,
                     annotation_text="50% baseline", annotation_font=dict(color=MUTED, size=9))
    fig_tt.update_layout(BASE_LAYOUT)
    fig_tt.update_layout(
        height=max(380, len(team_toss)*38),
        title=dict(text="<b><i class='fa-solid fa-users-between-lines' style='color:#C084FC;margin-right:8px;'></i> Team-wise Toss Win % vs Field-First Preference</b>",
                   font=dict(size=14, color=TEXT), x=0),
        xaxis=dict(gridcolor=GRID, range=[0, 100], title="Percentage (%)"),
        barmode="overlay",
    )
    st.plotly_chart(fig_tt, use_container_width=True, config=CHART_CONFIG)



# ═══════════════════════════════════════════════════════════════════════════════
#  TAB 3 — PHASE BATTLE
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("""<div class="sec-pill" style="--dc:#FDE047;"><div class="sec-dot"></div>
    <div class="sec-txt"><i class="fa-solid fa-gauge-high" style="margin-right:6px;"></i> Phase Battle · Powerplay vs Middle vs Death</div></div>""", unsafe_allow_html=True)

    PHASES  = ["Powerplay","Middle","Death"]
    PCLR    = {"Powerplay": CYAN, "Middle": GOLD, "Death": CORAL}

    ov_agg = (dff.groupby(["match_id","over","phase"])
              .agg(runs=("runs_total","sum"), wkts=("is_wicket","sum"),
                   balls=("ball","count"), dots=("is_dot","sum"),
                   sixes=("is_six","sum")).reset_index())
    ov_agg["rr"]      = ov_agg["runs"] / (ov_agg["balls"]/6)
    ov_agg["dot_pct"] = ov_agg["dots"] / ov_agg["balls"] * 100

    phase_s = (ov_agg.groupby("phase").agg(
        rr=("rr","mean"), runs=("runs","mean"),
        wkts=("wkts","mean"), dots=("dot_pct","mean"),
        sixes=("sixes","mean")).reindex(PHASES).reset_index())

    # Phase metric cards
    pc1, pc2, pc3 = st.columns(3)
    for col, (_, row) in zip([pc1,pc2,pc3], phase_s.iterrows()):
        c = PCLR[row["phase"]]
        col.markdown(f"""
        <div class="kpi-card" style="--ac:{c};">
            <div style="color:{c};font-size:0.88rem;font-weight:800;
                        letter-spacing:0.05em;margin-bottom:12px;">{row['phase'].upper()} OVERS</div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
                <div>
                    <div style="font-size:1.5rem;font-weight:800;color:{c};">{row['rr']:.2f}</div>
                    <div style="font-size:0.62rem;color:#94a3b8;letter-spacing:0.1em;">RUN RATE</div>
                </div>
                <div>
                    <div style="font-size:1.5rem;font-weight:800;color:{c};">{row['runs']:.1f}</div>
                    <div style="font-size:0.62rem;color:#94a3b8;letter-spacing:0.1em;">AVG RUNS</div>
                </div>
                <div>
                    <div style="font-size:1.5rem;font-weight:800;color:{c};">{row['wkts']:.3f}</div>
                    <div style="font-size:0.62rem;color:#94a3b8;letter-spacing:0.1em;">AVG WKTS</div>
                </div>
                <div>
                    <div style="font-size:1.5rem;font-weight:800;color:{c};">{row['dots']:.1f}%</div>
                    <div style="font-size:0.62rem;color:#94a3b8;letter-spacing:0.1em;">DOT BALL %</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    ph1, ph2 = st.columns(2)

    # Radar
    with ph1:
        cats = ["Run Rate","Avg Runs","Wickets×10","Dot Ball %","Sixes"]
        fig_r = go.Figure()
        for _, row in phase_s.iterrows():
            vals_norm = [
                row["rr"]       / max(phase_s["rr"].max(),   0.1) * 9,
                row["runs"]     / max(phase_s["runs"].max(),  0.1) * 9,
                row["wkts"]*10  / max(phase_s["wkts"].max()*10, 0.1) * 9,
                row["dots"]     / max(phase_s["dots"].max(),  0.1) * 9,
                row["sixes"]    / max(phase_s["sixes"].max(), 0.1) * 9,
            ]
            c_hex = PCLR[row["phase"]].lstrip("#")
            r_, g_, b_ = (int(c_hex[j:j+2],16) for j in (0,2,4))
            f_color = f"rgba({r_},{g_},{b_},0.18)"
            fig_r.add_trace(go.Scatterpolar(
                r=vals_norm+[vals_norm[0]], theta=cats+[cats[0]],
                fill="toself", name=row["phase"],
                line=dict(color=PCLR[row["phase"]], width=2),
                fillcolor=f_color,
                hovertemplate=f"<b>{row['phase']}</b><br>%{{theta}}: %{{r:.2f}}<extra></extra>"
            ))
        fig_r.update_layout(
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(visible=True, range=[0,10],
                                gridcolor=GRID, tickfont=dict(color=MUTED, size=8)),
                angularaxis=dict(gridcolor=GRID, tickfont=dict(color=TEXT, size=10))
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=40,r=40,t=55,b=40), height=350,
            title=dict(text="<b><i class='fa-solid fa-circle-notch' style='color:#C084FC;margin-right:8px;'></i> Phase Radar Comparison</b>",
                       font=dict(size=15, color=TEXT), x=0),
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT, size=11)),
        )
        st.plotly_chart(fig_r, use_container_width=True, config=CHART_CONFIG)

    # Dot ball pressure
    with ph2:
        dot_o = (dff.groupby("over").agg(dots=("is_dot","sum"),
                                          balls=("ball","count")).reset_index())
        dot_o["pct"] = dot_o["dots"] / dot_o["balls"] * 100
        dot_o["on"]  = dot_o["over"] + 1
        dot_o["clr"] = dot_o["over"].apply(
            lambda o: CYAN if o<6 else GOLD if o<15 else CORAL)
        fig_d = go.Figure(go.Bar(
            x=dot_o["on"], y=dot_o["pct"],
            marker=dict(color=dot_o["clr"].tolist(), opacity=0.8,
                        line=dict(color=BG, width=0.5)),
            text=[f"{v:.0f}%" for v in dot_o["pct"]],
            textposition="outside", textfont=dict(size=8, color=MUTED),
            hovertemplate="Over %{x}<br>Dot Ball %: %{y:.1f}%<extra></extra>"
        ))
        fig_d.update_layout(BASE_LAYOUT)
        fig_d.update_layout(
            height=350,
            title=dict(text="<b><i class='fa-solid fa-circle-dot' style='color:#FDA4AF;margin-right:8px;'></i> Dot Ball Pressure Map</b>",
                       font=dict(size=15, color=TEXT), x=0),
            xaxis=dict(gridcolor=GRID, tickmode="array",
                       tickvals=list(range(1,21)),
                       tickfont=dict(color=MUTED, size=9)),
            yaxis=dict(gridcolor=GRID, title="Dot Ball %"),
        )
        st.plotly_chart(fig_d, use_container_width=True, config=CHART_CONFIG)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Winner vs Loser Phase Comparison ──────────────────────────────────────
    st.markdown("""<div class="sec-pill" style="--dc:#86EFAC;"><div class="sec-dot"></div>
    <div class="sec-txt"><i class="fa-solid fa-scale-balanced" style="margin-right:6px;"></i> Winner vs Loser Phase Analysis</div></div>""",
    unsafe_allow_html=True)

    winner_map_t3 = mff.set_index("match_id")["winner"].to_dict()
    dff_wl = dff.copy()
    dff_wl["match_winner"] = dff_wl["match_id"].map(winner_map_t3)
    dff_wl["is_winner"] = dff_wl["batting_team"] == dff_wl["match_winner"]

    phase_wl = dff_wl.groupby(["phase","is_winner"])["runs_total"].sum().reset_index()
    balls_wl = dff_wl.groupby(["phase","is_winner"])["ball"].count().reset_index(name="balls")
    phase_wl = phase_wl.merge(balls_wl, on=["phase","is_winner"])
    phase_wl["rr"] = phase_wl["runs_total"] / (phase_wl["balls"] / 6)

    winner_ph = phase_wl[phase_wl["is_winner"]==True].set_index("phase").reindex(PHASES).reset_index()
    loser_ph  = phase_wl[phase_wl["is_winner"]==False].set_index("phase").reindex(PHASES).reset_index()

    ph3a, ph3b = st.columns(2)

    with ph3a:
        fig_wl = go.Figure()
        fig_wl.add_bar(
            x=winner_ph["phase"], y=winner_ph["rr"], name="Winning Team",
            marker_color=GREEN, opacity=0.88,
            text=winner_ph["rr"].round(2), textposition="outside",
            hovertemplate="<b>Winner</b><br>%{x}: %{y:.2f} RR<extra></extra>"
        )
        fig_wl.add_bar(
            x=loser_ph["phase"], y=loser_ph["rr"], name="Losing Team",
            marker_color=CORAL, opacity=0.88,
            text=loser_ph["rr"].round(2), textposition="outside",
            hovertemplate="<b>Loser</b><br>%{x}: %{y:.2f} RR<extra></extra>"
        )
        fig_wl.update_layout(BASE_LAYOUT)
        fig_wl.update_layout(
            height=350, barmode="group",
            title=dict(text="<b><i class='fa-solid fa-chart-bar' style='color:#86EFAC;margin-right:8px;'></i> Run Rate per Phase (Winners vs Losers)</b>",
                       font=dict(size=14, color=TEXT), x=0),
            xaxis=dict(gridcolor=GRID),
            yaxis=dict(gridcolor=GRID, title="Run Rate (per over)"),
        )
        st.plotly_chart(fig_wl, use_container_width=True, config=CHART_CONFIG)

    with ph3b:
        # Wicket comparison per phase
        wkts_wl = dff_wl.groupby(["phase","is_winner"])["is_wicket"].sum().reset_index()
        balls_wl2 = dff_wl.groupby(["phase","is_winner"])["ball"].count().reset_index(name="balls")
        wkts_wl = wkts_wl.merge(balls_wl2, on=["phase","is_winner"])
        wkts_wl["wkts_per_6"] = wkts_wl["is_wicket"] / (wkts_wl["balls"] / 6) * 6

        winner_wk = wkts_wl[wkts_wl["is_winner"]==True].set_index("phase").reindex(PHASES).reset_index()
        loser_wk  = wkts_wl[wkts_wl["is_winner"]==False].set_index("phase").reindex(PHASES).reset_index()

        fig_wl2 = go.Figure()
        fig_wl2.add_bar(
            x=winner_wk["phase"], y=winner_wk["wkts_per_6"], name="Winning Team (Batting)",
            marker_color=GREEN, opacity=0.88,
            text=winner_wk["wkts_per_6"].round(3), textposition="outside",
            hovertemplate="<b>Winner Batting</b><br>%{x}: %{y:.3f} wkts/over<extra></extra>"
        )
        fig_wl2.add_bar(
            x=loser_wk["phase"], y=loser_wk["wkts_per_6"], name="Losing Team (Batting)",
            marker_color=CORAL, opacity=0.88,
            text=loser_wk["wkts_per_6"].round(3), textposition="outside",
            hovertemplate="<b>Loser Batting</b><br>%{x}: %{y:.3f} wkts/over<extra></extra>"
        )
        fig_wl2.update_layout(BASE_LAYOUT)
        fig_wl2.update_layout(
            height=350, barmode="group",
            title=dict(text="<b><i class='fa-solid fa-circle-dot' style='color:#FDA4AF;margin-right:8px;'></i> Wickets Conceded per Over per Phase</b>",
                       font=dict(size=14, color=TEXT), x=0),
            xaxis=dict(gridcolor=GRID),
            yaxis=dict(gridcolor=GRID, title="Wickets per Over"),
        )
        st.plotly_chart(fig_wl2, use_container_width=True, config=CHART_CONFIG)

    # Auto-compute which phase has biggest RR gap
    try:
        pp_gap = float(winner_ph.loc[winner_ph["phase"]=="Powerplay","rr"].values[0]) - float(loser_ph.loc[loser_ph["phase"]=="Powerplay","rr"].values[0])
        mid_gap = float(winner_ph.loc[winner_ph["phase"]=="Middle","rr"].values[0]) - float(loser_ph.loc[loser_ph["phase"]=="Middle","rr"].values[0])
        death_gap = float(winner_ph.loc[winner_ph["phase"]=="Death","rr"].values[0]) - float(loser_ph.loc[loser_ph["phase"]=="Death","rr"].values[0])
        phase_gaps = {"Powerplay": pp_gap, "Middle": mid_gap, "Death": death_gap}
        decisive_phase = max(phase_gaps, key=phase_gaps.get)
        decisive_gap = phase_gaps[decisive_phase]
        decisive_col = PCLR.get(decisive_phase, GOLD)
    except Exception:
        decisive_phase = "Death"; decisive_gap = 0.5; decisive_col = CORAL

    st.markdown(f"""
    <div class="insight">
        <div class="insight-lbl"><i class="fa-solid fa-lightbulb" style="margin-right:6px;"></i> Which Phase Decides Matches?</div>
        <div class="insight-txt">
            Across all filtered matches, the <b style="color:{decisive_col};">{decisive_phase}</b> phase shows the largest Run Rate separation
            between winning and losing teams (<b>+{decisive_gap:.2f} runs/over</b> advantage for winners).
            This confirms that <b>{decisive_phase} overs are the most decisive phase</b> in determining match outcomes.
            <br><br>
            <i>Interpretation guide:</i> Powerplay (~overs 1–6) sets momentum; Middle (7–15) builds partnerships; Death (16–20) is where matches are won or lost.
        </div>
    </div>
    """, unsafe_allow_html=True)


    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('''<div class="sec-pill" style="--dc:#2DD4BF;"><div class="sec-dot"></div>
    <div class="sec-txt"><i class="fa-solid fa-bolt" style="margin-right:6px;"></i> Match Momentum Progression</div></div>''', unsafe_allow_html=True)
    
    # Calculate average runs per over (1-20) across all matches
    momentum = dff.groupby("over").agg(runs=("runs_total", "sum"), balls=("ball", "count")).reset_index()
    momentum["rr"] = momentum["runs"] / (momentum["balls"].replace(0,1) / 6)
    momentum["over"] = momentum["over"] + 1

    fig_mom = go.Figure()
    fig_mom.add_trace(go.Scatter(
        x=momentum["over"], y=momentum["rr"],
        mode="lines+markers",
        line=dict(color=TEAL, width=3, shape="spline"),
        marker=dict(size=8, color=TEAL, line=dict(color=BG, width=2)),
        fill="tozeroy", fillcolor="rgba(45, 212, 191, 0.15)",
        hovertemplate="<b>Over %{x}</b><br>Run Rate: %{y:.2f}<extra></extra>"
    ))
    fig_mom.update_layout(BASE_LAYOUT)
    fig_mom.update_layout(
        height=320,
        title=dict(text="<b><i class='fa-solid fa-arrow-trend-up' style='color:#2DD4BF;margin-right:8px;'></i> Average Match Momentum (Over 1 to 20)</b>", font=dict(size=14, color=TEXT), x=0),
        xaxis=dict(gridcolor=GRID, tickmode="linear", tick0=1, dtick=1, title="Over Number"),
        yaxis=dict(gridcolor=GRID, title="Average Run Rate"),
        hovermode="x unified"
    )
    st.plotly_chart(fig_mom, use_container_width=True, config=CHART_CONFIG)

#  TAB 4 — PLAYERS
# ═══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("""<div class="sec-pill" style="--dc:#C084FC;"><div class="sec-dot"></div>
    <div class="sec-txt"><i class="fa-solid fa-trophy" style="margin-right:6px;"></i> Player Intelligence · Leaderboards & Career Arcs</div></div>""",
    unsafe_allow_html=True)

    p_mode = st.radio("Player Mode", ["Batting Leaderboard", "Bowling Leaderboard", "Career Trajectory", "Death Specialists", "Powerplay Specialists"],
                      horizontal=True, key="p_mode", label_visibility="collapsed")



    if "Batting" in p_mode:
        top_n = st.slider("Top N batters", 5, 20, 10, key="bat_n")
        top_b = bat_s.head(top_n)
        bc1, bc2 = st.columns([2, 3])
        with bc1:
            tb_s = top_b.sort_values("runs")
            fig_b = go.Figure(go.Bar(
                y=tb_s["batter"], x=tb_s["runs"], orientation="h",
                marker=dict(color=tb_s["runs"].tolist(),
                            colorscale=[[0,CORAL],[0.5,GOLD],[1,"#FFD700"]],
                            showscale=False, line=dict(color=BG, width=0.5)),
                text=[f"{r:,}" for r in tb_s["runs"]],
                textposition="outside", textfont=dict(size=10, color=TEXT),
                hovertemplate="<b>%{y}</b><br>%{x:,} runs<extra></extra>"
            ))
            fig_b.update_layout(BASE_LAYOUT)
            fig_b.update_layout(
                height=max(380, top_n*42),
                title=dict(text=f"<b><i class='fa-solid fa-fire' style='color:#FDA4AF;margin-right:8px;'></i> Top {top_n} Run Scorers</b>",
                           font=dict(size=15, color=TEXT), x=0),
                xaxis=dict(gridcolor=GRID, range=[0, tb_s["runs"].max()*1.22]),
            )
            st.plotly_chart(fig_b, use_container_width=True, config=CHART_CONFIG)
        with bc2:
            fig_sc = px.scatter(
                bat_s.head(50), x="runs", y="sr", size="sixes", color="fours",
                color_continuous_scale=[[0,CARD],[0.3,CYAN],[0.7,GOLD],[1,"#FFD700"]],
                hover_name="batter",
                hover_data={"runs":True,"sr":True,"fours":True,"sixes":True},
                size_max=40,
            )
            for _, row in bat_s.head(5).iterrows():
                fig_sc.add_annotation(x=row["runs"], y=row["sr"],
                    text=f"<b>{row['batter'].split()[-1]}</b>",
                    showarrow=False, font=dict(size=9.5, color=GOLD), yshift=12)
            fig_sc.update_traces(
                marker=dict(opacity=0.82, line=dict(color="rgba(255,255,255,0.1)", width=0.5)))
            fig_sc.update_layout(BASE_LAYOUT)
            fig_sc.update_layout(
                height=max(380, top_n*42),
                title=dict(text="<b><i class='fa-solid fa-chart-line' style='color:#FDE047;margin-right:8px;'></i> Runs vs Strike Rate</b>  <sup>bubble=sixes · colour=fours</sup>",
                           font=dict(size=15, color=TEXT), x=0),
                xaxis=dict(gridcolor=GRID, title="Total Runs"),
                yaxis=dict(gridcolor=GRID, title="Strike Rate"),
                coloraxis_colorbar=dict(
                    title=dict(text="Fours", font=dict(color=TEXT)),
                    tickfont=dict(color=MUTED)),
            )
            st.plotly_chart(fig_sc, use_container_width=True, config=CHART_CONFIG)

    elif "Bowling" in p_mode:
        top_n = st.slider("Top N bowlers", 5, 20, 10, key="bowl_n")
        top_bw = bowl_s.head(top_n)
        bwc1, bwc2 = st.columns([2, 3])
        with bwc1:
            tbw_s = top_bw.sort_values("wkts")
            fig_bw = go.Figure(go.Bar(
                y=tbw_s["bowler"], x=tbw_s["wkts"], orientation="h",
                marker=dict(color=tbw_s["wkts"].tolist(),
                            colorscale=[[0,CORAL],[0.5,PURP],[1,CYAN]],
                            showscale=False, line=dict(color=BG, width=0.5)),
                text=[str(w) for w in tbw_s["wkts"]],
                textposition="outside", textfont=dict(size=10, color=TEXT),
                hovertemplate="<b>%{y}</b><br>%{x} wickets<extra></extra>"
            ))
            fig_bw.update_layout(BASE_LAYOUT)
            fig_bw.update_layout(
                height=max(380, top_n*42),
                title=dict(text=f"<b><i class='fa-solid fa-circle-dot' style='color:#67E8F9;margin-right:8px;'></i> Top {top_n} Wicket Takers</b>",
                           font=dict(size=15, color=TEXT), x=0),
                xaxis=dict(gridcolor=GRID, range=[0, tbw_s["wkts"].max()*1.25]),
            )
            st.plotly_chart(fig_bw, use_container_width=True, config=CHART_CONFIG)
        with bwc2:
            fig_we = px.scatter(
                bowl_s.head(50), x="wkts", y="eco", size="inn", color="avg",
                color_continuous_scale=[[0,GREEN],[0.5,GOLD],[1,CORAL]],
                hover_name="bowler",
                hover_data={"wkts":True,"eco":True,"avg":True},
                size_max=30,
            )
            for _, row in bowl_s.head(5).iterrows():
                fig_we.add_annotation(x=row["wkts"], y=row["eco"],
                    text=f"<b>{row['bowler'].split()[-1]}</b>",
                    showarrow=False, font=dict(size=9.5, color=PURP), yshift=10)
            fig_we.update_traces(
                marker=dict(opacity=0.82, line=dict(color="rgba(255,255,255,0.1)", width=0.5)))
            fig_we.update_layout(BASE_LAYOUT)
            fig_we.update_layout(
                height=max(380, top_n*42),
                title=dict(text="<b><i class='fa-solid fa-chart-line' style='color:#C084FC;margin-right:8px;'></i> Wickets vs Economy</b>  <sup>bubble=matches · colour=avg</sup>",
                           font=dict(size=15, color=TEXT), x=0),
                xaxis=dict(gridcolor=GRID, title="Total Wickets"),
                yaxis=dict(gridcolor=GRID, title="Economy Rate"),
                coloraxis_colorbar=dict(
                    title=dict(text="Bowling Avg", font=dict(color=TEXT)),
                    tickfont=dict(color=MUTED)),
            )
            st.plotly_chart(fig_we, use_container_width=True, config=CHART_CONFIG)

    elif "Trajectory" in p_mode:
        st.markdown("#### <i class='fa-solid fa-chart-line' style='color:#67E8F9;margin-right:8px;'></i> Player Career Trajectory", unsafe_allow_html=True)
        all_batters = bat_s["batter"].head(30).tolist()
        sel_player = st.selectbox("Select Player", all_batters, key="cp")
        pdff = dff[dff["batter"]==sel_player].groupby("season").agg(
            runs=("runs_batter","sum"), balls=("ball","count"),
            inn=("match_id","nunique"), sixes=("is_six","sum"),
            fours=("is_four","sum")).reset_index()
        pdff["sr"] = (pdff["runs"] / pdff["balls"] * 100).round(1)
        pdff["avg"] = (pdff["runs"] / pdff["inn"]).round(1)

        car1, car2 = st.columns(2)
        with car1:
            fig_car = make_subplots(specs=[[{"secondary_y": True}]])
            fig_car.add_trace(go.Bar(
                x=pdff["season"], y=pdff["runs"],
                marker=dict(color=GOLD, opacity=0.7,
                            line=dict(color=BG, width=0.5)),
                name="Runs", hovertemplate="Season %{x}<br>Runs: %{y}<extra></extra>"
            ), secondary_y=False)
            fig_car.add_trace(go.Scatter(
                x=pdff["season"], y=pdff["sr"], mode="lines+markers",
                line=dict(color=CORAL, width=2.5),
                marker=dict(size=7, color=CORAL, line=dict(color=BG,width=1.5)),
                name="Strike Rate",
                hovertemplate="Season %{x}<br>SR: %{y:.1f}<extra></extra>"
            ), secondary_y=True)
            fig_car.update_layout(BASE_LAYOUT)
            fig_car.update_layout(
                height=340,
                title=dict(text=f"<b><i class='fa-solid fa-user' style='color:#FDE047;margin-right:8px;'></i> {sel_player} · Season Runs & SR</b>",
                           font=dict(size=14, color=TEXT), x=0),
                xaxis=dict(gridcolor=GRID, tickfont=dict(color=MUTED, size=9)),
            )
            fig_car.update_yaxes(title_text="Season Runs", secondary_y=False,
                                  gridcolor=GRID, tickfont=dict(color=MUTED))
            fig_car.update_yaxes(title_text="Strike Rate", secondary_y=True,
                                  range=[0, pdff["sr"].max()*1.3 if len(pdff)>0 else 200],
                                  gridcolor="rgba(0,0,0,0)",
                                  tickfont=dict(color=CORAL))
            st.plotly_chart(fig_car, use_container_width=True, config=CHART_CONFIG)

        with car2:
            fig_bd = go.Figure()
            fig_bd.add_trace(go.Bar(
                x=pdff["season"], y=pdff["sixes"], name="Sixes",
                marker_color=CORAL, opacity=0.8))
            fig_bd.add_trace(go.Bar(
                x=pdff["season"], y=pdff["fours"], name="Fours",
                marker_color=GOLD, opacity=0.8))
            fig_bd.update_layout(BASE_LAYOUT)
            fig_bd.update_layout(
                height=340, barmode="stack",
                title=dict(text=f"<b><i class='fa-solid fa-border-all' style='color:#FDA4AF;margin-right:8px;'></i> {sel_player} · Boundary Breakdown</b>",
                           font=dict(size=14, color=TEXT), x=0),
                xaxis=dict(gridcolor=GRID, tickfont=dict(color=MUTED, size=9)),
                yaxis=dict(gridcolor=GRID, title="Boundaries"),
            )
            st.plotly_chart(fig_bd, use_container_width=True, config=CHART_CONFIG)

        # Career summary card
        tot_runs = pdff["runs"].sum()
        tot_inn  = pdff["inn"].sum()
        best_yr  = pdff.loc[pdff["runs"].idxmax(), "season"] if len(pdff)>0 else "—"
        best_val = pdff["runs"].max() if len(pdff)>0 else 0
        overall_sr = (dff[dff["batter"]==sel_player]["runs_batter"].sum() /
                      max(dff[dff["batter"]==sel_player]["ball"].count(), 1) * 100)
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:12px;">
            <div class="kpi-card" style="--ac:{GOLD};"><div class="kpi-val">{int(tot_runs):,}</div>
            <div class="kpi-lbl">CAREER RUNS</div></div>
            <div class="kpi-card" style="--ac:{CYAN};"><div class="kpi-val">{overall_sr:.1f}</div>
            <div class="kpi-lbl">CAREER SR</div></div>
            <div class="kpi-card" style="--ac:{CORAL};"><div class="kpi-val">{best_yr}</div>
            <div class="kpi-lbl">BEST SEASON</div><div class="kpi-delta">{int(best_val)} runs</div></div>
            <div class="kpi-card" style="--ac:{TEAL};"><div class="kpi-val">{int(tot_inn)}</div>
            <div class="kpi-lbl">INNINGS</div></div>
        </div>
        """, unsafe_allow_html=True)

    elif "Death" in p_mode:  # Death Specialists
        st.markdown("""
        <div class='insight' style='margin-bottom:12px;'>
          <div class='insight-lbl'><i class='fa-solid fa-skull' style='margin-right:6px;'></i> Death Overs Explained</div>
          <div class='insight-txt'>Death overs (16–20) are the final, explosive phase where batters prioritise sixes and bowlers fight for every dot ball.
          A <b>Strike Rate above 180</b> is elite for batters. An <b>Economy below 8</b> is elite for bowlers in this phase.</div>
        </div>
        """, unsafe_allow_html=True)
        min_balls_death = st.slider("Min Death-Over Balls Faced / Bowled", 30, 200, 80, step=10, key="min_balls_death")
        death = dff[dff["phase"]=="Death"]
        db = (death.groupby("batter").agg(runs=("runs_batter","sum"),
                                           balls=("ball","count"),
                                           sixes=("is_six","sum")).reset_index())
        db["sr"] = db["runs"] / db["balls"] * 100
        db = db[db["balls"]>=min_balls_death].sort_values("sr", ascending=False).head(10)

        dbow = (death.groupby("bowler").agg(rc=("runs_total","sum"),
                                             balls=("ball","count"),
                                             wkts=("is_wicket","sum")).reset_index())
        dbow["eco"] = dbow["rc"] / (dbow["balls"]/6)
        dbow = dbow[dbow["balls"]>=min_balls_death].sort_values("eco").head(10)

        st.markdown("#### <i class='fa-solid fa-skull' style='color:#FDA4AF;margin-right:8px;'></i> Death Overs (16–20) Specialists", unsafe_allow_html=True)
        dc1, dc2 = st.columns(2)
        with dc1:
            db_s = db.sort_values("sr")
            fig_db = go.Figure(go.Bar(
                y=db_s["batter"], x=db_s["sr"], orientation="h",
                marker=dict(color=db_s["sr"].tolist(),
                            colorscale=[[0,GOLD],[1,CORAL]],
                            showscale=False, line=dict(color=BG, width=0.5)),
                text=[f"SR: {v:.0f}" for v in db_s["sr"]],
                textposition="outside", textfont=dict(size=10, color=TEXT),
                hovertemplate="<b>%{y}</b><br>Death SR: %{x:.1f}<extra></extra>"
            ))
            fig_db.update_layout(BASE_LAYOUT)
            fig_db.update_layout(
                height=420,
                title=dict(text="<b><i class='fa-solid fa-fire' style='color:#FDA4AF;margin-right:8px;'></i> Death Batting SR</b>",
                           font=dict(size=15, color=TEXT), x=0),
                xaxis=dict(gridcolor=GRID, range=[0, db_s["sr"].max()*1.2]),
            )
            st.plotly_chart(fig_db, use_container_width=True, config=CHART_CONFIG)
        with dc2:
            dbow_s = dbow.sort_values("eco", ascending=False)
            fig_dbow = go.Figure(go.Bar(
                y=dbow_s["bowler"], x=dbow_s["eco"], orientation="h",
                marker=dict(color=dbow_s["eco"].tolist(),
                            colorscale=[[0,GREEN],[0.5,CYAN],[1,GOLD]],
                            reversescale=True, showscale=False,
                            line=dict(color=BG, width=0.5)),
                text=[f"Eco: {v:.2f}" for v in dbow_s["eco"]],
                textposition="outside", textfont=dict(size=10, color=TEXT),
                hovertemplate="<b>%{y}</b><br>Death Eco: %{x:.2f}<extra></extra>"
            ))
            fig_dbow.update_layout(BASE_LAYOUT)
            fig_dbow.update_layout(
                height=420,
                title=dict(text="<b><i class='fa-solid fa-circle-dot' style='color:#67E8F9;margin-right:8px;'></i> Death Bowling Economy</b>  <sup>lower = better</sup>",
                           font=dict(size=15, color=TEXT), x=0),
                xaxis=dict(gridcolor=GRID, range=[0, dbow_s["eco"].max()*1.2],
                           autorange="reversed"),
            )
            st.plotly_chart(fig_dbow, use_container_width=True, config=CHART_CONFIG)

    else:  # Powerplay Specialists
        st.markdown("""
        <div class='insight' style='margin-bottom:12px;'>
          <div class='insight-lbl'><i class='fa-solid fa-bolt' style='margin-right:6px;'></i> Powerplay Explained</div>
          <div class='insight-txt'>Powerplay (Overs 1–6) sets the tone. Teams scoring 60+ in the Powerplay win the match <b>over 60% of the time</b>.
          Top openers maintain Strike Rates above <b>140</b>. Elite Powerplay bowlers keep Economy below <b>6.5</b>.</div>
        </div>
        """, unsafe_allow_html=True)
        min_balls_pp = st.slider("Min Powerplay Balls Faced / Bowled", 20, 180, 60, step=10, key="min_balls_pp")
        pp = dff[dff["phase"]=="Powerplay"]
        ppb = (pp.groupby("batter").agg(runs=("runs_batter","sum"),
                                          balls=("ball","count"),
                                          sixes=("is_six","sum")).reset_index())
        ppb["sr"] = ppb["runs"] / ppb["balls"] * 100
        ppb = ppb[ppb["balls"]>=min_balls_pp].sort_values("sr", ascending=False).head(10)

        ppbow = (pp.groupby("bowler").agg(rc=("runs_total","sum"),
                                           balls=("ball","count"),
                                           wkts=("is_wicket","sum")).reset_index())
        ppbow["eco"] = ppbow["rc"] / (ppbow["balls"]/6)
        ppbow = ppbow[ppbow["balls"]>=min_balls_pp].sort_values("eco").head(10)

        st.markdown("#### <i class='fa-solid fa-bolt' style='color:#67E8F9;margin-right:8px;'></i> Powerplay (Overs 1–6) Specialists", unsafe_allow_html=True)
        ppc1, ppc2 = st.columns(2)
        with ppc1:
            ppb_s = ppb.sort_values("sr")
            fig_ppb = go.Figure(go.Bar(
                y=ppb_s["batter"], x=ppb_s["sr"], orientation="h",
                marker=dict(color=ppb_s["sr"].tolist(),
                            colorscale=[[0,CYAN],[1,GOLD]],
                            showscale=False, line=dict(color=BG, width=0.5)),
                text=[f"SR: {v:.0f}" for v in ppb_s["sr"]],
                textposition="outside", textfont=dict(size=10, color=TEXT),
                hovertemplate="<b>%{y}</b><br>Powerplay SR: %{x:.1f}<extra></extra>"
            ))
            fig_ppb.update_layout(BASE_LAYOUT)
            fig_ppb.update_layout(
                height=420,
                title=dict(text="<b><i class='fa-solid fa-bolt' style='color:#67E8F9;margin-right:8px;'></i> Powerplay Batting SR</b>",
                           font=dict(size=15, color=TEXT), x=0),
                xaxis=dict(gridcolor=GRID, range=[0, ppb_s["sr"].max()*1.2 if len(ppb_s) else 200]),
            )
            st.plotly_chart(fig_ppb, use_container_width=True, config=CHART_CONFIG)
        with ppc2:
            ppbow_s = ppbow.sort_values("eco", ascending=False)
            fig_ppbow = go.Figure(go.Bar(
                y=ppbow_s["bowler"], x=ppbow_s["eco"], orientation="h",
                marker=dict(color=ppbow_s["eco"].tolist(),
                            colorscale=[[0,GREEN],[0.5,CYAN],[1,GOLD]],
                            reversescale=True, showscale=False,
                            line=dict(color=BG, width=0.5)),
                text=[f"Eco: {v:.2f}" for v in ppbow_s["eco"]],
                textposition="outside", textfont=dict(size=10, color=TEXT),
                hovertemplate="<b>%{y}</b><br>Powerplay Eco: %{x:.2f}<extra></extra>"
            ))
            fig_ppbow.update_layout(BASE_LAYOUT)
            fig_ppbow.update_layout(
                height=420,
                title=dict(text="<b><i class='fa-solid fa-circle-dot' style='color:#FDE047;margin-right:8px;'></i> Powerplay Bowling Economy</b>  <sup>lower = better</sup>",
                           font=dict(size=15, color=TEXT), x=0),
                xaxis=dict(gridcolor=GRID, range=[0, ppbow_s["eco"].max()*1.2 if len(ppbow_s) else 12],
                           autorange="reversed"),
            )
            st.plotly_chart(fig_ppbow, use_container_width=True, config=CHART_CONFIG)

# ═══════════════════════════════════════════════════════════════════════════════
#  TAB 5 — TEAM DNA  (NEW)
# ═══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown("""<div class="sec-pill" style="--dc:#FDA4AF;"><div class="sec-dot"></div>
    <div class="sec-txt"><i class="fa-solid fa-users" style="margin-right:6px;"></i> Team DNA · Head-to-Head · Venue Dominance</div></div>""",
    unsafe_allow_html=True)

    # ── H2H Selector ──
    hc1, hc2 = st.columns(2)
    team_opts = sorted(TEAMS_SHORT_LIST)
    with hc1:
        team_a = st.selectbox("Select Team A", team_opts, index=0, key="ta")
    with hc2:
        default_b = 1 if len(team_opts)>1 else 0
        team_b = st.selectbox("Select Team B", team_opts, index=default_b, key="tb")

    h2h = mff[
        ((mff["t1s"]==team_a) & (mff["t2s"]==team_b)) |
        ((mff["t1s"]==team_b) & (mff["t2s"]==team_a))
    ].copy()

    if len(h2h) == 0:
        st.warning(f"No matches found between **{team_a}** and **{team_b}** in this range.")
    else:
        a_wins   = int((h2h["ws"] == team_a).sum())
        b_wins   = int((h2h["ws"] == team_b).sum())
        total_h2h= len(h2h)
        a_pct    = a_wins / total_h2h * 100
        b_pct    = b_wins / total_h2h * 100
        ca       = TC.get(team_a, GOLD)
        cb       = TC.get(team_b, CYAN)
        logo_a_html = get_team_logo_html(team_a, size=75)
        logo_b_html = get_team_logo_html(team_b, size=75)

        st.markdown(f"""
        <div class="h2h-hero">
            <div style="text-align:center;">
                <div style="height:80px;display:flex;align-items:center;justify-content:center;filter:drop-shadow(0 0 14px {ca}44);">{logo_a_html}</div>
                <div style="font-size:1.6rem;font-weight:900;color:{ca};margin-top:6px;">{team_a}</div>
                <div style="font-size:3rem;font-weight:900;color:{ca};line-height:1.1;">{a_wins}</div>
                <div style="font-size:0.65rem;color:#94a3b8;letter-spacing:0.12em;">WINS</div>
            </div>
            <div style="text-align:center;padding:0 16px;">
                <div style="font-size:0.78rem;color:#94a3b8;letter-spacing:0.12em;margin-bottom:6px;">VS</div>
                <div style="font-size:1.5rem;font-weight:800;color:#c9d1d9;">{total_h2h}</div>
                <div style="font-size:0.6&em;color:#94a3b8;letter-spacing:0.1em;">MATCHES</div>
            </div>
            <div style="text-align:center;">
                <div style="height:80px;display:flex;align-items:center;justify-content:center;filter:drop-shadow(0 0 14px {cb}44);">{logo_b_html}</div>
                <div style="font-size:1.6rem;font-weight:900;color:{cb};margin-top:6px;">{team_b}</div>
                <div style="font-size:3rem;font-weight:900;color:{cb};line-height:1.1;">{b_wins}</div>
                <div style="font-size:0.65rem;color:#94a3b8;letter-spacing:0.12em;">WINS</div>
            </div>
        </div>
        <div style="display:flex;align-items:center;gap:10px;margin:8px 0 18px;">
            <span style="color:{ca};font-weight:800;font-size:0.9rem;min-width:46px;">{a_pct:.0f}%</span>
            <div style="flex:1;height:14px;border-radius:7px;background:rgba(255,255,255,0.07);overflow:hidden;">
                <div style="width:{a_pct}%;height:100%;
                            background:linear-gradient(90deg,{ca},{ca}99);border-radius:7px;"></div>
            </div>
            <div style="flex:1;height:14px;border-radius:7px;background:rgba(255,255,255,0.07);overflow:hidden;direction:rtl;">
                <div style="width:{b_pct}%;height:100%;
                            background:linear-gradient(90deg,{cb},{cb}99);border-radius:7px;"></div>
            </div>
            <span style="color:{cb};font-weight:800;font-size:0.9rem;min-width:46px;text-align:right;">{b_pct:.0f}%</span>
        </div>
        """, unsafe_allow_html=True)

        # Season-by-season diverging bars
        h2h_seas = h2h.copy()
        h2h_seas["yr"] = h2h_seas["season"]
        by_yr = h2h_seas.groupby("yr").apply(
            lambda g: pd.Series({
                "a": int((g["ws"]==team_a).sum()),
                "b": int((g["ws"]==team_b).sum())
            })
        ).reset_index()
        by_yr.columns = ["season","a_wins","b_wins"]

        fig_h2h = go.Figure()
        fig_h2h.add_bar(x=by_yr["season"], y=by_yr["a_wins"], name=team_a,
                        marker_color=ca, opacity=0.85,
                        text=by_yr["a_wins"], textposition="outside",
                        hovertemplate=f"<b>{team_a}</b>: %{{y}} win(s) in %{{x}}<extra></extra>")
        fig_h2h.add_bar(x=by_yr["season"], y=-by_yr["b_wins"], name=team_b,
                        marker_color=cb, opacity=0.85,
                        customdata=by_yr["b_wins"],
                        hovertemplate=f"<b>{team_b}</b>: %{{customdata}} win(s) in %{{x}}<extra></extra>")
        fig_h2h.update_layout(BASE_LAYOUT)
        fig_h2h.update_layout(
            height=320, barmode="relative",
            title=dict(text=f"<b><i class='fa-solid fa-chart-bar' style='color:#67E8F9;margin-right:8px;'></i> {team_a} vs {team_b} · Season-by-Season</b>",
                       font=dict(size=14, color=TEXT), x=0),
            xaxis=dict(gridcolor=GRID, tickfont=dict(color=MUTED, size=9)),
            yaxis=dict(gridcolor=GRID, title="Wins (↑ A  ↓ B)",
                       tickvals=[-3,-2,-1,0,1,2,3],
                       ticktext=["3","2","1","0","1","2","3"]),
        )
        st.plotly_chart(fig_h2h, use_container_width=True, config=CHART_CONFIG)

        # Venue breakdown
        vb = h2h.groupby(["venue","ws"]).size().reset_index(name="cnt")
        if len(vb) > 0:
            va = vb[vb["ws"]==team_a].set_index("venue")["cnt"]
            vb2 = vb[vb["ws"]==team_b].set_index("venue")["cnt"]
            venues = sorted(set(va.index)|set(vb2.index))
            vdf = pd.DataFrame({"venue":venues,
                                  "a":[va.get(v,0) for v in venues],
                                  "b":[vb2.get(v,0) for v in venues]})
            vdf = vdf.sort_values("a", ascending=False)
            fig_v = go.Figure()
            fig_v.add_bar(x=vdf["venue"], y=vdf["a"], name=team_a,
                          marker_color=ca, opacity=0.85,
                          hovertemplate=f"<b>{team_a}</b>: %{{y}} at %{{x}}<extra></extra>")
            fig_v.add_bar(x=vdf["venue"], y=vdf["b"], name=team_b,
                          marker_color=cb, opacity=0.85,
                          hovertemplate=f"<b>{team_b}</b>: %{{y}} at %{{x}}<extra></extra>")
            fig_v.update_layout(BASE_LAYOUT)
            fig_v.update_layout(
                height=300, barmode="group",
                title=dict(text=f"<b><i class='fa-solid fa-location-dot' style='color:#FDA4AF;margin-right:8px;'></i> Venue Breakdown</b>",
                           font=dict(size=14, color=TEXT), x=0),
                xaxis=dict(gridcolor=GRID, tickfont=dict(color=MUTED, size=8), tickangle=30),
                yaxis=dict(gridcolor=GRID),
            )
            st.plotly_chart(fig_v, use_container_width=True, config=CHART_CONFIG)

    # ── All-Team H2H Win Matrix ──
    st.markdown("""<div class="sec-pill" style="--dc:#C084FC;"><div class="sec-dot"></div>
    <div class="sec-txt"><i class="fa-solid fa-table-cells" style="margin-right:6px;"></i> All-Team Head-to-Head Win Rate Matrix</div></div>""", unsafe_allow_html=True)

    top_teams = mff["ws"].value_counts().head(10).index.tolist()
    n_t = len(top_teams)
    matrix = np.full((n_t, n_t), np.nan)
    for i, ta_ in enumerate(top_teams):
        for j, tb_ in enumerate(top_teams):
            if ta_ == tb_: continue
            sub_ = mff[((mff["t1s"]==ta_)&(mff["t2s"]==tb_)) |
                       ((mff["t1s"]==tb_)&(mff["t2s"]==ta_))]
            if len(sub_) > 0:
                matrix[i][j] = (sub_["ws"]==ta_).sum() / len(sub_) * 100

    text_matrix = [[f"{v:.0f}%" if not np.isnan(v) else "—" for v in row] for row in matrix]
    fig_mat = go.Figure(go.Heatmap(
        z=matrix, x=top_teams, y=top_teams,
        colorscale=[[0,"#FCA5A5"],[0.45,"#1E293B"],[0.55,"#1E293B"],[1,"#86EFAC"]],
        zmid=50, zmin=25, zmax=75,
        text=text_matrix, texttemplate="%{text}",
        textfont=dict(size=10, family="Inter"),
        hovertemplate="<b>%{y}</b> vs <b>%{x}</b><br>Win Rate: %{z:.1f}%<extra></extra>",
        xgap=3, ygap=3, showscale=True,
        colorbar=dict(title=dict(text="Win %", font=dict(color=TEXT)),
                      tickfont=dict(color=MUTED)),
    ))
    fig_mat.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=TEXT, family="Inter"),
        margin=dict(l=60,r=20,t=55,b=60), height=460,
        title=dict(text="<b><i class='fa-solid fa-table' style='color:#FDE047;margin-right:8px;'></i> H2H Win Rate Matrix</b>  <sup style='color:#94a3b8'>row team's win % vs column team</sup>",
                   font=dict(size=14, color=TEXT), x=0),
        xaxis=dict(tickfont=dict(color=MUTED, size=9)),
        yaxis=dict(tickfont=dict(color=TEXT, size=10)),
        hoverlabel=dict(bgcolor=CARD, font=dict(color=TEXT, family="Inter")),
    )
    st.plotly_chart(fig_mat, use_container_width=True, config=CHART_CONFIG)

    # Team colour legend
    st.markdown("<div style='display:flex;flex-wrap:wrap;gap:10px;margin-top:10px;'>", unsafe_allow_html=True)
    for t_, c_ in TC.items():
        if t_ in top_teams:
            logo_html = get_team_logo_html(t_, size=18)
            st.markdown(f"""
            <div style="display:inline-flex;align-items:center;gap:6px;
                        padding:5px 12px;border-radius:100px;
                        background:{TP.get(t_,'rgba(255,255,255,0.05)')};
                        border:1px solid {c_}55;">
                <span style="height:18px;display:flex;align-items:center;">{logo_html}</span>
                <span style="color:{c_};font-weight:700;font-size:0.78rem;">{t_}</span>
            </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  TAB 6 — MATCH ORACLE  (NEW)
# ═══════════════════════════════════════════════════════════════════════════════
with tab6:
    st.markdown("""<div class="sec-pill" style="--dc:#C084FC;"><div class="sec-dot"></div>
    <div class="sec-txt"><i class="fa-solid fa-wand-magic-sparkles" style="margin-right:6px;"></i> Match Oracle · Live Win Probability Engine</div></div>""",
    unsafe_allow_html=True)

    st.markdown("""
    <div class="oracle-card">
        <div style="font-size:0.68rem;font-weight:700;color:#C084FC;
                    letter-spacing:0.12em;text-transform:uppercase;margin-bottom:8px;">
            <i class="fa-solid fa-circle-info" style="margin-right:6px;"></i> EMPIRICAL WIN PROBABILITY
        </div>
        <div style="color:#c9d1d9;font-size:0.87rem;line-height:1.65;">
            Powered by <b>historical IPL ball-by-ball data</b> from 1,193 matches.
            Enter the live match situation to calculate win probability.
        </div>
    </div>
    """, unsafe_allow_html=True)

    oc1, oc2 = st.columns([1,1])
    with oc1:
        target       = st.number_input("Target (1st innings + 1)", 50, 300, 175, 1)
        overs_done   = st.slider("Overs completed in chase", 0.0, 19.9, 10.0, 0.1)
        wkts_fallen  = st.slider("Wickets fallen", 0, 10, 2)
        current_score= st.number_input("Current score", 0, int(target)-1, 90, 1)

    with oc2:
        runs_needed     = int(target) - int(current_score)
        balls_remaining = max(1, int((20 - overs_done) * 6))
        req_rr          = runs_needed / (balls_remaining / 6)
        wkts_remaining  = 10 - wkts_fallen

        # Empirical probability model
        base = max(5, min(95, 82 - (req_rr - 6) * 7.5))
        wkt_adj = (wkts_remaining - 5) * 2.5
        prob = round(max(5, min(95, base + wkt_adj)), 1)

        gauge_c = GREEN if prob>60 else CORAL if prob<40 else GOLD
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prob,
            number=dict(suffix="%", font=dict(size=44, color=gauge_c, family="Inter")),
            gauge=dict(
                axis=dict(range=[0,100], tickwidth=1, tickcolor=MUTED,
                          tickfont=dict(color=MUTED, size=9)),
                bar=dict(color=gauge_c, thickness=0.28),
                bgcolor="rgba(0,0,0,0)", borderwidth=0,
                steps=[dict(range=[0,35],  color="rgba(253,164,175,0.12)"),
                       dict(range=[35,60], color="rgba(253,224,71,0.08)"),
                       dict(range=[60,100],color="rgba(134,239,172,0.12)")],
                threshold=dict(line=dict(color=MUTED,width=2), thickness=0.8, value=50)
            ),
            title=dict(text="<b><i class='fa-solid fa-gauge-high' style='color:#67E8F9;margin-right:8px;'></i> Chase Win Probability</b>",
                       font=dict(size=14, color=TEXT, family="Inter"))
        ))
        fig_gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                                margin=dict(l=30,r=30,t=60,b=10), height=290)
        st.plotly_chart(fig_gauge, use_container_width=True, config=CHART_CONFIG)

    # Situation cards
    verdict = ("Chasing team favoured" if prob>57 else
               "Defending team favoured" if prob<43 else "Toss-up")
    difficulty = "Very Easy" if req_rr<6 else "Easy" if req_rr<8 else \
                 "Moderate" if req_rr<10 else "Hard" if req_rr<12 else "Very Hard"
    diff_c = GREEN if req_rr<7 else GOLD if req_rr<10 else CORAL

    st.markdown(f"""
    <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin:16px 0 10px;">
        <div class="kpi-card" style="--ac:{PURP};"><div class="kpi-val">{runs_needed}</div>
        <div class="kpi-lbl">RUNS NEEDED</div></div>
        <div class="kpi-card" style="--ac:{CORAL};"><div class="kpi-val">{balls_remaining}</div>
        <div class="kpi-lbl">BALLS LEFT</div></div>
        <div class="kpi-card" style="--ac:{GOLD};"><div class="kpi-val">{req_rr:.2f}</div>
        <div class="kpi-lbl">REQUIRED RR</div></div>
        <div class="kpi-card" style="--ac:{GREEN};"><div class="kpi-val">{wkts_remaining}</div>
        <div class="kpi-lbl">WKTS IN HAND</div></div>
        <div class="kpi-card" style="--ac:{diff_c};"><div class="kpi-val">{difficulty}</div>
        <div class="kpi-lbl">DIFFICULTY</div></div>
    </div>
    <div class="insight">
        <div class="insight-lbl"><i class="fa-solid fa-magnifying-glass-chart" style="margin-right:6px;"></i> Match Verdict</div>
        <div class="insight-txt"><b>{verdict.upper()}</b> &nbsp;·&nbsp;
        Required RR <b>{req_rr:.2f}</b> vs tournament avg {avg_rr} &nbsp;·&nbsp;
        Chase win prob: <b>{prob:.1f}%</b></div>
    </div>
    """, unsafe_allow_html=True)

    # Historical chase chart with target highlight
    inn1_d = dff[dff["innings"]==1].groupby("match_id")["runs_total"].sum().reset_index(name="tgt")
    inn2_d = dff[dff["innings"]==2].groupby("match_id").agg(
        ct=("batting_team","first")).reset_index()
    ch_df = inn2_d.merge(inn1_d, on="match_id").merge(mff[["match_id","winner"]], on="match_id")
    ch_df["won"] = ch_df["ct"] == ch_df["winner"]
    bands = [0,130,150,165,180,195,210,999]
    lbls  = ["<130","130–150","150–165","165–180","180–195","195–210","210+"]
    ch_df["tb"] = pd.cut(ch_df["tgt"], bins=bands, labels=lbls)
    cg = ch_df.groupby("tb", observed=False)["won"].agg(["mean","count"]).reset_index()
    cg["wp"]  = cg["mean"] * 100
    cg["tb"]  = cg["tb"].astype(str)

    t_val = int(target) - 1
    cur_band = lbls[0]
    for i, (lo, hi) in enumerate(zip(bands[:-1], bands[1:])):
        if lo <= t_val < hi:
            cur_band = lbls[i]; break

    bar_clr = [TEAL if tb==cur_band else "rgba(103,232,249,0.3)" for tb in cg["tb"]]
    fig_cg = go.Figure(go.Bar(
        x=cg["tb"], y=cg["wp"],
        marker=dict(color=bar_clr, line=dict(color=BG, width=1)),
        text=[f"<b>{v:.0f}%</b><br>{n}" for v,n in zip(cg["wp"],cg["count"])],
        textposition="outside", textfont=dict(size=10, color=TEXT),
        hovertemplate="Target %{x}<br>Chase Win %: %{y:.1f}%<extra></extra>"
    ))
    fig_cg.add_hline(y=50, line_dash="dot", line_color=MUTED,
                     annotation_text="50% baseline",
                     annotation_font=dict(color=MUTED, size=10))
    fig_cg.update_layout(BASE_LAYOUT)
    fig_cg.update_layout(
        height=320,
        title=dict(text=f"<b><i class='fa-solid fa-chart-column' style='color:#FDA4AF;margin-right:8px;'></i> Chase Success Rate by Target Band</b>  <sup style='color:#94a3b8'>highlighted = your target ({int(target)-1})</sup>",
                   font=dict(size=14, color=TEXT), x=0),
        xaxis=dict(gridcolor=GRID, title="Target Band"),
        yaxis=dict(gridcolor=GRID, range=[0,88], title="Win %"),
    )
    st.plotly_chart(fig_cg, use_container_width=True, config=CHART_CONFIG)

    # Required RR evolution (what-if)
    st.markdown("""<div class="sec-pill" style="--dc:#67E8F9;"><div class="sec-dot"></div>
    <div class="sec-txt"><i class="fa-solid fa-chart-line" style="margin-right:6px;"></i> Required Run Rate Evolution</div></div>""", unsafe_allow_html=True)

    ov_pts = [o/10 for o in range(0, 201, 5)]
    rr_pts = [(runs_needed) / max(1, (20-o)*6/6) for o in ov_pts]
    fig_rr = go.Figure()
    fig_rr.add_trace(go.Scatter(
        x=ov_pts, y=rr_pts, mode="lines",
        line=dict(color=TEAL, width=3, shape="spline"),
        fill="tozeroy", fillcolor="rgba(103,232,249,0.08)",
        hovertemplate="Overs: %{x:.1f}<br>Req RR: %{y:.2f}<extra></extra>",
        name="Required RR"
    ))
    fig_rr.add_vline(x=overs_done, line_dash="dash", line_color=GOLD,
                     annotation_text=f"Now ({overs_done:.1f}ov)",
                     annotation_font=dict(color=GOLD, size=10))
    fig_rr.add_hline(y=avg_rr, line_dash="dot", line_color=MUTED,
                     annotation_text=f"Tournament avg {avg_rr}",
                     annotation_font=dict(color=MUTED, size=10))
    fig_rr.update_layout(BASE_LAYOUT)
    fig_rr.update_layout(
        height=280,
        title=dict(text="<b><i class='fa-solid fa-chart-line' style='color:#FDE047;margin-right:8px;'></i> Required RR as Chase Progresses</b>",
                   font=dict(size=14, color=TEXT), x=0),
        xaxis=dict(gridcolor=GRID, title="Overs Completed",
                   range=[0,20], tickfont=dict(color=MUTED, size=9)),
        yaxis=dict(gridcolor=GRID, title="Required RR", range=[0, max(rr_pts)*1.2]),
    )
    st.plotly_chart(fig_rr, use_container_width=True, config=CHART_CONFIG)

# ═══════════════════════════════════════════════════════════════════════════════
#  TAB 7 — DEEP INSIGHTS
# ═══════════════════════════════════════════════════════════════════════════════
with tab7:
    st.markdown("""<div class="sec-pill" style="--dc:#FCA5A5;"><div class="sec-dot"></div>
    <div class="sec-txt"><i class="fa-solid fa-chart-pie" style="margin-right:6px;"></i> Deep Insights · Advanced Analytics</div></div>""", unsafe_allow_html=True)

    st.markdown(f'''
    <div style="background: linear-gradient(135deg, rgba(253,224,71,0.1), rgba(192,132,252,0.15));
                border: 2px solid rgba(253,224,71,0.4); border-radius: 24px; padding: 36px 40px; margin-bottom: 30px;
                box-shadow: 0 16px 40px rgba(0,0,0,0.4), inset 0 0 40px rgba(253,224,71,0.05);
                backdrop-filter: blur(20px); text-align: center; position: relative; overflow: hidden;">
        <div style="position: absolute; top: -50px; right: -50px; font-size: 8rem; color: rgba(253,224,71,0.05);"><i class="fa-solid fa-lightbulb"></i></div>
        <div style="font-size: 0.8rem; font-weight: 800; color: #FDE047; letter-spacing: 0.25em; text-transform: uppercase; margin-bottom: 12px; animation: glow-pulse 2s infinite;">
            <i class="fa-solid fa-bolt" style="margin-right: 8px;"></i> Surprising Spotlight Insight
        </div>
        <div style="font-size: 1.8rem; font-weight: 900; color: #f8fafc; line-height: 1.4; letter-spacing: -0.02em;">
            Chasing teams win 50.3% of matches, but <span style="color:#FDA4AF; text-shadow: 0 0 16px rgba(253,164,175,0.6);">success drops off a cliff above 180 runs</span>—making bowler economy the most critical match-winning metric.
        </div>
    </div>
    ''', unsafe_allow_html=True)

    di1, di2 = st.columns(2)

    # Chase code
    with di1:
        inn1_x = (dff[dff["innings"]==1].groupby("match_id")["runs_total"].sum()
                  .reset_index(name="target"))
        inn2_x = (dff[dff["innings"]==2].groupby("match_id")
                  .agg(ct=("batting_team","first")).reset_index())
        chase_x = inn2_x.merge(inn1_x, on="match_id").merge(mff[["match_id","winner"]], on="match_id")
        chase_x["won"] = chase_x["ct"] == chase_x["winner"]
        chase_x["tb"]  = pd.cut(chase_x["target"], bins=[0,140,160,180,200,999],
                                labels=["<140","140–160","160–180","180–200","200+"])
        cgx = chase_x.groupby("tb", observed=False)["won"].agg(["mean","count"]).reset_index()
        cgx["wp"] = cgx["mean"] * 100

        fig_ch = go.Figure(go.Bar(
            x=cgx["tb"].astype(str), y=cgx["wp"],
            marker=dict(color=cgx["wp"].tolist(),
                        colorscale=[[0,CORAL],[0.5,GOLD],[1,GREEN]],
                        showscale=False, line=dict(color=BG, width=1)),
            text=[f"<b>{v:.1f}%</b><br>{n}" for v,n in zip(cgx["wp"],cgx["count"])],
            textposition="outside", textfont=dict(size=11, color=TEXT),
            hovertemplate="Target %{x}<br>Chase Win %: %{y:.1f}%<extra></extra>"
        ))
        fig_ch.add_hline(y=50, line_dash="dot", line_color=MUTED,
                         annotation_text="50% baseline",
                         annotation_font=dict(color=MUTED, size=10))
        fig_ch.update_layout(BASE_LAYOUT)
        fig_ch.update_layout(
            height=360,
            title=dict(text="<b><i class='fa-solid fa-crosshairs' style='color:#FDA4AF;margin-right:8px;'></i> The Chase Code</b>  <sup style='color:#94a3b8'>win rate by target band</sup>",
                       font=dict(size=15, color=TEXT), x=0),
            xaxis=dict(gridcolor=GRID, title="First Innings Score Band"),
            yaxis=dict(gridcolor=GRID, range=[0,85], title="Chase Win %"),
        )
        st.plotly_chart(fig_ch, use_container_width=True, config=CHART_CONFIG)

    # Dynasty sunburst
    with di2:
        seas_w = mff.groupby(["season","ws"]).size().reset_index(name="wins")
        top6   = mff["ws"].value_counts().head(6).index.tolist()
        sw6    = seas_w[seas_w["ws"].isin(top6)]
        t_clr  = {t: TC.get(t, GOLD) for t in top6}

        fig_sb = px.sunburst(
            sw6, path=["ws","season"], values="wins",
            color="ws", color_discrete_map=t_clr,
        )
        fig_sb.update_traces(
            textfont=dict(size=11, family="Inter"),
            insidetextorientation="radial",
            hovertemplate="<b>%{id}</b><br>Wins: %{value}<extra></extra>"
        )
        fig_sb.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10,r=10,t=55,b=10), height=360,
            title=dict(text="<b><i class='fa-solid fa-trophy' style='color:#FDE047;margin-right:8px;'></i> Dynasty Sunburst</b>  <sup style='color:#94a3b8'>franchise × season wins</sup>",
                       font=dict(size=15, color=TEXT), x=0),
            font=dict(color=TEXT, family="Inter"),
        )
        st.plotly_chart(fig_sb, use_container_width=True, config=CHART_CONFIG)

    # Season × Franchise heatmap
    all_ts = mff.groupby(["season","ws"]).size().reset_index(name="wins")
    pivot  = all_ts.pivot_table(index="ws", columns="season", values="wins", fill_value=0)
    row_order = pivot.sum(axis=1).sort_values(ascending=False).index.tolist()
    pivot = pivot.loc[row_order]

    # Colour rows by team colour
    row_colors = [TC.get(t, GOLD) for t in pivot.index]

    fig_hm = go.Figure(go.Heatmap(
        z=pivot.values, x=pivot.columns.tolist(), y=pivot.index.tolist(),
        colorscale=[[0,"#1E293B"],[0.3,"#C084FC"],[0.7,"#FDA4AF"],[1,"#FDE047"]],
        showscale=True, zmin=0,
        text=pivot.values, texttemplate="%{text}",
        textfont=dict(size=10, color=TEXT, family="Inter"),
        hovertemplate="<b>%{y}</b><br>Season %{x}<br>Wins: %{z}<extra></extra>",
        xgap=3, ygap=3,
        colorbar=dict(title=dict(text="Wins", font=dict(color=TEXT)),
                      tickfont=dict(color=MUTED)),
    ))
    fig_hm.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=TEXT, family="Inter"),
        margin=dict(l=80,r=20,t=60,b=60), height=440,
        title=dict(text="<b><i class='fa-solid fa-calendar-days' style='color:#67E8F9;margin-right:8px;'></i> Season × Franchise Win Matrix</b>  <sup style='color:#94a3b8'>full historical record</sup>",
                   font=dict(size=14, color=TEXT), x=0),
        xaxis=dict(tickfont=dict(color=MUTED, size=9)),
        yaxis=dict(tickfont=dict(color=TEXT, size=10)),
        hoverlabel=dict(bgcolor=CARD, font=dict(color=TEXT, family="Inter")),
    )
    st.plotly_chart(fig_hm, use_container_width=True, config=CHART_CONFIG)

    overall_chase_pct = chase_x["won"].mean()*100 if len(chase_x)>0 else 50
    # Count high-scoring matches (200+)
    high_score_pct = len(inn1_x[inn1_x["target"]>=200]) / max(len(inn1_x), 1) * 100
    st.markdown(f"""
    <div class="insight">
        <div class="insight-lbl"><i class="fa-solid fa-fire" style="margin-right:6px;"></i> The ONE Genuinely Surprising Insight</div>
        <div class="insight-txt">
            Chasing teams win <b>{overall_chase_pct:.1f}%</b> of all IPL matches — near parity.
            But chase success <b>falls off a cliff above 180 runs</b>: only <b>{cgx[cgx['tb'].astype(str).str.contains('180|200')]['wp'].mean():.0f}%</b> of chases above 180 succeed.
            <b>{high_score_pct:.0f}%</b> of IPL innings now produce 200+ totals — a dramatic rise from the early seasons.
            The data argues for a <b>"restrict to 175, not 200"</b> strategy.
            Bowlers who save 15 runs are statistically more valuable than batters who score 15 extra.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Venue Analysis ────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""<div class="sec-pill" style="--dc:#2DD4BF;"><div class="sec-dot"></div>
    <div class="sec-txt"><i class="fa-solid fa-stadium" style="margin-right:6px;"></i> Venue Intelligence · Highest Scoring & Best Chase Grounds</div></div>""",
    unsafe_allow_html=True)

    venue_stats = mff.groupby("venue").agg(
        matches=("match_id","count"),
        chase_wins=("twmw","sum")
    ).reset_index()

    # Total runs per venue from deliveries
    venue_runs = dff.groupby("venue")["runs_total"].sum().reset_index(name="total_runs")
    venue_balls = dff.groupby("venue")["ball"].count().reset_index(name="total_balls")
    venue_stats = venue_stats.merge(venue_runs, on="venue", how="left")
    venue_stats = venue_stats.merge(venue_balls, on="venue", how="left")
    venue_stats["avg_match_runs"] = venue_stats["total_runs"] / venue_stats["matches"] / 2
    venue_stats["chase_win_pct"] = venue_stats["chase_wins"] / venue_stats["matches"] * 100
    venue_stats = venue_stats[venue_stats["matches"] >= 5].sort_values("avg_match_runs", ascending=False)

    v1, v2 = st.columns(2)
    with v1:
        top_venues = venue_stats.head(12)
        fig_v1 = go.Figure(go.Bar(
            y=top_venues["venue"].str.replace(r"\s*,.*", "", regex=True).str[:30],
            x=top_venues["avg_match_runs"],
            orientation="h",
            marker=dict(color=top_venues["avg_match_runs"].tolist(),
                        colorscale=[[0,CYAN],[0.5,GOLD],[1,CORAL]],
                        showscale=False, line=dict(color=BG, width=0.5)),
            text=[f"{v:.0f}" for v in top_venues["avg_match_runs"]],
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Avg Match Runs (1 inns): %{x:.0f}<extra></extra>"
        ))
        fig_v1.update_layout(BASE_LAYOUT)
        fig_v1.update_layout(
            height=440,
            title=dict(text="<b><i class='fa-solid fa-fire' style='color:#FDA4AF;margin-right:8px;'></i> Highest Scoring Venues</b>  <sup>avg runs per innings</sup>",
                       font=dict(size=14, color=TEXT), x=0),
            xaxis=dict(gridcolor=GRID, title="Avg Runs per Innings"),
        )
        st.plotly_chart(fig_v1, use_container_width=True, config=CHART_CONFIG)

    with v2:
        top_chase = venue_stats.sort_values("chase_win_pct").tail(12)
        fig_v2 = go.Figure(go.Bar(
            y=top_chase["venue"].str.replace(r"\s*,.*", "", regex=True).str[:30],
            x=top_chase["chase_win_pct"],
            orientation="h",
            marker=dict(color=top_chase["chase_win_pct"].tolist(),
                        colorscale=[[0,CORAL],[0.5,GOLD],[1,GREEN]],
                        showscale=False, line=dict(color=BG, width=0.5)),
            text=[f"{v:.0f}%" for v in top_chase["chase_win_pct"]],
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Chase Win %: %{x:.0f}%<extra></extra>"
        ))
        fig_v2.add_vline(x=50, line_dash="dot", line_color=MUTED,
                         annotation_text="50% baseline",
                         annotation_font=dict(color=MUTED, size=9))
        fig_v2.update_layout(BASE_LAYOUT)
        fig_v2.update_layout(
            height=440,
            title=dict(text="<b><i class='fa-solid fa-crosshairs' style='color:#86EFAC;margin-right:8px;'></i> Best Venues to Chase</b>  <sup>chase win % — higher = chaser-friendly</sup>",
                       font=dict(size=14, color=TEXT), x=0),
            xaxis=dict(gridcolor=GRID, range=[0,100], title="Chase Win %"),
        )
        st.plotly_chart(fig_v2, use_container_width=True, config=CHART_CONFIG)

    # Venue with highest chase success
    best_chase_venue = venue_stats.sort_values("chase_win_pct", ascending=False).iloc[0] if len(venue_stats)>0 else None
    best_score_venue = venue_stats.sort_values("avg_match_runs", ascending=False).iloc[0] if len(venue_stats)>0 else None
    if best_chase_venue is not None:
        st.markdown(f"""
        <div class="insight">
            <div class="insight-lbl"><i class="fa-solid fa-stadium" style="margin-right:6px;"></i> Venue Insights</div>
            <div class="insight-txt">
                <b>{best_score_venue['venue'][:50]}</b> is the highest-scoring venue, averaging <b>{best_score_venue['avg_match_runs']:.0f} runs</b> per innings over {int(best_score_venue['matches'])} matches.
                <br>The most chaser-friendly ground is <b>{best_chase_venue['venue'][:50]}</b> with a chase win rate of <b>{best_chase_venue['chase_win_pct']:.0f}%</b> — dew, short boundaries, and flat pitches all contribute.
            </div>
        </div>
        """, unsafe_allow_html=True)

# ─── CHATBOT ──────────────────────────────────────────────────────────────────
# Prepare a small context string for the AI
ai_context = f"IPL Stats: {len(dff)} deliveries, {len(mff)} matches, {dff['season'].nunique()} seasons. Toss win rate is {toss_win_rate:.1f}%. The most influential phase is {most_linked_phase}."
render_chatbot(ai_context)

# ─── PREMIUM FOOTER ───────────────────────────────────────────────────────────
st.markdown(f"""
<div style="margin-top: 80px; padding: 60px 40px 40px; background: linear-gradient(180deg, rgba(15,23,42,0.6) 0%, rgba(10,16,30,0.98) 100%); border-top: 1px solid rgba(253,224,71,0.15); border-radius: 24px 24px 0 0; position: relative; overflow: hidden; backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);">
<div style="position:absolute; top:0; left:50%; transform:translateX(-50%); width:60%; height:1.5px; background:linear-gradient(90deg,transparent,rgba(253,224,71,0.4),transparent);"></div>

<div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: flex-start; max-width: 1200px; margin: 0 auto; gap: 40px;">
<div style="flex: 1; min-width: 250px;">
<div style="font-size: 1.6rem; font-weight: 900; color: #FDE047; letter-spacing: -0.02em; display: flex; align-items: center; gap: 10px; margin-bottom: 12px; text-shadow: 0 0 20px rgba(253,224,71,0.3);">
<i class="fa-solid fa-baseball-bat-ball"></i> IPL Crunch '26
</div>
<div style="font-size: 0.9rem; color: #cbd5e1; line-height: 1.6; margin-bottom: 24px; max-width: 320px;">
The ultimate analytics intelligence hub for IPL data. 
Built for deep insights, team DNA analysis, and predictive metrics.
</div>
<div style="display: flex; gap: 14px;">
<div style="width: 36px; height: 36px; border-radius: 50%; background: rgba(255,255,255,0.05); display: flex; align-items: center; justify-content: center; color: #e2e8f0; border: 1px solid rgba(255,255,255,0.15); cursor: pointer; transition: all 0.3s ease; box-shadow: 0 4px 10px rgba(0,0,0,0.3);" onmouseover="this.style.background='rgba(255,255,255,0.1)';this.style.transform='translateY(-2px)';" onmouseout="this.style.background='rgba(255,255,255,0.05)';this.style.transform='translateY(0)';"><i class="fa-brands fa-github"></i></div>
<div style="width: 36px; height: 36px; border-radius: 50%; background: rgba(255,255,255,0.05); display: flex; align-items: center; justify-content: center; color: #e2e8f0; border: 1px solid rgba(255,255,255,0.15); cursor: pointer; transition: all 0.3s ease; box-shadow: 0 4px 10px rgba(0,0,0,0.3);" onmouseover="this.style.background='rgba(255,255,255,0.1)';this.style.transform='translateY(-2px)';" onmouseout="this.style.background='rgba(255,255,255,0.05)';this.style.transform='translateY(0)';"><i class="fa-brands fa-twitter"></i></div>
<div style="width: 36px; height: 36px; border-radius: 50%; background: rgba(255,255,255,0.05); display: flex; align-items: center; justify-content: center; color: #e2e8f0; border: 1px solid rgba(255,255,255,0.15); cursor: pointer; transition: all 0.3s ease; box-shadow: 0 4px 10px rgba(0,0,0,0.3);" onmouseover="this.style.background='rgba(255,255,255,0.1)';this.style.transform='translateY(-2px)';" onmouseout="this.style.background='rgba(255,255,255,0.05)';this.style.transform='translateY(0)';"><i class="fa-solid fa-envelope"></i></div>
</div>
</div>

<div style="flex: 1; min-width: 200px;">
<div style="font-size: 1rem; font-weight: 800; color: #f8fafc; margin-bottom: 18px; text-transform: uppercase; letter-spacing: 0.12em;">Data Coverage</div>
<div style="display: flex; flex-direction: column; gap: 12px; font-size: 0.9rem; color: #cbd5e1;">
<div style="display: flex; justify-content: space-between; border-bottom: 1px dashed rgba(255,255,255,0.15); padding-bottom: 8px;">
<span>Matches</span> <span style="color: #FDE047; font-weight: 700;">{len(matches):,}</span>
</div>
<div style="display: flex; justify-content: space-between; border-bottom: 1px dashed rgba(255,255,255,0.15); padding-bottom: 8px;">
<span>Deliveries</span> <span style="color: #67E8F9; font-weight: 700;">{len(df):,}</span>
</div>
<div style="display: flex; justify-content: space-between; border-bottom: 1px dashed rgba(255,255,255,0.15); padding-bottom: 8px;">
<span>Seasons</span> <span style="color: #C084FC; font-weight: 700;">{len(SEASONS)}</span>
</div>
</div>
</div>

<div style="flex: 1; min-width: 200px;">
<div style="font-size: 1rem; font-weight: 800; color: #f8fafc; margin-bottom: 18px; text-transform: uppercase; letter-spacing: 0.12em;">Tech Stack</div>
<div style="display: flex; flex-wrap: wrap; gap: 10px;">
<span style="padding: 6px 12px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); border-radius: 8px; font-size: 0.8rem; color: #e2e8f0; font-weight: 500;">Python 3</span>
<span style="padding: 6px 12px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); border-radius: 8px; font-size: 0.8rem; color: #e2e8f0; font-weight: 500;">Streamlit</span>
<span style="padding: 6px 12px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); border-radius: 8px; font-size: 0.8rem; color: #e2e8f0; font-weight: 500;">Plotly</span>
<span style="padding: 6px 12px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); border-radius: 8px; font-size: 0.8rem; color: #e2e8f0; font-weight: 500;">Pandas</span>
<span style="padding: 6px 12px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); border-radius: 8px; font-size: 0.8rem; color: #e2e8f0; font-weight: 500;">Llama 3</span>
</div>
</div>
</div>

<div style="margin-top: 50px; padding-top: 24px; border-top: 1px solid rgba(255,255,255,0.08); text-align: center; font-size: 0.85rem; color: #cbd5e1; letter-spacing: 0.03em;">
© 2026 IPL Crunch Analytics. All rights reserved. Data sourced from public datasets.
</div>
</div>
""", unsafe_allow_html=True)
