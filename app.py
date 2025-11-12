from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# ====== アプリ基本設定 ======
st.set_page_config(
    page_title="LangChain × Streamlit デモ",
    page_icon="📚",
    layout="centered"
)

st.title("📚 LangChain × Streamlit デモ")
st.markdown("""
このアプリでは、入力した質問に対して、選択した専門家の視点で回答を生成します。

1. 質問を入力  
2. 専門家を選択  
3. 「送信」をクリック
""")

# ====== 専門家選択 ======
expert_choice = st.radio(
    "専門家を選択してください",
    ("健康アドバイザー", "料理コンサルタント")
)

# ====== ユーザー入力 ======
user_input = st.text_input("質問を入力してください:")

# ====== LLM呼び出し関数 ======
def get_llm_response(user_question: str, expert: str) -> str:
    """入力と専門家選択をもとにLLMから回答を取得"""
    if expert == "健康アドバイザー":
        system_prompt = "あなたは健康に関するアドバイザーです。安全で実用的なアドバイスを提供してください。"
    else:
        system_prompt = "あなたは料理に関する専門家です。レシピや調理法をわかりやすく説明してください。"

    # ChatOpenAIインスタンスを作成
    client = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)

    # invoke() で実行
    response = client.invoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_question}
    ])

    return response.content  # ←ここでtextを返す

# ====== 送信ボタン ======
if st.button("送信"):
    if not user_input.strip():
        st.warning("質問を入力してください。")
    else:
        with st.spinner("回答を生成中…"):
            answer = get_llm_response(user_input, expert_choice)
        st.success("💬 回答:")
        st.write(answer)