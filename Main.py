"""
Made by Kenny Van and Ben Hunter
"""

import cx_Oracle
import getpass
import sys
import re
import SQL_statements
import Search
import npyscreen as np
import DateArray

curs = 0
file_table = "p1_setup.sql"
file_data = "p1_data.sql"
results = list()

def openSQL(file_name):
    # read in the sql file to execute the create table statements
    SQL_File = open(file_name, 'r')
    SQL_statements = SQL_File.read()
    SQL_File.close()

    #cursor = connection.cursor()
    cursor = curs

    # separate the code into lines where semicolons and / are
    SQL_statements = SQL_statements.strip()
    statements = re.split(';|/',SQL_statements)

    # run each command
    for command in statements:
            # only take in lines that arent empty
            # if (len(command) > 0):
            command = command + ";"
            command = command.strip()
            if (command[0] != "*") and (command[0] != ";"):
                    try:
                            command = command[:-1]

                            # print(command)
                            cursor.execute(command)

                    except cx_Oracle.DatabaseError as exc:
                            error, = exc.args
                            print( sys.stderr, "Oracle code:", error.code)
                            print( sys.stderr, "Oracle message:", error.message)

# Opening Screen
class MainMenu(np.Form):

    def create(self):
        self.name = "CMPUT 291 Auto Registration System --- Kenny Van and Ben Hunter"
        self.add(np.FixedText, editable = False, value = "Log into Oracle Database to proceed")
        self.nextrelx -= 1
        self.nextrely += 1
        def login_button(*args):
            self.parentApp.switchForm("LOGIN")

        self.login_button = self.add(np.ButtonPress, name = "Login")
        self.login_button.whenPressed = login_button

# Code to take login information
class login(np.ActionPopup):
    def create(self):
            self.userName = self.add(np.TitleText, name = "Username: ")
            self.password = self.add(np.TitlePassword, name="Password: ")

  
    def on_ok(self):
        self.conString=''+self.userName.value+'/' + self.password.value +'@gwynne.cs.ualberta.ca:1521/CRS'
        try:
            self.connection = cx_Oracle.connect(self.conString) 
            global curs
            curs = self.connection.cursor()
            """
            openSQL(file_table)
            openSQL(file_data)
            """
            
            self.parentApp.switchForm("OPEN")
        except:
           self.name = "Invalid Username/Password - Please Try Again"

    def on_cancel(self):
        self.parentApp.switchFormPrevious()

# Main menu screen
class OpenScreen(np.Form):

    def create(self):
        self.name = "CMPUT 291 Auto Registration System --- Kenny Van and Ben Hunter"
        self.add(np.FixedText, editable = False, value = "Select an Option")
        self.nextrely += 1
        self.nextrelx -= 2

        def Vreg_button(*args):
            self.parentApp.switchForm("VREG")

        def trans_button(*args):
            self.parentApp.switchForm("ATRANS")

        def DLreg_button(*args):
            self.parentApp.switchForm("DLREG")
            
        def Vrecord_button(*args):
            self.parentApp.switchForm("VREC")

        def search_button(*args):
            self.parentApp.switchForm("SEARCH")

        # to find use ctrl+F #>>>Vechicle registration<<<#
        self.Vreg_button = self.add(np.ButtonPress, name = "New Vehicle Registration")
        self.Vreg_button.whenPressed = Vreg_button

        # to find use ctrl+F #>>>Auto Transaction<<<#
        self.trans_button = self.add(np.ButtonPress, name = "Auto Transaction")
        self.trans_button.whenPressed = trans_button

        # to find use ctrl+F #>>>Driver Licence Registration<<<#
        self.DLreg_button = self.add(np.ButtonPress, name = "Drivers Licence Registration")
        self.DLreg_button.whenPressed = DLreg_button

        # to find use ctrl+F #>>>Violation Recond<<<#
        self.Vrecord_button = self.add(np.ButtonPress, name = "Issue Violation Record")
        self.Vrecord_button.whenPressed = Vrecord_button

        # to find use ctrl+F #>>>SEARCH<<<#
        self.search_button = self.add(np.ButtonPress, name = "Search database")
        self.search_button.whenPressed = search_button


