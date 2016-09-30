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
	
def slashes( _str, _left, _right ):
	#Crop leading slash
	if _str[0] == '/' and not _left:
		_str = _str[1:]
	elif _str[0] != '/' and _left:
		_str = '/' + _str
		
	#Add trailing slash
	l = len(_str) - 1
	if _str[l] == '/' and not _right:
		_str = _str[:l]
	elif _str[l] != '/' and _right:
		_str += '/'
		
	return _str
	
def dirfmt( _str ):
	ret = ""
	for i in _str:
		if i != '\n':
			ret += i
	return ret
	
def cleanStringArray( _array ):
	ret = []
	for i in _array:
		if i != "":
			ret.append(i)
	return ret
	
	
	
