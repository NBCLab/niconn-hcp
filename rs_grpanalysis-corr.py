import os
import os.path as op
import argparse
import sys
sys.path.append('/home/miriedel/niconn')
from connectivity.rs_corr import rs_grouplevel
from glob import glob
import nibabel as nib
import numpy as np

def get_parser():
    parser = argparse.ArgumentParser(description='Preprocess rs data using nipype workflow')
    parser.add_argument('--rs_data_dir', required=True, dest='rs_data_dir')
    parser.add_argument('--work_dir', required=True, dest='work_dir')
    parser.add_argument('--mask_fn', required=True, dest='mask')
    parser.add_argument('--output_dir', required=True, dest='output_dir')
    return parser


def main(argv=None):

    args = get_parser().parse_args(argv)
    rs_data_dir = args.rs_data_dir
    mask = op.basename(args.mask).strip('.nii.gz')

    work_dir = op.join(args.work_dir, 'rsfc', mask)
    output_dir = args.output_dir

    os.makedirs(work_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    z = sorted(glob(op.join(rs_data_dir, 'derivatives', '*', mask, 'z.nii.gz')))

    rs_grouplevel(z, mask, output_dir, work_dir)


if __name__ == '__main__':
    main()
