"""
Chapitre 11.2
"""


import numbers
import copy
import collections
import collections.abc
from typing import Tuple


class Matrix:
	"""
	Matrice numérique stockée en tableau 1D en format rangée-major.

	:param height: La hauteur (nb de rangées)
	:param width: La largeur (nb de colonnes)
	:param data: Si une liste, alors les données elles-mêmes (affectées, pas copiées). Si un nombre, alors la valeur de remplissage
	"""

	def __init__(self, height, width, data = 0.0):
		if not isinstance(height, numbers.Integral) or not isinstance(width, numbers.Integral):
			raise TypeError()
		if height == 0 or width == 0:
			raise ValueError(numbers.Integral)
		self.__height = height
		self.__width = width
		if isinstance(data, list):
			if len(data) != len(self):
				raise ValueError(list)
			self.__data = data
		elif isinstance(data, numbers.Number):
			self.__data = [data for i in range(len(self))]
		else:
			raise TypeError()

	@property
	def height(self):
		return self.__height

	@property
	def width(self):
		return self.__width

	@property
	def data(self):
		return self.__data

	# TODO: Accès à un élément en lecture
	def __getitem__(self, indexes:tuple):
		"""
		Indexation rangée-major

		:param indexes: Les index en `tuple` (rangée, colonne)
		"""

		if not isinstance(indexes, tuple):
			raise IndexError()
		if indexes[0] >= self.height or indexes[1] >= self.width:
			raise IndexError()
		return copy.deepcopy(self.data[indexes[0]*self.width+indexes[1]])

	# TODO: Affectation à un élément
	def __setitem__(self, indexes:tuple, value):
		"""
		Indexation rangée-major

		:param indexes: Les index en `tuple` (rangée, colonne)
		"""
		if not isinstance(indexes, tuple):
			raise IndexError()
		if indexes[0] >= self.height or indexes[1] >= self.width:
			raise IndexError()
		self.data[indexes[0]*self.width+indexes[1]] = value

	def __len__(self):
		"""
		Nombre total d'éléments
		"""
		return self.height * self.width

	def __str__(self):
		return format(self, "")

	def __repr__(self):
		return f"Matrix({self.height}, {self.width}, {self.data.__repr__()})"

	def __format__(self,frmt):
		prt=""
		for i, elem in enumerate(self.data):
			prt+=str(format(elem, frmt))+" "
			if (i+1)%self.width==0:
				prt+="\n"
		return prt

	def clone(self):
		return Matrix(self.height, self.width, self.data)

	def copy(self):
		return Matrix(self.height, self.width, copy.deepcopy(self.data))

	def has_same_dimensions(self, other):
		return (self.height, self.width) == (other.height, other.width)

	def __pos__(self):
		return self.copy()

	def __neg__(self):
		return Matrix(self.height, self.width, [-e for e in self.data])

	def __add__(self, other):
		if self.has_same_dimensions(other):
			return Matrix(self.height, self.width, [self.data[i]+other.data[i] for i in range(len(self.data))])

	def __sub__(self, other):
		return self + (-other)

	def __mul__(self, other):
		if isinstance(other, Matrix):
			if self.width == other.height:
				result = Matrix(self.height, other.width, 0)

				for i in range(self.height):
					for j in range(other.width):
						for k in range(self.width):
							result[i, j] = self[i, k] * other[k, j]
				return result
		elif isinstance(other, numbers.Number):
			return Matrix(self.height, self.width, [other*e for e in self.data])
		else:
			raise TypeError()

	def __rmul__(self,other):
		return self*other

	def __abs__(self):
		return Matrix(self.height, self.width, [abs(e) for e in self.data])

	def __eq__(self,other):
		return (self.width,self.height,self.data)==(other.width, other.height, other.data)

	@classmethod
	def identity(cls, width):
		result = cls(width, width)
		for i in range(width):
			result[i, i] = 1.0
		return result

