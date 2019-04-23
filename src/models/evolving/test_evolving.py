from sklearn import preprocessing
from evolving import EvolvingClustering, load_dataset, Metrics, util
import matplotlib.pyplot as plt
import pickle

cmap = plt.cm.get_cmap('rainbow')

X, y = load_dataset.load_dataset("s2")
standardized_X = preprocessing.scale(X)
minmaxscaler = preprocessing.MinMaxScaler()
minmaxscaler.fit(standardized_X)
X = minmaxscaler.transform(standardized_X)

## Running training and prediction..
evol_model = EvolvingClustering.EvolvingClustering(variance_limit=0.01, debug=True)
evol_model.fit(X)
y_pred = evol_model.predict(X)

pickle.dump(evol_model, open("evol_model.pkl", "wb"))
## END Running training and prediction..

## Load pickle
# evol_model = pickle.load(open("evol_model.pkl", "rb"))
# y_pred = evol_model.labels_
## END Load pickle

y_pred = [x+1 for x in y_pred]

y_pred = util.adjust_labels(y_pred, y)

util.plot_macro_clusters(X, evol_model)

print("Purity: %10.4f"% (Metrics.purity(y,y_pred)))
print("Precision: %10.4f"% (Metrics.precision(y,y_pred)))
print("Recall: %10.4f"% (Metrics.recall(y,y_pred)))
print("CH Score: %10.4f"% (Metrics.ch_score(y,y_pred)))


