try:
import streamlit as st
import plotly.graph_objects as go
import yfinance as yf
from google import genai

# Page Config
st.set_page_config(page_title="RVTRADES AI System", page_icon="📈", layout="wide")

# App Header
st.title("⚡ RVTRADES Pro - AI Trading Terminal")
st.caption("XAUUSD SMC Analysis | Personal AI Agent | Backtester & Journalist")

# Sidebar - Settings
st.sidebar.header("⚙️ Configuration")
api_key = st.sidebar.text_input("Google AI Studio API Key", type="password")

# Navigation
menu = st.sidebar.radio("Navigation", [
    "🤖 AI Agent & Strategy Maker", 
    "📊 Live XAUUSD Chart", 
    "🧪 Strategy Tester",
    "📓 Auto Journalist"
])

# --- TAB 1: AI AGENT & STRATEGY MAKER ---
if menu == "🤖 AI Agent & Strategy Maker":
    st.subheader("🤖 Personal Trading AI Agent")
    st.info("Aapka AI Mentor: Strategy Generation, SMC Setup Analysis, aur Pine Script v5 Code Helper.")
    
    user_query = st.text_area("Poochiye (e.g., 'XAUUSD 1-min SMC Strategy banao with FVG & Order Block'):")
    
    if st.button("Generate Strategy / Analyze"):
        if not api_key:
            st.error("Kripya Sidebar mein apni Google AI Studio API Key daalein!")
        else:
            try:
                client = genai.Client(api_key=api_key)
                system_prompt = "You are RVTRADES AI Agent, an expert Forex & XAUUSD trader specializing in Smart Money Concepts (SMC), Market Structure Shift (MSS), Order Blocks, FVG, and Pine Script v5."
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=f"{system_prompt}\n\nUser Request: {user_query}"
                )
                
                st.markdown("### 💡 AI Response:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Error: {e}")

# --- TAB 2: LIVE CHART & ANALYSIS ---
elif menu == "📊 Live XAUUSD Chart":
    st.subheader("📊 XAUUSD Live Market Data")
    timeframe = st.selectbox("Select Timeframe", ["1m", "5m", "15m", "1h", "1d"], index=1)
    
    if st.button("Fetch Gold Chart"):
        data = yf.download(tickers="GC=F", period="5d", interval=timeframe)
        if not data.empty:
            fig = go.Figure(data=[go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name="XAUUSD"
            )])
            fig.update_layout(title="Gold (XAUUSD) Realtime Candlestick", template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Market data load nahi ho paya. Retry karein.")

# --- TAB 3: STRATEGY TESTER ---
elif menu == "🧪 Strategy Tester":
  
    st.subheader("🧪 Quick Strategy Backtester")
    st.write("Apni Trading Strategy ke rules test karein.")
    
    initial_capital = st.number_input("Starting Capital ($)", value=1000)
    win_rate = st.slider("Target Win Rate (%)", 10, 100, 60)
    risk_reward = st.slider("Risk-Reward Ratio (1:X)", 1.0, 5.0, 2.0)
    
    if st.button("Run Simulation"):
        expected_return = (win_rate/100 * risk_reward) - ((100-win_rate)/100 * 1)
        st.metric("Expected Expectancy Per Trade", f"{expected_return:.2f} R")
        if expected_return > 0:
            st.success("Strategy is Profitable over long period!")
        else:
            st.warning("Strategy has negative expectancy. Rules tweak karein.")

# --- TAB 4: AUTO JOURNALIST ---
elif menu == "📓 Auto Journalist":
    st.subheader("📓 Trade Journal & AI Review")
  
    col1, col2 = st.columns(2)
    with col1:
        pair = st.text_input("Pair", value="XAUUSD")
        trade_type = st.selectbox("Type", ["BUY", "SELL"])
        lot_size = st.number_input("Lot Size", value=0.01)
    with col2:
        entry_price = st.number_input("Entry Price", value=2600.0)
        exit_price = st.number_input("Exit Price", value=2610.0)
        notes = st.text_area("Setup Reasons (e.g., FVG Tap + 1m MSS)")

    if st.button("Log Trade & AI Analysis"):
        pnl = (exit_price - entry_price) * 100 if trade_type == "BUY" else (entry_price - exit_price) * 100
        st.success(f"Trade Logged! Calculated PnL: ${pnl:.2f}")
        
        if api_key:
            client = genai.Client(api_key=api_key)
            prompt = f"Analyze this trade: Pair={pair}, Type={trade_type}, PnL=${pnl}, Notes={notes}. Give 3 constructive feedback points."
            review = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
            st.markdown("#### 🧠 AI Coach Review:")
            st.write(review.text)
          except Exception as e: st.error(e)
