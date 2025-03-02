from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
from paddleocr import PaddleOCR

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

ocr = PaddleOCR(lang="en")


@app.post("/ocr")
async def extract_text(file: UploadFile = File(...)):
    try:
       
        contents = await file.read()
        np_arr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

     
        if img is None:
            raise HTTPException(status_code=400, detail="Imagem inválida")

   
        result = ocr.ocr(img, cls=True)

       
        extracted_text = []
        for line in result:
            for word in line:
                bbox, (text, conf) = word
                extracted_text.append({"text": text, "confidence": conf, "bbox": bbox})

        if not extracted_text:
            raise HTTPException(status_code=404, detail="Nenhum texto detectado")

        return {"text_detected": extracted_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
