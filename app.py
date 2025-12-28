import streamlit as st
import pandas as pd
from datetime import datetime
import traceback

# ページ設定
st.set_page_config(
    page_title="エラー処理マスター",
    page_icon="🛡️",
    layout="wide"
)

# セッション状態の初期化
if 'error_log' not in st.session_state:
    st.session_state.error_log = []

# タイトル
st.title("🛡️ エラー処理マスター")
st.write("エラーが起きても安全に動くプログラムを学びます")

# タブで機能を分ける
tab1, tab2, tab3, tab4 = st.tabs(["📝 基本", "🧮 計算", "📁 ファイル", "📊 ログ"])

# ━━━━━━━━━━━━━━━━━━━━━━━━
# タブ1: 基本的なエラー処理
# ━━━━━━━━━━━━━━━━━━━━━━━━
with tab1:
    st.header("📝 基本的なエラー処理")
    
    st.subheader("例1: 数値入力のエラー処理")
    
    user_input = st.text_input("数字を入力してください", placeholder="例: 100")
    
    if st.button("数字チェック", key="check1"):
        try:
            # 文字列を数字に変換
            number = int(user_input)
            st.success(f"✅ 正しい数字です: {number}")
            st.balloons()
            
        except ValueError:
            # 数字じゃない場合のエラー
            st.error("❌ エラー: 数字を入力してください")
            st.session_state.error_log.append({
                "時刻": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "場所": "基本 - 数値入力",
                "エラー": "ValueError",
                "入力値": user_input,
                "メッセージ": "数字以外が入力されました"
            })
            
        except Exception as e:
            # その他のエラー
            st.error(f"❌ 予期しないエラー: {str(e)}")
            st.session_state.error_log.append({
                "時刻": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "場所": "基本 - 数値入力",
                "エラー": type(e).__name__,
                "入力値": user_input,
                "メッセージ": str(e)
            })
    
    st.divider()
    
    st.subheader("例2: リストのエラー処理")
    
    col1, col2 = st.columns(2)
    
    with col1:
        list_index = st.number_input("リストの番号（0-4）", min_value=0, max_value=10, value=0)
    
    with col2:
        if st.button("リスト取得", key="check2"):
            sample_list = ["りんご", "バナナ", "みかん", "ぶどう", "いちご"]
            
            try:
                item = sample_list[list_index]
                st.success(f"✅ 取得成功: {item}")
                
            except IndexError:
                st.error(f"❌ エラー: 番号{list_index}は範囲外です（0-4を入力してください）")
                st.session_state.error_log.append({
                    "時刻": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "場所": "基本 - リスト取得",
                    "エラー": "IndexError",
                    "入力値": list_index,
                    "メッセージ": "リストの範囲外"
                })

# ━━━━━━━━━━━━━━━━━━━━━━━━
# タブ2: 計算のエラー処理
# ━━━━━━━━━━━━━━━━━━━━━━━━
with tab2:
    st.header("🧮 計算のエラー処理")
    
    st.subheader("ゼロ除算エラーの処理")
    
    col1, col2 = st.columns(2)
    
    with col1:
        num1 = st.number_input("割られる数", value=100.0)
    
    with col2:
        num2 = st.number_input("割る数", value=10.0)
    
    if st.button("割り算実行", key="calc1"):
        try:
            result = num1 / num2
            st.success(f"✅ 結果: {num1} ÷ {num2} = {result}")
            
        except ZeroDivisionError:
            st.error("❌ エラー: 0で割ることはできません")
            st.info("💡 ヒント: 「割る数」を0以外の数字にしてください")
            st.session_state.error_log.append({
                "時刻": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "場所": "計算 - 割り算",
                "エラー": "ZeroDivisionError",
                "入力値": f"{num1} ÷ {num2}",
                "メッセージ": "ゼロ除算"
            })
    
    st.divider()
    
    st.subheader("物販の利益計算（エラー処理付き）")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        sales_price = st.text_input("販売価格", placeholder="1000", key="sales")
    
    with col2:
        cost_price = st.text_input("仕入れ価格", placeholder="700", key="cost")
    
    with col3:
        fee_rate = st.text_input("手数料率(%)", placeholder="10", key="fee")
    
    if st.button("利益計算", key="calc2"):
        try:
            # 入力を数値に変換
            sales = float(sales_price)
            cost = float(cost_price)
            fee = float(fee_rate)
            
            # バリデーション
            if sales <= 0:
                raise ValueError("販売価格は0より大きい必要があります")
            if cost < 0:
                raise ValueError("仕入れ価格は0以上である必要があります")
            if fee < 0 or fee > 100:
                raise ValueError("手数料率は0〜100の範囲で入力してください")
            
            # 計算
            fee_amount = sales * (fee / 100)
            profit = sales - cost - fee_amount
            profit_rate = (profit / sales) * 100
            
            # 結果表示
            st.success("✅ 計算成功！")
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("販売価格", f"¥{sales:,.0f}")
            col2.metric("仕入れ価格", f"¥{cost:,.0f}")
            col3.metric("手数料", f"¥{fee_amount:,.0f}")
            col4.metric("利益", f"¥{profit:,.0f}", f"{profit_rate:.1f}%")
            
        except ValueError as e:
            st.error(f"❌ 入力エラー: {str(e)}")
            st.session_state.error_log.append({
                "時刻": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "場所": "計算 - 利益計算",
                "エラー": "ValueError",
                "入力値": f"販売:{sales_price}, 仕入:{cost_price}, 手数料:{fee_rate}",
                "メッセージ": str(e)
            })
            
        except Exception as e:
            st.error(f"❌ 予期しないエラー: {str(e)}")
            st.session_state.error_log.append({
                "時刻": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "場所": "計算 - 利益計算",
                "エラー": type(e).__name__,
                "入力値": f"販売:{sales_price}, 仕入:{cost_price}, 手数料:{fee_rate}",
                "メッセージ": str(e)
            })

