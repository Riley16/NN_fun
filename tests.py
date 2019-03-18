from models import *
import numpy as np
import util


# each test returns
# models: a list of models for training
# data_loader: an object for loading and sampling data from test dataset
# runset parameters: n_runs, n_epochs, n_samples, batchsize


# Experimental models with linear targets from
# "Random synaptic feedback weights support error backpropagation for deep learning" (Lillicrap et al)
def linear_target_Lillicrap(units=None, seed=None):
    if seed is not None:
        np.random.seed(seed)

    models = []

    # linear NN model layer sizes from Lillicrap paper
    if units is None:
        in_size = 30
        out_size = 10
        units = (in_size, 20, out_size)
    else:
        in_size = units[0]
        out_size = units[-1]
    layers = len(units)

    # basic GD model
    # unclear what the original hyperparameters used were in Lillicrap paper for the linear target learning task
    # learning rate of 0.005 (true rate unspecified) seems to give performance similar to Lillicrap et al, Fig. 2 (a).
    lilli_GD = LillicrapModel(layers=layers, units=units, weight_init_range=(-0.01, 0.01), lr=0.005, decay_rate=0)
    models.append(lilli_GD)

    # random feedback weight model (Lillicrap et al)
    lilli_randFB = LillicrapModel(layers=layers, units=units, weight_init_range=(-0.01, 0.01), lr=0.005, decay_rate=0,
                                  random_weights=True, randFB_init_range=(-0.5, 0.5))
    models.append(lilli_randFB)

    # runset hyperparameters
    n_samples = 2000
    batch_size = 1

    n_epochs = 1
    n_runs = 20

    def sampler(n_samples):
        # linear target function
        LinFunc = LillicrapModel(layers=layers-1, units=(in_size, out_size), weight_init_range=(-1, 1))
        samples = np.random.multivariate_normal(np.zeros(in_size), np.eye(in_size), n_samples)
        labels = np.array([LinFunc.forward(sample) for sample in samples])
        return samples, labels

    data_loader = util.DataLoader(only_samples=True, sampler=sampler)

    return models, data_loader, n_runs, n_epochs, n_samples, batch_size


def linear_target_BCM(units=None, BCM_decay_rate=1.0, BCM_sat_const = 0.9, seed=None):
    if seed is not None:
        np.random.seed(seed)

    models = []

    # linear NN model layer sizes from Lillicrap paper
    if units is None:
        in_size = 30
        out_size = 10
        units = (in_size, 20, out_size)
    else:
        in_size = units[0]
        out_size = units[-1]
    layers = len(units) - 1

    # basic GD model
    # unclear what the original hyperparameters used were in Lillicrap paper for the linear target learning task
    # learning rate of 0.005 (true rate unspecified) seems to give performance similar to Lillicrap et al, Fig. 2 (a).
    # lilli_GD = LillicrapModel(layers=layers, units=units, weight_init_range=(-0.01, 0.01), lr=0.005, decay_rate=0)
    # models.append(lilli_GD)
    #
    # # random feedback weight model (Lillicrap et al)
    # lilli_randFB = LillicrapModel(layers=layers, units=units, weight_init_range=(-0.01, 0.01), lr=0.005, decay_rate=0,
    #                               random_weights=True, randFB_init_range=(-0.5, 0.5))
    # models.append(lilli_randFB)

    # def __init__(self, layers, units, weight_init_range, nonlins=None,
    #              random_weights=False, randFB_init_range=None,
    #              lr=0.001, decay_rate=1e-06, normalization="NSE", BCM_decay_rate=0.9, BCM_sat_const=1):
    BCM_randFB = BCMModel(layers=layers, units=units, weight_init_range=(-0.01, 0.01), lr=0.005, decay_rate=0,
                                  random_weights=True, randFB_init_range=(-0.5, 0.5),
                          BCM_decay_rate=BCM_decay_rate, BCM_sat_const=BCM_sat_const)
    models.append(BCM_randFB)

    # BCM DECAY RATE IS NOT AN AVERAGE, EXPONENTIAL DECAY CAN BUILD UP TO VALUES LARGER THAN
    # TRUE ERROR AVERAGE, LEADING TO WEAK LEARNING,
    # CORRELATIVE GRADIENTS ARE NOT REFERENCED TO TRUE MEAN OF LOSS, NOT VERY EFFECTIVE, TRY USING
    # BATCH MEAN, ONGOING MEAN WITH NUMBER OF SAMPLES LIKE 1/ROOT(T) RATHER THAN EXPONENTIAL DECAY

    # runset hyperparameters
    n_samples = 2000
    batch_size = 1

    n_epochs = 1
    n_runs = 20

    def sampler(n_samples):
        # linear target function
        LinFunc = LillicrapModel(layers=layers-1, units=(in_size, out_size), weight_init_range=(-1, 1))
        samples = np.random.multivariate_normal(np.zeros(in_size), np.eye(in_size), n_samples)
        labels = np.array([LinFunc.forward(sample) for sample in samples])
        return samples, labels

    data_loader = util.DataLoader(only_samples=True, sampler=sampler)

    return models, data_loader, n_runs, n_epochs, n_samples, batch_size


