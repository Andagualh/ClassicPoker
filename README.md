# ClassicPoker
A simple Python script that builds an English Deck, deals hands, rate each hand and compares them. This is a script based on console use rather than featuring any GUI,
it will handle the creation of an English Deck of 52 non-repeated cards, the dealing of said hands to the number of players selected by the user (Up to 10 players due to
the nature of the deck itself), the rating and evaluation of each player hand and the resolution of the rounds.

## Requirements
- Python 3.8 (Might work in any version of Python 3)
- Pip Library Random
- Pip Library itertools
- Pip Library Enum
- Pip Library Collections
- Pip Library Copy

The installation of any Pip Library can be done with the following command:

```console
pip install library
```
## Execution
To execute this script we have to assume you already met the Requirements on your execution environment. Just executing the ``.py`` file should be enough to make it work.
On a terminal this can be done by using the following command:

```console
python poker.py
```
##Code Structure
The script counts with various class on it that should be in mind when reading the code:

- Suit Enumerate
- Value Enumerate
- Card Object
- Deck Object
- Hand Object
- Poker: Main program.
- TestCases: Test cases for single methods or functionalities.

Additionally the script itself has noted a main execution sentences that calls upon the Poker and TestCases classes depending on user selection.

## User Manual
The first thing that one will get prompted after the execution, will be the selection mode which has two options:
- Program Execution, noted with a 1.
- Test Case Execution, noted with a 2.

Selecting program execution will ask for the number of desired players, which only can be up to 10 due to deck structure limitations of the game.
After selecting the number of players, the program will ask to start the round and will return the result of the round.
The result of a round has two possible outcomes:
- A player won the round on its own and his hand will be prompted in the trace along with the kind of winning hand or sets used.
- There was a tie, both players hands will be prompted in the trace and the kind of winning hand or sets used.

After a round has been resolved, the program will ask to start another round with the same number of players.

Test Case Execution will execute the test written during the making of this program.

## Original Statement of the problem
Escribir un programa que ejecute rondas de poker y determine qué mano es la ganadora. Detalles:
 - El número de jugadores debe poder ser variable.
- La solución debe cubrir una de las variantes de poker (como el clásico de 5 cartas), pero debe ser extensible a futuro a texas hold-em y omaha hi/lo.
- La ejecución de la mano solo debe cubrir el reparto de cartas y la resolución de la mano ganadora. No hay interacción por parte de los jugadores ni, por tanto, apuestas o contabilidad.
- Debo ser capaz de jugar varias rondas sin reiniciar el programa.

### Translation:
Write a program that runs different Poker rounds and rate which hand is the winner one. Details:
- The number of players must be variable.
- The proposed solution must cover one Poker variant (Like the Classic 5 Cards one), but it should be possible to extend it on the future to Texas Hold-em and Omaha Hi-Lo.
- The program only should deal the hands and choose which is the winner one. There is no player interaction of any kind.
- The program has to run different rounds without requiring a restart.

## Approach explanation and possible improvements
This is a heavily object based approach to the problem instead of a purely mathematical one. While a mathematical solution purely based on a variable reward depending on
the value of the cards could have been much shorter, I felt like it would be trickier for me to understand when reading the code in the future. I also tried to incentivize 
modularity between methods, trying to write certain methods with reusable code so extensibility might be easier.

Test Cases might be improved by using a code coverage library, which I didn't had enough time to do, this might be one improvement to do in the future. Other improvement would be within the tie resolution code, which is quite messy due to the unique approach used.

While this is not a justification of my code flaws, I felt right to communicate my thoughts at tackling this problem since it would be easier to answer frequent questions that
might arise from reading the .py file. I am well aware that my approach might had the opposite effect of my intentions, I will read and review any critique made on this piece of
code.

## Code Snippets used
Some of the code present in this script is heavily inspired by others works, here's a list of URLs consulted during the making of this script:

- [Diego Salinas article in Towards Data Science about Texas Hold'Em scoring](https://towardsdatascience.com/poker-with-python-how-to-score-all-hands-in-texas-holdem-6fd750ef73d)
- [Toby Speigh answer in a StackExchange question](https://codereview.stackexchange.com/questions/128702/poker-hands-in-python)
- [Jim Mischel answer in a StackOverFlow question](https://stackoverflow.com/questions/42380183/algorithm-to-give-a-value-to-a-5-card-poker-hand)
- [Unknown Author Card Player reference sheet for hand ranking](https://www.cardplayer.com/rules-of-poker/hand-rankings)

