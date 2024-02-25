from time import strftime
from tkinter import *
from tkinter import font
from tkinter import messagebox
from tkinter import ttk
from tkinter import simpledialog
from tkcalendar import *
from calendar import *
import tkinter as tk
import re
from reportlab.platypus import TableStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table,Spacer
# import customtkinter
from ttkwidgets.autocomplete import AutocompleteEntry
from datetime import date, datetime
import mysql.connector

mydb1=mysql.connector.connect(host="localhost",user="root",password="",database="Accounting_Soft")
mycursor=mydb1.cursor()

# bg1=fram colors
# bg2=backcolors
# bg3=active background color
# fg1=font color
# bt1,cursor=cur1=button color
# fg2=button text color
# lbg1=label background
# abg=active background for button
# afg=active foreground for button
# bt2=backgroung of other buttons which need different color
global bg1,bg2,bg3,fg1,bt1,fg2,lbg1,bt2,ico_photo
bg1="#FFFFD9"
bg2= "#BFBFBF"
bg3="red"
fg1="black"
fg2="white"
bt1="red"
bt2="#081947"
abg="black"
afg="white"
lbg1="#BFBFBF"
cur1="hand2"
# ico_photo="E:\Tirth\Project\Accounting System\icon_photo,ico"

# First Form
def win_main():
    try:
        win3.destroy()
    except:
        pass
    global main1
    main1=Tk()

    # mycursor.execute("SELECT * FROM purchase where company_name=%s AND p_type=%s",('Tirthlimited','Bank'))
    # sql1=mycursor.fetchall()
    # print(sql1)
    # data=("Tirthlimited",500000,100000,5000,10000,20000,30000)
    # mycursor.execute("INSERT INTO calculation (company_name,tot_cash,tot_bank,gst_give_cash,gst_take_cash,gst_give_bank,gst_take_bank) VALUES(%s,%s,%s,%s,%s,%s,%s)",data)
    # mydb1.commit()
    # data=(2023/2/2,None)
    # mycursor.execute("update contra set c_date=%s where c_date=%s",data)
    # mydb1.commit()

    main1.state("zoomed")
    main1.title("Accounting System")
    # main1.iconbitmap(ico_photo)
    main1.config(bg=bg1)
    fram2=Frame(main1, bg=bg2,borderwidth=5,relief=SUNKEN,width=15,height=200)
    fram2.pack(side=TOP,fill=X,padx=20,pady=5)
    fram3=Frame(main1, bg=bg2,borderwidth=5,relief=SUNKEN,width=15,height=200)
    fram3.pack(side=BOTTOM,fill=X,padx=20,pady=5)
    fram1=Frame(main1, bg=bg2,borderwidth=5,relief=SUNKEN,width=15,height=200)
    fram1.pack(side=RIGHT,fill=Y,padx=25)
    flab1=Label(fram2,fg=fg1,text="Accounting Managment System",bg=bg2,font=("bold",25),borderwidth=20)
    flab1.pack(padx=20,pady=5)
    flab2=Label(fram3,fg=fg1,text="Hello! This is bookmate Which hepls you for Accounting.",bg=bg2,font=("bold",20),borderwidth=20)
    flab2.pack(padx=20,pady=5)

    def help():
        messagebox.showinfo("Help","""In This Page You Can Select Your Company From Existing Companies.If You Don't Have Company Yet Then Create Your Company From Company Creation.""")
    bat2=Button(fram1,fg=fg2,text="Help",bg=bt1,cursor="question_arrow",activeforeground=afg,activebackground=abg,width=14,command=help)
    bat2.pack(side=BOTTOM)
    
    # Style
    style=ttk.Style()
    style.theme_use('classic')
    style.configure("Vertical.Tscrollbar:",background="#B3BED1",bordercolor="red")
    
    lab11=Label(main1, fg=fg1,text="Existing Companys:",bg=bg1,font=("bold",15))
    lab11.place(relx=0.5, rely=0.23, anchor="center")
    mycursor.execute("SELECT company_name from c_creation")
    option_name=mycursor.fetchall()
    
    frm_list = Frame(main1, bg=bg2, borderwidth=5, relief=SUNKEN)
    frm_list.place(relx=0.5, rely=0.53, anchor="center")
    scroll1=ttk.Scrollbar(frm_list,orient=VERTICAL)
    scroll1.pack(side=RIGHT,fill=Y)

    def on_key_press(event):
        global selected_item, index
        selection = lis1.curselection()
        if not selection:
            return
        index = selection[0]
        if event.keysym == 'Up':
            if index > 0:
                lis1.selection_clear(0, tk.END)
                lis1.activate(index - 1)
                lis1.selection_set(index - 1, last=None)
        elif event.keysym == 'Down':
            if index < lis1.size() - 1:
                lis1.selection_clear(0, tk.END)
                lis1.activate(index + 1)
                lis1.selection_set(index + 1, last=None)
        update_label()

    def on_item_click(event):
        update_label()

    def update_label():
        global selected_item, index
        selection = lis1.curselection()
        if not selection:
            return
        index = selection[0]
        selected_item = lis1.get(index)

    lis1 = Listbox(frm_list, selectmode=tk.SINGLE, width=35, height=20, bg=bg2, fg=fg1, font=3, yscrollcommand=scroll1.set, activestyle="none")
    lis1.pack()
    for item in option_name:
        lis1.insert(END, item[0])
    

    lis1.bind("<Up>", on_key_press)
    lis1.bind("<Down>", on_key_press)
    lis1.bind("<ButtonRelease-1>", on_item_click)
    
    def open_com():
        if lis1.get(index):
            global c_name,c_name_string
            c_name=(lis1.get(index),)
            c_name_string=lis1.get(index)
            open_password=simpledialog.askstring("Password","Enter Password for Open Company:",show="*")
            mycursor.execute("SELECT password from c_creation WHERE company_name=%s",c_name)
            sql=mycursor.fetchall()
            dat1=str(sql)
            try:
                dat2="[('" + open_password + "',)]"
                if(dat1==dat2):
                    getdata()
                    main2()
                elif(dat1!=dat2):
                    messagebox.showerror("Error","Password is Incorrect.")
            except:
                pass
        else:
            messagebox.showinfo("Select","Please Select Company For Open.")
    
    def remove_com():
        if lis1.get(index):
            c_name1=lis1.get(index)
            # c_name=str(c_name1)
            c_name=(lis1.get(index),)
            qus=messagebox.askyesno("Alert","Are you Sure to delete that Company?")
            if(qus==YES):
                delete_password=simpledialog.askstring("Password","Enter Password of this Company To Remove:",show="*")
                delete_company=lis1.get(index)
                dt1=delete_company
                mycursor=mydb1.cursor()
                mycursor.execute("SELECT password from c_creation WHERE company_name=%s",c_name)
                sql1=mycursor.fetchall()
                dt2=str(sql1)
                try:
                    dt3="[('" + delete_password + "',)]"
                    if(dt2==dt3):
                        mycursor.execute("DELETE FROM c_creation WHERE company_name=%s",c_name)
                        lis1.delete(index)
                        mydb1.commit()
                    else:
                        messagebox.showerror("Error","Password is Incorrect.")
                except:
                    pass
        else:
            messagebox.showinfo("Select","Please Select Company For Remove.")

    def qut():
        qus=messagebox.askyesno("Alert","Are you want to Exit?")
        if(qus==YES):
            main1.destroy()
    main1.bind("<Return>",lambda event:open_com())
    main1.bind("<Control-c>",lambda event:win1())
    main1.bind("<Control-C>",lambda event:win1())
    main1.bind("<Control-h>",lambda event:help())
    main1.bind("<Control-H>",lambda event:help())
    main1.bind("<Control-r>",lambda event:remove_com())
    main1.bind("<Control-R>",lambda event:remove_com())
    main1.bind("<Escape>",lambda event:qut())
    try: 
        bt_open = Button(main1, fg=fg2, text="Open This Company", bg=bt1, cursor=cur1, activeforeground=afg, activebackground=abg, command=open_com)
        bt_open.place(relx=0.45, rely=0.83, anchor="center")
    except:
        pass
    bt_delete = Button(main1, fg=fg2, text="Remove This Company", bg=bt1, cursor=cur1, activeforeground=afg, activebackground=abg, command=remove_com)
    bt_delete.place(relx=0.55, rely=0.83, anchor="center")
    bat1=Button(fram1,fg=fg2,text="Company Creation",bg=bt1,cursor=cur1,activeforeground=afg,activebackground=abg,command=lambda:{(win1())})
    bat1.pack()
    main1.mainloop()

# Company_creation form
def win1():
    win=Tk()
    # ic_photo=PhotoImage(file= 'Z:\Project\Accounting System\icon_photo.png')
    win.minsize(height=650,width=1300)
    win.maxsize(height=650,width=1300)
    win.title("Company Creation")
    # win.iconbitmap(ico_photo)
    fram=LabelFrame(win,fg=fg1,text='Company Creation',bg=bg2,font=10,height=25,width=1500)
    fram.pack()
    win.configure(bg=bg1)
    global state_list
    state_list=[
            "Andhra Pradesh","Arunachal Pradesh ","Assam","Bihar","Chhattisgarh","Goa","Gujarat","Haryana","Himachal Pradesh","Jammu and Kashmir",
            "Jharkhand","Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan",
            "Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal","Andaman and Nicobar Islands","Chandigarh",
            "Dadra and Nagar Haveli","Daman and Diu","Lakshadweep","Delhi","Puducherry"
            ]

    global Txt1,Txt3,Txt4,Txt5,Txt6,Txt7,Txt8,Txt9,Txt10,Txt11
    Txt1=StringVar()
    Txt3=StringVar()
    Txt4=StringVar()
    Txt5=StringVar()
    Txt6=StringVar()
    Txt7=StringVar()
    Txt8=StringVar()
    Txt9=StringVar()
    Txt10=StringVar()
    Txt11=StringVar()

    lab1=Label(win, fg=fg1,text="Company Name:",bg=bg1,font=15).place(x=20,y=40)
    txt1=Entry(win,bg=bg2,borderwidth=3,font=5,width=40,textvariable=Txt1)
    txt1.place(x=150,y=40)

    lab2=Label(win, fg=fg1,text="Address:",bg=bg1,font=15).place(x=20,y=75)
    txt2=Text(win,bg=bg2,borderwidth=3,font=5,width=40,height=6)
    txt2.place(x=150,y=75)

    lab3=Label(win, fg=fg1,text="Country:",bg=bg1,font=15).place(x=20,y=210)
    txt3=Entry(win,bg=bg2,borderwidth=3,font=5,width=15)
    txt3.insert(0,"India")
    txt3.config(state=DISABLED)
    txt3.place(x=150,y=210)

    lab4=Label(win, fg=fg1,text="State:",bg=bg1,font=15).place(x=20,y=245)
    # txt4=Entry(win,bg=bg2,borderwidth=3,font=5,width=15,textvariable=Txt4,completevalues=state_list)
    txt4=AutocompleteEntry(win,completevalues=state_list)
    txt4.place(x=150,y=245)

    lab5=Label(win, fg=fg1,text="Pincode:",bg=bg1,font=15).place(x=20,y=280)
    txt5=Entry(win,bg=bg2,borderwidth=3,font=5,width=15,textvariable=Txt5)
    txt5.place(x=150,y=280)

    lab6=Label(win, fg=fg1,text="Telephone:",bg=bg1,font=15).place(x=20,y=315)
    txt6=Entry(win,bg=bg2,borderwidth=3,font=5,width=15,textvariable=Txt6)
    txt6.place(x=150,y=315)

    lab7=Label(win, fg=fg1,text="Mobile:",bg=bg1,font=15).place(x=20,y=350)
    txt7=Entry(win,bg=bg2,borderwidth=3,font=5,width=15,textvariable=Txt7)
    txt7.place(x=150,y=350)

    lab8=Label(win, fg=fg1,text="E-mail:",bg=bg1,font=15).place(x=20,y=385)
    txt8=Entry(win,bg=bg2,borderwidth=3,font=5,width=30,textvariable=Txt8)
    txt8.place(x=150,y=385)

    lab9=Label(win, fg=fg1,text="Website:",bg=bg1,font=15).place(x=20,y=420)
    txt9=Entry(win,bg=bg2,borderwidth=3,font=5,width=30,textvariable=Txt9)
    txt9.place(x=150,y=420)

    lab10=Label(win, fg=fg1,text="Financial year:",bg=bg1,font=("bold",15)).place(x=700,y=40)
    dt10=DateEntry(win,selectmode='day',font=5,width=10,background='darkblue',year=2022,month=4,day=1)
    dt10.place(x=910,y=40)

    lab11=Label(win, fg=fg1,text="Books Beginning From:",bg=bg1,font=("bold",15)).place(x=700,y=75)
    dt11=DateEntry(win,selectmode='day',font=5,width=10,background='darkblue',year=2022,month=4,day=1)
    dt11.place(x=910,y=75)

    def submit_info() :

        global company_name,state,mail_address,country,pincode,telephone,mobile,email,website,financial_year,books

        def valid_country():
            global country_list,cou
            country_list=[x.upper() for x in state_list]

            cou=state.upper()

        dt1=dt10.get_date()
        dt2=dt11.get_date()
        company_name=txt1.get()
        mail_address=txt2.get(1.0,END)
        country=txt3.get()
        state=txt4.get()
        pincode=txt5.get()
        telephone=txt6.get()
        mobile=txt7.get()
        email=txt8.get()
        website=txt9.get()
        financial_year=dt1.strftime("%Y/%m/%d")
        books=dt2.strftime("%Y/%m/%d")

        valid_country()
        company_name_validate=r"^[.@&]?[a-zA-Z0-9 ]+[ !.@&()]?[ a-zA-Z0-9!()]+"
        mobile_validate=r"[6-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]"
        email_valid=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        pincode_valid=r"^[1-9][0-9]{5}$"

        if company_name=="" or mail_address=="""
""" or state=="" or country=="" or pincode=="" or mobile=="" or email=="":
            messagebox.showinfo("Alert","Please Enter Information.")
        else:
            if re.match(company_name_validate,company_name):
                v2=True
            else:
                messagebox.showinfo("Alert","Please Enter Valid Company Name")
            if cou in country_list:
                v1=True
            else:
                messagebox.showinfo("Alert","Please Enter Valid State Name.")
            if re.match(mobile_validate,mobile):
                v3=True
            else:
                messagebox.showinfo("Alert","Please Enter Valid Mobile Number")
            if re.match(email_valid,email):
                v4=True
            else:
                messagebox.showinfo("Alert","Please Enter Valid E-mail")
            if re.match(pincode_valid,pincode):
                v5=True
            else:
                messagebox.showinfo("Alert","Please Enter Valid Pincode")
            try:
                if(v1==True and v2==True and v3==True and v4==True and v5==True):
                    gst()
            except:
                pass

            

