import re


def slugify(value):
    slugified_value =\
        str(value)\
            .lower()\
            .strip()\
            .replace(' ', '-')\
            .replace('&', '-and-')\

    slugified_value = re.sub(r"[^\w\-]+", "", slugified_value)
    slugified_value = re.sub(r"--+", "-", slugified_value)
    return slugified_value
