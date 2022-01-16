from tkinter import *
from tkinter import messagebox

import now as now
from tksheet import Sheet
import sqlite3
import datetime
import smtplib
from email.message import  EmailMessage




root = Tk()
root.title('WaitList')



rg = Tk()
rg.title('Register')
rg.withdraw()
# Database
conn = sqlite3.connect('wait_list.db') # if that doesn't exist , it will create
# Create Cursor
c = conn.cursor()
'''
# Create table  (only for once)

c.execute("""CREATE TABLE waitlists (
         f_name text,
         l_name text,
         phone_number text,
         how_many_people integer,
         email_address text,
         time timestamp 
    )    
""")
'''


'''
for record in records:
    print_records += str(record) + "\n"
'''

def email_alert(subject, body, to):
    msg = EmailMessage() #that's going to create email message
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to
    user = "emailAlertPython30@gmail.com"

    msg['from'] = user

    password = "wrhfsbyhhctuklky"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)

    server.quit()

    messagebox.showinfo("Great! ","You've succesfully sent an alert")



def al_submit():
    conn = sqlite3.connect("wait_list.db")
    c = conn.cursor()

    global record_id
    record_id = which_alert.get()

    c.execute("SELECT * FROM waitlists WHERE oid = " + record_id)
    record = c.fetchone()
    '''
    record[0] = first name
    record[1] = last name
    record[2] = phone number
    record[3] = how_many_people
    record[4] = email_address
    record[5] = time
    '''
    #for now I will only test email address since Videotron does not support email SMS gateway service
    subject = "You have a place for our restaurant"
    body = "Hello "+ str(record[0]) + " " + str(record[1]) + " You put your name on our waiting list and our table for " + str(record[3]) +" people is ready now you may come now\n Thank you "

    email_alert(subject, body, record[4])


def alert():
    global al
    al = Tk()
    al.title('Text Alert')

    global which_alert
    which_alert = Entry(al, width=30)
    which_alert.grid(row=0, column=1, padx=20)

    which_alert_label = Label(al, text="Which index do you want to send an alert message?")
    which_alert_label.grid(row=0, column=0)

    al_submit_btn = Button(al, text="Send Email Alert", command=al_submit)
    al_submit_btn.grid(row=1, column=1, columnspan=2, pady=10, padx=10, ipadx=100)


# function oid_update updates oid according to its order everytime a user updates or deletes its data
def oid_update():
    conn = sqlite3.connect("wait_list.db")
    c = conn.cursor()

    c.execute("SELECT *, oid FROM waitlists")
    records = c.fetchall()
    print_records = ''
    # Loop thru results
    counter = 1
    temp_num = 0
    for record in records:
        temp_num = record[6]
        c.execute("""UPDATE waitlists SET
            oid = :count
            WHERE oid = :temp_num""",
                  {'count' : counter,
                   'temp_num' : temp_num
                  })
        counter +=1

    conn.commit()
    conn.close()




def change_record():
    conn = sqlite3.connect("wait_list.db")
    c = conn.cursor()

    c.execute("""UPDATE waitlists SET 
            f_name = :first,
            l_name = :last,
            phone_number = :phone_number,
            how_many_people = :how_many_people,
            email_address = :email_address
            WHERE oid = :oid""",  # Python Dictionary {Key:value}
              {'first': f_name.get(),
               'last': l_name.get(),
               'phone_number': phone_number.get(),
               'how_many_people': num_people.get(),
               'email_address': email_add.get(),
               'oid': record_id
               })


    conn.commit()
    conn.close()
    query()
    up.destroy()



def up_submit():

    conn = sqlite3.connect("wait_list.db")
    c = conn.cursor()

    global record_id
    record_id = which_update.get()

    c.execute("SELECT * FROM waitlists WHERE oid = " + record_id)

    records = c.fetchall()



    global f_name, l_name, phone_number, num_people, email_add

    # Text boxes
    f_name = Entry(up, width=30)
    f_name.grid(row=2, column=1, padx=20)
    l_name = Entry(up, width=30)
    l_name.grid(row=3, column=1, padx=20)
    phone_number = Entry(up, width=30)
    phone_number.grid(row=4, column=1, padx=20)
    num_people = Entry(up, width=30)
    num_people.grid(row=5, column=1, padx=20)
    email_add = Entry(up, width=30)
    email_add.grid(row=6, column=1, padx=20)

    # Create Text box labels
    f_name_label = Label(up, text="First Name")
    f_name_label.grid(row=2, column=0)
    l_name_label = Label(up, text="Last Name")
    l_name_label.grid(row=3, column=0)
    phone_number_label = Label(up, text="Phone Number")
    phone_number_label.grid(row=4, column=0)
    num_people_label = Label(up, text="How many people")
    num_people_label.grid(row=5, column=0)
    email_label = Label(up, text="Email")
    email_label.grid(row=6, column=0)

    change_btn = Button(up, text="Change", command=change_record)
    change_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

    for record in records:
        f_name.insert(0, record[0])
        l_name.insert(0, record[1])
        phone_number.insert(0, record[2])
        num_people.insert(0, record[3])
        email_add.insert(0, record[4])

    conn.commit()
    conn.close()


