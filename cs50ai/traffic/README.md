# Project 5: Traffic - Analysis

This convolutional neural network is created using a sequential model from the TensorFlow Keras api.

1. The very first model was built using 1 convolutional layer with 32 filters and a 3x3 kernel, a 2 x 2 max pool layer, and 1 hidden layer with 128 neurons. This was done with a 0.5 dropout layer to minimize potential for overfitting. As can be seen from the results below, while fast to train, the results were quite poor.

    500/500 [==============================] - 1s 2ms/step - loss: 5.0721 - accuracy: 0.0539
    Epoch 2/10
    500/500 [==============================] - 1s 2ms/step - loss: 3.5900 - accuracy: 0.0571
    Epoch 3/10
    500/500 [==============================] - 1s 2ms/step - loss: 3.5410 - accuracy: 0.0570
    Epoch 4/10
    500/500 [==============================] - 1s 2ms/step - loss: 3.5184 - accuracy: 0.0570
    Epoch 5/10
    500/500 [==============================] - 1s 2ms/step - loss: 3.5079 - accuracy: 0.0570
    Epoch 6/10
    500/500 [==============================] - 1s 2ms/step - loss: 3.5030 - accuracy: 0.0570
    Epoch 7/10
    500/500 [==============================] - 1s 2ms/step - loss: 3.5007 - accuracy: 0.0570
    Epoch 8/10
    500/500 [==============================] - 1s 2ms/step - loss: 3.4995 - accuracy: 0.0570
    Epoch 9/10
    500/500 [==============================] - 1s 2ms/step - loss: 3.4989 - accuracy: 0.0564
    Epoch 10/10
    500/500 [==============================] - 1s 2ms/step - loss: 3.4986 - accuracy: 0.0570
    333/333 - 0s - loss: 3.4982 - accuracy: 0.0555 - 331ms/epoch - 994us/step

2. From there, I decided to double the filters in the input layer as well as the number of neurons in the hidden layer. While there was significant increase in the viability of the model, it was still far from accurate. Furthermore, this appeared to increase the training time significantly, making me question whether the sacrifice is worth it.

    500/500 [==============================] - 5s 10ms/step - loss: 6.4501 - accuracy: 0.0611
    Epoch 2/10
    500/500 [==============================] - 5s 10ms/step - loss: 3.5488 - accuracy: 0.0664
    Epoch 3/10
    500/500 [==============================] - 5s 10ms/step - loss: 3.4926 - accuracy: 0.0692
    Epoch 4/10
    500/500 [==============================] - 5s 10ms/step - loss: 3.4669 - accuracy: 0.0696
    Epoch 5/10
    500/500 [==============================] - 5s 10ms/step - loss: 3.4566 - accuracy: 0.0673
    Epoch 6/10
    500/500 [==============================] - 5s 10ms/step - loss: 3.4376 - accuracy: 0.0765
    Epoch 7/10
    500/500 [==============================] - 5s 10ms/step - loss: 3.3979 - accuracy: 0.0890
    Epoch 8/10
    500/500 [==============================] - 5s 10ms/step - loss: 3.3183 - accuracy: 0.1167
    Epoch 9/10
    500/500 [==============================] - 5s 10ms/step - loss: 3.1206 - accuracy: 0.1552
    Epoch 10/10
    500/500 [==============================] - 5s 10ms/step - loss: 2.6795 - accuracy: 0.2433
    333/333 - 1s - loss: 1.9408 - accuracy: 0.4163 - 521ms/epoch - 2ms/step

3. On the third attempt, I brought the number of filters and neurons back down, but doubled the number of convolution, pooling, and hidden layers. This resulted in significantly better performance while actually decreasing the training time from the previous runthrough. 

    500/500 [==============================] - 2s 2ms/step - loss: 3.0514 - accuracy: 0.2920
    Epoch 2/10
    500/500 [==============================] - 1s 2ms/step - loss: 1.2577 - accuracy: 0.6288
    Epoch 3/10
    500/500 [==============================] - 1s 2ms/step - loss: 0.7068 - accuracy: 0.7884
    Epoch 4/10
    500/500 [==============================] - 1s 2ms/step - loss: 0.4732 - accuracy: 0.8599
    Epoch 5/10
    500/500 [==============================] - 1s 2ms/step - loss: 0.3371 - accuracy: 0.9029
    Epoch 6/10
    500/500 [==============================] - 1s 2ms/step - loss: 0.2785 - accuracy: 0.9207
    Epoch 7/10
    500/500 [==============================] - 1s 2ms/step - loss: 0.2441 - accuracy: 0.9351
    Epoch 8/10
    500/500 [==============================] - 1s 2ms/step - loss: 0.2170 - accuracy: 0.9395
    Epoch 9/10
    500/500 [==============================] - 1s 2ms/step - loss: 0.1609 - accuracy: 0.9530
    Epoch 10/10
    500/500 [==============================] - 1s 2ms/step - loss: 0.1655 - accuracy: 0.9575
    333/333 - 0s - loss: 0.1724 - accuracy: 0.9615 - 385ms/epoch - 1ms/step

