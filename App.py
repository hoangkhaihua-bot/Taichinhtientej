import streamlit as st
import pandas as pd
import math

# Thiết lập cấu hình trang
st.set_page_config(
    page_title="Tính Lãi Gửi Tiết Kiệm & Lãi Kép",
    page_icon="💰",
    layout="centered"
)

# Custom CSS cho giao diện tươi vui, thân thiện
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #6C5CE7;
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 0px;
    }
    .sub-header {
        text-align: center;
        color: #A29BFE;
        font-size: 1.0rem;
        margin-bottom: 25px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #A855F7 0%, #EC4899 100%);
        color: white;
        font-weight: bold;
        border-radius: 12px;
        padding: 10px 24px;
        border: none;
        width: 100%;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(236, 72, 153, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# Hiển thị hình ảnh
col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
with col_img2:
    try:
        st.image("IMG_20260927_092457.jpg", width=160)
    except Exception:
        pass

# Header
st.markdown('<h1 class="main-header">💰 Tính Lãi Gửi Tiết Kiệm</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Tài chính thông minh - Tích lũy tương lai ✨</p>', unsafe_allow_html=True)

st.divider()

# Bảng lãi suất tham chiếu tương ứng với kỳ hạn (%/năm)
DEFAULT_RATES = {
    1: 3.0,
    3: 3.8,
    6: 4.7,
    12: 5.5,
    18: 5.7,
    24: 6.0,
    36: 6.2
}

# Cột nhập liệu
col_input1, col_input2 = st.columns(2)

with col_input1:
    amount = st.number_input(
        "💵 Số tiền gửi ban đầu (VNĐ):",
        min_value=1_000_000,
        value=100_000_000,
        step=5_000_000,
        format="%d"
    )
    
    term_option = st.selectbox(
        "⏳ Chọn kỳ hạn gửi:",
        options=[1, 3, 6, 12, 18, 24, 36, "Khác (Nhập tùy chỉnh)"]
    )
    
    if term_option == "Khác (Nhập tùy chỉnh)":
        term_months = st.number_input("Nhập số tháng gửi:", min_value=1, max_value=120, value=12, step=1)
        suggested_rate = 5.5
    else:
        term_months = int(term_option)
        suggested_rate = DEFAULT_RATES.get(term_months, 5.5)

with col_input2:
    interest_rate = st.number_input(
        "📈 Lãi suất (%/năm):",
        min_value=0.1,
        max_value=30.0,
        value=suggested_rate,
        step=0.1,
        format="%.2f",
        help="Lãi suất tự động gợi ý theo kỳ hạn đã chọn (bạn có thể tự sửa lại)."
    )
    
    interest_type = st.selectbox(
        "🔄 Hình thức nhận / Ghép lãi:",
        options=["Hàng tháng", "Hàng quý", "Cuối kỳ (Ghép lãi theo vòng quay)"]
    )

# Tùy chọn Bật/Tắt Lãi Kép
is_compound = st.checkbox(
    "🔥 Tái nhập gốc tiền lãi khi hết kỳ (Bật Lãi Kép)",
    value=True,
    help="Khi bật tính năng này, tiền lãi sau mỗi kỳ/vòng quay sẽ được dồn vào gốc để tính lãi cho kỳ tiếp theo."
)

# -------------------------------------------------------------
# HÀM TÍNH TOÁN LÃI ĐƠN & LÃI KÉP CHUẨN XÁC
# -------------------------------------------------------------
def calculate_interest_advanced(p, r_annual, months, itype, compound):
    r = r_annual / 100
    t_years = months / 12.0

    if not compound:
        # TÍNH LÃI ĐƠN (Không tái nhập gốc)
        if "Hàng tháng" in itype:
            periodic_interest = p * (r / 12)
            total_interest = periodic_interest * months
            num_periods = months
            period_name = "tháng"
        elif "Hàng quý" in itype:
            periodic_interest = p * (r / 4)
            num_periods = int(months / 3) if months >= 3 else 1
            total_interest = periodic_interest * num_periods
            period_name = "quý"
        else: # Cuối kỳ
            total_interest = p * r * t_years
            periodic_interest = total_interest
            num_periods = 1
            period_name = "cuối kỳ"
        
        total_amount = p + total_interest

    else:
        # TÍNH LÃI KÉP (Tái nhập gốc)
        if "Hàng tháng" in itype:
            n = 12 # 12 lần ghép lãi/năm
            num_periods = months
            period_name = "tháng"
            total_amount = p * math.pow(1 + (r / n), n * t_years)
        elif "Hàng quý" in itype:
            n = 4 # 4 lần ghép lãi/năm
            num_periods = int(months / 3) if months >= 3 else 1
            total_amount = p * math.pow(1 + (r / n), n * t_years)
            period_name = "quý"
        else: # Cuối kỳ (Quay vòng tái nhập gốc theo từng chu kỳ gửi)
            # Ví dụ: Gửi kỳ hạn 12 tháng trong 24 tháng = 2 vòng quay ghép lãi
            n = 12 / months if months <= 12 else 12 / term_months if 'term_months' in locals() else 1
            num_periods = int(math.ceil(months / (12 / n))) if n > 0 else 1
            total_amount = p * math.pow(1 + (r / n), n * t_years)
            period_name = "kỳ quay vòng"

        total_interest = total_amount - p
        periodic_interest = total_interest / num_periods if num_periods > 0 else total_interest

    return periodic_interest, total_interest, total_amount, num_periods, period_name

# Xử lý tính toán
periodic_interest, total_interest, total_amount, num_periods, period_name = calculate_interest_advanced(
    amount, interest_rate, term_months, interest_type, is_compound
)

# -------------------------------------------------------------
# HIỂN THỊ KẾT QUẢ
# -------------------------------------------------------------
st.markdown("### 📊 Kết Quả Tính Toán")

col1, col2, col3 = st.columns(3)

with col1:
    if "Cuối kỳ" in interest_type and not is_compound:
        st.metric(
            label="Tiền lãi nhận cuối kỳ",
            value=f"{total_interest:,.0f} đ".replace(",", ".")
        )
    else:
        st.metric(
            label=f"Lãi trung bình (mỗi {period_name})",
            value=f"{periodic_interest:,.0f} đ".replace(",", "."),
            help=f"Bạn nhận/ghép lãi tổng cộng {num_periods} lần trong kỳ hạn"
        )

with col2:
    st.metric(
        label="Tổng tiền lãi nhận được",
        value=f"{total_interest:,.0f} đ".replace(",", "."),
        delta=f"+{((total_interest/amount)*100):.1f}% so với gốc"
    )

with col3:
    st.metric(
        label="Tổng thực nhận (Gốc + Lãi)",
        value=f"{total_amount:,.0f} đ".replace(",", ".")
    )

st.divider()

# Tóm tắt thông tin chi tiết
st.subheader("📝 Tóm tắt gói tiết kiệm")
summary_data = {
    "Thông tin": [
        "Số tiền gửi ban đầu",
        "Kỳ hạn gửi",
        "Lãi suất áp dụng",
        "Hình thức nhận lãi",
        "Chế độ tính lãi",
        "Số lần nhận / ghép lãi",
        "Tiền lãi trung bình mỗi kỳ",
        "Tổng tiền lãi thu về",
        "Tổng thực nhận khi đáo hạn"
    ],
    "Giá trị": [
        f"{amount:,.0f} VNĐ".replace(",", "."),
        f"{term_months} tháng",
        f"{interest_rate}% / năm",
        interest_type,
        "🔥 Lãi Kép (Tái nhập gốc dồn lãi)" if is_compound else "Lãi Đơn (Rút tiền lãi định kỳ)",
        f"{num_periods} lần",
        f"{periodic_interest:,.0f} VNĐ".replace(",", "."),
        f"{total_interest:,.0f} VNĐ".replace(",", "."),
        f"{total_amount:,.0f} VNĐ".replace(",", ".")
    ]
}

df_summary = pd.DataFrame(summary_data)
st.table(df_summary)

st.success("🎉 Bạn đang quản lý tài chính rất hiệu quả! Chúc bạn tích lũy thành công!")
