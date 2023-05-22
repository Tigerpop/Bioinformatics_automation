import argparse
from dataclasses import dataclass
import sys
import logging
import subprocess

logging.basicConfig(level=logging.DEBUG)

DEBUG_MODE = False


@dataclass
class FParser:
    args: argparse.Namespace = None
    parser: argparse.ArgumentParser = None

    def __post_init__(self):
        logging.debug("post init")
        self.parser = argparse.ArgumentParser(add_help=False)
        self.parser.add_argument("--gene", type=str, metavar="GENE_PANEL", nargs=1, choices=["Q120T","Q120B","BC17B", "BC17T","BCP650","NBC650"],
                                 help="Chooice Gene Panel,Only: Q120B,Q120T,BC17B,BC17T,BCP650,NBC650")
        self.parser.add_argument("--tool", type=str, metavar="TOOL_NAME", nargs=1,
                                 choices=["msisensor-pro", "msisensor2"],
                                 help="Chooice Annalyze Tool,Only msisensor-pro,msisensor2")
        self.parser.add_argument("other_args", nargs="*", help="Other Args")
        logging.debug(self.parser)

    def run(self, args):
        args = self.parser.parse_args(args)


class MsiPro:
    def __init__(self):
        if DEBUG_MODE:
            self.base_path = "/home/stamp/myFirm/myWorkSpace/msisensor-pro"
        else:
            self.base_path = "/opt/msisensor-pro"

    @classmethod
    def execute_cmd(cls, cmd_str):
        p = subprocess.Popen(
            cmd_str,
            shell=True,
            stdout=subprocess.PIPE
        )
        try:
            while line := iter(p.stdout.readline, b'').__next__():
                logging.debug(line.decode("utf-8").replace("\n", ""))
        except StopIteration:
            print("Ok")

    def scan(self, l):
        ref_gene_path = l[0]
        target_msi_list_path = l[1]
        cmd_str = f"{self.base_path}/msisensor-pro scan -d {ref_gene_path} -o {target_msi_list_path}"
        logging.debug(f"cmd_str_scan:{cmd_str}")
        self.execute_cmd(cmd_str)

    def baseline(self, l):
        ref_gene_path=l[0]
        msi_configure_path=l[1]
        baseline_dir=l[2]
        cmd_str = f"{self.base_path}/msisensor-pro baseline -d {ref_gene_path} -i {msi_configure_path} -o {baseline_dir}"
        logging.debug(f"cmd_str_baseline:{cmd_str}")
        self.execute_cmd(cmd_str)

    def pro(self,l):
        baseline_file_path=l[0]
        sample_bam_file_path=l[1]
        result_file_path=l[2]
        cmd_str = f"{self.base_path}/msisensor-pro pro -d {baseline_file_path} -t {sample_bam_file_path} -o {result_file_path}"
        logging.debug(f"cmd_str_pro:{cmd_str}")
        self.execute_cmd(cmd_str)


@dataclass
class MsiProParser:
    args = None
    fparser = FParser()
    tool = MsiPro()
    parser = None

    def __post_init__(self):
        self.parser = argparse.ArgumentParser(
            parents=[self.fparser.parser],
            epilog="Example1:\t<<\tpython --tool msisensor-pro --gene Q120 baselines/Q120/Q120.msi.baseline result/Test/Test3\t>>\t\r\n"
                   "Example2:\t<<\tpython --tool msisensor-pro --scan hg19.fasta msi.hg19.list\t>>\r\n"
                   "Example3:\t<<\tpython --tool msisensor-pro --baseline msi.hg19.list msi_Q120.configure.txt baslines/Q120\t>>\t\r\n"
                   "Example4:\t<<\tpython --tool msisensor-pro --pro baselines/Q120/Q120.msi.list result/Test/Test4\t>>\t\r\n"

        )
        # Base Cmdline
        self.parser.add_argument("--scan", type=str, metavar=("IN_REF_FASTA", "OUT_MSI_LIST"), nargs=2,
                                 help="Scan Reference Gene Group And Output Msi List")
        self.parser.add_argument("--baseline", type=str,
                                 metavar=("IN_REF_FASTA", "IN_MSI_CONFIGURE", "OUT_BASELINE_DIR"),
                                 nargs=3, help="Construct MSS DATA BaseLine")
        self.parser.add_argument("--pro", type=str,
                                 metavar=("IN_BASELINE_FILE", "IN_SAMPLE_BAM_FILE", "OUT_RESULT_FILE"), nargs=3,
                                 help="Detect MSI", )

    def run(self, args):
        self.args = self.parser.parse_args(args)

        logging.debug(f"msipro_args:{self.args}")
        # Judegement gene panel is None
        if self.args.gene is None:
            logging.debug(f"gene:{self.args.gene}")
            logging.debug(f"arg_scan:{getattr(self.args, 'scan')}")

            map(
                lambda x: (
                    logging.debug(f"args_scan:{getattr(self.args, x)}"),
                    getattr(self.tool, x)(getattr(self.args, x))

                ),
                # Add Args
                [s for s in ["scan", "baseline", "pro"] if not getattr(self.args, s,) is None]
            )

        else:
            # Excute a Group Action
            self.tool.pro(
                [f"{self.tool.base_path}/baselines/{self.args.gene[0]}/{self.args.gene[0]}.msi.baseline",
                f"{self.args.other_args[0]}",
                f"{self.args.other_args[1]}"]
            )


class Msi2:
    pass


class Msi2Parser:
    pass


if __name__ == '__main__':
    logging.debug("Start...")
    logging.debug(f"args:{sys.argv[1:]}")
    tool_parser = argparse.ArgumentParser(parents=[FParser().parser])
    # Please Specify tool arg For the First Arg
    # switch
    # Add tool
    {
        "msisensor-pro": lambda: (
            logging.debug("msisensor-pro"),
            msi_detect := MsiProParser(),
            msi_detect.run(sys.argv[1:])
        ),
        "msisensor2": lambda: (
            logging.debug("None,Please Wait Future Version !")
        )
    }[tool_parser.parse_args(sys.argv[1:3]).tool[0]]()
