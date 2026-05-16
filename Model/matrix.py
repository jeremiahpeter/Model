import math
import copy
from xml.dom.minidom import ReadOnlySequentialNamedNodeMap

class matrixError(Exception) :
	def __init__ (self, num) :
		if num == 1 :
			raise KeyError("Unsquare matrix")
		elif num == 2 :
			raise KeyError("Modified column exceeds current matrix size (proposed solution: turn on column override)")
		elif num == 3 :
			raise KeyError("Modified row exceeds current matrix size (proposed solution: turn on row override)")
		elif num == 4 :
			raise KeyError("Attempted to delete a row that doesn't exist")
		elif num == 5 :
			raise KeyError("Attempted to delete a column that doesn't exist")
		elif num == 6 :
			raise KeyError("not all columns or rows have the same size")
		elif num == 7 :
			raise KeyError("Attempted to delete a row that doesn't exist: ")
		elif num == 8 :
			raise KeyError("Attempted to delete a column that doesn't exist: ")
		elif num == 9 :
			raise TypeError("Attempted to multiply non matrix (Dissapointed) ")
		elif num == 10 :
			raise TypeError("number of columns of first matrix to not match number of rows of second matrix")




def defaulted_matrix (rows, columns) :
	row = [0] * rows
	return  [[0] * rows for I in range(columns)]

