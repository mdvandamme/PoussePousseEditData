import sys
import math
import random

from grille import Grille

def validation(acquisition_file_path, validation_file_path, g, C, Nc, B = 500, factor = 10**3):

    N = len(C)
    bootstrap_sample_size = B

    F = open(acquisition_file_path, 'r') 

    XA = list()
    YA = list()

    for line in F: 
        record = line.split(',')
        if (len(record) != 2):
            continue
        if record[0] != 'x':
            XA.append(float(record[0]))
            YA.append(float(record[1]))

    F = open(validation_file_path, 'r') 

    XV = list()
    YV = list()

    for line in F: 
        record = line.split(',')
        if (len(record) != 2):
            continue
        if record[0] != 'x':
            XV.append(float(record[0]))
            YV.append(float(record[1]))
		
    print("--------------------------------------------------------------------------------")
    print("Acquisition sample size: ", len(XA))
    print("Validation sample size: ", len(XV))
    print("--------------------------------------------------------------------------------")
    

    TA = [[[] for x in range(g.ny)]for x in range(g.nx)]
    TV = [[[] for x in range(g.ny)]for x in range(g.nx)]

    for i in range(g.nx):
        for j in range(g.ny):
            TA[i][j] = list()
            TV[i][j] = list()
    

    for k in range(len(XA)):
        ik = math.floor( (XA[k] - g.xmin) / g.rx)
        jk = math.floor( (YA[k] - g.ymin) / g.ry)
        TA[ik][jk].append(k) 
		
    for k in range(len(XV)):
        ik = math.floor((XV[k]-g.xmin)/g.rx)
        jk = math.floor((YV[k]-g.ymin)/g.ry)
        TV[ik][jk].append(k)


    BE = list()
    BN = list()
    RMSE = list()
    ERROR = list()
    COMPLETION = list()
    NB_SHORTAGE_TOTAL = list()
	
    #bar = progressbar.ProgressBar(maxval=bootstrap_sample_size, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    #bar.start()

    for bootstrap in range(bootstrap_sample_size):
	
        # bar.update(bootstrap+1)
	
        be = 0
        bn = 0
        rmse = 0
        error = 0
        counter = 0
        nb_shortage = 0
        
        for i in range(len(C)):
			
            i2 = int(math.floor((random.random()*len(C))))
            idx = C[i2][0]
            idy = C[i2][1]
            if (len(TA[idx][idy]) < len(TV[idx][idy])):
                continue
            nb_shortage = nb_shortage + (len(TA[idx][idy])-len(TV[idx][idy]))
            
            for j in range(len(TV[idx][idy])):
			
                xv = XV[TV[idx][idy][j]]
                yv = YV[TV[idx][idy][j]]
                d = sys.float_info.max
				
                for k in range(len(TA[idx][idy])):
				
                    xa = XA[TA[idx][idy][k]]
                    ya = YA[TA[idx][idy][k]]
                    dk = (xv-xa)**2+(yv-ya)**2
					
                    if (dk < d):
                        d = dk	
                        be2 = (xv-xa)
                        bn2 = (yv-ya)
						
                if (d == sys.float_info.max):
                    continue
					
                rmse = rmse + d
                error = error + math.sqrt(d)
                be = be + be2
                bn = bn + bn2
                counter = counter + 1
			
        if counter > 0:
            rmse = math.sqrt(rmse/counter)
            error = error/counter
            be = be/counter
            bn = bn/counter
        else:
            rmse = 0
            error = 0
            be = 0
            bn = 0

        nb_shortage_total = nb_shortage*Nc/N
        div = len(XA)+nb_shortage_total
        if div > 0:
            completion = math.floor(10000*(len(XA)/div))/100
        else:
            completion = 0
		
        BE.append(be)
        BN.append(bn)
        RMSE.append(rmse)
        ERROR.append(error)
        COMPLETION.append(completion)
        NB_SHORTAGE_TOTAL.append(math.floor(nb_shortage_total)+1)
		
		
    be = 0
    bn = 0
    rmse = 0
    error = 0
    completion = 0
    nb_shortage = 0
	
		
    be2 = 0
    bn2 = 0
    rmse2 = 0
    error2 = 0
    completion2 = 0
    nb_shortage2 = 0
	
    for i in range(bootstrap_sample_size):
        be = be + BE[i]
        bn = bn + BN[i]
        rmse = rmse + RMSE[i]
        error = error + ERROR[i]
        completion = completion + COMPLETION[i]
        nb_shortage = nb_shortage + NB_SHORTAGE_TOTAL[i]
        be2 = be2 + BE[i]**2
        bn2 = bn2 + BN[i]**2
        rmse2 = rmse2 + RMSE[i]**2
        error2 = error2 + ERROR[i]**2
        completion2 = completion2 + COMPLETION[i]**2
        nb_shortage2 = nb_shortage2 + NB_SHORTAGE_TOTAL[i]**2

		
    be = be/bootstrap_sample_size
    bn = bn/bootstrap_sample_size
    rmse = rmse/bootstrap_sample_size
    error = error/bootstrap_sample_size
    completion = completion/bootstrap_sample_size
    nb_shortage = nb_shortage/bootstrap_sample_size
		
    be2 = be2/bootstrap_sample_size
    bn2 = bn2/bootstrap_sample_size
    rmse2 = rmse2/bootstrap_sample_size
    error2 = error2/bootstrap_sample_size
    completion2 = completion2/bootstrap_sample_size
    nb_shortage2 = nb_shortage2/bootstrap_sample_size
	
    sbe = math.sqrt(abs(be2 - be**2))
    sbn = math.sqrt(abs(bn2 - bn**2))
    srmse = math.sqrt(abs(rmse2 - rmse**2))
    serror = math.sqrt(abs(error2 - error**2))
    scompletion = math.sqrt(abs(completion2 - completion**2))
    snb_shortage = math.sqrt(abs(nb_shortage2 - nb_shortage**2))
	
    rmse = math.floor(rmse*factor)/factor
    error = math.floor(error*factor)/factor
    be = math.floor(be*factor)/factor
    bn = math.floor(bn*factor)/factor
    completion = math.floor(completion*factor)/factor
	
    srmse = math.floor(srmse*factor)/factor
    serror = math.floor(serror*factor)/factor
    sbe = math.floor(sbe*factor)/factor
    sbn = math.floor(sbn*factor)/factor
    scompletion = math.floor(scompletion*factor)/factor
    snb_shortage = math.floor(snb_shortage*factor)/factor
	
    missing = math.floor(nb_shortage + 1.96*snb_shortage)+1
	
    output = "Completion: "+str(completion)+" (+/- "+str(scompletion)+") %\r\n"	
    output = output + "Theoretical missing number: < "+str(missing)+"\r\n"
    output = output + "Mean error: "+str(error)+" (+/- "+str(serror)+") m\r\n"
    output = output + "Root mean square error: "+str(rmse)+" (+/- "+str(srmse)+") m\r\n"
    output = output + "X bias: "+str(be)+" (+/- "+str(sbe)+") m\r\n"
    output = output + "Y bias: "+str(bn)+" (+/- "+str(sbn)+") m"
    print (output)
    
    return (completion,scompletion,missing,error,serror,rmse,srmse,be,sbe,bn,sbn)


	


acquisition_file_path = 'D:\\DATA\\PoussePousse\\Points.csv'
validation_file_path = 'D:\\DATA\\PoussePousse\\ctrl_20190526_233430.dat'
xmin = 650851.648136
ymin = 6859531.09908
nx = 8
ny = 7
Nc = 16
rx = 250
ry = 250
C = [[5, 4], [4, 6], [6, 6], [4, 5], [7, 6], [7, 4], [7, 5], [3, 6], [6, 5], [5, 5]]

g = Grille(nx, ny, xmin, ymin, rx, ry)

# B=1000
print(validation(acquisition_file_path, validation_file_path, g, C, Nc))
		
print("--------------------------------------------------------------------------------")