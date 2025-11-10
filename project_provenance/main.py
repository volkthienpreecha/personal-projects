from fastapi import FastAPI,File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from app_provenance.gradient_map_hash import image_hash_computation, hamming_distance

app = FastAPI()
 

@app.post("/compare") 

async def compare_images(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    img1_bytes = await file1.read()
    img2_bytes = await file2.read()

    hash1 = image_hash_computation(img1_bytes)
    hash2 = image_hash_computation(img2_bytes)
    dist = hamming_distance(hash1, hash2)

    verdict = "Identical image" if dist == 0 else "Image has been changed"

    return JSONResponse({
        "hash1": hash1,
        "hash2": hash2,
        "hamming_distance": dist,
        "verdict": verdict 
    })

app.mount("/", StaticFiles(directory='static', html=True), name = 'static')
