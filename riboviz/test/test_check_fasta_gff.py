"""
:py:mod:`riboviz.check_fasta_gff` tests.
"""
import os
import tempfile
import pytest
import pandas as pd
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from riboviz import check_fasta_gff
from riboviz.test import data


TEST_FASTA_CHECK_FILE = os.path.join(os.path.dirname(data.__file__),
                                     "test_check_fasta_gff.fasta")
""" Test FASTA file in :py:mod:`riboviz.test.data`. """
TEST_GFF_CHECK_FILE = os.path.join(os.path.dirname(data.__file__),
                                   "test_check_fasta_gff.gff")
""" Test GFF file in :py:mod:`riboviz.test.data`. """
TEST_CHECK_GFF_ISSUES = [
    ("YAL004CNoIDNameAttr_mRNA", "YAL004CNoIDNameAttr_mRNA_CDS",
     check_fasta_gff.NO_ID_NAME, None),
    ("YAL005CNonUniqueID_mRNA", "YAL005_7CNonUniqueID_CDS",
     check_fasta_gff.DUPLICATE_FEATURE_ID, None),
    ("YAL006CNonUniqueID_mRNA", "YAL005_7CNonUniqueID_CDS",
     check_fasta_gff.DUPLICATE_FEATURE_ID, None),
    ("YAL007CNonUniqueID_mRNA", "YAL005_7CNonUniqueID_CDS",
     check_fasta_gff.DUPLICATE_FEATURE_ID, None),
    (check_fasta_gff.SEQUENCE_WILDCARD, "YAL005_7CNonUniqueID_CDS",
     check_fasta_gff.DUPLICATE_FEATURE_IDS, 3),
    ("YAL015CMultiCDS_mRNA", "",
     check_fasta_gff.MULTIPLE_CDS, 3),
]
"""
Expected GFF-specific issues (sequence ID, feature ID, issue type,
issue data) for GFF file (:py:const:`TEST_GFF_CHECK_FILE`) only.
"""
TEST_CHECK_FASTA_ISSUES = [
    ("YAL003CMissingSequence_mRNA", "",
     check_fasta_gff.SEQUENCE_NOT_IN_FASTA, None),
    ("YAL008CBadLengthNoStop_mRNA", "YAL008CBadLengthNoStop_CDS",
     check_fasta_gff.INCOMPLETE_FEATURE, None),
    ("YAL008CBadLengthNoStop_mRNA", "YAL008CBadLengthNoStop_CDS",
     check_fasta_gff.NO_STOP_CODON, None),
    ("YAL009CNoATGStart_mRNA", "YAL09CNoATGStart_CDS",
     check_fasta_gff.NO_ATG_START_CODON, None),
    ("YAL010CNoStop_mRNA", "YAL010CNoStop_CDS",
     check_fasta_gff.NO_STOP_CODON, None),
    ("YAL011CInternalStop_mRNA", "YAL011CInternalStop_CDS",
     check_fasta_gff.INTERNAL_STOP_CODON, None),
    ("YAL012CNoATGStartNoStop_mRNA", "YAL12CNoATGStartNoStop_CDS",
     check_fasta_gff.NO_ATG_START_CODON, None),
    ("YAL012CNoATGStartNoStop_mRNA", "YAL12CNoATGStartNoStop_CDS",
     check_fasta_gff.NO_STOP_CODON, None),
    ("YAL013CNoATGStartInternalStop_mRNA",
     "YAL13CNoATGStartInternalStop_CDS",
     check_fasta_gff.NO_ATG_START_CODON, None),
    ("YAL013CNoATGStartInternalStop_mRNA",
     "YAL13CNoATGStartInternalStop_CDS",
     check_fasta_gff.INTERNAL_STOP_CODON, None),
    ("YAL014CNoATGStartInternalStopNoStop_mRNA",
     "YAL14CNoATGStartInternalStopNoStop_CDS",
     check_fasta_gff.NO_ATG_START_CODON, None),
    ("YAL014CNoATGStartInternalStopNoStop_mRNA",
     "YAL14CNoATGStartInternalStopNoStop_CDS",
     check_fasta_gff.NO_STOP_CODON, None),
    ("YAL014CNoATGStartInternalStopNoStop_mRNA",
     "YAL14CNoATGStartInternalStopNoStop_CDS",
     check_fasta_gff.INTERNAL_STOP_CODON, None),
    ("YAL016CMissingGFF_mRNA", "",
     check_fasta_gff.SEQUENCE_NOT_IN_GFF, None),
    ("YAL017CMissingGFF_mRNA", "",
     check_fasta_gff.SEQUENCE_NOT_IN_GFF, None),
    ("YAL018CMissingSequence_mRNA", "",
     check_fasta_gff.SEQUENCE_NOT_IN_FASTA, None),
]
"""
Expected FASTA-specific issues (sequence ID, feature ID, issue type,
issue data) for checking FASTA file
(:py:const:`TEST_FASTA_CHECK_FILE`) and GFF file
(:py:const:`TEST_GFF_CHECK_FILE`).
"""
TEST_CHECK_ISSUES = TEST_CHECK_GFF_ISSUES + TEST_CHECK_FASTA_ISSUES
"""
All expected issues (sequence ID, feature ID, issue) for checking
FASTA file (:py:const:`TEST_FASTA_CHECK_FILE`) and GFF file
(:py:const:`TEST_GFF_CHECK_FILE`).
"""


