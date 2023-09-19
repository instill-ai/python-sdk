#!/usr/bin/env python

"""Package entry point."""
import pprint

from instill_sdk.configuration import config

# from instill_sdk.client import

if __name__ == "__main__":  # pragma: no cover
    # main()  # pylint: disable=no-value-for-parameter
    print("======================Configured Hosts======================")
    pprint.pprint(config.remotes)
