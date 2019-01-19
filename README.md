README
=

Requisitos
==
- Python 2.7.x.
- Pip

Setup & running
==
- `pip install -r requirements.txt`
- `python main.py

Configuración de la ejecución
==

Fichero de datos de entrada
===

En formato CSV, se ha de colocar en la carpeta `input_files`. Despues, en `main.py` indicaremos
el nombre de fichero en la variable `filename`.

Lo genera automaticamente el do-file de Stata a partir del RawData de zTree. Dicho fichero bere contener las siguientes columnas:

group,P1,P2,...,PN,type,action,period

Donde:

* group: identificador unico de grupo, que sigue el formato [id_de_sesion][id_de_tratamiento][id_de_grupo]. Por ejemplo, el grupo 1162 corresponde a la sesion numero 11, tratamiento 6 (ENDO_HIGH_FREE), grupo 2 dentro de esa sesion.
* P1..PN: identificador de player dentro del grupo.
* type: tipo de jugador (0: minoria, 1:mayoria)
* action: accion del jugador (0 o 1)
* periodo: numero de perioodo, donde -4..0 son trial rounds.


Parámetros de los datos
===
En `main.py``

* N = numero de jugadores por grupo (típicamente 15).
* NG = numero de grupos unicos en el fichero (si generamos solo para 1 sesion, este parametro valdra tipicamente 3).
* NP = numerto total de periodos incluyendo trials (tipicamente 25)
* show_trials: (True | False), mostrar rondas trial o no


Parámetros de dibujado
===

En `network_drawer.py`:

* SHOW_TITLE: Mostrar o no el título en cada imagen
* BASE_NODE_SIZE y INCREASE_NODE_SIZE: tamaño base (sin links) e incremento por link, respectiamente.
* SHAPES y COLOR: Forma y color en función del type de jugador (ver https://matplotlib.org/api/markers_api.html)
* Método `get_treatment_name`: podemos configurar como generar el prefijo de las imágenes en función del identificador 
único del grupo.`

Resultado de la ejecución
===

En `output_images` habrá 1 imagen por grupo/periodo, llamadas:
 
[nombre_tratamiento]_[id_unico_de_grupo]_[periodo].png


Por ejemplo, para el experimento 'identities', tendremos:

ENDO_HIGH_FIXED_1781_-4.png
ENDO_HIGH_FIXED_1781_-3.png
...
ENDO_HIGH_FIXED_1781_0.png
...
ENDO_HIGH_FIXED_1781_20.png

ENDO_HIGH_FIXED_1782_-4.png
...
ENDO_HIGH_FIXED_1782_20.png

ENDO_HIGH_FIXED_1783_-4.png
...
ENDO_HIGH_FIXED_1783_20.png


Sobre la web de las 'simulaciones'
==

Una vez las imagenes han sido generadas, hay que subirlas al servidor vlineex. La pagina web que las sirve con los controles de animacion esta en:

`/var/www/html/lineex/on/conflict

Aqui hay 2 carpetas, 'one_shot' y 'repeated'. Solo trabajamos con 'repeated' ahora mismo. Dentro de ella hay a su vez 2 carpetas: 

* endogenous: trabajaremos en ella con los tratamientos ENDO_*
* exogenous: trabajaremos en ella con los tratameintos EXO_*

Dentro de cadauna de estas carpetas hay varias subcarpetas/ficheros. Solo nos interesa:

* carpeta 'img': Aqui subiremos directamente las imagenes generadas con el programa de Python.
* index.php: Aqui tendremos que añadir/configurar variables para que muestre las nuevas imagenes/animaciones:

	* Si vamos a crear un nuevo tratamiento, deberemos añadirlo a $menu (linea ~9). Por ejemplo: 

	$menu = [
	    0 => ...,
	    1 => ...,
	    ...
	    5 => '(8-7) HIGH FIXED'
	];

	* En el switch( $treatment) de la linea 36, deberemos añadir al case correspondiente al indice del tratamiento a mostrar en el array $menu (en el ejemplo de arriba seria el 5), el prefijo de las imagenes generadas. El prefijo es el nombre de las imagenes quitando el periodo y la extension png. Para el ejemplo de arriba, los prefijos son "ENDO_HIGH_FIXED_1781", "ENDO_HIGH_FIXED_1782" y "ENDO_HIGH_FIXED_1783". 

	Tendriamos que añadir entonces un case al switch que quedaria asi:

    ```
	case 5:
        $prefix[1] = "ENDO_HIGH_FIXED_1781";
        $prefix[2] = "ENDO_HIGH_FIXED_1782";
        $prefix[3] = "ENDO_HIGH_FIXED_1783";
    ```

    Se accede ahora con el navegador a:

    http://on.lineex.es/confict/repeated





