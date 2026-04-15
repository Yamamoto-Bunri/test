import docx
import google.generativeai as genai
import pandas as pd
import json
import time

# --- 設定 ---
genai.configure(api_key="あなたのGEMINI_API_KEY") 
model = genai.GenerativeModel('gemini-1.5-flash')

def get_word_info_from_ai(word, context):
    prompt = f"""
    英文テキスト: "{context}"
    この中に出てくる単語 "{word}" について、以下の情報を日本語のJSON形式で正確に回答してください。
    
    1. pos_in_context: 本文中での品詞
    2. base_form: 単語本体（名詞は単数形、動詞は原形）
    3. meaning_in_context: 本文中での日本語の意味
    4. other_meanings: その他の主な意味（カンマ区切り）
    5. other_pos: 同じ単語で他の品詞とその意味
    6. derivatives: 派生語とその品詞と意味
    
    出力例:
    {{
        "pos_in_context": "動詞",
        "base_form": "run",
        "meaning_in_context": "経営する",
        "other_meanings": "走る、流れる",
        "other_pos": "名詞：走ること、走行",
        "derivatives": "runner (名詞：走る人)"
    }}
    """
    try:
        response = model.generate_content(prompt)
        return json.loads(response.text.replace('```json', '').replace('```', ''))
    except:
        return None

def create_word_set(file_path, unit_name):
    doc = docx.Document(file_path)
    full_text = "\n".join([p.text for p in doc.paragraphs])
    
    # 簡易的な単語抽出（実際にはspacy等を使うとより正確です）
    # ここではシンプルに空白で分割し、重複を除去
    words = list(dict.fromkeys([w.strip(",.?!()").lower() for w in full_text.split() if len(w) > 2]))
    
    data_list = []
    for word in words:
        print(f"解析中: {word}...")
        info = get_word_info_from_ai(word, full_text)
        if info:
            data_list.append(info)
        time.sleep(1) # APIの制限回避用
        
    df = pd.DataFrame(data_list)
    df.to_csv(f"{unit_name}.csv", index=False, encoding='utf-8-sig')
    print(f"完了! {unit_name}.csv を作成しました。")

# 実行例
# create_word_set("lesson1.docx", "Unit1")
