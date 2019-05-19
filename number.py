import cv2
import numpy as np
import pickle
from skimage.feature import hog
from sklearn.svm import SVC
from keras.datasets import mnist
from sklearn.metrics import accuracy_score

class Number:
    def __init__(self):
        (X_train,y_train),(X_test,y_test) = mnist.load_data()

        X_train_feature = []
        for i in range(len(X_train)):
            feature = hog(X_train[i],orientations=9,pixels_per_cell=(14,14),cells_per_block=(1,1),block_norm="L2")
            X_train_feature.append(feature)
        X_train_feature = np.array(X_train_feature,dtype = np.float32)

        X_test_feature = []
        for i in range(len(X_test)):
            feature = hog(X_test[i],orientations=9,pixels_per_cell=(14,14),cells_per_block=(1,1),block_norm="L2")
            X_test_feature.append(feature)
        X_test_feature = np.array(X_test_feature,dtype=np.float32)

        self.X_train_feature = X_train_feature
        self.y_train = y_train
        self.X_test_feature = X_test_feature
        self.y_test = y_test

    def SVM(self):
        clf = SVC(kernel='linear', C=0.01)
        clf.fit(self.X_train_feature,self.y_train)
        with open('Digits_SVC'+'.pickle', mode='wb') as f:
            pickle.dump(clf,f)
        return clf

    def print_accuracy(self):
        clf = self.SVM()
        y_pred = clf.predict(self.X_train_feature)
        acc_train=accuracy_score(self.y_train, y_pred)
        print ('accuracy on training data(not class average)',acc_train)

        y_pred_test = clf.predict(self.X_test_feature)
        acc_test=accuracy_score(self.y_test, y_pred_test)
        print ('accuracy on test data(not class average)',acc_test)

        y_pred_class = clf.predict_classes(self.X_test_feature)
        print(classification_report(self.y_test, y_pred_class))

number = Number()
number.print_accuracy()