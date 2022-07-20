#!/bin/bash

#SBATCH --job-name 10ar_multi
#SBATCH --output 10ar_multi.out
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=1G
#SBATCH --gres=gpu:1
#SBATCH --partition=iiplab
#SBATCH --time=7-00:00:00
#SBATCH --mail-user zenalisa@nmsu.edu
#SBATCH --mail-type END
#SBATCH --mail-type FAIL

#some predictions for various 10ar models

python3 /project/iip/zenalisa/pytorch_fnet_leb/predict.py --gpu_ids=0 --path_dataset_csv /project/iip/zenalisa/data/fixed_aia/test_list_10ar_210302.csv --n_images 500 --path_model_dir /project/iip/zenalisa/models/fix_aia/10ar_short --class_dataset TiffDataset --no_prediction_unpropped --path_save_dir /project/iip/zenalisa/data/output/10ar_multi/depth4

python3 /project/iip/zenalisa/pytorch_fnet_leb/predict.py --gpu_ids=0 --path_dataset_csv /project/iip/zenalisa/data/fixed_aia/test_list_10ar_210302.csv --n_images 500 --path_model_dir /project/iip/zenalisa/models/fix_aia/10ar_short_bigpatch  --class_dataset TiffDataset --no_prediction_unpropped --path_save_dir /project/iip/zenalisa/data/output/10ar_multi/bigpatch

python3 /project/iip/zenalisa/pytorch_fnet_leb/predict.py --gpu_ids=0 --path_dataset_csv /project/iip/zenalisa/data/fixed_aia/test_list_10ar_210302.csv --n_images 500 --path_model_dir /project/iip/zenalisa/models/fix_aia/10ar_short_depth5  --class_dataset TiffDataset --no_prediction_unpropped --path_save_dir /project/iip/zenalisa/data/output/10ar_multi/depth5

python3 /project/iip/zenalisa/pytorch_fnet_leb/predict.py --gpu_ids=0 --path_dataset_csv /project/iip/zenalisa/data/fixed_aia/test_list_10ar_210302.csv --n_images 500 --path_model_dir /project/iip/zenalisa/models/fix_aia/10ar_short_depth6  --class_dataset TiffDataset --no_prediction_unpropped --path_save_dir /project/iip/zenalisa/data/output/10ar_multi/depth6