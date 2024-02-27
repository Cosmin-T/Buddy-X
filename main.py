#main.py

from logic.util import *
from logic.model import *
from logic.settings import *
from logic.navigation import *


if __name__ == '__main__':
    apply_settings('x-chat', CENTERED)
    process()
    side()