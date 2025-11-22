from sklearn.metrics import (
    classification_report, confusion_matrix,
    roc_auc_score, roc_curve, precision_recall_curve,
    average_precision_score, cohen_kappa_score
)
import matplotlib.pyplot as plt

class ClassificationEvaluator:
    def __init__(self, y_true, y_pred, y_proba=None):
        self.y_true = y_true
        self.y_pred = y_pred
        self.y_proba = y_proba

    def compute_all_metrics(self):
        """Calculate comprehensive classification metrics"""
        metrics = {}

        # Classification report
        report = classification_report(
            self.y_true, self.y_pred, output_dict=True
        )
        metrics['precision'] = report['1']['precision']
        metrics['recall'] = report['1']['recall']
        metrics['f1'] = report['1']['f1-score']
        metrics['accuracy'] = report['accuracy']

        # Confusion matrix
        cm = confusion_matrix(self.y_true, self.y_pred)
        tn, fp, fn, tp = cm.ravel()

        metrics['confusion_matrix'] = {
            'tn': tn, 'fp': fp, 'fn': fn, 'tp': tp
        }

        # Specificity and sensitivity
        metrics['specificity'] = tn / (tn + fp)
        metrics['sensitivity'] = tp / (tp + fn)

        # Cohen's Kappa
        metrics['cohen_kappa'] = cohen_kappa_score(
            self.y_true, self.y_pred
        )

        if self.y_proba is not None:
            # AUC-ROC
            metrics['auc_roc'] = roc_auc_score(
                self.y_true, self.y_proba
            )

            # AUC-PR
            metrics['auc_pr'] = average_precision_score(
                self.y_true, self.y_proba
            )

        return metrics

    def plot_curves(self):
        """Plot ROC and Precision-Recall curves"""
        if self.y_proba is None:
            return

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        # ROC Curve
        fpr, tpr, _ = roc_curve(self.y_true, self.y_proba)
        auc_roc = roc_auc_score(self.y_true, self.y_proba)
        ax1.plot(fpr, tpr, label=f'AUC-ROC = {auc_roc:.3f}')
        ax1.plot([0, 1], [0, 1], 'k--', label='Random')
        ax1.set_xlabel('False Positive Rate')
        ax1.set_ylabel('True Positive Rate')
        ax1.set_title('ROC Curve')
        ax1.legend()

        # Precision-Recall Curve
        precision, recall, _ = precision_recall_curve(
            self.y_true, self.y_proba
        )
        auc_pr = average_precision_score(self.y_true, self.y_proba)
        ax2.plot(recall, precision, label=f'AUC-PR = {auc_pr:.3f}')
        ax2.set_xlabel('Recall')
        ax2.set_ylabel('Precision')
        ax2.set_title('Precision-Recall Curve')
        ax2.legend()

        plt.tight_layout()
        return fig