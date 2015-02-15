import math, sqlite3, os, datetime
 
def main():
	print "Running main function."
	if os.path.isfile('cvss.db'):
		print "A database file was found."
		try:
			conn = sqlite3.connect('cvss.db')
			db = conn.cursor()
		except sqlite3.Error, e: 
			print "Error %s:" % e.args[0]
		calculator()
	else:
		print "No database found. Creating one."
		try:
			conn = sqlite3.connect('cvss.db')
			db = conn.cursor()
		except: 
			print "Database creation failed."
		try:
			db.execute('''CREATE TABLE cvss
				(date, name, Av, Ac, Au, Con, Int, Avl, base, temporal, env, notes)''')
		except:
			print "Table creation failed."
		calculator()


def storedb(date, 
	    name, 
	    Av, Ac, Au,
	    Con, Int, Avl,
	    baseScore, 
            temporal, 
            env, 
            notes):
	store = raw_input("Do you want to store the result? Y/N: ")
	if store != 'Y':
		print "Canceling store."
	else:
		try:
			conn = sqlite3.connect('cvss.db')
			db = conn.cursor()
			db.execute('''INSERT INTO cvss(date, name, Av, Ac, Au, Con, Int, Avl, base, temporal, env, notes)
                                      VALUES(?,?,?,?,?,?,?,?,?,?,?,?)''', (date, name, Av, Ac, Au, Con, Int, Avl, baseScore, temporal, env, notes))
		except:
			print "Storing data failed."
		conn.commit()
		db.close()


def subScore(value):
        if value == 0:
                return 0
        else:
                return 1.176
 
def calculator():
        vulnName = raw_input("Enter vulnerability name: \n")
        print "==Access complexity=="
        print "(H)igh, (M)edium, (L)ow"
        ex_Ac = raw_input("Enter Complexity: \n")
        if ex_Ac == "H":
                Ac = 0.35
        elif ex_Ac == "M":
                Ac = 0.61
        elif ex_Ac == "L":
                Ac = 0.71
        else:
                print "You must select a valid Access Complexity."
        print "==Authentication=="
        print "(N)o authentication, (S)ingle instance, (M)ultiple instance"
        ex_Au = raw_input("Enter Authentication type: \n")
        if ex_Au == "N":
                Au = 0.704
        elif ex_Au == "S":
                Au = 0.56
        elif ex_Au == "M":
                Au = 0.45
        else:
                print "You must select a valid Authentication Type."   
        print "==Access Vector=="
        print "(L)ocal, (A)djacent network, (N)etwork"
        ex_Av = raw_input("Enter Access vector: \n")
        if ex_Av == "L":
                Av = 0.395
        elif ex_Av == "A":
                Av = 0.646
        elif ex_Av == "N":
                Av = 1
        else:
                print "You must select a valid Attack Vector."
        print "==Confidentiality Impact=="
        print "(N)o Impact, (P)artial Impact, (C)omplete compromise"
        im_Con = raw_input("Enter Confidentiality impact: \n")
        if im_Con == "N":
                Con = 0
        elif im_Con == "P":
                Con = 0.275
        elif im_Con == "C":
                Con = 0.660
        else:
                print "You must select a valid Confidentiality Impact."
        print "==Integrity Impact=="
        print "(N)o Impact, (P)artial Impact, (C)omplete loss"
        im_Int = raw_input("Enter Integrity impact: \n")
        if im_Int == "N":
                Int = 0
        elif im_Int == "P":
                Int = 0.275
        elif im_Int == "C":
                Int = 0.660
        else:
                print "You must select a valid Integrity Impact."
        print "==Availability Impact=="
        print "(N)o Impact, (P)artial Impact, (C)omplete loss"
        im_Avl = raw_input("Enter Availability impact: \n")
        if im_Avl == "N":
                Avl = 0
        elif im_Avl == "P":
                Avl = 0.275
        elif im_Avl == "C":
                Avl = 0.660
        else:
                print "You must select a valid Availability Impact."
        Exploitability = 20 * Ac * Au * Av
        Impact = 10.41 * (1 - (1 - Con) * (1 - Int) * (1 - Avl))
        BaseScore = (0.6 * Impact + 0.4 * Exploitability - 1.5) * subScore(Impact)
        BaseScore = round(BaseScore, 1)
        print "+Exploitability Metrics+"
        print "Vulnerability: " +vulnName
        Av = str(Av)
        print "Access Vector: " +Av
        Ac = str(Ac)
        print "Access Complexity: " +Ac
        Au = str(Au)
        print "Authentication: " +Au
        print "+Impact Metrics+"
        Con = str(Con)
        print "Confidentiality Impact: " +Con
        Int = str(Int)
        print "Integrity Impact: " +Int
        Avl = str(Avl)
        print "Availability Impact: " +Avl
        BaseScore = str(BaseScore)
        print "\n Base score: " +BaseScore
	date = datetime.datetime.now()
#I still need to accept input/calculate these values, so for now it's garbage. 
	temporal = 'test'
	env = 'test'
	notes = 'test'
	storedb(date, vulnName, Av, Ac, Au, Con, Int, Avl, BaseScore, temporal, env, notes)
	
main()
