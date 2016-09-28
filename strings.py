import os

def lev( _str1, _str2 ):
	m = len( _str1 )
	n = len( _str2 )
	
	if n == 0:
		return m
	elif m == 0:
		return n
		
	n += 1
	m += 1
	
	#Initialise a matrix with 0->m columns and 0->n rows
	matrix = [ [ 0 for x in range(n) ] for y in range(m) ]
		
	for x in range( m ):
		matrix[x][0] = x
	for y in range( n ):
		matrix[0][y] = y
	
	n -= 1
	m -= 1
		
	for i in range( m ):
		mx = i + 1
		for j in range( n ):
			my = j + 1
			cost = 0
			if( _str1[i] != _str2[j] ):
				cost = 1
				
			minVal = min( matrix[mx][my - 1] + 1, matrix[mx - 1][my] + 1 )
			minVal = min( minVal, matrix[mx - 1][my - 1] + cost	)
				
			matrix[mx][my] = minVal
	
	#for i in range(len(matrix)):
	#	print matrix[i]
					
	return matrix[m][n]
			
def match( _str1, _str2, _threshold ):
	return lev( _str1, _str2 ) <= _threshold
	
def slashes( _str ):
	#Crop leading slash
	if _str[0] == '/':
		_str = _str[1:]
	#Add trailing slash
	if _str[ len(_str) - 1 ] != '/':
		_str += '/'
	return _str
	
def dirfmt( _str ):
	_str = slashes( _str )
	_str = os.path.expanduser('~') + '/' + _str
	return _str
	
	
		
	
	
	
