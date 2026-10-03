import streamlit as st
import pandas as pd
st.image("IMG_20260927_092457.jpg")
# Thiết lập cấu hình trang
st.set_page_config(
    page_title="Tính Lãi Gửi Tiết Kiệm",
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

# Header
st.markdown('<h1 class="main-header">💰 Tính Lãi Gửi Tiết Kiệm</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Tài chính thông minh - Tích lũy tương lai ✨</p>', unsafe_allow_html=True)

st.divider()

# Cột nhập liệu
col_input1, col_input2 = st.columns(2)

with col_input1:
    amount = st.number_input(
        "💵 Số tiền gửi (VNĐ):",
        min_value=1_000_000,
        value=100_000_000,
        step=5_000_000,
        format="%d"
    )
    
    term_months = st.number_input(
        "⏳ Kỳ hạn gửi (tháng):",
        min_value=1,
        max_value=60,
        value=12,
        step=1
    )

with col_input2:
    interest_rate = st.number_input(
        "📈 Lãi suất (%/năm):",
        min_value=0.1,
        max_value=30.0,
        value=6.0,
        step=0.1,
        format="%.2f"
    )
    
    interest_type = st.selectbox(
        "🔄 Hình thức nhận lãi:",
        options=["Cuối kỳ", "Hàng tháng", "Hàng quý"]
    )

# Hàm tính toán
def calculate_interest(p, r_annual, months, itype):
    r = r_annual / 100
    
    if itype == "Cuối kỳ":
        # Lãi cuối kỳ = Số tiền gửi * Lãi suất/12 * Số tháng gửi
        total_interest = p * (r / 12) * months
        periodic_interest = total_interest  # Nhận 1 lần duy nhất lúc đáo hạn
        num_periods = 1
        period_name = "Cuối kỳ"
        
    elif itype == "Hàng tháng":
        # Lãi hàng tháng = Số tiền gửi * (Lãi suất/12)
        periodic_interest = p * (r / 12)
        total_interest = periodic_interest * months
        num_periods = months
        period_name = "tháng"
        
    elif itype == "Hàng quý":
        # Lãi hàng quý = Số tiền gửi * (Lãi suất/4)
        periodic_interest = p * (r / 4)
        num_quarters = months / 3
        total_interest = periodic_interest * num_quarters
        num_periods = int(num_quarters)
        period_name = "quý"
        
    total_amount = p + total_interest
    return periodic_interest, total_interest, total_amount, num_periods, period_name

# Xử lý tính toán
periodic_interest, total_interest, total_amount, num_periods, period_name = calculate_interest(
    amount, interest_rate, term_months, interest_type
)

st.markdown("### 📊 Kết Quả Tính Toán")

# Hiển thị kết quả dạng thẻ Metric
col1, col2, col3 = st.columns(3)

with col1:
    if interest_type == "Cuối kỳ":
        st.metric(
            label="Tiền lãi nhận cuối kỳ",
            value=f"{total_interest:,.0f} đ".replace(",", ".")
        )
    else:
        st.metric(
            label=f"Tiền lãi định kỳ (mỗi {period_name})",
            value=f"{periodic_interest:,.0f} đ".replace(",", "."),
            help=f"Bạn nhận tổng cộng {num_periods} lần trong kỳ hạn"
        )

with col2:
    st.metric(
        label="Tổng tiền lãi nhận được",
        value=f"{total_interest:,.0f} đ".replace(",", ".")
    )

with col3:
    st.metric(
        label="Tổng gốc + lãi nhận được",
        value=f"{total_amount:,.0f} đ".replace(",", ".")
    )

st.divider()

# Tóm tắt thông tin chi tiết
st.subheader("📝 Tóm tắt gói tiết kiệm")
summary_data = {
    "Thông tin": [
        "Số tiền gửi gốc",
        "Kỳ hạn gửi",
        "Lãi suất áp dụng",
        "Hình thức nhận lãi",
        "Số lần nhận lãi",
        "Tiền lãi mỗi kỳ",
        "Tổng tiền lãi thu về",
        "Tổng thực nhận khi đáo hạn"
    ],
    "Giá trị": [
        f"{amount:,.0f} VNĐ".replace(",", "."),
        f"{term_months} tháng",
        f"{interest_rate}% / năm",
        interest_type,
        f"{num_periods} lần" if interest_type != "Cuối kỳ" else "1 lần khi đáo hạn",
        f"{periodic_interest:,.0f} VNĐ".replace(",", ".") if interest_type != "Cuối kỳ" else "Nhận cuối kỳ",
        f"{total_interest:,.0f} VNĐ".replace(",", "."),
        f"{total_amount:,.0f} VNĐ".replace(",", ".")
    ]
}

df_summary = pd.DataFrame(summary_data)
st.table(df_summary)

st.success("🎉 Chúc bạn quản lý tài chính hiệu quả và tích lũy được nhiều tài sản!")
      
