import pickle
import shutil
import pandas as pd
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse

app = FastAPI() # uvicorn main:app --reload

model = pickle.load(open('./models/text_classifier.pkl', 'rb'))
tfidf_vectorizer = pickle.load(open('./models/text_vectorizer.pkl', 'rb'))
label_encoder = pickle.load(open('./models/text_encoder.pkl', 'rb'))

@app.post('/upload')
async def uploadFile(file: UploadFile = File(...)):
    # 把大文件分成一個一個小包，then保存
    with open('test.csv', 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {'file_name': file.filename}

@app.get('/')
def processor():
    input_df = pd.read_csv('./data/test.csv')
    # 文本特徵提取，衡量每個單詞對文章的重要性
    features = tfidf_vectorizer.transform(input_df['body'])
    preds =  model.predict(features)
    # 預測的值是訓練的結果(數值)，需要再轉換成對應的分類，使用label_encoder
    input_df['category'] = label_encoder.inverse_transform(preds)

    output_df = input_df[['id', 'category']]
    output_df.to_csv('result.csv', index=False)

    return FileResponse('result.csv')