# ━━━━━━━━━━━━━━━━━━━━━━━━
# タブ3: ファイル処理のエラー処理
# ━━━━━━━━━━━━━━━━━━━━━━━━
with tab3:
    st.header("📁 ファイル処理のエラー処理")
    
    uploaded_file = st.file_uploader("CSVファイルをアップロード", type=['csv'])
    
    if uploaded_file is not None:
        try:
            # CSVを読み込み
            df = pd.read_csv(uploaded_file)
            
            st.success("✅ ファイル読み込み成功！")
            st.write(f"行数: {len(df)}, 列数: {len(df.columns)}")
            
            # データ表示
            st.dataframe(df.head(10))
            
        except pd.errors.EmptyDataError:
            st.error("❌ エラー: ファイルが空です")
            st.session_state.error_log.append({
                "時刻": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "場所": "ファイル - CSV読み込み",
                "エラー": "EmptyDataError",
                "入力値": uploaded_file.name,
                "メッセージ": "空のファイル"
            })
            
        except pd.errors.ParserError:
            st.error("❌ エラー: CSVファイルの形式が正しくありません")
            st.info("💡 ヒント: Excelファイルの場合は「CSV UTF-8」形式で保存してください")
            st.session_state.error_log.append({
                "時刻": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "場所": "ファイル - CSV読み込み",
                "エラー": "ParserError",
                "入力値": uploaded_file.name,
                "メッセージ": "CSVパースエラー"
            })
            
        except Exception as e:
            st.error(f"❌ 予期しないエラー: {str(e)}")
            st.session_state.error_log.append({
                "時刻": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "場所": "ファイル - CSV読み込み",
                "エラー": type(e).__name__,
                "入力値": uploaded_file.name if uploaded_file else "None",
                "メッセージ": str(e)
            })
    
    st.divider()
    
    st.subheader("サンプルCSVをダウンロード")
    
    sample_data = {
        "商品名": ["商品A", "商品B", "商品C"],
        "販売価格": [1000, 2000, 1500],
        "仕入れ価格": [700, 1500, 1000]
    }
    
    sample_df = pd.DataFrame(sample_data)
    csv = sample_df.to_csv(index=False).encode('utf-8-sig')
    
    st.download_button(
        label="📥 サンプルCSVダウンロード",
        data=csv,
        file_name="sample.csv",
        mime="text/csv"
    )

# ━━━━━━━━━━━━━━━━━━━━━━━━
# タブ4: エラーログ
# ━━━━━━━━━━━━━━━━━━━━━━━━
with tab4:
    st.header("📊 エラーログ")
    
    if len(st.session_state.error_log) == 0:
        st.info("まだエラーは発生していません")
    else:
        st.write(f"合計 {len(st.session_state.error_log)} 件のエラー")
        
        # エラーログをDataFrameで表示
        df_log = pd.DataFrame(st.session_state.error_log)
        st.dataframe(df_log, use_container_width=True)
        
        # CSVダウンロード
        csv_log = df_log.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 エラーログをCSVでダウンロード",
            data=csv_log,
            file_name=f"error_log_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
        
        # ログクリア
        if st.button("🗑️ ログをクリア"):
            st.session_state.error_log = []
            st.rerun()

# サイドバー：説明
st.sidebar.header("💡 エラー処理とは？")

st.sidebar.info("""
**エラー処理の重要性**

プログラムは予期しない入力でエラーになることがあります。

**主なエラーの種類:**
- **ValueError**: 値が不正
- **ZeroDivisionError**: 0で割った
- **IndexError**: リストの範囲外
- **FileNotFoundError**: ファイルがない
- **TypeError**: 型が違う

**try-except構文:**
```python
try:
    # 実行したいコード
    result = 10 / 0
except ZeroDivisionError:
    # エラー時の処理
    print("0で割れません")
```

これにより、エラーが起きてもプログラムが止まらず、ユーザーに優しいメッセージを表示できます。
""")

st.sidebar.divider()

st.sidebar.success("""
**次のステップ（レベル10）**

LINE Notify連携で、エラーが起きたら自動でLINEに通知する仕組みを作ります！
""")
