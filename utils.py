from docx import Document
from bs4 import BeautifulSoup
import openpyxl


def format_html(data, file_name):
  title = data['title']
  keywords = data['keywords']
  description = data['description']
  content = data['content']
  data_type = data['data_type']
  data_second_type = data['data_second_type']

  # Create a new document


  # 获取HTML内容
  html = content

  # 解析HTML内容
  soup = BeautifulSoup(html, 'html.parser')

  # 创建一个新的Docx文档
  document = Document()
   # Add the title, keywords and description to the document
  document.add_heading(title, level=1)
  document.add_paragraph('Keywords: {}'.format(keywords))
  document.add_paragraph('description: {}'.format(description))
  document.add_paragraph('description: {}'.format(description))
  document.add_paragraph('data_type: {}'.format(data_type))
  document.add_paragraph('data_second_type: {}'.format(data_second_type))
  for tag in soup.find_all():
      text = tag.text
      if tag.name == 'p':
          document.add_paragraph(text)
      elif tag.name == 'h1':
          document.add_heading(text, level=1)
      elif tag.name == 'h2':
          document.add_heading(text, level=2)
      elif tag.name == 'h3':
          document.add_heading(text, level=3)
      # add other tag handling here

  # 保存文档
  document.save('./data/' + str(file_name) + '.docx')

def read_elsx(file_path):
  # 打开Excel文件
  workbook = openpyxl.load_workbook(file_path)

  # 获取工作表名称
  sheet_name = workbook.sheetnames[0]

  # 获取工作表对象
  sheet = workbook[sheet_name]

  # 定义一个空列表
  data = []

  # 获取标题行的值，用于作为字典的键
  headers = [cell.value for cell in sheet[1]]

  # 遍历每一行，并将每一行的数据整理成字典形式，添加到列表中
  for row in sheet.iter_rows(min_row=2):
      # 定义一个空字典，用于存储当前行的数据
      row_data = {}
      for index, cell in enumerate(row):
          # 将单元格的值添加到当前行的数据字典中
          row_data[headers[index]] = cell.value
      # 将当前行的数据字典添加到整个数据列表中
      data.append(row_data)

  # 打印整个数据列表
  return data