@pytest.fixture(scope="function")
def tmp_file():
    """
    Create a temporary file.

    :return: path to temporary file
    :rtype: str or unicode
    """
    _, tmp_file = tempfile.mkstemp(prefix="tmp")
    yield tmp_file
    if os.path.exists(tmp_file):
        os.remove(tmp_file)


def test_get_fasta_sequence_ids(tmp_file):
    """
    Test :py:func:`riboviz.check_fasta_gff.get_fasta_sequence_ids`
    with a FASTA file and check that the expected sequence IDs
    are returned.
    :param tmp_file: Temporary file
    :type tmp_file: str or unicode
    """
    fasta_seq_ids = ["SeqID_{}".format(i) for i in range(0, 5)]
    with open(tmp_file, "w") as f:
        for seq_id in fasta_seq_ids:
            record = SeqRecord(Seq("GATTACCA"),
                               id=seq_id,
                               description="test")
            SeqIO.write(record, f, "fasta")
    seq_ids = check_fasta_gff.get_fasta_sequence_ids(tmp_file)
    assert set(fasta_seq_ids) == seq_ids, "Unexpected set of sequence IDs"


def test_get_fasta_sequence_ids_empty_fasta(tmp_file):
    """
    Test :py:func:`riboviz.check_fasta_gff.get_fasta_sequence_ids`
    with an empty FASTA file and check that an empty set is
    returned.
    """
    seq_ids = check_fasta_gff.get_fasta_sequence_ids(tmp_file)
    assert not seq_ids, "Expected empty set of sequence IDs"


def test_get_fasta_gff_cds_issues():
    """
    Test :py:func:`riboviz.check_fasta_gff.get_fasta_gff_cds_issues`
    with FASTA file (:py:const:`TEST_FASTA_CHECK_FILE`) and GFF file
    (:py:const:`TEST_GFF_CHECK_FILE`) and check all issues match
    expected issues in :py:const:`TEST_CHECK_ISSUES`).
    """
    issues = check_fasta_gff.get_fasta_gff_cds_issues(
        TEST_FASTA_CHECK_FILE,
        TEST_GFF_CHECK_FILE)
    for issue in issues:
        assert issue in TEST_CHECK_ISSUES


def test_get_fasta_gff_cds_issues_empty_fasta(tmp_file):
    """
    Test :py:func:`riboviz.check_fasta_gff.get_fasta_gff_cds_issues`
    with an empty FASTA file and GFF file
    (:py:const:`TEST_GFF_CHECK_FILE`)  and check all issues match
    expected issues in :py:const:`TEST_CHECK_GFF_ISSUES`).
    :param tmp_file: Temporary file
    :type tmp_file: str or unicode
    """
    issues = check_fasta_gff.get_fasta_gff_cds_issues(
        tmp_file,
        TEST_GFF_CHECK_FILE)
    for issue in issues:
        assert issue in TEST_CHECK_GFF_ISSUES


def check_fasta_gff_issues_df(issues, df):
    """
    Check contents of given list of tuples with issues held within
    a DataFrame output by
    :py:func:`riboviz.check_fasta_gff.fasta_gff_issues_to_df`.

    :param issues: List of issues for sequences and features.
    :type issues: list(tuple(str or unicode, str or unicode, \
    str or unicode))
    :param df: Pandas DataFrame
    :rtype: pandas.core.frame.DataFrame
    """
    num_rows, num_columns = df.shape
    assert num_columns == 4, "Unexpected number of columns"
    for column in [check_fasta_gff.SEQUENCE,
                   check_fasta_gff.FEATURE,
                   check_fasta_gff.ISSUE_TYPE,
                   check_fasta_gff.ISSUE_DATA]:
        assert column in list(df.columns),\
            "Missing column {}".format(column)
    assert num_rows == len(issues), \
        "Unexpected number of rows"
    for sequence, feature, issue_type, issue_data in issues:
        issue_df = df[(df[check_fasta_gff.SEQUENCE] == sequence) &
                      (df[check_fasta_gff.FEATURE] == feature) &
                      (df[check_fasta_gff.ISSUE_TYPE] == issue_type)]
        assert not issue_df.empty, \
            "Expected 1 matching row for {} {} {}".format(
                sequence, feature, issue_type)
        if issue_data is None:
            expected_data = ""
        else:
            expected_data = issue_data
        df_issue_data = issue_df.iloc[0][check_fasta_gff.ISSUE_DATA]
        assert df_issue_data == expected_data, \
            "Unexpected data ({}) for {} {} {}".format(
                df_issue_data, sequence, feature, issue_type)


