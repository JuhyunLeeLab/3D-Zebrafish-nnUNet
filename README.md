
# Read this procedure to implement our nnUNetv2 
# Procedure courtesy of Saad Saeed and Gilberto Hernandez 

Installation of nnUNetv2 Procedure 
 

PART 1 NNUNET 

Setting up the environment 

Create new environment. 
Enter command: conda create -n NAME python==3.10 
NAME is desired environment name. Ex: nn_UNet 
conda create -n nn_UNet python==3.10 
 
Activate environment: 
conda activate NAME 
Ex: conda activate nn_UNet 
Check version. Enter command: python –version  
 
Cd to the directory where all the zebrafish repositories will be stored. 
 
Enter command git clone https://github.com/nasyxx/zebrafish_seg.git 
If git is not installed then – sudo apt install git – all 
Ex: conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia 
 

 
Transfer the tiff_converter.py file into this directory. 
 

cd into data directory 
Enter command: mkdir raw ori segmented results preprocessed cropped inference 
 
Save your environment variables. 
Enter command: vim ~/.bashrc 
If not installed enter following command: sudo apt install vim 
Retry command after installation is finished 
If blank, double check spelling and retry.  
Press Insert key to begin editing. 
Move indicator to very bottom of page and add: 
export nnUNet_raw_data_base=data/raw/ 

export nnUNet_raw=data/raw/nnUNet_raw_data 

export nnUNet_results=data/results/ 

export nnUNet_preprocessed=data/preprocessed/ 

export RESULTS_FOLDER=/home/USER/nnUNetFrame/zebrafish_seg/data/results/ 

Press Escape key to return to command mode. 
Enter :x to save and exit (Alternatively enter :wq) 
Enter :q! to exit WITHOUT saving 
 

Source your environmental variables: 
Enter command: source ~/.bashrc 
Reactivate your environment: conda activate NAME 
Ex: conda activate nn_UNet 
 
 
Install nnUNet repository  
git clone https://github.com/MIC-DKFZ/nnUNet.git 
cd nnUNet 
pip install -e . 
pip install --upgrade git+https://github.com/FabianIsensee/hiddenlayer.git 
 
Install pytorch https://pytorch.org/get-started/locally/ 
Follow directions to install according to computer specifications 
 
Install pdm and start project 
python -m pip install pdm 
pdm init 
Follow the prompts. You will see: 

"Please enter the Python interpreter to use 

0. /home/leelab/anaconda3/envs/zebrafish_seg/bin/python (3.10) 

1. /home/leelab/anaconda3/envs/zebrafish_seg/bin/python3.10 (3.10) 

2. /usr/bin/python3.10 (3.10) 

Please select (0): " 

Enter whichever is your preference. Ex: Please select (0): 2 

"Is the project a library that is installable? 
If yes, we will need to ask a few more questions to include the project name and build backend [y/n] (n):” 

Enter: y 

Project name: Zebrafish Segmentation 

Project version (0.1.0): 0.1.0 

Project description (): Auto-segmentation tool  

“Which build backend to use? 
	0. pdm-backend 
	1. Setuptools 
	2. flit-core 
	3. Hatchling “ 

Enter: 0 

“License(SPDX name) (MIT): AFL-1.1 
	Author name (): JL 
	Author email (): juhyun.lee@uta.edu 
	Python requires('*' to allow any) (>=3.10): >=3.10” 

Install remaining dependencies: 
pdm run pip install tqdm 
pdm run pip install pathlib 
pdm run pip install rich 
pdm run pip install smile_config 
pdm run pip install tifffile 
pdm run pip install nnunet 
pdm run pip install nnunetv2 
Note, some may not install. Keep an eye on errors for future commands to see which libraries are missing. 
Dataset Conversion 

Cd to src folder, then open dc.py 
Either with command: vim dc.py 
Press Insert key to begin editing 
If not installed enter following command: sudo apt install vim 
Try again when installed 
Or may be opened and edited using Notepad 
 
Edit line 75:  
Space = tuple(map(float,conf.space.split(“,”))) 
 
Comment out lines 88, 100-119 using # 
If on vim, press Escape key to return to command mode 
Use command :x  or  :wq  to save and exit, note to enter commands the command must begin with colon key “ : ” 
Use command  :q!  to exit WITHOUT saving 
If on Notepad, simply save the file before exiting.  
Either CTRL + S 
On menu bar File>Save 
Return to directory containing zebrafish_seg repositories from github  
Enter in terminal while in src directory: cd .. 
 
Enter command: pdm run python -m src.dc --tod --ori path/to/raw --seg path/to/seg --database path/to/database_directory --name NAME –t XXX 
Note:  
If environment variables are set up already, you do not need to specify --ori, --seg, --database. 
path/to/raw is the pathway to the ori directory. Default: data/ori 
path/to/seg is the pathway to the segmented directory. Default: data/segmented 
path/to/database_directory is pathway to zebrafish database. Default: data/ 
NAME is to be replaced with desired name. Ex: zebrafish_segv2 
XXX is to be replaced with three digit task identifier number. Ex: 777 
 
Convert Task (nnUNetv1 format) to Dataset (nnUNetv2 format): 
pdm run nnUNetv2_convert_old_nnUNet_dataset Path/To/Task/Folder DatasetXXX_NAME 
Path/To/Task/Folder is the pathway to where the task is located. Ex: data/raw/nnUNet_raw_data/Task777_zebrafish_segv2 
Replace XXX with three digit dataset identification number. Ex: 777 
Replace NAME with desired name for the dataset. Ex: zebrafish_segv2 
Final product example: Dataset777_zebrafish_segv2 
 

Plan and Preprocess 

Edit default preprocessor to include Laplacian of Gaussian. 
Download default_preprocessor.py file containing the pre-added code. Move to directory containing the nnUNet repositories. Default preprocessor can be found at: nnUNet > nnUNetv2 > preprocessing > preprocessors > default_preprocessor.py 
Delete default_preprocessor.py and replace with the updated default_preprocessor.py file. The new version will include the Lapacian of Gaussian code using scipy library. 
 
Begin plan and preprocessing. 
Enter code:  
pdm run nnUNetv2_plan_and_preprocess -d XXX -c 3d_fullres  
--verify_dataset_integrity  
Replace XXX with Dataset three digit ID. Ex: pdm run nnUNetv2_plan_and_preprocess -d 777 -c 3d_fullres --verify_dataset_integrity  
 
(Optional) To check to see if the new preprocessor is working as intended, utilize the tiff_converter.py file. 
Make new directory in data that will contain the preprocessed .tif files. 
(Optional) Create subdirectory for the converted .npz to .tif files for organizational purposes. 
Enter command: vim tiff_converter.py  
Replace input_folder = ‘path/to/preprocessed/images’ 
Ex. input_folder = '/home/senior/nnUNetFrame/zebrafish_seg/data/preprocessed/Dataset444_zebrafish/nnUNetPlans_3d_fullres/' 
Replace output_folder= ’path/to/tiff/output’ 
Ex: output_folder = '/home/senior/nnUNetFrame/zebrafish_seg/data/tiff_files/Dataset444_zebrafish_seg' 
Enter command: pdm run python tiff_converter.py 
 
 
Once completed, begin training. 
Enter code: pdm run nnUNetv2_train DATASET_NAME_OR_ID 3d_fullres 5 
Replace DATASET_NAME_OR_ID with dataset id used for plan and preprocessing. Ex: pdm run nnUNetv2_train 777 3d_fullres 5 
Results will be found in data/results 
