# -*- coding: utf-8 -*-
import re


def getnum(val):
    matches = re.findall(r"[-+]?\d*\.\d+|\d+]", val)
    if matches:
        return float(matches[0])
    return None


if __name__ == "__main__":
    f = getnum("> -0.24")
    print(f)
