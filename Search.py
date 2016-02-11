"""
Made by Kenny Van and Ben Hunter
"""

def Search_Driver_Licence(lNo):
	#List the name, licence_no, addr, birthday, driving class, driving_condition, and the expiring_date of a driver

	user_input = str(lNo)
	
	search_statement = "SELECT p.name, d.licence_no, p.addr, p.birthday, d.class, r.r_id, d.expiring_date \
FROM people p, drive_licence d, restriction r \
WHERE d.licence_no = {} AND p.sin = d.sin AND r.licence_no = d.licence_no".format(user_input,user_input)

	return search_statement


def Search_Driver_Name(dName):
	user_input = str(dName)
	modified_input = "%" + user_input.title().replace(" ","%") + "%"

	search_statement = "SELECT p.name, d.licence_no, p.addr, p.birthday, d.class, r.r_id, d.expiring_date \
FROM people p, drive_licence d, restriction r \
WHERE p.name like '{}' AND p.sin = d.sin AND r.licence_no = d.licence_no".format(modified_input)

	return search_statement


def Search_Viol_Licence(dNum):
	#List all violation records received by a person

	user_input = str(dNum)

	search_statement = "SELECT * FROM ticket t JOIN (SELECT p.sin FROM people p, drive_licence d \
WHERE p.sin = d.sin AND d.licence_no = {}) p1 on p1.sin = t.violator_no".format(user_input)

	return search_statement

#select * from ticket t join (SELECT p.sin from people p, drive_licence d where p.sin=d.sin and d.licence_no = 0000001) p1 on p1.sin = t.violator_no 


def Search_Viol_SIN(SIN):
	user_input = str(SIN)

	search_statement = "SELECT * FROM ticket WHERE violator_no = {}".format(user_input)

	return search_statement


def Search_Vehic_History(serNo):
	user_input = str(serNo)

	search_statement = "SELECT v.serial_no, count(DISTINCT transaction_id), avg(price), count(DISTINCT t.ticket_no) \
FROM vehicle v, auto_sale a1, ticket t \
WHERE t.vehicle_id (+) = v.serial_no AND a1.vehicle_id(+) = v.serial_no AND v.serial_no = {} \
GROUP BY v.serial_no".format(user_input)

	return search_statement

def Search_Owner(sID, vID):
	seller = str(sID)
	vehicle = str(vID)

	search_statement = "SELECT o.owner_id FROM owner o WHERE owner_id = {} AND vehicle_id = {} AND is_primary_owner = 'y'".format(seller,vehicle)

	return	search_statement