#####################################################################################################################
#                                              INSERTING DATA TO DATABASE                                           #
#####################################################################################################################

#>>>Vehicle registration<<<#
class veReg(np.ActionForm):

    def create(self):
        self.add(np.FixedText, editable = False, value = "Please Fill Out All Fields to Register a Vehicle")
        self.nextrely += 1
        self.serialNo = self.add(np.TitleText, name = "Serial # :")
        self.maker = self.add(np.TitleText, name = "Maker    :")
        self.model = self.add(np.TitleText, name = "Model    :")
        self.year = self.add(np.TitleCombo, name = "Year     :", values = DateArray.dates)
        self.color = self.add(np.TitleText, name = "Color    :")
        self.typeID = self.add(np.TitleText, name = "Type ID  :")

        self.nextrely += 1
        self.nextrelx -= 2
        
        def registerButton(*args):
            self.vehicle_statement = SQL_statements.Insert_Vehicle(self.serialNo.value,self.maker.value,\
                                   self.model.value,self.year.value,self.color.value,self.typeID.value)
            try:
                curs.execute(self.vehicle_statement)
                self.name = "Vehicle Registered Successfully"
            except cx_Oracle.DatabaseError as exc:
                error, = exc.args
                if error.code == 1:
                    self.parentApp.switchForm("SERIALERROR")
                    #self.name = "Serial Number Already In Database, Please Check Input."

        self.registerButton = self.add(np.ButtonPress, name = "Register")
        self.registerButton.whenPressed = registerButton
        self.nextrely += 1

        def ownerButton(*args):
            self.parentApp.switchForm("OWNER")
            
        self.ownerButton = self.add(np.ButtonPress, name = "Add Owner")
        self.ownerButton.whenPressed = ownerButton           

    def on_cancel(self):
        self.parentApp.switchForm("OPEN")

    def on_ok(self):
        self.parentApp.switchForm("OPEN")

#>>>Auto Transaction<<<#
class autoTrans(np.ActionForm):

    def create(self):
        
        self.add(np.FixedText, editable = False, value = "Please Fill In All Fields to Add an Auto-Transaction")
        self.nextrely += 1
        self.transID = self.add(np.TitleText, name = "TransID   :")
        self.sellerID = self.add(np.TitleText, name = "SellerID  :")
        self.buyerID = self.add(np.TitleText, name = "BuyerID   :")
        self.vehicleID = self.add(np.TitleText, name = "VehicleID :")
        self.saleDate = self.add(np.TitleDateCombo, name = "Sale Date :")
        self.price = self.add(np.TitleText, name = "Price     :")
        self.nextrely += 1
        self.nextrelx -= 2

        def submitButton(*args):
            try:
                self.date = self.saleDate.value.strftime("%d-%b-%Y")

                self.transaction_statement= SQL_statements.Insert_Transaction(self.transID.value, self.sellerID.value, self.buyerID.value, self.vehicleID.value, self.date,self.price.value)
                self.remove_statement = SQL_statements.Remove_Owner(self.sellerID.value,self.vehicleID.value)

                self.query = Search.Search_Owner(self.sellerID.value, self.vehicleID.value)
                curs.execute(self.query)
                rows = curs.fetchall()
                if len(rows) > 0:

                    try:
                        curs.execute(self.transaction_statement)
                        curs.execute(self.remove_statement)
                        self.name = "Transaction Successful"
                    except cx_Oracle.DatabaseError as exc:
                        error, = exc.args
                        if error.code == 2291:
                            self.parentApp.switchForm("TRANSERROR") 

                else:
                    self.parentApp.switchForm("SELLERROR")

            except AttributeError:
                self.parentApp.switchForm("DATEERROR")

        self.submitButton = self.add(np.ButtonPress, name = "Complete Transaction")
        self.submitButton.whenPressed = submitButton
        self.nextrely += 1

        def personButton(*args):
            self.parentApp.switchForm("ADDPERSON")
            
        self.personButton = self.add(np.ButtonPress, name = "Add Person")
        self.personButton.whenPressed = personButton

       
    def on_cancel(self):
        self.parentApp.switchFormPrevious()
    def on_ok(self):
        self.parentApp.switchFormPrevious()


