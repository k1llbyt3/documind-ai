import os,json,random
import streamlit as st
from PIL import Image
from pdf2image import convert_from_path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from src.parser import parse_pdf_document

st.set_page_config(
    page_title="DocuMind-AI | Multimodal Financial / Medical Document Parser & Extractor",
    page_icon="📄",
    layout="wide",
)

st.markdown(
    """
    <style>
    .main {
        background-color: #0e1117;
    }
    .stApp {
        color: #e6edf3;
    }
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #238636 0%, #2ea043 100%);
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        width: 100%;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #2ea043 100%, #3fb950 100%);
    }
    </style>
""",
    unsafe_allow_html=True,
)

def generate_random_document(output_dir, target_pages=2):
    os.makedirs(output_dir, exist_ok=True)
    archetype = random.choice(["ENTERPRISE_INVOICE", "CLINICAL_REPORT", "CLOUD_AUDIT"])
    
    issuers = {
        "ENTERPRISE_INVOICE": ["Vanguard Global Solutions", "Apex Infrastructure Corp", "Meridian Enterprise Partners"],
        "CLINICAL_REPORT": ["Metro General Pathology Lab", "BioHealth Diagnostics Group", "Advanced Clinical Research Institute"],
        "CLOUD_AUDIT": ["CloudScale Security Operations", "CyberGuard Systems Inc", "DevSecOps Global Auditing"]
    }
    
    clients = ["Acme Corporation", "Starlight Media LLC", "Quantum Global Logistics", "Alpha Cybernetics"]
    issuer = random.choice(issuers[archetype])
    client = random.choice(clients)
    doc_id = f"{archetype[:3]}-{random.randint(10000, 99999)}"
    
    safe_issuer = issuer.replace(" ", "_")
    filename = os.path.join(output_dir, f"{archetype}_{safe_issuer}_{doc_id}.pdf")

    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontSize=20, leading=24, textColor=colors.HexColor("#1a1a1a"))
    subtitle_style = ParagraphStyle('DocSub', parent=styles['Normal'], fontSize=10, leading=14, textColor=colors.HexColor("#555555"))
    h2_style = ParagraphStyle('SectionHeader', parent=styles['Heading2'], fontSize=14, leading=18, textColor=colors.HexColor("#0f4c81"), spaceBefore=12, spaceAfter=6)
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=10, leading=14, textColor=colors.HexColor("#222222"))
    
    story = []

    if archetype == "ENTERPRISE_INVOICE":
        story.append(Paragraph("COMMERCIAL MASTER SERVICES INVOICE", title_style))
        story.append(Spacer(1, 10))
        story.append(Paragraph(f"<b>Issued By:</b> {issuer} | <b>Ref:</b> {doc_id}", subtitle_style))
        story.append(Paragraph(f"<b>Billed To:</b> {client} | <b>Billing Cycle:</b> Q3 2026", subtitle_style))
        story.append(Spacer(1, 15))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0f4c81")))
        story.append(Spacer(1, 15))
        
        story.append(Paragraph("Executive Summary & Scope of Work", h2_style))
        story.append(Paragraph(
            "This invoice itemizes professional engineering, cloud architecture migration, and security auditing services rendered "
            "during the active operational term.", body_style
        ))
        story.append(Spacer(1, 15))
        story.append(Paragraph("Itemized Service Breakdown", h2_style))
        
        table_data = [["Item Description", "Hours", "Rate / Hr", "Total Amount"]]
        services_pool = [
            ("Kubernetes Multi-Cluster Orchestration Setup", 45, 150.0),
            ("Zero-Trust Network Architecture Design", 30, 200.0),
            ("PostgreSQL Database Sharding & Indexing", 25, 175.0),
            ("Automated Compliance Scripting & Testing", 40, 125.0),
            ("Legacy Monolith Refactoring to Microservices", 60, 160.0),
            ("Load Testing & High-Availability Tuning", 20, 190.0),
            ("Executive Technical Briefing & Documentation", 15, 220.0)
        ]
        
        for desc, hrs, rate in services_pool:
            table_data.append([desc, str(hrs), f"${rate:.2f}", f"${hrs * rate:,.2f}"])
            
        t = Table(table_data, colWidths=[280, 60, 80, 120])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f4c81")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (1,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f9f9f9")])
        ]))
        story.append(t)
        
        for p in range(2, target_pages + 1):
            story.append(PageBreak())
            story.append(Paragraph(f"COMMERCIAL MASTER SERVICES INVOICE (Page {p})", title_style))
            story.append(Spacer(1, 10))
            story.append(Paragraph(f"Reference ID: {doc_id} | Client: {client}", subtitle_style))
            story.append(Spacer(1, 15))
            story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cccccc")))
            story.append(Spacer(1, 15))
            if p == target_pages:
                story.append(Paragraph("Financial Settlement & Terms", h2_style))
                totals_data = [
                    ["Subtotal:", "$36,050.00"],
                    ["State & Federal Tax (8.5%):", "$3,064.25"],
                    ["Total Balance Due:", "$39,114.25"]
                ]
                t_tot = Table(totals_data, colWidths=[350, 190])
                t_tot.setStyle(TableStyle([
                    ('ALIGN', (0,0), (-1,-1), 'RIGHT'),
                    ('FONTNAME', (0,0), (-1,-2), 'Helvetica'),
                    ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
                    ('FONTSIZE', (0,0), (-1,-1), 10),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
                    ('TOPPADDING', (0,0), (-1,-1), 6),
                    ('LINEABOVE', (0,-1), (-1,-1), 1.5, colors.HexColor("#1a1a1a")),
                ]))
                story.append(t_tot)
            else:
                story.append(Paragraph(f"Continuation details for operational schedule block {p}.", body_style))

    elif archetype == "CLINICAL_REPORT":
        story.append(Paragraph("COMPREHENSIVE CLINICAL PATHOLOGY REPORT", title_style))
        story.append(Spacer(1, 10))
        story.append(Paragraph(f"<b>Laboratory:</b> {issuer} | <b>Accession ID:</b> {doc_id}", subtitle_style))
        story.append(Paragraph(f"<b>Patient Name:</b> {client} | <b>Status:</b> Confidant & Verified", subtitle_style))
        story.append(Spacer(1, 15))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2a7561")))
        story.append(Spacer(1, 15))
        
        story.append(Paragraph("Biochemical Assay Panels", h2_style))
        panel_a = [
            ["Test Parameter", "Observed Value", "Reference Range", "Diagnostic Status"],
            ["Comprehensive Metabolic Panel (CMP)", "Normal", "70 - 99 mg/dL", "Normal"],
            ["Serum Lipid Profile (Cholesterol)", "215 mg/dL", "< 200 mg/dL", "Elevated"],
            ["Glycated Hemoglobin (HbA1c)", "5.6%", "< 5.7%", "Normal"],
            ["Complete Blood Count (CBC)", "5.2 k/uL", "4.5 - 11.0 k/uL", "Normal"]
        ]
        t_pa = Table(panel_a, colWidths=[180, 100, 120, 140])
        t_pa.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2a7561")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
        ]))
        story.append(t_pa)
        
        for p in range(2, target_pages + 1):
            story.append(PageBreak())
            story.append(Paragraph(f"COMPREHENSIVE CLINICAL PATHOLOGY REPORT (Page {p})", title_style))
            story.append(Spacer(1, 10))
            story.append(Paragraph(f"Accession ID: {doc_id} | Patient: {client}", subtitle_style))
            story.append(Spacer(1, 15))
            story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cccccc")))
            story.append(Spacer(1, 15))
            if p == target_pages:
                sign_data = [
                    ["Attending Physician:", "Dr. Aris Vance, M.D."],
                    ["Laboratory Director:", "Dr. Elizabeth Cole, PhD"],
                    ["Verification Signature:", "___________________________"]
                ]
                t_sign = Table(sign_data, colWidths=[160, 380])
                t_sign.setStyle(TableStyle([
                    ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
                    ('FONTNAME', (1,0), (1,-1), 'Helvetica'),
                    ('FONTSIZE', (0,0), (-1,-1), 10),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 10),
                ]))
                story.append(t_sign)
            else:
                story.append(Paragraph(f"Additional diagnostic observations and supplementary panel details for section {p}.", body_style))

    else:
        story.append(Paragraph("CLOUD INFRASTRUCTURE & SECURITY AUDIT", title_style))
        story.append(Spacer(1, 10))
        story.append(Paragraph(f"<b>Auditor:</b> {issuer} | <b>Audit ID:</b> {doc_id}", subtitle_style))
        story.append(Paragraph(f"<b>Target Enterprise:</b> {client}", subtitle_style))
        story.append(Spacer(1, 15))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#b33939")))
        story.append(Spacer(1, 15))
        
        comp_data = [
            ["Region", "Instance Class", "Active Cores", "Monthly Cost"],
            ["us-central1", "n2-standard-16", "256 vCPUs", "$4,200.00"],
            ["europe-west1", "c2-standard-8", "128 vCPUs", "$2,850.00"]
        ]
        t_comp = Table(comp_data, colWidths=[120, 140, 120, 160])
        t_comp.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#b33939")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
        ]))
        story.append(t_comp)
        
        for p in range(2, target_pages + 1):
            story.append(PageBreak())
            story.append(Paragraph(f"SECURITY VULNERABILITY ASSESSMENT (Page {p})", title_style))
            story.append(Spacer(1, 10))
            story.append(Paragraph(f"Audit Reference: {doc_id}", subtitle_style))
            story.append(Spacer(1, 15))
            story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cccccc")))
            story.append(Spacer(1, 15))
            if p == target_pages:
                story.append(Paragraph("<b>Lead Security Architect:</b> Marcus Vance, CISSP", body_style))
            else:
                vuln_data = [
                    ["CVE Identifier", "Severity", "Component", "Status"],
                    ["CVE-2026-1042", "Critical", "OpenSSL 3.1.2", "Patched"],
                    ["CVE-2026-8819", "High", "Containerd Runtime", "Pending Action"]
                ]
                t_vuln = Table(vuln_data, colWidths=[130, 100, 160, 150])
                t_vuln.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#333333")),
                    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0,0), (-1,-1), 9),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 8),
                    ('TOPPADDING', (0,0), (-1,-1), 8),
                    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
                ]))
                story.append(t_vuln)

    doc.build(story)
    return filename

