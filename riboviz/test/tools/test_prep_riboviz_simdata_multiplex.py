"""
riboviz.tools.prep_riboviz test suite to test adaptor trimming,
barcode and UMI extraction, demultpliexing and deduplication.

The test suite runs riboviz.tools.prep_riboviz using a copy of
"vignette/simdata_multiplex_config.yaml" and the simulated data in
"data/simdata/". It then validates the outputs of the adaptor
trimming, barcode and UMI extraction, demultiplexing and deduplication
steps against the expected outputs, also in "data/simdata/".

The simulated data in "data/simdata/" is expected to have been created
using riboviz.tools.create_fastq_simdata.
"""
import os
import pytest
import riboviz
import riboviz.test
from riboviz import demultiplex_fastq
from riboviz import fastq
from riboviz import params
from riboviz import utils
from riboviz import workflow_files
from riboviz.test.tools import configuration_module  # Test fixture
from riboviz.test.tools import run_prep_riboviz  # Test fixture
from riboviz.test.tools.test_prep_riboviz_simdata_umi \
    import check_umi_groups
from riboviz.test.tools.test_prep_riboviz_simdata_umi \
    import check_tpms_collated_tsv


TEST_CONFIG_FILE = riboviz.test.SIMDATA_MULTIPLEX_CONFIG
"""
YAML configuration used as a template configuration by these tests -
required by configuration test fixture
"""


@pytest.mark.usefixtures("run_prep_riboviz")
def test_adaptor_trimming(configuration_module):
    """
    Validate that adaptor trimming, performed by "cutadapt" produces
    the expected results.

    :param configuration_module: configuration and path to \
    configuration file (pytest fixture)
    :type configuration_module: tuple(dict, str or unicode)
    """
    config, _ = configuration_module
    expected_output = os.path.join(
        riboviz.test.SIMDATA_DIR,
        fastq.FASTQ_FORMAT.format("multiplex_umi_barcode"))
    actual_output = os.path.join(
        config[params.TMP_DIR],
        workflow_files.ADAPTER_TRIM_FQ_FORMAT.format(
            "multiplex_umi_barcode_adaptor"))
    fastq.equal_fastq(expected_output, actual_output)


@pytest.mark.usefixtures("run_prep_riboviz")
def test_barcode_umi_extract(configuration_module):
    """
    Validate that barcode and UMI extraction, performed by "umi_tools
    extract" produces the expected results.

    :param configuration_module: configuration and path to \
    configuration file (pytest fixture)
    :type configuration_module: tuple(dict, str or unicode)
    """
    config, _ = configuration_module
    expected_output = os.path.join(
        riboviz.test.SIMDATA_DIR,
        fastq.FASTQ_FORMAT.format("multiplex"))
    actual_output = os.path.join(
        config[params.TMP_DIR],
        workflow_files.UMI_EXTRACT_FQ_FORMAT.format(
            "multiplex_umi_barcode_adaptor"))
    fastq.equal_fastq(expected_output, actual_output)


@pytest.mark.usefixtures("run_prep_riboviz")
def test_deplex_num_reads(configuration_module):
    """
    Validate that "num_reads.tsv", produced by
    riboviz.demultiplex_fastq has the expected content.

    :param configuration_module: configuration and path to \
    configuration file (pytest fixture)
    :type configuration_module: tuple(dict, str or unicode)
    """
    config, _ = configuration_module
    actual_dir = os.path.join(
        config[params.TMP_DIR],
        workflow_files.DEPLEX_DIR_FORMAT.format(
            "multiplex_umi_barcode_adaptor"))
    actual_output = os.path.join(actual_dir,
                                 demultiplex_fastq.NUM_READS_FILE)
    expected_output = os.path.join(
        riboviz.test.SIMDATA_DIR,
        "deplex",
        demultiplex_fastq.NUM_READS_FILE)
    utils.equal_tsv(expected_output, actual_output)


@pytest.mark.parametrize(
    "tag", ["Tag0", "Tag1", "Tag2", "Unassigned"])
@pytest.mark.usefixtures("run_prep_riboviz")
def test_deplex_reads(configuration_module, tag):
    """
    Validate that ".fastq", produced by
    riboviz.demultiplex_fastq have the expected content.

    :param configuration_module: configuration and path to \
    configuration file (pytest fixture)
    :type configuration_module: tuple(dict, str or unicode)
    :param tag: FASTQ fie name tag
    :type tag: str or unicode
    """
    # Actual data has a .fq extension.
    actual_file_name = fastq.FQ_FORMAT.format(tag)
    # Simulated data has a .fastq extension.
    expected_file_name = fastq.FASTQ_FORMAT.format(tag)
    config, _ = configuration_module
    actual_dir = os.path.join(
        config[params.TMP_DIR],
        workflow_files.DEPLEX_DIR_FORMAT.format(
            "multiplex_umi_barcode_adaptor"))
    actual_output = os.path.join(actual_dir, actual_file_name)
    expected_output = os.path.join(
        riboviz.test.SIMDATA_DIR, "deplex", expected_file_name)
    fastq.equal_fastq(expected_output, actual_output)


@pytest.mark.parametrize("sample_id", ["Tag0", "Tag1", "Tag2"])
@pytest.mark.usefixtures("run_prep_riboviz")
def test_deplex_umi_groups(configuration_module, sample_id):
    """
    Validate the information on UMI groups post-"umi_tools extract",
    for each demultiplexed file, by parsing the ".tsv" file output by
    "umi_tools group".

    :param configuration_module: configuration and path to \
    configuration file (pytest fixture)
    :type configuration_module: tuple(dict, str or unicode)
    :param sample_id: sample ID for demultiplexed reads
    :type sample_id: str or unicode
    """
    config, _ = configuration_module
    check_umi_groups(config, sample_id, 5)


@pytest.mark.parametrize("sample_id", ["Tag0", "Tag1", "Tag2"])
@pytest.mark.usefixtures("run_prep_riboviz")
def test_deplex_tpms_collated_tsv(configuration_module, sample_id):
    """
    Validate the "TPMs_collated.tsv" file produced by the workflow.

    :param configuration_module: configuration and path to \
    configuration file (pytest fixture)
    :type configuration_module: tuple(dict, str or unicode)
    :param sample_id: sample ID for demultiplexed reads
    :type sample_id: str or unicode
    """
    config, _ = configuration_module
    check_tpms_collated_tsv(config, sample_id, 4)
