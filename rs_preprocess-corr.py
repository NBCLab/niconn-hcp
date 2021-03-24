import sys
sys.path.append('/home/miriedel/niconn')
from connectivity.rs_corr import rs_preprocess
from glob import glob
import argparse
import os
import os.path as op


def get_parser():
    parser = argparse.ArgumentParser(description='Preprocess rs data using nipype workflow')
    parser.add_argument('--rs_data_dir', required=True, dest='rs_data_dir')
    parser.add_argument('--work_dir', required=True, dest='work_dir')
    parser.add_argument('--participant_id', required=True, dest='ppt')
    return parser


def main(argv=None):

    args = get_parser().parse_args(argv)
    rs_data_dir = args.rs_data_dir
    work_dir = args.work_dir
    ppt = args.ppt

    nii_files = sorted(glob(op.join(rs_data_dir, ppt, 'MNINonLinear', 'Results', 'rfMRI_REST*', 'rfMRI_REST*_hp2000_clean.nii.gz')))
    nii_files = [x for x in nii_files if '7T' not in x]

    for nii_fn in nii_files:
        print(nii_fn)

        #check to see if smoothed data exists
        smooth_fn = op.join(rs_data_dir, 'derivatives', 'smoothed', ppt, '{0}_smooth.nii.gz'.format(op.basename(nii_fn).split('.')[0]))

        if not op.isfile(smooth_fn):

            tmp_output_dir = op.join(rs_data_dir, 'derivatives', 'smoothed', ppt)
            if not op.isdir(tmp_output_dir):
                os.makedirs(tmp_output_dir)
            nii_work_dir = op.join(work_dir, 'rsfc', ppt, op.basename(nii_fn).split('.')[0])
            rs_preprocess(nii_fn, 4, nii_work_dir, tmp_output_dir)


if __name__ == '__main__':
    main()