def linear_target_BCM_pos_weights(units=None, BCM_decay_rate=1.0, BCM_sat_const = 0.9, seed=None):
    if seed is not None:
        np.random.seed(seed)

    models = []

    # linear NN model layer sizes from Lillicrap paper
    if units is None:
        in_size = 30
        out_size = 10
        units = (in_size, 20, out_size)
    else:
        in_size = units[0]
        out_size = units[-1]
    layers = len(units)

    # basic GD model
    # unclear what the original hyperparameters used were in Lillicrap paper for the linear target learning task
    # learning rate of 0.005 (true rate unspecified) seems to give performance similar to Lillicrap et al, Fig. 2 (a).
    # lilli_GD = LillicrapModel(layers=layers, units=units, weight_init_range=(-0.01, 0.01), lr=0.005, decay_rate=0)
    # models.append(lilli_GD)
    #
    # # random feedback weight model (Lillicrap et al)
    # lilli_randFB = LillicrapModel(layers=layers, units=units, weight_init_range=(-0.01, 0.01), lr=0.005, decay_rate=0,
    #                               random_weights=True, randFB_init_range=(-0.5, 0.5))
    # models.append(lilli_randFB)

    # def __init__(self, layers, units, weight_init_range, nonlins=None,
    #              random_weights=False, randFB_init_range=None,
    #              lr=0.001, decay_rate=1e-06, normalization="NSE", BCM_decay_rate=0.9, BCM_sat_const=1):
    BCM_randFB = BCMModel(layers=layers, units=units, weight_init_range=(-0.01, 0.01), lr=0.005, decay_rate=0,
                                  random_weights=True, randFB_init_range=(-0.5, 0.5),
                          BCM_decay_rate=BCM_decay_rate, BCM_sat_const=BCM_sat_const)
    models.append(BCM_randFB)

    # BCM DECAY RATE IS NOT AN AVERAGE, EXPONENTIAL DECAY CAN BUILD UP TO VALUES LARGER THAN
    # TRUE ERROR AVERAGE, LEADING TO WEAK LEARNING,
    # CORRELATIVE GRADIENTS ARE NOT REFERENCED TO TRUE MEAN OF LOSS, NOT VERY EFFECTIVE, TRY USING
    # BATCH MEAN, ONGOING MEAN WITH NUMBER OF SAMPLES LIKE 1/ROOT(T) RATHER THAN EXPONENTIAL DECAY

    # runset hyperparameters
    n_samples = 2000
    batch_size = 1

    n_epochs = 1
    n_runs = 20

    def sampler(n_samples):
        # linear target function
        LinFunc = LillicrapModel(layers=layers-1, units=(in_size, out_size), weight_init_range=(-1, 1))
        samples = np.random.multivariate_normal(np.zeros(in_size), np.eye(in_size), n_samples)
        labels = np.array([LinFunc.forward(sample) for sample in samples])
        return samples, labels

    data_loader = util.DataLoader(only_samples=True, sampler=sampler)

    return models, data_loader, n_runs, n_epochs, n_samples, batch_size


