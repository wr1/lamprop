"""Console CLI for lamprop."""
import argparse
import logging
import os
import sys
from ..io.parser import parse, info, warn
from ..io.text import text_output

def main():
    """Entry point for lamprop console application."""
    doc = (
        "Calculate the elastic properties of a fibrous composite laminate. "
        "See the manual (lamprop-manual.pdf) for more in-depth information."
    )
    opts = argparse.ArgumentParser(prog="lamprop", description=doc)
    group = opts.add_mutually_exclusive_group()
    group.add_argument(
        "-i",
        "--info",
        action="store_true",
        help="show information about source file (the default is not to)",
    )
    group.add_argument(
        "-l",
        "--latex",
        action="store_true",
        help="generate LaTeX output (the default is plain text)",
    )
    group.add_argument("-H", "--html", action="store_true", help="generate HTML output")
    opts.add_argument(
        "-e",
        "--eng",
        action="store_true",
        help="output only the engineering properties",
    )
    opts.add_argument(
        "-m",
        "--mat",
        action="store_true",
        help="output only the ABD matrix and stiffness tensor",
    )
    opts.add_argument(
        "-f", "--fea", action="store_true", help="output only material data for FEA"
    )
    group = opts.add_mutually_exclusive_group()
    group.add_argument(
        "-L", "--license", action="store_true", help="print the license"
    )
    group.add_argument("-v", "--version", action="version", version=__import__('lamprop').__version__)
    opts.add_argument(
        "--log",
        default="warning",
        choices=["debug", "info", "warning", "error"],
        help="logging level (defaults to 'warning')",
    )
    opts.add_argument(
        "files", metavar="file", nargs="*", help="one or more files to process"
    )
    args = opts.parse_args(sys.argv[1:])
    logging.basicConfig(
        level=getattr(logging, args.log.upper(), None),
        format="%(levelname)s: %(message)s",
    )
    del opts, group
    if args.mat is False and args.eng is False and args.fea is False:
        args.eng = True
        args.mat = True
        args.fea = True
    if len(args.files) == 0:
        sys.exit(1)
    out = text_output
    if args.latex:
        # Since we removed latex, fall back to text
        out = text_output
    elif args.html:
        # Since we removed html, fall back to text
        out = text_output
    if os.name == "nt":
        sys.stdout.reconfigure(encoding="utf-8")
    for f in args.files:
        logging.info("processing file '{}'".format(f))
        laminates = parse(f)
        if args.info and info:
            print(f'Information for "{f}":')
            for ln in info:
                print(ln)
            print()
        if warn:
            print(f'Warnings for "{f}":')
            for ln in warn:
                print(ln)
            print()
        for curlam in laminates:
            print(*out(curlam, args.eng, args.mat, args.fea), sep="\n")
