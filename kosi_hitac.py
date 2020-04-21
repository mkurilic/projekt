import pygame
from sys import exit
from pygame.gfxdraw import aacircle as circ
from pygame.gfxdraw import filled_circle as fcirc
from pygame.draw import line
import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import norm
from random import randrange
from scipy.constants import g

def T(h):
	return -131 + 0.003*h + 273.15

def tlak(h):
	h0 = 0
	M = 0.0289644
	R = 8.31432
	p0 = 101325
	return p0 * np.exp (-g * M * (h-h0) / (R * T(h)))

def ulaz(idealni = False, vjetar = False):
	h0 = int(input("\nNa kojoj visini zelite kuglicu? "))
	if (idealni or vjetar):
		fi = np.radians(int(input("Odaberite kut pod kojime ce kuglica biti izbacena: ")))
	v_iznos = int(input("Pocetna brzina: "))
	if (vjetar):
		smjer = np.radians(int(input("Odaberite smjer vjetra. (stupnjevi)\n")))
		print()
		return h0, fi, v_iznos, smjer
	if (idealni):
		print()
		return h0, fi, v_iznos
	else:
		return h0, v_iznos

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
			graf(svi, False, False)	
			return
		h0, fi, v_iznos = ulaz(True, False)
		
		t_izrac = (-v_iznos*np.sin(fi) - np.sqrt(((v_iznos*np.sin(fi))**2 + 2*g*h0))) / -g
		max_h = h0 + v_iznos**2 * np.sin(fi)**2 / (2 * g)
		domet = v_iznos* np.cos(fi) * t_izrac

		print("Izracunate vrijednosti: vrijeme = %.2f, maksimalna visina = %.2f, domet = %.2f" % (t_izrac, max_h, domet))


		br_podataka += 1
		kuglica = np.array([0.0, h0])
		izlazIdeal.write("%d. simulacija\n%13s\t\tVERTIKALNA BRZINA\t\tVRIJEME\n" % (br_podataka, "KOORDINATE"))
		v = np.array([v_iznos * np.cos(fi), v_iznos * np.sin(fi)])
		akceleracija = np.array([0.0, -g])
		screen = pygame.display.set_mode((Xsize, Ysize))
		pygame.display.set_caption('kosi hitac')
		hmax = 0
		
		while (kuglica[1] >= 0):
			screen.fill(pygame.Color(0,0,0))
			koordinatni(screen, Xsize, Ysize, bijela)
			izlazIdeal.write("%3.2f\t%3.2f\t\t%12.2f\t\t%7.2f\n" % (kuglica[0], kuglica[1], v[1], t))
			kuglica += v*dt 
			if (hmax < kuglica[1]):
				hmax = kuglica[1]
			pozicije.append(kuglica.copy())

			v += akceleracija*dt
			v_iznos = norm(v)
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

def otporZraka():
	global Xsize, Ysize, r, dt

	boja = pygame.Color(0, 133, 133)
	boja1 = pygame.Color(0, 50, 50)
	bijela = pygame.Color(255, 255, 255)

	
	m = 1				#masa kuglice 1kg
	R = 0.1				#radijus kuglice 10cm
	A = R**2 * np.pi 	
	t = 0
	Cd = 0.1			#koeficjent otpora zraka za glatku sferu			
	Rconst = 287.05		#plinska konstanta	
	
	h0, v_0 = ulaz()
	kuglice = []
	svi = []
	for i in range(10):
		kuglice.append(np.array([0.0, h0]))
	i = 0
	
	akceleracija = np.array([0.0, -g])
	screen = pygame.display.set_mode((Xsize, Ysize))
	pygame.display.set_caption('kosi hitac otpor zraka')
	screen.fill(pygame.Color(0,0,0))

	for fi in np.linspace(0, 90, 10):
		pozicije = []
		t = 0
		fi = np.radians(fi)
		kuglica = kuglice[i] 
		i+=1
		izlazOtpor.write("%d. kuglica\n%13s\t\tVERTIKALNA BRZINA\t\tVRIJEME\n" % (i+1, "KOORDINATE"))
		rand = pygame.Color(randrange(256), randrange(256), randrange(256))
		v = np.array([v_0 * np.cos(fi), v_0 * np.sin(fi)])
		while (kuglica[1] >= 0):
			v_iznos = norm(v)
			v_jed = v/v_iznos
			rho = tlak(kuglica[1])/(Rconst*T(kuglica[1]))		#gustoća zraka na visini
			#sila otpora = 0.5 * rho * Cd * A * norm(v)^2 * v^		
			f = 1/2 * rho * Cd * A *v_iznos**2*(-v_jed) 
			a = f/m + akceleracija		
			v += a*dt
			koordinatni(screen, Xsize, Ysize, bijela)
			izlazOtpor.write("%4.2f\t%4.2f\t\t%14.2f\t\t%7.2f\n" % (kuglica[0], kuglica[1], v[1], t))
			kuglica += v*dt
			pozicije.append(kuglica.copy())
			t += dt
			crtaj(screen, kuglica, 1, boja, Xsize, Ysize-100)
			pygame.displarand = pygame.Color(randrange(256), randrange(256), randrange(256))
			pygame.display.flip()
		izlazOtpor.write("\n\n")
		svi.append(pozicije)
	pygame.quit()
	graf(svi, True, False)

