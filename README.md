# convex-polygon

Because I hate technical tests which serve absolutely zero use in day-to-day practical work as a software engineer, only to test if I have too much time to waste.

# Usage

Linux:

* `python main.py`

## Design

`main.py`: Presentation layer, using `print` and `input`.
`shape.py`: Houses `Shape` class along with all member functions.

`Shape` class deals specifically with logic, whereas the main interface code is contained within main.py. Reason for doing this is to separate presentation from business/software logic, so Shape can be reused in another interface in the future.

Code for convex shape generation and validation derived from ChatGPT and internet sources.

---

TODO:
* Clean up
* Re-write algorithm to be working
* Implement better tests
