# VDAS_Project
This project is Vehicle Damage Assessment System via 3D retrieval
Pipeline
![pic](https://user-images.githubusercontent.com/68935390/154282165-a734bd79-3f40-456d-a4ad-f951583c0d56.PNG)
How to setup 
1. Must have anaconda or miniconda
2. Create an environment according to this order.
   - conda create -n pytorch3d python=3.9
   - conda activate pytorch3d
   - conda install -c pytorch pytorch=1.9.1 torchvision cudatoolkit=10.2
   - conda install -c fvcore -c iopath -c conda-forge fvcore iopath
3. Install pytorch 3D according to this order
   - git clone https://github.com/facebookresearch/pytorch3d.git
   - cd pytorch3d && pip install -e .
4. Finish
