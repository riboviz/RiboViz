#!/usr/bin/env python
"""
Subsample an input FASTQ (or other sequencing) file, to produce a
smaller file whose reads are randomly sampled from of the input with a
fixed probability.

Usage::

    python -m riboviz.tools.subsample_bioseqfile [-h]
        -i seqfilein -o seqfileout
        [-t FILE_TYPE] [-p PROB] [-f overwrite] [-v verbose]

    -h, --help                          show this help message and exit
    -i seqfilein, --input seqfilein     SeqIO file input
    -o seqfileout, --output seqfileout  SeqIO file output
    -t FILE_TYPE, --type FILE_TYPE      SeqIO file type (default 'fastq')
    -p PROB, --probability PROB         proportion to sample (default 0.01)
    -f overwrite, --overwrite           overwrite output if file exists
                                        (default False)
    -v, --verbose                       print progress statements

Examples::

    python -m riboviz.tools.subsample_bioseqfile
        -i vignette/input/SRR1042855_s1mi.fastq.gz
        -o vignette/tmp/subsamplefile.fastq.gz
        -p 0.001

    python -m riboviz.tools.subsample_bioseqfile
        -i vignette/input/SRR1042855_s1mi.fastq
        -o vignette/tmp/SRR1042855_s10.fastq.gz
        -t fastq
        -p 0.00001

See :py:func:`riboviz.subsample_bioseqfile.subsample_bioseqfile`.
"""
import argparse
import os
from riboviz import subsample_bioseqfile
from riboviz import provenance


def parse_command_line_options():
    """
    Parse command-line options.

    :returns: command-line options
    :rtype: argparse.Namespace
    """
    parser = argparse.ArgumentParser(
        description="Randomly subsample sequencing file with probability -p")
    parser.add_argument("-i",
                        "--seqfilein",
                        dest="seqfilein",
                        required=True,
                        help="SeqIO file input")
    parser.add_argument("-o",
                        "--seqfileout",
                        dest="seqfileout",
                        required=True,
                        help="SeqIO file output")
    parser.add_argument("-t",
                        "--type",
                        dest="file_type",
                        default="fastq",
                        help="SeqIO file type (default 'fastq')")
    parser.add_argument("-p",
                        "--probability",
                        dest="prob",
                        type=float,
                        default=0.01,
                        help="proportion to sample (default 0.01)")
    parser.add_argument("-f",
                        "--overwrite",
                        dest="overwrite",
                        default=False,
                        help="forces overwrite of output file if it exists")
    parser.add_argument("-v",
                        "--verbose",
                        dest="verbose",
                        action="store_true",
                        help="print progress statements")
    options = parser.parse_args()
    return options

    # files exist, overwrite output?
    if os.path.exists(options.seqfileout) and not options.overwrite:
        raise ValueError(
            "output file {} already exists, use '-overwrite' to replace"
            .format(options.seqfileout))
    if not os.path.exists(options.seqfilein):
        raise ValueError(
            "input file {} doesn't exist".format(options.seqfilein))


def invoke_subsample_bioseqfile():
    """
    Parse command-line options then invoke
    See :py:func:`riboviz.subsample_bioseqfile.subsample_bioseqfile`
    for information ...
    """
    print((provenance.write_provenance_to_str(__file__)))
    options = parse_command_line_options()
    seqfilein = options.seqfilein
    seqfileout = options.seqfileout
    file_type = options.file_type
    prob = options.prob
    overwrite = options.overwrite
    verbose = options.verbose
    subsample_bioseqfile.subsample_bioseqfile(seqfilein,
                                              seqfileout,
                                              file_type,
                                              prob,
                                              overwrite,
                                              verbose)


if __name__ == "__main__":
    invoke_subsample_bioseqfile()
