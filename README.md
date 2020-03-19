# Simulační výpočty exotických opcí
### (Valuation of Exotic Options via Simulations)

  
Repo obsahuje kód pro simulování cen některých exotických opcí vyskytujících se v energetice. Vytvořeno v rámci mé diplomové práce (FEL ČVUT).  

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

* [TODO] Mean reverting O-U simulace (Asijská opce - evropský typ)
	* Floating strike (Strike je průměr spotových cen, porovnává se s spotovou cenou v čase expirace opce)
	* Fixed strike (Strike je fixní, porovnává se s průměrem spotových cen)
* [TODO]
* [TODO]
