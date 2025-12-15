#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Written by Alan Viars

import sys
import json
from luhn import verify

LUHN_PREFIX = "80840"


def verify_npi(number):
    result = {"valid": False, "number": number}
    prefixed_number = "%s%s" % (LUHN_PREFIX, number)
    
    try:
        int(prefixed_number)
    except ValueError:
        error = "NPI must be numeric."
        result["error"] = error
        return result
    
    is_valid_npi =  verify(prefixed_number)
    if is_valid_npi:
        result["valid"] = True
    else:
        result["error"] = "Invalid NPI number"
    return result


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage:")
        print("vnpi.py [NPI]")
        print("Example:")
        print("vnpi.py ")
        sys.exit(1)

    # Get the file from the command line
    result = verify_npi(sys.argv[1])
    print(json.dumps(result, indent=4))