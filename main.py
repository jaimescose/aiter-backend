from datetime import datetime
import io
import re
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from PyPDF2 import PdfReader

# from utils.ol import query_llm

from . import crud
from .models import Lab, Result, User
from .database import engine

app = FastAPI()


@app.post("/users/", response_model=User)
def create_user(user: User):
    print(user)
    # existing_user = crud.get_user_by_email(user.email)
    user.date_of_birth = datetime.strptime(user.date_of_birth, "%Y-%m-%d")
    # if existing_user:
    #     raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(user)


@app.get("/users/{user_id}", response_model=crud.MedicalProfile)
def read_user_data(user_id: int, window: crud.Frequency = crud.Frequency.month):
    db_user = crud.get_user_data(user_id=user_id, window=window)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# Dependency for database session
def get_session():
    with Session(engine) as session:
        yield session


def extract_text_from_pdf_hemograma(content, keywords, session, lab_id):
    reader = PdfReader(io.BytesIO(content))
    pattern_a = r"^(?P<description>[^\d]+)\s*(?P<numeric>\d+(?:\.\d+)?)"
    special_keyword_set = set(k.lower() for k in keywords)

    for page_num in range(len(reader.pages)):
        page_text = reader.pages[page_num].extract_text()
        if page_text:
            lines = page_text.split('\n')
            for line in lines:
                special_unit = ""
                line = line.lower()
                words = set(word for word in line.split())
                common_words = special_keyword_set & words
                if common_words:
                    match = re.match(pattern_a, line)
                    if match:
                        description = match.group('description').strip().rstrip('.').capitalize()
                        numeric = match.group('numeric') + special_unit
                        save_to_database(session, description, numeric, lab_id)


def save_to_database(session, description, value, lab_id):
    result_entry = Result(lab_id=lab_id, parameter=description, value=value)
    session.add(result_entry)
    session.commit()


@app.post("/users/{user_id}/labs")
async def create_upload_file(user_id: int, file: UploadFile = File(...), session: Session = Depends(get_session)):
    if file.content_type != 'application/pdf':
        raise HTTPException(status_code=415, detail="Unsupported file provided.")
    
    lab_entry = Lab(user_id=user_id)
    session.add(lab_entry)
    session.commit()
    keywords = [
    "ERITROCITOS.",
    "HEMOGLOBINA.",
    "HEMATOCRITO.",
    "VCM.",
    "CHM.",
    "CHCM.",
    "ADE.",
    "PLAQUETAS.",
    "LEUCOCITOS.",
    "VPM.",
    "NEUTROFILOS.",
    "EOSINOFILOS.",
    "BASOFILOS.",
    "LINFOCITOS.",
    "MONOCITOS.",
    "NEUTROFILOS.",
    "EOSINOFILOS.",
    "BASOFILOS.",
    "LINFOCITOS.",
    "MONOCITOS.",
    "NITROGENO",
    "SICLEMIA",
    "GLOMERULAR",
    "COLESTEROL",
    "TRIGLICERIDOS",
    "ALANINO",
    "ASPARTATO",
    "AMILASA",
    "LIPASA",
    "HORMONAS",
    "TSH",
    "INSULINA",
    "PROTEINAS",
    "PROTEINA",
    "CREATININA",
    "ERITROSEDIMENTACION",
    "TESTOSTERONA"
    ]

    content = await file.read()
    extract_text_from_pdf_hemograma(content, keywords, session, lab_entry.id)
    
    return {'message': 'created', 'lab_id': lab_entry.id}

@app.get("/labs/{lab_id}", response_model=crud.LabDetail)
def read_lab(lab_id: int):
    return crud.get_lab(lab_id=lab_id)


"""
@app.get("/process")
def process():
    query = "How can I do to improve my VO2Max?"
    result = query_llm(query)
    return {"result": result}
"""



"""
@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)
"""
