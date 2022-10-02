CS50 AI Project 5 traffic

Author: Pekka Iso-Markku

\

Project involves the creation of a sequential DL model to classify
images of road signs.

\

Part 1: load\_data() function

\

Part 2: get\_model() function

\

A problem I encountered was the number of samples used in the model.fit
stage. For example:

\

Epoch 10/10

583/583 \[==============================\] - 5s 9ms/step - loss: 0.0165
- accuracy: 0.9950

\

Above is terminal output where one can see that the number of samples in
the training data is 583 (0.7/0.3 train test split) even though the
number of samples in the whole data set is \>25k.

\

I've checked both functions whether there is an issue somewhere, for
instance using len(labels), but I always see that the amounts are
correct. Do not know what is the issue here.

\

I started off using one Conv-Pool layer with number of channels in the
conv-layer set to 32. Also, inspired by the lecture notes I right away
included a hidden layer and Dropout.

\

After tinkering around with the number of channels I got the best
results with Conv-Conv-Pool Conv-Pool with a drop-out of 0.5 to prevent
overfitting.[ ]{.Apple-converted-space}

\

Model performed with .9939 accuracy on the test set.
