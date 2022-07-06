"""Unit tests for the MK configuration."""
import shutil

from pds.naif_pds4_bundler.__main__ import main


def test_insight_mk_error_extra_pattern(self):
    """Test for meta-kernel configuration loading error cases.

    Test is successful if it signals this run time error::

        The MK patterns insight_$YEAR_v$VERSION.tm do not correspond to the present MKs.
    """
    config = "../config/insight.xml"
    updated_config = "working/insight.xml"
    plan = "../data/insight_release_08.plan"

    with open(config, "r") as c:
        with open(updated_config, "w") as n:
            for line in c:
                if '<mk name="insight_v$VERSION.tm">' in line:
                    n.write('<mk name="insight_$YEAR_v$VERSION.tm">\n')
                else:
                    n.write(line)

    with self.assertRaises(RuntimeError):
        main(updated_config, plan, faucet="staging", silent=self.silent, log=True)


def test_insight_mk_error_wrong_name(self):
    """Test incorrect MK name in configuration.

    Test is successful if it signals this run time error::

        RuntimeError: The meta-kernel pattern VERSION is not provided.
    """
    config = "../config/insight.xml"
    updated_config = "working/insight.xml"
    plan = "../data/insight_release_08.plan"

    with open(config, "r") as c:
        with open(updated_config, "w") as n:
            for line in c:
                if '<mk name="insight_v$VERSION.tm">' in line:
                    n.write('        <mk name="insight.tm">\n')
                else:
                    n.write(line)

    with self.assertRaises(RuntimeError):
        main(updated_config, plan, self.faucet, silent=self.silent, log=True)


def test_insight_mk_double_keyword_in_pattern(self):
    """Test double keyword MK pattern in configuration."""
    config = "../config/insight.xml"
    updated_config = "working/insight.xml"
    plan = "../data/insight_release_08.plan"
    updated_plan = "working/insight_release_08.plan"

    with open(plan, "r") as c:
        with open(updated_plan, "w") as n:
            for line in c:
                if "insight_v08.tm" in line:
                    n.write("insight_2021_v08.tm \\\n")

    with open(config, "r") as c:
        with open(updated_config, "w") as n:
            for line in c:
                if '<mk name="insight_v$VERSION.tm">' in line:
                    n.write('           <mk name="insight_$YEAR_v$VERSION.tm">\n')
                elif '<kernel pattern="insight_v[0-9][0-9].tm">' in line:
                    n.write(
                        '<kernel pattern="insight_[0-9][0-9][0-9][0-9]_v[0-9][0-9].tm">'
                    )
                elif '<pattern length="2">VERSION</pattern>' in line:
                    n.write(
                        '                   <pattern length="2">VERSION</pattern>\n'
                    )
                    n.write('                   <pattern length="4">YEAR</pattern>\n')
                else:
                    n.write(line)

    main(updated_config, updated_plan, self.faucet, silent=self.silent, log=True)


def test_insight_mk_double_keyword_in_pattern_no_gen(self):
    """Test double keyword MK pattern in configuration with no generation.

    Note that given that the MK pattern has multiple keywords a MK will not
    be generated by default if not provided in the release plan.
    """
    config = "../config/insight.xml"
    updated_config = "working/insight.xml"
    plan = "../data/insight_release_08.plan"

    with open(config, "r") as c:
        with open(updated_config, "w") as n:
            for line in c:
                if '<mk name="insight_v$VERSION.tm">' in line:
                    n.write('           <mk name="insight_$YEAR_v$VERSION.tm">\n')
                elif '<pattern length="2">VERSION</pattern>' in line:
                    n.write(
                        '                   <pattern length="2">VERSION</pattern>\n'
                    )
                    n.write('                   <pattern length="4">YEAR</pattern>\n')
                else:
                    n.write(line)

    main(updated_config, plan, self.faucet, silent=self.silent, log=True)


def zz_test_orex_mk_multiple_mks(self):
    """Test MK configuration section with multiple MKs to generate."""
    config = "../config/orex.xml"
    plan = "../data/orex_release_10.plan"

    main(config, plan, self.faucet, silent=self.silent, log=True)


def zz_test_orex_mk_multiple_mks_version_three_digits(self):
    """Test MKs with 3 digits in the version."""
    config = "../config/orex.xml"
    updated_config = "working/orex.xml"
    plan = "working/orex_release_10.plan"

    with open(config, "r") as c:
        with open(updated_config, "w") as n:
            for line in c:
                if '<pattern length="2">VERSION</pattern>' in line:
                    n.write('<pattern length="3">VERSION</pattern>\n')
                elif "v[0-9]{2}.tm" in line:
                    n.write(line.replace("v[0-9]{2}.tm", "v[0-9]{3}.tm"))
                elif "<mk_inputs>" in line:
                    n.write("<!-- <mk_inputs>\n")
                elif "</mk_inputs>" in line:
                    n.write("</mk_inputs> -->\n")
                elif "_v[0-9][0-9].tm" in line:
                    n.write(line.replace("_v[0-9][0-9].tm", "_v[0-9][0-9][0-9].tm"))
                else:
                    n.write(line)

    shutil.copy2("kernels/mk/orx_2020_v05.tm", "kernels/mk/orx_2020_v003.tm")
    shutil.copy2("kernels/mk/orx_2020_v05.tm", "kernels/mk/orx_noola_2020_v003.tm")

    with open(plan, "w") as c:
        c.write("orx_2020_v003.tm\n")
        c.write("orx_noola_2020_v003.tm\n")

    main(updated_config, plan, faucet="staging", silent=self.silent, log=True)


def zz_test_orex_mk_multiple_mks_version_one_digit(self):
    """Test MKs with 1 digits in the version."""
    config = "../config/orex.xml"
    updated_config = "working/orex.xml"
    plan = "working/orex_release_10.plan"

    with open(config, "r") as c:
        with open(updated_config, "w") as n:
            for line in c:
                if '<pattern length="2">VERSION</pattern>' in line:
                    n.write('<pattern length="1">VERSION</pattern>\n')
                elif "v[0-9]{2}.tm" in line:
                    n.write(line.replace("v[0-9]{2}.tm", "v[0-9].tm"))
                elif "<mk_inputs>" in line:
                    n.write("<!-- <mk_inputs>\n")
                elif "</mk_inputs>" in line:
                    n.write("</mk_inputs> -->\n")
                elif "_v[0-9][0-9].tm" in line:
                    n.write(line.replace("_v[0-9][0-9].tm", "_v[0-9].tm"))
                else:
                    n.write(line)

    shutil.copy2("kernels/mk/orx_2020_v05.tm", "kernels/mk/orx_2020_v3.tm")
    shutil.copy2("kernels/mk/orx_2020_v05.tm", "kernels/mk/orx_noola_2020_v3.tm")

    with open(plan, "w") as c:
        c.write("orx_2020_v3.tm\n")
        c.write("orx_noola_2020_v3.tm\n")

    main(updated_config, plan, faucet="staging", silent=self.silent, log=True)
