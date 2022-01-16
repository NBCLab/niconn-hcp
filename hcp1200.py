import os
import os.path as op


def generate_random_pid(hcp_data_dir=None, n_pid=150):

    import random

    all_pid = os.listdir(op.join(hcp_data_dir))
    rand_pid = sorted(random.sample(all_pid, n_pid))
    return rand_pid


def download_ppt(hcp_data_dir=None, pid=None):

    import boto3
    import botocore

    boto3.setup_default_session(profile_name='HCP')
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('hcp-openaccess')

    for tmp_pid in pid:
        print(tmp_pid)
        s3_keys = bucket.objects.filter(Prefix='HCP_1200/{}/MNINonLinear/Results/rfMRI'.format(str(tmp_pid)))
        s3_keylist = [key.key for key in s3_keys]

        rsfmri_clean = [i for i in s3_keylist if i.endswith(('_hp2000_clean.nii.gz'))]
        rsfmri_clean = [i for i in rsfmri_clean if '7T' not in i]

        for tmp_run in rsfmri_clean:
            run_dir = tmp_run.split('/')[-2]
            os.makedirs(op.join(hcp_data_dir, str(tmp_pid), run_dir), exist_ok=True)

            rsfmri_download_file = op.join(hcp_data_dir, str(tmp_pid), run_dir, op.basename(tmp_run))
            with open(rsfmri_download_file, 'wb') as f:
                bucket.download_file(tmp_run, rsfmri_download_file)

            for mask in ['CSF', 'WM']:
                tmp_run_mask = tmp_run.replace('_hp2000_clean.nii.gz', '_{}.txt'.format(mask))
                mask_download_file = op.join(hcp_data_dir, str(tmp_pid), run_dir, op.basename(tmp_run_mask))
                with open(mask_download_file, 'wb') as f:
                    bucket.download_file(tmp_run_mask, mask_download_file)
