# YOLOv5_csgo

## Describe

A model and code for csgo character head detection and locking based on yolov5.

This is a practice and replication project for deep learning beginners. The project code can only be used for related knowledge learning and communication, and is not allowed to be used for the actual use of the game or to destroy the game environment.

The code tests are all done on csgo's personal server and have not been run in any competitive competitions.

Welcome everyone to communicate and improve this code.

## Quick Start Examples

### install

```python
git clone https://github.com/ArmandRay/yolov5_csgo
pip install -r requirements.txt
```

### run

Run the main.py file in the main directory.

### train and detect

If you need to train your own model or detect, the related method is the same as [yolov5](https://github.com/ultralytics/yolov5).

## Custom Parameters and Code Explanation

### window

![image-20220722170649387](C:\Users\Armand Ray\AppData\Roaming\Typora\typora-user-images\image-20220722170649387.png)

Used to determine related windows and subsequent operations.

 You need to modify this parameter, or comment the statement and use the `FindWindow()` function below. The 'csgo' parameter in parentheses is the title of the window you want to look for.

![image-20220722171602970](C:\Users\Armand Ray\AppData\Roaming\Typora\typora-user-images\image-20220722171602970.png)

If your `FindWindow()` function cannot find the relevant window, you can run the commented code at the bottom of the file separately. You can find the window handle you want in the output of the code.

NOTICE: If you use a fixed handle parameter, please do not close your window arbitrarily.

### model

![image-20220722171451697](C:\Users\Armand Ray\AppData\Roaming\Typora\typora-user-images\image-20220722171451697.png)

If you need to use your own model, please modify it here.

## Reference

https://github.com/ultralytics/yolov5

https://blog.csdn.net/light169/article/details/123378140

https://www.jianshu.com/p/f08af400f2fa