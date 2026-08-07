import streamlit as st
import yfinance as yf
import pandas as pd

# Page setup
st.set_page_config(page_title="NSE Stock Analyzer", layout="wide")

st.title("📊 NSE Bullish / Bearish Stock Analyzer")
st.write("Daily stock trend analysis based on Price & Volume.")

# Initialize Stock List in Session State
if 'stock_list' not in st.session_state:
    st.session_state.stock_list = [
        'RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS', 'ICICIBANK.NS',
        'TATAMOTORS.NS', 'SBIN.NS', 'BHARTIARTL.NS', 'AXISBANK.NS', 'ITC.NS'
    ]

# Sidebar
st.sidebar.header("⚙️ Manage Watchlist")

# Add New Stock
new_stock_input = st.sidebar.text_input("➕ Add New Stock (e.g. TATASTEEL):")
if st.sidebar.button("Add Stock"):
    if new_stock_input:
        symbol = new_stock_input.upper().strip()
        if not symbol.endswith('.NS'):
            symbol += '.NS'
        if symbol not in st.session_state.stock_list:
            st.session_state.stock_list.append(symbol)
            st.sidebar.success(f"{symbol.replace('.NS', '')} Added!")
        else:
            st.sidebar.warning("Stock already in list!")

# Multiselect for Watchlist
selected_stocks = st.sidebar.multiselect(
    "🗑️ Remove stocks using (x):",
    options=st.session_state.stock_list,
    default=st.session_state.stock_list
)

# Refresh Button
if st.button("🔄 Refresh Data"):
    st.cache_data.clear()

# Fetch Stock Data
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

# Display Analysis
if selected_stocks:
    with st.spinner("Fetching NSE Data..."):
        df = fetch_stock_data(selected_stocks)
        
    if not df.empty:
        filter_option = st.radio("Filter:", ["All", "🟢 Bullish Only", "🔴 Bearish Only"], horizontal=True)
        
        if filter_option == "🟢 Bullish Only":
            df_filtered = df[df['Category'] == 'Bullish']
        elif filter_option == "🔴 Bearish Only":
            df_filtered = df[df['Category'] == 'Bearish']
        else:
            df_filtered = df

        st.dataframe(df_filtered.drop(columns=['Category']), use_container_width=True)
    else:
        st.warning("No data found.")
else:
    st.info("Watchlist is empty. Add stocks from sidebar.")    options=st.session_state.stock_list,
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
