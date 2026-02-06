from fastapi import FastAPI , UploadFile , File 
from fastapi.responses import HTMLResponse
from PIL import Image
import io
from src.pipeline.prediction_pipeline import PredictionPipeline
pipeline = PredictionPipeline()

app = FastAPI(title = 'Helmet Detection')

@app.post
async def predict(file : UploadFile = File(...) ):
          image_bytes = await file.read()
          image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
          results = pipeline.predict(image)
          
          return {
              'detections' : results , "count" : len(results) 
          }
          
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <body style="text-align:center;">
        <h2>Helmet Detection</h2>
        <form action="/predict" method="post" enctype="multipart/form-data">
            <input type="file" name="file"/>
            <br><br>
            <button type="submit">Detect</button>
        </form>
    </body>
    </html>
    """
          


