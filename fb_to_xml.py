import firebirdsql
import xml.etree.ElementTree as ET

firebird_conn = firebirdsql.connect(
    host='ip adress',
    user='db username',
    password='password db username',
    database='name bd'
)

firebird_cursor = firebird_conn.cursor()

firebird_query = "SELECT * FROM table_used"
firebird_cursor.execute(firebird_query)

root = ET.Element("data")

for row in firebird_cursor.fetchall():
    item = ET.Element("item")
    root.append(item)
    for field_name, field_value in zip(firebird_cursor.description, row):
        field = ET.Element(field_name[0])
        field.text = str(field_value)
        item.append(field)

xml_data = ET.ElementTree(root)
xml_data.write("output.xml")

firebird_cursor.close()
firebird_conn.close()

print("The data was successfully converted to xml and saved to the output.xml file")
