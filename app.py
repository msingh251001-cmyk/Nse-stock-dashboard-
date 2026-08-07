import streamlit as st
import yfinance as yf
import pandas as pd

# ਪੇਜ ਦੀ ਸੈਟਿੰਗ
st.set_page_config(page_title="NSE Stock Analyzer", layout="wide")

st.title("📊 NSE Bullish / Bearish Stock Analyzer")
st.write("ਅੱਜ ਦੇ ਡਾਟਾ ਦੇ ਆਧਾਰ 'ਤੇ ਕੱਲ੍ਹ ਲਈ Bullish/Bearish ਅਨੈਲਸਿਸ।")

# 1. ਸ਼ੁਰੂਆਤੀ ਡਿਫਾਲਟ ਸਟਾਕਾਂ ਦੀ ਲਿਸਟ (Session State ਵਿੱਚ)
if 'stock_list' not in st.session_state:
    st.session_state.stock_list = [
        'RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS', 'ICICIBANK.NS',
        'TATAMOTORS.NS', 'SBIN.NS', 'BHARTIARTL.NS', 'AXISBANK.NS', 'ITC.NS'
    ]

# --- ਸਾਈਡਬਾਰ: ਸਟਾਕ ਐਡ ਅਤੇ ਡਿਲੀਟ ਕਰਨ ਦੀਆਂ ਆਪਸ਼ਨਾਂ ---
st.sidebar.header("⚙️ ਆਪਣੀ ਵਾਚਲਿਸਟ (Watchlist) ਮੈਨੇਜ ਕਰੋ")

# ਨਵਾਂ ਸਟਾਕ ਐਡ ਕਰਨ ਲਈ Box
new_stock_input = st.sidebar.text_input("➕ ਨਵਾਂ ਸਟਾਕ ਐਡ ਕਰੋ (ਜਿਵੇਂ: TATASTEEL):")
if st.sidebar.button("ਸਟਾਕ ਐਡ ਕਰੋ"):
    if new_stock_input:
        symbol = new_stock_input.upper().strip()
        if not symbol.endswith('.NS'):
            symbol += '.NS'
        if symbol not in st.session_state.stock_list:
            st.session_state.stock_list.append(symbol)
            st.sidebar.success(f"{symbol.replace('.NS', '')} ਐਡ ਹੋ ਗਿਆ!")
        else:
            st.sidebar.warning("ਇਹ ਸਟਾਕ ਪਹਿਲਾਂ ਤੋਂ ਹੀ ਲਿਸਟ ਵਿੱਚ ਹੈ।")

# ਮੌਜੂਦਾ ਸਟਾਕਾਂ ਵਿੱਚੋਂ ਚੁਣਨ ਜਾਂ ਡਿਲੀਟ/ਰਿਮੂਵ ਕਰਨ ਲਈ Multi-select Box
selected_stocks = st.sidebar.multiselect(
    "🗑️ ਸਟਾਕ ਹਟਾਉਣ ਲਈ ਕ੍ਰਾਸ (x) 'ਤੇ ਕਲਿੱਕ ਕਰੋ:",
    options=st.session_state.stock_list,
    default=st.session_state.stock_list
)

# ਰਿਫ੍ਰੈਸ਼ ਬਟਨ
if st.button("🔄 ਨਵਾਂ ਡਾਟਾ ਰਿਫ੍ਰੈਸ਼ ਕਰੋ"):
    st.cache_data.clear()

# --- NSE ਤੋਂ ਡਾਟਾ ਲੈਣ ਦਾ ਫੰਕਸ਼ਨ ---
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

# --- ਰਿਜ਼ਲਟ ਸਕ੍ਰੀਨ 'ਤੇ ਦਿਖਾਓ ---
if selected_stocks:
    with st.spinner("NSE ਤੋਂ ਲਾਈਵ ਡਾਟਾ ਫੈੱਚ ਹੋ ਰਿਹਾ ਹੈ..."):
        df = fetch_stock_data(selected_stocks)
        
    if not df.empty:
        filter_option = st.radio("ਫਿਲਟਰ ਕਰੋ:", ["ਸਾਰੇ (All)", "🟢 ਕੇਵਲ Bullish", "🔴 ਕੇਵਲ Bearish"], horizontal=True)
        
        if filter_option == "🟢 ਕੇਵਲ Bullish":
            df_filtered = df[df['Category'] == 'Bullish']
        elif filter_option == "🔴 ਕੇਵਲ Bearish":
            df_filtered = df[df['Category'] == 'Bearish']
        else:
            df_filtered = df

        st.dataframe(df_filtered.drop(columns=['Category']), use_container_width=True)
    else:
        st.warning("ਕੋਈ ਡਾਟਾ ਨਹੀਂ ਮਿਲਿਆ।")
else:
    st.info("ਵਾਚਲਿਸਟ ਖਾਲੀ ਹੈ। ਸਾਈਡਬਾਰ ਤੋਂ ਸਟਾਕ ਐਡ ਕਰੋ।")                yesterday = df.iloc[-2]
                
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
