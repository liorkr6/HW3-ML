import numpy as np


class conditional_independence():

    def __init__(self):
        # You need to fill the None value with *valid* probabilities
        self.X = {0: 0.3, 1: 0.7}  # P(X=x)
        self.Y = {0: 0.3, 1: 0.7}  # P(Y=y)
        self.C = {0: 0.5, 1: 0.5}  # P(C=c)

        self.X_Y = {
            (0, 0): round(self.X[0] * self.Y[0], 1),
            (0, 1): round(self.X[0] * self.Y[1], 1),
            (1, 0): round(self.X[1] * self.Y[0], 1),
            (1, 1): round(self.X[1] * self.Y[1], 1)
        }  # P(X=x, Y=y)

        self.X_C = {
            (0, 0): round(self.X[0] * self.C[0], 1),
            (0, 1): round(self.X[0] * self.C[1], 1),
            (1, 0): round(self.X[1] * self.C[0], 1),
            (1, 1): round(self.X[1] * self.C[1], 1)
        }  # P(X=x, C=y)

        self.Y_C = {
            (0, 0): round(self.Y[0] * self.C[0], 1),
            (0, 1): round(self.Y[0] * self.C[1], 1),
            (1, 0): round(self.Y[1] * self.C[0], 1),
            (1, 1): round(self.Y[1] * self.C[1], 1)
        }  # P(Y=y, C=c)

        self.X_Y_C = {
            (0, 0, 0): self.X[0] * self.Y[0] * self.C[0],
            (0, 0, 1): self.X[0] * self.Y[0] * self.C[1],
            (0, 1, 0): self.X[0] * self.Y[1] * self.C[0],
            (0, 1, 1): self.X[0] * self.Y[1] * self.C[1],
            (1, 0, 0): self.X[1] * self.Y[0] * self.C[0],
            (1, 0, 1): self.X[1] * self.Y[0] * self.C[1],
            (1, 1, 0): self.X[1] * self.Y[1] * self.C[0],
            (1, 1, 1): self.X[1] * self.Y[1] * self.C[1]
        }  # P(X=x, Y=y, C=c)

    def is_X_Y_dependent(self):
        """
        return True iff X and Y are depndendent
        """
        X = self.X
        Y = self.Y
        X_Y = self.X_Y

        x_probabilities, y_probabilities = np.array(list(X.values())), np.array(list(Y.values()))
        multiplications_x_y = np.array(np.concatenate(np.outer(x_probabilities, y_probabilities)))
        x_y_probabilities = np.array(list(X_Y.values()))
        print(x_y_probabilities, multiplications_x_y)
        comparison = np.isclose(x_y_probabilities, multiplications_x_y)
        if comparison.all():
            return False
        else:
            return True

    def is_X_Y_given_C_independent(self):
        """
        return True iff X_given_C and Y_given_C are indepndendent
        """
        X = self.X
        Y = self.Y
        C = self.C
        X_C = self.X_C
        Y_C = self.Y_C
        X_Y_C = self.X_Y_C

        x_c_probabilities = np.array(list(X_C.values())*2)
        y_c_probabilities = np.array(list(Y_C.values())*2)
        x_y_c_multiplication = x_c_probabilities * y_c_probabilities
        x_y_c_probabilities = np.array(list(X_Y_C.values()))
        independent = np.isclose(x_y_c_probabilities , x_y_c_multiplication)
        if independent.any() == False:
            return False
        
        
        return True
        pass

def poisson_log_pmf(k, rate):
    """
    k: A discrete instance
    rate: poisson rate parameter (lambda)

    return the log pmf value for instance k given the rate
    """
    log_p = np.log(np.power(rate,k)*(np.power(np.e,-rate))/(np.math.factorial(k)))
    return log_p


def get_poisson_log_likelihoods(samples, rates):
    """
    samples: set of univariate discrete observations
    rates: an iterable of rates to calculate log-likelihood by.

    return: 1d numpy array, where each value represent that log-likelihood value of rates[i]
    """
    likelihoods = []

    for i in range (len(rates)):
        samples_sum = 0
        for j in range (len(samples)):
            samples_sum += poisson_log_pmf(samples[j], rates[i])
        likelihoods.append(samples_sum)

    return likelihoods


def possion_iterative_mle(samples, rates):
    """
    samples: set of univariate discrete observations
    rate: a rate to calculate log-likelihood by.

    return: the rate that maximizes the likelihood 
    """
    rate = 0.0
    likelihoods = get_poisson_log_likelihoods(samples, rates)  # might help
    max_likelihood = likelihoods[0]
    for i in range (len(rates)):
        if likelihoods[i] > max_likelihood:
            max_likelihood = likelihoods[i]
            rate = rates[i]
    return rate


def possion_analytic_mle(samples):
    """
    samples: set of univariate discrete observations

    return: the rate that maximizes the likelihood
    """
    mean = np.mean(samples)
    return mean