# Gst form 
    def gst():
        Txt1i=StringVar()
        Txt3i=StringVar()
        Txt4i=StringVar()
        win1i=Tk()
        win1i.minsize(width=550,height=400)
        win1i.maxsize(width=550,height=400)
        win1i.config(bg=bg1)
        win1i.title("Enter GST Details")
        # win1i.iconbitmap(ico_photo)
        lab1i=Label(win1i,fg=fg1,text="State:",bg=bg1,font=15)
        lab1i.place(x=100,y=40)
        txt1i=Entry(win1i,bg=bg2,font=15,borderwidth=3,width=20)
        txt1i.place(x=270,y=40) 
        txt1i.insert(0,txt4.get())
        lab2i=Label(win1i, fg=fg1,text="Registration Type:",bg=bg1,font=15)
        lab2i.place(x=100,y=75)
        menu= StringVar(win1i)
        menu.set("Regular")
        list1=OptionMenu(win1i, menu,"Regular","Compositions")
        list1.place(x=270,y=75)
        list1.config(bg=bg2)
        lab3i=Label(win1i,fg=fg1,text="GST Applicable From:",bg=bg1,font=15)
        lab3i.place(x=100,y=110)
        txt3i=DateEntry(win1i,selectmode='day',font=5,width=10,background='darkblue',year=2022,month=4,day=1)
        txt3i.place(x=270,y=110)
        lab4i=Label(win1i,fg=fg1,text="GSTIN/UIN:",bg=bg1,font=15)
        lab4i.place(x=100,y=145)
        txt4i=Entry(win1i,bg=bg2,font=15,borderwidth=3,width=20,textvariable=Txt4i)
        txt4i.place(x=270,y=145)
        lab5i=Label(win1i,fg=fg1,text="Periodicity of GSTR1:",bg=bg1,font=15)
        lab5i.place(x=100,y=180)
        menu1=StringVar(win1i)
        menu1.set("Monthly")
        list1=OptionMenu(win1i, menu1,"Monthly","Quarterly")
        list1.place(x=270,y=180)
        list1.config(bg=bg2)

        def submit_gst():
            global state_gst,type_gst,from_gst,gstin_gst,period_gst
            dt3=txt3i.get_date()
            state_gst=txt1i.get()
            type_gst=menu.get()
            from_gst=dt3.strftime("%Y/%m/%d")
            gstin_gst=txt4i.get()
            period_gst=menu1.get()

            gst_valid=r"\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}"


            if state_gst=="" or gstin_gst=="":
                messagebox.showinfo("Alert","Please Enter Information.")
            else:
                if re.match(gst_valid,gstin_gst):
                    v1=True
                else:
                    messagebox.showinfo("Alert","Please Enter Valid Gst Number.")
                if state_gst in state_list:
                    v2=True
                else:
                    messagebox.showinfo("Alert","Please Enter Valid State Name.")
                try:
                    if v1==True and v2==True:
                        extra()
                except:
                    pass

        def extra():
            global password,password2,cash_db,branch_name,bank_db
            password=StringVar()
            password2=StringVar()
            cash_db=StringVar()
            branch_name=StringVar()
            bank_db=StringVar()
            ext=Tk()
            ext.title("Important Info")
            # ext.iconbitmap(ico_photo)
            ext.config(bg=bg1)
            ext.minsize(width=350,height=270)
            ext.maxsize(width=350,height=270)
            lb1=Label(ext,fg=fg1,text="Enter Password:",bg=bg1,font=15).place(x=15,y=30)
            lb2=Label(ext,fg=fg1,text="Conform Password:",bg=bg1,font=15).place(x=15,y=65)
            lb3=Label(ext,fg=fg1,text="Starting Cash Amount:",bg=bg1,font=15).place(x=15,y=100)
            lb4=Label(ext,fg=fg1,text="Bank Branch Name:",bg=bg1,font=15).place(x=15,y=135)
            lb5=Label(ext,fg=fg1,text="Starting Bank Amount:",bg=bg1,font=15).place(x=15,y=170)
            tx1=Entry(ext,font=15,width=16,bg=bg2,textvariable=password)
            tx1.place(x=180,y=30)
            tx2=Entry(ext,font=15,width=16,bg=bg2,show="*",textvariable=password2)
            tx2.place(x=180,y=65)
            tx5=Entry(ext,font=15,width=10,bg=bg2,textvariable=cash_db)
            tx5.place(x=180,y=100)
            tx3=Entry(ext,font=15,width=10,bg=bg2,textvariable=branch_name)
            tx3.place(x=180,y=135)
            tx4=Entry(ext,font=15,width=10,bg=bg2,textvariable=bank_db)
            tx4.place(x=180,y=170)
            
            def submit_extra():
                global password,cash_db,branch_name,bank_db
                password=StringVar()
                cash_db=StringVar()
                branch_name=StringVar()
                bank_db=StringVar()
                password=tx1.get()
                password2=tx2.get()
                branch_name=tx3.get()
                if password2=="" or cash_db=="" or branch_name=="" or bank_db=="":
                    messagebox.showinfo("Alert","Please Enter Information.")
                
                else:
                    v1=False 
                    v2=False
                    if(password != password2):
                        messagebox.showerror("Alert","Please Enter Same Password.") 
                    else:
                        v1=True
                    try:
                        cash_int=int(tx5.get())
                        bank_int=int(tx4.get())
                        cash_db=cash_int
                        bank_db=bank_int
                        v2=True
                    except:
                        messagebox.showerror("Alert","Please Enter Amount in Number.") 
                    if v1==True and v2==True:                                   
                        data=(company_name,mail_address,country,state,pincode,telephone,mobile,email,website,financial_year,books,type_gst,from_gst,gstin_gst,period_gst,password,cash_db,branch_name,bank_db)
                        data1=(company_name,cash_db,bank_db)
                        mycursor.execute("INSERT INTO c_creation(company_name,address,country,state,pincode,telephone,mobile,e_mail,website,f_year,book_from,type_db,from_db,gstin_db,period_db,password,cash_db,branch_name,bank_db) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",data)
                        mycursor.execute("INSERT INTO calculation(company_name,tot_cash,tot_bank) VALUES(%s,%s,%s)",data1)
                        mydb1.commit()
                        win1i.destroy()
                        win.destroy()
                        ext.destroy()
                        try:
                            main1.destroy()
                        except:
                            pass
                        win_main()
 
            bu1=Button(ext,fg=fg2,text="Submit Details",bg=bt1,cursor=cur1,activeforeground=afg,activebackground=abg,command=lambda:{submit_extra()}) 
            bu1.place(x=140,y=200)
            ext.mainloop()


        but1i=Button(win1i,fg=fg2,text="Submit gst info",bg=bt1,cursor=cur1,activeforeground=afg,activebackground=abg,command=lambda:{submit_gst()})
        but1i.place(x=200,y=215)
        
        win1i.mainloop()

    # def click(event):
    #     win.config=("<keys>",event.keysym)
        
    but1=Button(win, fg=fg2,text="Submit Information",bg=bt1,cursor=cur1,activeforeground=afg,activebackground=abg,command=lambda:{submit_info()})
    but1.place(x=500,y=500)

    win.mainloop()

# Destroys all frams
def fra_des():
        try:
            fra3.destroy()
        except:
            pass
        try:
            fra5.destroy()
        except:
            pass
        try:
            fra6.destroy()
        except:
            pass
        try:
            fra4.destroy()
        except:
            pass
        try:
            but9.destroy()
        except:
            pass
        try:
            but10.destroy()
        except:
            pass
        try:
            but11.destroy()
        except:
            pass
        try:
            rpdate1.destroy()
            rplab1.destroy()
            rpdate2.destroy()
            rplab2.destroy()
        except:
            pass
        try:
            rpdatec1.destroy()
            rplabc1.destroy()
            rpdatec2.destroy()
            rplabc2.destroy()
        except:
            pass

# Contra Vouchers
def contra():
    tot()
    fra_des()
    global vc1
    vc1=Tk()
    vc1.minsize(width=410,height=360)
    vc1.maxsize(width=410,height=360)
    vc1.config(bg=bg1)
    vc1.title("Contra Voucher")
    # vc1.iconbitmap(ico_photo)

    mycursor.execute("SELECT * FROM calculation WHERE company_name=%s",c_name)
    sql4=mycursor.fetchall()
    for row in sql4:
        global tot_cash_db,tot_bank_db
        tot_cash_db=row[1]
        tot_bank_db=row[2]
    
    lab1=Label(vc1, fg=fg1,text="Bank Branch Name:",bg=bg1,font=15)
    lab1.place(x=40,y=30)
    lab2=Label(vc1, fg=fg1,text="Current Bank Balance:",bg=bg1,font=15)
    lab2.place(x=40,y=70)
    lab6=Label(vc1, fg=fg1,text="Current Cash Balance:",bg=bg1,font=15)
    lab6.place(x=40,y=110)
    lab8=Label(vc1, fg=fg1,text="Date:",bg=bg1,font=15)
    lab8.place(x=40,y=190)
    lab3=Label(vc1, fg=fg1,text=branch_name_db,bg=bg1,font=15)
    lab3.place(x=220,y=30)
    lab4=Label(vc1, fg=fg1,text=tot_bank_db,bg=bg1,font=15)
    lab4.place(x=220,y=70)
    lab7=Label(vc1, fg=fg1,text=tot_cash_db,bg=bg1,font=15)
    lab7.place(x=220,y=110)
    lab5=Label(vc1, fg=fg1,text="Ammount:",bg=bg1,font=18)
    lab5.place(x=40,y=150)
    menu= StringVar(vc1)
    menu.set("Credit into Bank")
    list1=OptionMenu(vc1, menu,"Credit into Bank","Debit form Bank")
    list1.place(x=125,y=235)
    list1.config(bg=bg2,height=1)
    txt1=Entry(vc1,width=10,bg=bg2,font=18)
    txt1.place(x=220,y=150)
    txt2=DateEntry(vc1,selectmode='day',font=5,width=10,background='darkblue')
    txt2.place(x=220,y=190)
    def contra_submit():
            global c_type,c_amount
            c_type=menu.get()
            c_date=txt2.get_date()
            v1=False
            try:
                c_amount=int(txt1.get())
                v1=True
            except:
                messagebox.showinfo("Alert","Please Enter Valid Amount")
            # try:
            #     if(c_date <= curr_date):
            #         v2=True
            # except:
            #     messagebox.showinfo("Alert","Please Enter Valid Date")
            if v1 == True and c_amount != 0:
                if(c_type=="Credit into Bank"):
                    total_cash=int(tot_cash_db)-int(c_amount)
                    total_bank=int(tot_bank_db)+int(c_amount)
                    data_cash=(total_cash,total_bank,company_name_db)
                    mycursor.execute("UPDATE calculation SET tot_cash=%s,tot_bank=%s WHERE company_name=%s",data_cash)
                    mydb1.commit()
                    
                else:
                    total_cash=int(tot_cash_db)+int(c_amount)
                    total_bank=int(tot_bank_db)-int(c_amount)
                    data_cash=(total_cash,total_bank,company_name_db)
                    mycursor.execute("UPDATE calculation SET tot_cash=%s,tot_bank=%s WHERE company_name=%s",data_cash)
                    mydb1.commit()
                data=(company_name_db,c_date,c_type,c_amount)
                mycursor.execute("INSERT INTO contra(company_name,c_date,c_type,c_amount) VALUES(%s,%s,%s,%s)",data)
                mydb1.commit()
                vc1.destroy()
    but1=Button(vc1,fg=fg2,text="Submit",bg=bt1,cursor=cur1,activeforeground=afg,activebackground=abg,font=15,width=10,command=lambda:{contra_submit()})
    but1.place(x=140,y=280)
    vc1.mainloop()

