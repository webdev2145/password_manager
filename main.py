from tkinter import *
from tkinter import messagebox
import string
import random
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_pass():
    letters = [l for l in string.ascii_letters]
    digits = [d for d in string.digits]
    special_chars = [sc for sc in string.punctuation]

    g_password = []

    pass_chars = random.randint(8, 10)
    pass_digits = random.randint(2, 4)
    pass_special = random.randint(2, 4)

    for x in range(pass_chars):
        g_password.append(random.choice(letters))

    for char in range(pass_digits):
        g_password.append(random.choice(digits))

    for sc in range(pass_special):
        g_password.append(random.choice(special_chars))

    random.shuffle(g_password)
    gen_text = ''.join(g_password)
    txt_password.delete(0, END)
    txt_password.insert(0, gen_text)
    #copy the password to the clipboard to be pasted into a site
    pyperclip.copy(gen_text)
# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_password():
    website = txt_website.get()
    username = txt_email.get()
    password = txt_password.get()

    data = {
        website: {
            "email": username,
            "password": password
        }
    }
    if not website or not password:
        messagebox.showerror(title='Oops!', message='Do not leave any field empty')
    else:

        is_ok = messagebox.askyesno(title='Verification', message=f'Username: {username}\nWebsite: {website}\nPassword: {password}')

        if is_ok:
            # with open('data.txt', 'a') as file:
            #     output = f'{website} | {username} | {password}\n'
            #     file.write(output)
            # txt_password.delete(0, END)
            # txt_website.delete(0, END)
            try:
                with open('data.json', 'r') as file:
                    read_data = json.load(file)
                    #update the contents with new data:
                    read_data.update(data)
            except FileNotFoundError:
                messagebox.showinfo(title='File does not exist', message='The file was created successfully')
                with open('data.json', 'w') as file:
                    json.dump(data, file, indent=4)

            else:
                #write to the json file
                with open('data.json', "w") as d_file:
                    json.dump(read_data, d_file, indent=4)
            finally:
                txt_password.delete(0, END)
                txt_website.delete(0, END)

def pass_search():
    website_name = txt_website.get()
    website_name = website_name.title()

    if not website_name:
        messagebox.showerror(title="Oops", message='You need to enter a site name')
    else:
        try:
            with open('data.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            messagebox.showinfo(title="Oops", message="The file does not exist. you need to add sites first")
        else:
            if website_name in data:
                messagebox.showinfo(title=website_name, message=f'Email: {data[website_name]["email"]}\nPassword: {data[website_name]["password"]}')

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title('Password Manager')
window.config(padx=20, pady=20)
canvas = Canvas(width=200, height=200, highlightthickness=0)
pass_image = PhotoImage(file="logo.png")


canvas.create_image(100, 100, image=pass_image)
canvas.grid(row=1, column=1)

lbl_website = Label(text="Website:", font=('Arial', 12))
lbl_website.grid(row=2, column=0)

txt_website = Entry(width=21)
txt_website.grid(row=2, column=1)

btn_search = Button(text='Search', command=pass_search, width=14)
btn_search.grid(row=2, column=2)

lbl_email = Label(text="Email/Username:", font=('Arial', 12))
lbl_email.grid(row=3, column=0)

txt_email = Entry(width=38)
txt_email.insert(0, "onepinn980@gmail.com")
txt_email.grid(row=3, column=1, columnspan=2)

lbl_password = Label(text="Password:", font=('Arial', 12))
lbl_password.grid(row=4, column=0)

txt_password = Entry(width=21)
txt_password.grid(row=4, column=1)

btn_generate = Button(text="Generate Password", width=14, command=generate_pass)
btn_generate.grid(row=4, column=2)

btn_add = Button(text="Add", width=36, command=add_password)
btn_add.grid(row=5, column=1, columnspan=2)

window.mainloop()