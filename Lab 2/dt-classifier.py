import pandas as pd

#Load CSV files for iris datasets:
inputs_train=pd.read_csv('datasets/iris_train.csv',usecols = [0,1,2,3],skiprows = None,header=None).values
labels_train = pd.read_csv('datasets/iris_train.csv',usecols = [4],skiprows = None ,header=None).values.reshape(-1)
inputs_val=pd.read_csv('datasets/iris_test.csv',usecols = [0,1,2,3],skiprows = None,header=None).values
labels_val = pd.read_csv('datasets/iris_test.csv',usecols = [4],skiprows = None ,header=None).values.reshape(-1)

from sklearn import tree
from sklearn.metrics import accuracy_score
# TODO build a decision tree here.
# TODO evaluate its accuracy on the validation set (should score>90%)
# TODO plot your decision tree and save it to a file called "decision-tree-iris.png"
# TODO save the decision tree using pickle
clf=tree.DecisionTreeClassifier(max_depth=2,min_samples_leaf=1)
clf.fit(inputs_train,labels_train)
output_predictions=clf.predict(inputs_val)
print("output_predictions",output_predictions)
print("Accuracy",accuracy_score(labels_val,output_predictions))


import matplotlib.pyplot as plt
fig=plt.figure()
tree.plot_tree(clf,feature_names=['sepal length (cm)','sepal width (cm)','petal length (cm)','petal width (cm)'],
               class_names=['setosa', 'versicolor', 'virginica'],filled=True)
fig.savefig('decision_tree.png')


import pickle
pickle_out=open("iris_decision_tree.p","wb")
s=pickle.dump(clf,pickle_out)
pickle_out.close()


pickle_in=open("iris_decision_tree.p","rb")
my_clf=pickle.load(pickle_in)
output_predictions_loaded=my_clf.predict(inputs_val)
print("Accuracy(from loaded tree)",accuracy_score(labels_val,output_predictions_loaded))