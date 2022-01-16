
hcp_data_dir='/home/data/nbc/external-datasets/hcp/niconn-hcp'

if [ ! -d $hcp_data_dir/code/err ]; then
  mkdir $hcp_data_dir/code/err
fi
if [ ! -d $hcp_data_dir/code/out ]; then
  mkdir $hcp_data_dir/code/out
fi

#maskdir=$hcp_data_dir/code/hoa_amygdala_right
maskdir=/home/data/abcd/abcd-hispanic-via/code/vmPFC_rsfc/rsfc_rois
masks=$(dir $maskdir)
output_dir=/home/data/abcd/abcd-hispanic-via/derivatives/hcp_rsfc
if [ ! -d $output_dir ]; then
  mkdir -p $output_dir
fi

for tmp_mask in $masks; do
  echo "running now"
  while [ $(squeue -u miriedel -o %j --noheader -r | sed -n '/_niconn-hcp_grpanalysis/p' | wc -l) -gt 59 ]; do
    sleep 5s
  done

  sbatch -J "$tmp_mask"_niconn-hcp_grpanalysis \
         -o $hcp_data_dir/code/out/"$tmp_mask"_niconn-hcp_grpanalysis \
         -e $hcp_data_dir/code/err/"$tmp_mask"_niconn-hcp_grpanalysis \
         -p investor \
         --account=iacc_nbc \
         --qos=pq_nbc \
         -c 8 \
         --wrap="python3 $hcp_data_dir/code/rs_grpanalysis-corr.py --rs_data_dir $hcp_data_dir/hcp-openaccess/HCP1200 --output_dir $output_dir --work_dir /scratch/nbc/miriedel/niconn-hcp --mask_fn $maskdir/$tmp_mask"
done
