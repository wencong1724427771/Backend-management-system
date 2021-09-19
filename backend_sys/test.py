# -*- coding = utf-8 -*-
# @Time: 2021/8/2 8:15
# @Author: Bon
# @File: test.py
# @Software: PyCharm
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR)
print(os.path.join(BASE_DIR, 'statics'))