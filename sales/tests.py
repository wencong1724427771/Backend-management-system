from django.test import TestCase

# Create your tests here.
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR)
print(os.path.join(__file__, 'templates'))