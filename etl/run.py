#!/usr/bin/env python


import sys

import setup
from calisphere_etl import CalisphereETLProcess
from dpla_etl import DPLAETLProcess
from pth_etl import PTHETLProcess
from si_etl import SIETLProcess


# REVIEW: TODO clean up "list" values so that they are easier to read (put each on its own line)
# REVIEW: TODO check if date values can be converted accurately, and convert them to python date values ...
#   - for calisphere, date is treated as a display date ('date') a sort date ('date_ss') and then sort_date_start and sort_date_end
#   - for dplay, date is treated as 'displaydate' and then 'begin' and 'end', and is sometimes not available
#   - for PTH date is sometimes not more specific than year.
#   - for SI date is frequently more of a subject or topic, possibly with multiple values, and sometimes not available


# REVIEW: TODO look at how smithsonian metadata varies across collections within smithsonian
# REVIEW: TODO put internet archive into new ETL layout (first pass at least)

# REVIEW: TODO make sure keyword vs title search is consistent across institutions
# REVIEW: TODO figure out how to deal with dates - separate search field and display field?
# REVIEW: TODO come up with ability to pull entire dataset for institutions.


INST_ETL_MAP = {
    "cali": CalisphereETLProcess,
    "dpla": DPLAETLProcess,
    "pth": PTHETLProcess,
    "si": SIETLProcess,
}


def run_etl(institutions, format):

    etl_classes = [ INST_ETL_MAP[inst] for inst in institutions ]

    for etl_class in etl_classes:

        etl_process = etl_class(format=format)

        data = etl_process.extract()
        etl_process.transform(data=data)
        etl_process.load(data=data)


if __name__ == "__main__":

    format_ = "csv"
    institutions = []

    # Parse command-line args.
    for idx, arg in enumerate(sys.argv):

        if idx == 0:

            pass

        elif arg.startswith("--format="):

            if len(arg) < 12:

                raise Exception(msg=f"Invalid format: {arg}")

            pos = arg.find('=')
            format_ = arg[ pos + 1 : ]

        else:

            if arg not in INST_ETL_MAP:

                raise Exception(msg=f"Invalid institution: {arg}")

            institutions.append(arg)

    if not institutions:

        raise Exception(msg=f"Usage: run.py institution1 ... institutionN --format[=csv]")

    # Run the ETL.
    run_etl(institutions=institutions, format=format_)
