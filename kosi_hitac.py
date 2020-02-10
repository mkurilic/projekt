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
from time import sleep

def T(h):
    return -131 + 0.003*h + 273.15

def tlak(h):
    h0 = 0
    M = 0.0289644   #molarna masa zraka
    R = 8.31432     #opca plinska konstanta
    p0 = 101325     #tlak na povrsini zemlje
    return p0 * np.exp (-g * M * (h-h0) / (R * T(h)))

def ulaz(vjetar = False):
    h0 = int(input("\nNa kojoj visini zelite kuglicu? "))
    fi = np.radians(int(input("Odaberite kut pod kojime ce kuglica biti izbacena: ")))
    v_iznos = int(input("Pocetna brzina: "))
    if (vjetar):
        smjer = np.radians(int(input("Odaberite smjer vjetra. (stupnjevi)\n")))
        print()
        return h0, fi, v_iznos, smjer
    print()
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
            kuglica += v*dt + 1/2*akceleracija*dt**2
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
    
    svi = []
    m = 0.1             #masa kuglice 100g
    R = 0.001           #radijus kuglice 1cm
    A = R**2 * np.pi
    t = 0
    C = 0.4             #pretpostavljeni koeficijent otpora zraka na kuglici 
    h0, fi, v0, smjer = ulaz(True)
    kuglice = []
    for i in range(11):
        kuglice.append(np.array([0.0, h0]))
    akceleracija = np.array([0.0, -g])
    screen = pygame.display.set_mode((Xsize, Ysize))
    pygame.display.set_caption('kosi hitac pod utjecajem vjetra')
    screen.fill(pygame.Color(0,0,0))
    hmax = 0
    i = 0
    for w in np.linspace(-20, 20, 11):
        pozicije = []
        v = np.array([v0 * np.cos(fi), v0 * np.sin(fi)])
        wv = np.array([w * np.cos(smjer), w * np.sin(smjer)])
        kuglica = kuglice[i]
        izlazVjetar.write("%d. kuglica\n%13s\t\tBRZINA KUGLICE\t\tSILA VJETRA\t\tVRIJEME\n" % (i+1, "KOORDINATE"))
        kuglica = kuglice[i]
        rand = pygame.Color(randrange(256), randrange(256), randrange(256))
        i+=1
        while (kuglica[1] >= 0):
            v_iznos = norm(v)
            D = tlak(kuglica[1])*C*A/2  #konstanta otpora ovisna o tlaku
            f = D*norm(wv)*wv           #sila kojom vjetar djeluje na kuglicu
            a = f/m + akceleracija      #ukupna akceleracija koja djeluje na kuglicu
            v += akceleracija*dt
            koordinatni(screen, Xsize, Ysize, bijela)
            izlazVjetar.write("%3.2f\t%3.2f\t\t%14.2f\t\t%11.2f\t\t%7.2f\n" % (kuglica[0], kuglica[1], v_iznos, norm(f), t))
            kuglica += v*dt + 1/2*a*(dt**2)
            if (hmax < kuglica[1]):
                hmax = kuglica[1]
            pozicije.append(kuglica.copy())
            t += dt
            for p in pozicije:
                crtaj(screen, p, 1, rand, Xsize, Ysize-100)    
            pygame.displarand = pygame.Color(randrange(256), randrange(256), randrange(256))
            pygame.display.flip()
        print ("%2d. kuglica je postigla visinu %3.2f" % (i, hmax))
        izlazVjetar.write("\n\n")
        svi.append(pozicije)
    print()
    pygame.quit()
    graf(svi, True)
        
        
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
