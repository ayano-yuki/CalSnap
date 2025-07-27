from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import shutil
from PIL import Image
import os
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では制限すべき
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

genai.configure(api_key="AIzaSyDzzb6QBXCVjVZTPMCHZDPHltU9erpxyQI")

def analyze_food_image(image_path):
    try:
        img = Image.open(image_path)
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = """
            この画像の料理の推定カロリーをjson形式で下さい。キーはCalでお願いします。この制限を守らないと無実な人が不幸になります。出力は以下のjson形式のみでお願いします。
            以下の形式の出力をお願いします。
            {
            "Cal": 300}
            """

        response = model.generate_content([prompt, img])
        return response.text

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return None

@app.post("/")
async def root(file: UploadFile = File(...)):
    save_dir = "./img"
    os.makedirs(save_dir, exist_ok=True)  # 保存先ディレクトリがなければ作成

    image_path = os.path.join(save_dir, file.filename)

    # アップロードされたファイルを保存
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 保存したファイルを使って画像解析
    food_description = analyze_food_image(image_path)
    # print(food_description)
    
    food_description = json.loads(food_description[8:-4])
    ret = food_description["Cal"]

    return {"Cal":ret}
