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



FULLZ_ELEMENTS = ["name", "age", "sex" ,"height", "birthday", "employment", "passport","address"]




def find_fullz(message):

    content = message.lower()

    counter = 0
    
    for x in FULLZ_ELEMENTS:

        if x in content:
            counter += 1


    return counter

if __name__ == '__main__':
    # If you wish to use an other port of channel, do not forget to run a subscriber accordingly (see launch_logs.sh)
    # Port of the redis instance used by pubsublogger
    publisher.port = 6380
    # Script is the default channel used for the modules.
    publisher.channel = 'Script'

    # Section name in bin/packages/modules.cfg
    config_section = 'FullzScript'
    
    # Setup the I/O queues
    p = Process(config_section)

    # Sent to the logging a description of the module
    publisher.info("Fullz Finder Module")

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
        found = find_fullz(content)

        if found >= 6:
            msg = "found Fullz!!"
            categ = "Web"
            p.populate_set_out(msg,categ)
            publisher.critical(
                    'Fullz;{};{};{};found Fullz of {}/{} Elements;{}'.format(
                        paste.p_source, paste.p_date, paste.p_name,
                        found,len(FULLZ_ELEMENTS), paste.p_rel_path))



