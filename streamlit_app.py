# streamlit_app.py (v3)
import streamlit as st

def volume(l, w, h): return l * w * h
def iso_factor(level): return 250 if level == "حرارة منخفضة" else 300
def people_btu(n): return max(0, (n - 1) * 600)
def app_btu(watts): return sum(watts) * 3.41
def to_tons(btu): return btu / 12000.0

st.set_page_config(page_title="HAUKIA | حاسبة التبريد", page_icon="❄️", layout="centered")

if "page" not in st.session_state: st.session_state.page = "welcome"
if "watts" not in st.session_state: st.session_state.watts = []

def parse_float(label, s):
    s = (s or "").strip().replace("،", ".")
    try:
        v = float(s)
        if v <= 0: return None, f"القيمة في {label} يجب أن تكون أكبر من الصفر."
        return v, None
    except Exception:
        return None, f"أدخل رقماً صحيحاً في {label}."

def header_logo(path, width=420):
    c1, c2, c3 = st.columns([1,2,1])
    with c2: st.image(path, width=width)
    st.markdown("---")

def page_welcome():
    header_logo("assets/logo_haukia.png", 420)
    st.markdown("## أهلاً بك في حاسبة التبريد")
    st.caption("هنا يمكنك حساب الطنية واختيار الجهاز المناسب لمختلف المساحات")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("ابدأ الحاسبة ✅", use_container_width=True):
            st.session_state.page = "calc"; st.rerun()
    with c2:
        if st.button("اذهب إلى الدعم 💙", use_container_width=True):
            st.session_state.page = "support"; st.rerun()

def top_nav():
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("الصفحة الرئيسية"): st.session_state.page = "welcome"; st.rerun()
    with col2:
        if st.button("الحاسبة"): st.session_state.page = "calc"; st.rerun()
    with col3:
        if st.button("الدعم"): st.session_state.page = "support"; st.rerun()

def page_support():
    header_logo("assets/logo_solvion.png", 420)
    top_nav()
    st.subheader("الدعم")
    st.link_button("Facebook", "https://www.facebook.com/calvinghost/")
    st.link_button("Instagram", "https://instagram.com/g95rr")
    st.link_button("Whatsapp", "https://wa.me/9647716947221")
    st.link_button("Telegram", "https://t.me/g95rr")
    st.link_button("TikTok", "https://tiktok.com/@g95rr")

def page_calc():
    header_logo("assets/logo_haukia.png", 420)
    top_nav()
    st.subheader("الحاسبة")
    with st.form("calc_form", clear_on_submit=False):
        ca, cb = st.columns(2)
        with ca:
            l_str = st.text_input("(المتر) الطول", value="", placeholder="مثال: 5.0")
            h_str = st.text_input("(المتر) الارتفاع", value="", placeholder="مثال: 3.0")
        with cb:
            w_str = st.text_input("(المتر) العرض", value="", placeholder="مثال: 4.0")
            iso = st.selectbox("أدخل مستوى الحرارة", ["", "حرارة منخفضة", "حرارة عالية"])
        ppl = st.slider("أدخل عدد الأشخاص", 0, 100, 0)
        calc = st.form_submit_button("أحسب", type="primary", use_container_width=True)

    st.markdown("### الأجهزة الكهربائية (واط)")
    with st.form("appliances_form", clear_on_submit=True):
        c1, c2 = st.columns([3,1])
        with c1:
            watt_str = st.text_input("واط", value="", placeholder="مثال: 1200")
        with c2:
            add = st.form_submit_button("إضافة", use_container_width=True)
        if add:
            s = (watt_str or "").strip()
            if s.isdigit():
                st.session_state.watts.append(int(s))
            else:
                st.warning("أدخل رقماً صحيحاً (واط).")

    if st.session_state.watts:
        colL, colR = st.columns([3,1])
        with colL: st.write("القائمة:", ", ".join(f"{w}W" for w in st.session_state.watts))
        with colR:
            if st.button("حذف الكل", use_container_width=True):
                st.session_state.watts.clear(); st.rerun()

    if calc:
        L, e1 = parse_float("الطول", l_str)
        W, e2 = parse_float("العرض", w_str)
        H, e3 = parse_float("الارتفاع", h_str)
        errs = [e for e in (e1, e2, e3) if e]
        if errs:
            for e in errs: st.error(e)
            return
        if iso not in ("حرارة منخفضة", "حرارة عالية"):
            st.error("اختر مستوى الحرارة: منخفضة أو عالية."); return
        room = volume(L, W, H) * iso_factor(iso)
        btu = int(room + people_btu(ppl) + app_btu(st.session_state.watts))
        st.success("تمت العملية بنجاح")
        st.markdown(f"### التبريد المقترح: **{btu:,} BTU**")
        st.caption(f"≈ {to_tons(btu):.2f} طن تبريد")

if st.session_state.page == "welcome":
    page_welcome()
elif st.session_state.page == "calc":
    page_calc()
else:
    page_support()
