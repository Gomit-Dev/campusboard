import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=60, bottom=60, left=100, right=100):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def generate_report(filename="CampusBoard_Project_Report.docx"):
    doc = Document()

    # Page Margins - Standard 1 inch
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Styles
    styles = doc.styles
    normal_style = styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(30, 41, 59)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(3)

    # Configure Heading styles for compact, elegant spacing
    h1_style = styles['Heading 1']
    h1_style.font.name = 'Calibri'
    h1_style.font.size = Pt(16)
    h1_style.font.bold = True
    h1_style.font.color.rgb = RGBColor(30, 58, 138) # Deep Navy
    h1_style.paragraph_format.space_before = Pt(12)
    h1_style.paragraph_format.space_after = Pt(4)

    h2_style = styles['Heading 2']
    h2_style.font.name = 'Calibri'
    h2_style.font.size = Pt(13)
    h2_style.font.bold = True
    h2_style.font.color.rgb = RGBColor(15, 23, 42)
    h2_style.paragraph_format.space_before = Pt(8)
    h2_style.paragraph_format.space_after = Pt(3)

    h3_style = styles['Heading 3']
    h3_style.font.name = 'Calibri'
    h3_style.font.size = Pt(11.5)
    h3_style.font.bold = True
    h3_style.font.color.rgb = RGBColor(37, 99, 235)
    h3_style.paragraph_format.space_before = Pt(6)
    h3_style.paragraph_format.space_after = Pt(2)

    # ═══════════════════════════════════════════════════════════════
    # TITLE / COVER SECTION
    # ═══════════════════════════════════════════════════════════════
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(18)
    p_title.paragraph_format.space_after = Pt(4)
    run_proj = p_title.add_run("CampusBoard")
    run_proj.font.size = Pt(30)
    run_proj.font.bold = True
    run_proj.font.color.rgb = RGBColor(30, 58, 138)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(14)
    run_sub = p_sub.add_run("Smart Campus Community, Notice Board & Collaboration Platform")
    run_sub.font.size = Pt(13)
    run_sub.font.color.rgb = RGBColor(71, 85, 105)

    p_srs = doc.add_paragraph()
    p_srs.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_srs.paragraph_format.space_after = Pt(20)
    run_srs = p_srs.add_run("SOFTWARE REQUIREMENTS SPECIFICATION (SRS)\n& PROJECT REPORT")
    run_srs.font.size = Pt(16)
    run_srs.font.bold = True
    run_srs.font.color.rgb = RGBColor(15, 23, 42)

    # Meta Table on Title Section
    table_meta = doc.add_table(rows=6, cols=2)
    table_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_meta.autofit = False

    meta_data = [
        ("Course Name:", "Full Stack Web Development / Software Engineering"),
        ("Course Code:", "[Course Code — e.g. INT219 / CSE316]"),
        ("Student Name(s):", "[Student Name]"),
        ("Registration Number(s):", "[Student Reg. No. — e.g. 12315267]"),
        ("Academic Term:", "Spring 2025 / Continuous Assessment 3 (CA3)"),
        ("Institutional Domain:", "Lovely Professional University (@lpu.in)")
    ]

    for idx, (label, val) in enumerate(meta_data):
        row = table_meta.rows[idx]
        cell_lbl, cell_val = row.cells[0], row.cells[1]
        cell_lbl.width = Inches(2.2)
        cell_val.width = Inches(4.3)
        set_cell_margins(cell_lbl, 50, 50, 80, 80)
        set_cell_margins(cell_val, 50, 50, 80, 80)
        
        p_l = cell_lbl.paragraphs[0]
        p_l.paragraph_format.space_after = Pt(2)
        r_l = p_l.add_run(label)
        r_l.font.bold = True
        r_l.font.size = Pt(10.5)
        r_l.font.color.rgb = RGBColor(15, 23, 42)

        p_v = cell_val.paragraphs[0]
        p_v.paragraph_format.space_after = Pt(2)
        r_v = p_v.add_run(val)
        r_v.font.size = Pt(10.5)
        r_v.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_page_break()

    # ═══════════════════════════════════════════════════════════════
    # REVISION HISTORY & TABLE OF CONTENTS
    # ═══════════════════════════════════════════════════════════════
    doc.add_heading("Revision History", level=1)
    
    t_rev = doc.add_table(rows=4, cols=4)
    t_rev.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Version", "Date", "Description", "Author(s)"]
    for i, h in enumerate(headers):
        cell = t_rev.rows[0].cells[i]
        set_cell_background(cell, "1E3A8A")
        set_cell_margins(cell, 50, 50, 80, 80)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(255, 255, 255)

    rev_rows = [
        ("1.0", "Sep 2026", "Initial SRS, Core Models (Student, Post, Report), Categories", "Project Team"),
        ("1.1", "Nov 2026", "Role Separation (Student vs Teacher), Announcement Access Restriction", "Project Team"),
        ("1.2", "Nov 2026", "Three-Tier RBAC (Admin Role), /panel/ Moderation & User Deletion", "Project Team")
    ]
    for r_idx, (v, d, desc, a) in enumerate(rev_rows):
        row = t_rev.rows[r_idx + 1]
        for c_idx, text in enumerate([v, d, desc, a]):
            cell = row.cells[c_idx]
            set_cell_margins(cell, 50, 50, 80, 80)
            if r_idx % 2 == 1:
                set_cell_background(cell, "F1F5F9")
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(text)
            r.font.size = Pt(9.5)

    doc.add_heading("Table of Contents", level=1)

    toc_items = [
        ("1. Introduction", "1"),
        ("   1.1 Purpose", "1"),
        ("   1.2 Scope", "1"),
        ("   1.3 Definitions, Acronyms, and Abbreviations", "2"),
        ("   1.4 References", "2"),
        ("   1.5 Overview", "2"),
        ("2. General Description", "3"),
        ("   2.1 Product Perspective", "3"),
        ("   2.2 Product Functions", "3"),
        ("   2.3 User Characteristics", "3"),
        ("   2.4 General Constraints", "4"),
        ("   2.5 Assumptions and Dependencies", "4"),
        ("3. Specific Requirements", "4"),
        ("   3.1 External Interface Requirements", "4"),
        ("       3.1.1 User Interfaces", "4"),
        ("       3.1.2 Hardware Interfaces", "5"),
        ("       3.1.3 Software Interfaces", "5"),
        ("       3.1.4 Communications Interfaces", "5"),
        ("   3.2 Functional Requirements", "5"),
        ("       3.2.1 User Authentication & Role Validation", "5"),
        ("       3.2.2 Categorized Campus Post Management", "6"),
        ("       3.2.3 Official Announcement Publishing Control", "6"),
        ("       3.2.4 Content Moderation & Reporting Pipeline", "7"),
        ("       3.2.5 Administrative User Management & Deletion", "7"),
        ("   3.5 Non-Functional Requirements", "8"),
        ("       3.5.1 Performance", "8"),
        ("       3.5.2 Reliability & Availability", "8"),
        ("       3.5.3 Security", "8"),
        ("       3.5.4 Maintainability & Portability", "8"),
        ("   3.7 Design Constraints", "9"),
        ("   3.9 Other Requirements", "9"),
        ("4. Analysis Models", "9"),
        ("   4.1 Data Flow Diagrams (Level 0 & Level 1 DFD)", "9"),
        ("   4.2 Entity-Relationship Diagram (ERD)", "10"),
        ("5. GitHub Repository Link", "11"),
        ("6. Deployed Application Link", "11"),
        ("A. Appendices", "11"),
        ("   A.1 Appendix 1: Database Migration Log", "11"),
        ("   A.2 Appendix 2: URL Routing Architecture", "12")
    ]

    for item, page in toc_items:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(1.5)
        r_item = p.add_run(item)
        r_item.font.size = Pt(10)
        if not item.startswith("   "):
            r_item.font.bold = True
        dots = " " + "." * max(4, (68 - len(item))) + " "
        r_dots = p.add_run(dots)
        r_dots.font.color.rgb = RGBColor(148, 163, 184)
        r_dots.font.size = Pt(9.5)
        r_page = p.add_run(page)
        r_page.font.bold = True
        r_page.font.size = Pt(10)

    # ═══════════════════════════════════════════════════════════════
    # SECTION 1: INTRODUCTION
    # ═══════════════════════════════════════════════════════════════
    doc.add_heading("1. Introduction", level=1)
    
    p = doc.add_paragraph()
    p.add_run("This Software Requirements Specification (SRS) document details the functional, operational, and non-functional requirements for ")
    r = p.add_run("CampusBoard")
    r.font.bold = True
    p.add_run(", a unified digital notice board and collaboration web application designed specifically for collegiate communities.")

    doc.add_heading("1.1 Purpose", level=2)
    doc.add_paragraph(
        "The purpose of this SRS is to establish a clear, structured technical foundation for the design, implementation, verification, and governance of the CampusBoard system. "
        "The intended audience includes academic evaluators, project reviewers, software engineers, and system administrators."
    )

    doc.add_heading("1.2 Scope", level=2)
    doc.add_paragraph(
        "CampusBoard provides a centralized, web-accessible platform tailored to university ecosystems (specifically Lovely Professional University). "
        "The software replaces scattered physical bulletin boards and fragmented chat groups with an organized, role-governed web portal."
    )
    p = doc.add_paragraph()
    p.add_run("Key Scope Inclusions:").font.bold = True
    bullet_scope = [
        "Three-tier Role-Based Access Control (Student, Teacher, Admin).",
        "Strict university email validation (@lpu.in) with regex ID matching (8-digit student IDs, 5-digit faculty IDs).",
        "Categorized content publishing: Notes & Resources (with file attachments), Lost & Found tracking, Campus Events, Official Announcements, and Student Help.",
        "Role-restricted announcement publishing (Teachers and Admins only).",
        "User reporting mechanism for flagging spam, false information, or offensive material.",
        "Dedicated Administration Panel (/panel/) with platform KPIs, post moderation, report dismissal, and user deletion safeguards.",
        "Modern responsive UI with persistent Light and Dark theme switching."
    ]
    for b in bullet_scope:
        p_b = doc.add_paragraph(b, style='List Bullet')
        p_b.paragraph_format.space_after = Pt(2)

    p_out = doc.add_paragraph()
    p_out.add_run("Out of Scope: ").font.bold = True
    p_out.add_run("Monetary transactions, fee processing, academic grading, and real-time socket chat.")

    doc.add_heading("1.3 Definitions, Acronyms, and Abbreviations", level=2)
    t_def = doc.add_table(rows=8, cols=2)
    t_def.alignment = WD_TABLE_ALIGNMENT.CENTER
    defs = [
        ("Term / Acronym", "Definition"),
        ("SRS", "Software Requirements Specification"),
        ("RBAC", "Role-Based Access Control — restricts system privileges based on user role."),
        ("Django MVT", "Model-View-Template software architectural design pattern."),
        ("LPU", "Lovely Professional University (campus domain constraint: @lpu.in)."),
        ("ORM", "Object-Relational Mapping (maps Python models to SQL database tables)."),
        ("CSRF", "Cross-Site Request Forgery security tokens on all POST submissions."),
        ("Cascade Delete", "Database rule: deleting a User automatically purges their posts and reports.")
    ]
    for idx, (t, d) in enumerate(defs):
        row = t_def.rows[idx]
        set_cell_margins(row.cells[0], 40, 40, 60, 60)
        set_cell_margins(row.cells[1], 40, 40, 60, 60)
        if idx == 0:
            set_cell_background(row.cells[0], "1E3A8A")
            set_cell_background(row.cells[1], "1E3A8A")
            r0 = row.cells[0].paragraphs[0].add_run(t)
            r0.font.bold = True
            r0.font.size = Pt(10)
            r0.font.color.rgb = RGBColor(255, 255, 255)
            r1 = row.cells[1].paragraphs[0].add_run(d)
            r1.font.bold = True
            r1.font.size = Pt(10)
            r1.font.color.rgb = RGBColor(255, 255, 255)
        else:
            row.cells[0].width = Inches(1.8)
            row.cells[1].width = Inches(4.7)
            if idx % 2 == 1:
                set_cell_background(row.cells[0], "F8FAFC")
                set_cell_background(row.cells[1], "F8FAFC")
            r0 = row.cells[0].paragraphs[0].add_run(t)
            r0.font.bold = True
            r0.font.size = Pt(9.5)
            r1 = row.cells[1].paragraphs[0].add_run(d)
            r1.font.size = Pt(9.5)

    doc.add_heading("1.4 References", level=2)
    refs = [
        "IEEE Std 830-1998: IEEE Recommended Practice for Software Requirements Specifications.",
        "Django 6.1 Documentation: Web Framework for Perfectionists with Deadlines (https://docs.djangoproject.com/).",
        "Python 3.14 Language Specification & Standard Library Documentation (https://www.python.org/).",
        "Bootstrap Icons Specification v1.11 (https://icons.getbootstrap.com/)."
    ]
    for r in refs:
        p_r = doc.add_paragraph(r, style='List Bullet')
        p_r.paragraph_format.space_after = Pt(1.5)

    doc.add_heading("1.5 Overview", level=2)
    doc.add_paragraph(
        "The remainder of this document is organized into standard IEEE sections. Section 2 describes the product perspective, functions, user profiles, and constraints. "
        "Section 3 outlines exact functional requirements and interface requirements. Section 4 provides architectural models (DFD and ERD). "
        "Sections 5, 6, and Appendices present technical repository links, deployment specifications, and database migration logs."
    )

    # ═══════════════════════════════════════════════════════════════
    # SECTION 2: GENERAL DESCRIPTION
    # ═══════════════════════════════════════════════════════════════
    doc.add_heading("2. General Description", level=1)

    doc.add_heading("2.1 Product Perspective", level=2)
    doc.add_paragraph(
        "CampusBoard operates as an independent, self-contained web platform developed on the Python/Django framework. "
        "It interfaces with SQLite (local development) and PostgreSQL (production). "
        "It replaces uncoordinated physical notice boards by providing structured, queryable digital feeds."
    )

    doc.add_heading("2.2 Product Functions", level=2)
    funcs = [
        ("Account Onboarding & Identity Gating:", "Validates collegiate credentials, assigns roles, and auto-verifies domain membership."),
        ("Categorized Notice Publishing:", "Enables uploading notes, lost/found tracking, event notifications, announcements, and peer assistance."),
        ("Search & Discovery:", "Full-text search combined with category filtering, status filtering (Active/Resolved), and chronological sorting."),
        ("Peer Contact Channel:", "One-click mailto: integration with clean contextual etiquette for faculty and students."),
        ("Content Moderation Pipeline:", "Community reporting mechanism paired with administrative post dismissal and content removal."),
        ("Administrative Operations Console:", "Platform KPI tracking, user filtering/search, and safe account deletion with cascade protection.")
    ]
    for title, desc in funcs:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(2)
        r1 = p.add_run(title + " ")
        r1.font.bold = True
        p.add_run(desc)

    doc.add_heading("2.3 User Characteristics", level=2)
    u_types = [
        ("Student Users:", "Regular collegiate students who use the platform to share study notes, report lost items, check events, and ask questions. Restricted from posting official announcements."),
        ("Faculty / Teacher Users:", "Teachers who post official academic announcements and departmental updates reaching the entire campus."),
        ("Platform Administrators:", "Privileged staff who review reports, remove spam/offensive posts, and permanently delete rule-breaking users.")
    ]
    for u_name, u_desc in u_types:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(2)
        p.add_run(u_name + " ").font.bold = True
        p.add_run(u_desc)

    doc.add_heading("2.4 General Constraints", level=2)
    constraints = [
        "Domain Restriction: Users must register with an authorized email matching @lpu.in.",
        "Framework Constraint: Built with Django 6.1 adhering strictly to Model-View-Template architecture.",
        "Stateless Client Architecture: Session state managed via secure HTTP cookies and Django session engine.",
        "File Storage Constraints: Uploaded images restricted to image/* MIME types; documents restricted to .pdf, .doc, .docx.",
        "Platform Independence: Fully responsive across Chrome, Firefox, Safari, Edge, and mobile browsers."
    ]
    for c in constraints:
        p = doc.add_paragraph(c, style='List Bullet')
        p.paragraph_format.space_after = Pt(1.5)

    doc.add_heading("2.5 Assumptions and Dependencies", level=2)
    doc.add_paragraph(
        "Users possess active internet connectivity and modern HTML5 web browsers. "
        "Dependencies include Python 3.12+, Django 6.1, Pillow, python-docx, and python-pptx."
    )

    # ═══════════════════════════════════════════════════════════════
    # SECTION 3: SPECIFIC REQUIREMENTS
    # ═══════════════════════════════════════════════════════════════
    doc.add_heading("3. Specific Requirements", level=1)

    doc.add_heading("3.1 External Interface Requirements", level=2)
    
    doc.add_heading("3.1.1 User Interfaces", level=3)
    ui_views = [
        "Home Page (/): Hero section with custom SVG illustration, live category count cards, search bar, and recent active posts.",
        "Browse Page (/posts/browse/): Multi-filter sidebar (category, status, sort order), responsive cards grid, and pagination.",
        "Post Detail (/posts/<id>/): Author avatar, role badge, post metadata, attachment viewer, contact button, and report button.",
        "Post Creation Form (/posts/create/): Dynamic form showing conditional fields (Lost/Found date/location) and filtering category choices based on role.",
        "Admin Moderation Console (/panel/): Metrics grid, reported posts queue with dismiss/remove buttons, and user search/deletion table."
    ]
    for v in ui_views:
        p = doc.add_paragraph(v, style='List Bullet')
        p.paragraph_format.space_after = Pt(1.5)

    doc.add_heading("3.1.2 Hardware Interfaces", level=3)
    doc.add_paragraph("Server requires min. 1 vCPU, 1 GB RAM, 10 GB persistent storage. Clients require any smartphone, laptop, or desktop.")

    doc.add_heading("3.1.3 Software Interfaces", level=3)
    doc.add_paragraph("Python 3.12/3.14 on Linux/Windows. Relational storage via SQLite (dev) and PostgreSQL (prod). Web server support via WSGI/ASGI.")

    doc.add_heading("3.1.4 Communications Interfaces", level=3)
    doc.add_paragraph("HTTP/HTTPS over TCP/IP (Ports 80/443). Client-side email triggers utilize RFC 6068 mailto URI schemes.")

    doc.add_heading("3.2 Functional Requirements", level=2)

    # 3.2.1
    doc.add_heading("3.2.1 User Authentication & Role Validation", level=3)
    doc.add_paragraph().add_run("Description: ").font.bold = True
    doc.paragraphs[-1].add_run("Ensures secure onboarding, authentication, and role allocation using email-as-username.")
    doc.add_paragraph("Inputs: Full Name, Role ('student' or 'teacher'), College Email, Password, Confirm Password.")
    doc.add_paragraph(
        "Processing:\n"
        "1. clean_email() normalizes address and verifies uniqueness in Student model.\n"
        "2. Domain verification confirms address terminates with @lpu.in.\n"
        "3. If Student: regex strictly checks ^\\d{8}@lpu\\.in$ (8-digit roll number).\n"
        "4. If Teacher: regex strictly checks ^\\d{5}@lpu\\.in$ (5-digit employee ID).\n"
        "5. Passwords compared for exact match and hashed using PBKDF2 with SHA256."
    )
    doc.add_paragraph("Outputs: Created Student instance; user session initialized with immediate redirect to homepage.")
    doc.add_paragraph("Error Handling: Clear field-level error messages ('Student email must be 8 digits', 'Passwords do not match').")

    # 3.2.2
    doc.add_heading("3.2.2 Categorized Campus Post Management", level=3)
    doc.add_paragraph().add_run("Description: ").font.bold = True
    doc.paragraphs[-1].add_run("Enables users to publish, edit, browse, search, and resolve campus notices.")
    doc.add_paragraph("Inputs: Title, Category (notes, lost_found, events, announcements, student_help), Description, File/Image uploads, Item Location/Date, Event Date/Time.")
    doc.add_paragraph(
        "Processing:\n"
        "1. Validates required fields and file formats (PDF, DOCX, PNG, JPG).\n"
        "2. Binds post author to request.user.\n"
        "3. Stores record in posts_post table.\n"
        "4. Authors can mark status as 'Resolved' or 'Closed' when issues are handled."
    )
    doc.add_paragraph("Outputs: Detailed post webpage with shareable URL (/posts/<id>/).")
    doc.add_paragraph("Error Handling: Non-authors attempting to edit or delete posts receive an HTTP 403 Forbidden response.")

    # 3.2.3
    doc.add_heading("3.2.3 Official Announcement Publishing Control", level=3)
    doc.add_paragraph().add_run("Description: ").font.bold = True
    doc.paragraphs[-1].add_run("Protects the campus community from unauthorized or fraudulent official notices.")
    doc.add_paragraph("Inputs: Post category selection.")
    doc.add_paragraph(
        "Processing:\n"
        "1. PostForm.__init__() evaluates user.is_teacher.\n"
        "2. If user is a student, the 'Announcements' option is removed from the form dropdown.\n"
        "3. Server-side validation rejects any manual form tampering attempting to set category='announcements'."
    )
    doc.add_paragraph("Outputs: Official notices carry a distinct Announcement badge with high visibility across the portal.")

    # 3.2.4
    doc.add_heading("3.2.4 Content Moderation & Reporting Pipeline", level=3)
    doc.add_paragraph().add_run("Description: ").font.bold = True
    doc.paragraphs[-1].add_run("Empowers community self-policing through structured post reporting.")
    doc.add_paragraph("Inputs: Target Post ID, Flag Reason (spam, inappropriate, fake, other), Explanatory details.")
    doc.add_paragraph(
        "Processing:\n"
        "1. Verifies reporter != post.author (users cannot report own posts).\n"
        "2. Checks unique_together constraint on [post, reporter] to stop duplicate spam reporting.\n"
        "3. Records report and increments post report counter in /panel/ queue."
    )
    doc.add_paragraph("Outputs: Confirmation message to user; entry displayed in Admin Moderation queue.")

    # 3.2.5
    doc.add_heading("3.2.5 Administrative User Management & Deletion Power", level=3)
    doc.add_paragraph().add_run("Description: ").font.bold = True
    doc.paragraphs[-1].add_run("Grants authorized staff the power to monitor metrics, dismiss reports, remove posts, and permanently delete users.")
    doc.add_paragraph("Inputs: User search query, Role filter, User ID for deletion.")
    doc.add_paragraph(
        "Processing:\n"
        "1. Endpoint secured with @staff_member_required.\n"
        "2. Self-Deletion Guard: if target_user == request.user, deletion is rejected with an error.\n"
        "3. Superuser Hierarchy Check: Non-superusers cannot delete superuser accounts.\n"
        "4. On POST confirmation, target_user.delete() executes, cascading deletion to all their posts and reports."
    )
    doc.add_paragraph("Outputs: Clean removal of user and associated records; flash message confirmation.")

    doc.add_heading("3.5 Non-Functional Requirements", level=2)
    nfr_items = [
        ("3.5.1 Performance:", "Page load times remain under 800ms for browse queries. Media files served efficiently with client-side caching."),
        ("3.5.2 Reliability:", "Database transactions execute with ACID guarantees. Database cascade rules eliminate orphaned records."),
        ("3.5.3 Availability:", "Designed for 99.9% uptime. Automated health-check endpoints support containerized orchestration."),
        ("3.5.4 Security:", "Mandatory CSRF token verification, PBKDF2 password encryption, SQL injection defense via Django ORM parameterization, and XSS sanitization in templates."),
        ("3.5.5 Maintainability:", "Adherence to Django conventions, strict separation between accounts and posts apps, clear migrations history."),
        ("3.5.6 Portability:", "Runs identically on Windows, Linux, and macOS environments without platform-specific code.")
    ]
    for nfr_t, nfr_d in nfr_items:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(2)
        p.add_run(nfr_t + " ").font.bold = True
        p.add_run(nfr_d)

    doc.add_heading("3.7 Design Constraints", level=2)
    doc.add_paragraph(
        "Compliance with university IT policies; email domain hardcoded to @lpu.in with debug bypass toggle for local sandbox testing."
    )

    doc.add_heading("3.9 Other Requirements", level=2)
    doc.add_paragraph(
        "Accessibility: Semantic HTML5 tags (header, nav, main, footer) and high-contrast color ratios for WCAG 2.1 compliance in both dark and light modes."
    )

    # ═══════════════════════════════════════════════════════════════
    # SECTION 4: ANALYSIS MODELS
    # ═══════════════════════════════════════════════════════════════
    doc.add_heading("4. Analysis Models", level=1)

    doc.add_heading("4.1 Data Flow Diagrams (DFD)", level=2)
    
    doc.add_heading("Level 0 DFD (Context Diagram)", level=3)
    doc.add_paragraph(
        "The Level 0 DFD portrays CampusBoard as a central processing entity interacting with three external entities:\n"
        "• Student Entity: Sends registration data, posts, search queries, and reports. Receives verified feeds, post details, and status updates.\n"
        "• Teacher Entity: Sends registration data, announcements, and notes. Receives campus feed and contact queries.\n"
        "• Administrator Entity: Sends moderation commands, post deletions, and user deletions. Receives system analytics, reported post queues, and user logs."
    )

    doc.add_heading("Level 1 DFD (Decomposed Processes)", level=3)
    doc.add_paragraph(
        "1.0 Process Authentication & Role Gating (Interacts with Users Data Store D1)\n"
        "2.0 Process Post Creation & Validation (Interacts with Posts Data Store D2 & Media Store D3)\n"
        "3.0 Process Search, Filter & Browse (Reads from D2 with active status filters)\n"
        "4.0 Process Post Reporting & Flagging (Writes to Reports Data Store D4)\n"
        "5.0 Process Administrative Moderation & Deletion (Manages D1, D2, D4 with Cascade Integrity)"
    )

    doc.add_heading("4.2 Entity-Relationship Diagram (ERD)", level=2)
    t_erd = doc.add_table(rows=4, cols=3)
    t_erd.alignment = WD_TABLE_ALIGNMENT.CENTER
    erd_headers = ["Entity", "Primary Attributes", "Relationships"]
    for i, h in enumerate(erd_headers):
        cell = t_erd.rows[0].cells[i]
        set_cell_background(cell, "1E3A8A")
        set_cell_margins(cell, 40, 40, 60, 60)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(255, 255, 255)

    erd_data = [
        ("Student (User)", "id (PK), email (UQ), full_name, role, is_verified, password, date_joined", "1-to-Many with Post (as author)\n1-to-Many with Report (as reporter)"),
        ("Post", "id (PK), author_id (FK), category, title, description, image, file, status, created_at", "Many-to-1 with Student\n1-to-Many with Report"),
        ("Report", "id (PK), post_id (FK), reporter_id (FK), reason, details, created_at", "Many-to-1 with Post (CASCADE)\nMany-to-1 with Student (CASCADE)\nUQ(post_id, reporter_id)")
    ]
    for r_i, (e, a, rel) in enumerate(erd_data):
        row = t_erd.rows[r_i + 1]
        for c_i, val in enumerate([e, a, rel]):
            cell = row.cells[c_i]
            set_cell_margins(cell, 40, 40, 60, 60)
            if r_i % 2 == 1:
                set_cell_background(cell, "F1F5F9")
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val)
            r.font.size = Pt(9.5)

    # ═══════════════════════════════════════════════════════════════
    # SECTIONS 5 & 6: REPOSITORY & DEPLOYMENT LINKS
    # ═══════════════════════════════════════════════════════════════
    doc.add_heading("5. GitHub Repository Link", level=1)
    p = doc.add_paragraph()
    p.add_run("Repository URL: ").font.bold = True
    r = p.add_run("https://github.com/[Your-Username]/campusboard")
    r.font.color.rgb = RGBColor(37, 99, 235)
    r.font.underline = True
    doc.add_paragraph("Branch: main / production | License: MIT License | Tech Stack: Django 6.1, Python 3.14, SQLite/PostgreSQL")

    doc.add_heading("6. Deployed Application Link", level=1)
    p = doc.add_paragraph()
    p.add_run("Application URL: ").font.bold = True
    r = p.add_run("https://campusboard.lpu.in (or http://127.0.0.1:8000/ for Local Demonstration)")
    r.font.color.rgb = RGBColor(37, 99, 235)
    doc.add_paragraph("Deployment Infrastructure: Python WSGI Application, Gunicorn HTTP Server, Nginx Reverse Proxy.")

    # ═══════════════════════════════════════════════════════════════
    # APPENDICES
    # ═══════════════════════════════════════════════════════════════
    doc.add_heading("A. Appendices", level=1)

    doc.add_heading("A.1 Appendix 1: Database Migration Log", level=2)
    mig_info = [
        ("accounts.0001_initial.py", "Creates custom Student user model inheriting AbstractUser, drops username, sets email as unique identifier, adds is_verified and full_name."),
        ("accounts.0002_alter_student_options_student_role_and_more.py", "Introduces role field (Student vs Teacher), updates verbose name to 'user', updates is_verified to 'campus member'."),
        ("accounts.0003_alter_student_role.py", "Upgrades role choices to 3-tier architecture: [('student', 'Student'), ('teacher', 'Teacher'), ('admin', 'Admin')]."),
        ("posts.0001_initial.py", "Creates Post table with author FK (CASCADE), category choices, attachments, and Report table with post FK (CASCADE), reporter FK (CASCADE), and unique_together constraint.")
    ]
    for mf, md in mig_info:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(2)
        p.add_run(mf + ": ").font.bold = True
        p.add_run(md)

    doc.add_heading("A.2 Appendix 2: URL Routing Reference", level=2)
    t_url = doc.add_table(rows=12, cols=3)
    t_url.alignment = WD_TABLE_ALIGNMENT.CENTER
    u_headers = ["URL Pattern", "View Controller", "Access Level"]
    for i, h in enumerate(u_headers):
        cell = t_url.rows[0].cells[i]
        set_cell_background(cell, "1E3A8A")
        set_cell_margins(cell, 40, 40, 60, 60)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(255, 255, 255)

    routes = [
        ("/", "home_view", "Public / All Users"),
        ("/accounts/register/", "register_view", "Public (Guest)"),
        ("/accounts/login/", "login_view", "Public (Guest)"),
        ("/accounts/logout/", "logout_view", "Authenticated"),
        ("/accounts/profile/", "profile_view", "Authenticated"),
        ("/posts/browse/", "browse_view", "Public / All Users"),
        ("/posts/create/", "post_create_view", "Authenticated (Role-gated)"),
        ("/posts/<int:pk>/", "post_detail_view", "Public / All Users"),
        ("/posts/<int:pk>/report/", "report_post_view", "Authenticated (Non-author)"),
        ("/panel/", "admin_dashboard_view", "Staff / Admin Only"),
        ("/panel/user/<int:pk>/delete/", "admin_delete_user_view", "Staff / Admin Only")
    ]
    for r_idx, (u, v, a) in enumerate(routes):
        row = t_url.rows[r_idx + 1]
        for c_idx, val in enumerate([u, v, a]):
            cell = row.cells[c_idx]
            set_cell_margins(cell, 40, 40, 60, 60)
            if r_idx % 2 == 1:
                set_cell_background(cell, "F1F5F9")
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val)
            r.font.size = Pt(9.5)

    doc.save(filename)
    print(f"Compact project report successfully generated as '{filename}'.")

if __name__ == "__main__":
    generate_report()
