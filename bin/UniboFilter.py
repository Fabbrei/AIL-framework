#!/usr/bin/env python3
# -*-coding:UTF-8 -*
"""
    Template for new modules
"""

import time
from pubsublogger import publisher
from packages import Paste

from Helper import Process
import re

REGEX = "[[a-zA-Z0-9\\._-]+@unibo|@studio.unibo+\.[a-zA-Z]{2,6}"


def find_regex(message):
    unibo = re.findall(REGEX,message,re.IGNORECASE)

    return len(unibo)

if __name__ == '__main__':
    # If you wish to use an other port of channel, do not forget to run a subscriber accordingly (see launch_logs.sh)
    # Port of the redis instance used by pubsublogger
    publisher.port = 6380
    # Script is the default channel used for the modules.
    publisher.channel = 'Script'

    # Section name in bin/packages/modules.cfg
    config_section = 'UniboFilter'
    
    # Setup the I/O queues
    p = Process(config_section)

    # Sent to the logging a description of the module
    publisher.info("Unibo Filter Module")

    # Endless loop getting messages from the input queue
    while True:
        # Get one message from the input queue
        filename = p.get_from_set()
        if filename is None:
            publisher.debug("{} queue is empty, waiting".format(config_section))
            time.sleep(1)
            continue

        paste = Paste.Paste(filename)
        content = paste.get_p_content()

        # Do something with the message from the queue
        found = find_regex(content)

        if found != 0:
            msg='infoleak:automatic-detection="Unibo-creds";'
            categ = "Tags"
            p.populate_set_out(msg,categ)
            publisher.critical(
                    'UNIBO;{};{};{};found {} email unibo;{}'.format(
                        paste.p_source, paste.p_date, paste.p_name,
                        found, paste.p_rel_path))


