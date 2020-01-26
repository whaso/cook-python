import sys
import xlsxwriter

def tryPyQt5():
    from PyQt5 import QtWidgets
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    widget.resize(400, 100)
    widget.setWindowTitle('This is a demo for PyQt Widget')
    widget.show()

    exit(app.exec_())

def tryXlsxwriter():
    workExcel = xlsxwriter.Workbook('excel_name')
    workSheet = workExcel.add_worksheet('sheet_name')
    workFormat = workExcel.add_format({
        'bold': True,

    })

# Pr1 Pr2
def trySys():

    batch = sys.argv  # list['*.py', 'Pr1', 'Pr2'...]
    git_m = sys.argv[1]

    print('sys.argv[1]', git_m, 'type:', type(git_m))
    for i in git_m:
        print(i)

    print('batch: ', batch, 'type: ', type(batch))


if __name__ == '__main__':
    # trySys()
    tryPyQt5()

