# VDAS_Project
This project is Vehicle Damage Assessment System via 3D retrieval
Part 1 Upload 3D model
![Part1](https://user-images.githubusercontent.com/68935390/156372314-04cadd35-cd7c-4a9e-99f1-a78125d0d270.PNG)
Part 2 Compare 3D models
![Part2](https://user-images.githubusercontent.com/68935390/156372367-79a64b0c-3794-4b8b-8600-ebfe3d5192d5.PNG)
How to setup pytorch 3D library
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
