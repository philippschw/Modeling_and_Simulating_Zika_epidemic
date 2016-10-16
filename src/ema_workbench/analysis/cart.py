'''
A scenario discovery oriented implementation of CART. It essentially is a 
wrapper around scikit-learn's version of CART. 


'''
from __future__ import (absolute_import, print_function, division,
                        unicode_literals)
import six
import math

import numpy as np
import numpy.lib.recfunctions as recfunctions
from sklearn import tree
from sklearn.externals.six import StringIO

from ..util import ema_logging
from . import scenario_discovery_util as sdutil


# Created on May 22, 2015
# 
# .. codeauthor:: jhkwakkel <j.h.kwakkel (at) tudelft (dot) nl>


__all__ = ['setup_cart',
           'CART']

def setup_cart(results, classify, incl_unc=[], mass_min=0.05):
    """helper function for performing cart in combination with data
    generated by the workbench. 
    
    Parameters
    ----------
    results : tuple of structured array and dict with numpy arrays
              the return from :meth:`perform_experiments`.
    classify : string, function or callable
               either a string denoting the outcome of interest to 
               use or a function. 
    incl_unc : list of strings
    mass_min : float
    
    
    Raises
    ------
    TypeError 
        if classify is not a string or a callable.
    
    """
    
    if not incl_unc:
        x = np.ma.array(results[0])
    else:
        drop_names = set(recfunctions.get_names(results[0].dtype))-set(incl_unc)
        x = recfunctions.drop_fields(results[0], drop_names, asrecarray = True)
    if isinstance(classify, six.string_types):
        y = results[1][classify]
        mode = sdutil.REGRESSION
    elif callable(classify):
        y = classify(results[1])
        mode = sdutil.BINARY
    else:
        raise TypeError("unknown type for classify")
    
    return CART(x, y, mass_min, mode=mode)


