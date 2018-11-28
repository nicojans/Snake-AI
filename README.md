# Snake-AI
Simple Python implementation of Snake controlled by an AI using Tensorflow/Keras

### The model

##### Input:
4 values representing the distance from the food in each direction, if the food is not in the direction the value is high to represent it being very far away. This works much better than having 2 inputs that represent the relative position of the food.
4 values representing the available space in each direction. 0 means the snake will dies if it goes in that direction. The value is a good enough approximation of the longest path the snake could take while still being quick to compute.

##### Hidden layer:
1 with 16 nodes. More nodes or layers does not improve the results.

##### Output:
4 for each directions

### Result:
Trained in 10x10 space. The NN find the best strategy for this model in less than 5 minutes. 
It learns quickly to avoid dying and get the food then it learns how to prioritize a safe path while still getting the food. With these inputs it cannot learn how to navigate the area in order to always have a safe path so it get stuck and dies at a size of 39 on average.
