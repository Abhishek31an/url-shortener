import string
import secrets
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import models, schemas
from database import engine, get_db

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def generate_short_key(length=5):
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))

@app.post("/shorten", response_model=schemas.URLInfo)
def create_short_url(item: schemas.URLCreate, db: Session = Depends(get_db)):
    key = generate_short_key()
    db_url = models.URLItem(original_url=item.url, short_key=key)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    
    return db_url
@app.get("/{short_key}")
def forward_to_target_url(short_key: str, db: Session = Depends(get_db)):
    db_url = db.query(models.URLItem).filter(models.URLItem.short_key == short_key).first()
    if db_url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    db_url.clicks += 1
    db.commit()
    return RedirectResponse(url=db_url.original_url)
@app.get("/stats/{short_key}", response_model=schemas.URLInfo)
def get_url_stats(short_key: str, db: Session = Depends(get_db)):
    db_url = db.query(models.URLItem).filter(models.URLItem.short_key == short_key).first()
    if db_url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return db_url