def normal_pdf(x, mean, std):
    """
    Calculate normal density function for a given x, mean and standard deviation.
 
    Input:
    - x: A value we want to compute the distribution for.
    - mean: The mean value of the distribution.
    - std:  The standard deviation of the distribution.
 
    Returns the normal distribution pdf according to the given mean and std for the given x.    
    """

    # var = float(std)**2
    # denom = (2*np.math.pi*var)**.5
    # num = np.math.exp(-(float(x)-float(mean))**2/(2*var))
    return (np.pi*std) * np.exp(-0.5*((x-mean)/std)**2)


class NaiveNormalClassDistribution():
    def __init__(self, dataset, class_value):
        """
        A class which encapsulates the relevant parameters(mean, std) for a class conditinoal normal distribution.
        The mean and std are computed from a given data set.
        
        Input
        - dataset: The dataset as a 2d numpy array, assuming the class label is the last column
        - class_value : The class to calculate the parameters for.
        """
        self.dataset = dataset
        self.samples = dataset[dataset[:,-1]==class_value][:,0:2]
        self.mean = np.mean(self.samples, axis=0)
        self.std = np.std(self.samples,axis=0)

    def get_prior(self):
        """
        Returns the prior probability of the class according to the dataset distribution.
        """
        prior = self.samples.shape[0]/self.dataset.shape[0]
        return prior

    def get_instance_likelihood(self, x):
        """
        Returns the likelihood probability of the instance under the class according to the dataset distribution.
        """
        likelihood = np.prod([normal_pdf(feature, self.mean, self.std) for feature in x[0:2]])
        return likelihood

    def get_instance_posterior(self, x):
        """
        Returns the posterior probability of the instance under the class according to the dataset distribution.
        * Ignoring p(x)
        """
        posterior = self.get_prior() * self.get_instance_likelihood(x)
        return posterior


class MAPClassifier():
    def __init__(self, ccd0, ccd1):
        """
        A Maximum a posteriori classifier. 
        This class will hold 2 class distributions. 
        One for class 0 and one for class 1, and will predict an instance
        using the class that outputs the highest posterior probability 
        for the given instance.
    
        Input
            - ccd0 : An object contating the relevant parameters and methods 
                     for the distribution of class 0.
            - ccd1 : An object contating the relevant parameters and methods 
                     for the distribution of class 1.
        """
        self.ccd0 = ccd0
        self.ccd1 = ccd1

    def predict(self, x):
        """
        Predicts the instance class using the 2 distribution objects given in the object constructor.
    
        Input
            - An instance to predict.
        Output
            - 0 if the posterior probability of class 0 is higher and 1 otherwise.
        """
        pred = 0 if self.ccd0.get_instance_posterior(x) > self.ccd1.get_instance_posterior(x) else 1
        return pred


def compute_accuracy(test_set, map_classifier):
    """
    Compute the accuracy of a given a test_set using a MAP classifier object.
    
    Input
        - test_set: The test_set for which to compute the accuracy (Numpy array). where the class label is the last column
        - map_classifier : A MAPClassifier object capable of predicting the class for each instance in the testset.
        
    Ouput
        - Accuracy = #Correctly Classified / test_set size
    """
    predictions = [map_classifier.predict(test_set[i,:]) for i in range(test_set.shape[0])]
    correct_predictions = 0
    for (idx, pred) in enumerate(predictions):
        if pred == test_set[idx, -1]:
            correct_predictions += 1

    return correct_predictions/test_set.shape[0]



def multi_normal_pdf(x, mean, cov):
    """
    Calculate multi variable normal desnity function for a given x, mean and covarince matrix.
 
    Input:
    - x: A value we want to compute the distribution for.
    - mean: The mean vector of the distribution.
    - cov:  The covariance matrix of the distribution.
 
    Returns the normal distribution pdf according to the given mean and var for the given x.    
    """
    d = mean.shape[0]
    det_cov = (np.linalg.det(cov)**(-0.5))
    inverse_cov = np.linalg.inv(cov)
    pdf = ((2*np.pi)**(-d/2))*det_cov*np.e**((np.transpose(x - mean).dot(inverse_cov).dot(x - mean))*-0.5)
    return pdf


class MultiNormalClassDistribution():

    def __init__(self, dataset, class_value):
        """
        A class which encapsulate the relevant parameters(mean, cov matrix) for a class conditinoal multi normal distribution.
        The mean and cov matrix (You can use np.cov for this!) will be computed from a given data set.
        
        Input
        - dataset: The dataset as a numpy array
        - class_value : The class to calculate the parameters for.
        """
        self.dataset = dataset
        self.samples = dataset[dataset[:,-1]==class_value][:,0:2]
        self.cov = np.cov(self.samples,rowvar=False, bias=True)
        self.mean = np.mean(self.samples, axis=0)

    def get_prior(self):
        """
        Returns the prior porbability of the class according to the dataset distribution.
        """
        prior = self.samples.shape[0]/self.dataset.shape[0]
        return prior

    def get_instance_likelihood(self, x):
        """
        Returns the likelihood of the instance under the class according to the dataset distribution.
        """
        likelihood = multi_normal_pdf(x[0:2], self.mean, self.cov)
        return likelihood

    def get_instance_posterior(self, x):
        """
        Returns the posterior porbability of the instance under the class according to the dataset distribution.
        * Ignoring p(x)
        """
        posterior = self.get_prior() * self.get_instance_likelihood(x)
        return posterior


