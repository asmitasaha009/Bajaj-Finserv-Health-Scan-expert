from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from main import extract_lab_tests

app = FastAPI()

@app.post("/get-lab-tests")
async def get_lab_tests(file: UploadFile = File(...)):
    try:
        # Read the uploaded image file as bytes
        img_bytes = await file.read()

        # Extract lab test results using your function from main.py
        parsed_results = extract_lab_tests(img_bytes)

        # Return results in expected format
        return JSONResponse({
            "is_success": True,
            "data": parsed_results
        })

    except Exception as e:
        # Return error message on failure
        return JSONResponse({
            "is_success": False,
            "error": str(e)
        })
