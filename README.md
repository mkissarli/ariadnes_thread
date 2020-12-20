# Ariadne's Thread

## General Flow
The program starts with a Dash dashboard in your browser where you can select to
start at a company or officer code, and choose your depth. The link would be
(http://127.0.0.1:8050/) by default.

After typing in your company number, we recursively fetch all related companies
and officers using a Breadth First Search (adjusted slightly to account for
different types) with a max depth, because I considered this the simpliest way
to do this. 

We store our json responses in Graph class which is really just a wrapper around
an adjacency matrix, as by inspection, our data seems to be sparsely populated,
and this tends to be a good way to represents sparse graphs.

From here we create an object Dash can understand, and calculate the Risk for 
each company, and send this object for rendering.

## Future Considerations

Ideally, we would add some more unit tests. We would also improve the GUI
interface as while it is functional, it isn't very pretty, nor very feature full.

I would also likely change the risk function, to something an economist would
recommend, as with the limited data from Companies Houses I'm not sure how best
to calculate risk.

## How to run

Ensure python 3.7 is installed. Then run

```pip install dash dash-cytograph dotenv requests ```

to install dependencies. 

Now to run the server run (while in the project root)

```python src/app.py ```

and point your browser to

```http://127.0.0.1:8050```

