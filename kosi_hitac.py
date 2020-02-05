import pygame
from sys import exit
from pygame.gfxdraw import aacircle as circ
from pygame.gfxdraw import filled_circle as fcirc
from pygame.draw import line
import matplotlib.pyplot as plt
import numpy as np
from random import randrange
from scipy.constants import g

def ulaz(vjetar = False):
	h0 = int(input("Na kojoj visini zelite kuglicu? "))
	fi = np.radians(int(input("Odaberite kut pod kojime ce kuglica biti izbacena: ")))
	v_iznos = int(input("Pocetna brzina: "))
	if (vjetar):
		smjer = np.radians(int(input("Odaberite smjer vjetra. (stupnjevi)\n")))
		return h0, fi, v_iznos, smjer
	return h0, fi, v_iznos

def crtaj(screen, pozicija, r, boja, X, Y):
	x = int(pozicija[0]) + X//2
	y = Y - int(pozicija[1])
	fcirc(screen, x, y, r, boja)
	circ(screen, x, y, r, boja)

def koordinatni(screen, X, Y, b):
	xos1 = np.array([0, Y-100])
	xos2 = np.array([X, Y-100])
	yos1 = np.array([X//2, 0])
	yos2 = np.array([X//2, Y])
	line(screen, b, xos1, xos2)
	line(screen, b, yos1, yos2)

def idealniUvjeti():
	global Xsize, Ysize, r, dt

	boja = pygame.Color(0, 133, 133)
	boja1 = pygame.Color(0, 50, 50)
	bijela = pygame.Color(255, 255, 255)
	svi = []
	boje = []
	br_podataka = 0
	while True:
		t = 0
		pozicije = []
		u = input("\nZelite li pokrenuti simulaciju? ('n' za izlaz)\n")
		if (u == 'n'):
			graf(svi, False)	
			return
		h0, fi, v_iznos = ulaz()
		
		t_izrac = (-v_iznos*np.sin(fi) - np.sqrt(((v_iznos*np.sin(fi))**2 + 2*g*h0))) / -g
		max_h = h0 + v_iznos**2 * np.sin(fi)**2 / (2 * g)
		domet = v_iznos* np.cos(fi) * t_izrac

		print("Izracunate vrijednosti: vrijeme = %.2f, maksimalna visina = %.2f, domet = %.2f" % (t_izrac, max_h, domet))


		br_podataka += 1
		kuglica = np.array([0.0, h0])
		izlazIdeal.write("%d. simulacija\n%13s\t\tIZNOS BRZINE\t\tVRIJEME\n" % (br_podataka, "KOORDINATE"))
		v = np.array([v_iznos * np.cos(fi), v_iznos * np.sin(fi)])
		akceleracija = np.array([0.0, -g])
		screen = pygame.display.set_mode((Xsize, Ysize))
		pygame.display.set_caption('kosi hitac')
		hmax = 0
		
		while (kuglica[1] >= 0):
			screen.fill(pygame.Color(0,0,0))
			koordinatni(screen, Xsize, Ysize, bijela)
			izlazIdeal.write("%3.2f\t%3.2f\t\t%12.2f\t\t%7.2f\n" % (kuglica[0], kuglica[1], v_iznos, t))
			kuglica += v*dt + 1/2*akceleracija*(dt**2)
			if (hmax < kuglica[1]):
				hmax = kuglica[1]
			pozicije.append(kuglica.copy())

			v += akceleracija*dt
			v_iznos = np.sqrt(v[0]**2 + v[1]**2)
			t += dt
			i = 0
			for kugla in svi:
				for pozicija in kugla:
					crtaj(screen, pozicija, 1, boje[i], Xsize, Ysize-100)
				i += 1

			for p in pozicije:
				crtaj(screen, p, r//2, boja1, Xsize, Ysize-100)

			crtaj(screen, kuglica, r, boja, Xsize, Ysize-100)
			pygame.display.flip()
		print("Vrijednosti pomocu simulacije: vrijeme = %.2f, maksimalna visina = %.2f, domet = %.2f" % (t, hmax, kuglica[0]))
		svi.append(pozicije)
		rand = pygame.Color(randrange(256), randrange(256), randrange(256))
		boje.append(rand)
		izlazIdeal.write("\n\n")
		pygame.quit()


def utjecajVjetra():
	global Xsize, Ysize, r, dt

	boja = pygame.Color(0, 133, 133)
	boja1 = pygame.Color(0, 50, 50)
	bijela = pygame.Color(255, 255, 255)
	
	br_podataka = 0
	svi = []
	while True:
		t = 0

		u = input("\nZelite li pokrenuti simulaciju? ('n' za izlaz)\n")
		if (u == 'n'):
			graf(svi, True)
			return
		h0, fi, v0, smjer = ulaz(True)
		alfa = 0.15 	#koeficijent koji ovisi o površini iznad koje gledamo iznose vjetra, uzeta vrijednost za ravnicu 
		br_podataka += 1
		kuglice = []
		for i in range(11):
			kuglice.append(np.array([0.0, h0]))
		
		akceleracija = np.array([0.0, -g])
		screen = pygame.display.set_mode((Xsize, Ysize))
		pygame.display.set_caption('kosi hitac pod utjecajem vjetra')
		screen.fill(pygame.Color(0,0,0))
		hmax = 0
		i = 0
		
		for v10 in np.linspace(-20, 20, 11):
			pozicije = []
			v = np.array([v0 * np.cos(fi), v0 * np.sin(fi)])
			izlazVjetar.write("%d. kuglica\n%13s\t\tBRZINA KUGLICE\t\tBRZINA VJETRA\t\tVRIJEME\n" % (i, "KOORDINATE"))
			kuglica = kuglice[i]
			i+=1
			while (kuglica[1] >= 0):
				v_iznos = np.sqrt(v[0]**2 + v[1]**2)
				koordinatni(screen, Xsize, Ysize, bijela)
				vH = v10 * (kuglica[1]/10)**alfa
				vjetar = np.array([vH * np.cos(smjer), vH * np.sin(smjer)])
				izlazVjetar.write("%3.2f\t%3.2f\t\t%14.2f\t\t%13.2f\t\t%7.2f\n" % (kuglica[0], kuglica[1], v_iznos, vH, t))

				kuglica += v*dt + 1/2*akceleracija*(dt**2)  + vjetar*dt
				if (hmax < kuglica[1]):
					hmax = kuglica[1]
				pozicije.append(kuglica.copy())
				v += akceleracija*dt
				t += dt
				crtaj(screen, kuglica, 1, boja, Xsize, Ysize-100)
				pygame.display.flip()
			izlazVjetar.write("\n\n")
			svi.append(pozicije)
		pygame.quit()
		
		
def graf(podaci, vjetar):
	plt.xlabel('x os')
	plt.ylabel('y os')
	if (vjetar):
		vv = list(np.linspace(-20, 20, 11))
		plt.title("Graficki prikaz hica s utjecajem vjetra")
		for i in range(11):
			kuglica = podaci[i]
			x, y = zip(*kuglica)
			plt.plot(x, y, label = "v(vjetar) = %d" % vv[i])
	else:
		plt.title("Graficki prikaz hica bez utjecaja vjetra")
		i = 1
		for kuglica in podaci:
			x, y = zip(*kuglica)
			plt.plot(x, y, label = "%d. kuglica" % i)
			i += 1
	plt.grid(True)
	plt.legend()
	plt.show()

Xsize = 1000
Ysize = 500
r = 10
dt = 0.02

while True:
	odabir = int(input("Odaberi simulaciju:\n\t1. Idealni uvjeti\n\t\t- bez utjecaja vjetra, odabir pocetne visine, brzine i kuta\n\t2. Utjecaj vjetra\n\t\t- s utjecajem vjetra brzine u rasponu od -20 do 20m/s, odabir pocetne visine, brzine, kuta ispucanja, kuta puhanja vjetra\n\t3. Izlaz\n"))
	pygame.init()
	if (odabir == 1):
		izlazIdeal = open('izlaz.txt', 'w')
		idealniUvjeti()
		izlazIdeal.close()
	elif (odabir == 2):
		izlazVjetar = open('izlaz_vjetar.txt', 'w')
		utjecajVjetra()
		izlazVjetar.close()
	elif (odabir == 3):
		exit()