import pickle
import shutil
import pandas as pd
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

app = FastAPI()

model = pickle.load(open('text_classifier.pkl', 'rb'))
tfidf_vectorizer = pickle.load(open('text_vectorizer.pkl', 'rb'))
label_encoder = pickle.load(open('text_encoder.pkl', 'rb'))

@app.post('/upload')
async def uploadFile(file: UploadFile = File(...)):
    with open( 'test.csv', 'wb' ) as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {'file_name': file.filename}

@app.get('/')
def processor():

    input_df = pd.read_csv('test.csv')

    features = tfidf_vectorizer.transform(input_df['body'])

    predictions = model.predict(features)

    input_df['category'] = label_encoder.inverse_transform(predictions)

    outPut_df = input_df[['id', 'category']]
    outPut_df.to_csv('result.csv', index=False)

    try:
        return FileResponse('result.csv')
    except:
        raise HTTPException(status_code=404, detail="CSV file not uploaded.")