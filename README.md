Zebrafish
1 Requirments

Self
    Clone this repo with submodules.

        git clone --recursive git@github.com:nasyxx/zebrafish_seg.git

Python and nnUNet
    Require python >= 3.10 with GPUs.

        Run the following shell commands.
        python -m pip install pdm # for python project management.
        pdm install # install python dependencies.

Data
    Raw and segmented tif files.

        Default raw data folder should in data/ori. You can change it with the ori property of Conf class in the config.py file or using command line option --ori path/to/raw.
        Default segmented data folder should in data/seg. You can change it with the seg property of Conf class in the config.py or using command line option --seg path/to/seg.

2 Usage

    Input
        3d tif files with the shape (Height, Weight, T)
    Output
        nnUNet MSD files
        See: https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/dataset_conversion.md

2.1 Train
2.1.1 Data conversion

Run the following shell commands to convert data with default folders:

pdm run python -m src.dc --tod

Run the following shell commands to convert data with custom folders:

pdm run python -m src.dc --tod --ori path/to/raw --seg path/to/seg --database path/to/database_folder
2.1.2 Shell env

After data conversion, you should see a env.sh file in the root folder. Run the following shell command to source it and set the nnUNet env.

source env.sh

The default of it should be like:

export nnUNet_raw_data_base=data/raw/
export nnUNet_preprocessed=data/preprocessed/
export RESULTS_FOLDER=data/results/

See here https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/setting_up_paths.md for nnUNet env.
2.1.3 Train

Run the following shell commands to train the model.

pdm run nnUNet_train 3d_fullres nnUNetTrainerV2 777 0

If you use multiple GPUs, you can run the following shell commands to train the model.

pdm run nnUNet_train_DP 2d nnUNetTrainerV2_DP 777 0 -gpus 2 --dbs

The results should be in the data/results folder by default.

nnUNet_train
    The train entry point.
3d_fullres
    The model class. Can be 2d, 3d_fullres, 3d_lowres and 3d_cascade_fullres. See here: https://github.com/MIC-DKFZ/nnUNet#2d-u-net
nnUNetTrainerV2
    The trainer class.
777
    Task ID. Should geater than 500. You can change it in config.py or using command line option --task=777.
0
    Fold. Should be 0, 1, 2, 3, 4.

Here is the nnUNet train example:

    https://github.com/MIC-DKFZ/nnUNet#examples
    https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/training_example_Hippocampus.md
    https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/inference_example_Prostate.md

2.2 Inference

The pipeline of inference is: Test Data conversion from tif to nii=>Inference=>Data conversion from nii back to tif.
2.2.1 Data conversion

It’s the same as the train data conversion.
2.2.2 Inference

See in nnUNet: https://github.com/MIC-DKFZ/nnUNet#run-inference

Thus, you can run this command to inference:

pdm run nnUNet_predict -i path/to/converted/test/folder -o path/to/output -t 777 -m 3d_fullres -tr nnUNetTrainerV2 -m 2d

If you use multiple GPUs, simply change the -tr nnUNetTrainerV2 to -tr nnUNetTrainerV2_DP.
2.2.3 From nii to tif

Run the following shell commands to convert the nii files to tif files.

pdm run python -m src.dc --tot in_=path/to/input_nii out_=path/to/output_tif
3 Complete help buffer

> python config.py --help

usage: config.py [-h] [--task TASK] [--name NAME] [--postfix POSTFIX] [--database DATABASE] [--raw RAW] [--preprocessed PREPROCESSED]
                 [--results RESULTS] [--cropped CROPPED] [--ori ORI] [--seg SEG] [--space SPACE] [--tod | --no-tod] [--tot | --no-tot] [--in_ IN_]
                 [--out_ OUT_] [--raw_ RAW_] [--preprocessed_ PREPROCESSED_] [--results_ RESULTS_]

Configuration for zebrafish.

options:
  -h, --help            show this help message and exit
  --task TASK           nnUNet task ID. (default: 777)
  --name NAME           nnUNet task name (default: Task777_Zebrafish)
  --postfix POSTFIX     - (default: )
  --database DATABASE   Dataset base path (default: data/)
  --raw RAW             nnUNet raw data path (default: raw/)
  --preprocessed PREPROCESSED
                        nnUNet preprocessed data path (default: preprocessed/)
  --results RESULTS     nnUNet results path (default: results/)
  --cropped CROPPED     nnUNet cropped path (default: cropped/)
  --ori ORI             Original photo dir. (default: data/ori/)
  --seg SEG             Segmented dir. (default: data/segmented/)
  --space SPACE         Distance of each dim of the one pixel (T, H, W) (default: 1,1,1)
  --tod, --no-tod       Convert tif to dataset? (default: True)
  --tot, --no-tot       Convert nii back to tif? (default: True)
  --in_ IN_             Dir of result of nii.gz (default: )
  --out_ OUT_           Dir of results of tif dir (default: )
  --raw_ RAW_           Alias, left empty (default: data/raw/)
  --preprocessed_ PREPROCESSED_
                        Alias, left empty (default: data/preprocessed/)
  --results_ RESULTS_   Alias, left empty (default: data/results/)