# project/scripts/email_templates.py

def success_mail():
    subject = "Order process Automation – SUCCESS"
    body = """
Hello Team,

Order processAutomation executed successfully.

Attached:
- Raw DMS files
- Merlin upload report
- Execution log

Regards,
Automation Bot
"""
    return subject, body


def failure_mail(error):
    subject = "Ordedr Process Automation – FAILED"
    body = f"""
Hello Team,

Order process Automation FAILED.
Error:
{error}

Please check attached log.

Regards,
Automation Bot
"""
    return subject, body