#>>>Driver licence registration<<<#
class dlReg(np.ActionForm):
    def create(self):
        self.add(np.FixedText, editable = False, value = "Complete These Fields to Register a Driver's Licence")
        self.nextrely += 1
        self.licenceNumber = self.add(np.TitleText, name = "Licence #   :")
        self.sin = self.add(np.TitleText, name = "Sin         :")
        self.licenceClass = self.add(np.TitleText, name = "Class       :")
        self.photoLocation = self.add(np.TitleText, name = "Photo       :")
        self.issuingDate = self.add(np.TitleDateCombo, name = "Date Issued :")
        self.expDate = self.add(np.TitleDateCombo, name = "Expiry Date :")
        self.nextrely += 1
        self.nextrelx -= 2

        def submitButton(*args):
            try:
                self.iDate = self.issuingDate.value.strftime("%d-%b-%Y")
                self.eDate = self.expDate.value.strftime("%d-%b-%Y")

                self.licence_statement = SQL_statements.Insert_Licence(self.licenceNumber.value,\
                                         self.sin.value,self.licenceClass.value,\
                                         self.photoLocation.value,self.iDate,self.eDate)
                try:
                    curs.execute(self.licence_statement)
                    self.name = "Successfully Registered"
                
                except cx_Oracle.DatabaseError as exc:
                    error, = exc.args
                    if error.code == 2291:
                        self.parentApp.switchForm("TRANSERROR")
                    elif error.code == 1:
                        self.parentApp.switchForm("PERSONERROR")        

            except AttributeError:
                self.parentApp.switchForm("DATEERROR") 


        self.submitButton = self.add(np.ButtonPress, name = "Register")
        self.submitButton.whenPressed = submitButton
        self.nextrely += 1

        def personButton(*args):
            self.parentApp.switchForm("ADDPERSON")
            
        self.personButton = self.add(np.ButtonPress, name = "Add Person")
        self.personButton.whenPressed = personButton

        self.nextrely +=1

        def restButton(*args):
            self.parentApp.switchForm("ADDCOND")
            
        self.restButton = self.add(np.ButtonPress, name = "Add Condition")
        self.restButton.whenPressed = restButton

    def on_cancel(self):
        self.parentApp.switchFormPrevious()

    def on_ok(self):
        self.parentApp.switchFormPrevious()

#>>>Violation Record<<<#
class vRecord(np.ActionForm):
    def create(self):
        self.ticketNumber = self.add(np.TitleText, name = "Ticket #   :")
        self.violatorNumber = self.add(np.TitleText, name = "Violator # :")
        self.vehicleID = self.add(np.TitleText, name = "Vehicle ID :")
        self.officerNumber = self.add(np.TitleText, name = "Officer #  :")
        self.violationType = self.add(np.TitleText, name = "Type       :")
        self.violationDate = self.add(np.TitleDateCombo, name = "Date       :")
        self.loc = self.add(np.TitleText, name = "Location   :")      
        self.desc = self.add(np.TitleText, name = "Desc.      :")
        self.nextrely += 1
        self.nextrelx -= 2

        def submitButton(*args):     
            try:
                self.date = self.violationDate.value.strftime("%d-%b-%Y")

                violation_statement = SQL_statements.Insert_Violation(self.ticketNumber.value,self.violatorNumber.value,\
                                self.vehicleID.value,self.officerNumber.value,self.violationType.value,self.date,self.loc.value,self.desc.value)

                try:
                        curs.execute(violation_statement)
                        self.name = "Violation Issued"
                except cx_Oracle.DatabaseError as exc:
                        error, = exc.args
                        if error.code == 2291:
                            self.parentApp.switchForm("TRANSERROR") 
                            #2291 for missing vehicle

            except AttributeError:
                self.parentApp.switchForm("DATEERROR")

    
        self.submitButton = self.add(np.ButtonPress, name = "Issue Violation Record")
        self.submitButton.whenPressed = submitButton
        
    def on_cancel(self):
        self.parentApp.switchFormPrevious()

