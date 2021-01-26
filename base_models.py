import sys
# import xlsxwriter
import pickle

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


def result_code():
    print("in")
    res = [200, 1,  {"clinic_code": 200, "result_oode":300, "Id": 2, "StatusFlag": 0}]
    out_register_info = res[2]
    if res[0] == 200:
        dto = {
        }
        if res[2]['StatusFlag'] == 0:
            # 未挂号, 需要进行挂号处理
            sync_res = [200, 1, 1,{"clinic_code": 200, "result_oode":300}]
            if sync_res[0] == 200:
                result_data = sync_res[2]
                if result_data:
                    register_no = result_data.get('clinic_code', None)
                    print(register_no)
                    dto.update({"RegisterNo": register_no})
                    # result_code = 4则不要update OutRegisters里的RegisterNo
                    result_code = result_data.get('result_code', None)
                    print("inout")

    print("out")

def try_pickle():
    f = open("test.pkl", "rb")
    data = pickle.load(f)
    print(data)

if __name__ == '__main__':
    pass
    try_pickle()
