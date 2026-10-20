import logging
from planner import plan_audit
from security import security_audit
from bugs import bug_audit
from performance import performance_audit
from reviewer import review_findings
from audit_logger import logger


def run_audits(code):
    logger.info("Starting code audit")

    try:
        logger.info("Planning audit")
        plan = plan_audit(code)
        logger.info("Selected audits: %s", plan)

        findings = {}

        if plan.security:
            logger.info("Running security audit")
            findings["security"] = security_audit(code)

        if plan.bugs:
            logger.info("Running bug audit")
            findings["bugs"] = bug_audit(code)

        if plan.performance:
            logger.info("Running performance audit")
            findings["performance"] = performance_audit(code)

        logger.info("Reviewing and consolidating findings")
        final_report = review_findings(code, findings)

        logger.info("Code audit completed successfully")
        return final_report

    except Exception:
        logger.exception("Code audit failed")
        raise


if __name__ == "__main__":
    code = """
def get_user(db, user_id):
    query = "SELECT * FROM users WHERE id=" + user_id
    return db.execute(query)
"""

    report = run_audits(code)

    print("\n" + "=" * 60)
    print("FINAL CODE AUDIT REPORT")
    print("=" * 60)
    print(report)