def update():
    global up
    up = Tk()
    up.title('Update a record')

    global which_update
    which_update = Entry(up, width=30)
    which_update.grid(row=0, column=1, padx=20)

    which_update_label = Label(up, text="Which index do you want to update?")
    which_update_label.grid(row=0, column=0)

    up_submit_btn = Button(up, text="Submit", command=up_submit)
    up_submit_btn.grid(row=1, column=0, columnspan=2, pady=10, padx=10, ipadx=100)



def dl_submit():
    conn = sqlite3.connect("wait_list.db")
    c = conn.cursor()

    # Delete a record
    c.execute("DELETE from waitlists WHERE oid= " + which_delete.get())



    conn.commit()
    conn.close()
    dl.destroy()
    oid_update()
    query()



def delete():
    global dl
    dl= Tk()
    dl.title('Delete a record')



    global which_delete
    which_delete = Entry(dl, width=30)
    which_delete.grid(row=0, column=1, padx=20)

    which_delete_label = Label(dl, text="Which index do you want to delete?")
    which_delete_label.grid(row=0, column=0)

    dl_submit_btn = Button(dl, text="Submit", command=dl_submit)
    dl_submit_btn.grid(row=1, column=0, columnspan=2, pady=10, padx=10, ipadx=100)





def query():
    c.execute("SELECT *, oid FROM waitlists")
    records = c.fetchall()
    print_records = ''

    sheet = Sheet(root,
                  data = [[f"{record[c]}" for c in range(6)] for record in records],
                 height=500,
                 width=1500)
    sheet.grid(row=4, column=0, columnspan=20)
    sheet.set_all_column_widths(width = 200, only_set_if_too_small = False, redraw = True, recreate_selection_boxes = True)
    sheet.headers(["First Name", "Last Name", "Phone Number", "How many people", "Email", "Time"])

query() #call query




def submit():
    conn = sqlite3.connect("wait_list.db")
    c = conn.cursor()
    now = datetime.datetime.now()
    c.execute("INSERT INTO waitlists VALUES (:f_name, :l_name, :phone_number, :num_people, :email_address, :time)",
              {
                  'f_name': f_name.get(),
                  'l_name': l_name.get(),
                  'phone_number': phone_number.get(),
                  'num_people': num_people.get(),
                  'email_address': email_add.get(),
                  'time': now.strftime("%Y-%m-%d %H:%M:%S")
              }
              )

    # clear the text boxes
    f_name.delete(0, END)
    l_name.delete(0, END)
    phone_number.delete(0, END)
    num_people.delete(0, END)
    email_add.delete(0, END)

    conn.commit()
    conn.close()

    query()
    # don't destroy rg because when you re-register destroyed rg can't deiconify again
    rg.withdraw()




def register():
    conn = sqlite3.connect("wait_list.db")
    c = conn.cursor()

    rg.deiconify()

    conn.commit()
    conn.close()





register_btn = Button(root, text="Register", command=register)
register_btn.grid(row=0, column=0)
delete_btn = Button(root, text="Delete", command = delete)
delete_btn.grid(row=0, column=1)
update_btn = Button(root, text="Update", command = update)
update_btn.grid(row=0, column=2)
alert_btn = Button(root, text="Text Alert", command = alert)
alert_btn.grid(row=0, column=3)

# Text boxes
f_name = Entry(rg, width=30)
f_name.grid(row=0, column=1, padx=20)
l_name = Entry(rg, width=30)
l_name.grid(row=1, column=1, padx=20)
phone_number = Entry(rg, width=30)
phone_number.grid(row=2, column=1, padx=20)
num_people = Entry(rg, width=30)
num_people.grid(row=3, column=1, padx=20)
email_add = Entry(rg, width=30)
email_add.grid(row=4, column=1, padx=20)


# Create Text box labels
f_name_label = Label(rg, text="First Name")
f_name_label.grid(row=0, column=0)
l_name_label = Label(rg, text="Last Name")
l_name_label.grid(row=1, column=0)
phone_number_label = Label(rg, text="Phone Number")
phone_number_label.grid(row=2, column=0)
num_people_label = Label(rg, text="How many people")
num_people_label.grid(row=3, column=0)
email_label = Label(rg, text="Email")
email_label.grid(row=4, column=0)

# Create Submit button
submit_btn = Button(rg, text="Submit", command=submit)
submit_btn.grid(row=5, column=0, columnspan=2, pady=10, padx=10, ipadx=100)


root.mainloop()



conn.commit()
conn.close()