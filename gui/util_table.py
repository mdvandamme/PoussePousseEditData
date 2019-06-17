# -*- coding: utf-8 -*-
"""
/***************************************************************************
 
 Functions to manage QTableWidget
                              -------------------
        begin                : 2019-05-17
        git sha              : $Format:%H$
        author               : M.-D. Van Damme
 ***************************************************************************/
"""

from PyQt4.QtGui import QTableWidgetItem


def suppLigne(table, indice):
    """
        Indice de l'élément à supprimer dans le tableau:
    """    
    
    table.removeRow(indice)
    return table


def addLigne(table, x, y):
    """
    """
    
    # On ajoute les coordonnées au tableau
    n = table.rowCount()
    table.insertRow(n);
        
    itemX = QTableWidgetItem(str(x))
    itemY = QTableWidgetItem(str(y))
    
    table.setItem(n, 0, itemX);
    table.setItem(n, 1, itemY);
    table.scrollToBottom()

    return table           


def charge(uriSL, table):

    with open(uriSL) as f:
        
        i = 0
        num_lines = sum(1 for line in open(uriSL))
        #print (num_lines)
        table.setRowCount(num_lines - 1)
            
        cpt = 0
        for line in f:
            if cpt == 0:
                # Ligne d'entete
                entetes = line.strip().split(",")
                # print (len(entetes))
                # table.setColumnCount(len(entetes))
                table.setColumnCount(2)
                colHearder = []
                # for j in range(len(entetes)):
                for j in range(2):
                    nom = entetes[j]
                    colHearder.append(nom)
                    table.setHorizontalHeaderLabels(colHearder)
            else:
                coord = line.strip().split(",")
                if len(coord) > 1:
                    itemX = QTableWidgetItem(str(coord[0]))
                    itemY = QTableWidgetItem(str(coord[1]))
                    table.setItem(i, 0, itemX)
                    table.setItem(i, 1, itemY)
                    i = i + 1
            cpt = cpt + 1
            
        f.close()
        
    return table
