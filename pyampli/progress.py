#!/usr/bin/python

import sys, logging, time


def update_progress(variant_number, amount_total_variants):
    progress = (float(variant_number) / float(amount_total_variants))
    barLength = 100  # Modify this to change the length of the progress bar
    status = "- running - "
    if isinstance(progress, int):
        progress = float(progress)
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    elif progress >= 1:
        #time.sleep(1)
        #sys.stdout.write("\033[F")  # back to previous line
        #time.sleep(1)
        #sys.stdout.write("\033[K")  # clear line
        #sys.stdout.write("\033[K")  # clear line

        time.sleep(3)
        sys.stdout.flush()
        #logging.info('\r')
        logging.info('\rVCF processing done')
    else:
        block = int(round(barLength * progress))
        text = "\r\t\t>>> Status : [{0}] {1}% {2} <<<".format("#" * block + "-" * (barLength - block),
                                                                               round((progress * 100), 2), status)
        sys.stdout.write(text)
        sys.stdout.flush()
