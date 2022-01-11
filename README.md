# OCR for Handwritting

Author: Yunxiang MA; Yiyu WANG; Yiming YAN

Instructions on how to run the code.

## Before running:

First download EMNIST dataset. Unzip the split dataset you need to use in experiment.(eg. We used emnist-mnist dataset for training).

​	**· **If you need to train on different dataset, please modify the path of dataset. Location: dataProcess.py, line 9-14. 

Please build a new folder "dataset" at the same directory as python scripts were placed.

![](https://github.com/SoutaTakanashi/MYXNB/blob/main/image-20220111014630400.png)

And in folder "dataset" place the dataset files with folders :

![](https://github.com/SoutaTakanashi/MYXNB/blob/main/image-20220111014746464.png)



## Dependencies:

Make sure you're ready for running the code.

Get them installed:

​	pytorch , torchvision, Pillow, PyQt5 , scikit-image



## Guidance:

​	Run main.py in pytorch environment. 

![](https://github.com/SoutaTakanashi/MYXNB/blob/main/image-20220111015453668.png)

​	

​	Enter the number as told: 1 for training, 2 for selecting a picture for prediction. 

​	If you enter 1,then you have to wait for about 15 mins for training the model.

When entering 2, a window will pop up and you may select images for OCR.

![](https://github.com/SoutaTakanashi/MYXNB/blob/main/image-20220111015639037.png)

Click "Get Picture" and select a picture from local directory, then click "Predict", you may get the result of OCR.

![](https://github.com/SoutaTakanashi/MYXNB/blob/main/image-20220111015847880.png)



