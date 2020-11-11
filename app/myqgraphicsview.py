# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 22:30:53 2020

@author: adwait
"""
from PyQt5.QtWidgets import QGraphicsView

# %% Zoomable QGraphicsView Display
class MyQGraphicsView(QGraphicsView): #zoom QFraphicsView
    def __init__ (self, parent=None):
        super(MyQGraphicsView, self).__init__ (parent)

    def wheelEvent(self, event):
       
        zoomInFactor = 1.25  # Zoom Factor
        zoomOutFactor = 1 / zoomInFactor

        # Set Anchors
        self.setTransformationAnchor(QGraphicsView.NoAnchor)
        self.setResizeAnchor(QGraphicsView.NoAnchor)

        # Save the scene pos
        oldPos = self.mapToScene(event.pos())

        # Zoom
        if event.angleDelta().y() > 0:
            zoomFactor = zoomInFactor
        else:
            zoomFactor = zoomOutFactor
        self.scale(zoomFactor, zoomFactor)

        # Get the new position
        newPos = self.mapToScene(event.pos())

        # Move scene to old position
        delta = newPos - oldPos
        self.translate(delta.x(), delta.y())