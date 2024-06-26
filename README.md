# magicrailroad

RailNL groepsproject, Algoritme en Heuristieken.

Deze case gaat over de dienstregeling voor treinverkeer, specifieker gezegd het maken van de lijnvoering van intercitytreinen.
Dat betekent dat er binnen een 120 een aantal trajecten uitgezet worden. Een traject is een route van sporen en stations waarover treinen heen en weer rijden. Een traject mag niet langer zijn dan het 120 minuten. De doelfunctie (K) wordt gemeten met het percentage van gereden connecties en de hoeveelheid trajecten. Hoe hoger de K, hoe beter de score.


**Aan de slag**

Deze code is geschreven in Python 3.10.8. Hieronder staan alle benodigde packages om de code succesvol te draaien. Deze zijn te installeren met de volgende terminal input:

pip install geopandas

pip install shapely

**Gebruik**

Voor een kaart van Nederlandse intercity routes, roep dan het volgende aan:

python main.py data/StationsNationaal.csv data/ConnectiesNationaal.csv output_file.csv


Voor een kaart van Noord- en Zuid-Hollandse intercity routes, roep dan het volgende aan:

python main.py data/StationsHolland.csv data/ConnectiesHolland.csv output_file.csv

**Structuur**

De hierop volgende lijst beschrijft de belangrijkste mappen en files in het project, en waar je ze kan vinden:

/code: bevat alle code van dit project

/code/algorithms: bevat de code voor algoritmes

/code/classes: bevat de drie benodigde classes voor deze case

/code/visualize: bevat de code voor de visualisatie

/data: bevat de verschillende databestanden (de stations en connecties)

/visualizations: bevat de gevisualiseerde resultaten


**Auteurs**

Pierre Jacod

Arne Verwaaijen

Sofie van der Westen
