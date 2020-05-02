# Simulační výpočty exotických opcí
### (Valuation of Exotic Options via Simulations)


Repo obsahuje kód pro simulování cen některých exotických opcí vyskytujících se v energetice. Vytvořeno v rámci mé diplomové práce (FEL ČVUT).  

Podkladová aktiva, která jsou pro energetiku relevantní (opce jsou většinou na futures těchto komodit):

* Ropa
* Plyn
* Biomasa
* Elektřina

V práci používám jako podkladové aktivum futures na ropu.

Zaměřuji se na opce dostupné na NYMEX. Opce, které se na NYMEX obchodují jsou například **WTI Average Price Option** a **WTI Calendar Spread (1, 2, 3, 6, 12 Month) Option**. Seznam všech je v [seznamu produktů](https://www.cmegroup.com/trading/products/#pageNumber=1&sortAsc=false&sortField=oi&group=7&page=1&cleared=Options) na stránkách CME Group.

Jako programovací jazyk jsem zvolil Python. Pro psaní kódu používám Atom a Jupyter Notebook.


### Vybrané exotické opce  

* Asijská opce
* Spread opce

### Seznam simulací

* Asijská opce - model na základě GBM [Výpočet](vypocty_diplomova_prace_asian_gbm.ipynb)
* Calendar spread opce - model na základě GBM [Výpočet](vypocty_diplomova_prace_calendar_gbm.ipynb)
* Asijská opce - mean reverting model [Výpočet](vypocty_diplomova_prace_mean_reverting_regression.ipynb) [Výpočet2](vypocty_diplomova_prace_mean_reverting_regression_bonus.ipynb)

