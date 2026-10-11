import os,json
from google import genai
from google.genai import types
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pdf2image import convert_from_path

load_dotenv()
api_key=os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables. Please set it before running the script.")

client = genai.Client(api_key=api_key)

class LineItem(BaseModel):
    description: str = Field(description="Description of the item, product, or service")
    quantity: int = Field(description="Quantity purchased")
    unit_price: float = Field(description="Price per single unit")
    total_price: float = Field(description="Total line cost")

class DocumentSchema(BaseModel):
    document_title: str = Field(description="Title or type of the document (e.g., Invoice, Receipt, Report)")
    document_number: str = Field(description="Unique identifier, invoice number, or reference code")
    issuer_name: str = Field(description="Name of the company or entity issuing the document")
    issue_date: str = Field(description="Date the document was issued")
    line_items: list[LineItem] = Field(description="List of extracted line items or data rows")
    subtotal: float = Field(description="Subtotal amount if present, else 0.0")
    tax_amount: float = Field(description="Tax value applied if present, else 0.0")
    total_amount_due: float = Field(description="Grand total amount due or the final sum")

def parse_pdf_document(pdf_path: str) -> dict:
    """Converts a PDF file to images and extracts structured JSON using Gemini Flash."""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Could not find PDF file at: {pdf_path}")
    
    print(f"[*] Converting PDF pages to high-res images: {pdf_path}")
    images = convert_from_path(pdf_path, dpi=300, poppler_path=r'C:\poppler\Library\bin')
    image = images[0]

    print("[*] Sending image to Gemini 2.5 Flash for structured extraction...")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            image,
            "Extract all table values, line items, totals, and metadata from this document accurately according to the required schema."
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=DocumentSchema,
            temperature=0.1  # Low temperature ensures factual consistency
        ))
    return json.loads(response.text)

if __name__ == "__main__":
    sample_pdf_path = "sample_invoice.pdf"  # Replace with your PDF file path
    if not os.path.exists(sample_pdf_path):
        print(f"Sample PDF file not found at: {sample_pdf_path}. Please provide a valid PDF file.")
    else:
        result = parse_pdf_document(sample_pdf_path)
        print("[*] Extracted structured data:")
        print(json.dumps(result, indent=2))