#####################################################################################################################
#                                              FUNCTIONS TO ADD OWNER/PERSON                                        #
#####################################################################################################################

#Ownership
class owner(np.ActionForm):
    def create(self):
        self.add(np.FixedText, editable = False, value = "Enter Information About The Vehicle's Owner")
        self.nextrely += 1
        self.ownerID = self.add(np.TitleText, name = "Owner ID   : ")
        self.nextrely += 1
        self.vehicleID = self.add(np.TitleText, name = "Vehicle ID : ")
        self.nextrely += 1
        self.nextrelx -= 2
        self.isPrimary = self.add(np.TitleSelectOne, max_height=4, value = [1,], name="  Primary Owner :", values = ["Yes","No"], scroll_exit=True)  
 
        def submitButton(*args):
            isP = 'n'
            if(self.isPrimary.value == [0]):
                isP = 'y'
            self.owner_statement = SQL_statements.Insert_Owner(self.ownerID.value,self.vehicleID.value,isP)
            try:
                curs.execute(self.owner_statement)
                self.parentApp.switchForm("VREG")
            except cx_Oracle.DatabaseError as exc:
                self.parentApp.switchForm("ERROR")                
          
        self.nextrely += 1
        self.submitButton = self.add(np.ButtonPress, name = "Add")
        self.submitButton.whenPressed = submitButton

    def on_cancel(self):
        self.parentApp.switchForm("VREG")

    def on_ok(self):
        self.parentApp.switchFormPrevious()

class addperson(np.ActionForm):
    def create(self):
        self.add(np.FixedText, editable = False, value = "Enter Information About The Person")
        self.nextrely += 1
        self.sin = self.add(np.TitleText, name = "SIN        : ")
        self.name = self.add(np.TitleText, name = "Name       : ")
        self.height = self.add(np.TitleText, name = "Height     : ")
        self.weight = self.add(np.TitleText, name = "Weight     : ")
        self.eyecolor = self.add(np.TitleText, name = "Eye Color  : ")
        self.haircolor = self.add(np.TitleText, name = "Hair Color : ")
        self.addr = self.add(np.TitleText, name = "Address    : ")
        self.gender = self.add(np.TitleText, name = "Gender     : ")
        self.birthday = self.add(np.TitleDateCombo, name = "Birthday   : ")
        self.nextrely += 1
        self.nextrelx -= 2
 
        def submitButton(*args):

            try:
                self.bDate = self.birthday.value.strftime("%d-%b-%Y")

                self.person_statement = SQL_statements.Insert_Person(self.sin.value,\
                                         self.name.value,self.height.value,\
                                         self.weight.value,self.eyecolor.value,\
                                         self.haircolor.value, self.addr.value,\
                                         self.gender.value, self.bDate)
                try:
                    curs.execute(self.person_statement)
                    self.parentApp.switchFormPrevious()
                except cx_Oracle.DatabaseError as exc:
                    self.parentApp.switchForm("ERROR")

            except AttributeError:
                self.parentApp.switchForm("DATEERROR")

        self.nextrely += 1
        self.submitButton = self.add(np.ButtonPress, name = "Add")
        self.submitButton.whenPressed = submitButton

    def on_cancel(self):
        self.parentApp.switchFormPrevious()
    
    def on_ok(self):
        self.parentApp.switchFormPrevious()

# Restriction adding
class addrestriction(np.ActionForm):
    def create(self):
        self.add(np.FixedText, editable = False, value = "Enter Information About The Licence Owner's Condition")
        self.nextrely += 1
        self.licID = self.add(np.TitleText, name = "Licence ID                           : ")
        self.nextrely += 1
        self.condID = self.add(np.TitleText, name = "Condition ID (0800 for no condition) : " )
        self.nextrely += 1
        
        def submitButton(*args):
            self.restrict_statement = SQL_statements.Insert_Condition(self.licID.value,self.condID.value)
            try:
                curs.execute(self.restrict_statement)
                self.name = "Condition Added"
            except cx_Oracle.DatabaseError as exc:
                self.parentApp.switchForm("ERROR")                
          
        self.nextrely += 1
        self.submitButton = self.add(np.ButtonPress, name = "Add")
        self.submitButton.whenPressed = submitButton

    def on_cancel(self):
        self.parentApp.switchFormPrevious()

    def on_ok(self):
        self.parentApp.switchFormPrevious()

