import math


def validation(xmin, ymin, nx, ny, N):

	acquisition_file_path = "saisie.csv"
	validation_file_path = "validation.csv"

	F = open(acquisition_file_path, 'r') 

	XA = list()
	YA = list()

	for line in F: 
		record = line.split()
		if (len(record) != 2):
			continue
		XA.append(float(record[0]))
		YA.append(float(record[1]))
		
		
	F = open(validation_file_path, 'r') 

	XV = list()
	YV = list()

	for line in F: 
		record = line.split()
		if (len(record) != 2):
			continue
		XV.append(float(record[0]))
		YV.append(float(record[1]))
		
	print("---------------------------------")
	print("Acquisition sample size: ", len(XA))
	print("Validation sample size: ", len(XV))
	print("---------------------------------")

	TA = [[[] for x in range(ny)]for x in range(nx)]
	TV = [[[] for x in range(ny)]for x in range(nx)]

	for i in range(nx):
		for j in range(ny):
			TA[i][j] = 0
			TV[i][j] = 0


	for k in range(len(XA)):
		ik = math.floor(XA[k])
		jk = math.floor(YA[k])
		TA[ik][jk] = TA[ik][jk] + 1 
		
	for k in range(len(XV)):
		ik = math.floor(XV[k])
		jk = math.floor(YV[k])
		TV[ik][jk] = TV[ik][jk] + 1 
					
	SHORTAGE = list()		
	for i in range(nx):
		for j in range(ny):
			if (TV[i][j] > TA[i][j]):
				SHORTAGE.append(TV[i][j] - TA[i][j])

	nb_shortage = 0
	for i in range(len(SHORTAGE)):
		nb_shortage = nb_shortage + SHORTAGE[i]
		
	nb_shortage_total = nb_shortage*(nx*ny)/N
	completion = math.floor(10000*(len(XA)/(len(XA)+nb_shortage_total))) / 100

	output = "Completion: "+str(completion)+"%\r\n"	
	output = output + "Theoretical missing number: "+str(math.floor(nb_shortage_total)+1)

	return output


	
xmin = 0
ymin = 0
nx = 100
ny = 200
N = 1000

print(validation(xmin, ymin, nx, ny, N))
		
print("---------------------------------")