4. Since the last round of experimentation was so successful, I decided to try to repeat it to further increase the the number of layers to three of each convolution, pooling, and hidden. However, this simply served to increase the training time while actually decreasing overall accuracy and increasing the loss. 

    500/500 [==============================] - 2s 2ms/step - loss: 2.7790 - accuracy: 0.3027
    Epoch 2/10
    500/500 [==============================] - 1s 2ms/step - loss: 1.3028 - accuracy: 0.6207
    Epoch 3/10
    500/500 [==============================] - 1s 2ms/step - loss: 0.8220 - accuracy: 0.7564
    Epoch 4/10
    500/500 [==============================] - 1s 2ms/step - loss: 0.5891 - accuracy: 0.8286
    Epoch 5/10
    500/500 [==============================] - 1s 2ms/step - loss: 0.4607 - accuracy: 0.8659
    Epoch 6/10
    500/500 [==============================] - 1s 2ms/step - loss: 0.3916 - accuracy: 0.8901
    Epoch 7/10
    500/500 [==============================] - 1s 2ms/step - loss: 0.3483 - accuracy: 0.9040
    Epoch 8/10
    500/500 [==============================] - 1s 2ms/step - loss: 0.3016 - accuracy: 0.9136
    Epoch 9/10
    500/500 [==============================] - 1s 2ms/step - loss: 0.2418 - accuracy: 0.9290
    Epoch 10/10
    500/500 [==============================] - 1s 2ms/step - loss: 0.2587 - accuracy: 0.9294
    333/333 - 0s - loss: 0.2233 - accuracy: 0.9378 - 412ms/epoch - 1ms/step

5. Since it appears that increasing the number of layers was counterproductive, I once again decided to try increasing the number of filters or neurons in 1, 2, 3, or 4 of the layers. All this served to do was increase the amount of training time while maintaining more or less the same accuracy and, once again, increasing the loss. The results below were from doubling the number of filters/neurons on all four. 

    500/500 [==============================] - 3s 5ms/step - loss: 2.5087 - accuracy: 0.4537   
    Epoch 2/10
    500/500 [==============================] - 2s 5ms/step - loss: 0.6411 - accuracy: 0.8185
    Epoch 3/10
    500/500 [==============================] - 2s 5ms/step - loss: 0.3418 - accuracy: 0.9038
    Epoch 4/10
    500/500 [==============================] - 2s 5ms/step - loss: 0.2553 - accuracy: 0.9324
    Epoch 5/10
    500/500 [==============================] - 2s 5ms/step - loss: 0.2155 - accuracy: 0.9416
    Epoch 6/10
    500/500 [==============================] - 2s 5ms/step - loss: 0.1926 - accuracy: 0.9503
    Epoch 7/10
    500/500 [==============================] - 2s 5ms/step - loss: 0.1702 - accuracy: 0.9550
    Epoch 8/10
    500/500 [==============================] - 2s 5ms/step - loss: 0.1346 - accuracy: 0.9635
    Epoch 9/10
    500/500 [==============================] - 2s 5ms/step - loss: 0.1353 - accuracy: 0.9647
    Epoch 10/10
    500/500 [==============================] - 2s 5ms/step - loss: 0.1397 - accuracy: 0.9635
    333/333 - 1s - loss: 0.2207 - accuracy: 0.9597 - 562ms/epoch - 2ms/step

6. After performing various more experiments by increasing and decreasing the filters, neurons, and even the dropout rate, it would appear that the code from the third input consistently performed the best. As such, it was the version that was preserved in the final submission.