#####################################################################################################################
#                                                      SEARCH FUNCTIONS                                             #
#####################################################################################################################

#>>>SEARCH<<<#
class search(np.ActionForm):
    def create(self):
        self.name = "Search"
        self.add(np.FixedText, editable = False, value = "Search From one of the Follwing Categories")
        self.nextrely += 1
        self.nextrelx -= 2
        
        # for license or driver data
        def ldData_button(*args) :
           self.parentApp.switchForm("LDDATA")
        # for violation records
        def violData_button(*args) :
           self.parentApp.switchForm("VIOLDATA")
        # for vehicle history
        def vhist_button(*args) :
           self.parentApp.switchForm("VHISTDATA")
           
        self.ldData_button = self.add(np.ButtonPress, name = "Licence or Driver Data")
        self.ldData_button.whenPressed = ldData_button
        self.violData_button = self.add(np.ButtonPress, name = "Violation Records")
        self.violData_button.whenPressed = violData_button
        self.vhist_button = self.add(np.ButtonPress, name = "Vehicle History")
        self.vhist_button.whenPressed = vhist_button
        #12341234
    
    def on_cancel(self):
        self.parentApp.switchFormPrevious()

class lDSearch(np.ActionPopup):
    def create(self):
        self.name = ""
        self.which = self.add(np.TitleSelectOne, max_height=4, name="Search Via:", values = ["Licence Number","Given Name"], scroll_exit=True)  

    def on_ok(self):
        if (self.which.value == [0]):
            self.parentApp.switchForm("LNSEARCH")
        else:
            self.parentApp.switchForm("GNAMESEARCH")

    def on_cancel(self):
        self.parentApp.switchFormPrevious()

class violationSearch(np.ActionPopup):
    def create(self):
        self.name = ""
        self.which = self.add(np.TitleSelectOne, max_height=4, name="Search Via:", values = ["Licence Number","Sin"], scroll_exit=True)  

    def on_ok(self):
        if (self.which.value == [0]):
            self.parentApp.switchForm("LN2SEARCH")
        else:
            self.parentApp.switchForm("SINSEARCH")
        
    def on_cancel(self):
        self.parentApp.switchFormPrevious()

class vehicleHistorySearch(np.ActionForm):
    def create(self):
        self.serNo = self.add(np.TitleText, name = "Serial # :")
        self.nextrely += 1
        self.nextrelx -= 2
        
        def searchButton(*args):
            vehicle_history_search = Search.Search_Vehic_History(self.serNo.value)
            results = list()
            
            try:
                curs.execute(vehicle_history_search)
                rows = curs.fetchall()
                
                if len(rows) > 0:
                    results.append("vehicle id, number of transactions, average price, number of violations")
                
                    for row in rows:
                        row = str(row)
                        row = row.strip()
                        results.append(row)
                else:
                    results = list()
                    results.append("No results found")

                F = np.Form(name = "Query")
                F.add(np.TitlePager,name = "Results:",values = results)
                F.edit()


            except cx_Oracle.DatabaseError as exc:
                self.parentApp.switchForm("ERROR")

        self.searchButton = self.add(np.ButtonPress, name = "Search")
        self.searchButton.whenPressed = searchButton
          

    def on_cancel(self):
        self.parentApp.switchFormPrevious()

class givenNameSearch(np.ActionForm):

        def create(self):
            self.gName = self.add(np.TitleText, name = "Given Name :")
            self.nextrely += 1
            self.nextrelx -= 2
                
            def searchButton(*args):
                name_data_search = Search.Search_Driver_Name(self.gName.value)
                results = list()
                
                try:
                    curs.execute(name_data_search)
                    rows = curs.fetchall()
                    
                    if len(rows) > 0:
                        results.append("name, licence number, address, birthday, driving class, driving condition, expiring date")
                        
                        for row in rows:
                            row = str(row)
                            row = row.strip()
                            results.append(row)
                    else:
                        results = list()
                        results.append("No results found")

                    F = np.Form(name = "Query")
                    F.add(np.TitlePager,name = "Results:",values = results)
                    F.edit()

                except cx_Oracle.DatabaseError as exc:
                    self.parentApp.switchForm("ERROR")

            self.searchButton = self.add(np.ButtonPress, name = "Search")
            self.searchButton.whenPressed = searchButton
                
        def on_cancel(self):
                self.parentApp.switchFormPrevious()

