import numpy as np
from sklearn.metrics import precision_recall_fscore_support

def compute_detection_metrics(y_true_counts, y_pred_counts):
    # simple aggregate metrics across images
    y_true = np.array(y_true_counts)
    y_pred = np.array(y_pred_counts)
    # treat counts as a regression proxy; compute precision/recall by thresholding presence
    y_true_bin = (y_true > 0).astype(int)
    y_pred_bin = (y_pred > 0).astype(int)
    p, r, f, _ = precision_recall_fscore_support(y_true_bin, y_pred_bin, average='binary', zero_division=0)
    return {"precision": float(p), "recall": float(r), "f1": float(f)}
