from Handler.brandNew import BrandNew
from Handler.revision import Revision
from Handler import commit

# Command to start the mysql server
import os
status = os.system('systemctl status mysql')

if status != '0':
    # Start the server
    os.system('systemctl start mysql')


print("\nWelcome to Re-Iterator\n")
choice = int(input("Enter 1 for new 0 for revision : "))


if choice == 1:
    # Do stuff for new.
    bn = BrandNew()
    bn.addTopic()
    bn.updateDb()
else:
    # For revision
    rev = Revision()
    rev.reviseTopic()
    commit()

    # Command to stop the mysql server
    os.system('systemctl stop mysql')
