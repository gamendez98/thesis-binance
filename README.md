# TODO

- Train MOE-TS with MSE
- try other losses


# Research questions

here are some of the questions to be answered with this experiments

### Dataset

we are using F1-2010 benchmark dataset, it is available [here](https://etsin.fairdata.fi/dataset/73eb48d7-4dbc-4a10-a52a-da745b47a649/data)

### Anatoley-Gerko as a regularized loss function

In the unnormalized anatoley-gerko loss `L = C * B - A` is the B term a form of regularization?

what happens when `C >> 1` and when `C << 1`

### Loss comparison

How does AG-loss compare with cross-entropy and weighted cross-entropy

# Concepts

### Order

Order `o = (e, p, v, t)`

e = Direction = {+1 for buy and -1 for sell}
p = price (it is discrete)
v = volume (number of assets)
t = time

L_r = L + R()

# Data sources

### Binance

- T (transaction time): It's the last time at which the orderbook was updated
- E (event time / message out time): is T + server side latency
- lastUpdateId: The last ID updated in the request. It is sequential, meaning that it can be used to find how many
updates happened between two fetches

### Directional Losses

- Directional mae: https://www.sciencedirect.com/science/article/pii/S1877750324001686?via%3Dihub