class licNumSearch(np.ActionForm):

        def create(self):
            self.serNo = self.add(np.TitleText, name = "Licence # :")
            self.nextrely += 1
            self.nextrelx -= 2
                
            def searchButton(*args):
                licence_data_search = Search.Search_Driver_Licence(self.serNo.value)
                results = list()
                try:
                    curs.execute(licence_data_search)
                    rows = curs.fetchall()    
                    
                    if len(rows) > 0:
                        results.append("name, licence number, address, birthday, driving class, driving condition, expiring date")
                       
                        for row in rows:
                            row = str(row)
                            row = row.strip(" ")
                            results.append(row)
                            
                    else:
                        results = list()
                        results.append("No results found")
                    
                    F = np.Form(name = "Query:")
                    F.add(np.TitlePager,name = "Results:", values = results)
                    F.edit()


                except cx_Oracle.DatabaseError as exc:
                    self.parentApp.switchForm("ERROR")

            self.searchButton = self.add(np.ButtonPress, name = "Search")
            self.searchButton.whenPressed = searchButton

        def on_cancel(self):
                self.parentApp.switchFormPrevious()

    

class licNum2Search(np.ActionForm):

        def create(self):
            self.serNo = self.add(np.TitleText, name = "Licence # :")
            self.nextrely += 1
            self.nextrelx -= 2
                
            def searchButton(*args):
                viol_licence_search = Search.Search_Viol_Licence(self.serNo.value)
                driver_licence_search = Search.Search_Driver_Licence(self.serNo.value)
                results = list()
                licence_res = list()
                try:
                    curs.execute(driver_licence_search)
                    drows = curs.fetchall()
                    
                    if len(drows) > 0:
                        
                        try:
                            curs.execute(viol_licence_search)
                            rows = curs.fetchall()
                            
                            if len(rows) > 0:
                                results.append("Column Names    ")

                                for row in rows:
                                    row = str(row)
                                    row = row.strip()
                                    results.append(row)
                            
                            else:
                                results = list()
                                results.append("No results found")

                            F = np.Form(name = "Query:")
                            F.add(np.TitlePager,name = "Results:", values = results)
                            F.edit()
                        
                        except cx_Oracle.DatabaseError as exc:
                            self.parentApp.switchForm("ERROR")

                    else: 
                        self.parentApp.switchForm("VIOLERROR")
                    
                except cx_Oracle.DatabaseError as exc:
                    self.parentApp.switchForm("ERROR")

            self.searchButton = self.add(np.ButtonPress, name = "Search")
            self.searchButton.whenPressed = searchButton
                
        def on_cancel(self):
                self.parentApp.switchFormPrevious()

class sinSearch(np.ActionForm):

        def create(self):
            self.serNo = self.add(np.TitleText, name = "SIN :")
            self.nextrely += 1
            self.nextrelx -= 2
                
            def searchButton(*args):
                viol_sin_search = Search.Search_Viol_SIN(self.serNo.value)
                results = list()
                try:
                    curs.execute(viol_sin_search)
                    rows = curs.fetchall()

                    if len(rows) > 0:

                        results.append("Column names    ")
                        for row in rows:
                            rows = str(rows)
                            rows = rows.strip()
                            results.append(rows)
                    else:
                        results = list()
                        results.append("No results found")

                    F = np.Form(name = "Query:")
                    F.add(np.TitlePager,name = "Results:", values = results)
                    F.edit()

                except cx_Oracle.DatabaseError as exc:
                    self.parentApp.switchForm("ERROR")

            self.searchButton = self.add(np.ButtonPress, name = "Search")
            self.searchButton.whenPressed = searchButton
                
        def on_cancel(self):
                self.parentApp.switchFormPrevious()


