import sys
sys.path.append('/home/miriedel/niconn/')
from datasets.hcp1200 import hcp1200_download
import os
import os.path as op
import pandas as pd
from datasets.hcp1200 import download_ppt

hcp_data_dir = '/home/data/nbc/external-datasets/hcp/niconn-hcp/'

pids_df = pd.read_csv(op.join(hcp_data_dir, 'code', 'hcp1200_participants-150.tsv'), sep='\t')

hcp_data_dir = op.join(hcp_data_dir, 'hcp-openaccess', 'HCP1200')

download_ppt(hcp_data_dir=hcp_data_dir, pid=pids_df['participant_id'].tolist())
