from scrapy import signals
from scrapy.exceptions import NotConfigured
import glob
import filecmp

class EmailOnChange(object):
    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool("EMAIL_ON_CHANGE_ENALBLED"):
            raise NotConfigured

        # Create an instance of our extension
        extension = cls()

        crawler.signals.connect(extension.engine_stopped, signal=signals.engine_stopped)

        return extension

    def engine_stopped(self):
        runs = sorted(glob.glob("/Users/jennynguyen/Downloads/output/[0-9]*-[0-9]*-[0-9]*T[0-9]*-[0-9]*-[0-9]*.json"), reverse=True)

        if len(runs) < 2:
            # We can't compare if there're only 1 run
            return

        current_file, previous_file = runs[0:2]
        if not filecmp.cmp(current_file, previous_file):
            print("\n\nTHE FILES ARE DIFFERENT\n\n")
        else:
            print("\n\nNO CHANGE\n\n")



