from transaction import commit

import sys


site = app[sys.argv[3]]  # noqa:F821

if not site.MailHost.smtp_queue:
    site.MailHost.smtp_queue = True
if site.MailHost.smtp_queue_directory != sys.argv[4]:
    site.MailHost.smtp_queue_directory = sys.argv[4]

commit()