def MNIST_basic(in_size=None, units=None, seed=None):
    # if seed is not None:
    #     np.random.seed(seed)

    models = []

    # MNIST NN model layer sizes from Lillicrap paper
    if in_size is None:
        in_size = 784

    if units is None:
        out_size = 10
        units = (1000, out_size)
    else:
        out_size = units[-1]
    layers = len(units)

    # basic model for MNIST
    omega = 0.1  # 0.175 based on Neural Smithing, pg. 100
    omega_bias = 0.01
    weight_init_range = (-omega, omega)
    bias_init_range = (-omega_bias, omega_bias)
    model = Model(layers=layers, in_size=in_size, units=units,
                  weight_init_range=weight_init_range, bias_init_range=bias_init_range,
                  lr=0.001, decay_rate=1.0e-06, nonlins=['sigmoid', 'sigmoid'], loss="MSE",
                  normalization="NSE")

    """
    LOOK AT MNIST DARK PIXEL VALUES - floats varying between 0 and 1
    WRITE SOMETHING TO DETERMINE WHAT PERCENTAGE OF SIGMOIDS ARE SATURATED
    OR WHETHER THE GRADIENTS ARE VANISHING
    CHECK WEIGHT/bias MAGNITUDES near beginning and ending of training
    TRY SIGNIFICANTLY LARGER WEIGHT INITIALIZATION MAGNITUDES, increase UNTIL SATURATION
    
    test BP on trivial networks, 1 neuron layers, and then MNIST, find mistake in BP, 
    also try hyperparameters from the tutorial, see if my results are significantly off from those
    
    VARY INITIALIZATION RANGES SYSTEMATICALLY
    save weights to pickle file
    """
    # running on full train and test datasets with Lillicrap hyperparameters (batchsize 1, lr 0.001, weights/bias omega 0.01, decay rate 1.0e-06)
    # generalizes terribly (max 1135/10000 correct after one epoch, 1/10000 after that),
    # reaches min NSE on training set of ~0.001 (on some specific epochs) to ~0.15 asymptotically

    # train_size 5000, test_size 1000, lr 0.01, batchsize 10, w/b init omega 0.175
    # generalizes poorly, about same if not worse than above test, NSE reaches 0.1545 with 20 epochs

    # train_size 5000, test_size 1000, lr 0.01, batchsize 10, w/b init omega 0.1
    # generalizes poorly, about same if not worse than above test, NSE reaches 0.1545 with 20 epochs

    # train_size 5000, test_size 1000, lr 0.1, batchsize 10, w/b init omega 0.1
    # generalizes poorly, ~0.10 NSE with 10 epochs

    # train_size 5000, test_size 1000, lr 0.1, batchsize 10, weight init omega 0.1, bias init omega 0.01
    # generalizes poorly asymptotically, but gets 673/1000 after one epoch, ~0.13 NSE with 5 epochs

    # train_size 5000, test_size 1000, lr 1, batchsize 10, weight init omega 0.1, bias init omega 0.01
    # generalizes poorly asymptotically, ~0.5555 NSE constant with 5 epochs

    # train_size 5000, test_size 1000, lr 1, batchsize 10, weight init omega 0.1, bias init omega 0.01, 30 hidden units
    # generalizes poorly asymptotically, gets 809/1000, 0.21 NSE with one epoch, ~0.035 NSE with 20 epochs

    # train_size 5000, test_size 1000, lr 3, batchsize 10, weight init omega 0.1, bias init omega 0.01, 30 hidden units
    # generalizes poorly asymptotically, gets 856/1000, 0.13 NSE with one epoch, ~0.0018 NSE with 20 epochs

    # train_size 50000, test_size 10000, lr 3, batchsize 10, weight init omega 0.1, bias init omega 0.01, 30 hidden units
    # generalizes poorly asymptotically, gets 9332/10000, 0.07 NSE with one epoch, ~0.024 NSE with 20 epochs

    # train_size 50000, test_size 10000, lr 3, batchsize 10, weight init omega 0.1, bias init omega 0.01, 30 hidden units, decay rate of 0 (all previous had 1.0e-06
    # generalizes poorly asymptotically, gets 9360/10000, 0.064 NSE with one epoch, ~0.024 NSE with 20 epochs

    # train_size 50000, test_size 10000, sampled data set in order of download, lr 3, batchsize 10, weight init omega 0.1, bias init omega 0.01, 30 hidden units, decay rate of 0 (all previous had 1.0e-06
    # generalizes poorly asymptotically, gets 9251/10000, 0.11 NSE with one epoch, ~0.0191 NSE with 20 epochs

    models.append(model)
    X_train, y_train_idx, X_test, y_test_idx = util.load_mnist()
    n_samples = 55000
    batch_size = 1
    n_epochs = 20
    n_runs = 1

    n_classes = 10
    train_dataset_size = 55000
    test_dataset_size = 1000

    X_train = X_train[:train_dataset_size]
    y_train_idx = y_train_idx[:train_dataset_size]
    X_test = X_test[:test_dataset_size]
    y_test_idx = y_test_idx[:test_dataset_size]

    # get labels as one-hot vectors
    y_train = np.zeros((train_dataset_size, n_classes))
    y_train[np.arange(train_dataset_size), y_train_idx] = 1

    y_test = np.zeros((test_dataset_size, n_classes))
    y_test[np.arange(test_dataset_size), y_test_idx] = 1

    data_loader = util.DataLoader(examples=X_train, labels=y_train, examples_test=X_test, labels_test=y_test)

    return models, data_loader, n_runs, n_epochs, n_samples, batch_size