# Initialize session state for navigation
if 'app_mode' not in st.session_state:
    st.session_state['app_mode'] = "Home"

def navigate_to(mode):
    st.session_state['app_mode'] = mode

# Sidebar navigation
st.sidebar.title("Navigation")
if st.sidebar.button("Home"):
    navigate_to("Home")
if st.sidebar.button("Document Extractor"):
    navigate_to("Document Extractor")
if st.sidebar.button("Random Document Generator"):
    navigate_to("Random Document Generator")

# Main Routing Based on Session State
if st.session_state['app_mode'] == "Home":
    st.title("DocuMind-AI: Intelligent Document Intelligence Platform")
    st.markdown("Welcome to DocuMind-AI. Choose a utility module below to begin parsing structured documents or generating randomized multi-page schemas.")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Document Extractor")
        st.markdown("Upload commercial invoices, medical pathology reports, or cloud statements to execute multi-modal extraction pipelines.")
        if st.button("Launch Extractor"):
            navigate_to("Document Extractor")
            st.rerun()
            
    with col2:
        st.subheader("Random Document Generator")
        st.markdown("Build customized multi-page test PDFs with dynamic layouts, tables, and structured datasets.")
        if st.button("Launch Generator"):
            navigate_to("Random Document Generator")
            st.rerun()

