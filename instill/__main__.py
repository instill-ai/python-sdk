#!/usr/bin/env python

"""Package entry point."""
import pprint

from instill.configuration import global_config

if __name__ == "__main__":  # pragma: no cover
    # main()  # pylint: disable=no-value-for-parameter
    print("======================Configured Hosts======================")
    pprint.pprint(global_config.hosts)
