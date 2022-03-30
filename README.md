# VDAS_Project
## This project is Vehicle Damage Assessment System via 3D retrieval
## Overview
![allpic](https://user-images.githubusercontent.com/68935390/160869047-3d61d84c-f685-4c73-ba85-4ffb1ff8309b.PNG)


---------------------------------------------------------------------------------------------------------------------
## setup pytorch 3D library
 1. Must have anaconda or miniconda
 2. Create an environment according to this order:
            
            conda create -n pytorch3d python=3.9
            conda activate pytorch3d
            conda install -c pytorch pytorch=1.9.1 torchvision cudatoolkit=10.2
            conda install -c fvcore -c iopath -c conda-forge fvcore iopath
 3. Install pytorch 3D according to this order
   
         git clone https://github.com/facebookresearch/pytorch3d.git
         cd pytorch3d && pip install -e .
 4. Finish
----------------------------------------------------------------------------------------------------------------------
## install openpyxl 
#### we use openpyxl for open excel file.  Install with this command: 
     conda install openpyxl" and y for confirm install
----------------------------------------------------------------------------------------------------------------------
## How to use this project?
 1. Clone this github:
         
        git clone https://github.com/MeenTers/VDAS_Project.git
 2. open terminal and select path folder cd (your root) /VDAS_Project
 3. activate pytorch3D 
 
         conda activate pytorch3d 
 4. open webapplication 
      
        python webflask.py
 5. now you can use that! 