#####################################################################################################################
#                                                   ERROR HANDLING STUFF                                            #
#####################################################################################################################
class generror(np.ActionPopup):
    def create(self):
        self.name = "ERROR"
        self.add(np.TitleText, name = "Invalid Input, Please Check Inputs")

    def on_ok(self):
        self.parentApp.switchFormPrevious()

class violerror(np.ActionPopup):
    def create(self):
        self.name = "VIOLERROR"
        self.add(np.TitleText,name = "Invalid Licence Number, Person Does Not Exist")

    def on_ok(self):
        self.parentApp.switchFormPrevious()

class serror(np.ActionPopup):
    def create(self):
        self.name = "SERIALERROR"
        self.add(np.TitleText, name = "Serial Number Already In Database, Please Check Input")

    def on_ok(self):
        self.parentApp.switchFormPrevious()

class aterror(np.ActionPopup):
    def create(self):
        self.name = "TRANSERROR"
        self.add(np.TitleText, name = "Person or Vehicle Does Not Exist")

        def personButton(*args):
            self.parentApp.switchForm("ADDPERSON")
            
        self.personButton = self.add(np.ButtonPress, name = "Add Person")
        self.personButton.whenPressed = personButton

    def on_ok(self):
        self.parentApp.switchFormPrevious()

class perror(np.ActionPopup):
    def create(self):
        self.name = "PERSONERROR"
        self.add(np.TitleText, name = "Person Already Has Licence")

    def on_ok(self):
        self.parentApp.switchFormPrevious()

class derror(np.ActionPopup):
    def create(self):
        self.name = "DATEERROR"
        self.add(np.TitleText, name = "Invalid Date, Please Insert Valid Date")

    def on_ok(self):
        self.parentApp.switchFormPrevious()

class serror(np.ActionPopup):
    def create(self):
        self.name = "SELLERROR"
        self.add(np.TitleText, name = "Person Does Not Own Vehicle")

    def on_ok(self):
        self.parentApp.switchFormPrevious()
#####################################################################################################################
#                                              ADDING WINDOWS TO MAIN FUNCTION                                      #
#####################################################################################################################

class MyApplication(np.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', MainMenu, name='MAIN MENU')
        self.addForm('LOGIN',login,name='Oracle Login')
        self.addForm('OPEN', OpenScreen, name = 'OPEN SCREEN')
        self.addForm('VREG', veReg, name = 'Vehicle Registration')
        self.addForm('ATRANS', autoTrans, name = "Auto Transaction")
        self.addForm('DLREG', dlReg, name = "Driver's licence registration")
        self.addForm('VREC', vRecord, name = "violation record")
        self.addForm('SEARCH', search, name = "search")
        self.addForm('OWNER', owner, name = "owner")
        self.addForm('ADDPERSON', addperson, name = "Add Person")
        self.addForm('ADDCOND', addrestriction, name = "Add Condition")
        self.addForm("LDDATA", lDSearch, name = "Search For Licence or Driver Data")
        self.addForm("VIOLDATA", violationSearch, name = "Search For Violation Records")
        self.addForm("VHISTDATA", vehicleHistorySearch, name = "Search for Vehicle History")
        self.addForm("GNAMESEARCH", givenNameSearch, name = "Search by Given Name :")
        self.addForm("LNSEARCH", licNumSearch, name = "Search by Licence Number :")
        self.addForm("LN2SEARCH", licNum2Search, name = "Search by Licence Number :")
        self.addForm("SINSEARCH", sinSearch, name = "Search by Social Insurance Number :")
        self.addForm("ERROR", generror, name = "")
        self.addForm("VIOLERROR", violerror, name = "")
        self.addForm("SERIALERROR", serror, name = "")
        self.addForm("TRANSERROR", aterror, name = "")
        self.addForm("DATEERROR", derror, name = "")
        self.addForm("SELLERROR", serror, name = "")
        self.addForm("PERSONERROR", perror, name = "")

if __name__ == '__main__':
    TestApp = MyApplication()
    TestApp.run()
