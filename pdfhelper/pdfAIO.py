import PyPDF2
import os

from PyPDF2 import PdfReader, PdfWriter

BASEPATH = os.getcwd() + "/pdfhelper/"
# 打开多个PDF文件
pdf_files = [BASEPATH + "1.pdf", BASEPATH + "2.pdf"]
pdf_readers = []
for pdf_file in pdf_files:
    pdf_readers.append(PdfReader(pdf_file))

# 创建一个新的PDF写入对象
pdf_writer = PdfWriter()

# 将每个PDF文件的所有页面添加到新的PDF文件中
page_num = 0
for pdf_reader in pdf_readers:
    for page in pdf_reader.pages:
        pdf_writer.add_outline_item(f"{page_num}", page_num)
        page_num += 1
        pdf_writer.add_page(page)

# 将合并后的PDF文件写入磁盘
with open(BASEPATH + "merged_file.pdf", "wb") as f:
    pdf_writer.write(f)
