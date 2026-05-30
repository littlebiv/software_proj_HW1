HW1 — K-means Clustering
=========================

Project scaffold for the K-means assignment. Implements the assignment in Python and provides a C skeleton ready for completion.

Quick start (Python):

```bash
# Run Python implementation (K=3, iter=100) reading input from a file
python3 src/python/kmeans.py 3 100 < data/sample_input.txt
```

C notes:
- See `src/c/kmeans.c` for a starting skeleton and compile instructions.

Files added:
- `src/python/kmeans.py` — full Python implementation (reads STDIN)
- `src/c/kmeans.c` — C skeleton (argument parsing and input reader)
- `Makefile` — targets for building / running examples
- `data/sample_input.txt` — sample input from the assignment PDF

Follow the PDF requirements (formatting, argument validation, epsilon=0.001, default iter=400).
