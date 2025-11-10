# streamlit_app.py
import streamlit as st
from PIL import Image

def volume(l, w, h): return l * w * h
def iso_factor(level): return 250 if level == "حرارة منخفضة" else 300
def people_btu(n): return max(0, (n - 1) * 600)
def app_btu(watts): return sum(watts) * 3.41
def to_tons(btu): return btu / 12000.0

st.set_page_config(page_title="HAUKIA | حاسبة التبريد", page_icon="❄️", layout="centered")

st.markdown("<style>.block-container{padding-top:2rem;padding-bottom:2.5rem}</style>", unsafe_allow_html=True)

if "watts" not in st.session_state: st.session_state["watts"] = []
if "new_watt" not in st.session_state: st.session_state["new_watt"] = ""

c1, c2, c3 = st.columns([1,2,1])
with c2:
    try: st.image("assets/logo_light.png", use_container_width=False)
    except Exception: pass

st.markdown("### أهـلا بـك فـي حــاسبة التبــريد")
st.caption("هنا يمكنك حساب الطنية وأختيار الجهاز المناسب لمختلف المساحات")

with st.form("calc_form"):
    colA, colB = st.columns(2)
    with colA:
        length = st.number_input("(المتر) الطول", min_value=0.0, step=0.1, format="%.2f")
        height = st.number_input("(المتر) الارتفاع", min_value=0.0, step=0.1, format="%.2f")
    with colB:
        width  = st.number_input("(المتر) العرض", min_value=0.0, step=0.1, format="%.2f")
        iso    = st.selectbox("أدخل مستوى الحرارة", ["", "حرارة منخفضة", "حرارة عالية"])

    ppl = st.slider("أدخل عدد الأشخاص", 0, 100, 0)

    st.divider()
    st.write("**أدخل الأجهزة الكهربائية (واط):**")
    wcol1, wcol2 = st.columns([3,1])
    with wcol1:
        st.text_input("واط", key="new_watt", placeholder="مثال: 1200")
    with wcol2:
        add_clicked = st.form_submit_button("إضافة", use_container_width=True)

    if add_clicked:
        s = (st.session_state.get("new_watt") or "").strip()
        if s.isdigit():
            st.session_state["watts"].append(int(s))
            st.session_state["new_watt"] = ""
            st.rerun()
        else:
            st.warning("أدخل رقماً صحيحاً (واط).")

    if st.session_state["watts"]:
        st.write("القائمة:", ", ".join(f"{w}W" for w in st.session_state["watts"]))
        clear = st.form_submit_button("حذف الكل")
        if clear:
            st.session_state["watts"].clear()
            st.rerun()

    calc = st.form_submit_button("أحسب", type="primary")

if calc:
    if length <= 0 or width <= 0 or height <= 0:
        st.error("القيم يجب أن تكون أكبر من الصفر.")
    elif iso not in ("حرارة منخفضة", "حرارة عالية"):
        st.error("اختر مستوى الحرارة: منخفضة أو عالية.")
    else:
        room = volume(length, width, height) * iso_factor(iso)
        btu = int(room + people_btu(ppl) + app_btu(st.session_state["watts"]))
        st.success("تمت العملية بنجاح")
        st.markdown(f"### التبريد المقترح: **{btu:,} BTU**")
        st.caption(f"≈ {to_tons(btu):.2f} طن تبريد")

st.divider()
with st.expander("الدعم"):
    st.image("assets/logo_dark.png", use_container_width=False)
    st.link_button("Facebook", "https://www.facebook.com/calvinghost/")
    st.link_button("Instagram", "https://instagram.com/g95rr")
    st.link_button("Whatsapp", "https://wa.me/9647716947221")
    st.link_button("Telegram", "https://t.me/g95rr")
    st.link_button("TikTok", "https://tiktok.com/@g95rr")
