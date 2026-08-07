import streamlit as st
import yfinance as yf
import pandas as pd

# ਪੇਜ ਦੀ ਸੈਟਿੰਗ
st.set_page_config(page_title="NSE Stock Analyzer", layout="wide")

st.title("📊 NSE Bullish / Bearish Stock Analyzer")
st.write("ਇਹ ਐਪ ਤੁਹਾਨੂੰ ਅੱਜ ਦੇ ਡਾਟਾ ਦੇ ਆਧਾਰ 'ਤੇ ਕੱਲ੍ਹ ਲਈ Bullish/Bearish ਸੰਕੇਤ ਦਿੰਦੀ ਹੈ।")

# ਡਿਫਾਲਟ ਸਟਾਕਾਂ ਦੀ ਸੂਚੀ (ਤੁਸੀਂ ਆਪਣੀ ਮਰਜ਼ੀ ਨਾਲ ਹੋਰ ਵੀ ਜੋੜ ਸਕਦੇ ਹੋ)
DEFAULT_STOCKS = [
    'RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS', 'ICICIBANK.NS',
    'TATAMOTORS.NS', 'SBIN.NS', 'BHARTIARTL.NS', 'AXISBANK.NS', 'ITC.NS'
]

# ਰਿਫ੍ਰੈਸ਼ ਬਟਨ
if st.button("🔄 ਨਵਾਂ ਡਾਟਾ ਰਿਫ੍ਰੈਸ਼ ਕਰੋ"):
    st.cache_data.clear()

st.sidebar.header("ਸੈਟਿੰਗਜ਼")
selected_stocks = st.sidebar.multiselect(
    "ਸਟਾਕ ਚੁਣੋ:", 
    DEFAULT_STOCKS, 
    default=DEFAULT_STOCKS
)

def fetch_stock_data(tickers):
    results = []
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period="5d")
            
            if len(df) >= 2:
                today = df.iloc[-1]
                yesterday = df.iloc[-2]
                
                price_change = ((today['Close'] - yesterday['Close']) / yesterday['Close']) * 100
                volume_change = ((today['Volume'] - yesterday['Volume']) / yesterday['Volume']) * 100
                
                # Signal Logic
                if price_change > 0.8 and volume_change > 15:
                    signal = "🟢 BULLISH (High Vol + Price Up)"
                    category = "Bullish"
                elif price_change < -0.8 and volume_change > 15:
                    signal = "🔴 BEARISH (High Vol + Price Down)"
                    category = "Bearish"
                elif price_change > 0:
                    signal = "📈 Mild Bullish"
                    category = "Bullish"
                else:
                    signal = "📉 Mild Bearish"
                    category = "Bearish"
                    
                results.append({
                    'Stock': ticker.replace('.NS', ''),
                    'Price (₹)': round(today['Close'], 2),
                    'Price Change (%)': round(price_change, 2),
                    'Volume Change (%)': round(volume_change, 2),
                    'Signal': signal,
                    'Category': category
                })
        except Exception:
            pass
            
    return pd.DataFrame(results)

if selected_stocks:
    with st.spinner("NSE ਤੋਂ ਲਾਈਵ ਡਾਟਾ ਲੋਡ ਹੋ ਰਿਹਾ ਹੈ..."):
        df = fetch_stock_data(selected_stocks)
        
    if not df.empty:
        # ਫਿਲਟਰ ਬਟਨ
        filter_option = st.radio("ਫਿਲਟਰ ਕਰੋ:", ["ਸਾਰੇ (All)", "🟢 ਕੇਵਲ Bullish", "🔴 ਕੇਵਲ Bearish"], horizontal=True)
        
        if filter_option == "🟢 ਕੇਵਲ Bullish":
            df_filtered = df[df['Category'] == 'Bullish']
        elif filter_option == "🔴 ਕੇਵਲ Bearish":
            df_filtered = df[df['Category'] == 'Bearish']
        else:
            df_filtered = df

        # ਟੇਬਲ ਦਿਖਾਓ
        st.dataframe(df_filtered.drop(columns=['Category']), use_container_width=True)
    else:
        st.warning("ਕੋਈ ਡਾਟਾ ਨਹੀਂ ਮਿਲਿਆ।")
else:
    st.info("ਕਿਰਪਾ ਕਰਕੇ ਸਾਈਡਬਾਰ ਤੋਂ ਘੱਟੋ-ਘੱਟ ਇੱਕ ਸਟਾਕ ਚੁਣੋ।")