elif st.session_state['app_mode'] == "Document Extractor":
    if st.button("← Back to Home"):
        navigate_to("Home")
        st.rerun()
        
    st.title(" DocuMind-AI: Multimodal Financial / Medical Document Parser & Extractor")
    st.markdown("Advanced multimodal document parser driven by **Gemini Flash Vision** and strict **Pydantic schemas** for structured financial and operational data extraction.")

    uploaded_file = st.file_uploader("Upload Document (PDF)", type=["pdf"])

    if uploaded_file is not None:
        temp_pdf_path = "temp_uploaded.pdf"
        with open(temp_pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Uploaded Document Preview")
            try:
                images = convert_from_path(
                    temp_pdf_path, dpi=150, poppler_path=r"C:\poppler\Library\bin"
                )
                st.image(images[0], caption="Page 1 Preview", use_column_width=True)
            except Exception as e:
                st.error(
                    f"Could not render PDF preview. Make sure Poppler is installed. Error: {e}"
                )

        with col2:
            st.subheader("Extracted Structured Data (JSON)")
            if st.button("Run Extraction Pipeline", type="primary"):
                with st.spinner("Processing document layout via Gemini Vision..."):
                    try:
                        extracted_data = parse_pdf_document(temp_pdf_path)
                        st.success("Extraction completed successfully!")

                        st.json(extracted_data)

                        json_string = json.dumps(extracted_data, indent=2)
                        st.download_button(
                            label="Download Extracted JSON",
                            data=json_string,
                            file_name="extracted_document.json",
                            mime="application/json",
                        )
                    except Exception as e:
                        st.error(f"An error occurred during extraction: {e}")

        if os.path.exists(temp_pdf_path):
            os.remove(temp_pdf_path)

elif st.session_state['app_mode'] == "Random Document Generator":
    if st.button("← Back to Home"):
        navigate_to("Home")
        st.rerun()
        
    st.title("Multi-Page Test Document Generator")
    st.markdown("Configure and generate complex multi-page mock documents for pipeline validation and testing.")

    doc_count = st.number_input("Number of Documents", min_value=1, max_value=10, value=1, step=1)
    page_count = st.number_input("Pages per Document", min_value=1, max_value=5, value=2, step=1)

    if st.button("Generate Documents", type="primary"):
        output_folder = "inputs"
        generated_files = []
        for _ in range(doc_count):
            path = generate_random_document(output_folder, target_pages=page_count)
            generated_files.append(path)
            
        st.success(f"Successfully generated {doc_count} document(s).")
        st.markdown("---")
        st.subheader("Download Generated Files")
        
        for path in generated_files:
            file_name = os.path.basename(path)
            with open(path, "rb") as pdf_file:
                bytes_data = pdf_file.read()
                st.download_button(
                    label=f"Download {file_name}",
                    data=bytes_data,
                    file_name=file_name,
                    mime="application/pdf"
                )