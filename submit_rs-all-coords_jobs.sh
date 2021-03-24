
hcp_data_dir='/home/data/nbc/external-datasets/hcp/niconn-hcp'

if [ ! -d $hcp_data_dir/code/err ]; then
  mkdir $hcp_data_dir/code/err
fi
if [ ! -d $hcp_data_dir/code/out ]; then
  mkdir $hcp_data_dir/code/out
fi

#this count thing is to skip the header line
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
  while [ $(squeue -u miriedel -o %j --noheader -r | sed -n '/_niconn-hcp_rs-all-coords/p' | wc -l) -gt 59 ]; do
      sleep 30s
  done

    sbatch -J "$sub"_niconn-hcp_rs-all-coords \
           -o $hcp_data_dir/code/out/"$sub"_niconn-hcp_rs-all-coords \
           -e $hcp_data_dir/code/err/"$sub"_niconn-hcp_rs-all-coords \
           -p IB_44C_512G \
           --account=iacc_nbc \
           --qos=pq_nbc \
           -n 1 \
           --wrap="python3 $hcp_data_dir/code/rs-all-coords.py --rs_data_dir $hcp_data_dir --work_dir /scratch/miriedel/niconn-hcp --participant_id $sub --roi_dir /home/data/nbc/misc-projects/meta-analyses/meta-analysis_implicit-learning/derivatives/rois"
done
