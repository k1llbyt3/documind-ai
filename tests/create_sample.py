import os,random,argparse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_random_document(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    # Choose from 3 distinct multi-page document archetypes
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

    # Setup document geometry (Letter size, 0.5-inch margins)
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
        # --- PAGE 1: Invoice Header & Summary ---
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
            "during the active operational term. All tasks have been completed in accordance with the Master Service Agreement (MSA) "
            "and verified via automated CI/CD pipeline telemetry logs.", body_style
        ))
        story.append(Spacer(1, 15))
        
        story.append(Paragraph("Itemized Service Breakdown (Page 1 of 2)", h2_style))
        
        # Large table to populate page 1 & push items to page 2
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
        
        # Force Page Break to guarantee multi-page structure
        story.append(PageBreak())
        
        # --- PAGE 2: Financial Totals & Compliance Terms ---
        story.append(Paragraph("INVOICE (Continued) - Financial Settlement", title_style))
        story.append(Spacer(1, 10))
        story.append(Paragraph(f"Reference ID: {doc_id} | Client: {client}", subtitle_style))
        story.append(Spacer(1, 15))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cccccc")))
        story.append(Spacer(1, 15))
        
        story.append(Paragraph("Payment Terms & Remittance Information", h2_style))
        story.append(Paragraph(
            "Net 30 terms apply from the date of issuance. Wire transfers should be routed through the primary corporate banking portal. "
            "Failure to settle balances within 60 days will incur a standard 1.5% monthly compounding service fee.", body_style
        ))
        story.append(Spacer(1, 20))
        
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

    elif archetype == "CLINICAL_REPORT":
        # --- PAGE 1: Patient Details & Initial Panels ---
        story.append(Paragraph("COMPREHENSIVE CLINICAL PATHOLOGY REPORT", title_style))
        story.append(Spacer(1, 10))
        story.append(Paragraph(f"<b>Laboratory:</b> {issuer} | <b>Accession ID:</b> {doc_id}", subtitle_style))
        story.append(Paragraph(f"<b>Patient Name:</b> {client} | <b>Status:</b> Confidant & Verified", subtitle_style))
        story.append(Spacer(1, 15))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2a7561")))
        story.append(Spacer(1, 15))
        
        story.append(Paragraph("Biochemical Assay Panels (Panel A)", h2_style))
        
        panel_a = [
            ["Test Parameter", "Observed Value", "Reference Range", "Diagnostic Status"],
            ["Comprehensive Metabolic Panel (CMP)", "Normal", "70 - 99 mg/dL", "Normal"],
            ["Serum Lipid Profile (Cholesterol)", "215 mg/dL", "< 200 mg/dL", "Elevated"],
            ["Glycated Hemoglobin (HbA1c)", "5.6%", "< 5.7%", "Normal"],
            ["Complete Blood Count (CBC)", "5.2 k/uL", "4.5 - 11.0 k/uL", "Normal"],
            ["Thyroid Stimulating Hormone (TSH)", "2.4 mIU/L", "0.4 - 4.0 mIU/L", "Optimal"]
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
        
        story.append(PageBreak())
        
        # --- PAGE 2: Pathology Notes & Physician Sign-off ---
        story.append(Paragraph("CLINICAL PATHOLOGY REPORT (Page 2)", title_style))
        story.append(Spacer(1, 10))
        story.append(Paragraph(f"Accession ID: {doc_id} | Patient: {client}", subtitle_style))
        story.append(Spacer(1, 15))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cccccc")))
        story.append(Spacer(1, 15))
        
        story.append(Paragraph("Pathologist Evaluation & Recommendations", h2_style))
        story.append(Paragraph(
            "Patient demonstrates stable baseline chemistry across most evaluated parameters. Minor elevation noted in lipid profile "
            "warrants dietary modification and a follow-up screening in 6 months. No acute systemic anomalies detected.", body_style
        ))
        story.append(Spacer(1, 40))
        
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
        # --- PAGE 1: Cloud Architecture Audit ---
        story.append(Paragraph("CLOUD INFRASTRUCTURE & SECURITY AUDIT", title_style))
        story.append(Spacer(1, 10))
        story.append(Paragraph(f"<b>Auditor:</b> {issuer} | <b>Audit ID:</b> {doc_id}", subtitle_style))
        story.append(Paragraph(f"<b>Target Enterprise:</b> {client} | <b>Scope:</b> Global Multi-Region", subtitle_style))
        story.append(Spacer(1, 15))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#b33939")))
        story.append(Spacer(1, 15))
        
        story.append(Paragraph("Executive Infrastructure Overview", h2_style))
        story.append(Paragraph(
            "This comprehensive 3-page audit report evaluates resource allocation efficiency, IAM security postures, and cost-anomaly "
            "mitigation strategies across all active Kubernetes clusters and serverless deployments.", body_style
        ))
        story.append(Spacer(1, 15))
        
        story.append(Paragraph("Multi-Region Compute Allocation", h2_style))
        comp_data = [
            ["Region", "Instance Class", "Active Cores", "Monthly Cost"],
            ["us-central1", "n2-standard-16", "256 vCPUs", "$4,200.00"],
            ["europe-west1", "c2-standard-8", "128 vCPUs", "$2,850.00"],
            ["asia-east1", "e2-highmem-4", "64 vCPUs", "$1,450.00"]
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
        
        story.append(PageBreak())
        
        # --- PAGE 2: Security Vulnerability Matrix ---
        story.append(Paragraph("SECURITY VULNERABILITY ASSESSMENT (Page 2)", title_style))
        story.append(Spacer(1, 10))
        story.append(Paragraph(f"Audit Reference: {doc_id}", subtitle_style))
        story.append(Spacer(1, 15))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cccccc")))
        story.append(Spacer(1, 15))
        
        story.append(Paragraph("Identified CVE Vulnerabilities & Remediation", h2_style))
        vuln_data = [
            ["CVE Identifier", "Severity", "Component", "Status"],
            ["CVE-2026-1042", "Critical", "OpenSSL 3.1.2", "Patched"],
            ["CVE-2026-8819", "High", "Containerd Runtime", "Pending Action"],
            ["CVE-2026-3021", "Medium", "NodeJS Base Image", "Mitigated"]
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
        
        story.append(PageBreak())
        
        # --- PAGE 3: Final Recommendations & Sign-off ---
        story.append(Paragraph("AUDIT CONCLUSION & SIGN-OFF (Page 3)", title_style))
        story.append(Spacer(1, 10))
        story.append(Paragraph(f"Audit Reference: {doc_id}", subtitle_style))
        story.append(Spacer(1, 15))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cccccc")))
        story.append(Spacer(1, 15))
        
        story.append(Paragraph("Final Architectural Sign-Off", h2_style))
        story.append(Paragraph(
            "Overall system architecture meets tier-2 enterprise standards. Implementation of automated container runtime patches "
            "is strongly recommended prior to Q4 deployment cycles.", body_style
        ))
        story.append(Spacer(1, 30))
        story.append(Paragraph("<b>Lead Security Architect:</b> Marcus Vance, CISSP", body_style))
        story.append(Paragraph("<b>Date of Certification:</b> October 11, 2026", body_style))

    # Build the PDF document
    doc.build(story)
    print(f"[+] Generated multi-page document: {filename} ({archetype})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate multi-page test documents into the root inputs folder.")
    parser.add_argument("--count", type=int, default=1, help="Number of documents to generate (default: 1)")
    args = parser.parse_args()

    inputs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "inputs"))

    for _ in range(args.count):
        generate_random_document(inputs_dir)