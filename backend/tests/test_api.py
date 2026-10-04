def headers(token): return {"Authorization": f"Bearer {token}"}

def test_auth_and_protected_access(client, auth):
    assert client.get("/api/books").status_code == 401
    assert client.get("/api/books", headers=headers(auth)).json() == []

def test_upload_rejects_non_pdf(client, auth):
    response = client.post("/api/books", headers=headers(auth), files={"file": ("notes.txt", b"hello", "text/plain")})
    assert response.status_code == 415

def test_upload_creates_owned_book(client, auth):
    response = client.post("/api/books", headers=headers(auth), files={"file": ("sample.pdf", b"%PDF-1.4\n", "application/pdf")})
    assert response.status_code == 201
    book = response.json(); assert book["status"] == "UPLOADED"; assert book["title"] == "sample"

def test_pipeline_helpers():
    from app.services.pipeline import chunk_text, normalize_text
    assert normalize_text("Hello\nworld") == "Hello world"
    chunks = chunk_text("Sentence one. " * 300, limit=100)
    assert len(chunks) > 1 and "Sentence" in "".join(chunks)
