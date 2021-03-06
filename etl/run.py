#!/usr/bin/env python


import sys

from etl import setup
from etl.calisphere_etl import CalisphereETLProcess
from etl.dpla_etl import DPLAETLProcess
from etl.pth_etl import PTHETLProcess
from etl.si_etl import SIETLProcess


# REVIEW: look into date issues:
#   - for calisphere, date is treated as a display date ('date') a sort date ('date_ss') and then sort_date_start and sort_date_end
#   - for dpla, date is treated as 'displaydate' and then 'begin' and 'end', and is sometimes not available
#   - for SI date is frequently more of a subject or topic, possibly with multiple values, and sometimes not available
#   - figure out how to deal with dates - separate search field and display field?

# REVIEW: TODO put internet archive into new ETL layout (first pass at least)


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

def run_cmd_line(args):

    format_ = "csv" # default output format.
    institutions = []

    # Parse command-line args.
    for idx, arg in enumerate(args):

        if arg.startswith("--format="):

            if len(arg) < 12:

                raise Exception(f"Invalid format: {arg}")

            pos = arg.find('=')
            format_ = arg[ pos + 1 : ]

        else:

            if arg not in INST_ETL_MAP:

                raise Exception(f"Invalid institution: {arg}")

            institutions.append(arg)

    if not institutions:

        raise Exception(f"Usage: run.py institution1 ... institutionN --format[=csv]")

    # Run the ETL.
    run_etl(institutions=institutions, format=format_)


if __name__ == "__main__":    # pragma: no cover

    run_cmd_line(sys.argv[ 1: ])
