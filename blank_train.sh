#!/bin/bash

#SBATCH --job-name JOBNAME
#SBATCH --output JOBNAME.out
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=1G
#SBATCH --gres=gpu:1
#SBATCH --partition=iiplab
#SBATCH --time=7-00:00:00
#SBATCH --mail-user zenalisa@nmsu.edu
#SBATCH --mail-type END
#SBATCH --mail-type FAIL

#7/3/21 training MODELNAME (with fixed AIA data) on TRAINLIST

python3 /project/iip/zenalisa/pytorch_fnet_leb/train_model.py --gpu_ids=0 --n_iter=200000 --path_dataset_csv /fs1/project/iip/zenalisa/data/DATASET/lists/TRAINLIST --buffer_size 5 --path_run_dir /fs1/project/iip/zenalisa/models/last/MODELNAME --batch_size 30 --class_dataset TiffDataset --patch_size 256 256 --nn_module fnet_nn_2d