class MaxPrior():
    def __init__(self, ccd0, ccd1):
        """
        A Maximum prior classifier. 
        This class will hold 2 class distributions, one for class 0 and one for class 1, and will predicit an instance
        by the class that outputs the highest prior probability for the given instance.
    
        Input
            - ccd0 : An object contating the relevant parameters and methods for the distribution of class 0.
            - ccd1 : An object contating the relevant parameters and methods for the distribution of class 1.
        """
        self.ccd0 = ccd0
        self.ccd1 = ccd1

    def predict(self, x):
        """
        Predicts the instance class using the 2 distribution objects given in the object constructor.
    
        Input
            - An instance to predict.
        Output
            - 0 if the posterior probability of class 0 is higher and 1 otherwise.
        """
        pred = 0 if self.ccd0.get_prior() > self.ccd1.get_prior() else 1
        return pred


class MaxLikelihood():
    def __init__(self, ccd0, ccd1):
        """
        A Maximum Likelihood classifier. 
        This class will hold 2 class distributions, one for class 0 and one for class 1, and will predicit an instance
        by the class that outputs the highest likelihood probability for the given instance.
    
        Input
            - ccd0 : An object contating the relevant parameters and methods for the distribution of class 0.
            - ccd1 : An object contating the relevant parameters and methods for the distribution of class 1.
        """
        self.ccd0 = ccd0
        self.ccd1 = ccd1

    def predict(self, x):
        """
        Predicts the instance class using the 2 distribution objects given in the object constructor.
    
        Input
            - An instance to predict.
        Output
            - 0 if the posterior probability of class 0 is higher and 1 otherwise.
        """
        pred = 0 if self.ccd0.get_instance_likelihood(x) > self.ccd1.get_instance_likelihood(x) else 1
        return pred


EPSILLON = 1e-6  # if a certain value only occurs in the test set, the probability for that value will be EPSILLON.


class DiscreteNBClassDistribution():
    def __init__(self, dataset, class_value):
        """
        A class which computes and encapsulate the relevant probabilites for a discrete naive bayes 
        distribution for a specific class. The probabilites are computed with laplace smoothing.
        
        Input
        - dataset: The dataset as a numpy array.
        - class_value: Compute the relevant parameters only for instances from the given class.
        """
        self.dataset = dataset
        self.samples = dataset[dataset[:,-1]==class_value][:,0:-1]

    def get_prior(self):
        """
        Returns the prior porbability of the class 
        according to the dataset distribution.
        """
        prior = self.samples.shape[0]/self.dataset.shape[0]
        return prior

    def get_instance_likelihood(self, x):
        """
        Returns the likelihood of the instance uder 
        the class according to the dataset distribution.
        """
        likelihood = 1
        for i in range(x.shape[0]-1):
            Nij = self.samples[self.samples[:,i]==x[i]].shape[0] # num of instances of class_value with the same value as x for feature i
            Vj = len(np.unique(self.samples[:,i]))
            Ni = self.samples.shape[0]
            probability = (Nij + 1) / (Ni + Vj)
            likelihood *= probability
        return likelihood

    def get_instance_posterior(self, x):
        """
        Returns the posterior porbability of the instance 
        under the class according to the dataset distribution.
        * Ignoring p(x)
        """
        posterior = self.get_prior() * self.get_instance_likelihood(x)
        return posterior


class MAPClassifier_DNB():
    def __init__(self, ccd0, ccd1):
        """
        A Maximum a posteriori classifier. 
        This class will hold 2 class distributions, one for class 0 and one for class 1, and will predict an instance
        by the class that outputs the highest posterior probability for the given instance.
    
        Input
            - ccd0 : An object contating the relevant parameters and methods for the distribution of class 0.
            - ccd1 : An object contating the relevant parameters and methods for the distribution of class 1.
        """
        self.ccd0 = ccd0
        self.ccd1 = ccd1

    def predict(self, x):
        """
        Predicts the instance class using the 2 distribution objects given in the object constructor.
    
        Input
            - An instance to predict.
        Output
            - 0 if the posterior probability of class 0 is higher and 1 otherwise.
        """
        pred = 0 if self.ccd0.get_instance_posterior(x) > self.ccd1.get_instance_posterior(x) else 1
        return pred

    def compute_accuracy(self, test_set):
        """
        Compute the accuracy of a given a testset using a MAP classifier object.

        Input
            - test_set: The test_set for which to compute the accuracy (Numpy array).
        Ouput
            - Accuracy = #Correctly Classified / #test_set size
        """
        predictions = [self.predict(test_set[i,:]) for i in range(test_set.shape[0])]
        correct_predictions = 0
        for (idx, pred) in enumerate(predictions):
            if pred == test_set[idx, -1]:
                correct_predictions += 1

        return correct_predictions/test_set.shape[0]
