import streamlit as st
import pandas as pd
import datetime
import os
import json

# Set page configuration
st.set_page_config(
    page_title="Page & Mood: 나만의 독서 아카이브 & 독립서점 맵",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# JSON Database Persistence Setup
DB_FILE = "books_db.json"

# Default books list (11 books total, including '바다의 철학' and predefined quotes)
DEFAULT_BOOKS = [
    {
        "title": "바다의 철학",
        "author": "군터 슐츠",
        "status": "읽은 책",
        "rating": 5,
        "mood": "🌌 감성적인 새벽녘",
        "review": "이 책은 바다를 철학의 발상지로 보고 철학의 바다를 누비는 특별한 항해를 시도한다. 저자는 최초의 철학자로 여겨지는 탈레스부터 세네카, 플라톤, 헤르더, 칸트, 헤겔, 니체, 야스퍼스와 같은 여러 위대한 철학자들이 공유하고 있던 생각을 ‘바다’를 통해 풀어내며 근본적으로 철학적 사고와 바다가 어떤 관계인지 묻는다. 그동안 우리를 지탱해 온 완고한 대지 저편에 출렁이는 생각의 세계가 존재하고, 이제는 우리가 그곳으로 뛰어들 시간이 왔다는 것이다.\n\n☞ 선정 및 수상내역\n2020 세종도서 교양부문에 선정",
        "quote": "그동안 우리를 지탱해 온 완고한 대지 저편에 출렁이는 생각의 세계가 존재한다.",
        "color": "#0284c7",
        "cover_url": "https://contents.kyobobook.co.kr/sih/fit-in/458x0/pdt/9791189534066.jpg"
    },
    {
        "title": "데미안",
        "author": "헤르만 헤세",
        "status": "읽은 책",
        "rating": 5,
        "mood": "🌌 감성적인 새벽녘",
        "review": "따스한 가정에서 착하게 살아가던 싱클레어 앞에 어느 날 신비한 소년 데미안이 나타나 성서 속 카인과 아벨 이야기로 선악의 진실을 하나씩 가르치기 시작한다. 내면의 선악 사이에서 고뇌하던 싱클레어는 유혹을 이기지 못하고 거리로 나가 금지된 쾌락을 추구하기도 하지만 베아트리체를 만나면서 어두운 내면을 이겨 낸다. 싱클레어가 그린 베아트리체의 초상화는 어딘지 데미안과 닮았다. 데미안에 대한 동경과 강렬한 그리움 때문이다. 그러던 어느 날 싱클레어는 길에서 데미안과 그의 어머니 에바 부인을 만나고, 이후 에바 부인이야말로 자신의 내면에 존재하던 여인이라는 것을 깨닫는다. 얼마 뒤 발발한 전쟁에 참전한 데미안과 싱클레어는 야전 병원에 누워 대화를 나눈다. 자신이 필요할 때면 자기 안에 귀를 기울이라는 말을 남긴 데미안은 다음 날 아침 사라져 버린다.\n『데미안』은 주인공 싱클레어와 데미안의 우정을 바탕으로, 성장 과정에서 겪는 시련과 그 시련의 극복, 깨달음을 통해 완전한 자아에 이르는 과정을 성찰한다. 이 작품은 헤세 자신에게도 재출발을 의미했으며, 소년기의 심리, 엄격한 구도성, 문명 비판, 만물의 근원으로서의 어머니라는 관념 등 헤세의 전, 후기 작품 특징이 고루 나타나 있다.",
        "quote": "새는 알을 깨고 나오려고 투쟁한다. 알은 세계다. 태어나려는 자는 하나의 세계를 깨뜨려야 한다.",
        "color": "#6366f1",
        "cover_url": "https://contents.kyobobook.co.kr/sih/fit-in/458x0/pdt/9788937460449.jpg"
    },
    {
        "title": "도둑맞은 집중력",
        "author": "요한 하리",
        "status": "읽은 책",
        "rating": 4,
        "mood": "🌲 깊은 숲속의 집중",
        "review": "우리의 집중력 저하는 개인의 의지 탓이 아닌 현대 사회의 시스템 문제임을 예리하게 지적한다. 도파민 중독에서 벗어나 몰입을 되찾기 위한 필독서.",
        "quote": "집중력 저하는 개인의 의지 문제가 아니다. 우리의 관심사를 가로채는 현대 시스템의 문제다.",
        "color": "#0ea5e9",
        "cover_url": "https://images.unsplash.com/photo-1506126613408-eca07ce68773?q=80&w=200&auto=format&fit=crop"
    },
    {
        "title": "불편한 편의점",
        "author": "김호연",
        "status": "읽은 책",
        "rating": 5,
        "mood": "☕ 잔잔한 에코 카페",
        "review": "외롭고 힘든 시대를 살아가는 평범한 이웃들이 청파동 골목의 작은 편의점에서 서로 온기를 나누며 치유받는 과정이 매우 따뜻하고 유쾌하게 그려진다.",
        "quote": "결국 삶은 관계였고 관계는 소통이었다. 행복은 내 옆의 사람들과 마음을 나누는 데 있었다.",
        "color": "#10b981",
        "cover_url": "https://images.unsplash.com/photo-1578916171728-46686eac8d58?q=80&w=200&auto=format&fit=crop"
    },
    {
        "title": "사피엔스",
        "author": "유발 하라리",
        "status": "읽은 책",
        "rating": 5,
        "mood": "🌲 깊은 숲속의 집중",
        "review": "인류가 어떻게 다른 생명체들을 지배하고 문명을 일구어냈는지 인지혁명, 농업혁명, 과학혁명을 통해 통찰력 있게 짚어내는 명저입니다.",
        "quote": "상상의 질서가 창조한 권력이 인류를 가장 힘센 지배자로 만들었다.",
        "color": "#22c55e",
        "cover_url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=200&auto=format&fit=crop"
    },
    {
        "title": "미드나잇 라이브러리",
        "author": "맷 헤이그",
        "status": "읽은 책",
        "rating": 4,
        "mood": "🌌 감성적인 새벽녘",
        "review": "죽기 직전 열리는 마법의 도서관에서 자신이 후회했던 다른 선택의 삶들을 살아보며, 평범한 현재의 삶이 얼마나 소중하고 찬란한지 느끼게 해줍니다.",
        "quote": "살아보지 않고는 결코 깨달을 수 없다. 후회하는 일을 멈출 때에야 비로소 삶이 시작된다.",
        "color": "#ec4899",
        "cover_url": "https://images.unsplash.com/photo-1507842217343-583bb7270b66?q=80&w=200&auto=format&fit=crop"
    },
    # 앞으로 읽고 싶은 책들
    {
        "title": "코스모스",
        "author": "칼 세이건",
        "status": "읽고 싶은 책",
        "rating": 0,
        "mood": "🌲 깊은 숲속의 집중",
        "review": "광활한 우주 속에서 인류의 미미하면서도 경이로운 존재를 되짚어보고, 코스모스의 일원으로서 나 자신을 성찰하기 위해 꼭 완독해보고 싶다.",
        "quote": "우리는 우주적 존재다. 우리는 우주가 스스로를 이해하기 위해 만들어낸 한 방편이다.",
        "color": "#a855f7",
        "cover_url": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?q=80&w=200&auto=format&fit=crop"
    },
    {
        "title": "생각의 탄생",
        "author": "로버트 루트번스타인",
        "status": "읽고 싶은 책",
        "rating": 0,
        "mood": "☕ 잔잔한 에코 카페",
        "review": "창조적인 천재들의 13가지 생각 도구들을 배우고 훈련함으로써 나의 사고력을 한 단계 더 창의적으로 확장시키고 싶어 이 책을 선정했다.",
        "quote": "직관과 상상력은 논리적 분석을 만들어내기 전, 창조를 이끌어내는 불씨가 된다.",
        "color": "#f59e0b",
        "cover_url": "https://images.unsplash.com/photo-1499750310107-5fef28a66643?q=80&w=200&auto=format&fit=crop"
    },
    {
        "title": "마흔에 읽는 쇼펜하우어",
        "author": "강용수",
        "status": "읽고 싶은 책",
        "rating": 0,
        "mood": "🌧️ 비 오는 날의 서재",
        "review": "인생의 본질적인 결핍과 고통을 현명하게 마주하고 위로를 받기 위해, 쇼펜하우어의 날카롭지만 현실적인 철학적 조언들을 읽고 싶다.",
        "quote": "삶은 결핍과 충족 사이를 흔들리는 시계추와 같다. 고통 속에서 깊은 나를 발견하게 된다.",
        "color": "#ef4444",
        "cover_url": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=200&auto=format&fit=crop"
    },
    {
        "title": "도파민네이션",
        "author": "애나 렘키",
        "status": "읽고 싶은 책",
        "rating": 0,
        "mood": "🌲 깊은 숲속의 집중",
        "review": "끊임없이 즉각적인 쾌락을 좇는 스마트폰과 중독 시대 속에서, 고통과 쾌락의 저울을 정상화하는 뇌과학적 관점의 조율법을 배우고자 합니다.",
        "quote": "쾌락의 보상을 너무 자주 탐닉하면, 우리의 저울은 고통 쪽으로 기울어져 불행해진다.",
        "color": "#06b6d4",
        "cover_url": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=200&auto=format&fit=crop"
    },
    {
        "title": "클린 코드",
        "author": "robert C. 마틴",
        "status": "읽고 싶은 책",
        "rating": 0,
        "mood": "☕ 잔잔한 에코 카페",
        "review": "가독성 높고 유지보수하기 쉬운 클린 코드를 만들기 위한 설계 원칙과 리팩터링 철학을 내재화하여 실력 있는 엔지니어로 거듭나기 위해.",
        "quote": "깨끗한 코드는 읽기 쉽고 고치기 쉽다. 프로그래머의 정성이 녹아든 예술품이다.",
        "color": "#eab308",
        "cover_url": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?q=80&w=200&auto=format&fit=crop"
    }
]

def load_books():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                books = json.load(f)
                
                # Database Schema Migration (add quote field if missing, auto-fill default quotes)
                default_quotes = {b["title"]: b["quote"] for b in DEFAULT_BOOKS}
                modified = False
                for b in books:
                    if "quote" not in b:
                        b["quote"] = default_quotes.get(b["title"], "")
                        modified = True
                
                if modified:
                    save_books(books)
                return books
        except Exception:
            return DEFAULT_BOOKS
    else:
        save_books(DEFAULT_BOOKS)
        return DEFAULT_BOOKS

def save_books(books):
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(books, f, ensure_ascii=False, indent=4)
    except Exception as e:
        st.error(f"데이터 저장 실패: {e}")

# Initialize session state variables
if "selected_book" not in st.session_state:
    st.session_state.selected_book = None
if "selected_book_idx" not in st.session_state:
    st.session_state.selected_book_idx = None
if "editing_book_idx" not in st.session_state:
    st.session_state.editing_book_idx = None
if "delete_confirm" not in st.session_state:
    st.session_state.delete_confirm = False
if "last_archive_time" not in st.session_state:
    if os.path.exists(DB_FILE):
        mtime = os.path.getmtime(DB_FILE)
        dt = datetime.datetime.fromtimestamp(mtime)
        st.session_state.last_archive_time = dt.strftime("%Y년 %m월 %d일 %H시 %M분")
    else:
        st.session_state.last_archive_time = datetime.datetime.now().strftime("%Y년 %m월 %d일 %H시 %M분")

# Load books from database file into session state
if "books" not in st.session_state:
    st.session_state.books = load_books()

# Global Custom CSS for styling the entire app (Glassmorphism, animations & horizontal cards)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');
    
    /* Universal Font Override */
    html, body, [class*="st-"], [class*="stEmotionCache"], p, div, span, h1, h2, h3, h4, h5, h6, label, button, input {
        font-family: 'Noto Sans KR', sans-serif !important;
    }
    
    /* Header Card */
    .main-header {
        background: linear-gradient(135deg, #1e1b4b 0%, #311042 50%, #4c0519 100%);
        padding: 40px 30px;
        border-radius: 24px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .main-header::before {
        content: "";
        position: absolute;
        top: -50%;
        right: -10%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(168, 85, 247, 0.3) 0%, transparent 70%);
        border-radius: 50%;
        pointer-events: none;
    }
    .main-header::after {
        content: "";
        position: absolute;
        bottom: -50%;
        left: -10%;
        width: 350px;
        height: 350px;
        background: radial-gradient(circle, rgba(99, 102, 241, 0.25) 0%, transparent 70%);
        border-radius: 50%;
        pointer-events: none;
    }
    .header-tag {
        background: rgba(255, 255, 255, 0.12);
        padding: 5px 12px;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        display: inline-block;
        margin-bottom: 15px;
        backdrop-filter: blur(5px);
    }
    .header-title {
        font-size: 2.8rem;
        font-weight: 800;
        margin: 0;
        line-height: 1.2;
        background: linear-gradient(to right, #ffffff, #e9d5ff, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .header-subtitle {
        font-size: 1.15rem;
        opacity: 0.85;
        margin-top: 10px;
        font-weight: 300;
        color: #f3e8ff;
    }
    
    /* Animation */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(15px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Glassmorphism Horizontal Book Card */
    .book-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 18px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        height: 220px;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        animation: fadeInUp 0.5s ease-out both;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        margin-bottom: 10px;
    }
    .book-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
        border-color: rgba(255, 255, 255, 0.18);
        background: rgba(255, 255, 255, 0.06);
    }
    .book-card-content {
        display: flex;
        gap: 15px;
        height: 100%;
        width: 100%;
        overflow: hidden;
    }
    .book-cover-wrapper {
        flex-shrink: 0;
        width: 95px;
        height: 135px;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0,0,0,0.35);
        border: 1px solid rgba(255,255,255,0.1);
        align-self: center;
    }
    .book-cover-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    .book-info {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        flex-grow: 1;
        overflow: hidden;
    }
    .book-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }
    .status-badge {
        padding: 3px 9px;
        border-radius: 50px;
        font-size: 0.65rem;
        font-weight: 700;
    }
    .status-read {
        background-color: rgba(16, 185, 129, 0.12);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.25);
    }
    .status-wish {
        background-color: rgba(14, 165, 233, 0.12);
        color: #38bdf8;
        border: 1px solid rgba(14, 165, 233, 0.25);
    }
    .mood-tag {
        font-size: 0.65rem;
        color: #cbd5e1;
        background: rgba(255, 255, 255, 0.05);
        padding: 3px 8px;
        border-radius: 6px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .book-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #f8fafc;
        margin: 0 0 3px 0;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    .book-author {
        font-size: 0.8rem;
        color: #94a3b8;
        margin: 0 0 8px 0;
        font-weight: 400;
    }
    .rating-stars {
        color: #fbbf24;
        font-size: 0.8rem;
        margin-bottom: 6px;
    }
    .book-review {
        font-size: 0.8rem;
        color: #cbd5e1;
        line-height: 1.45;
        margin: 4px 0 0 0;
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        flex-grow: 1;
    }
    
    /* Bookstore Card Style */
    .store-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 12px;
        transition: all 0.25s ease;
        animation: fadeInUp 0.4s ease-out both;
    }
    .store-card:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: rgba(139, 92, 246, 0.3);
        transform: translateX(3px);
    }
    .store-name {
        font-size: 1.15rem;
        font-weight: 700;
        color: #ffffff;
    }
    .store-badge {
        background: rgba(139, 92, 246, 0.1);
        color: #c084fc;
        border: 1px solid rgba(139, 92, 246, 0.2);
        padding: 2px 7px;
        border-radius: 50px;
        font-size: 0.65rem;
        font-weight: 600;
        margin-left: 5px;
        display: inline-block;
    }
    .store-desc {
        font-size: 0.8rem;
        color: #cbd5e1;
        margin: 8px 0;
        line-height: 1.55;
    }
    .store-meta {
        font-size: 0.75rem;
        color: #94a3b8;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    /* Sidebar styling enhancements */
    .sidebar-profile {
        text-align: center;
        padding: 15px 0 20px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }
    .sidebar-desc {
        font-size: 0.85rem;
        color: #cbd5e1;
        line-height: 1.5;
        margin-top: 10px;
    }
    
    /* Compact BGM Player bar styling */
    .bgm-widget-container {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 12px 18px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 20px;
        backdrop-filter: blur(10px);
    }
    .bgm-info-title {
        font-size: 0.9rem;
        font-weight: 700;
        color: #c084fc;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .bgm-info-desc {
        font-size: 0.75rem;
        color: #94a3b8;
        margin: 2px 0 0 0;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------- DETAIL DIALOG FUNCTION -----------------
@st.dialog("📖 도서 상세 정보")
def show_detail_dialog():
    book_idx = st.session_state.selected_book_idx
    if book_idx is None or book_idx >= len(st.session_state.books):
        st.session_state.selected_book = None
        st.session_state.selected_book_idx = None
        st.session_state.editing_book_idx = None
        st.rerun()
        return

    book = st.session_state.books[book_idx]
    
    # Check if we are in edit mode
    is_editing = (st.session_state.editing_book_idx == book_idx)
    
    if not is_editing:
        if st.session_state.delete_confirm:
            st.markdown(f"⚠️ **정말 '{book['title']}' 도서를 책장에서 영구히 삭제하시겠습니까?**")
            st.write("삭제된 데이터는 복구할 수 없습니다.")
            st.divider()
            confirm_col1, confirm_col2 = st.columns(2)
            with confirm_col1:
                if st.button("🔴 예, 삭제합니다", width='stretch'):
                    st.session_state.books.pop(book_idx)
                    save_books(st.session_state.books)
                    st.session_state.last_archive_time = datetime.datetime.now().strftime("%Y년 %m월 %d일 %H시 %M분")
                    
                    st.session_state.selected_book = None
                    st.session_state.selected_book_idx = None
                    st.session_state.editing_book_idx = None
                    st.session_state.delete_confirm = False
                    st.success("도서가 성공적으로 삭제되었습니다.")
                    st.rerun()
            with confirm_col2:
                if st.button("취소", width='stretch'):
                    st.session_state.delete_confirm = False
                    st.rerun()
        else:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(book['cover_url'], width='stretch')
            with col2:
                st.markdown(f"도서명: {book['title']}")
                st.markdown(f"저자: {book['author']}")
                st.markdown(f"분류: {book['status']}")
                st.markdown(f"추천 독서 무드: {book['mood']}")
                
                if book['status'] == "읽은 책":
                    stars = "★" * book['rating'] + "☆" * (5 - book['rating'])
                    st.markdown(f"나의 평점: {stars}")
                    
            st.divider()
            st.markdown("책 소개 및 선택하게 된 이유:")
            st.markdown(book['review'])
            
            # Show impressive quote if it exists
            if book.get('quote'):
                st.divider()
                st.markdown("✨ 인상 깊은 구절:")
                st.markdown(f"> *{book['quote']}*")
            
            # Action buttons
            btn_col1, btn_col2, btn_col3 = st.columns(3)
            with btn_col1:
                if st.button("✏️ 수정하기", width='stretch'):
                    st.session_state.editing_book_idx = book_idx
                    st.rerun()
            with btn_col2:
                if st.button("🗑️ 삭제하기", width='stretch'):
                    st.session_state.delete_confirm = True
                    st.rerun()
            with btn_col3:
                if st.button("닫기", width='stretch'):
                    st.session_state.selected_book = None
                    st.session_state.selected_book_idx = None
                    st.session_state.editing_book_idx = None
                    st.session_state.delete_confirm = False
                    st.rerun()
    else:
        st.markdown(f"### ✏️ 도서 정보 수정: **{book['title']}**")
        
        edit_title = st.text_input("도서명", value=book['title'])
        edit_author = st.text_input("저자", value=book['author'])
        edit_status = st.selectbox("분류", ["읽은 책", "읽고 싶은 책"], index=0 if book['status'] == "읽은 책" else 1)
        
        edit_rating = st.slider("나의 별점 (읽은 책만 해당)", 1, 5, value=book['rating'] if book['rating'] > 0 else 5)
        
        moods_list = ["🌧️ 비 오는 날의 서재", "☕ 잔잔한 에코 카페", "🌲 깊은 숲속의 집중", "🌌 감성적인 새벽녘"]
        try:
            mood_index = moods_list.index(book['mood'])
        except ValueError:
            mood_index = 0
            
        edit_mood = st.selectbox(
            "추천 독서 무드",
            moods_list,
            index=mood_index
        )
        
        edit_review = st.text_area("책 소개 및 선택하게 된 이유", value=book['review'])
        edit_quote = st.text_area("인상 깊은 구절", value=book.get('quote', ''))
        edit_color = st.color_picker("카드 포인트 테마 색상", value=book['color'])
        edit_cover_url = st.text_input("도서 표지 이미지 URL", value=book['cover_url'])
        
        st.divider()
        edit_btn_col1, edit_btn_col2 = st.columns(2)
        with edit_btn_col1:
            if st.button("💾 저장", width='stretch'):
                if edit_title and edit_author:
                    # Update global books database
                    st.session_state.books[book_idx] = {
                        "title": edit_title,
                        "author": edit_author,
                        "status": edit_status,
                        "rating": edit_rating if edit_status == "읽은 책" else 0,
                        "mood": edit_mood,
                        "review": edit_review,
                        "quote": edit_quote,
                        "color": edit_color,
                        "cover_url": edit_cover_url
                    }
                    st.session_state.editing_book_idx = None
                    st.session_state.selected_book = st.session_state.books[book_idx]
                    save_books(st.session_state.books) # Persist to JSON
                    st.session_state.last_archive_time = datetime.datetime.now().strftime("%Y년 %m월 %d일 %H시 %M분")
                    st.success("도서 정보가 성공적으로 수정되었습니다.")
                    st.rerun()
                else:
                    st.error("도서명과 저자명을 모두 입력해 주세요.")
        with edit_btn_col2:
            if st.button("❌ 취소", width='stretch'):
                st.session_state.editing_book_idx = None
                st.rerun()

# Trigger detail dialog if selected_book is set in session state
if st.session_state.selected_book is not None:
    show_detail_dialog()

# ----------------- SIDEBAR PROFILE & INPUT FORM -----------------
with st.sidebar:
    st.markdown('<div class="sidebar-profile">', unsafe_allow_html=True)
    
    # Render generated avatar image or fallback
    avatar_path = "profile_reading.png"
    if os.path.exists(avatar_path):
        st.image(avatar_path, width='stretch')
    else:
        st.markdown("<h2 style='text-align:center;'>📖</h2>", unsafe_allow_html=True)
        
    st.markdown("### **취향 깊은 북 아카이버**")
    st.markdown(
        '<p class="sidebar-desc">비즈니스 전공생의 독서 기록 공간입니다.<br>지금까지 축적해 온 독서 발자취와 생각을 아카이빙하고 있습니다.</p>',
        unsafe_allow_html=True
    )
    st.sidebar.markdown(f"🕒 **마지막 아카이브**: {st.session_state.last_archive_time}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Form to add a new book
    st.markdown("### ➕ 책장에 책 추가하기")
    with st.form("add_book_form", clear_on_submit=True):
        new_title = st.text_input("도서명", placeholder="예: 데미안")
        new_author = st.text_input("저자", placeholder="예: 헤르만 헤세")
        new_status = st.selectbox("분류", ["읽은 책", "읽고 싶은 책"])
        
        # Rating is only relevant for read books
        new_rating = st.slider("나의 별점 (읽은 책만 해당)", 1, 5, 5)
        
        new_mood = st.selectbox(
            "추천 독서 무드",
            ["🌧️ 비 오는 날의 서재", "☕ 잔잔한 에코 카페", "🌲 깊은 숲속의 집중", "🌌 감성적인 새벽녘"]
        )
        
        new_review = st.text_area("책 소개 및 선택하게 된 이유", placeholder="이 책에 대한 소개나 선택하게 된 이유를 적어주세요.")
        new_quote = st.text_area("인상 깊은 구절 (선택)", placeholder="기억에 남는 인상 깊은 구절을 적어주세요.")
        
        # Color accent selector for book card border
        new_color = st.color_picker("카드 포인트 테마 색상", "#8b5cf6")
        
        # Cover Image URL Input (with aesthetic default cover)
        new_cover_url = st.text_input("도서 표지 이미지 URL (선택)", value="https://images.unsplash.com/photo-1544947950-fa07a98d237f?q=80&w=200")
        
        submit_btn = st.form_submit_button("책장에 추가")
        
        if submit_btn:
            if new_title and new_author:
                # Add to session state
                st.session_state.books.insert(0, {
                    "title": new_title,
                    "author": new_author,
                    "status": new_status,
                    "rating": new_rating if new_status == "읽은 책" else 0,
                    "mood": new_mood,
                    "review": new_review if new_review else "기록된 소개가 없습니다.",
                    "quote": new_quote,
                    "color": new_color,
                    "cover_url": new_cover_url
                })
                save_books(st.session_state.books) # Persist to JSON
                st.session_state.last_archive_time = datetime.datetime.now().strftime("%Y년 %m월 %d일 %H시 %M분")
                st.success(f"'{new_title}' 도서가 책장에 추가되었습니다!")
                st.rerun()
            else:
                st.warning("도서명과 저자명을 모두 입력해 주세요.")

# ----------------- MAIN VIEW & BANNERS -----------------
# Header HTML
st.markdown("""
    <div class="main-header">
        <span class="header-tag">Web Deployment Project</span>
        <h1 class="header-title">Page & Mood</h1>
        <p class="header-subtitle">나만의 독서 아카이브 & 감성 독립서점 가이드</p>
    </div>
""", unsafe_allow_html=True)

# Define Independent Bookstores Database (Seoul)
bookstores = [
    {
        "name": "유어마인드 (Your Mind)",
        "latitude": 37.568393,
        "longitude": 126.931165,
        "region": "서대문구 (연희동)",
        "theme": "🎨 독립출판 & 아트북",
        "address": "서울 서대문구 연희로11라길 10-6 2층",
        "description": "국내외 독립출판물, 소규모 브랜드의 문구 및 아트북을 유통하는 대표적인 독립서점입니다. 오래된 주택을 개조한 평화로운 분위기 속에서 취향 가득한 서적을 탐색할 수 있습니다.",
        "link": "https://your-mind.com"
    },
    {
        "name": "당인리책발전소 (Danginri Book Plant)",
        "latitude": 37.547167,
        "longitude": 126.918239,
        "region": "마포구 (합정동)",
        "theme": "☕ 북카페 & 큐레이션",
        "address": "서울 마포구 독막로8길 15",
        "description": "김소영, 오상진 아나운서 부부가 운영하는 감성적인 분위기의 북카페 서점입니다. 매주 인상적인 '서점 주인 추천도서 베스트 10'과 손글씨 코멘터리 큐레이션이 특징입니다.",
        "link": "https://www.instagram.com/danginribookplant"
    },
    {
        "name": "최인아책방 (Choi In-ah Books)",
        "latitude": 37.505295,
        "longitude": 127.042531,
        "region": "강남구 (역삼동)",
        "theme": "🧠 생각의 숲 & 인문학",
        "address": "서울 강남구 선릉로 521",
        "description": "전 제일기획 부사장 최인아가 오픈한 강남의 숨겨진 문화 오아시스. '생각의 숲'을 컨셉으로 하여 명사들의 추천 코멘트와 함께 깊은 영감을 주는 강연/모임이 자주 열립니다.",
        "link": "https://www.instagram.com/inabooks"
    },
    {
        "name": "고요서사 (Goyo Bookshop)",
        "latitude": 37.543419,
        "longitude": 126.987229,
        "region": "용산구 (해방촌)",
        "theme": "✍️ 소설 & 수필 전문",
        "address": "서울 용산구 신흥로15길 18-4",
        "description": "서울 해방촌 골목에 조용히 자리 잡은 소형 문학 전문 서점입니다. 엄선된 한국 및 세계 문학, 에세이, 독립 잡지들을 취급하며 책과 함께 사색할 수 있는 문학 중심 서재입니다.",
        "link": "https://www.instagram.com/goyo_bookshop"
    },
    {
        "name": "역사책방 (History Bookstore)",
        "latitude": 37.578611,
        "longitude": 126.971944,
        "region": "종로구 (통의동)",
        "theme": "📜 역사 & 사회과학",
        "address": "서울 종로구 자하문로10길 24",
        "description": "경복궁 옆 서촌 골목길에 위치한 역사 전문 독립서점. 미세하게 조율된 한국사, 동양사, 서양사 큐레이션부터 인문 사회학적 깊이가 담긴 독서 클럽과 강좌를 제공합니다.",
        "link": "https://www.instagram.com/history_book_shop"
    },
    {
        "name": "살롱드북 (Salon de Book)",
        "latitude": 37.480556,
        "longitude": 126.953056,
        "region": "관악구 (봉천동)",
        "theme": "🍷 낮과 밤의 심야책방",
        "address": "서울 관악구 남부순환로231길 11",
        "description": "낮에는 책을, 밤에는 위스키와 와인을 즐길 수 있는 특별한 분위기의 독립서점. 아늑하고 살롱 같은 공간에서 낯선 책을 접하고 다른 독서가들과 교류하는 경험을 선사합니다.",
        "link": "https://www.instagram.com/salondebook"
    }
]

# Create standard Streamlit tabs for primary content navigation
tab1, tab2, tab3 = st.tabs(["📚 나의 책장 (Bookshelf)", "🎵 독서 BGM & 타이머", "🗺️ 서울 독립서점 맵"])

# ================= TAB 1: MY BOOKSHELF =================
with tab1:
    # LOFI Background Music Container for Tab 1
    st.markdown("""
        <div class="bgm-widget-container">
            <div>
                <p class="bgm-info-title">🎵 책장 BGM: 24/7 Lo-Fi Chill Beats</p>
                <p class="bgm-info-desc">잔잔하고 세련된 비트와 함께 독서 카드를 넘겨보세요.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.iframe("https://www.youtube.com/embed/36YnV9nHBPc?autoplay=1&loop=1&playlist=36YnV9nHBPc", height=80)
    
    st.subheader("📚 아카이빙된 나의 서재")
    st.write("도서 카드 밑의 **'📖 상세보기'** 버튼을 클릭하시면 책의 상세 이미지와 자세한 감상평 팝업창을 확인하실 수 있습니다.")
    
    # Filters & Search layout
    search_col, filter_col = st.columns([2, 1])
    
    with search_col:
        search_query = st.text_input("🔎 책 이름 또는 작가 검색", placeholder="도서명 또는 저자명을 입력하세요...", label_visibility="collapsed")
        
    with filter_col:
        category_filter = st.selectbox(
            "카테고리 필터:",
            ["전체 책 보기", "읽은 책 (인상 깊었던 도서)", "읽고 싶은 책 (읽을 예정인 도서)"],
            label_visibility="collapsed"
        )
        
    # Apply filters
    filtered_books = st.session_state.books
    
    # 1. Search Query Filter
    if search_query:
        filtered_books = [
            b for b in filtered_books 
            if search_query.lower() in b['title'].lower() or search_query.lower() in b['author'].lower()
        ]
        
    # 2. Category Filter
    if category_filter == "읽은 책 (인상 깊었던 도서)":
        filtered_books = [b for b in filtered_books if b['status'] == "읽은 책"]
    elif category_filter == "읽고 싶은 책 (읽을 예정인 도서)":
        filtered_books = [b for b in filtered_books if b['status'] == "읽고 싶은 책"]
        
    # Render Grid of Cards
    if filtered_books:
        # Create columns (2-column layout for horizontal style with covers)
        cols = st.columns(2)
        for idx, book in enumerate(filtered_books):
            with cols[idx % 2]:
                # Stars mapping
                rating_stars = "★" * book.get("rating", 0) + "☆" * (5 - book.get("rating", 0)) if book.get("status") == "읽은 책" else ""
                
                # Badges
                status_class = "status-read" if book.get("status") == "읽은 책" else "status-wish"
                status_label = book.get("status")
                
                # HTML layout for Horizontal Book Card with Cover Image
                card_html = f"""
                <div class="book-card" style="border-top: 4px solid {book.get('color', '#8b5cf6')};">
                    <div class="book-card-content">
                        <div class="book-cover-wrapper">
                            <img src="{book.get('cover_url')}" class="book-cover-img" onerror="this.src='https://images.unsplash.com/photo-1544947950-fa07a98d237f?q=80&w=200'"/>
                        </div>
                        <div class="book-info">
                            <div class="book-header">
                                <span class="status-badge {status_class}">{status_label}</span>
                                <span class="mood-tag">{book.get('mood', '📝 일반')}</span>
                            </div>
                            <h4 class="book-title">{book.get('title')}</h4>
                            <p class="book-author">by {book.get('author')}</p>
                            {"<div class='rating-stars'>" + rating_stars + "</div>" if rating_stars else ""}
                            <p class="book-review">{book.get('review')}</p>
                        </div>
                    </div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
                
                # Button underneath the card to trigger detail dialog
                if st.button("📖 상세보기", key=f"details_{idx}", width='stretch'):
                    st.session_state.selected_book = book
                    st.session_state.selected_book_idx = st.session_state.books.index(book)
                    st.rerun()
    else:
        st.info("검색 조건에 부합하는 도서가 없습니다. 사이드바를 이용해 새로운 도서를 등록해 보세요!")

# ================= TAB 2: BGM & TIMER =================
with tab2:
    # Jazz Background Music Container for Tab 2
    st.markdown("""
        <div class="bgm-widget-container">
            <div>
                <p class="bgm-info-title">🎵 공간 BGM: 따뜻한 아쿠스틱 카페 재즈 BGM</p>
                <p class="bgm-info-desc">카페에 앉아 조용히 책장을 넘길 때 들리는 감성적인 재즈 음악입니다.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.subheader("🎵 몰입을 위한 소리공간 & 타이머")
    st.write("책을 펼쳐 들고, 마음에 드는 독서용 BGM을 켠 채로 타임박싱을 지정해 독서 루틴을 만들어보세요.")
    
    bgm_col, timer_col = st.columns([1, 1])
    
    with bgm_col:
        st.markdown("### 📻 독서 무드 BGM 채널")
        mood_selection = st.selectbox(
            "원하는 무드를 선택하세요 (기본: 잔잔한 에코 카페 재즈 BGM):",
            ["☕ 잔잔한 에코 카페 (재즈 BGM & 커피숍 소음)", "🌧️ 비 오는 날의 서재 (감성 피아노 & 빗소리)", "🌲 깊은 숲속의 집중 (자연 백색소음 & 새소리)", "🌌 감성적인 새벽녘 (차분한 로파이 라디오)"]
        )
        
        # BGM Player embed links
        bgm_embeds = {
            "☕ 잔잔한 에코 카페 (재즈 BGM & 커피숍 소음)": "https://www.youtube.com/embed/5w3P1nJmQ9Y?autoplay=1&loop=1&playlist=5w3P1nJmQ9Y",
            "🌧️ 비 오는 날의 서재 (감성 피아노 & 빗소리)": "https://www.youtube.com/embed/n42R81vO46I?autoplay=1&loop=1&playlist=n42R81vO46I",
            "🌲 깊은 숲속의 집중 (자연 백색소음 & 새소리)": "https://www.youtube.com/embed/pH0uJg45E4w?autoplay=1&loop=1&playlist=pH0uJg45E4w",
            "🌌 감성적인 새벽녘 (차분한 로파이 라디오)": "https://www.youtube.com/embed/36YnV9nHBPc?autoplay=1&loop=1&playlist=36YnV9nHBPc"
        }
        
        embed_url = bgm_embeds[mood_selection]
        
        # Embedded Player Frame using st.iframe (Streamlit 2026 syntax)
        st.iframe(embed_url, height=240)
        
    with timer_col:
        st.markdown("### ⏱️ 인터랙티브 독서 타이머")
        
        # Elegant HTML/JS Pomodoro Timer
        timer_code = """
        <div class="timer-card">
            <div class="timer-modes">
                <button onclick="setTimer(25)">📚 25분 몰입</button>
                <button onclick="setTimer(50)">🧠 50분 극대화</button>
                <button onclick="setTimer(10)">☕ 10분 휴식</button>
            </div>
            <div class="timer-display" id="time">25:00</div>
            <div class="timer-controls">
                <button id="startBtn" onclick="toggleTimer()">시작</button>
                <button onclick="resetTimer()">리셋</button>
            </div>
        </div>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&family=Noto+Sans+KR:wght@400;700&display=swap');
            body {
                margin: 0;
                padding: 0;
                font-family: 'Outfit', 'Noto Sans KR', sans-serif;
                background: transparent;
                color: #fff;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100%;
            }
            .timer-card {
                background: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 18px;
                padding: 22px;
                text-align: center;
                width: 100%;
                box-sizing: border-box;
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
                backdrop-filter: blur(12px);
            }
            .timer-modes {
                display: flex;
                gap: 8px;
                justify-content: center;
                margin-bottom: 15px;
            }
            .timer-modes button {
                background: rgba(255, 255, 255, 0.06);
                border: 1px solid rgba(255, 255, 255, 0.08);
                color: #cbd5e1;
                padding: 6px 12px;
                border-radius: 50px;
                font-size: 0.75rem;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.2s ease;
            }
            .timer-modes button:hover {
                background: rgba(139, 92, 246, 0.2);
                color: #fff;
                border-color: #8b5cf6;
            }
            .timer-display {
                font-size: 3rem;
                font-weight: 800;
                font-family: 'Outfit', sans-serif;
                margin: 15px 0;
                color: #fff;
                text-shadow: 0 0 15px rgba(139, 92, 246, 0.5);
                letter-spacing: 1px;
            }
            .timer-controls {
                display: flex;
                gap: 12px;
                justify-content: center;
            }
            .timer-controls button {
                padding: 8px 22px;
                border-radius: 50px;
                font-weight: 600;
                font-size: 0.85rem;
                cursor: pointer;
                transition: all 0.2s ease;
            }
            #startBtn {
                background: #8b5cf6;
                color: white;
                border: none;
                box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3);
            }
            #startBtn:hover {
                background: #7c3aed;
                transform: translateY(-2px);
            }
            .timer-controls button:nth-child(2) {
                background: rgba(255, 255, 255, 0.08);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.15);
            }
            .timer-controls button:nth-child(2):hover {
                background: rgba(255, 255, 255, 0.18);
            }
        </style>
        <script>
            let timer;
            let minutes = 25;
            let seconds = 0;
            let isRunning = false;
            
            function updateDisplay() {
                const minStr = String(minutes).padStart(2, '0');
                const secStr = String(seconds).padStart(2, '0');
                document.getElementById('time').innerText = `${minStr}:${secStr}`;
            }
            
            function setTimer(mins) {
                clearInterval(timer);
                minutes = mins;
                seconds = 0;
                isRunning = false;
                document.getElementById('startBtn').innerText = '시작';
                document.getElementById('startBtn').style.background = '#8b5cf6';
                updateDisplay();
            }
            
            function toggleTimer() {
                if (isRunning) {
                    clearInterval(timer);
                    isRunning = false;
                    document.getElementById('startBtn').innerText = '시작';
                    document.getElementById('startBtn').style.background = '#8b5cf6';
                } else {
                    isRunning = true;
                    document.getElementById('startBtn').innerText = '일시정지';
                    document.getElementById('startBtn').style.background = '#ef4444';
                    timer = setInterval(() => {
                        if (seconds === 0) {
                            if (minutes === 0) {
                                clearInterval(timer);
                                alert('독서 집중 시간이 종료되었습니다! 잠시 머리를 식혀보세요.');
                                setTimer(25);
                                return;
                            }
                            minutes--;
                            seconds = 59;
                        } else {
                            seconds--;
                        }
                        updateDisplay();
                    }, 1000);
                }
            }
            
            function resetTimer() {
                setTimer(minutes);
            }
        </script>
        """
        # Embedded timer using st.iframe (Streamlit 2026 syntax)
        st.iframe(timer_code, height=260)

# ================= TAB 3: INDEPENDENT BOOKSTORES MAP =================
with tab3:
    # New Age Background Music Container for Tab 3
    st.markdown("""
        <div class="bgm-widget-container">
            <div>
                <p class="bgm-info-title">🎵 서점 맵 BGM: 서정적인 뉴에이지 피아노곡 모음</p>
                <p class="bgm-info-desc">지도를 따라 서울 곳곳의 골목길 책방들을 마음으로 산책하며 듣기 좋은 아름다운 뉴에이지 피아노 BGM입니다.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.iframe("https://www.youtube.com/embed/WJ3-F02-F_Y?autoplay=1&loop=1&playlist=WJ3-F02-F_Y", height=80)
    
    st.subheader("🗺️ 서울 독립서점 테마 맵")
    st.write("서울 내에서 저마다 독창적인 색깔을 지니고 숨쉬고 있는 대표 독립서점들을 테마별로 만나보세요.")
    
    # Map filters layout
    map_f1, map_f2 = st.columns([1, 1])
    
    with map_f1:
        # Extract unique region areas
        regions_list = sorted(list(set([store['region'].split(" ")[0] for store in bookstores])))
        selected_region = st.selectbox("원하는 지역구 필터:", ["전체 지역"] + regions_list)
        
    with map_f2:
        themes_list = sorted(list(set([store['theme'] for store in bookstores])))
        selected_theme = st.selectbox("원하는 테마 필터:", ["전체 테마"] + themes_list)
        
    # Apply Map Filters
    filtered_stores = bookstores
    if selected_region != "전체 지역":
        filtered_stores = [s for s in filtered_stores if s['region'].startswith(selected_region)]
    if selected_theme != "전체 테마":
        filtered_stores = [s for s in filtered_stores if s['theme'] == selected_theme]
        
    if filtered_stores:
        # Construct dataframe for st.map
        store_df = pd.DataFrame(filtered_stores)
        
        # Interactive Streamlit Map showing locations
        st.map(store_df, latitude='latitude', longitude='longitude', zoom=11)
        
        st.markdown("### 🔍 서점 디렉토리 리스트")
        
        # Render cards below map
        for store in filtered_stores:
            store_html = f"""
            <div class="store-card">
                <div style="display: flex; justify-content: space-between; align-items: start; flex-wrap: wrap;">
                    <div class="store-name">
                        {store['name']}
                        <span class="store-badge">{store['theme']}</span>
                        <span class="store-badge" style="background: rgba(16, 185, 129, 0.1); color: #34d399; border-color: rgba(16, 185, 129, 0.2);">{store['region']}</span>
                    </div>
                </div>
                <p class="store-desc">{store['description']}</p>
                <div class="store-meta">
                    <span>📍 {store['address']}</span>
                    <span>🔗 <a href="{store['link']}" target="_blank" style="color: #c084fc; text-decoration: none; font-weight: 500;">공식 사이트 바로가기</a></span>
                </div>
            </div>
            """
            st.markdown(store_html, unsafe_allow_html=True)
    else:
        st.info("해당 필터 구성에 매칭되는 독립서점이 서치되지 않았습니다. 다른 필터 옵션을 골라주세요.")
