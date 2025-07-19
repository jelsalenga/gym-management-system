import sys 
from login import *

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window  = Login()
    window.show()
    sys.exit(app.exec_())