def utjecajVjetra():
	global Xsize, Ysize, r, dt

	boja = pygame.Color(0, 133, 133)
	boja1 = pygame.Color(0, 50, 50)
	bijela = pygame.Color(255, 255, 255)

	
	m = 1				#masa kuglice 1kg
	R = 0.1				#radijus kuglice 10cm
	A = R**2 * np.pi 	
	t = 0
	Cd = 0.1			#koeficjent otpora zraka za glatku sferu			
	Rconst = 287.05		#plinska konstanta	
	
	h0, fi, v_0, smjer = ulaz(False, True)
	kuglice = []
	svi = []
	for i in range(11):
		kuglice.append(np.array([0.0, h0]))
	i = 0
	
	akceleracija = np.array([0.0, -g])
	screen = pygame.display.set_mode((Xsize, Ysize))
	pygame.display.set_caption('kosi hitac utjecaj vjetra')
	screen.fill(pygame.Color(0,0,0))

	for w in np.linspace(-40,40, 11):
		pozicije = []
		t = 0
		kuglica = kuglice[i] 
		i+=1
		izlazVjetar.write("%d. kuglica\n%13s\t\tVERTIKALNA BRZINA\t\tSILA VJETRA\t\tVRIJEME\n" % (i+1, "KOORDINATE"))
		rand = pygame.Color(randrange(256), randrange(256), randrange(256))
		wv = np.array([w * np.cos(smjer), w * np.sin(smjer)])
		v = np.array([v_0 * np.cos(fi), v_0 * np.sin(fi)])
		while (kuglica[1] >= 0):
			v_iznos = norm(v - wv)
			v_jed = (v - wv)/v_iznos
			rho = tlak(kuglica[1])/(Rconst*T(kuglica[1]))		#gustoća zraka na visini
			#sila otpora = 0.5 * rho * Cd * A * norm(v)^2 * v^		
			f = 1/2 * rho * Cd * A *v_iznos**2*(-v_jed) 
			a = f/m + akceleracija		
			v += a*dt
			koordinatni(screen, Xsize, Ysize, bijela)
			izlazVjetar.write("%3.2f\t%3.2f\t\t%14.2f\t\t%11.2f\t\t%7.2f\n" % (kuglica[0], kuglica[1], v[1], norm(f), t))
			kuglica += v*dt
			pozicije.append(kuglica.copy())
			t += dt
			crtaj(screen, kuglica, 1, boja, Xsize, Ysize-100)
			pygame.displarand = pygame.Color(randrange(256), randrange(256), randrange(256))
			pygame.display.flip()
		izlazVjetar.write("\n\n")
		svi.append(pozicije)
	pygame.quit()
	graf(svi, False, True)
	
		
		
def graf(podaci, otpor, vjetar):
	plt.xlabel('x os')
	plt.ylabel('y os')

	if (vjetar):
		wv = list(np.linspace(-40, 40, 11))
		plt.title("Graficki prikaz hica s utjecajem vjetra")
		for i in range(11):
			kuglica = podaci[i]
			x, y = zip(*kuglica)
			plt.plot(x, y, label = "v(vjetar) = %d" % wv[i])
			plt.axis('equal')
	elif (otpor):
		fi = list(np.linspace(0, 90, 10))
		plt.title("Graficki prikaz hica s otporom zraka")
		for i in range(10):
			kuglica = podaci[i]
			x, y = zip(*kuglica)
			plt.plot(x, y, label = "kut izbacaja = %d" % fi[i])
			plt.axis('equal')
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
	odabir = int(input("Odaberi simulaciju:\n\t1. Idealni uvjeti\n\t\t- bez utjecaja vjetra, odabir pocetne visine, brzine i kuta\n\t2. Hitac s otporom zraka\n\t\t- bez utjecaja vjetra, ali s otporom zraka, odabir pocetne brzine i visine\n\t\t- kutevi izbacaja od 0° do 90°\n\t3. Utjecaj vjetra\n\t\t- s utjecajem vjetra brzine u rasponu od -40 do 40m/s, odabir pocetne visine, brzine, kuta ispucanja, kuta puhanja vjetra\n\t4. Izlaz\n"))
	pygame.init()
	if (odabir == 1):
		izlazIdeal = open('izlaz.txt', 'w')
		idealniUvjeti()
		izlazIdeal.close()
	elif (odabir == 2):
		izlazOtpor = open('izlaz_otpor.txt', 'w')
		otporZraka()
		izlazOtpor.close()
	elif (odabir == 3):
		izlazVjetar = open('izlaz_vjetar.txt', 'w')
		utjecajVjetra()
		izlazVjetar.close()
	elif (odabir == 4):
		exit()