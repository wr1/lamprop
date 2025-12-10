#!/usr/bin/env python3
"""Console CLI for lamprop."""
import sys

from loguru import logger
from rich.console import Console
from treeparse import argument, cli, command, option

from lamprop.io.parser import info, parse, warn
from lamprop.io.text import text_output

console = Console()

def process_files(files, *, eng, mat, fea):
    """Process the files and output results."""
    logger.add(sys.stderr, level="INFO")
    out = text_output
    for f in files:
        logger.info(f"processing file '{f}'")
        laminates = parse(f)
        if warn:
            console.print(f'[red]Warnings for "{f}":[/red]')
            for ln in warn:
                console.print(ln)
            console.print()
        if not laminates:
            console.print(f"No laminates found in '{f}'.")
            continue
        for curlam in laminates:
            for line in out(curlam, eng=eng, mat=mat, fea=fea):
                console.print(line)

def eng_callback(files):
    """Output engineering properties."""
    process_files(files, eng=True, mat=False, fea=False)

def mat_callback(files):
    """Output ABD matrix and stiffness tensor."""
    process_files(files, eng=False, mat=True, fea=False)

def fea_callback(files, output=None):
    """Output material data for FEA."""
    logger.add(sys.stderr, level="INFO")
    out = text_output
    all_lines = []
    for f in files:
        logger.info(f"processing file '{f}'")
        laminates = parse(f)
        if warn:
            if output:
                all_lines.extend([f'** Warnings for "{f}":'] + [f"** {w}" for w in warn] + ["**"])
            else:
                console.print(f'[red]Warnings for "{f}":[/red]')
                for ln in warn:
                    console.print(ln)
                console.print()
        if not laminates:
            if output:
                all_lines.append(f"** No laminates found in '{f}'.")
            else:
                console.print(f"No laminates found in '{f}'.")
            continue
        for curlam in laminates:
            lines = out(curlam, eng=False, mat=False, fea=True)
            all_lines.extend(lines)
    if output:
        from pathlib import Path
        Path(output).write_text("\n".join(all_lines) + "\n", encoding="utf-8")
    else:
        for line in all_lines:
            console.print(line)

def tex_callback(files):
    """Generate LaTeX output."""
    console.print("LaTeX output not implemented, falling back to text.")
    process_files(files, eng=True, mat=True, fea=True)

def info_callback(files):
    """Show information about source files."""
    logger.add(sys.stderr, level="INFO")
    for f in files:
        logger.info(f"processing file '{f}'")
        laminates = parse(f)
        if info and info:
            console.print(f'Information for "{f}":')
            for ln in info:
                console.print(ln)
            console.print()
        if warn:
            console.print(f'[red]Warnings for "{f}":[/red]')
            for ln in warn:
                console.print(ln)
            console.print()
        if not laminates:
            console.print(f"No laminates found in '{f}'.")

app = cli(
    name="lamprop",
    help="Calculate the elastic properties of a fibrous composite laminate. See the manual (lamprop-manual.pdf) for more in-depth information.",
    commands=[
        command(
            name="eng",
            help="Output only the engineering properties",
            callback=eng_callback,
            arguments=[
                argument(name="files", nargs="+", arg_type=str, help="one or more files to process")
            ],
        ),
        command(
            name="mat",
            help="Output only the ABD matrix and stiffness tensor",
            callback=mat_callback,
            arguments=[
                argument(name="files", nargs="+", arg_type=str, help="one or more files to process")
            ],
        ),
        command(
            name="fea",
            help="Output only material data for FEA",
            callback=fea_callback,
            arguments=[
                argument(name="files", nargs="+", arg_type=str, help="one or more files to process")
            ],
            options=[
                option(flags=["--output", "-o"], arg_type=str, help="output file for FEA data"),
            ],
        ),
        command(
            name="tex",
            help="Generate LaTeX output",
            callback=tex_callback,
            arguments=[
                argument(name="files", nargs="+", arg_type=str, help="one or more files to process")
            ],
        ),
        command(
            name="info",
            help="Show information about source files",
            callback=info_callback,
            arguments=[
                argument(name="files", nargs="+", arg_type=str, help="one or more files to process")
            ],
        ),
    ],
)

def main():
    """Entry point for lamprop console application."""
    app.run()
