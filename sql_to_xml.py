import pymysql
import xml.etree.ElementTree as ET

connection = pymysql.connect(
    host='ip adress',
    user='db username',
    password='password db username',
    database='name bd'
)

cursor = connection.cursor()

sql_query = "SELECT * FROM table_used"
cursor.execute(sql_query)

root = ET.Element("data")

for row in cursor.fetchall():
    item = ET.Element("item")
    root.append(item)
    for idx, col in enumerate(cursor.description):
        field = ET.Element(col[0])
        field.text = str(row[idx])
        item.append(field)

xml_data = ET.ElementTree(root)
xml_data.write("output.xml")

cursor.close()
connection.close()

print("The data was successfully converted to xml and saved to the output.xml file")
