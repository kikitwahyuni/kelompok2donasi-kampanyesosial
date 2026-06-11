import streamlit as st
import copy
import re
from datetime import datetime

st.set_page_config(
    page_title="DonasiKita — Bersama Membantu Sesama",
    page_icon="🤍",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }
    .stApp { background: #fff8f6; }

    .hero {
        background: linear-gradient(145deg, #f9c4ba, #f5a89a);
        border-radius: 20px; padding: 1.6rem 2rem;
        color: #6b2a20; margin-bottom: 1.2rem;
        position: relative; overflow: hidden;
    }
    .hero::before {
        content: "♥"; position: absolute; right: -10px; top: -20px;
        font-size: 7rem; opacity: 0.1; color: #c05040;
    }
    .hero h1 { margin: 0; font-size: 1.7rem; font-weight: 800; letter-spacing: -0.3px; }
    .hero p  { margin: 0.3rem 0 0; font-size: 0.88rem; color: #8b3a2d; font-weight: 500; }
    .hero .tag {
        display: inline-block; background: rgba(255,255,255,0.35);
        border-radius: 20px; padding: 0.2rem 0.9rem;
        font-size: 0.75rem; margin-top: 0.6rem; color: #6b2a20; font-weight: 600;
    }

    .stat-row  { display: flex; gap: 0.8rem; margin-bottom: 1.2rem; }
    .stat-card {
        flex: 1; background: white; border-radius: 14px;
        padding: 0.9rem 0.8rem; text-align: center;
        border: 1px solid #fce8e4;
        box-shadow: 0 3px 12px rgba(230,100,80,0.07);
        transition: transform 0.18s;
    }
    .stat-card:hover { transform: translateY(-2px); }
    .stat-card .icon { font-size: 1.3rem; margin-bottom: 0.2rem; }
    .stat-card .val  { font-size: 1.1rem; font-weight: 800; color: #e05a46; line-height: 1.1; }
    .stat-card .lbl  { font-size: 0.67rem; color: #b0988e; margin-top: 2px; font-weight: 600; }

    .chat-area {
        background: white; border-radius: 16px;
        padding: 1rem 1rem 0.6rem; min-height: 340px; max-height: 400px;
        overflow-y: auto; border: 1px solid #fce8e4;
        box-shadow: 0 4px 16px rgba(230,100,80,0.06); margin-bottom: 0.7rem;
    }
    .empty-chat {
        display: flex; flex-direction: column;
        align-items: center; justify-content: center;
        height: 260px; color: #d4a8a0;
    }
    .empty-chat .ico { font-size: 2.5rem; margin-bottom: 0.5rem; }
    .empty-chat p    { font-size: 0.82rem; text-align: center; max-width: 220px; }

    .msg-wrap-user { display: flex; justify-content: flex-end; margin: 0.35rem 0; }
    .msg-wrap-bot  { display: flex; justify-content: flex-start; margin: 0.35rem 0; }
    .msg-inner { display: flex; flex-direction: column; }
    .msg-inner.user { align-items: flex-end; }
    .msg-inner.bot  { align-items: flex-start; }
    .role-lbl { font-size: 0.62rem; color: #c4a09a; font-weight: 700; letter-spacing: 0.3px; margin-bottom: 2px; }
    .bubble-u {
        background: linear-gradient(135deg, #f5957e, #e8674f);
        color: white; border-radius: 16px 16px 4px 16px;
        padding: 0.6rem 0.95rem; max-width: 72%;
        font-size: 0.85rem; line-height: 1.5;
        box-shadow: 0 3px 10px rgba(230,100,80,0.22); white-space: pre-wrap;
    }
    .bubble-b {
        background: #fff8f6; color: #3a2520;
        border-radius: 16px 16px 16px 4px;
        padding: 0.6rem 0.95rem; max-width: 72%;
        font-size: 0.85rem; line-height: 1.6;
        border: 1px solid #fce8e4;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04); white-space: pre-wrap;
    }

    .stButton > button {
        border-radius: 20px !important; border: 1.5px solid #f5c0b5 !important;
        color: #c05040 !important; background: white !important;
        font-size: 0.78rem !important; font-weight: 700 !important;
        padding: 0.3rem 0.75rem !important; font-family: 'Nunito', sans-serif !important;
        transition: all 0.15s !important; box-shadow: 0 2px 6px rgba(230,100,80,0.08) !important;
    }
    .stButton > button:hover {
        background: #f5957e !important; border-color: #f5957e !important;
        color: white !important; transform: translateY(-1px) !important;
    }
    .donate-btn > button {
        background: linear-gradient(135deg,#f5957e,#e8674f) !important;
        color: white !important; border: none !important;
        font-size: 0.88rem !important; padding: 0.5rem 1rem !important;
    }
    .donate-btn > button:hover { opacity: 0.9 !important; color: white !important; }

    .prog-card {
        background: white; border-radius: 14px; padding: 0.9rem 1rem;
        margin-bottom: 0.7rem; border-left: 4px solid #f5957e;
        box-shadow: 0 3px 10px rgba(230,100,80,0.07);
    }
    .prog-card h4   { margin: 0 0 0.15rem; color: #e05a46; font-size: 0.85rem; font-weight: 800; }
    .prog-card .desc{ font-size: 0.72rem; color: #b0988e; margin-bottom: 0.5rem; }
    .pct-badge {
        display: inline-block; background: #fff0ec; color: #e05a46;
        border-radius: 20px; padding: 1px 8px; font-size: 0.68rem; font-weight: 800; margin-bottom: 5px;
    }
    .new-badge {
        display: inline-block; background: #e05a46; color: white;
        border-radius: 20px; padding: 1px 8px; font-size: 0.65rem; font-weight: 800; margin-left: 5px;
    }
    .bar-bg   { background: #fce8e4; border-radius: 6px; height: 7px; overflow: hidden; margin-bottom: 4px; }
    .bar-fill { background: linear-gradient(90deg,#f5957e,#e8674f); border-radius: 6px; height: 7px; }
    .bar-meta { display: flex; justify-content: space-between; font-size: 0.67rem; }
    .bar-meta .col { color: #e05a46; font-weight: 700; }
    .bar-meta .tar { color: #c4a09a; }

    .sec-lbl {
        font-size: 0.7rem; font-weight: 800; color: #c4a09a;
        letter-spacing: 1px; text-transform: uppercase; margin: 0.9rem 0 0.45rem;
    }

    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input {
        border-radius: 12px !important; border: 1.5px solid #f5c0b5 !important;
        font-family: 'Nunito', sans-serif !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #e8674f !important; box-shadow: 0 0 0 3px rgba(230,100,80,0.1) !important;
    }

    .success-box {
        background: #f0faf2; border: 1px solid #a5d6a7; border-radius: 14px;
        padding: 1rem 1.1rem; font-size: 0.82rem; color: #2e7d32; line-height: 1.8;
    }
    .success-box strong { color: #1b5e20; }

    [data-testid="stSidebar"] { background: #fff8f6 !important; }
    #MainMenu, footer { visibility: hidden; }
    header { visibility: visible; }

    .admin-header {
        background: linear-gradient(135deg, #e8674f, #c05040);
        border-radius: 16px; padding: 1.2rem 1.5rem; color: white; margin-bottom: 1.2rem;
    }
    .admin-header h2 { margin: 0; font-size: 1.3rem; font-weight: 800; }
    .admin-header p  { margin: 0.2rem 0 0; font-size: 0.8rem; opacity: 0.85; }
    .admin-card {
        background: white; border-radius: 14px; padding: 1rem 1.2rem; margin-bottom: 0.8rem;
        border: 1px solid #fce8e4; box-shadow: 0 3px 10px rgba(230,100,80,0.07);
    }
    .admin-card h4 { margin: 0 0 0.3rem; color: #e05a46; font-size: 0.95rem; font-weight: 800; }
</style>
""", unsafe_allow_html=True)

# ─── Kredensial Admin ──────────────────────────────────────────────────────────
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "kelompok2"

# ─── Data Program Bawaan ───────────────────────────────────────────────────────
DATA_PROGRAM = [
    {"nama": "Donasi Pendidikan",   "deskripsi": "Bantu anak-anak kurang mampu raih pendidikan layak", "target": 50_000_000, "terkumpul": 18_500_000},
    {"nama": "Donasi Kesehatan",    "deskripsi": "Akses layanan kesehatan untuk semua kalangan",       "target": 75_000_000, "terkumpul": 31_200_000},
    {"nama": "Bantuan Bencana Alam","deskripsi": "Respons cepat untuk korban bencana di Indonesia",   "target": 30_000_000, "terkumpul": 22_800_000},
]

# ─── Session State ─────────────────────────────────────────────────────────────
defaults = {
    "messages":         [],
    "donation_count":   0,
    "last_donation":    None,
    "show_success":     None,
    "flow_step":        None,
    "flow_data":        {},
    "program_progress": {p["nama"]: p["terkumpul"] for p in DATA_PROGRAM},
    "admin_logged_in":  False,
    "halaman":          "publik",
    "custom_programs":  [],
    "donation_log":     [],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─── Helper ────────────────────────────────────────────────────────────────────
def get_live_data():
    base = copy.deepcopy(DATA_PROGRAM) + copy.deepcopy(st.session_state.get("custom_programs", []))
    for p in base:
        p["terkumpul"] = st.session_state.program_progress.get(p["nama"], p.get("terkumpul", 0))
    return base

def rp(n):     return f"Rp {int(n):,}".replace(",", ".")
def now():     return datetime.now().strftime("%H:%M")
def pct(t, g): return min(round(t / g * 100), 100) if g else 0

def add_msg(role, content):
    st.session_state.messages.append({"role": role, "content": content, "time": now()})

# ─── Chatbot Logic ─────────────────────────────────────────────────────────────
def chatbot_response(text):
    t    = text.lower()
    live = get_live_data()

    def daftar_program():
        return "\n".join(f"• {p['nama']}" for p in live)

    # Trigger alur donasi
    if any(k in t for k in ["donasi sekarang","mulai donasi","ingin donasi","mau donasi","donasi dong"]):
        st.session_state.flow_step = "program"
        st.session_state.flow_data = {}
        return (f"Oke, mari kita mulai! 🤍\n\n"
                f"Silakan ketik nama program donasi yang ingin Anda dukung:\n\n"
                f"{daftar_program()}")

    if any(k in t for k in ["halo","hai","hello","hi","selamat pagi","selamat siang","selamat malam","selamat sore"]):
        return ("Halo! Selamat datang di DonasiKita 🤍\n\n"
                "Saya siap membantu Anda berbagi kebaikan.\n\n"
                "Silakan tanyakan:\n"
                "• Semua program donasi\n"
                "• Cara berdonasi\n"
                "• Kontak kami\n\n"
                "Atau ketik 'donasi sekarang' untuk mulai berdonasi!")

    if any(k in t for k in ["semua","program","apa saja","list","daftar"]):
        hasil = "Berikut program donasi aktif kami:\n\n"
        for i, p in enumerate(live, 1):
            pp = pct(p["terkumpul"], p["target"])
            hasil += f"{i}. {p['nama']}\n   {p['deskripsi']}\n   Progress: {pp}% dari {rp(p['target'])}\n\n"
        hasil += "Ketik 'donasi sekarang' untuk mulai berdonasi!"
        return hasil.strip()

    # Cocokkan nama program secara dinamis (bawaan + custom)
    for p in live:
        kata = p["nama"].lower().split()
        if p["nama"].lower() in t or any(k in t for k in kata):
            pp = pct(p["terkumpul"], p["target"])
            return (f"{p['nama']} 🎯\n\n"
                    f"{p['deskripsi']}\n\n"
                    f"Progress : {pp}% terkumpul\n"
                    f"Terkumpul: {rp(p['terkumpul'])} dari {rp(p['target'])}\n\n"
                    f"Ketik 'donasi sekarang' untuk berdonasi!")

    if any(k in t for k in ["cara","transfer","rekening","bank","gopay","ovo","dana","qris","bayar","nomor"]):
        st.balloons()
        return ("Cara Berdonasi 💝\n\n"
                "━━━━━━━━━━━━━━━━\n"
                "Transfer Bank:\n"
                "  BCA     : 1234567890\n"
                "  Mandiri : 0987654321\n"
                "  a.n Yayasan DonasiKita\n\n"
                "━━━━━━━━━━━━━━━━\n"
                "Dompet Digital:\n"
                "  GoPay / OVO / Dana : 081215376856\n\n"
                "━━━━━━━━━━━━━━━━\n"
                "Kirim bukti ke WhatsApp:\n"
                "📲 wa.me/6281215376856\n\n"
                "Atau ketik 'donasi sekarang' untuk panduan langsung!")

    if any(k in t for k in ["kontak","hubungi","whatsapp","telepon","email","alamat"]):
        return ("Hubungi Kami 📞\n\n"
                "WhatsApp : wa.me/6281215376856\n"
                "Email    : donasi@donasikita.org\n"
                "Alamat   : Jl. Peduli No. 1, Jakarta\n\n"
                "Jam Layanan:\n"
                "Senin–Jumat : 08.00–17.00 WIB\n"
                "Sabtu       : 08.00–13.00 WIB")

    if any(k in t for k in ["terima kasih","makasih","thanks","thank you"]):
        return ("Sama-sama! 🤍\n\n"
                "Kebaikan Anda sangat berarti bagi mereka yang membutuhkan.\n"
                "Semoga menjadi amal jariyah yang terus mengalir.\n\n"
                "Ada yang bisa saya bantu lagi?")

    return (f"Maaf, saya belum memahami pertanyaan itu 🙏\n\n"
            f"Coba tanyakan:\n"
            f"• 'semua program'\n"
            f"• nama program donasi\n"
            f"• 'cara donasi'\n"
            f"• 'kontak'\n\n"
            f"Program aktif:\n{daftar_program()}\n\n"
            f"Atau ketik 'donasi sekarang' untuk mulai berdonasi!")

# ─── Render Progress Cards ─────────────────────────────────────────────────────
def render_progress_cards(highlight=None):
    for p in get_live_data():
        pp    = pct(p["terkumpul"], p["target"])
        badge = '<span class="new-badge">+update</span>' if highlight == p["nama"] else ""
        st.markdown(f"""
        <div class="prog-card">
            <h4>{p['nama']} {badge}</h4>
            <p class="desc">{p['deskripsi']}</p>
            <span class="pct-badge">{pp}% tercapai</span>
            <div class="bar-bg"><div class="bar-fill" style="width:{pp}%"></div></div>
            <div class="bar-meta">
                <span class="col">Terkumpul: {rp(p['terkumpul'])}</span>
                <span class="tar">Target: {rp(p['target'])}</span>
            </div>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🤍 DonasiKita")
    st.markdown("---")
    if st.session_state.admin_logged_in:
        st.success("Login sebagai **admin**")
        if st.button("📊 Dashboard Admin", use_container_width=True):
            st.session_state.halaman = "admin"
            st.rerun()
        if st.button("🌐 Halaman Publik", use_container_width=True):
            st.session_state.halaman = "publik"
            st.rerun()
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.admin_logged_in = False
            st.session_state.halaman = "publik"
            st.rerun()
    else:
        st.markdown("##### 🔐 Login Admin")
        sb_usr = st.text_input("Username", key="sb_usr")
        sb_pwd = st.text_input("Password", type="password", key="sb_pwd")
        if st.button("Login", use_container_width=True, key="sb_login"):
            if sb_usr == ADMIN_USERNAME and sb_pwd == ADMIN_PASSWORD:
                st.session_state.admin_logged_in = True
                st.session_state.halaman = "admin"
                st.rerun()
            else:
                st.error("Username atau password salah!")

# ══════════════════════════════════════════════════════════════════════════════
# HALAMAN ADMIN
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.halaman == "admin" and st.session_state.admin_logged_in:

    st.markdown("""
    <div class="admin-header">
        <h2>⚙️ Dashboard Admin</h2>
        <p>Kelola program donasi, pantau progress, dan lihat riwayat donasi</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📋 Kelola Program", "➕ Tambah Program", "📜 Riwayat Donasi"])

    with tab1:
        st.markdown("### Program Aktif")
        for i, p in enumerate(get_live_data()):
            with st.expander(f"🎯 {p['nama']} — {pct(p['terkumpul'], p['target'])}% tercapai"):
                col_a, col_b = st.columns(2)
                with col_a:
                    new_nama = st.text_input("Nama Program", value=p["nama"], key=f"adm_nama_{i}")
                    new_desk = st.text_input("Deskripsi",    value=p["deskripsi"], key=f"adm_desk_{i}")
                with col_b:
                    new_target    = st.number_input("Target (Rp)",    value=int(p["target"]),    min_value=1_000_000, step=1_000_000, key=f"adm_target_{i}")
                    new_terkumpul = st.number_input("Terkumpul (Rp)", value=int(p["terkumpul"]), min_value=0,         step=100_000,   key=f"adm_terkumpul_{i}")
                c1, c2, c3 = st.columns(3)
                with c1:
                    if st.button("💾 Simpan", key=f"adm_save_{i}", use_container_width=True):
                        for dp in DATA_PROGRAM:
                            if dp["nama"] == p["nama"]:
                                dp["nama"] = new_nama; dp["deskripsi"] = new_desk; dp["target"] = new_target
                                break
                        for cp in st.session_state.custom_programs:
                            if cp["nama"] == p["nama"]:
                                cp["nama"] = new_nama; cp["deskripsi"] = new_desk; cp["target"] = new_target
                                break
                        st.session_state.program_progress.pop(p["nama"], None)
                        st.session_state.program_progress[new_nama] = new_terkumpul
                        st.success(f"Program '{new_nama}' diperbarui!")
                        st.rerun()
                with c2:
                    if st.button("🔄 Reset", key=f"adm_reset_{i}", use_container_width=True):
                        st.session_state.program_progress[p["nama"]] = 0
                        st.success(f"Progress '{p['nama']}' direset!")
                        st.rerun()
                with c3:
                    is_custom = any(cp["nama"] == p["nama"] for cp in st.session_state.custom_programs)
                    if is_custom:
                        if st.button("🗑️ Hapus", key=f"adm_del_{i}", use_container_width=True):
                            st.session_state.custom_programs = [cp for cp in st.session_state.custom_programs if cp["nama"] != p["nama"]]
                            st.session_state.program_progress.pop(p["nama"], None)
                            st.success(f"Program '{p['nama']}' dihapus!")
                            st.rerun()
                    else:
                        st.caption("Program bawaan tidak bisa dihapus")

    with tab2:
        st.markdown("### Tambah Program Baru")
        t_nama   = st.text_input("Nama Program *",  placeholder="cth: Donasi Masjid", key="new_nama")
        t_desk   = st.text_input("Deskripsi *",     placeholder="cth: Pembangunan masjid desa", key="new_desk")
        t_target = st.number_input("Target Dana (Rp) *", min_value=1_000_000, value=10_000_000, step=1_000_000, key="new_target")
        t_awal   = st.number_input("Dana Awal (Rp)", min_value=0, value=0, step=100_000, key="new_awal")
        if st.button("✅ Tambah Program", use_container_width=True, key="btn_add_prog"):
            if not t_nama.strip() or not t_desk.strip():
                st.error("Nama dan deskripsi wajib diisi!")
            elif any(p["nama"].lower() == t_nama.strip().lower() for p in get_live_data()):
                st.error("Nama program sudah ada!")
            else:
                new_prog = {"nama": t_nama.strip(), "deskripsi": t_desk.strip(), "target": int(t_target), "terkumpul": int(t_awal)}
                st.session_state.custom_programs.append(new_prog)
                st.session_state.program_progress[new_prog["nama"]] = int(t_awal)
                st.success(f"Program '{new_prog['nama']}' berhasil ditambahkan! 🎉")
                st.rerun()

    with tab3:
        st.markdown("### Riwayat Donasi Masuk")
        log = st.session_state.donation_log
        if not log:
            st.info("Belum ada donasi yang masuk.")
        else:
            total_masuk = sum(d["nominal"] for d in log)
            c1, c2 = st.columns(2)
            c1.metric("Total Donasi Masuk", rp(total_masuk))
            c2.metric("Jumlah Transaksi", f"{len(log)} donasi")
            st.markdown("---")
            for d in reversed(log):
                st.markdown(f"""
                <div class="admin-card">
                    <h4>{d['nama']} &nbsp;·&nbsp; {d['waktu']}</h4>
                    <span style="color:#3a2520;font-size:0.82rem">
                        📂 {d['program']} &nbsp;|&nbsp; 💰 {rp(d['nominal'])} &nbsp;|&nbsp; 🏦 {d['metode']}
                    </span>
                </div>""", unsafe_allow_html=True)
            if st.button("🗑️ Hapus Semua Riwayat", key="clear_log"):
                st.session_state.donation_log = []
                st.rerun()

    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# HALAMAN LOGIN ADMIN (jika diakses via tombol)
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.halaman == "login_admin":
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.markdown("### 🔐 Login Admin")
        login_usr = st.text_input("Username", key="login_usr")
        login_pwd = st.text_input("Password", type="password", key="login_pwd")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("✅ Login", use_container_width=True, key="btn_do_login"):
                if login_usr == ADMIN_USERNAME and login_pwd == ADMIN_PASSWORD:
                    st.session_state.admin_logged_in = True
                    st.session_state.halaman = "admin"
                    st.rerun()
                else:
                    st.error("Username atau password salah!")
        with col_b:
            if st.button("← Kembali", use_container_width=True, key="btn_back"):
                st.session_state.halaman = "publik"
                st.rerun()
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# HALAMAN PUBLIK
# ══════════════════════════════════════════════════════════════════════════════

# Tombol admin kecil di kanan atas
if not st.session_state.admin_logged_in:
    _, btn_col = st.columns([9, 1])
    with btn_col:
        if st.button("🔐 Admin", key="btn_admin_top"):
            st.session_state.halaman = "login_admin"
            st.rerun()

data = get_live_data()
main_col, info_col = st.columns([3, 2], gap="large")

# ── KOLOM KIRI — Chat ──────────────────────────────────────────────────────────
with main_col:
    st.markdown("""
    <div class="hero">
        <h1>🤍 DonasiKita</h1>
        <p>Asisten donasi siap membantu Anda berbagi kebaikan</p>
        <span class="tag">✨ Satu langkah kecilmu, perubahan besar bagi mereka</span>
    </div>
    """, unsafe_allow_html=True)

    total_target    = sum(p["target"]    for p in data)
    total_terkumpul = sum(p["terkumpul"] for p in data)
    pct_total       = pct(total_terkumpul, total_target)

    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-card"><div class="icon">📋</div><div class="val">{len(data)}</div><div class="lbl">Program Aktif</div></div>
        <div class="stat-card"><div class="icon">📈</div><div class="val">{rp(total_terkumpul)}</div><div class="lbl">Total Terkumpul</div></div>
        <div class="stat-card"><div class="icon">🎯</div><div class="val">{pct_total}%</div><div class="lbl">Progress</div></div>
        <div class="stat-card"><div class="icon">💝</div><div class="val">{st.session_state.donation_count}</div><div class="lbl">Donasi Masuk</div></div>
    </div>
    """, unsafe_allow_html=True)

    # Quick Buttons
    st.markdown('<div class="sec-lbl">💡 Pertanyaan Cepat</div>', unsafe_allow_html=True)
    q_cols = st.columns(5)
    quick_map = {
        "📚 Pendidikan":  "pendidikan",
        "🏥 Kesehatan":   "kesehatan",
        "🌋 Bencana":     "bencana",
        "💳 Cara Donasi": "cara donasi",
        "📋 Semua":       "semua program",
    }
    for col, (label, query) in zip(q_cols, quick_map.items()):
        with col:
            if st.button(label, use_container_width=True, key=f"q_{label}"):
                add_msg("user", label)
                reply = chatbot_response(query)
                if reply:
                    add_msg("assistant", reply)
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="donate-btn">', unsafe_allow_html=True)
        if st.button("🤍 Donasi Sekarang", use_container_width=True, key="btn_donasi"):
            add_msg("user", "donasi sekarang")
            reply = chatbot_response("donasi sekarang")
            if reply:
                add_msg("assistant", reply)
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Chat Display
    st.markdown('<div class="sec-lbl" style="margin-top:1rem">💬 Percakapan</div>', unsafe_allow_html=True)
    chat_html = '<div class="chat-area">'
    if not st.session_state.messages:
        chat_html += """
        <div class="empty-chat">
            <div class="ico">🤍</div>
            <p>Hai! Mulai percakapan dengan mengetik pertanyaan atau klik tombol di atas.</p>
        </div>"""
    else:
        for msg in st.session_state.messages:
            t_str = msg.get("time", "")
            c     = msg["content"].replace("\n", "<br>")
            if msg["role"] == "user":
                chat_html += f"""
                <div class="msg-wrap-user"><div class="msg-inner user">
                    <div class="role-lbl">Anda · {t_str}</div>
                    <div class="bubble-u">{c}</div>
                </div></div>"""
            else:
                chat_html += f"""
                <div class="msg-wrap-bot"><div class="msg-inner bot">
                    <div class="role-lbl">🤍 DonasiBot · {t_str}</div>
                    <div class="bubble-b">{c}</div>
                </div></div>"""
    chat_html += "</div>"
    st.markdown(chat_html, unsafe_allow_html=True)

    # Chat Input
    user_input = st.chat_input("Ketik pertanyaan atau jawaban Anda di sini...")
    if user_input:
        add_msg("user", user_input)
        flow_now = st.session_state.flow_step
        t_input  = user_input.lower().strip()

        if flow_now == "program":
            matched = None
            for p in get_live_data():
                nama_lower = p["nama"].lower()
                if nama_lower == t_input or nama_lower in t_input or any(k in t_input for k in nama_lower.split()):
                    matched = p["nama"]
                    break
            if matched:
                st.session_state.flow_data["program"] = matched
                st.session_state.flow_step = "nominal"
                add_msg("assistant",
                    f"Program dipilih: {matched} ✅\n\n"
                    f"Sekarang, berapa nominal donasi Anda?\n\n"
                    f"Contoh: '50rb', '100 ribu', '250000', '1 juta'")
            else:
                add_msg("assistant",
                    f"Maaf, program tidak ditemukan 🙏\n\n"
                    f"Ketik salah satu:\n" + "\n".join(f"• {p['nama']}" for p in get_live_data()))

        elif flow_now in ("nominal", "nominal_custom"):
            nominal = None
            t2 = (t_input
                .replace("ribu","000").replace("rb","000")
                .replace("juta","000000").replace("jt","000000")
                .replace("lima puluh","50").replace("seratus","100")
                .replace("dua ratus lima puluh","250").replace("dua ratus","200")
                .replace("lima ratus","500").replace("satu juta","1000000")
                .replace(".","").replace(",",""))
            nums = re.findall(r'\d+', t2)
            if nums:
                candidates = []
                for n in nums:
                    val = int(n)
                    if val < 1000:
                        val = val * 1000
                    candidates.append(val)
                nominal = max(candidates) if candidates else None
            if nominal and nominal >= 1000:
                st.session_state.flow_data["nominal"] = nominal
                st.session_state.flow_step = "metode"
                add_msg("assistant",
                    f"Nominal {rp(nominal)} dicatat ✅\n\n"
                    f"Pilih metode pembayaran:\n\n"
                    f"• Transfer BCA\n• Transfer Mandiri\n• GoPay / OVO / Dana\n• Tunai")
            else:
                add_msg("assistant",
                    "Maaf, nominal tidak terbaca 🙏\n\n"
                    "Coba ketik seperti ini:\n"
                    "• '50rb' atau '50 ribu'\n• '100000'\n• '250 ribu'\n• '1 juta'")

        elif flow_now == "metode":
            metode_map = {
                "bca":"Transfer BCA","mandiri":"Transfer Mandiri",
                "gopay":"GoPay/OVO/Dana","ovo":"GoPay/OVO/Dana","dana":"GoPay/OVO/Dana",
                "dompet":"GoPay/OVO/Dana","digital":"GoPay/OVO/Dana",
                "tunai":"Tunai","cash":"Tunai","langsung":"Tunai",
                "transfer":"Transfer BCA",
            }
            matched_metode = next((v for k, v in metode_map.items() if k in t_input), None)
            if matched_metode:
                st.session_state.flow_data["metode"] = matched_metode
                st.session_state.flow_step = "nama"
                add_msg("assistant",
                    f"Metode {matched_metode} dipilih ✅\n\n"
                    f"Siapa nama donatur? (atau ketik 'anonim' / 'hamba allah')")
            else:
                add_msg("assistant",
                    "Metode tidak dikenali 🙏\n\n"
                    "Ketik salah satu:\n• BCA\n• Mandiri\n• GoPay / OVO / Dana\n• Tunai")

        elif flow_now == "nama":
            nama = user_input.strip() or "Hamba Allah"
            if t_input in ("anonim", "-", "anonymous"):
                nama = "Hamba Allah"
            fd = st.session_state.flow_data
            st.session_state.program_progress[fd["program"]] = \
                st.session_state.program_progress.get(fd["program"], 0) + fd["nominal"]
            st.session_state.donation_count += 1
            st.session_state.last_donation  = fd["program"]
            st.session_state.show_success   = {
                "nama": nama, "program": fd["program"],
                "nominal": fd["nominal"], "metode": fd["metode"]
            }
            st.session_state.donation_log.append({
                "waktu":   datetime.now().strftime("%d/%m/%Y %H:%M"),
                "nama":    nama, "program": fd["program"],
                "nominal": fd["nominal"], "metode": fd["metode"],
            })
            add_msg("assistant",
                f"Terima kasih, {nama}! 🤍\n\n"
                f"Program  : {fd['program']}\n"
                f"Nominal  : {rp(fd['nominal'])}\n"
                f"Metode   : {fd['metode']}\n\n"
                f"Silakan transfer dan kirim bukti ke:\n"
                f"📲 wa.me/6281215376856\n\n"
                f"Jazakallah khairan 🙏")
            st.session_state.flow_step = None
            st.session_state.flow_data = {}

        else:
            reply = chatbot_response(user_input)
            if reply:
                add_msg("assistant", reply)

        st.rerun()

    if st.session_state.messages:
        if st.button("🗑️ Hapus Riwayat Chat", key="clear_chat"):
            st.session_state.messages  = []
            st.session_state.flow_step = None
            st.session_state.flow_data = {}
            st.rerun()

# ── KOLOM KANAN — Progress & Info ─────────────────────────────────────────────
with info_col:
    st.markdown('<div class="sec-lbl">📊 Progress Program</div>', unsafe_allow_html=True)
    render_progress_cards(highlight=st.session_state.last_donation)
    st.session_state.last_donation = None

    if st.session_state.show_success:
        d = st.session_state.show_success
        st.balloons()
        st.markdown(f"""
        <div class="success-box">
            ✅ <strong>Terima kasih, {d['nama']}!</strong><br><br>
            Program &nbsp;: {d['program']}<br>
            Nominal &nbsp;: {rp(d['nominal'])}<br>
            Metode &nbsp;&nbsp;: {d['metode']}<br><br>
            Silakan transfer dan kirim bukti ke:<br>
            📲 <strong>wa.me/6281215376856</strong><br><br>
            Semoga menjadi amal jariyah yang berkah 🙏
        </div>
        """, unsafe_allow_html=True)
        st.session_state.show_success = None

    st.markdown('<div class="sec-lbl" style="margin-top:1rem">💡 Tip</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:white;border-radius:12px;padding:0.85rem 1rem;
                border:1px solid #fce8e4;font-size:0.78rem;color:#7a4a42;line-height:1.7">
        Ketik <strong style="color:#e05a46">"donasi sekarang"</strong> di chat
        atau klik tombol <strong style="color:#e05a46">🤍 Donasi Sekarang</strong>
        untuk panduan donasi langkah demi langkah!
    </div>
    """, unsafe_allow_html=True)