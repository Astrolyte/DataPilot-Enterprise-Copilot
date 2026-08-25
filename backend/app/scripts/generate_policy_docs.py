from pathlib import Path

DOCS_DIR = Path("backend/data/documents")

# Each entry: (relative_path, department, allowed_roles, content)
POLICY_DOCS = [
    ("finance/refund_policy.txt", "finance", ["finance", "sales", "admin"], """
AcmeCloud Refund Policy

AcmeCloud offers refunds according to the terms specified in each
customer's signed contract. Standard contracts include a 15-30 day
refund window from the date of purchase. Enterprise contracts extend
this window to 30-60 days. Custom contracts may specify extended
refund windows of up to 120 days, as negotiated individually.

Refund requests must be submitted in writing to finance@acmecloud.com
and include the original order ID. Refunds are processed within 10
business days of approval. Partial refunds are calculated on a
pro-rated basis for annual subscriptions cancelled mid-term.
"""),
    ("finance/invoice_policy.txt", "finance", ["finance", "admin"], """
AcmeCloud Invoice Policy

Invoices are issued monthly for all active subscriptions, on the
anniversary date of contract signing. Enterprise customers may
request quarterly or annual consolidated invoicing.

Payment terms are net-30 from invoice date unless otherwise specified
in the customer contract. Overdue invoices incur a 1.5% monthly late
fee after a 15-day grace period.
"""),
    ("finance/payment_policy.txt", "finance", ["finance", "sales", "admin"], """
AcmeCloud Payment Policy

Accepted payment methods include ACH transfer, wire transfer, and
major credit cards for contracts under $50,000 annual value. Contracts
above this threshold require ACH or wire transfer.

Failed payments trigger an automated retry after 3 business days.
Accounts with two consecutive failed payments are flagged for
account manager review before service suspension.
"""),
    ("sales/discount_policy.txt", "sales", ["sales", "admin"], """
AcmeCloud Discount Policy

Standard discount authority for Account Executives is up to 10% off
list price. Discounts between 10-20% require Sales Manager approval.
Discounts above 20% require VP Sales approval and are reserved for
multi-year enterprise commitments.

Volume discounts apply automatically for orders exceeding 5 product
licenses in a single transaction.
"""),
    ("sales/pricing_policy.txt", "sales", ["sales", "admin"], """
AcmeCloud Pricing Policy

List pricing is tiered by product category: Analytics, Security,
Collaboration, Infrastructure, and AI products each have independent
pricing schedules published internally.

Enterprise segment customers are eligible for custom pricing
negotiated at contract signing. SMB and mid-market customers are
generally subject to list pricing with standard discount bands.
"""),
    ("sales/commission_policy.txt", "sales", ["sales", "finance", "admin"], """
AcmeCloud Commission Policy

Account Executives earn commission on closed-won revenue at a base
rate of 8%, rising to 10% after exceeding quarterly quota. Renewals
are commissioned at 4%.

Commission is paid the month following invoice collection, not at
deal close, to align incentives with actual realized revenue.
"""),
    ("hr/employee_handbook.txt", "hr", ["hr", "admin"], """
AcmeCloud Employee Handbook (Summary)

This handbook covers core policies for all AcmeCloud employees,
including code of conduct, working hours, and reporting structure.
Employees are expected to complete onboarding training within their
first two weeks.

Full policy details are maintained by the HR department and updated
annually each January.
"""),
    ("hr/leave_policy.txt", "hr", ["hr", "admin"], """
AcmeCloud Leave Policy

Full-time employees accrue 20 days of paid time off annually, plus
10 company holidays. PTO accrues monthly and may be carried over up
to 5 days into the following year.

Sick leave is separate from PTO, with 10 days annually that do not
require advance notice. Extended medical leave follows applicable
regional regulations.
"""),
    ("hr/remote_work_policy.txt", "hr", ["hr", "admin"], """
AcmeCloud Remote Work Policy

Employees in Support, Engineering, and Analytics roles are eligible
for full remote work. Sales and Account Management roles require
in-region presence for client meetings but may work remotely
otherwise.

Remote employees must maintain core overlap hours of 10am-3pm in
their local timezone for team coordination.
"""),
    ("security/security_policy.txt", "security", ["admin"], """
AcmeCloud Security Policy

All customer data is encrypted at rest using AES-256 and in transit
using TLS 1.2 or higher. Access to production customer data requires
multi-factor authentication and is logged for audit purposes.

Employees are granted the minimum access necessary for their role.
Access reviews occur quarterly.
"""),
    ("security/incident_response.txt", "security", ["admin"], """
AcmeCloud Incident Response Policy

Security incidents must be reported to the security team within 1
hour of detection. Customer-impacting incidents trigger notification
to affected customers within 72 hours, in line with standard
regulatory requirements.

The incident response team conducts a post-mortem within 5 business
days of resolution for all Severity 1 and 2 incidents.
"""),
    ("security/password_policy.txt", "security", ["admin", "hr"], """
AcmeCloud Password Policy

All internal systems require passwords of at least 12 characters with
multi-factor authentication enabled. Passwords must be rotated every
90 days for systems handling customer financial data.

Shared or generic accounts are prohibited except for designated
service accounts with restricted, logged access.
"""),
    ("product/product_overview.txt", "product", ["sales", "support", "admin"], """
AcmeCloud Product Overview

AcmeCloud offers products across five categories: Analytics, Security,
Collaboration, Infrastructure, and AI. Each category includes tiered
offerings suited to SMB, mid-market, and enterprise customers.

Enterprise tier products include dedicated support and custom SLA
options not available on standard tiers.
"""),
    ("product/support_policy.txt", "product", ["support", "sales", "admin"], """
AcmeCloud Support Policy

Standard support includes email support with a 24-business-hour
response time. Enterprise contracts include priority support with
4-hour response time and a dedicated Customer Success Manager.

Critical (Severity 1) issues are supported 24/7 regardless of
contract tier.
"""),
    ("product/sla_policy.txt", "product", ["support", "sales", "admin"], """
AcmeCloud SLA Policy

Standard tier: 99.5% uptime guarantee, measured monthly.
Enterprise tier: 99.9% uptime guarantee with service credits for
breaches, measured monthly.

Planned maintenance windows are excluded from uptime calculations
and are announced at least 72 hours in advance.
"""),
]


def main():
    for relative_path, department, allowed_roles, content in POLICY_DOCS:
        file_path = DOCS_DIR / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)

        header = (
            f"[department: {department}]\n"
            f"[allowed_roles: {','.join(allowed_roles)}]\n\n"
        )
        file_path.write_text(header + content.strip() + "\n")

    print(f"Generated {len(POLICY_DOCS)} policy documents in {DOCS_DIR}/")


if __name__ == "__main__":
    main()