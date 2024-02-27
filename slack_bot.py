from slack_logic.util import *
from slack_logic.query import *

if __name__ == "__main__":
    SocketModeHandler(app, os.environ[APP_TOKEN]).start()