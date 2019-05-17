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
        