class matrix :

	def __init__ (self, rows=0, columns=0, content=[]) :
		self.rows = rows 
		self.columns = columns 
		self.content = content 
		self.eigenvals = None 

		if self.rows == 0 and self.columns == 0 and self.content != [] :
			self.columns = len(self.content)
			self.rows = len(self.content[0] )
		
		#initiates matrix :
		self.content = self.defaulted_matrix()



		
	#creates an empty matrix of the correct sizes
	def defaulted_matrix (self) :
		row = [0] * self.rows
		return  [[0] * self.rows for I in range(self.columns)]

	#for use with pre-initiated lists/matrices
	def overwrite_matrix(self, double_list_input) :
		for X in range(len(double_list_input)) :
			for Y in range(len(double_list_input[X])) :
				self.content[X][Y] = double_list_input[X][Y]
		self.eigenvals = None 

	
	#creates a seperate list, does not edit content of self
	def transpose(self) :
		return_matrix = self.default
		for X in range(len(self.content)) :
			for Y in range(len(self.content[X])):
				return_matrix[Y][X] = self.content[X][Y]
		self.eigenvals = None 
		return return_matrix

	#position starts indexing at 0, be aware, position can be a list, in which case each index in list will have a row added
	#also, I'm sorry for making you try to read this
	def add_row (self, position, num_rows=1) :			 
		# iterates through a list to insert at each listed index
		if isinstance(position, list) :
			for pos in position :
				for Y in range(len(self.content)) :
					for I in range(pos, pos + num_rows) :
						self.content[Y].insert(I, 0)
		

		#default for single index
		if isinstance(position, int) :
			for Y in range(len(self.content)) :
				for I in range(position, position + num_rows) :
					self.content[Y].insert(I, 0)

		self.rows = len(self.content[0])
		self.columns = len(self.content)
		self.eigenvals = None 


	#adds columns at specified indexes
	def add_column (self, position, num_col=1) : 
		#creates the empty columns
		if isinstance(position, list):
			for I in position:
				for X in range(I, I + num_col):
					self.content.insert(X, [0] * self.rows)  # fresh list each time
		else:
			for I in range(position, position + num_col):
				self.content.insert(I, [0] * self.rows)      # fresh list each time

		self.rows = len(self.content[0])
		self.columns = len(self.content)
		self.eigenvals = None 


	#makes in a new row input into a row
	def edit_row (self, position, new_row, do_row_override=True, do_column_override=True) :

		position = position -1
		#ensures there are enough columns
		if len(self.content) < len(new_row) :

			if do_column_override == False: 
				matrixError(2)
			if do_column_override == True :
				excess_columns = len(new_row) - len(self.content)
				self.add_column(self.columns, excess_columns)

		#ensures there are enough rows
		if len(self.content[1]) < position :
			if do_row_override == False :
				matrixError(3)
			if do_row_override == True :
				excess_rows = position - len(self.content[0])
				self.add_row(len(self.content[0]), excess_rows)

		self.rows = len(self.content[0]) 
		self.columns = len(self.content) 


		for I in range(len(new_row)) :
			self.content[I][position] = new_row[I]
		self.eigenvals = None 

		

	#at this point you have to understand what's happening
	def edit_column (self, position, new_column, do_row_override=True, do_column_override=True) :

		position = position -1

		#ensures there are enough rows
		if len(self.content[1]) < len(new_column) :

			if do_row_override == False :
				matrixError(3)

			if do_row_override == True :
				excess_rows = len(new_column) - len(self.content[1])
				self.add_row(len(self.content[1]), num_rows=excess_rows) 

		#ensures there are enough columns 
		if len(self.content) < position : 
			if do_column_override == False: 
				matrixError(2)
			if do_column_override == True :
				needed_cols = position - len(self.content)
				self.add_column(len(self.content), needed_cols)

		self.content[position] = new_column

		self.rows = len(self.content[0])
		self.columns = len(self.content)
		self.eigenvals = None 


	def update_sizes (self, do_consistency_check=True) :

		#compares the length of all rows against the first row to make sure they all match
		if do_consistency_check == True : 
			expected_row_length = len(self.content[0])
			for I in range(len(self.content)) :
				if len(self.content[I]) != expected_row_length :
					matrixError(6)
		
		self.rows = len(self.content[0])
		self.columns = len(self.content)


	def delete_row(self, rows) :
		if isinstance(rows, list) : 
			for I in rows: 
				if (I -1) not in range(len(self.content[0])) :
					rows.remove(I)

			
			for row in rows :
				for (I) in range(len(self.content)) : 
					self.content[I].pop(row - 1)

		else: 
			if rows not in range(len(self.content[0])) :
				matrixError(7)
			else: 
				for I in range(len(self.content)) :
					self.content[I].pop(rows -1)

		self.rows = len(self.content[0])
		self.columns = len(self.content)
		self.eigenvals = None 

	
	def delete_column (self, column) :
		
		if isinstance(column, list) :
			for I in column :
				if I - 1 not in range(len(self.content)) :
					print(f"Attempted to delete a column that doesn't exist: {I}")
					column = column.remove(I)

		else: 
			if column -1 not in range(len(self.content)) :
				matrixError(8) 
			else: 
				self.content.pop(column - 1)

		self.rows = len(self.content[0])
		self.columns = len(self.content)
		self.eigenvals = None 

	
	def divide(self, divisor, return_as_matrix=True) :
		return_matrix = defaulted_matrix(self.rows, self.columns)
		for X in range(self.columns) :
			for Y in range(self.columns) :
				return_matrix[X][Y] =  ( self.content[X][Y] / divisor )

		if return_as_matrix==True : 
			return_matrix = matrix(content=return_matrix)
			return return_matrix
		else: 
			return return_matrix
		self.eigenvals = None 


	def multiply (self, multiplier, return_as_matrix=True) :
		return_matrix = defaulted_matrix()
		for X in range(self.columns) :
			for Y in range(self.columns) :
				return_matrix[X][Y] =  ( self.content[X][Y] * multiplier )


		if return_as_matrix==True : 
			return_matrix = matrix(content=return_matrix)
			return return_matrix
		else: 
			return return_matrix
		self.eigenvals = None 
	
	def inverse (self, return_as_matrix=True) :

		if self.rows != self.columns :
			matrixError(1)

		determinant = self.det

		return_matrix = defaulted_matrix(self.rows, self.columns)

		for X in range(self.columns) :
			for Y in range(self.columns) : 
				return_matrix[Y][X] = self.content[X][Y]

		if return_as_matrix==True : 
			return_matrix = matrix(content=return_matrix)
			return return_matrix

		else: 
			return return_matrix
		self.eigenvals = None 



	def row_scale (self, row, scalar, do_replacement=True) :
		if row > len(self.content[0]) :
			matrixError(3)
		else: 
			new_row = []
			for I in range(len(self.content)) :
				new_row += [self.content[I][row] * scalar]

			if do_replacement == True :
				self.content = self.edit_row( row, new_row )
			else: 
				return new_row
			self.eigenvals = None 



	def swap_rows(self, row1, row2, do_row_override=True):
		if do_row_override == False:
			if row1 not in range(self.rows) or row2 not in range(self.rows):
				matrixError(6)
		else:
			if row1 not in range(self.rows):
				for I in range(self.rows, row1):
					self.add_row(I)
				self.update_sizes()
			if row2 not in range(self.rows):
				for I in range(self.rows, row2):
					self.add_row(I)
				self.update_sizes()
		store_row = self.content[row1]
		self.content[row1] = self.content[row2]
		self.content[row2] = store_row
		self.eigenvals = None 



	def add_rows( self, row1, row2, scalar) :
		if row1 not in range(self.rows) or row2 not in range(self.rows) :
				matrixError(6)
		else: 
			for I in range(self.columns) :
				self.content[row2][I] = self.content[row2][I] + (self.content[row1][I] * scalar)
		self.eigenvals = None 
	

	def pr(self) :
		for Y in range(self.rows) :
			for X in range(self.columns) :
				print(f"{self.content[X][Y]}", end=" ")
			print("")


	def write(self, listed) :
		max_index = len(listed)
		index = 0
		for Y in range(self.rows) :
			for X in range(self.columns) :
				self.content[X][Y] = listed[index]
				index += 1
				if index > max_index :
					break
			if index > max_index :
					break
		self.eigenvals = None 



	def triangulate(self, get_diagonal=False, do_matrix_return=False, do_matrix_rewrite=True):
		i = 0
		temp = copy.deepcopy(self)

		for X in range(temp.columns):
			if i >= temp.rows:
				break

			# pivot check: content[row][column]
			if temp.content[i][X] == 0:
				for Z in range(i + 1, temp.rows):
					if temp.content[Z][X] != 0:
						temp.swap_rows(i, Z)
						break
				if temp.content[i][X] == 0:
					continue

        # eliminate rows below pivot
			for Y in range(i + 1, temp.rows):
				scalar = -(temp.content[Y][X] / temp.content[i][X])
				temp.add_rows(i, Y, scalar)

			i += 1

		if get_diagonal:
			
			vals = []
			for I in range(temp.rows) :
					vals += [temp.content[I][I]]
			return vals

		elif do_matrix_return:
			return temp

		elif do_matrix_rewrite:
			self.content = temp.content
			self.update_sizes()



	def det(self) :
		if self.rows != self.columns :
			matrixError(1)
		elif self.rows == 2 :
			determinant = (self.content[0][0] * self.content[1][1]) - (self.content[0][1] * self.content[1][0])
			return determinant
		elif self.rows == 3 :
			positive_diagonals = 0
			for I in range(len(self.content)) :
				diagonal_starting_at_I = 1
				for y in range(len(self.content)) :
					if (y + I) >= len(self.content) :
						diagonal_starting_at_I *= self.content[y + I - len(self.content)][y]
					else: 
						diagonal_starting_at_I *= self.content[y + I][y]
				positive_diagonals += diagonal_starting_at_I
				
				
			negative_diagonals = 0 
			for i in range(len(self.content)) :
				diagonal_starting_at_i = 1
				for y in range(len(self.content)) :
					if (y + i) >= len(self.content) :
						diagonal_starting_at_i *= self.content[y + i - len(self.content)][-y]
					else: 
						diagonal_starting_at_i *= self.content[y + i][-y]
				negative_diagonals += diagonal_starting_at_i
				

			determinant = positive_diagonals - negative_diagonals
			return determinant
		elif self.rows > 3 :
			diagonals = self.triangulate(get_diagonal=True, do_matrix_rewrite=False)
			determinant = 1
			for I in range(len(diagonals)) :
				determinant *= diagonals[I]
			return determinant



	def eigenVals (self) :
		if self.rows != self.columns :
			matrixError(1)
		else:
			diagonals = self.triangulate(get_diagonal=True, do_matrix_rewrite=False)
		return diagonals



	def max_eigen_vect(self) :
		if self.rows != self.columns :
			matrixError(1)
		else:
			if isinstance(self.eigenvalues, None) :
		
				eigen = max(self.eigenVals())
			else: 
				eigen = max(self.eigenvalues)
			

			temp = copy.deepcopy(self)
			for I in range(temp.rows) :
				temp[I][I] = temp[I][I] - eigen


			guess_vector = []
			for I in range(temp.rows) :
				guess_vector += [1]


			previous_length = 0
			while True :
				guess_vector = mult(temp, guess_vector)
				length = 0
				for I in range(len(guess_vector)) :
					length = guess_vector[I] ** 2

				length = math.sqrt(length)

				if abs(length - previous_length) < .00001 :
					break

			return guess_vector
				

				
				



#Here starts the matrix related functions outside of the class itself



#matrix multiplication
def mult(A, B, return_as_matrix=True) :

	if not isinstance(A, matrix ) or not isinstance(B, matrix ) :
		matrixError(9)

	if A.columns != B.rows :
		matrixError(10)

	else: 
		return_matrix = matrix(rows=A.rows, columns=B.columns)
		for X in range(return_matrix.columns) :
			for Y in range(return_matrix.rows) :
				number  = 0
				for I in range(return_matrix.columns) :
					number += A.content[I][Y] * B.content[X][I]

				return_matrix.content[X][Y] = number

	if return_as_matrix==True : 
		return return_matrix

	else: 
		return return_matrix.content


	#do eigenvectors
	#do characteristic equation
	#do orthogonal regression
	#do linear regression to the nth degree


def regress(X, Y, degree)  :
	x_matrix = matrix()