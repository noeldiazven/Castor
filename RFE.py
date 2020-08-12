##################################################################
# Authors: Alexandre Gramfort <alexandre.gramfort@inria.fr>      # 
#          Vincent Michel <vincent.michel@inria.fr>              #
#          Gilles Louppe <g.louppe@gmail.com>                    #
#                                                                #
# Modified by Dylan Lebatteux <lebatteux.dylan@courrier.uqam.ca> #
#                                                                #
# License: BSD 3 clause                                          #
##################################################################

# Imports
import numpy as np
from sklearn.base import clone
from sklearn.utils import safe_sqr
from sklearn.metrics import f1_score
from sklearn.base import BaseEstimator
from sklearn.base import is_classifier
from sklearn.metrics import check_scoring
from sklearn.base import MetaEstimatorMixin
from sklearn.model_selection import check_cv
from sklearn.utils.metaestimators import _safe_split
from sklearn.utils.validation import check_is_fitted
from sklearn.model_selection._validation import _score
from joblib import Parallel, delayed, effective_n_jobs
from sklearn.feature_selection.base import SelectorMixin
from sklearn.utils.metaestimators import if_delegate_has_method
from sklearn.utils.validation import _deprecate_positional_args

def _rfe_single_fit(rfe, estimator, X, y, train, test, scorer):
	X_train, y_train = _safe_split(estimator, X, y, train)
	X_test, y_test = _safe_split(estimator, X, y, test, train)
	return rfe._fit(X_train, y_train, lambda estimator, features: _score(estimator, X_test[:, features], y_test, scorer)).scores_

class RFE(SelectorMixin, MetaEstimatorMixin, BaseEstimator):
	@_deprecate_positional_args
	def __init__(self, estimator, *, n_features_to_select=None, step=1, verbose=0):
		self.supports = []
		self.estimator = estimator
		self.n_features_to_select = n_features_to_select
		self.step = step
		self.verbose = verbose

	@property
	def _estimator_type(self): return self.estimator._estimator_type

	@property
	def classes_(self): return self.estimator_.classes_

	def fit(self, X, y): return self._fit(X, y)

	def _fit(self, X, y, step_score=None):
		tags = self._get_tags()
		X, y = self._validate_data(X, y, accept_sparse="csc",ensure_min_features=2, force_all_finite=not tags.get('allow_nan', True),multi_output=True)

		# Inicialización
		n_features = X.shape[1]
		if self.n_features_to_select is None: n_features_to_select = n_features // 2
		else: n_features_to_select = self.n_features_to_select

		if 0.0 < self.step < 1.0: step = int(max(1, self.step * n_features))
		else: step = int(self.step)
		if step <= 0: raise ValueError("Step must be >0")

		support_ = np.ones(n_features, dtype=np.bool)
		ranking_ = np.ones(n_features, dtype=np.int)

		if step_score: self.scores_ = []

		# Eliminación
		while np.sum(support_) > n_features_to_select:
			# Features restantes
			features = np.arange(n_features)[support_]

			# Clasifique las características restantes
			estimator = clone(self.estimator)
			if self.verbose > 0: print("Fitting estimator with %d features." % np.sum(support_))

			# Ajuste
			estimator.fit(X[:, features], y)

         # Obtener coefs
			if hasattr(estimator, 'coef_'): coefs = estimator.coef_
			else: coefs = getattr(estimator, 'feature_importances_', None)
			if coefs is None: raise RuntimeError("The classifier does not expose coef_or feature_importances_attributes")

			# Obtener rangos
			if coefs.ndim > 1: ranks = np.argsort(safe_sqr(coefs).sum(axis=0))
			else: ranks = np.argsort(safe_sqr(coefs))

			# Para rangos de casos dispersos es matriz
			ranks = np.ravel(ranks)

			# Elimina las peores características
			threshold = min(step, np.sum(support_) - n_features_to_select)

			# Guardar soporte de características seleccionadas
			self.supports.append(list(support_))

			# Calcule el puntaje de paso en la iteración de selección anterior porque el 'estimador' debe usar características que aún no se han eliminado
			if step_score: self.scores_.append(step_score(estimator, features))
			support_[features[ranks][:threshold]] = False
			ranking_[np.logical_not(support_)] += 1
		
		# Establecer atributos finales
		features = np.arange(n_features)[support_]
		self.estimator_ = clone(self.estimator)
		self.estimator_.fit(X[:, features], y)

		# Calcule la puntuación por pasos cuando solo quedan n características para seleccionar características
		if step_score: self.scores_.append(step_score(self.estimator_, features))
		self.n_features_ = support_.sum()
		self.support_ = support_
		self.ranking_ = ranking_

		# Guardar soporte de características seleccionadas
		self.supports.append(list(support_))

		return self

	@if_delegate_has_method(delegate='estimator')
	def predict(self, X):
		check_is_fitted(self)
		return self.estimator_.predict(self.transform(X))

	@if_delegate_has_method(delegate='estimator')
	def score(self, X, y):
		check_is_fitted(self)
		return self.estimator_.score(self.transform(X), y)

	def _get_support_mask(self):
		check_is_fitted(self)
		return self.support_

	@if_delegate_has_method(delegate='estimator')
	def decision_function(self, X):
		check_is_fitted(self)
		return self.estimator_.decision_function(self.transform(X))

	@if_delegate_has_method(delegate='estimator')
	def predict_proba(self, X):
		check_is_fitted(self)
		return self.estimator_.predict_proba(self.transform(X))

	@if_delegate_has_method(delegate='estimator')
	def predict_log_proba(self, X):
		check_is_fitted(self)
		return self.estimator_.predict_log_proba(self.transform(X))

	def _more_tags(self):
		estimator_tags = self.estimator._get_tags()
		return {'poor_score': True, 'allow_nan': estimator_tags.get('allow_nan', True), 'requires_y': True,}

