
hcp_data_dir='/home/data/nbc/external-datasets/hcp/niconn-hcp/'

if [ ! -d $hcp_data_dir/code/err ]; then
  mkdir $hcp_data_dir/code/err
fi
if [ ! -d $hcp_data_dir/code/out ]; then
  mkdir $hcp_data_dir/code/out
fi

count=0
subs=
while read line; do
  if [ $count -gt 0 ]; then
    subs+="$line "
  fi
  count=$((count+1))
done < $hcp_data_dir/code/hcp1200_participants-150.tsv

for sub in $subs; do
  echo $sub
  sbatch -J "$sub"_niconn-hcp_preprocess \
         -o $hcp_data_dir/code/out/"$sub"_niconn-hcp_preprocess \
         -e $hcp_data_dir/code/err/"$sub"_niconn-hcp_preprocess \
         -p IB_44C_512G \
         --account=iacc_nbc \
         --qos=pq_nbc \
         -n 2 \
         --wrap="python3 $hcp_data_dir/code/rs_preprocess-corr.py --rs_data_dir $hcp_data_dir/hcp-openaccess/HCP1200 --work_dir /scratch/nbc/miriedel/niconn-hcp --participant_id $sub"
done
