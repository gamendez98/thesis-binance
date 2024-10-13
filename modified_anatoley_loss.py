import tensorflow as tf


class AnatoleyLoss(tf.keras.losses.Loss):
    def __init__(self, regularization = 1):
        super().__init__()
        self.regularization = regularization

    def call(self, y_true, y_pred_p):
        '''
        returns the anatoley loss defined by:
        A = sum(y_pred_sign[t] * y_true[t] for t in range(T))/T # for the strategic return
        B = sum(y_pred_sign[t] for t in range(T)) * sum(y_true[t] for t in range(T)) / T**2 # for the random return
        :param y_true: price delta at each time step
        :param y_pred_p: probability of buying at each time step
        :return:
        '''
        y_pred_sign = 2 * (y_pred_p - 0.5)
        correlated_return = tf.reduce_mean(tf.multiply(y_pred_sign, y_true))
        uncorrelated_return = tf.reduce_mean(y_pred_sign) * tf.reduce_mean(y_true)

        # Return total loss
        return uncorrelated_return - correlated_return