def linear_target_basic_GD_model_class_test(in_size=None, units=None, seed=None):
    if seed is not None:
        np.random.seed(seed)

    models = []

    # MNIST NN model layer sizes from Lillicrap paper
    if in_size is None:
        in_size = 30

    if units is None:
        out_size = 10
        units = (20, out_size)
    else:
        out_size = units[-1]
    layers = len(units)

    # basic model for MNIST
    # def __init__(self, layers, in_size, units, weight_init_range, nonlins=None, loss="MSE",
    #              lr=0.001, decay_rate=0, normalization=None, name="Basic NN Model"):
    model = Model(layers=layers, in_size=in_size, units=units, weight_init_range=(-0.01, 0.01),
                  lr=0.005, decay_rate=0, nonlins=['linear', 'linear'], loss="MSE", normalization="NSE")

    models.append(model)

    # random feedback weight model (Lillicrap et al)
    # lilli_randFB = LillicrapModel(layers=layers, units=units, weight_init_range=(-0.01, 0.01), lr=0.005, decay_rate=0,
    #                               random_weights=True, randFB_init_range=(-0.5, 0.5))
    # models.append(lilli_randFB)

    # runset hyperparameters
    n_samples = 2000
    batch_size = 1

    n_epochs = 1
    n_runs = 20

    def sampler(n_samples):
        # linear target function
        LinFunc = LillicrapModel(layers=1, in_size=in_size, units=[out_size], weight_init_range=(-1, 1))
        samples = np.random.multivariate_normal(np.zeros(in_size), np.eye(in_size), n_samples)
        labels = np.squeeze(np.array([LinFunc.forward(sample) for sample in samples]), -1)
        # labels = np.matrix(labels)
        return samples, labels

    data_loader = util.DataLoader(only_samples=True, sampler=sampler)

    return models, data_loader, n_runs, n_epochs, n_samples, batch_size
