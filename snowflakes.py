#!/usr/bin/python3 -tt

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import random


class Snowflake:

	def __init__(self, x=0.0, y=0.0, z=0.0):
		self.num_twigs = random.randint(0, 3) + 3
		self.pinkie_length = 0.5 + random.random() / 2.0
		self.branch_length = 1.0 + random.random()
		self.segments = random.randint(0, 3) + 2
		self.x = x
		self.y = y
		self.z = z
		self.xspin = self.yspin = self.zspin = 0.0

	def draw_twig(self, base, height, sides):
		glPushMatrix()
		glRotated(-90.0, 1.0, 0.0, 0.0)
		glutSolidCone(base, height, sides, 5)
		glPopMatrix()

	def draw_branch(self, size, left, segments=None):

		if segments is None:
			segments = self.segments

		glPushMatrix()
		glPushMatrix()
		glRotated(30, 0.0, 0.0, 1.0)
		if segments > 1:
			self.draw_branch(size / 1.5, size, int(segments / 2))
		self.draw_twig(0.025, size, 6)
		glRotated(-60, 0.0, 0.0, 1.0)
		if segments > 1:
			self.draw_branch(size / 1.5, size, int(segments / 2))
		self.draw_twig(0.025, size, 6)
		glPopMatrix()
		glTranslated(0.0, left / (segments * .75), 0.0)
		if segments > 1:
			self.draw_branch(
				size / 1.5,
				left - left / (segments * .75),
				int(segments - 1)
			)
		glPopMatrix()

	def draw(self):

		glPushMatrix()
		glTranslated(self.x, self.y, self.z)
		glRotated(self.xspin, 1.0, 0.0, 0.0)
		glRotated(self.yspin, 0.0, 1.0, 0.0)
		glRotated(self.zspin, 0.0, 0.0, 1.0)

		glEnable(GL_COLOR_MATERIAL)
		glEnable(GL_BLEND)
		glColor4d(0.60, 0.86, 1.0, 0.35)

		for i in range(1, self.num_twigs + 1):
			glPushMatrix()
			glRotated(360 / self.num_twigs * (i - 1), 0.0, 0.0, 1.0)
			self.draw_branch(
				self.pinkie_length / 1.25,
				self.branch_length / 1.25,
			)
			self.draw_twig(0.05, self.branch_length / 1.25, 12)
			glPopMatrix()

		glPushMatrix()
		glRotated(90, 1.0, 0.0, 0.0)
		self.draw_branch(self.pinkie_length / 1.25, self.branch_length / 1.25)
		glRotated(90, 0.0, 1.0, 0.0)
		self.draw_branch(self.pinkie_length / 1.25, self.branch_length / 1.25)
		self.draw_twig(0.05, self.branch_length / 1.25, 12)

		glRotated(-180, 1.0, 0.0, 0.0)
		self.draw_branch(self.pinkie_length / 1.25, self.branch_length / 1.25)
		glRotated(90, 0.0, 1.0, 0.0)
		self.draw_branch(self.pinkie_length / 1.25, self.branch_length / 1.25)
		self.draw_twig(0.05, self.branch_length / 1.25, 12)
		glPopMatrix()

		glDisable(GL_BLEND)
		glDisable(GL_COLOR_MATERIAL)
		glPopMatrix()

	def spin(self, xdelta, ydelta, zdelta):
		self.xspin += xdelta
		self.yspin += ydelta
		self.zspin += zdelta


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(1500, 500)
glutCreateWindow('snowflake')
glLightfv(GL_LIGHT0, GL_DIFFUSE, [.9, .9, 1.0, 1.0])
glLightfv(GL_LIGHT0, GL_POSITION, [1.0, 1.0, 1.0, 0.0])
glEnable(GL_LIGHT0)
glEnable(GL_LIGHTING)
glEnable(GL_CULL_FACE)
glShadeModel(GL_SMOOTH)
glClearColor(1.0, 1.0, 1.0, 0.0)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

glEnable(GL_DEPTH_TEST)

flakes = [Snowflake(z=-5.0, x=i) for i in (2.0, 0.0, -2.0)]


def display():

	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()

	for f in flakes:
		f.draw()

	glFlush()
	glutSwapBuffers()


def idle():
	flakes[0].spin(0.3, 0.6, 0.0)
	flakes[1].spin(0.3, 0.0, 0.6)
	flakes[2].spin(0.0, 0.3, 0.6)
	glutPostRedisplay()


def reshape(x, y):

	if (x == 0) or (y == 0):
		return

	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(30.0, x / y, 0.5, 20.0)
	glMatrixMode(GL_MODELVIEW)
	glViewport(0, 0, x, y)


glutDisplayFunc(display)
glutIdleFunc(idle)
glutReshapeFunc(reshape)
glutMainLoop()
