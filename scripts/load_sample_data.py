import os
import sys
import django

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from apps.documents.models import Document
from apps.documents.ingestion.embedding_generator import generate_embeddings_for_text

def create_sample_documents():
    documents = [
        {
            "title": "Tender Procurement Guidelines 2024",
            "content": """
TENDER ELIGIBILITY REQUIREMENTS:
- Registered contractors with valid business licenses
- Minimum 3 years experience in relevant field
- Financial stability with turnover of at least $500,000 annually
- Clean criminal record and tax compliance certificate
- Professional indemnity insurance coverage

REQUIRED DOCUMENTS FOR TENDER SUBMISSION:
1. Business Registration Certificate
2. Tax Clearance Certificate
3. Financial Statements for last 3 years
4. Proof of Experience (previous project contracts)
5. Technical Proposals and Methodologies
6. CVs of Key Personnel
7. Quality Assurance Plans
8. Health and Safety Compliance Certificates
9. Environmental Impact Assessment (if applicable)
10. Bank Reference Letters

SUBMISSION DEADLINES:
- Tender notices published 30 days before closing
- Submission deadline: 5:00 PM on the specified closing date
- Late submissions will not be accepted under any circumstances
- Extensions may be granted in exceptional cases

SUBMISSION FORMAT:
- All documents must be submitted in PDF format
- Maximum file size: 50MB per document
- Use the official tender application template
- Submit via the online procurement portal only
- Hard copies not accepted unless specified

EVALUATION CRITERIA:
- Technical compliance (40% weight)
- Price competitiveness (30% weight)
- Past performance (20% weight)
- Local content preference (10% weight)
- Evaluation completed within 30 days of closing

CONTACT INFORMATION:
- Procurement Office: procurement@school.edu
- Phone: +1-234-567-8900
- Office Hours: Monday-Friday 9AM-5PM
- Clarifications must be requested in writing 7 days before deadline
            """
        },
        {
            "title": "School Admission Policy 2024-2025",
            "content": """
ADMISSION ELIGIBILITY CRITERIA:
- Age requirements: 5-18 years for primary and secondary
- Academic performance in previous institution
- Good conduct certificate required
- Medical fitness certificate
- Proof of residency in catchment area (priority given)
- Siblings already enrolled get preference

REQUIRED DOCUMENTS FOR ADMISSION:
1. Birth Certificate
2. Previous School Leaving Certificate
3. Academic Transcripts/Report Cards
4. Conduct Certificate from previous school
5. Medical Fitness Certificate
6. Proof of Address (utility bills, lease agreement)
7. Parent/Guardian ID and proof of relationship
8. Immunization Records
9. Passport-sized photographs (4 copies)
10. Admission Application Form (duly filled)

APPLICATION DEADLINES:
- Early bird applications: January 15 - February 28
- Regular applications: March 1 - April 30
- Late applications: May 1 - June 15 (with late fee)
- Admission tests conducted in May-June
- Results announced within 2 weeks of test

ADMISSION PROCESS:
1. Submit complete application package
2. Pay non-refundable application fee of $50
3. Appear for entrance examination (if applicable)
4. Attend parent interview
5. Medical examination
6. Final selection and offer letter
7. Pay admission fee within 7 days to secure seat

FEES AND PAYMENTS:
- Admission fee: $200 (one-time)
- Annual tuition: $2,500 (payable quarterly)
- Development fee: $300 annually
- Transportation fee: $400 quarterly (optional)
- Activity fee: $150 annually

CONTACT FOR ADMISSIONS:
- Admissions Office: admissions@school.edu
- Phone: +1-234-567-8901
- Office Hours: Monday-Friday 8AM-4PM
- Visit our website for online application portal
            """
        },
        {
            "title": "Fee Structure and Payment Guidelines",
            "content": """
TUITION FEE STRUCTURE:
- Primary (Grades 1-5): $1,800 per annum
- Middle (Grades 6-8): $2,200 per annum
- Secondary (Grades 9-10): $2,800 per annum
- Senior Secondary (Grades 11-12): $3,200 per annum
- International students: 25% surcharge

FEE PAYMENT SCHEDULE:
- Annual payment: Due July 1st, 10% discount
- Quarterly payments: July 1, October 1, January 1, April 1
- Monthly payments: Available with 5% surcharge
- Late payment penalty: 2% per month after due date

PAYMENT METHODS ACCEPTED:
1. Online banking transfer to school account
2. Credit/Debit card payments via portal
3. Bank draft/cheque (payable to school name)
4. Cash payments at school office (receipt required)
5. Third-party payment processors (additional fees apply)

FEE BREAKDOWN DETAILS:
- Academic fees: 70% of total tuition
- Facilities and maintenance: 15%
- Staff salaries: 10%
- Administrative costs: 5%

PAYMENT CONFIRMATION:
- Online payments: Instant confirmation email
- Bank transfers: Confirmation within 2 working days
- Cheque payments: Cleared within 7-10 working days
- Keep all receipts and transaction IDs

REFUND POLICY:
- Admission fee: Non-refundable
- Tuition fees: Prorated refund for withdrawal
- Notice period: 30 days for refund processing
- Medical withdrawals: Full refund considered

FINANCIAL AID AND SCHOLARSHIPS:
- Merit-based scholarships: Up to 50% tuition waiver
- Need-based assistance: Means-tested
- Sibling discounts: 10% for second child
- Early bird discount: 10% for annual payment

CONTACT FINANCE OFFICE:
- Finance Department: finance@school.edu
- Phone: +1-234-567-8902
- Office Hours: Monday-Friday 9AM-3PM
- Online payment portal: payments.school.edu
            """
        },
        {
            "title": "School Code of Conduct and Discipline Policy",
            "content": """
STUDENT CONDUCT EXPECTATIONS:
- Respect for teachers, staff, and fellow students
- Punctuality and regular attendance
- Academic honesty and integrity
- Proper uniform and personal grooming
- Use of appropriate language and behavior
- Care for school property and environment

DISCIPLINARY MEASURES:
- Verbal warning for minor infractions
- Written warning with parent notification
- Detention or community service
- Suspension (1-5 days) for serious offenses
- Expulsion in extreme cases (violence, drugs, etc.)

ATTENDANCE REQUIREMENTS:
- Minimum 90% attendance required
- Medical certificates for absences
- Prior permission for planned leaves
- Make-up work for excused absences
- Parent notification for unexcused absences

UNIFORM AND APPEARANCE:
- Complete uniform as specified
- Clean and well-maintained clothing
- School ID card must be worn
- Hair neatly groomed and appropriate length
- No jewelry except stud earrings

TECHNOLOGY USAGE POLICY:
- School devices for educational purposes only
- No social media during school hours
- Internet usage monitored and filtered
- Personal devices must be silent and out of sight
- Cyberbullying strictly prohibited

PARENTAL INVOLVEMENT:
- Regular parent-teacher meetings
- PTM schedule: Quarterly meetings
- Online portal for progress tracking
- Volunteer opportunities available
- Parent feedback encouraged

EMERGENCY CONTACTS:
- School Security: +1-234-567-8903
- Nurse Office: +1-234-567-8904
- Principal Office: +1-234-567-8905
- Emergency Services: 911
            """
        }
    ]

    for doc_data in documents:
        if not Document.objects.filter(title=doc_data["title"]).exists():
            doc = Document.objects.create(
                title=doc_data["title"],
                text=doc_data["content"]
            )
            print(f"Created document: {doc.title}")
            # Generate embeddings
            generate_embeddings_for_text(doc.id, doc.text)
            print(f"Generated embeddings for: {doc.title}")

if __name__ == "__main__":
    create_sample_documents()
    print("Sample data loaded successfully!")