class CART(sdutil.OutputFormatterMixin):
    '''CART algorithm
    
    can be used in a manner similar to PRIM. It provides access
    to the underlying tree, but it can also show the boxes described by the
    tree in a table or graph form similar to prim.

    Parameters
    ----------
    x : recarray
    y : ndarray
    mass_min : float, optional
               a value between 0 and 1 indicating the minimum fraction
               of data points in a terminal leaf. Defaults to 0.05, 
               identical to prim. 
    mode : {BINARY, CLASSIFICATION, REGRESSION}
           indicates the mode in which CART is used. Binary indicates
           binary classification, classification is multiclass, and regression
           is regression.

    Attributes
    ----------
    boxes : list
            list of recarray box lims
    stats : list
            list of dicts with stats 
    
    Notes
    -----
    This class is a wrapper around scikit-learn's CART algorithm. It provides
    an interface to CART that is more oriented towards scenario discovery, and
    shared some methods with PRIM
    
    See also
    --------
    :mod:`prim`
        
    '''
    
    sep = '?!?'
    
    def __init__(self, x,y, mass_min=0.05, mode=sdutil.BINARY):
        ''' init
        
        '''
        
        self.x = x
        self.y = y
        self.mass_min = mass_min
        self.mode = mode

        # we need to transform the structured array to a ndarray
        # we use dummy variables for each category in case of categorical 
        # variables. Integers are treated as floats
        self.feature_names = []
        columns = []
        for unc, dtype in x.dtype.descr:
            dtype = x.dtype.fields[unc][0]
            if dtype==np.object:
                categories =  sorted(list(set(x[unc])))
                for cat in categories:
                    label = '{}{}{}'.format(unc, self.sep,cat)
                    self.feature_names.append(label)
                    columns.append(x[unc]==cat)
            else:
                self.feature_names.append(unc)
                columns.append(x[unc])

        self._x = np.column_stack(columns)
        self._boxes = None
        self._stats = None

    @property
    def boxes(self):
        assert self.clf
        
        if self._boxes:
            return self._boxes
    
        # based on
        # http://stackoverflow.com/questions/20224526/how-to-extract-the-
        # decision-rules-from-scikit-learn-decision-tree
        assert self.clf
        
        left = self.clf.tree_.children_left
        right = self.clf.tree_.children_right
        threshold = self.clf.tree_.threshold
        features = [self.feature_names[i] for i in self.clf.tree_.feature]
    
        # get ids of leaf nodes
        leafs = np.argwhere(left == -1)[:,0]     
    
        def recurse(left, right, child, lineage=None):          
            if lineage is None:
                # lineage = [self.clf.tree_.value[child]]
                lineage = []
            
            if child in left:
                parent = np.where(left == child)[0].item()
                split = 'l'
            else:
                parent = np.where(right == child)[0].item()
                split = 'r'
    
            lineage.append((parent, split, threshold[parent],
                            features[parent]))
    
            if parent == 0:
                lineage.reverse()
                return lineage
            else:
                return recurse(left, right, parent, lineage)
            
        box_init = sdutil._make_box(self.x)
        boxes = []
        for leaf in leafs:
            branch = recurse(left, right, leaf)
            box = np.copy(box_init)
            for node in branch:
                direction = node[1]
                value = node[2]
                unc = node[3]
                
                if direction=='l':
                    try:
                        box[unc][1] = value
                    except ValueError:
                        unc, cat = unc.split(self.sep)
                        cats = list(box[unc][0])
                        cats.pop(cats.index(cat))
                        box[unc][:]=set(cats)
                else:
                    try:
                        if (box.dtype.fields[unc][0])==np.int32:
                            value = math.ceil(value)
                        box[unc][0] = value
                    except (ValueError, KeyError):
                        # we are in the right hand branch, so 
                        # the category is included
                        pass
                        
            boxes.append(box) 
        self._boxes = boxes
        return self._boxes       
    
    @property
    def stats(self):
        if self._stats:
            return self._stats
        
        boxes = self.boxes
        
        box_init = sdutil._make_box(self.x)
        
        self._stats = []
        for box in boxes:
            boxstats = self._boxstat_methods[self.mode](self, box, box_init)
            self._stats.append(boxstats)
        return self._stats

    
    def _binary_stats(self, box, box_init):
        indices = sdutil._in_box(self.x, box)
            
        y_in_box = self.y[indices]
        box_coi = np.sum(y_in_box)
        
        boxstats = {'coverage': box_coi/np.sum(self.y),
                    'density': box_coi/y_in_box.shape[0],
                    'res dim':sdutil._determine_nr_restricted_dims(box,
                                                                   box_init),
                    'mass':y_in_box.shape[0]/self.y.shape[0]}
        return boxstats
    
    def _regression_stats(self, box, box_init):
        indices = sdutil._in_box(self.x, box)
            
        y_in_box = self.y[indices]
        
        boxstats = {'mean': np.mean(y_in_box),
                    'mass':y_in_box.shape[0]/self.y.shape[0],
                    'res dim':sdutil._determine_nr_restricted_dims(box,
                                                                   box_init)}
        return boxstats

    
    def _classification_stats(self, box, box_init):
        indices = sdutil._in_box(self.x, box)
            
        y_in_box = self.y[indices]
        classes = set(self.y)
        classes = list(classes)
        classes.sort()
        
        counts = [y_in_box[y_in_box==ci].shape[0] for ci in classes]

        total_gini = 0
        for count in counts:
            total_gini += (count/y_in_box.shape[0])**2
        gini = 1 - total_gini
        
        boxstats = {'gini': gini,
            'mass':y_in_box.shape[0]/self.y.shape[0],
            'box_composition': counts,
            'res dim':sdutil._determine_nr_restricted_dims(box,
                                                           box_init)}
        
        return boxstats

    _boxstat_methods = {sdutil.BINARY:_binary_stats, 
                        sdutil.REGRESSION:_regression_stats,
                        sdutil.CLASSIFICATION: _classification_stats}

    def build_tree(self):
        '''train CART on the data'''
        min_samples = int(self.mass_min*self.x.shape[0])
        
        if self.mode==sdutil.REGRESSION:
            self.clf =  tree.DecisionTreeRegressor(min_samples_leaf=min_samples)
        else:
            self.clf = tree.DecisionTreeClassifier(min_samples_leaf=min_samples)
        self.clf.fit(self._x,self.y)

    def show_tree(self):
        '''return a png of the tree'''
        assert self.clf
        import pydot # dirty hack for read the docs

        dot_data = StringIO() 
        tree.export_graphviz(self.clf, out_file=dot_data, 
                             feature_names=self.feature_names) 
        graph = pydot.graph_from_dot_data(dot_data.getvalue().encode('ascii')) 
        img = graph.create_png()
        return img

       
if __name__ == '__main__':
    from test import test_utilities
    import matplotlib.pyplot as plt

    ema_logging.log_to_stderr(ema_logging.INFO)

    def scarcity_classify(outcomes):
        outcome = outcomes['relative market price']
        change = np.abs(outcome[:, 1::]-outcome[:, 0:-1])
        
        neg_change = np.min(change, axis=1)
        pos_change = np.max(change, axis=1)
        
        logical = (neg_change > -0.6) & (pos_change > 0.6)
        
        classes = np.zeros(outcome.shape[0])
        classes[logical] = 1
        
        return classes
 
    results = test_utilities.load_scarcity_data()
    
    cart = setup_cart(results, scarcity_classify)
    cart.build_tree()
    
    print(cart.boxes_to_dataframe())
    print(cart.stats_to_dataframe())
    cart.display_boxes(together=True)
    
#     img = cart.show_tree()
#      
#     import matplotlib.pyplot as plt
#     import matplotlib.image as mpimg
#   
#     # treat the dot output string as an image file
#     sio = StringIO()
#     sio.write(img)
#     sio.seek(0)
#     img = mpimg.imread(sio)
#       
#     # plot the image
#     imgplot = plt.imshow(img, aspect='equal')
#       
    plt.show()