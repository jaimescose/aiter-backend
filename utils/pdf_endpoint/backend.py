from typing import List, Optional
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from sqlmodel import SQLModel, Field, Session, create_engine, select, Relationship
from PyPDF2 import PdfReader
import io
import re

# Define your SQLModel models
class Lab(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: str = Field(index=True)
    user: str
    results: List["Result"] = Relationship(back_populates="lab")

class Result(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    lab_id: int = Field(foreign_key="lab.id")
    parameter: str 
    value: float
    lab: Lab = Relationship(back_populates="results")



# Setup Database
engine = create_engine("sqlite:///database.db")
SQLModel.metadata.create_all(engine)

app = FastAPI()

# Dependency for database session
def get_session():
    with Session(engine) as session:
        yield session


@app.post("/upload/")
async def create_upload_file(file: UploadFile = File(...), session: Session = Depends(get_session)):
    if file.content_type != 'application/pdf':
        raise HTTPException(status_code=415, detail="Unsupported file provided.")
    
    #TO-DO modify dates and username
    lab_entry = Lab(date="2024-05-01", user="username")  # Adjust these values based on your context or inputs
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

    return {"filename": file.filename, "labId": lab_entry.id}


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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
