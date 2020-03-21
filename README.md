# Simulační výpočty exotických opcí
### (Valuation of Exotic Options via Simulations)


Repo obsahuje kód pro simulování cen některých exotických opcí vyskytujících se v energetice. Vytvořeno v rámci mé diplomové práce (FEL ČVUT).  

Podkladová aktiva, která jsou pro energetiku relevantní (opce jsou většinou na futures těchto komodit):

* Ropa
* Plyn
* Biomasa
* Elektřina

Zaměřuji se na opce dostupné na NYMEX. K futures na ropu a plyn jsou dostupné [datasety](https://www.eia.gov/dnav/pet/pet_pri_fut_s1_d.htm) s historickými cenami. Opce, které se na NYMEX obchodují jsou například **WTI Average Price Option** a **WTI Calendar Spread (1, 2, 3, 6, 12 Month) Option**. Seznam všech je v [seznamu produktů](https://www.cmegroup.com/trading/products/#pageNumber=1&sortAsc=false&sortField=oi&group=7&page=1&cleared=Options) na stránkách CME Group.

Jako programovací jazyk jsem zvolil Python. Pro psaní kódu používám Atom a Jupyter Notebook.


#### Vybrané exotické opce  
* Asijské opce
* Spread opce


#### Popis
* Funkce pro výpočet parametrů modelů
	* Markov chain monte carlo (MCMC)
 	* Euler discretization
 	* ARIMA
* Funkce pro simulování opcí po zadání nutných parametrů
	* Monte Carlo simulace stochastických modelů
		* diskrétní modely vytvořené ze spojitých modelů (Geometric Brownian Motion, Ornstein-Uhlenbeck process, ...)
		* ARIMA modely
	* Simulace jsou upraveny pro jednotlivé typy exotických opcí
	* Výstupem je grafické zobrazení cest simulací a ohodnocení opce


## Seznam simulací
##### Evropská opce
* Mean reverting O-U simulace (Evropská put a call opce)

##### Exotické opce

* Geometric Brownian Motion simulace
* Mean reverting O-U simulace (Asijská opce - evropský typ)
	* Floating strike (Strike je průměr spotových cen, porovnává se s spotovou cenou v čase expirace opce)
	* Fixed strike (Strike je fixní, porovnává se s průměrem spotových cen)
* Mean reverting O-U simulace (Spread opce)
* [TODO] mean reverting w/ jump diffusion

## Simulace reálného produktu

##### WTI Average Price Option (Asijská opce)

1. Výpočet parametrů pro model z datasetu (decomposition, MCMC)
2. Výběr modelu (diskrétní forma stochastického modelu, ARIMA)
3. Simulace
4. Porovnání (se vzorcem/s jiným modelem)