# Sales Vouchers
def sales():
    global vc2
    fra_des()
    mycursor.execute("SELECT * FROM calculation WHERE company_name=%s",c_name)
    sql4=mycursor.fetchall()
    for row in sql4:
        global tot_cash_db,tot_bank_db
        tot_cash_db=row[1]
        tot_bank_db=row[2]
    vc2=Tk()
    vc2.minsize(width=420,height=400)
    vc2.maxsize(width=420,height=400)
    vc2.config(bg=bg1)
    vc2.title("Sales Voucher")
    # vc2.iconbitmap(ico_photo)
    lab1=Label(vc2, fg=fg1,text="Party Name:",bg=bg1,font=15)
    lab1.place(x=40,y=30)
    lab2=Label(vc2, fg=fg1,text="Date:",bg=bg1,font=15)
    lab2.place(x=40,y=70)
    lab3=Label(vc2, fg=fg1,text="Item Name:",bg=bg1,font=15)
    lab3.place(x=40,y=110)
    lab4=Label(vc2, fg=fg1,text="Quantity:",bg=bg1,font=15)
    lab4.place(x=40,y=150)
    lab5=Label(vc2, fg=fg1,text="Rate per Unit:",bg=bg1,font=15)
    lab5.place(x=40,y=190)
    lab6=Label(vc2, fg=fg1,text="GST%:",bg=bg1,font=15)
    lab6.place(x=40,y=230)
    lab7=Label(vc2, fg=fg1,text="Payment Type:",bg=bg1,font=15)
    lab7.place(x=40,y=270)
    menu1= StringVar(vc2)
    menu1.set("Bank")
    list2=OptionMenu(vc2, menu1,"Bank","Cash")
    list2.place(x=180,y=270)
    list2.config(bg=bg2,height=1)
    txt1=Entry(vc2,width=20,bg=bg2,font=15)
    txt1.place(x=180,y=30)
    txt2=DateEntry(vc2,width=10,bg=bg2,font=15)
    txt2.place(x=180,y=70)
    txt3=Entry(vc2,width=18,bg=bg2,font=15)
    txt3.place(x=180,y=110)
    txt4=Entry(vc2,width=5,bg=bg2,font=15)
    txt4.place(x=180,y=150)
    txt5=Entry(vc2,width=10,bg=bg2,font=15)
    txt5.place(x=180,y=190)
    txt6=Entry(vc2,width=5,bg=bg2,font=15)
    txt6.place(x=180,y=230)

    def sales_submit():
            global s_pname,s_date,s_itemname,s_quantity,s_rate,s_gst,s_type
            s_type=menu1.get()
            v1=False
            try:
                s_pname=str(txt1.get())
                s_date=txt2.get_date()
                s_itemname=str(txt3.get())
                s_quantity=int(txt4.get())
                s_rate=int(txt5.get())
                s_gst=int(txt6.get())
                v1=True
            except:
                messagebox.showinfo("Alert","Please Enter Valid information")
            if v1==True:
                if(s_type=="Cash"):
                    item_tot=(int(s_rate) * int(s_quantity))
                    gst_per=(int(item_tot)*int(s_gst))/100
                    tot_give=item_tot+gst_per
                    total_cash=int(tot_cash_db)+(item_tot+gst_per)
                    gst_per0=gst_take_cash_db+gst_per
                    data_cash=(total_cash,gst_per0,company_name_db)
                    mycursor.execute("UPDATE calculation SET tot_cash=%s,gst_take_cash=%s WHERE company_name=%s",data_cash)
                    mydb1.commit()
                    
                else:
                    item_tot=(int(s_rate) * int(s_quantity))
                    gst_per1=(int(item_tot)*int(s_gst))/100
                    tot_give=item_tot+gst_per1
                    total_bank=int(tot_bank_db)+(item_tot+gst_per1)
                    gst_per0=gst_take_bank_db+gst_per1
                    data_bank=(total_bank,gst_per0,company_name_db)
                    mycursor.execute("UPDATE calculation set tot_bank=%s,gst_take_bank=%s WHERE company_name=%s",data_bank)
                    mydb1.commit()

                data=(company_name_db,s_pname,s_date,s_itemname,s_quantity,s_rate,item_tot,s_gst,tot_give,s_type)
                mycursor.execute("INSERT INTO sales(company_name,s_pname,s_date,s_itemname,s_quantity,s_rate,s_total,s_gst,s_tot_pay,s_type) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",data)
                mydb1.commit()
                vc2.destroy()
    
    but1=Button(vc2,fg=fg2,text="Submit",bg=bt1,cursor=cur1,activeforeground=afg,activebackground=abg,font=15,width=10,command=lambda:{sales_submit()})
    but1.place(x=150,y=320)
    vc2.mainloop()

# Purchase Vouchers
def purchase():
    global vc3
    fra_des()
    mycursor.execute("SELECT * FROM calculation WHERE company_name=%s",c_name)
    sql4=mycursor.fetchall()
    for row in sql4:
        global tot_cash_db,tot_bank_db
        tot_cash_db=row[1]
        tot_bank_db=row[2]

    vc3=Tk()
    vc3.minsize(width=420,height=400)
    vc3.maxsize(width=420,height=400)
    vc3.config(bg=bg1)
    vc3.title("Purchase Voucher")
    # vc3.iconbitmap(ico_photo)
    lab1=Label(vc3, fg=fg1,text="Party Name:",bg=bg1,font=15)
    lab1.place(x=40,y=30)
    lab2=Label(vc3, fg=fg1,text="Date:",bg=bg1,font=15)
    lab2.place(x=40,y=70)
    lab3=Label(vc3, fg=fg1,text="Item Name:",bg=bg1,font=15)
    lab3.place(x=40,y=110)
    lab4=Label(vc3, fg=fg1,text="Quantity:",bg=bg1,font=15)
    lab4.place(x=40,y=150)
    lab5=Label(vc3, fg=fg1,text="Rate per Unit:",bg=bg1,font=15)
    lab5.place(x=40,y=190)
    lab6=Label(vc3, fg=fg1,text="GST%:",bg=bg1,font=15)
    lab6.place(x=40,y=230)
    lab7=Label(vc3, fg=fg1,text="Payment Type:",bg=bg1,font=15)
    lab7.place(x=40,y=270)
    menu1= StringVar(vc3)
    menu1.set("Bank")
    list2=OptionMenu(vc3, menu1,"Bank","Cash")
    list2.place(x=180,y=270)
    list2.config(bg=bg2,height=1)
    txt1=Entry(vc3,width=20,bg=bg2,font=15)
    txt1.place(x=180,y=30)
    txt2=DateEntry(vc3,width=10,bg=bg2,font=15)
    txt2.place(x=180,y=70)
    txt3=Entry(vc3,width=18,bg=bg2,font=15)
    txt3.place(x=180,y=110)
    txt4=Entry(vc3,width=5,bg=bg2,font=15)
    txt4.place(x=180,y=150)
    txt5=Entry(vc3,width=10,bg=bg2,font=15)
    txt5.place(x=180,y=190)
    txt6=Entry(vc3,width=5,bg=bg2,font=15)
    txt6.place(x=180,y=230)

    def purchase_submit():
            global p_pname,p_date,p_itemname,p_quantity,p_rate,p_gst,p_type
            p_type=menu1.get()
            v1=False
            try:
                p_pname=str(txt1.get())
                p_date=txt2.get_date()
                p_itemname=str(txt3.get())
                p_quantity=int(txt4.get())
                p_rate=int(txt5.get())
                p_gst=int(txt6.get())
                v1=True
            except:
                messagebox.showinfo("Alert","Please Enter Valid information")
            if v1==True:
                if(p_type=="Cash"):
                    item_tot=(int(p_rate) * int(p_quantity))
                    gst_per=(int(item_tot)*int(p_gst))/100
                    total_cash=int(tot_cash_db)-(item_tot+gst_per)
                    gst_per0=gst_give_cash_db+gst_per
                    tot_give=item_tot+gst_per
                    data_cash=(total_cash,gst_per0,company_name_db)
                    mycursor.execute("UPDATE calculation SET tot_cash=%s,gst_give_cash=%s WHERE company_name=%s",data_cash)
                    mydb1.commit()
                    
                else:
                    item_tot=(int(p_rate) * int(p_quantity))
                    gst_per1=(int(item_tot)*int(p_gst))/100
                    total_bank=int(tot_bank_db)-(item_tot+gst_per1)
                    gst_per0=gst_give_bank_db+gst_per1
                    tot_give=item_tot+gst_per1
                    data_bank=(total_bank,gst_per0,company_name_db)
                    mycursor.execute("UPDATE calculation set tot_bank=%s,gst_give_bank=%s WHERE company_name=%s",data_bank)
                    mydb1.commit()

                data=(company_name_db,p_pname,p_date,p_itemname,p_quantity,p_rate,item_tot,p_gst,tot_give,p_type)
                mycursor.execute("INSERT INTO purchase(company_name,p_pname,p_date,p_itemname,p_quantity,p_rate,p_total,p_gst,p_tot_pay,p_type) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",data)
                mydb1.commit()
                vc3.destroy()

    but1=Button(vc3,fg=fg2,text="Submit",bg=bt1,cursor=cur1,activeforeground=afg,activebackground=abg,font=15,width=10,command=lambda:{purchase_submit()})
    but1.place(x=150,y=320)
    
    vc3.mainloop()

# Other Vouchers
def other():
    global vc4
    fra_des()
    
    vc4=Tk()
    vc4.minsize(width=400,height=320)
    vc4.maxsize(width=400,height=320)
    vc4.config(bg=bg1)
    vc4.title("Other Voucher")
    # vc4.iconbitmap(ico_photo)
    lab1=Label(vc4, fg=fg1,text="Detail:",bg=bg1,font=15)
    lab1.place(x=40,y=30)
    lab2=Label(vc4, fg=fg1,text="Date:",bg=bg1,font=15)
    lab2.place(x=40,y=70)
    txt1=Entry(vc4,width=20,bg=bg2,font=18)
    txt1.place(x=125,y=30)
    txt2=DateEntry(vc4,width=10,bg=bg2,font=18)
    txt2.place(x=125,y=70)
    lab3=Label(vc4, fg=fg1,text="Ammount:",bg=bg1,font=15)
    lab3.place(x=40,y=110)
    lab4=Label(vc4, fg=fg1,text="GST%:",bg=bg1,font=15)
    lab4.place(x=40,y=150)
    lab5=Label(vc4, fg=fg1,text="Payment Type:",bg=bg1,font=15)
    lab5.place(x=40,y=190)
    menu1= StringVar(vc4)
    menu1.set("Bank")
    list2=OptionMenu(vc4, menu1,"Bank","Cash")
    list2.place(x=160,y=190)
    list2.config(bg=bg2,height=1)
    menu= StringVar(vc4)
    menu.set("Credit")
    list1=OptionMenu(vc4, menu,"Credit","Debit")
    list1.place(x=125,y=110)
    list1.config(bg=bg2,height=1)
    txt3=Entry(vc4,width=10,bg=bg2,font=18)
    txt3.place(x=220,y=110)
    txt4=Entry(vc4,width=5,bg=bg2,font=15)
    txt4.place(x=125,y=150)

    def other_submit():

        mycursor.execute("SELECT * FROM calculation WHERE company_name=%s",c_name)
        sql4=mycursor.fetchall()
        for row in sql4:
            global tot_cash_db,tot_bank_db
            tot_cash_db=row[1]
            tot_bank_db=row[2]
            global o_detail,o_date,o_method,o_amount,o_gst,o_type
            
            o_date=txt2.get_date()
            o_method=menu.get()
            o_type=menu1.get()
            v1=False
            try:
                o_detail=str(txt1.get())
                o_amount=int(txt3.get())
                o_gst=int(txt4.get())
                v1=True
            except:
                messagebox.showinfo("Alert","Please Enter Valid information")
            if v1==True:
                if(o_method=="Debit"):
                    if(o_type=="Cash"):
                            item_tot=(int(o_amount))
                            gst_per=(int(item_tot)*int(o_gst))/100
                            total_cash=int(tot_cash_db)-(item_tot+gst_per)   
                            gst_per0=gst_give_cash_db+gst_per               
                            data_cash=(total_cash,gst_per0,company_name_db)
                            mycursor.execute("UPDATE calculation SET tot_cash=%s,gst_give_cash=%s WHERE company_name=%s",data_cash)
                            mydb1.commit()
                        
                    else:
                            item_tot=(int(o_amount))
                            gst_per=(int(item_tot)*int(o_gst))/100
                            total_bank=int(tot_bank_db)-(item_tot+gst_per)
                            gst_per0=gst_give_bank_db+gst_per
                            data_bank=(total_bank,gst_per0,company_name_db)
                            mycursor.execute("UPDATE calculation set tot_bank=%s,gst_give_bank=%s WHERE company_name=%s",data_bank)
                            mydb1.commit()
                elif(o_method=="Credit"):
                    if(o_type=="Cash"):
                            item_tot=(int(o_amount))
                            gst_per=(int(item_tot)*int(o_gst))/100
                            total_cash=int(tot_cash_db)+(item_tot+gst_per)
                            gst_per0=gst_take_cash_db+gst_per
                            data_cash=(total_cash,gst_per0,company_name_db)
                            mycursor.execute("UPDATE calculation SET tot_cash=%s,gst_take_cash=%s WHERE company_name=%s",data_cash)
                            mydb1.commit()
                        
                    else:
                            item_tot=(int(o_amount))
                            gst_per=(int(item_tot)*int(o_gst))/100
                            total_bank=int(tot_bank_db)+(item_tot+gst_per)
                            gst_per0=gst_take_bank_db+gst_per
                            data_bank=(total_bank,gst_per0,company_name_db)
                            mycursor.execute("UPDATE calculation set tot_bank=%s,gst_take_bank=%s WHERE company_name=%s",data_bank)
                            mydb1.commit()
                tot_pay=item_tot+gst_per
                data=(company_name_db,o_detail,o_date,o_method,o_amount,o_gst,tot_pay,o_type)
                mycursor.execute("INSERT INTO other(company_name,o_detail,o_date,o_method,o_amount,o_gst,o_tot_pay,o_type) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",data)
                mydb1.commit()
                vc4.destroy()

    but1=Button(vc4,fg=fg2,text="Submit",bg=bt1,cursor=cur1,activeforeground=afg,activebackground=abg,font=15,width=10,command=lambda:{other_submit()})
    but1.place(x=140,y=240)
    vc4.mainloop()

