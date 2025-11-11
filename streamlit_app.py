# streamlit_app.py (v2)
import streamlit as st
from PIL import Image

def volume(l, w, h): return l * w * h
def iso_factor(level): return 250 if level == "حرارة منخفضة" else 300
def people_btu(n): return max(0, (n - 1) * 600)
def app_btu(watts): return sum(watts) * 3.41
def to_tons(btu): return btu / 12000.0

st.set_page_config(page_title="HAUKIA | حاسبة التبريد", page_icon="❄️", layout="centered")

# session
if "page" not in st.session_state: st.session_state.page = "welcome"
if "watts" not in st.session_state: st.session_state.watts = []
if "theme_dark" not in st.session_state: st.session_state.theme_dark = False

def apply_theme(dark: bool):
    if dark:
        css = """
        <style>
        :root { --bg: #0f172a; --card:#111827; --text:#e5e7eb; --muted:#9ca3af; --primary:#4ea1ff; }
        .block-container { padding-top: 2rem; padding-bottom: 2.5rem; }
        body, .stApp { background: var(--bg); color: var(--text); }
        .stMarkdown, .stText, .stCaption, .stSelectbox label, label { color: var(--text) !important; }
        div[data-testid="stForm"] { background: var(--card); padding: 1.2rem; border-radius: 12px; }
        </style>
        """
    else:
        css = """
        <style>
        :root { --bg:#ffffff; --card:#ffffff; --text:#0f172a; --muted:#6b7280; --primary:#0077FF; }
        .block-container { padding-top: 2rem; padding-bottom: 2.5rem; }
        div[data-testid="stForm"] { background: var(--card); padding: 1.2rem; border-radius: 12px; }
        </style>
        """
    st.markdown(css, unsafe_allow_html=True)

apply_theme(st.session_state.theme_dark)

col_logo, col_title, col_theme = st.columns([2,3,2])
with col_logo:
    logo_path = "assets/logo_dark.png" if st.session_state.theme_dark else "assets/logo_light.png"
    try: st.image(logo_path, use_container_width=False)
    except Exception: pass

with col_theme:
    st.toggle("الوضع الداكن", key="theme_dark", on_change=lambda: st.experimental_rerun())

st.markdown("---")
nav_cols = st.columns(3)
with nav_cols[0]:
    if st.button("الصفحة الرئيسية"): st.session_state.page = "welcome"
with nav_cols[1]:
    if st.button("الحاسبة"): st.session_state.page = "calc"
with nav_cols[2]:
    if st.button("الدعم"): st.session_state.page = "support"

def parse_float(label, value_str):
    s = (value_str or "").strip().replace("،", ".")
    try:
        v = float(s)
        if v <= 0: return None, f"القيمة في {label} يجب أن تكون أكبر من الصفر."
        return v, None
    except Exception:
        return None, f"أدخل رقماً صحيحاً في {label}."

def page_welcome():
    st.markdown("## أهلاً بك في حاسبة التبريد")
    st.caption("هنا يمكنك حساب الطنية واختيار الجهاز المناسب لمختلف المساحات")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("ابدأ الحاسبة ✅", use_container_width=True):
            st.session_state.page = "calc"; st.experimental_rerun()
    with c2:
        if st.button("اذهب إلى الدعم 💙", use_container_width=True):
            st.session_state.page = "support"; st.experimental_rerun()

def page_support():
    st.markdown("## الدعم")
    try: st.image("assets/logo_dark.png" if st.session_state.theme_dark else "assets/logo_light.png", width=260)
    except Exception: pass
    st.write("أدعمني على السوشيال ميديا:")
    st.link_button("Facebook", "https://www.facebook.com/calvinghost/")
    st.link_button("Instagram", "https://instagram.com/g95rr")
    st.link_button("Whatsapp", "https://wa.me/9647716947221")
    st.link_button("Telegram", "https://t.me/g95rr")
    st.link_button("TikTok", "https://tiktok.com/@g95rr")

def page_calc():
    st.markdown("## الحاسبة")
    with st.form("calc_form", clear_on_submit=False):
        colA, colB = st.columns(2)
        with colA:
            length_str = st.text_input("(المتر) الطول", value="", placeholder="مثال: 5.0")
            height_str = st.text_input("(المتر) الارتفاع", value="", placeholder="مثال: 3.0")
        with colB:
            width_str  = st.text_input("(المتر) العرض", value="", placeholder="مثال: 4.0")
            iso        = st.selectbox("أدخل مستوى الحرارة", ["", "حرارة منخفضة", "حرارة عالية"])

        ppl = st.slider("أدخل عدد الأشخاص", 0, 100, 0)

        st.divider()
        st.write("**أدخل الأجهزة الكهربائية (واط):**")
        wcol1, wcol2 = st.columns([3,1])
        with wcol1:
            watt_val = st.text_input("واط", key="watt_input", value="", placeholder="مثال: 1200")
        with wcol2:
            add_clicked = st.form_submit_button("إضافة", use_container_width=True)

        if add_clicked:
            s = (st.session_state.get("watt_input") or "").strip()
            if s.isdigit():
                st.session_state.watts.append(int(s))
                st.session_state.watt_input = ""  # clear without rerun
            else:
                st.warning("أدخل رقماً صحيحاً (واط).")

        if st.session_state.watts:
            st.write("القائمة:", ", ".join(f"{w}W" for w in st.session_state.watts))
            clear = st.form_submit_button("حذف الكل")
            if clear:
                st.session_state.watts.clear()

        calc = st.form_submit_button("أحسب", type="primary", use_container_width=True)

    if calc:
        L, errL = parse_float("الطول", length_str)
        W, errW = parse_float("العرض", width_str)
        H, errH = parse_float("الارتفاع", height_str)
        errs = [e for e in (errL, errW, errH) if e]
        if errs:
            for e in errs: st.error(e); return
        if iso not in ("حرارة منخفضة", "حرارة عالية"): st.error("اختر مستوى الحرارة: منخفضة أو عالية."); return
        room = volume(L, W, H) * iso_factor(iso)
        btu = int(room + people_btu(ppl) + app_btu(st.session_state.watts))
        st.success("تمت العملية بنجاح")
        st.markdown(f"### التبريد المقترح: **{btu:,} BTU**")
        st.caption(f"≈ {to_tons(btu):.2f} طن تبريد")

# Router
if st.session_state.page == "welcome":
    page_welcome()
elif st.session_state.page == "calc":
    page_calc()
else:
    page_support()
