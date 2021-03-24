import os
import os.path as op
import sys
sys.path.append('/home/miriedel/niconn')
from connectivity.rs_corr import rs_secondlevel
import argparse
import nibabel as nib
import numpy as np
from glob import glob


def get_parser():
    parser = argparse.ArgumentParser(description='Preprocess rs data using nipype workflow')
    parser.add_argument('--rs_data_dir', required=True, dest='rs_data_dir')
    parser.add_argument('--work_dir', required=True, dest='work_dir')
    parser.add_argument('--participant_id', required=True, dest='ppt')
    parser.add_argument('--roi_dir', required=True, dest='roi_dir')
    return parser

def main(argv=None):

    args = get_parser().parse_args(argv)
    rs_data_dir = args.rs_data_dir
    work_dir = args.work_dir
    roi_dir = args.roi_dir
    ppt = args.ppt

    rois = os.listdir(roi_dir)

    nii_files = sorted(glob(op.join(rs_data_dir, 'hcp-openaccess', 'HCP1200', ppt, 'MNINonLinear', 'Results', 'rfMRI_REST*', 'rfMRI_REST*_hp2000_clean.nii.gz')))
    nii_files = [x for x in nii_files if '7T' not in x]

    for nii_fn in nii_files:
        smooth_fn = op.join(rs_data_dir, 'hcp-openaccess', 'HCP1200', 'derivatives', 'smoothed', ppt, '{0}_smooth.nii.gz'.format(op.basename(nii_fn).split('.')[0]))

        mask_fn = "_".join(op.basename(smooth_fn).split('.')[0].split('_')[:-1])

        brainmask = nib.load(op.join(op.dirname(smooth_fn), '{prefix}_mask.nii.gz'.format(prefix=mask_fn)))
        brainmask_inds = np.nonzero(brainmask.get_fdata())

        tmpimg = nib.load(smooth_fn)
        tmpimg_data_array = tmpimg.get_fdata()[brainmask_inds]

        colsum_tmpimg_data_array = np.sum(tmpimg_data_array, axis=1)
        colsum_tmpimg_data_array_square = np.sum(np.square(tmpimg_data_array), axis=1)
        square_colsum_tmpimg_data_array = np.square(colsum_tmpimg_data_array)

        for i, tmproi in enumerate(rois):
            tmp_output_dir = op.join(rs_data_dir, 'hcp-openaccess', 'HCP1200', 'derivatives', ppt, op.basename(nii_fn).split('.')[0], tmproi.strip('.nii.gz'))

            if not op.isfile(op.join(tmp_output_dir, 'r.nii.gz')):

                os.makedirs(tmp_output_dir, exist_ok=True)

                tmproiimg = nib.load(op.join(roi_dir, tmproi))
                tmproiimg_inds = np.nonzero(tmproiimg.get_fdata())

                shared_inds_locs = [np.where(np.all(np.transpose(brainmask_inds) == x, axis=1))[0] for x in np.transpose(tmproiimg_inds)]
                shared_inds_locs = [loc for tup in shared_inds_locs for loc in tup]

                mean_ts = np.mean(tmpimg_data_array[shared_inds_locs,:], axis=0)

                corrdata = np.zeros(brainmask.shape)

                colsum_mean_ts = np.sum(mean_ts)
                colsum_mean_ts_square = np.sum(np.square(mean_ts))
                numerator = len(mean_ts)*np.sum(mean_ts * tmpimg_data_array, axis=1) - (colsum_mean_ts * colsum_tmpimg_data_array)
                denom = np.sqrt((len(mean_ts)*colsum_mean_ts_square - np.square(colsum_mean_ts)) * (len(mean_ts)*colsum_tmpimg_data_array_square - square_colsum_tmpimg_data_array))
                corrcoef = numerator/denom

                corrdata[brainmask_inds] = corrcoef

                corrimg = nib.Nifti1Image(corrdata, brainmask.affine)
                nib.save(corrimg, op.join(tmp_output_dir, 'r.nii.gz'))

    for tmproi in rois:

        r = sorted(glob(op.join(rs_data_dir, 'hcp-openaccess', 'HCP1200', 'derivatives', ppt, '*', tmproi.strip('.nii.gz'), 'r.nii.gz')))
        rcomplete = []
        for tmp_r in r:
            tmpimg = nib.load(tmp_r)
            if np.max(tmpimg.get_fdata()) > 0:
                rcomplete.append(tmp_r)
        if len(rcomplete) > 0:
            output_dir = op.join(rs_data_dir, 'hcp-openaccess', 'HCP1200', 'derivatives', ppt, tmproi.strip('.nii.gz'))
            os.makedirs(output_dir, exist_ok=True)
            img = np.zeros((np.prod(nib.load(rcomplete[0]).shape), len(rcomplete)))
            for i, rimg in enumerate(rcomplete):
                tmpimg = nib.load(rimg).get_fdata()
                img[:,i] = tmpimg.flatten()
            imgmin = np.abs(img).min(axis=1)
            imginds = np.nonzero(imgmin)[0]
            imgmean = np.mean(img[imginds,:], axis=1)
            imgmean[imgmean == 1] = 1 - np.finfo(float).eps
            imgout = np.zeros(nib.load(rcomplete[0]).shape)
            imgout[np.unravel_index(imginds, nib.load(rcomplete[0]).shape)] = np.arctanh(imgmean)
            nib.save(nib.Nifti1Image(imgout, nib.load(rcomplete[0]).affine), op.join(output_dir, 'z.nii.gz'))


if __name__ == '__main__':
    main()