#getdata
def getdata():
    #c_creation

    mycursor.execute("SELECT * FROM c_creation WHERE company_name=%s",c_name)
    sql=mycursor.fetchall()
    for row in sql:
        global company_name_db,mail_address_db,country_db,state_db,pincode_db,telephone_db,mobile_db,email_db,website_db,financial_year_db,books_db,type_gst_db,from_gst_db,gstin_gst_db,period_gst_db,password_db,cash_db_db,branch_name_db,bank_db_db
                    
        company_name_db=row[0]
        mail_address_db=row[1]
        country_db=row[2]
        state_db=row[3]
        pincode_db=row[4]
        mobile_db=row[5]
        telephone_db=row[6]
        email_db=row[7]
        website_db=row[8]
        financial_year_db=row[9]
        books_db=row[10]
        type_gst_db=row[11]
        from_gst_db=row[12]
        gstin_gst_db=row[13]
        period_gst_db=row[14]
        password_db=row[15]
        cash_db_db=row[16]
        branch_name_db=row[17]
        bank_db_db=row[18]

    #sales

    mycursor.execute("SELECT * FROM sales WHERE company_name=%s",c_name)
    sql1=mycursor.fetchall()
    for row in sql1:
        global s_pname_db,s_date_db,s_itemname_db,s_quantity_db,s_rate_db,s_total_db,s_gst_db,s_tot_pay_db,s_type_db,sales_total
        s_pname_db=row[1]
        s_date_db=row[2]
        s_itemname_db=row[3]
        s_quantity_db=row[4]
        s_rate_db=row[5]
        s_total_db=row[6]
        s_gst_db=row[7]
        s_tot_pay_db=row[8]
        s_type_db=row[9]
 

    #purchase

    mycursor.execute("SELECT * FROM purchase WHERE company_name=%s",c_name)
    sql2=mycursor.fetchall()
    for row in sql2:
        global p_pname_db,p_date_db,p_itemname_db,p_quantity_db,p_rate_db,p_total_db,p_gst_db,p_tot_pay_db,p_type_db
        p_pname_db=row[1]
        p_date_db=row[2]
        p_itemname_db=row[3]
        p_quantity_db=row[4]
        p_rate_db=row[5]
        p_total_db=row[6]
        p_gst_db=row[7]
        p_tot_pay_db=row[8]
        p_type_db=row[9]

    #contra

    mycursor.execute("SELECT * FROM contra WHERE company_name=%s",c_name)
    sql3=mycursor.fetchall()
    for row in sql3:
        global c_type_db,c_amount_db
        c_type_db=row[1]
        c_amount_db=row[2]

    #other

    mycursor.execute("SELECT * FROM other WHERE company_name=%s",c_name)
    sql4=mycursor.fetchall()
    for row in sql4:
        global o_detail_db,o_date_db,o_method_db,o_amount_db,o_gst_db,o_tot_pay_db,o_type_db
        o_detail_db=row[1]
        o_date_db=row[2]
        o_method_db=row[3]
        o_amount_db=row[4]
        o_gst_db=row[5]
        o_tot_pay_db=row[6]
        o_type_db=row[7]

    #calculation

    mycursor.execute("SELECT * FROM calculation WHERE company_name=%s",c_name)
    sql4=mycursor.fetchall()
    for row in sql4:
        global tot_cash_db,tot_bank_db,gst_give_bank_db,gst_take_bank_db,gst_take_cash_db,gst_give_cash_db
        tot_cash_db=row[1]
        tot_bank_db=row[2]
        gst_give_cash_db=row[3]
        gst_take_cash_db=row[4]
        gst_give_bank_db=row[5]
        gst_take_bank_db=row[6]

#totals
def tot():

    global curr_date,cur_date
    date_cur=datetime.now()
    curr_date=datetime.date(date_cur)
    cur_date=curr_date.strftime("%d-%m-%Y")

    mycursor.execute("select p_total from purchase where company_name=%s and p_type=%s",(c_name_string,'Bank'))
    sql1=mycursor.fetchall()
    mycursor.execute("select s_total from sales where company_name=%s and s_type=%s",(c_name_string,'Bank'))
    sql2=mycursor.fetchall()
    mycursor.execute("select o_amount from other where company_name=%s and o_method=%s and o_type=%s",(c_name_string,'Credit','Bank'))
    sql3=mycursor.fetchall()
    mycursor.execute("select p_total from purchase where company_name=%s and p_type=%s",((c_name_string,"Cash")))
    sql4=mycursor.fetchall()
    mycursor.execute("select s_total from sales where company_name=%s and s_type=%s",((c_name_string,"Cash")))
    sql5=mycursor.fetchall()
    mycursor.execute("select o_amount from other where company_name=%s and o_method=%s and o_type=%s",(c_name_string,'Debit','Bank'))
    sql6=mycursor.fetchall()
    mycursor.execute("select o_amount from other where company_name=%s and o_method=%s and o_type=%s",(c_name_string,'Credit','Cash'))
    sql7=mycursor.fetchall()
    mycursor.execute("select o_amount from other where company_name=%s and o_method=%s and o_type=%s",(c_name_string,'Debit','Cash'))
    sql8=mycursor.fetchall()
    mycursor.execute("SELECT c_amount FROM contra where company_name=%s and c_type=%s",(c_name_string,'Credit into Bank'))
    sql9=mycursor.fetchall()
    mycursor.execute("SELECT c_amount FROM contra where company_name=%s and c_type=%s",(c_name_string,'Debit from Bank'))
    sql10=mycursor.fetchall()
    sum1=0
    sum2=0
    sum3=0
    sum4=0
    sum5=0
    sum6=0
    sum7=0
    sum8=0
    sum9=0
    sum10=0

    for i in sql1:
        sum1+=i[0]
    for ii in sql2:  
        sum2+=ii[0]
    for iii in sql3:
        sum3+=iii[0]
    for iv in sql4:
        sum4+=iv[0]
    for v in sql5:
        sum5+=v[0]
    for vi in sql6:
        sum6+=vi[0]
    for vii in sql7:
        sum7+=vii[0]
    for viii in sql8:
        sum8+=viii[0]
    for ix in sql9:
        sum9+=ix[0]
    for x in sql10:
        sum10+=x[0]

    # bank_sum_tot2=credit
    # bank_sum_tot=debit
    global cash_sum_tot,cash_sum_tot2,bank_sum_tot,bank_sum_tot2,journal_tot,journal_tot2,cash_in_hand,bank_in_hand,bal_hand
    cash_sum_tot=sum4+sum8+sum9
    cash_sum_tot2=sum5+sum7+sum10+cash_db_db
    bank_sum_tot=sum1+sum6+sum10
    bank_sum_tot2=sum2+sum3+sum9+bank_db_db
    journal_tot2=sum5+sum7+sum2+sum3+cash_db_db+bank_db_db
    journal_tot=sum4+sum8+sum1+sum6


    cash_in_hand=cash_sum_tot2-cash_sum_tot
    bank_in_hand=bank_sum_tot2-bank_sum_tot
    bal_hand=journal_tot2-journal_tot

    global cash_profit,cash_loss
    cash_profit=cash_sum_tot2-cash_sum_tot
    cash_loss=cash_sum_tot-cash_sum_tot2

    global bank_profit,bank_loss
    bank_profit=bank_sum_tot2-bank_sum_tot
    bank_loss=bank_sum_tot-bank_sum_tot2

    if cash_in_hand > 0:
        cash_sum_tot = cash_sum_tot + cash_in_hand
    else:
        cash_sum_tot2 = cash_sum_tot2 + abs(cash_in_hand)
    if bank_in_hand > 0:
        bank_sum_tot = bank_sum_tot + bank_in_hand
    else:
        bank_sum_tot2 = bank_sum_tot2 + abs(bank_in_hand)
    if bal_hand > 0:
        journal_tot = journal_tot + bal_hand
    else:
        journal_tot2 = journal_tot2 + abs(bal_hand)

