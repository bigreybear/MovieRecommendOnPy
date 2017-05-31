import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import sys
import movieRecom


if __name__ == '__main__':
    src_dir = './ml-latest-small/ml-latest-small/'
    # movieRecom.factory(src_dir)
    movieRecom.construct_avg_rat()
