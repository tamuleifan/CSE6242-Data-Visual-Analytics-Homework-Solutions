from util import entropy, information_gain, partition_classes
import numpy as np 
import ast

class DecisionTree(object):
    def __init__(self):
        # Initializing the tree as an empty dictionary or list, as preferred
        #self.tree = []
        #self.tree = {}
        self.tree = {}
        self.max_depth = 50

    def learn(self, X, y):
        # TODO: Train the decision tree (self.tree) using the the sample X and labels y
        # You will have to make use of the functions in utils.py to train the tree
        
        # One possible way of implementing the tree:
        #    Each node in self.tree could be in the form of a dictionary:
        #       https://docs.python.org/2/library/stdtypes.html#mapping-types-dict
        #    For example, a non-leaf node with two children can have a 'left' key and  a 
        #    'right' key. You can add more keys which might help in classification
        #    (eg. split attribute and split value)

        return self.grow_tree(X, y, 1)

    def grow_tree(self,X, y, depth):
        if depth >=self.max_depth:
            self.tree['node'] = 'leaf'
            self.tree['label'] = self.majority_vote(y)
            return

        if len(set(y)) == 1:
            self.tree['node'] = 'leaf'# this is a leaf
            self.tree['label'] = y[0]# class label for the leaf
            return

        num_attributes = len(X[0])

        #theoretical optimal number of attributes for splitting
        #num_split_attributes = int(np.floor(np.sqrt(num_attributes)))-1

        attrbutes_index_container = np.random.choice(num_attributes,size = 6,replace=False)

        #print(attrbutes_index_container)
        # initialize the value for the maximum information gain, split attribute and value, and containers of children nodes 
        maxIG = -1
        split_attribute = -1
        split_val = None
        X_left = []
        X_right = []
        y_left = []
        y_right = []
        # iterate the attributes
        for j in attrbutes_index_container: 
            attrValContainer = []
            #iterate the instances
            for i in range(len(X)):             
                attrValContainer.append(X[i][j])
            #get unique values for each attribute and sort asec 
            #if numerical attribute, try the means of adjacent values as the split values
            valUniqueContainer = sorted(set(attrValContainer))
            if isinstance(X[0][j],float) or isinstance(X[0][j],int):
                splitValueContainer = [(a + b)/2 for a, b in zip(valUniqueContainer[:-1], valUniqueContainer[1:])]
                #splitValueContainer = [float(np.mean(attrValContainer)),float(np.mean(attrValContainer))]
            #if categorical attribute, try each value
            else:
                splitValueContainer = valUniqueContainer
            for value in splitValueContainer:
                X1, X2, y1, y2 = partition_classes(X, y, j, value)
                IG = information_gain(y,[y1,y2])
                if IG > maxIG:
                    maxIG = IG
                    split_attribute = j
                    split_val = value
                    X_left = X1
                    X_right = X2
                    y_left = y1
                    y_right = y2

        if len(y_left) == 0 or len(y_right) == 0 or maxIG <= 0.01:
            self.tree['node'] = 'leaf'
            self.tree['label'] = self.majority_vote(y)
            return
        else:
            self.tree['left'] = DecisionTree()
            self.tree['right'] = DecisionTree()
            self.tree['split_attribute'] = split_attribute
            self.tree['split_value'] = split_val
            self.tree['node'] = 'internal'
            self.tree['left'].grow_tree(X_left, y_left,depth+1)
            self.tree['right'].grow_tree(X_right, y_right,depth+1)


    def majority_vote(self, y):
        counts = np.bincount(y)
        vote = np.argmax(counts)
        return vote

    def classify(self, record):
        # TODO: classify the record using self.tree and return the predicted label
        root = self.tree
        #print(root)
        while 'split_value' in root:
            split_attribute = root['split_attribute']
            split_val = root['split_value']

            if isinstance(record[split_attribute], float) or isinstance(record[split_attribute], int):
                if record[split_attribute] <= split_val:
                    root = root['left'].tree
                else:
                    root = root['right'].tree
            else:
                if record[split_attribute] == split_val:
                    root = root['left'].tree
                else:
                    root = root['right'].tree

        return root['label']