# Main Form
def main2():

    try:
        main1.destroy()
    except:
        pass
    getdata()
    global win3
    win3=Tk()
    win3.title("Accounting System")
    # win3.iconbitmap(ico_photo)
    win3.state("zoomed")
    win3.geometry('1500x700')
    win3.config(bg=bg1)
    global fra1
    fra1=Frame(win3, bg=bg2,borderwidth=5,relief=SUNKEN,width=290,height=700)
    fra1.place(x=1075,y=10)
    fra2=Frame(win3, bg=bg2,borderwidth=5,relief=SUNKEN,width=1075,height=200)
    fra2.place(x=0,y=10)  
    #style
    style=ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview",background="light blue",foreground=fg1,font=15,rowheight="27",fieldbackground="light gray")
    style.map("Treeview",background=[('selected','green')])

    def get_tree_items():
        # Create a list to store the items
        items = []
        items.append(['Date', 'Detail(Debit)','Amount'])
        try:
            children = tj.get_children()    
            for child in children:
                item = tj.item(child)
                items.append(item['values'])
            items.append(['', 'Total',journal_tot2])
        except:
            pass
        try:
            children = cv.get_children()    
            for child in children:
                item = cv.item(child)
                items.append(item['values'])
            items.append(['', 'Total',cash_sum_tot2])
        except:
            pass
        try:
            children = tv.get_children()    
            for child in children:
                item = tv.item(child)
                items.append(item['values'])
            items.append(['', 'Total',bank_sum_tot2])
        except:
            pass
        return items

    def get_tree_items2():
        items2=[]
        items2.append(['Date', 'Detail(Credit)','Amount'])
        try:
            children2=tj1.get_children()
            for child2 in children2:
                item = tj1.item(child2)
                items2.append(item['values'])
            items2.append(['', 'Total',journal_tot])
        except:
            pass
        try:
            children2=cv1.get_children()
            for child2 in children2:
                item = cv1.item(child2)
                items2.append(item['values'])
            items2.append(['', 'Total',cash_sum_tot])
        except:
            pass
        try:
            children2=tv1.get_children()
            for child2 in children2:
                item = tv1.item(child2)
                items2.append(item['values'])
            items2.append(['', 'Total',bank_sum_tot])
        except:
            pass
        return items2

    # def cus():
    #     global pdfrp
    #     customtkinter.set_appearance_mode("dark")
    #     customtkinter.set_default_color_theme("dark-blue")
    #     pdfrp=customtkinter.CTk()
    #     pdfrp.minsize(width=150,height=170)
    #     pdfrp.minsize(width=150,height=170)



    #     global txt
    #     lab=customtkinter.CTkLabel(pdfrp,text="Enter File Name:")
    #     lab.pack()
    #     txt=customtkinter.CTkEntry(pdfrp,placeholder_text="only name")
    #     txt.pack()

        def gen():
            file_name=txt.get()
            fileName=f"{file_name}.pdf"

            pdf = SimpleDocTemplate(
                fileName,
                pagesize=letter
            )

            table = Table(get_tree_items())
            table2 = Table(get_tree_items2())

            combined_table_data=[[table,table2]]
            colWidths=[250,250]

            # table1=Table(combined_table_data,colWidths=colWidths)

            style = TableStyle([
                ('BACKGROUND', (0,0), (3,0), colors.green),
                ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),

                ('ALIGN',(0,0),(-1,-1),'CENTER'),

                ('FONTNAME', (0,0), (-1,0), 'Courier-Bold'),
                ('FONTSIZE', (0,0), (-1,0), 14),

                ('BOTTOMPADDING', (0,0), (-1,0), 12),

                ('BACKGROUND',(0,1),(-1,-1),colors.beige),
                ('VALIGE',(0,0),(-1,-1),'TOP'),
                ('hGrid',(0,0),(-1,-1),0,colors.white),
                ('PADDING',(0,0),(0,0),0)

            ])
            # table1.setStyle(style)
            style2 = TableStyle([
                ('BACKGROUND', (0,0), (3,0), colors.green),
                ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),

                ('ALIGN',(0,0),(-1,-1),'CENTER'),

                ('FONTNAME', (0,0), (-1,0), 'Courier-Bold'),
                ('FONTSIZE', (0,0), (-1,0), 14),

                ('BOTTOMPADDING', (0,0), (-1,0), 12),

                ('BACKGROUND',(0,1),(-1,-1),colors.beige),
            ])
            table.setStyle(style)
            table2.setStyle(style2)

            # 2) Alternate backgroud color
            rowNumb = len(get_tree_items())
            for i in range(1, rowNumb):
                if i % 2 == 0:
                    bc = colors.burlywood
                else:
                    bc = colors.beige
                
                ts = TableStyle(
                    [('BACKGROUND', (0,i),(-1,i), bc)]
                )
                table.setStyle(ts)

            rowNumb2 = len(get_tree_items2())
            for i in range(1, rowNumb2):
                if i % 2 == 0:
                    bc = colors.burlywood
                else:
                    bc = colors.beige
                
                ts = TableStyle(
                    [('BACKGROUND', (0,i),(-1,i), bc)]
                )
                table2.setStyle(ts)

            # 3) Add borders
            ts = TableStyle(
                [
                ('BOX',(0,0),(-1,-1),2,colors.black),

                ('LINEBEFORE',(2,1),(2,-1),2,colors.red),
                ('LINEABOVE',(0,2),(-1,2),2,colors.green),

                ('GRID',(0,1),(-1,-1),2,colors.black),
                ]
            )
            table.setStyle(ts)
            table2.setStyle(ts)

            elems = []
            elems.append(table)
            elems.append(table2)

            pdf.build(elems)
            try:
                pdfrp.destroy()
            except:
                pass

        but=customtkinter.CTkButton(pdfrp,text="Create",command=gen)
        but.pack()

        pdfrp.mainloop()


    def cash_main():
        global fra3,but9,but10
        fra_des()
        tot()
        
        fra3=Frame(win3,bg=bg1,borderwidth=5,relief=SOLID,width=1072,height=500)
        fra3.place(x=0,y=210)

        global cv,cv1,rpdatec1,rplabc1,rpdatec2,rplabc2

        laba1=Label(fra3,fg=fg1,text="Cash Ledger",font=("bold",20,"underline"),bg=bg1).place(x=455,y=2)
        cv = ttk.Treeview(fra3,columns=(1, 2, 3), show='headings', height=14,cursor=cur1)

        rplabc1=Label(fra2, fg=fg1,text="Select Starting Date:",font=15,bg=bg2)
        rplabc1.place(x=800,y=76)
        rpdatec1=DateEntry(fra2,selectmode='day',font=5,width=10,background='darkblue',month=4,day=1,year=2022)
        rpdatec1.place(x=850,y=100)
        rplabc2=Label(fra2, fg=fg1,text="Select Endind Date:",font=15,bg=bg2)
        rplabc2.place(x=800,y=125)
        rpdatec2=DateEntry(fra2,selectmode='day',font=5,width=10,background='darkblue')
        rpdatec2.place(x=850,y=150)

        cv.place(x=0,y=43)
        cv.column('# 1',anchor=CENTER,stretch=NO,width=134)
        cv.column('# 2',anchor=CENTER,stretch=NO,width=260)
        cv.column('# 3',anchor=CENTER,stretch=NO,width=134)

        def sort_date_column(cv, col, reverse):
            data = [(datetime.strptime(cv.item(item, 'values')[col], '%d-%m-%Y'), item) for item in cv.get_children()]
            data.sort(reverse=reverse)
            for index, item in enumerate(data):
                cv.move(item[1], '', index)
        def sort_date_column2(cv1, col, reverse):
            data = [(datetime.strptime(cv1.item(item, 'values')[col], '%d-%m-%Y'), item) for item in cv1.get_children()]
            data.sort(reverse=reverse)
            for index, item in enumerate(data):
                cv1.move(item[1], '', index)

        cv1 = ttk.Treeview(fra3, columns=(1, 2, 3), show='headings', height=14,cursor=cur1)
        cv1.place(x=529,y=43)
        cv1.column(1,anchor=CENTER,stretch=NO,width=134)
        cv1.column(2,anchor=CENTER,stretch=NO,width=260)
        cv1.column(3,anchor=CENTER,stretch=NO,width=134)

        cv.heading(1, text="Date" ,command=lambda: sort_date_column(cv, 0, True))
        cv.heading(2, text="Details(Debit)")
        cv.heading(3, text="Amount")
        cv1.heading(1, text="Date" ,command=lambda: sort_date_column(cv1, 0, True))
        cv1.heading(2, text="Details(Credit)")
        cv1.heading(3, text="Amount")

        sb = Scrollbar(fra3, orient=VERTICAL)
        cv.config(yscrollcommand=sb.set)
        cv1.config(yscrollcommand=sb.set)
        sb.config(command=cv1.yview)
        sb.config(command=cv.yview)

        def report():
            for item1 in cv.get_children():
                cv.delete(item1)
            for item2 in cv1.get_children():
                cv1.delete(item2)
            
            rdatec1=rpdatec1.get_date()
            rdatec2=rpdatec2.get_date()
            # data=(c_name_string,rpdatec1,rpdatec2)
            # data1=(c_name_string,'Credit',rpdatec1,rpdatec2)
            # data2=(c_name_string,'Debit',rpdatec1,rpdatec2)
            
            data=(c_name_string,'Cash',rdatec1,rdatec2)
            data1=(c_name_string,'Credit','Cash',rdatec1,rdatec2)
            data2=(c_name_string,'Debit','Cash',rdatec1,rdatec2)
            data3=(c_name_string,'Credit into Bank',rdatec1,rdatec2)
            data4=(c_name_string,'Debit from Bank',rdatec1,rdatec2)
            mycursor.execute("SELECT p_date,p_pname,p_itemname,p_total FROM purchase where company_name=%s AND p_type=%s AND p_date BETWEEN %s and %s",data)
            sql1=mycursor.fetchall()
            mycursor.execute("SELECT s_date,s_pname,s_itemname,s_total FROM sales where company_name=%s and s_type=%s AND s_date BETWEEN %s and %s",data)
            sql2=mycursor.fetchall()
            mycursor.execute("SELECT o_date,o_detail,o_amount FROM other where company_name=%s and o_method=%s and o_type=%s AND o_date BETWEEN %s and %s",data1)
            sql3=mycursor.fetchall()
            mycursor.execute("SELECT o_date,o_detail,o_amount FROM other where company_name=%s and o_method=%s and o_type=%s AND o_date BETWEEN %s and %s",data2)
            sql4=mycursor.fetchall()
            mycursor.execute("SELECT c_date,c_type,c_amount FROM contra where company_name=%s and c_type=%s AND c_date BETWEEN %s and %s",data3)
            sql5=mycursor.fetchall()
            mycursor.execute("SELECT c_date,c_type,c_amount FROM contra where company_name=%s and c_type=%s AND c_date BETWEEN %s and %s",data4)
            sql6=mycursor.fetchall()

            for row in sql1:
                dt1=row[0].strftime("%d-%m-%Y")
                cv.insert(parent='', index=1, values=(dt1, row[1]+"("+row[2]+")",row[3]))
            for row1 in sql2:
                dt2=row1[0].strftime("%d-%m-%Y")
                cv1.insert(parent='', index=1, values=(dt2, row1[1]+"("+row1[2]+")",row1[3]))
            for row2 in sql3:
                dt3=row2[0].strftime("%d-%m-%Y")
                cv1.insert(parent='', index=1, values=(dt3, row2[1] , row2[2]))
            for row3 in sql4:
                dt4=row3[0].strftime("%d-%m-%Y")
                cv.insert(parent='', index=1, values=(dt4, row3[1] , row3[2])) 
            for row4 in sql5:
                dt5=row4[0].strftime("%d-%m-%Y")
                cv.insert('', 'end', values=(dt5, row4[1] , row4[2]))
            for row5 in sql6:
                dt6=row5[0].strftime("%d-%m-%Y")
                cv1.insert('', 'end', values=(dt6, row5[1] , row5[2]))

        def update_item():
            try:
                if cv.selection() and cv1.selection():
                    selected=cv.selection()
                    selected1=cv1.selection()
                    messagebox.showinfo("Info","Select One Thing")
                    cv.selection_remove(selected)
                    cv1.selection_remove(selected1)

                elif cv.selection():
                    selected = cv.selection()
                    temp = cv.item(selected, 'values')
                    date_back=datetime.strptime(temp[0],'%d-%m-%Y')
                    new_date_str=date_back.strftime('%Y-%m-%d')
                    data=new_date_str,temp[1],temp[2]
                    try:
                        mycursor.execute("select * from other where o_date=%s AND o_detail=%s AND o_amount=%s",data)
                        sql1=mycursor.fetchone()
                        if sql1!=None:
                            print(sql1)
                        else:
                            pass
                    except:
                        pass
                    try:
                        input_str=temp[1]
                        open_index=input_str.index("(")
                        close_index=input_str.index(")")
                        string1=input_str[:open_index]
                        string2=input_str[open_index+1:close_index]
                        data3=new_date_str,string1,string2,temp[2]
                        mycursor.execute("select * from purchase where p_date=%s AND p_pname=%s AND p_itemname=%s AND p_total=%s",data3)
                        sql2=mycursor.fetchone()
                        if sql2!=None:
                            print(sql2)
                        else:
                            pass
                    except:
                        pass
                    try:
                        mycursor.execute("select * from contra where c_date=%s AND c_type=%s AND c_amount=%s",data)
                        sql1=mycursor.fetchone()
                        if sql1!=None:
                            print(sql1)
                        else:
                            pass
                    except:
                        pass
                    cv.selection_remove(selected)

                elif cv1.selection():
                    selected = cv1.selection()
                    temp = cv1.item(selected, 'values')
                    date_back=datetime.strptime(temp[0],'%d-%m-%Y')
                    new_date_str=date_back.strftime('%Y-%m-%d')
                    data=new_date_str,temp[1],temp[2]
                    try:
                        mycursor.execute("select * from other where o_date=%s AND o_detail=%s AND o_amount=%s",data)
                        sql1=mycursor.fetchone()
                        if sql1!=None:
                            print(sql1)
                        else:
                            pass
                    except:
                       pass
                    try:
                        input_str=temp[1]
                        open_index=input_str.index("(")
                        close_index=input_str.index(")")
                        string1=input_str[:open_index]
                        string2=input_str[open_index+1:close_index]
                        data3=new_date_str,string1,string2,temp[2]
                        mycursor.execute("select * from sales where s_date=%s AND s_pname=%s AND s_itemname=%s AND s_total=%s",data3)
                        sql2=mycursor.fetchone()
                        if sql2!=None:
                            print(sql2)
                        else:
                            pass
                    except:
                       pass
                    try:
                        mycursor.execute("select * from contra where c_date=%s AND c_type=%s AND c_amount=%s",data)
                        sql1=mycursor.fetchone()
                        if sql1!=None:
                            print(sql1)
                        else:
                            pass
                    except:
                       pass
                    print(data)
                    if (data == books_db_str, "Starting Cash Amount", cash_db_db):
                        messagebox.showinfo("Information","This data Can't be edited")
                    
                    cv1.selection_remove(selected)
                else:
                    messagebox.showerror("Error","Please select the data you want to edit")
            except:
                messagebox.showerror("Error","Please select the data you want to edit")
        but9=Button(fra1,text='Edit Record',width=25,bg=bt2,activeforeground=afg,activebackground=abg,fg=fg2,font=(15),command=update_item,cursor=cur1)
        but9.place(x=25,y=550)
        but10=Button(fra1,text='Search',width=25,bg=bt2,activeforeground=afg,activebackground=abg,fg=fg2,font=(15),command=report,cursor=cur1)
        but10.place(x=25,y=600)
        # but11=Button(fra1,text='Get PDF',width=25,bg=bt2,activeforeground=afg,activebackground=abg,fg=fg2,font=(15),command=cus,cursor=cur1)
        # but11.place(x=25,y=540)
        data=(c_name_string,'Cash')
        data1=(c_name_string,'Credit','Cash')
        data2=(c_name_string,'Debit','Cash')
        data3=(c_name_string,'Credit into Bank')
        data4=(c_name_string,'Debit from Bank')
        mycursor.execute("SELECT p_date,p_pname,p_itemname,p_total FROM purchase where company_name=%s AND p_type=%s",data)
        sql1=mycursor.fetchall()
        mycursor.execute("SELECT s_date,s_pname,s_itemname,s_total FROM sales where company_name=%s and s_type=%s",data)
        sql2=mycursor.fetchall()
        mycursor.execute("SELECT o_date,o_detail,o_amount FROM other where company_name=%s and o_method=%s and o_type=%s",data1)
        sql3=mycursor.fetchall()
        mycursor.execute("SELECT o_date,o_detail,o_amount FROM other where company_name=%s and o_method=%s and o_type=%s",data2)
        sql4=mycursor.fetchall()
        mycursor.execute("SELECT c_date,c_type,c_amount FROM contra where company_name=%s and c_type=%s",data3)
        sql5=mycursor.fetchall()
        mycursor.execute("SELECT c_date,c_type,c_amount FROM contra where company_name=%s and c_type=%s",data4)
        sql6=mycursor.fetchall()

        books_db_str=books_db.strftime("%d-%m-%Y")
        cv1.insert(parent='', index=0, values=(books_db_str, "Starting Cash Amount", cash_db_db))
            
        for row in sql1:
            dt1=row[0].strftime("%d-%m-%Y")
            cv.insert(parent='', index=1, values=(dt1, row[1]+"("+row[2]+")",row[3]))
        for row1 in sql2:
            dt2=row1[0].strftime("%d-%m-%Y")
            cv1.insert(parent='', index=1, values=(dt2, row1[1]+"("+row1[2]+")",row1[3]))
        for row2 in sql3:
            dt3=row2[0].strftime("%d-%m-%Y")
            cv1.insert(parent='', index=1, values=(dt3, row2[1] , row2[2]))
        for row3 in sql4:
            dt4=row3[0].strftime("%d-%m-%Y")
            cv.insert(parent='', index=1, values=(dt4, row3[1] , row3[2])) 
        for row4 in sql5:
            dt5=row4[0].strftime("%d-%m-%Y")
            cv.insert('', 'end', values=(dt5, row4[1] , row4[2]))
        for row5 in sql6:
            dt6=row5[0].strftime("%d-%m-%Y")
            cv1.insert('', 'end', values=(dt6, row5[1] , row5[2]))

        if cash_in_hand>0:
            cv.insert('', 'end', values=(cur_date, "Cash in Hand", cash_in_hand))           
        else:
            cv1.insert('', 'end', values=(cur_date, "Cash in Hand", abs(cash_in_hand)))

        lab_tot=Label(fra3,text=cash_sum_tot2,font=("bold",12),fg=fg1,bg="light blue")
        lab_tot.place(x=965,y=453)
        lab_tot2=Label(fra3,text=cash_sum_tot,font=("bold",12),fg=fg1,bg="light blue")
        lab_tot2.place(x=425,y=453)
         
    def bank_main():
        global fra4,but9,rpdateb1,rplabb1,rpdateb2,rplabb2,but10
        fra_des()
        tot()
        fra4=Frame(win3,bg=bg1,borderwidth=5,relief=SOLID,width=1072,height=500)
        fra4.place(x=0,y=210)
        rplabb1=Label(fra2, fg=fg1,text="Select Starting Date:",font=15,bg=bg2)
        rplabb1.place(x=800,y=76)
        rpdateb1=DateEntry(fra2,selectmode='day',font=5,width=10,background='darkblue',month=4,day=1,year=2022)
        rpdateb1.place(x=850,y=100)
        rplabb2=Label(fra2, fg=fg1,text="Select Endind Date:",font=15,bg=bg2)
        rplabb2.place(x=800,y=125)
        rpdateb2=DateEntry(fra2,selectmode='day',font=5,width=10,background='darkblue')
        rpdateb2.place(x=850,y=150)

        def sort_date_column(tv, col, reverse):
            data = [(datetime.strptime(tv.item(item, 'values')[col], '%d-%m-%Y'), item) for item in tv.get_children()]
            data.sort(reverse=reverse)
            for index, item in enumerate(data):
                tv.move(item[1], '', index)
        def sort_date_column2(tv1, col, reverse):
            data = [(datetime.strptime(tv1.item(item, 'values')[col], '%d-%m-%Y'), item) for item in tv1.get_children()]
            data.sort(reverse=reverse)
            for index, item in enumerate(data):
                tv1.move(item[1], '', index)

        global tv,tv1
        laba1=Label(fra4,fg=fg1,text="Bank Ledger",font=("bold",20,"underline"),bg=bg1).place(x=455,y=2)
        tv = ttk.Treeview(fra4,columns=(1, 2, 3), show='headings', height=14,cursor=cur1)
        tv.place(x=0,y=43)
        tv.column(1,anchor=CENTER,stretch=NO,width=134)
        tv.column(2,anchor=CENTER,stretch=NO,width=260)
        tv.column(3,anchor=CENTER,stretch=NO,width=134)
        tv1 = ttk.Treeview(fra4, columns=(1, 2, 3), show='headings', height=14,cursor=cur1)
        tv1.place(x=529,y=43)
        tv1.column(1,anchor=CENTER,stretch=NO,width=134)
        tv1.column(2,anchor=CENTER,stretch=NO,width=260)
        tv1.column(3,anchor=CENTER,stretch=NO,width=134)

        tv.heading(1, text="Date" ,command=lambda: sort_date_column(tv, 0, True))
        tv.heading(2, text="Details(Debit)")
        tv.heading(3, text="Amount")
        tv1.heading(1, text="Date" ,command=lambda: sort_date_column2(tv1, 0, True))
        tv1.heading(2, text="Details(Credit)")
        tv1.heading(3, text="Amount")

        sb = Scrollbar(fra4, orient=VERTICAL)
        tv.config(yscrollcommand=sb.set)
        tv1.config(yscrollcommand=sb.set)
        sb.config(command=tv1.yview)
        sb.config(command=tv.yview)

        def report():
            for item1 in tv.get_children():
                tv.delete(item1)
            for item2 in tv1.get_children():
                tv1.delete(item2)
            
            rdateb1=rpdateb1.get_date()
            rdateb2=rpdateb2.get_date()
            # data=(c_name_string,rpdatec1,rpdatec2)
            # data1=(c_name_string,'Credit',rpdatec1,rpdatec2)
            # data2=(c_name_string,'Debit',rpdatec1,rpdatec2)
            
            data=(c_name_string,'Bank',rdateb1,rdateb2)
            data1=(c_name_string,'Credit','Bank',rdateb1,rdateb2)
            data2=(c_name_string,'Debit','Bank',rdateb1,rdateb2)
            data3=(c_name_string,'Credit into Bank',rdateb1,rdateb2)
            data4=(c_name_string,'Debit from Bank',rdateb1,rdateb2)
            mycursor.execute("SELECT p_date,p_pname,p_itemname,p_total FROM purchase where company_name=%s AND p_type=%s AND p_date BETWEEN %s AND %s",data)
            sql1=mycursor.fetchall()
            mycursor.execute("SELECT s_date,s_pname,s_itemname,s_total FROM sales where company_name=%s and s_type=%s and s_date BETWEEN %s AND %s",data)
            sql2=mycursor.fetchall()
            mycursor.execute("SELECT o_date,o_detail,o_amount FROM other where company_name=%s and o_method=%s and o_type=%s and o_date BETWEEN %s AND %s",data1)
            sql3=mycursor.fetchall()
            mycursor.execute("SELECT o_date,o_detail,o_amount FROM other where company_name=%s and o_method=%s and o_type=%s and o_date BETWEEN %s AND %s",data2)
            sql4=mycursor.fetchall()
            mycursor.execute("SELECT c_date,c_type,c_amount FROM contra where company_name=%s and c_type=%s and c_date BETWEEN %s AND %s",data3)
            sql5=mycursor.fetchall()
            mycursor.execute("SELECT c_date,c_type,c_amount FROM contra where company_name=%s and c_type=%s and c_date BETWEEN %s AND %s",data4)
            sql6=mycursor.fetchall()

            for row in sql1:
                dt1=row[0].strftime("%d-%m-%Y")
                tv.insert('', 'end', values=(dt1, row[1]+"("+row[2]+")",row[3]))
            for row1 in sql2:
                dt2=row1[0].strftime("%d-%m-%Y")
                tv1.insert('', 'end', values=(dt2, row1[1]+"("+row1[2]+")",row1[3]))
            for row2 in sql3:
                dt3=row2[0].strftime("%d-%m-%Y")
                tv1.insert('', 'end', values=(dt3, row2[1] , row2[2]))
            for row3 in sql4:
                dt4=row3[0].strftime("%d-%m-%Y")
                tv.insert('', 'end', values=(dt4, row3[1] , row3[2]))
            for row4 in sql5:
                dt5=row4[0].strftime("%d-%m-%Y")
                tv1.insert('', 'end', values=(dt5, row4[1] , row4[2]))
            for row5 in sql6:
                dt6=row5[0].strftime("%d-%m-%Y")
                tv.insert('', 'end', values=(dt6, row5[1] , row5[2]))

        def update_item():
            try:
                if tv.selection() and tv1.selection():
                    selected=tv.selection()
                    selected1=tv1.selection()
                    messagebox.showinfo("Info","Select One Thing")
                    tv.selection_remove(selected)
                    tv1.selection_remove(selected1)

                elif tv.selection():
                    selected = tv.selection()
                    temp = tv.item(selected, 'values')
                    date_back=datetime.strptime(temp[0],'%d-%m-%Y')
                    new_date_str=date_back.strftime('%Y-%m-%d')
                    data=new_date_str,temp[1],temp[2]
                    try:
                        mycursor.execute("select * from other where o_date=%s AND o_detail=%s AND o_amount=%s",data)
                        sql1=mycursor.fetchone()
                        if sql1!=None:
                            print(sql1)
                        else:
                            pass
                    except:
                        messagebox.showinfo("Information","This data Can't be edited")
                    try:
                        input_str=temp[1]
                        open_index=input_str.index("(")
                        close_index=input_str.index(")")
                        string1=input_str[:open_index]
                        string2=input_str[open_index+1:close_index]
                        data3=new_date_str,string1,string2,temp[2]
                        mycursor.execute("select * from purchase where p_date=%s AND p_pname=%s AND p_itemname=%s AND p_total=%s",data3)
                        sql2=mycursor.fetchone()
                        if sql2!=None:
                            print(sql2)
                        else:
                            pass
                    except:
                        messagebox.showinfo("Information","This data Can't be edited")
                    try:
                        mycursor.execute("select * from contra where c_date=%s AND c_type=%s AND c_amount=%s",data)
                        sql1=mycursor.fetchone()
                        if sql1!=None:
                            print(sql1)
                        else:
                            pass
                    except:
                        messagebox.showinfo("Information","This data Can't be edited")
                    tv.selection_remove(selected)
                elif tv1.selection():
                    
                    selected = tv1.selection()
                    temp = tv1.item(selected, 'values')
                    date_back=datetime.strptime(temp[0],'%d-%m-%Y')
                    new_date_str=date_back.strftime('%Y-%m-%d')
                    data=new_date_str,temp[1],temp[2]
                    try:
                        mycursor.execute("select * from other where o_date=%s AND o_detail=%s AND o_amount=%s",data)
                        sql1=mycursor.fetchone()
                        if sql1!=None:
                            print(sql1)
                        else:
                            pass
                    except:
                        messagebox.showinfo("Information","This data Can't be edited")
                    try:
                        input_str=temp[1]
                        open_index=input_str.index("(")
                        close_index=input_str.index(")")
                        string1=input_str[:open_index]
                        string2=input_str[open_index+1:close_index]
                        data3=new_date_str,string1,string2,temp[2]
                        mycursor.execute("select * from purchase where s_date=%s AND s_pname=%s AND s_itemname=%s AND s_total=%s",data3)
                        sql2=mycursor.fetchone()
                        if sql2!=None:
                            print(sql2)
                        else:
                            pass
                    except:
                        messagebox.showinfo("Information","This data Can't be edited")
                    try:
                        mycursor.execute("select * from contra where c_date=%s AND c_type=%s AND c_amount=%s",data)
                        sql1=mycursor.fetchone()
                        if sql1!=None:
                            print(sql1)
                        else:
                            pass
                    except:
                        messagebox.showinfo("Information","This data Can't be edited")
                    tv1.selection_remove(selected)
                else:
                    messagebox.showerror("Error","Please select the data you want to edit")
            except:
                messagebox.showerror("Error","Please select the data you want to edit")

        but9=Button(fra1,text='Edit Record',width=25,bg=bt2,activeforeground=afg,activebackground=abg,fg=fg2,font=(15),command=update_item,cursor=cur1)
        but9.place(x=25,y=550)

        but10=Button(fra1,text='Search',width=25,bg=bt2,activeforeground=afg,activebackground=abg,fg=fg2,font=(15),command=report,cursor=cur1)
        but10.place(x=25,y=600)
        # but11=Button(fra1,text='Get PDF',width=25,bg=bt2,activeforeground=afg,activebackground=abg,fg=fg2,font=(15),command=cus,cursor=cur1)
        # but11.place(x=25,y=540)
            

        data=(c_name_string,'Bank')
        data1=(c_name_string,'Credit','Bank')
        data2=(c_name_string,'Debit','Bank')
        data3=(c_name_string,'Credit into Bank')
        data4=(c_name_string,'Debit from Bank')
        mycursor.execute("SELECT p_date,p_pname,p_itemname,p_total FROM purchase where company_name=%s AND p_type=%s",data)
        sql1=mycursor.fetchall()
        mycursor.execute("SELECT s_date,s_pname,s_itemname,s_total FROM sales where company_name=%s and s_type=%s",data)
        sql2=mycursor.fetchall()
        mycursor.execute("SELECT o_date,o_detail,o_amount FROM other where company_name=%s and o_method=%s and o_type=%s",data1)
        sql3=mycursor.fetchall()
        mycursor.execute("SELECT o_date,o_detail,o_amount FROM other where company_name=%s and o_method=%s and o_type=%s",data2)
        sql4=mycursor.fetchall()
        mycursor.execute("SELECT c_date,c_type,c_amount FROM contra where company_name=%s and c_type=%s",data3)
        sql5=mycursor.fetchall()
        mycursor.execute("SELECT c_date,c_type,c_amount FROM contra where company_name=%s and c_type=%s",data4)
        sql6=mycursor.fetchall()

        books_db_str=books_db.strftime("%d-%m-%Y")

        tv1.insert(parent='', index=0, values=(books_db_str, "Starting Bank Amount", bank_db_db))
        for row in sql1:
            dt1=row[0].strftime("%d-%m-%Y")
            tv.insert('', 'end', values=(dt1, row[1]+"("+row[2]+")",row[3]))
        for row1 in sql2:
            dt2=row1[0].strftime("%d-%m-%Y")
            tv1.insert('', 'end', values=(dt2, row1[1]+"("+row1[2]+")",row1[3]))
        for row2 in sql3:
            dt3=row2[0].strftime("%d-%m-%Y")
            tv1.insert('', 'end', values=(dt3, row2[1] , row2[2]))
        for row3 in sql4:
            dt4=row3[0].strftime("%d-%m-%Y")
            tv.insert('', 'end', values=(dt4, row3[1] , row3[2]))
        for row4 in sql5:
            dt5=row4[0].strftime("%d-%m-%Y")
            tv1.insert('', 'end', values=(dt5, row4[1] , row4[2]))
        for row5 in sql6:
            dt6=row5[0].strftime("%d-%m-%Y")
            tv.insert('', 'end', values=(dt6, row5[1] , row5[2]))

        if bank_in_hand>0:
            tv.insert('', 'end', values=(cur_date, "Current Bank Balance", bank_in_hand))           
        else:
            tv1.insert('', 'end', values=(cur_date, "Current Bank Balance", abs(bank_in_hand)))


        lab_tot=Label(fra4,text=bank_sum_tot2,font=("bold",12),fg=fg1,bg="light blue")
        lab_tot.place(x=965,y=453)
        lab_tot2=Label(fra4,text=bank_sum_tot,font=("bold",12),fg=fg1,bg="light blue")
        lab_tot2.place(x=425,y=453)

        global bank_profit,bank_loss
        bank_profit=bank_sum_tot2-bank_sum_tot
        bank_loss=bank_sum_tot-bank_sum_tot2

    def profit_loss_main():
        global fra5,but9
        fra_des()
        tot()

        fra5=Frame(win3,bg=bg1,borderwidth=5,relief=SOLID,width=1072,height=500)
        fra5.place(x=0,y=210)

        laba1=Label(fra5,fg=fg1,text="Profit & Loss Ledger",font=("bold",20,"underline"),bg=bg1).place(x=455,y=2)

        date1=books_db.strftime("%d-%m-%Y")
        cash_str=str(cash_db_db)
        bank_str=str(bank_db_db)
        tot_profit=cash_profit+bank_profit
        tot_loss=cash_loss+bank_loss
        str_profit=str(tot_profit)
        str_loss=str(tot_loss)
        loss_total=0
        profit_total=0

        heading1="      Date                                 Loss Details                                    Amount"
        heading2="      Date                                 Profit Details                                  Amount"
        line1="======================================================"
        c_hand = f"   {cur_date}                        Cash in Hand                                {abs(cash_in_hand)}"
        b_hand = f"   {cur_date}                        Current Bank Balance                 {abs(bank_in_hand)}"
        ent1="    "+date1+"                       Starting Cash                                 "+cash_str
        ent2="    "+date1+"                       Starting Bank                                 "+bank_str
        ent3="                                                     Profit                                         "+str_profit
        ent4="                                                     Loss                                         "+str_loss

        listpl1=Listbox(fra5,selectmode=SINGLE,width=55,borderwidth=2,relief=SOLID,height=20,bg="light blue",fg=fg1,font=3,selectbackground="black",selectforeground="white",activestyle="none")
        listpl1.place(x=33,y=55)
        listpl2=Listbox(fra5,selectmode=SINGLE,width=55,borderwidth=2,relief=SOLID,height=20,bg="light blue",fg=fg1,font=3,selectbackground="black",selectforeground="white",activestyle="none")
        listpl2.place(x=533,y=55)

        listpl1.insert(0,heading1)
        listpl1.insert(1,line1)
        listpl1.insert(2,"")


        listpl2.insert(0,heading2)
        listpl2.insert(1,line1)
        listpl2.insert(2,"")

        # if(cash_db_db<0):
        #     listpl1.insert(3,ent1)
        #     listpl2.insert(3,"")
        # else:
        #     listpl2.insert(3,ent1)
        #     listpl1.insert(3,"")
        # if(bank_db_db<0):
        #     listpl1.insert(4,ent2)
        #     listpl2.insert(4,"")
        # else:
        #     listpl2.insert(4,ent2)
        #     listpl1.insert(4,"")

        # listpl1.insert(5,"")
        # listpl2.insert(5,"")
        listpl1.insert(6,"")
        listpl2.insert(6,"")
        if cash_in_hand>0:
            listpl1.insert(7,c_hand)
            listpl2.insert(7,"")
            loss_total=loss_total+cash_in_hand
        elif cash_in_hand<0:
            listpl2.insert(7,c_hand)
            listpl1.insert(7,"")
            profit_total=profit_total+cash_in_hand          

        if bank_in_hand>0:
            listpl1.insert(8,b_hand)
            listpl2.insert(8,"")
            loss_total=loss_total+bank_in_hand
        elif bank_in_hand<0:
            listpl2.insert(8,b_hand)
            listpl1.insert(8,"")
            profit_total=profit_total+bank_in_hand
            

        listpl1.insert(9,"")
        listpl2.insert(9,"")

        if(tot_profit>0):
            listpl2.insert(10,ent3)
            listpl1.insert(10,"")
            profit_total=profit_total+tot_profit

        if(tot_loss>0):
            listpl1.insert(10,ent4)
            listpl2.insert(10,"")
            loss_total=loss_total+tot_loss
            

        listpl1.insert(11,"")
        listpl2.insert(11,"")
        listpl1.insert(12,line1)
        listpl2.insert(12,line1)

        # listpl1.insert(13,"")
        # listpl2.insert(13,"")
        ent5=f"                                                                                                      {abs(profit_total)}"
        ent6=f"                                                                                                       {abs(loss_total)}"
        listpl1.insert(14,ent5)
        listpl2.insert(14,ent6)

        listpl1.bind("<<ListboxSelect>>",lambda event:no_selection())
        listpl2.bind("<<ListboxSelect>>",lambda event:no_selection())

        def no_selection():
            try:
                sele=listpl1.get(ANCHOR)
                if sele==heading1 or sele==line1 or sele=="":
                    listpl1.select_clear(ANCHOR)
            except:
                pass
            try:
                sele2=listpl2.get(ANCHOR)
                if sele2==heading2 or sele2==line1 or sele2=="":
                    listpl2.select_clear(ANCHOR)
            except:
                pass
         
    def Balance_sheet_main():
        global fra6,but9,rpdate1,rplab1,rpdate2,rplab2,but10,but11
        fra_des()
        tot()
        
        fra6=Frame(win3,bg=bg1,borderwidth=5,relief=SOLID,width=1072,height=500)
        fra6.place(x=0,y=210)
        rplab1=Label(fra2, fg=fg1,text="Select Starting Date:",font=15,bg=bg2)
        rplab1.place(x=800,y=76)
        rpdate1=DateEntry(fra2,selectmode='day',font=5,width=10,background='darkblue',month=4,day=1,year=2022)
        rpdate1.place(x=850,y=100)
        rplab2=Label(fra2, fg=fg1,text="Select Endind Date:",font=15,bg=bg2)
        rplab2.place(x=800,y=125)
        rpdate2=DateEntry(fra2,selectmode='day',font=5,width=10,background='darkblue')
        rpdate2.place(x=850,y=150)

        def sort_date_column(tj, col, reverse):
            data = [(datetime.strptime(tj.item(item, 'values')[col], '%d-%m-%Y'), item) for item in tj.get_children()]
            data.sort(reverse=reverse)
            for index, item in enumerate(data):
                tj.move(item[1], '', index)
        def sort_date_column2(tj1, col, reverse):
            data = [(datetime.strptime(tj1.item(item, 'values')[col], '%d-%m-%Y'), item) for item in tj1.get_children()]
            data.sort(reverse=reverse)
            for index, item in enumerate(data):
                tj1.move(item[1], '', index)

        global tj,tj1
        laba1=Label(fra6,fg=fg1,text="Balance-Sheet",font=("bold",20,"underline"),bg=bg1).place(x=455,y=2)
        tj = ttk.Treeview(fra6,columns=(1, 2, 3), show='headings', height=14,cursor=cur1)
        tj.place(x=0,y=43)
        tj.column(1,anchor=CENTER,stretch=NO,width=134)
        tj.column(2,anchor=CENTER,stretch=NO,width=260)
        tj.column(3,anchor=CENTER,stretch=NO,width=134)
        tj1 = ttk.Treeview(fra6, columns=(1, 2, 3), show='headings', height=14,cursor=cur1)
        tj1.place(x=529,y=43)
        tj1.column(1,anchor=CENTER,stretch=NO,width=134)
        tj1.column(2,anchor=CENTER,stretch=NO,width=260)
        tj1.column(3,anchor=CENTER,stretch=NO,width=134)

        tj.heading(1, text="Date" ,command=lambda: sort_date_column(tj, 0, True))
        tj.heading(2, text="Details(Debit)")
        tj.heading(3, text="Amount")
        tj1.heading(1, text="Date" ,command=lambda: sort_date_column2(tj1, 0, True))
        tj1.heading(2, text="Details(Credit)")
        tj1.heading(3, text="Amount")

        sb = Scrollbar(fra6, orient=VERTICAL)
        tj.config(yscrollcommand=sb.set)
        tj1.config(yscrollcommand=sb.set)
        sb.config(command=tj1.yview)
        sb.config(command=tj.yview)

        def report():
            for item1 in tj.get_children():
                tj.delete(item1)
            for item2 in tj1.get_children():
                tj1.delete(item2)
            
            rdate1=rpdate1.get_date()
            rdate2=rpdate2.get_date()
            data=(c_name_string,rdate1,rdate2)
            data1=(c_name_string,'Credit',rdate1,rdate2)
            data2=(c_name_string,'Debit',rdate1,rdate2)
            
            # mycursor.execute("select s_date,s_pname,s_itemname,s_total from sales where company_name=%s and s_type=%s and s_date=%s",data)
            # sql=mycursor.fetchall()
            # for i in sql:
            #     print(i)
            mycursor.execute("SELECT p_date,p_pname,p_itemname,p_total FROM purchase where company_name=%s AND p_date BETWEEN %s AND %s",data)
            sql1=mycursor.fetchall()
            mycursor.execute("SELECT s_date,s_pname,s_itemname,s_total FROM sales where company_name=%s and s_date BETWEEN %s AND %s",data)
            sql2=mycursor.fetchall()
            mycursor.execute("SELECT o_date,o_detail,o_amount FROM other where company_name=%s and o_method=%s and o_date BETWEEN %s AND %s",data1)
            sql3=mycursor.fetchall()
            mycursor.execute("SELECT o_date,o_detail,o_amount FROM other where company_name=%s and o_method=%s and o_date BETWEEN %s AND %s",data2)
            sql4=mycursor.fetchall()
            for row in sql1:
                dt1=row[0].strftime("%d-%m-%Y")
                tj.insert('', 'end', values=(dt1, row[1]+"("+row[2]+")",row[3]))
            for row1 in sql2:
                dt2=row1[0].strftime("%d-%m-%Y")
                tj1.insert('', 'end', values=(dt2, row1[1]+"("+row1[2]+")",row1[3]))
            for row2 in sql3:
                dt3=row2[0].strftime("%d-%m-%Y")
                tj1.insert('', 'end', values=(dt3, row2[1] , row2[2]))
            for row3 in sql4:
                dt4=row3[0].strftime("%d-%m-%Y")
                tj.insert('', 'end', values=(dt4, row3[1] , row3[2]))

        def update_item():
            try:
                if tj.selection() and tj1.selection():
                    selected=tj.selection()
                    selected1=tj1.selection()
                    messagebox.showinfo("Info","Select One Thing")
                    tj.selection_remove(selected)
                    tj1.selection_remove(selected1)

                elif tj.selection():
                    selected = tj.selection()
                    temp = tj.item(selected, 'values')
                    date_back=datetime.strptime(temp[0],'%d-%m-%Y')
                    new_date_str=date_back.strftime('%Y-%m-%d')
                    data=new_date_str,temp[1],temp[2]
                    try:
                        mycursor.execute("select * from other where o_date=%s AND o_detail=%s AND o_amount=%s",data)
                        sql1=mycursor.fetchone()
                        if sql1!=None:
                            print(sql1)
                        else:
                            pass
                    except:
                        pass
                    try:
                        input_str=temp[1]
                        open_index=input_str.index("(")
                        close_index=input_str.index(")")
                        string1=input_str[:open_index]
                        string2=input_str[open_index+1:close_index]
                        data3=new_date_str,string1,string2,temp[2]
                        mycursor.execute("select * from purchase where p_date=%s AND p_pname=%s AND p_itemname=%s AND p_total=%s",data3)
                        sql2=mycursor.fetchone()
                        if sql2!=None:
                            print(sql2)
                        else:
                            pass
                    except:
                        pass
                    try:
                        mycursor.execute("select * from contra where c_date=%s AND c_type=%s AND c_amount=%s",data)
                        sql1=mycursor.fetchone()
                        if sql1!=None:
                            print(sql1)
                        else:
                            pass
                    except:
                        pass

                    tj.selection_remove(selected)
                elif tj1.selection():
                    
                    selected = tj1.selection()
                    temp = tj1.item(selected, 'values')
                    date_back=datetime.strptime(temp[0],'%d-%m-%Y')
                    new_date_str=date_back.strftime('%Y-%m-%d')
                    data=new_date_str,temp[1],temp[2]
                    try:
                        mycursor.execute("select * from other where o_date=%s AND o_detail=%s AND o_amount=%s",data)
                        sql1=mycursor.fetchone()
                        if sql1!=None:
                            print(sql1)
                        else:
                            pass
                    except:
                        pass
                    try:
                        input_str=temp[1]
                        open_index=input_str.index("(")
                        close_index=input_str.index(")")
                        string1=input_str[:open_index]
                        string2=input_str[open_index+1:close_index]
                        data3=new_date_str,string1,string2,temp[2]
                        mycursor.execute("select * from purchase where s_date=%s AND s_pname=%s AND s_itemname=%s AND s_total=%s",data3)
                        sql2=mycursor.fetchone()
                        if sql2!=None:
                            print(sql2)
                        else:
                            pass
                    except:
                        pass
                    try:
                        mycursor.execute("select * from contra where c_date=%s AND c_type=%s AND c_amount=%s",data)
                        sql1=mycursor.fetchone()
                        if sql1!=None:
                            print(sql1)
                        else:
                            pass
                    except:
                        pass
                    tj1.selection_remove(selected)
                else:
                    messagebox.showerror("Error","Please select the data you want to edit")
            except:
                messagebox.showerror("Error","Please select the data you want to edit")

        but9=Button(fra1,text='Edit Record',width=25,bg=bt2,activeforeground=afg,activebackground=abg,fg=fg2,font=(15),command=update_item,cursor=cur1)
        but9.place(x=25,y=550)

        data=(c_name_string,)
        data1=(c_name_string,'Credit')
        data2=(c_name_string,'Debit')

        mycursor.execute("SELECT p_date,p_pname,p_itemname,p_total FROM purchase where company_name=%s",data)
        sql1=mycursor.fetchall()
        mycursor.execute("SELECT s_date,s_pname,s_itemname,s_total FROM sales where company_name=%s",data)
        sql2=mycursor.fetchall()
        mycursor.execute("SELECT o_date,o_detail,o_amount FROM other where company_name=%s and o_method=%s",data1)
        sql3=mycursor.fetchall()
        mycursor.execute("SELECT o_date,o_detail,o_amount FROM other where company_name=%s and o_method=%s",data2)
        sql4=mycursor.fetchall()

        books_db_str=books_db.strftime("%d-%m-%Y")
        tj1.insert(parent='', index=0, values=(books_db_str, "Starting Bank Amount", bank_db_db))
        books_db_str=books_db.strftime("%d-%m-%Y")
        tj1.insert(parent='', index=0, values=(books_db_str, "Starting Cash Amount", cash_db_db))
        for row in sql1:
            dt1=row[0].strftime("%d-%m-%Y")
            tj.insert('', 'end', values=(dt1, row[1]+"("+row[2]+")",row[3]))
        for row1 in sql2:
            dt2=row1[0].strftime("%d-%m-%Y")
            tj1.insert('', 'end', values=(dt2, row1[1]+"("+row1[2]+")",row1[3]))
        for row2 in sql3:
            dt3=row2[0].strftime("%d-%m-%Y")
            tj1.insert('', 'end', values=(dt3, row2[1] , row2[2]))
        for row3 in sql4:
            dt4=row3[0].strftime("%d-%m-%Y")
            tj.insert('', 'end', values=(dt4, row3[1] , row3[2]))
        if bal_hand>0:
            tj.insert('', 'end', values=(cur_date, "Total Profit", bal_hand))           
        else:
            tj1.insert('', 'end', values=(cur_date, "Total Loss", abs(bal_hand)))

        but10=Button(fra1,text='Search',width=25,bg=bt2,activeforeground=afg,activebackground=abg,fg=fg2,font=(15),command=report,cursor=cur1)
        but10.place(x=25,y=600)
        # but11=Button(fra1,text='Get PDF',width=25,bg=bt2,activeforeground=afg,activebackground=abg,fg=fg2,font=(15),command=cus,cursor=cur1)
        # but11.place(x=25,y=540)


        lab_tot=Label(fra6,text=journal_tot2,font=("bold",12),fg=fg1,bg="light blue")
        lab_tot.place(x=965,y=453)
        lab_tot2=Label(fra6,text=journal_tot,font=("bold",12),fg=fg1,bg="light blue")
        lab_tot2.place(x=425,y=453)

    def qut():
        try:
            try:
                vc1.destroy()
            except:
                pass
            try:
                vc2.destroy()
            except:
                pass
            try:
                vc3.destroy()
            except:
                pass
            try:
                vc4.destroy()
            except:
                pass
            try:
                qus=messagebox.askyesno("Alert","Are you want to Exit?")
                if(qus==YES):
                    win3.destroy()
            except:
                pass
        except:
            pass
    
    win3.bind("<Escape>",lambda event:qut())
    win3.bind("<Control-Alt-c>",lambda event:contra())
    win3.bind("<Control-Alt-C>",lambda event:contra())
    win3.bind("<Control-s>",lambda event:sales())
    win3.bind("<Control-S>",lambda event:sales())
    win3.bind("<Control-p>",lambda event:purchase())
    win3.bind("<Control-p>",lambda event:purchase())
    win3.bind("<Control-o>",lambda event:other())
    win3.bind("<Control-O>",lambda event:other())
    win3.bind("<Alt-c>",lambda event:cash_main())
    win3.bind("<Alt-C>",lambda event:cash_main())
    win3.bind("<Alt-b>",lambda event:bank_main())
    win3.bind("<Alt-B>",lambda event:bank_main())
    win3.bind("<Alt-p>",lambda event:profit_loss_main())
    win3.bind("<Alt-P>",lambda event:profit_loss_main())
    win3.bind("<Control-Alt-b>",lambda event:Balance_sheet_main())
    win3.bind("<Control-Alt-B>",lambda event:Balance_sheet_main())
    win3.bind("<Control-Alt-l>",lambda event:win_main())
    win3.bind("<Control-Alt-L>",lambda event:win_main())
    # win3.bind("<Control-Alt-p>",lambda event:cus())
    # win3.bind("<Control-Alt-P>",lambda event:cus())


    lab1=Label(fra2, fg=fg1,text="Company Name:",font=15,bg=bg2).place(x=100,y=25)
    lab2=Label(fra2, fg=fg1,text="Gst Number:",font=15,bg=bg2).place(x=100,y=76)
    lab3=Label(fra2, fg=fg1,text="Mobile Number:",font=15,bg=bg2).place(x=100,y=125)
    lab4=Label(fra2, fg=fg1,text=company_name_db,font=("Bodoni MT",15),bg=lbg1).place(x=250,y=25)
    lab5=Label(fra2, fg=fg1,text=gstin_gst_db,font=("Bodoni MT",15),bg=lbg1).place(x=225,y=76)
    lab6=Label(fra2, fg=fg1,text=mobile_db,font=("Bodoni MT",15),bg=lbg1).place(x=250,y=125)
    lab7=Label(fra2, fg=fg1,text="Year:",font=15,bg=bg2).place(x=800,y=25)
    lab8=Label(fra2, fg=fg1,text=financial_year_db,font=("Bodoni MT",12),bg=lbg1).place(x=840,y=25)
    can=Canvas(fra1,bg=bg2,width=290,height=700)
    can.pack()
    can.create_line(10,245,280,245,width=2)
    can.create_line(10,455,280,455,width=3)
    lab9=Label(fra1,fg=fg1,text="Vouchers",bg=bg2,width=20,font=("bold",15)).place(x=25,y=15)
    but1=Button(fra1,fg=fg2,text="Contra",bg=bt1,cursor=cur1,activeforeground=afg,activebackground=abg,width=25,font=15,command=contra).place(x=25,y=60)
    but2=Button(fra1,fg=fg2,text="Sales",bg=bt1,cursor=cur1,activeforeground=afg,activebackground=abg,width=25,font=15,command=sales).place(x=25,y=100)
    but3=Button(fra1,fg=fg2,text="Purchase",bg=bt1,cursor=cur1,activeforeground=afg,activebackground=abg,width=25,font=15,command=purchase).place(x=25,y=140)
    but4=Button(fra1,fg=fg2,text="Other",bg=bt1,cursor=cur1,activeforeground=afg,activebackground=abg,width=25,font=15,command=other).place(x=25,y=180)

    lab10=Label(fra1,fg=fg1,text="Ledger",bg=bg2,width=20,font=("bold",15)).place(x=25,y=270)
    but5=Button(fra1,fg=fg2,text="Cash Ledger",bg=bt1,cursor=cur1,activeforeground=afg,activebackground=abg,width=25,font=15,command=lambda:{cash_main()}).place(x=25,y=310)
    but6=Button(fra1,fg=fg2,text="Bank Ledger",bg=bt1,cursor=cur1,activeforeground=afg,activebackground=abg,width=25,font=15,command=lambda:{bank_main()}).place(x=25,y=350)
    but7=Button(fra1,fg=fg2,text="Profit And Loss Ledger",bg=bt1,cursor=cur1,activeforeground=afg,activebackground=abg,width=25,font=15,command=lambda:{profit_loss_main()}).place(x=25,y=390)
    but8=Button(fra1,fg=fg2,text="Balance-Sheet",bg=bt1,cursor=cur1,activeforeground=afg,activebackground=abg,width=25,font=15,command=lambda:{Balance_sheet_main()}).place(x=25,y=480)
    but12=Button(fra1,text='Logout',width=25,bg=bt2,activeforeground=afg,activebackground=abg,fg=fg2,font=(15),command=lambda:{win_main()},cursor=cur1)
    but12.place(x=25,y=640)
    win3.mainloop()

c_name=("Tirthlimited",)
c_name_string="Tirthlimited"

win_main()
# main2()
