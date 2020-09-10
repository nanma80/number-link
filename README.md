# Solver of a puzzle game where you need to cancel out numbers. See  [this video](https://www.youtube.com/watch?v=Fzo6MO9Et2A&feature=youtu.be&t=3207)  for a demo of the game used in a Chinese game show.

How to use?
- Install python 3.* with the following packages:
    - colorama
    - primefac from the fork `https://github.com/elliptic-shiho/primefac-fork`. The command to install this fork is `pip3 install git+git://github.com/elliptic-shiho/primefac-fork@master`
- Write the game board in a CSV file, using `,` as the delimiter. Leave the empty cells blank. See `sample.csv` as an example.
- Run `python3 solve.py sample.csv`. Follow the printed instruction to see the result.