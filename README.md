# Viola-Jones-Implementation

This project covers a basic implementation of the Viola-Jones algorithm through use of openCV and their Haar Cascade files. The method itself is simple. By rapidly checking certain haar-like features against the target image, it can determine if certain features - specific light and dark areas- composite a human face. If you use different haar cascades, you can apply the model to detect many other things, but I choose to provide the example with face detection as an easy to understand motivation. For example, we apply the model to a stock image of multiple individuals. 

![VJTest](https://github.com/user-attachments/assets/2eb19ebf-d609-4ea8-88fe-b7ee11dc561d)

As we can see, the model has no issue identifying the faces of every individual in the photo. However, it won't be easy to have such easily readable data, and the images you collect from video feeds are going to have a ton of different angles, expressions and distances. 
