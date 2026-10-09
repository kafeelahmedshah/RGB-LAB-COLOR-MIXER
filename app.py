import streamlit as st
import pandas as pd

st.set_page_config(page_title="RGB + LAB Color Mixer", page_icon="🎨", layout="wide")

# Standard sRGB / D65 conversion functions
def srgb_to_linear(c):
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def linear_to_srgb(c):
    c = max(0.0, min(1.0, c))
    return 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055

def rgb_to_xyz(r, g, b):
    r, g, b = map(srgb_to_linear, (r, g, b))
    return (
        (0.4124564*r + 0.3575761*g + 0.1804375*b) * 100,
        (0.2126729*r + 0.7151522*g + 0.0721750*b) * 100,
        (0.0193339*r + 0.1191920*g + 0.9503041*b) * 100,
    )

def f(t):
    d = 6 / 29
    return t ** (1/3) if t > d**3 else t / (3*d*d) + 4/29

def finv(t):
    d = 6 / 29
    return t**3 if t > d else 3*d*d*(t - 4/29)

def xyz_to_lab(x, y, z):
    fx, fy, fz = f(x/95.047), f(y/100.0), f(z/108.883)
    return 116*fy-16, 500*(fx-fy), 200*(fy-fz)

def rgb_to_lab(r, g, b):
    return xyz_to_lab(*rgb_to_xyz(r, g, b))

def lab_to_xyz(L, a, b):
    fy = (L+16)/116
    fx = fy + a/500
    fz = fy - b/200
    return 95.047*finv(fx), 100.0*finv(fy), 108.883*finv(fz)

def xyz_to_rgb(x, y, z):
    x, y, z = x/100, y/100, z/100
    r = 3.2404542*x - 1.5371385*y - 0.4985314*z
    g = -0.9692660*x + 1.8760108*y + 0.0415560*z
    b = 0.0556434*x - 0.2040259*y + 1.0572252*z
    return tuple(round(linear_to_srgb(v)*255) for v in (r, g, b))

def lab_to_rgb(L, a, b):
    return xyz_to_rgb(*lab_to_xyz(L, a, b))

def clamp_rgb(rgb):
    return tuple(max(0, min(255, int(round(v)))) for v in rgb)

def rgb_hex(rgb):
    return "#{:02X}{:02X}{:02X}".format(*rgb)

def show_preview(rgb):
    hx = rgb_hex(rgb)
    st.markdown(f'''<div style="height:240px;background:{hx};border-radius:18px;border:1px solid #bbb;display:flex;align-items:flex-end;justify-content:center;padding:18px;box-sizing:border-box"><span style="background:rgba(0,0,0,.55);color:#fff;padding:8px 14px;border-radius:10px;font-family:monospace;font-size:18px">{hx}</span></div>''', unsafe_allow_html=True)

def save_color(rgb, lab):
    item = {"RGB": tuple(map(int, rgb)), "LAB": tuple(round(x,2) for x in lab), "HEX": rgb_hex(rgb)}
    if not st.session_state.history or st.session_state.history[0] != item:
        st.session_state.history.insert(0, item)
        st.session_state.history = st.session_state.history[:20]

if "history" not in st.session_state:
    st.session_state.history = []
if "rgb" not in st.session_state:
    st.session_state.rgb = (128, 128, 128)

st.title("🎨 RGB + LAB Color Mixer")
st.caption("Create and explore colors using RGB and CIELAB values with standard sRGB / D65 conversion.")

tab_rgb, tab_lab = st.tabs(["🔴 RGB Color Mixer", "🌈 LAB Color Mixer"])

with tab_rgb:
    st.subheader("RGB Color Section")
    c1, c2, c3 = st.columns(3)
    with c1: r = st.slider("Red (R)", 0, 255, st.session_state.rgb[0])
    with c2: g = st.slider("Green (G)", 0, 255, st.session_state.rgb[1])
    with c3: b = st.slider("Blue (B)", 0, 255, st.session_state.rgb[2])
    rgb = (r, g, b)
    lab = rgb_to_lab(*rgb)
    st.session_state.rgb = rgb
    show_preview(rgb)
    m1, m2, m3 = st.columns(3)
    m1.metric("RGB", str(rgb))
    m2.metric("HEX", rgb_hex(rgb))
    m3.metric("LAB", f"({lab[0]:.2f}, {lab[1]:.2f}, {lab[2]:.2f})")
    if st.button("💾 Save Current RGB Color"):
        save_color(rgb, lab)
        st.success("Color saved.")

with tab_lab:
    st.subheader("LAB Color Section")
    current_lab = rgb_to_lab(*st.session_state.rgb)
    c1, c2, c3 = st.columns(3)
    with c1: L = st.slider("L* (Lightness)", 0.0, 100.0, float(current_lab[0]), step=0.1)
    with c2: a = st.slider("a* (Green ↔ Red)", -128.0, 127.0, float(max(-128, min(127, current_lab[1]))), step=0.1)
    with c3: bb = st.slider("b* (Blue ↔ Yellow)", -128.0, 127.0, float(max(-128, min(127, current_lab[2]))), step=0.1)
    lab = (L, a, bb)
    rgb = clamp_rgb(lab_to_rgb(*lab))
    show_preview(rgb)
    m1, m2, m3 = st.columns(3)
    m1.metric("LAB", f"({L:.2f}, {a:.2f}, {bb:.2f})")
    m2.metric("RGB", str(rgb))
    m3.metric("HEX", rgb_hex(rgb))
    st.info("LAB colors outside the sRGB display gamut are clipped to valid 0–255 RGB channels for display.")
    if st.button("💾 Save Current LAB Color"):
        save_color(rgb, lab)
        st.success("Color saved.")

st.divider()
st.header("🕘 Color History")
if st.session_state.history:
    if st.button("🗑️ Clear History"):
        st.session_state.history = []
        st.rerun()
    for i, item in enumerate(st.session_state.history, 1):
        c1, c2, c3 = st.columns([1, 3, 3])
        with c1:
            st.markdown(f'<div style="height:55px;border-radius:8px;background:{item["HEX"]};border:1px solid #aaa"></div>', unsafe_allow_html=True)
        with c2:
            st.write(f'**HEX:** {item["HEX"]}')
            st.write(f'**RGB:** {item["RGB"]}')
        with c3:
            st.write(f'**LAB:** {item["LAB"]}')
else:
    st.info("No saved colors yet. Save a color from either mixer tab.")
