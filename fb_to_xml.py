import firebirdsql
import xml.etree.ElementTree as ET

# Connecting to a Firebird database
firebird_conn = firebirdsql.connect(
    host='ip adress',
    user='db username',
    password='password db username',
    database='name bd'
)

# Creating an object to execute SQL queries
firebird_cursor = firebird_conn.cursor()

# Running an SQL query to retrieve data from Firebird
firebird_query = "SELECT * FROM table_used"
firebird_cursor.execute(firebird_query)

# Creating an xml root element
root = ET.Element("data")

# Extracting data from a query result and creating xml elements
for row in firebird_cursor.fetchall():
    item = ET.Element("item")
    root.append(item)
    for field_name, field_value in zip(firebird_cursor.description, row):
        field = ET.Element(field_name[0])
        field.text = str(field_value)
        item.append(field)

# Creating an xml document and writing it to a file
xml_data = ET.ElementTree(root)
xml_data.write("output.xml")

# Closing a connection to a Firebird database
firebird_cursor.close()
firebird_conn.close()

print("The data was successfully converted to xml and saved to the output.xml file")
