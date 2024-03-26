import logging
import sys

from recensio.plone.subscribers.review import update_generated_pdf
from slc.zopescript.script import InstanceScript
from transaction import commit

logger = logging.getLogger(__name__)


class GeneratePdfs(InstanceScript):
    def run(self):
        reviews = self.portal.portal_catalog(
            object_provides="recensio.plone.interfaces.IReview"
        )
        for brain in reviews:
            review = brain.getObject()
            if not getattr(review, "generatedPdf", None) and hasattr(review, "review"):
                logger.info("Updating PDF for %s", brain.getPath())
                update_generated_pdf(review)
                commit()


site = sys.argv[3]  # noqa:F821
GeneratePdfs(app)("admin", portal_id=site)