def test_fasta_gff_issues_to_df():
    """
    Test :py:func:`riboviz.check_fasta_gff.fasta_gff_issues_to_df`
    with FASTA file (:py:const:`TEST_FASTA_CHECK_FILE`) and GFF file
    (:py:const:`TEST_GFF_CHECK_FILE`) and check all issues match
    expected issues in :py:const:`TEST_CHECK_ISSUES`).
    """
    df = check_fasta_gff.fasta_gff_issues_to_df(TEST_CHECK_ISSUES)
    df = df.fillna("")  # Force None to "" not "nan"
    check_fasta_gff_issues_df(TEST_CHECK_ISSUES, df)


def test_fasta_gff_issues_to_df_empty():
    """
    Test :py:func:`riboviz.check_fasta_gff.fasta_gff_issues_to_df`
    with no values produces an empty data frame.
    """
    df = check_fasta_gff.fasta_gff_issues_to_df([])
    check_fasta_gff_issues_df([], df)


def test_check_fasta_gff_empty_fasta(tmp_file):
    """
    Test :py:func:`riboviz.check_fasta_gff.check_fasta_gff` with an
    empty FASTA file and GFF file (:py:const:`TEST_GFF_CHECK_FILE`)
    and validate the TSV file output.

    :param tmp_file: Temporary file
    :type tmp_file: str or unicode
    """
    # Use tmp_file as both empty FASTA input file and TSV output
    # file
    check_fasta_gff.check_fasta_gff(tmp_file, TEST_GFF_CHECK_FILE, tmp_file)
    df = pd.read_csv(tmp_file, delimiter="\t", comment="#")
    df = df.fillna("")  # Force None to "" not "nan"
    check_fasta_gff_issues_df(TEST_CHECK_GFF_ISSUES, df)


def test_check_fasta_gff(tmp_file):
    """
    Test :py:func:`riboviz.check_fasta_gff.check_fasta_gff` with
    FASTA file (:py:const:`TEST_FASTA_CHECK_FILE`) and GFF file
    (:py:const:`TEST_GFF_CHECK_FILE`) and validate the TSV file
    output.

    :param tmp_file: Temporary file
    :type tmp_file: str or unicode
    """
    check_fasta_gff.check_fasta_gff(TEST_FASTA_CHECK_FILE,
                                    TEST_GFF_CHECK_FILE,
                                    tmp_file)
    df = pd.read_csv(tmp_file, delimiter="\t", comment="#")
    df = df.fillna("")  # Force None to "" not "nan"
    check_fasta_gff_issues_df(TEST_CHECK_ISSUES, df)


def test_check_fasta_gff_feature_format(tmp_file):
    """
    Test :py:func:`riboviz.check_fasta_gff.check_fasta_gff` with
    FASTA file (:py:const:`TEST_FASTA_CHECK_FILE`) and GFF file
    (:py:const:`TEST_GFF_CHECK_FILE`) and a custom feature name
    format and validate the TSV file output.

    :param tmp_file: Temporary file
    :type tmp_file: str or unicode
    """
    check_fasta_gff.check_fasta_gff(TEST_FASTA_CHECK_FILE,
                                    TEST_GFF_CHECK_FILE,
                                    tmp_file,
                                    feature_format="{}-Custom")
    df = pd.read_csv(tmp_file, delimiter="\t", comment="#")
    df = df.fillna("")  # Force None to "" not "nan"
    test_check_issues = TEST_CHECK_ISSUES.copy()
    # Delete the test entry that uses the default CDS_FEATURE_FORMAT.
    test_check_issues.pop(0)
    # Add the expected result for the custom entry.
    test_check_issues.insert(
        0, ("YAL004CNoIDNameAttr_mRNA", "YAL004CNoIDNameAttr_mRNA-Custom",
            check_fasta_gff.NO_ID_NAME, None))
    check_fasta_gff_issues_df(test_check_issues, df)