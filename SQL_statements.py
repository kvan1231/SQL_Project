"""
Made by Kenny Van and Ben Hunter
"""

"""

INSERT STATEMENTS

"""

def Insert_Vehicle(sNo,maker,model,year,colour,tId):
	#vehicle_columns = ["serial no: ", "maker: ", "model: ", "year: ", "color: ", "type id: "]
	vehicle_columns = [sNo,maker,model,year,colour,tId]
	vehicle_statement = "INSERT INTO VEHICLE VALUES ("
	
	for value in vehicle_columns:
		user_input = str(value)
		vehicle_statement = vehicle_statement + "'" + user_input + "',"

	vehicle_statement = vehicle_statement[:-1] + ")"
	return vehicle_statement

def Insert_Person(SIN,name,height,weight,eColor,hColor,addr,gender,birthday):
	person_columns = [SIN,name,height,weight,eColor,hColor,addr,gender,birthday]
	person_statement = "INSERT INTO PEOPLE VALUES ("

	for value in person_columns:
		user_input = str(value)
		person_statement = person_statement + "'" + user_input + "',"

	person_statement = person_statement[:-1] + ")"
	return person_statement

def Insert_Owner(ownID,vID,p):
	owner_columns = [ownID,vID,p]
	owner_statement = "INSERT INTO OWNER VALUES ("

	for value in owner_columns:
		user_input = value
		owner_statement = owner_statement + "'" + user_input + "',"

	owner_statement = owner_statement[:-1] + ")"
	return owner_statement


def Insert_Transaction(tID,sID,bID,vID,sDate,price):

	trans_columns = [tID,sID,bID,vID,sDate,price]
	trans_statement = "INSERT INTO auto_sale VALUES ("

	for value in trans_columns:
		#user_input = input(value)
		if value == sDate:
			trans_statement = trans_statement + "to_date('" + value + "','dd-mon-yyyy'),"
		else:	
			trans_statement = trans_statement + "'" + value + "',"

	trans_statement = trans_statement[:-1] + ")"
	return trans_statement


def Insert_Licence(lNo,SIN,lClass,phLoc,issDate,expDate):
	licence_columns = [lNo,SIN,lClass,phLoc,issDate,expDate]
	licence_statement = "INSERT INTO drive_licence VALUES ("

	for value in licence_columns:
		user_input = str(value)
		if (value == issDate) or (value == expDate):
			licence_statement = licence_statement + "to_date('" + user_input + "','dd-mon-yyyy'),"
		else:
			licence_statement = licence_statement + "'" + user_input + "',"

	licence_statement = licence_statement[:-1] + ")"
	return licence_statement

def Insert_Condition(lNo, cNo):
	condition_columns = [lNo,cNo]
	condition_statement = "INSERT INTO restriction VALUES ("

	for value in condition_columns:
		user_input = str(value)
		condition_statement = condition_statement + "'" + user_input + "',"

	condition_statement = condition_statement[:-1] + ")"
	return condition_statement

def Insert_Violation(tNo,vNo,vID,offNo,violType,violDate,place,desc):
	# violation_columns = ["ticket number: ", "violatior number: ", "vehicle id: ", "officer number: ", \
	# "violation type: ", "violation date: ", "place: ", "description: "]
	violation_columns = [tNo,vNo,vID,offNo,violType,violDate,place,desc]
	violation_statement = "INSERT INTO ticket VALUES ("

	for value in violation_columns:
		user_input = str(value)
		if (value == violDate):
			violation_statement = violation_statement + "to_date('" + user_input + "','dd-mon-yyyy'),"
		else:
			violation_statement = violation_statement + "'" + user_input + "',"

	violation_statement = violation_statement[:-1] + ")"
	return violation_statement

"""

REMOVE STATEMENTS

"""


def Remove_Owner(prevOwnId,vID):
	owner_id = str(prevOwnId)
	vehicle_id = str(vID)
	remove_statement = "DELETE FROM owner WHERE owner_id = {} and vehicle_id = {}".format(owner_id,vehicle_id)
	return remove_statement

if __name__ == "__main__":
    pass	
