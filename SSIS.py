import csv
import tkinter as tk
import pandas as pd
from tkinter import ttk
import customtkinter 
from tkinter import messagebox


class EditCourseWindow:
    def __init__(self, main_window, main_window_class, course_code, course_desc):
        process = Processing
        self.course_data = process.read_csv("Courses.csv")
        self.main_window = main_window
        self.main_window_class = main_window_class
        self.course_code = course_code
        self.course_desc = course_desc
        self.window = tk.Toplevel(self.main_window)
        self.window.title("Edit Course")
        self.window.geometry("730x75") 
        

        self.code_str = tk.StringVar(value = course_code)
        self.desc_str = tk.StringVar(value = course_desc)

        self.code_label = tk.Label(self.window, text="Course Code:",padx=1, pady=1).grid(row=0,column=0)
        self.code_entry = tk.Entry(self.window, textvariable=self.code_str,width=20)
        self.code_entry.bind("<KeyRelease>", self.allow_edit_button)

        self.desc_label = tk.Label(self.window, text="Course Description:", padx=5, pady=1).grid(row=1, column=0)
        self.desc_entry = tk.Entry(self.window,textvariable=self.desc_str, width=100)
        self.desc_entry.bind("<KeyRelease>", self.allow_edit_button)

        self.edit_course_button = tk.Button(self.window, text="Edit Course", command=self.edit_course)

        self.code_entry.grid(row=0, column=1, padx=1, pady=1,sticky='w')
        self.desc_entry.grid(row=1, column=1, padx=1, pady=1)
        self.edit_course_button.grid(row=3, column=1, padx=1, pady=1, sticky='w')

    def edit_course(self):
        process = Processing
        rem_courses =[]
        self.edited_course = [self.code_entry.get(), self.desc_entry.get()]
        self.course_data = process.read_csv("Courses.csv")
        self.student_data = process.read_csv("Students.csv")
        course_num_rows = len(self.course_data)
        student_num_rows = len(self.student_data)

        for i in range(course_num_rows):
                if self.course_data[i][0]==self.edited_course[0]:
                    rem_courses = [row for row in self.course_data if row != self.course_data[i]]
        
        if self.desc_entry.get().upper() in [rem_courses[row][1] for row in range(1,len(rem_courses))] or self.code_entry.get() in [rem_courses[row][0] for row in range(1,len(rem_courses))]: 
                messagebox.showerror(title="Course Duplicate", message="Course already exists")
                self.window.lift()
        else:   
            if self.desc_entry.get() == self.course_desc and self.code_entry.get() ==  self.course_code:
                messagebox.showerror(title="Course Duplicate", message="No Changes has been made")
                self.window.lift()
            else:
                self.edit(course_num_rows, student_num_rows)

        
    
    def edit(self, course_num_rows, student_num_rows):
        result = messagebox.askquestion(title="Exit Edit Course", message="Is the edit final")
        if result == 'yes':
            process = Processing
            messagebox.showinfo(title="Action Successful", message="Course Edit is successful")
            for i in range(student_num_rows):
                    if self.student_data[i][5] == self.course_code:
                        self.student_data[i][5] = self.edited_course[0]
                        with open("Students.csv", 'w', newline='') as edit:
                            writer = csv.writer(edit)
                            writer.writerows(self.student_data)
            process.show_students(self.student_data)
            for i in range(course_num_rows):
                if self.course_data[i][0] == self.course_code:
                    self.course_data[i] = self.edited_course
                    with open('Courses.csv', 'w', newline='') as edit:
                        writer = csv.writer(edit)
                        writer.writerows(self.course_data)
            update = process.read_csv("Courses.csv")            
            self.main_window_class.set_desc_combo([update[row][1]+" ("+update[row][0]+")" for row in range(1,len(self.course_data))])
            self.window.destroy()
        else:
            self.window.lift()
    def allow_edit_button(self, event):
        self.code_str.set(self.code_entry.get().upper())
        self.desc_str.set(self.desc_entry.get().upper())
        self.edited_course = [self.code_entry.get(), self.desc_entry.get()]
        if self.edited_course[0] == "" or self.edited_course[1] == "":
            self.edit_course_button['state'] = "disabled"
        else:
            self.edit_course_button['state'] = "normal"
        
        
    
class AddCourseWindow:
    def __init__(self, main_window, main_window_class):
        process = Processing
        self.course_data = process.read_csv("Courses.csv")
        self.main_window = main_window
        self.main_window_class = main_window_class
        self.window = tk.Toplevel(self.main_window)
        self.window.title("Add Course")
        self.window.geometry("730x75")

        self.code_label = tk.Label(self.window, text="Course Code:", padx=1, pady=1).grid(row=0,column=0)
        self.code_entry = tk.Entry(self.window, width=20)
        self.code_entry.bind("<KeyRelease>", self.allow_add_button)

        self.desc_label = tk.Label(self.window, text="Course Description:", padx=1, pady=1).grid(row=1, column=0)
        self.desc_entry = tk.Entry(self.window, width=100)
        self.desc_entry.bind("<KeyRelease>", self.allow_add_button)

        self.add_course_button = tk.Button(self.window, text="Add Course", state=["disabled"],command=self.add_course)
        

        self.code_entry.grid(row=0, column=1, padx=1, pady=1,sticky='w')
        self.desc_entry.grid(row=1, column=1, padx=1, pady=1)
        self.add_course_button.grid(row=3, column=1, padx=1, pady=1, sticky='w')

    def add_course(self):
        process = Processing
        self.course_data = process.read_csv("Courses.csv")
        course_rows = len(self.course_data)
        self.added_course = [self.code_entry.get(), self.desc_entry.get()]
        
        if self.added_course[0] != "" and self.added_course[1] != "" and self.added_course[0] not in [self.course_data[row][0] for row in range(1,course_rows)] and self.added_course[1] not in [self.course_data[row][1] for row in range(1,course_rows)]:
            result = messagebox.askquestion(title="Exit Add Course", message="Is the Added Course final")
            if result == "yes":
                messagebox.showinfo(title="Action Succesful", message="Course Added succesfully")
                with open("Courses.csv", "a", newline="") as courses_file:
                    writer = csv.writer(courses_file)
                    writer.writerow(self.added_course)
                update = process.read_csv("Courses.csv")
                update_len = len(update)
                self.main_window_class.set_desc_combo([update[row][1]+" ("+update[row][0]+")" for row in range(1,update_len)])
                self.window.destroy()
            else:
                self.window.lift()
        else:
            messagebox.showerror(title="Course Duplicate", message="Course already exists")

    def allow_add_button(self, event):
        self.added_course = [self.code_entry.get(), self.desc_entry.get()]
        if self.added_course[0] != "" and self.added_course[1] != "" :
            self.add_course_button['state'] = "normal"
        else:
            self.add_course_button['state'] = "disabled"
        
class AddStudentWindow:
    def __init__(self, main_window, main_window_class):
        process = Processing
        self.stud_data = process.read_csv("Students.csv")
        self.course_data = process.read_csv("Courses.csv")
        year_range = ['1', '2', '3', '4']
        
        self.main_window = main_window
        self.main_window_class = main_window_class
        self.window = tk.Toplevel(self.main_window)
        self.window.title("Add Student")
        self.window.geometry("300x160")
        self.window.resizable(False, False)
        self.label_frame = tk.Frame(self.window)
        self.entry_frame = tk.Frame(self.window)

        self.entry_dict = {}
        self.entry_list = ["ID Number:", "Name:", "Year Level:", "Gender:"]
        for value in self.entry_list:
            if value == "ID Number:":
                valid_entry = self.window.register(process.valid_id_entry)
                self.label = tk.Label(self.label_frame, text=value, width=10)
                self.label.grid(row=self.entry_list.index(value),column=0, sticky="n")
                self.entry = tk.Entry(self.entry_frame, validate="key", validatecommand=(valid_entry, '%P'), width=30)
                self.entry.grid(row=self.entry_list.index(value), column=1)
                self.entry_dict[value] = self.entry
                self.entry.bind("<KeyRelease>", self.allow_add_button)
            elif value == "Year Level:":
                self.label = tk.Label(self.label_frame, text=value, width=10)
                self.label.grid(row=self.entry_list.index(value),column=0, sticky="n")
                self.year_combo = ttk.Combobox(self.entry_frame, width=27, values=year_range, state="readonly")
                self.year_combo.grid(row=self.entry_list.index(value),column=1)
                self.year_combo.bind("<<ComboboxSelected>>", self.allow_add_button)
                self.entry_dict[value] = self.year_combo
            else:
                self.label = tk.Label(self.label_frame, text=value, width=10)
                self.label.grid(row=self.entry_list.index(value),column=0, sticky="n")
                self.entry = tk.Entry(self.entry_frame, width=30)
                self.entry.grid(row=self.entry_list.index(value),column=1)
                self.entry.bind("<KeyRelease>", self.allow_add_button)
                self.entry_dict[value] = self.entry

        self.enrollment_status_var = tk.StringVar(value="Not Enrolled")
        self.enroll_label = tk.Label(self.label_frame, text="Enrollment Status:")
        self.enroll_label.grid(row=4, column=0)
        self.enroll_combo = ttk.Combobox(self.entry_frame, textvariable=self.enrollment_status_var, 
                                        values=["Enrolled", "Not Enrolled"], state="readonly", width=27)
        self.enroll_combo.grid(row=4, column=1)
        self.enroll_combo.bind("<<ComboboxSelected>>", self.allow_course_combo)
        
        self.combo_var = tk.StringVar(value="")
        self.courses_label = tk.Label(self.label_frame, text="Course:", width=10)
        self.courses_label.grid(row=5,column=0)
        self.courses_combo = ttk.Combobox(self.entry_frame, width=27, textvariable=self.combo_var, values=[], state="disabled")
        self.set_code_combo([self.course_data[row][0] for row in range(1,len(self.course_data))])
        self.courses_combo.grid(row=5, column=1)
        self.courses_combo.bind("<<ComboboxSelected>>", self.allow_add_button)
        
        self.add_button = tk.Button(self.window, text="Add Student", command=self.add_student, state="disabled")

        self.add_button.grid(row=1, column=1)
        self.label_frame.grid(row=0, column=0)
        self.entry_frame.grid(row=0, column=1)
        
    def get_window(self):
        return self.window
    
    def add_student(self):
        process = Processing
        self.stud_data = process.read_csv("Students.csv")
        students_id = [self.stud_data[row][0]
                        for row in range(1,len(self.stud_data))]
        students_name = [self.stud_data[row][1]
                        for row in range(1,len(self.stud_data))]
        self.courses_var = self.courses_combo.get()
        self.enrollment_status_var = self.enroll_combo.get()
        self.new_student = [self.entry_dict["ID Number:"].get(), 
                            self.entry_dict["Name:"].get(), 
                            self.entry_dict["Year Level:"].get(), 
                            self.entry_dict["Gender:"].get(), 
                            self.enrollment_status_var, self.courses_var]
        
        if self.entry_dict["ID Number:"].get() in students_id or self.entry_dict["Name:"].get() in students_name:
            messagebox.showerror(title='ID Error',message="Student already exists")
        else:
            result  = messagebox.askquestion(title="Exit Add Student",message="Is your Added Student final")
            if result == "yes":
                messagebox.showinfo(title="Action Successful", message="Student Added succesfully")
                with open("Students.csv", "a", newline="") as students_file:
                    writer = csv.writer(students_file)
                    writer.writerow(self.new_student)

                update = process.read_csv("Students.csv")
                update_len = len(update)
                self.main_window_class.set_id_combo([update[row][1] + " ("+update[row][0]+")" for row in range(1,update_len)])
                process.show_students(update)
                self.window.destroy()
            else:
                self.window.lift()

    def allow_add_button(self, event):
        self.id_str = self.entry_dict["ID Number:"].get()
        id_to_int = self.id_str[0:3] + self.id_str[5:8]
        allow = False
        try:
            id_int = int(id_to_int)
            allow = True 
            pass
        except(ValueError):
            self.add_button["state"] = "disabled"
        

        if all(entry.get() for entry in self.entry_dict.values()) and allow == True:
            if len(self.entry_dict["ID Number:"].get())==9:
                if self.id_str[4] == "-":
                    self.add_button["state"] = "normal"
                else:
                    self.add_button["state"] = "disabled"
            else:
                self.add_button["state"] = "disabled"
        else:
            self.add_button["state"] = "disabled"

    def allow_course_combo(self, event):
        picked = self.enroll_combo.get()
        if picked == "Enrolled" and self.courses_combo.get() == "":
            self.courses_combo["state"] = "readonly"
            self.add_button["state"] = "disabled"
        else:
            self.courses_combo.set("")
            self.courses_combo["state"] = "disabled"
            self.add_button["state"] = "normal"

    def set_code_combo(self, val):
        self.courses_combo['values'] = val

class EditStudentWindow:
    def __init__(self, main_window, main_window_class, id, name, year, gender, enroll, course):
        process = Processing
        self.course_data = process.read_csv("Courses.csv")
        year_range = ['1', '2', '3', '4']
        self.main_window = main_window
        self.window = tk.Toplevel(self.main_window)
        self.label_frame = tk.Frame(self.window)
        self.entry_frame = tk.Frame(self.window)
        self.window.title("Edit Student")
        self.window.geometry("300x160")
        self.window.resizable(False, False)

        self.main_window_class = main_window_class
        self.id_str = tk.StringVar(self.window, value=id)
        self.name_str = tk.StringVar(self.window, value=name)
        self.year_str = tk.StringVar(self.window, value=year)
        self.gender_str = tk.StringVar(self.window, value=gender)
        self.enroll_str = tk.StringVar(self.window, value=enroll)
        self.course_str = tk.StringVar(self.window, value=course)
        self.entry_dict ={}
        self.entry_list = ["ID Number:", "Name:", "Year Level:", "Gender:"]
        self.entry_val = [self.id_str, self.name_str, self.year_str, self.gender_str]
        
        for value in self.entry_list:
            if value == "ID Number:":
                valid_entry = self.window.register(process.valid_id_entry)
                self.label = tk.Label(self.label_frame, text=value, width=10)
                self.label.grid(row=self.entry_list.index(value),column=0, sticky="n")
                self.entry = tk.Entry(self.entry_frame, textvariable=self.entry_val[self.entry_list.index(value)], validate="key", validatecommand=(valid_entry, '%P'), state="disabled", width=30)
                self.entry.grid(row=self.entry_list.index(value), column=1)
                self.entry_dict[value] = self.entry
                self.entry.bind("<KeyRelease>", self.allow_edit_button)
            elif value == "Year Level:":
                self.label = tk.Label(self.label_frame, text=value, width=10)
                self.label.grid(row=self.entry_list.index(value),column=0, sticky="n")
                self.year_combo = ttk.Combobox(self.entry_frame, textvariable=self.entry_val[self.entry_list.index(value)],width=27, values=year_range, state="readonly")
                self.year_combo.grid(row=self.entry_list.index(value),column=1)
                self.year_combo.bind("<<ComboboxSelected>>", self.allow_edit_button)
                self.entry_dict[value] = self.year_combo
            else:
                self.label = tk.Label(self.label_frame, text=value, width=10)
                self.label.grid(row=self.entry_list.index(value),column=0, sticky="n")
                self.entry = tk.Entry(self.entry_frame, textvariable=self.entry_val[self.entry_list.index(value)],width=30)
                self.entry.grid(row=self.entry_list.index(value),column=1)
                self.entry.bind("<KeyRelease>", self.allow_edit_button)
                self.entry_dict[value] = self.entry

        
        self.enroll_label = tk.Label(self.label_frame, text="Enrollment Status:")
        self.enroll_label.grid(row=5, column=0)
        self.enroll_combo = ttk.Combobox(self.entry_frame, textvariable=self.enroll_str,
                                        values=["Enrolled", "Not Enrolled"], state="readonly", width=27)
        self.enroll_combo.grid(row=5, column=1)
        self.enroll_combo.bind("<<ComboboxSelected>>", self.allow_course_combo)

        self.courses_label = tk.Label(self.label_frame, text="Course:", width=10)
        self.courses_label.grid(row=6,column=0)
        self.courses_combo = ttk.Combobox(self.entry_frame, width=27, textvariable=self.course_str, values=[])
        self.set_code_combo([self.course_data[row][0] for row in range(1,len(self.course_data))])
        self.courses_combo.grid(row=6,column=1)
        self.courses_combo.bind("<<ComboboxSelected>>", self.allow_edit_button)
        if enroll != "Enrolled":
            self.courses_combo.set("")
            self.courses_combo["state"] = "disabled"
        else:
            self.courses_combo["state"] = "readonly"

        self.edit_button = tk.Button(self.window, text="Edit", command=self.edit_student)
        
        self.label_frame.grid(row=0, column=0)
        self.entry_frame.grid(row=0, column=1)
        self.edit_button.grid(row=5, column=1)
    
    def get_window(self):
        return self.window
    
    def edit_student(self):
        process = Processing
        main = MainWindow
        self.courses_var = self.courses_combo.get()
        self.enrollment_status_var = self.enroll_combo.get()
        self.rows = process.read_csv("Students.csv")
        num_rows = len(self.rows)
        self.new_info = [self.entry_dict["ID Number:"].get(), 
                        self.entry_dict["Name:"].get(), 
                        self.entry_dict["Year Level:"].get(), 
                        self.entry_dict["Gender:"].get(), 
                        self.enrollment_status_var, self.courses_var]
        
        result = messagebox.askquestion(title="Exit Edit Student", message="Is the Edit final")
        if result == "yes":
            for i in range(num_rows):
                if self.rows[i][0] == self.entry_dict["ID Number:"].get():
                    self.rows[i] = self.new_info

                with open('Students.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(self.rows)
            messagebox.showinfo(title="Action Succesful", message="Edit Successful")
            self.stud_data = process.read_csv("Students.csv")
            self.main_window_class.set_id_combo([self.stud_data[row][1] + " ("+self.stud_data[row][0]+")" for row in range(1,len(self.stud_data))])
            process.show_students(self.rows)
            self.window.destroy()
        else:
            self.window.lift()

    def allow_edit_button(self, event):
        process = Processing
        self.stud_data = process.read_csv("Students.csv")
        if all(entry.get() for entry in self.entry_dict.values()):
            self.edit_button["state"] = "normal"
        else:
            self.edit_button["state"] = "disabled"  

    def allow_course_combo(self, event):
        picked = self.enroll_combo.get()
        if picked == "Enrolled" and self.courses_combo.get() == "":
            self.courses_combo["state"] = "readonly"
            self.edit_button["state"] = "disabled"
        else:
            self.courses_combo.set("")
            self.courses_combo["state"] = "disabled"
            self.edit_button["state"] = "normal"

    def set_code_combo(self, val):
        self.courses_combo['values'] = val

class MainWindow:
    def __init__(self, window):
        self.add_stud = AddStudentWindow
        self.edit_stud = EditStudentWindow
        process = Processing
        self.window = window
        self.stud_data = process.read_csv("Students.csv")
        self.course_data = process.read_csv("Courses.csv")
        self.desc_var = tk.StringVar()
        self.id_var = tk.StringVar()
        self.top_frame = tk.Frame(window, padx=5)
        self.course_frame = tk.Frame(self.top_frame, pady=5)
        self.student_frame = tk.Frame(self.top_frame, pady=5)
        self.desc_label = tk.Label(self.course_frame, text="Course Description (Course Code):")
        self.desc_list = ttk.Combobox(self.course_frame, textvariable=self.desc_var,values=[], width=110, justify="center")
        self.set_desc_combo([self.course_data[row][1]+" ("+self.course_data[row][0]+")" for row in range(1,len(self.course_data))])
        self.desc_list.bind("<KeyRelease>", self.desc_search)
        self.add_course = tk.Button(self.course_frame, text="Add Course",command=self.open_add_course_window, height=1, padx=5, pady=5)
        self.edit_course = tk.Button(self.course_frame, text="Edit Course",command=self.open_edit_course_window,height=1, padx=5, pady=5)
        self.del_course = tk.Button(self.course_frame, text="Delete Course",command=self.delete_course,height=1, padx=5, pady=5)
        self.separation = tk.Label(self.top_frame, text="|", height=2, padx=5, pady=5)
        self.stud_label = tk.Label(self.student_frame, text="Name (ID Number):")
        self.stud_list = ttk.Combobox(self.student_frame, textvariable=self.id_var,values=[], width=40, justify="center")
        self.set_id_combo([self.stud_data[row][1] + " ("+self.stud_data[row][0]+")" for row in range(1,len(self.stud_data))])
        self.stud_list.bind("<KeyRelease>", self.student_search)
        self.add_stud = tk.Button(self.student_frame, text="Add Student",command=self.open_add_student_window,height=1, padx=5, pady=5)
        self.edit_stud = tk.Button(self.student_frame, text="Edit Student", command=self.open_edit_student_window, height=1, padx=5, pady=5)
        self.del_stud = tk.Button(self.student_frame, text= "Delete Student",command=self.delete_student,height=1, padx=5, pady=5)

        process.show_students(self.stud_data)
        
        self.top_frame.grid(row=0,column=1, padx=10, pady=10)
        self.course_frame.grid(row=0, column=0)
        self.student_frame.grid(row=0, column=2)
        self.desc_label.grid(row=0, column=1)
        self.desc_list.grid(row=1, column=0, columnspan=3)
        self.add_course.grid(row=2,column=0, pady=5)
        self.edit_course.grid(row=2, column=1, pady=5)
        self.del_course.grid(row=2,column=2, pady=5)
        self.separation.grid(row=0, column=1, rowspan=2)

        self.stud_label.grid(row=0, column=1)
        self.stud_list.grid(row=1, column=0, columnspan=3)
        self.add_stud.grid(row=2, column=0, padx=5, pady=5)
        self.edit_stud.grid(row=2, column=1, padx=5, pady=5)
        self.del_stud.grid(row=2, column=2, padx=5, pady=5)
    
    def set_id_combo(self, val):
        self.stud_list['values'] = val
        self.stud_list.set("")

    def set_desc_combo(self, val):
        self.desc_list['values'] = val
        self.desc_list.set("")

    def desc_search(self,event):
        value = event.widget.get()
        if value == '':
            self.desc_list['values'] = [self.course_data[row][1]+" ("+self.course_data[row][0]+")" for row in range(1,len(self.course_data))]
        else:
            items = []
            for data in [self.course_data[row][1]+" ("+self.course_data[row][0]+")" for row in range(1,len(self.course_data))]:
                if value.upper() in data:
                    items.append(data)
            self.desc_list['values'] = items

    def student_search(self, event):
        value = event.widget.get()
        if value == "":
            self.stud_list['values'] = [self.stud_data[row][1] + " ("+self.stud_data[row][0]+")" for row in range(1,len(self.stud_data))]
        else:
            items = []
            for data in [self.stud_data[row][1] + " ("+self.stud_data[row][0]+")" for row in range(1,len(self.stud_data))]:
                if value.lower() in data.lower():
                    items.append(data)
            self.stud_list['values'] = items


    def open_edit_student_window(self):
        process = Processing
        self.stud_data = process.read_csv("Students.csv")
        num_rows = len(self.stud_data)
        if self.stud_list.get()== "":
            messagebox.showerror(title='Button Error', message="No Student picked!")
        elif self.stud_list.get() not in [self.stud_data[row][1] + " ("+self.stud_data[row][0]+")" for row in range(1,len(self.stud_data))]:
            messagebox.showerror(title='Button Error', message="No existing Student picked!")
        else:
            self.get_id = self.stud_list.get().split(' (')
            self.specific_id = self.get_id[1].split(')')
            for i in range(num_rows):
                if self.stud_data[i][0]==self.specific_id[0]:
                    edit_student_window = EditStudentWindow(self.window, self, self.specific_id[0], self.stud_data[i][1], 
                                                            self.stud_data[i][2], self.stud_data[i][3], self.stud_data[i][4], self.stud_data[i][5])

    def open_add_student_window(self):
        add_student_window = AddStudentWindow(self.window,self)
    
    def delete_student(self):
        process = Processing
        self.stud_data = process.read_csv("Students.csv")
        if self.stud_list.get() == "":
            messagebox.showerror(title='Button Error', message="No Student picked!")
        elif self.stud_list.get() not in [self.stud_data[row][1] + " ("+self.stud_data[row][0]+")" for row in range(1,len(self.stud_data))]:
            messagebox.showerror(title='Button Error', message="No existing Student picked!")
        else:
            self.get_id = self.stud_list.get().split(' (')
            self.specific_id = self.get_id[1].split(')')
            with open('Students.csv', 'r') as read_file:
                reader = csv.reader(read_file)
                rows = [row for row in reader]
                num_rows = len(rows)
            for i in range(num_rows):
                if rows[i][0]==self.specific_id[0]:
                    rem_row = [row for row in rows if row != rows[i]]
                    with open('Students.csv', 'w', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerows(rem_row)
            messagebox.showinfo(title="Action Successful", message="Student successfully deleted")
            self.stud_list['textvariable'] = tk.StringVar(value="")
            self.stud_data = process.read_csv("Students.csv")
            self.set_id_combo([self.stud_data[row][1] + " ("+self.stud_data[row][0]+")" for row in range(1,len(self.stud_data))])
            process.show_students(rem_row)

    def open_add_course_window(self):
        add_course_window = AddCourseWindow(self.window, self)

    def open_edit_course_window(self):
        process = Processing
        self.course_data = process.read_csv("Courses.csv")
        if self.desc_list.get() == "":
            messagebox.showerror(title='Button Error', message="No Course picked!")
        elif self.desc_list.get() not in [self.course_data[row][1]+" ("+self.course_data[row][0]+")" for row in range(1,len(self.course_data))]:
            messagebox.showerror(title='Button Error', message="No existing Course picked!")
        else:
            self.get_course = self.desc_list.get().split(' (')
            self.specific_course = self.get_course[0]
            num_rows = len(self.course_data)
            for i in range(num_rows):
                if self.course_data[i][1] == self.specific_course:
                    edit_course_window = EditCourseWindow(self.window, self, self.course_data[i][0], self.course_data[i][1])

    def delete_course(self):
        process = Processing
        self.course_data = process.read_csv("Courses.csv")
        student_num_rows = len(self.stud_data)
        enroll_stat = ["Not Enrolled", ""]
        if self.desc_list.get()== "":
            messagebox.showerror(title='Button Error', message="No Course picked!")
        elif self.desc_list.get() not in [self.course_data[row][1]+" ("+self.course_data[row][0]+")" for row in range(1,len(self.course_data))]:
            messagebox.showerror(title='Button Error', message="No existing Course picked!")
        else:
            self.get_course = self.desc_list.get().split(' (')
            self.specific_course = self.get_course[0]
            with open('Courses.csv', 'r') as read_file:
                reader = csv.reader(read_file)
                course = [row for row in reader]
                course_num_rows = len(course)
            for i in range(course_num_rows):
                if course[i][1]==self.specific_course:
                    self.code = course[i][0]
                    rem_course = [row for row in course if row != course[i]]
                    with open('Courses.csv', 'w', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerows(rem_course)
                    update = process.read_csv("Courses.csv")
                    self.set_desc_combo([update[row][1]+" ("+update[row][0]+")" for row in range(1,len(rem_course)-1)])
            for i in range(student_num_rows):
                if self.stud_data[i][5] == self.code:
                    self.stud_data[i][4] = enroll_stat[0]
                    self.stud_data[i][5] = enroll_stat[1]
            
            with open('Students.csv', 'w', newline='') as new_enroll_stat:
                writer = csv.writer(new_enroll_stat)
                writer.writerows(self.stud_data)
            messagebox.showinfo(title="Action Successful", message="Course successfully deleted")
            process.show_students(self.stud_data)
            self.desc_list['textvariable'] = tk.StringVar(value="")
class Processing:
    def read_csv(csv_file):
        student_data = []
        with open(csv_file, 'r', newline='') as read_file:
            reader = csv.reader(read_file)
            for row in reader:
                student_data.append(row)
        return student_data
    def show_students(stud_data):
        students_frame = customtkinter.CTkScrollableFrame(window, 
                                                          height= 450, 
                                                          width=700, 
                                                          fg_color='#d9d9d9')
        showlist = []
        for i, row in enumerate(stud_data, start=0):
            showlist.append(row[0])
            for col in range(0, 6):
                tk.Label(students_frame, text=row[col], bg="#d9d9d9").grid(row=i, column=col, padx=17, pady=3)

        students_frame.grid(row=1, column=1, padx=45, pady=10)
        students_frame.grid_propagate()
    def valid_id_entry(entry):
        return len(entry) <= 9

    
if __name__ == "__main__":
        window = tk.Tk()
        main_window = MainWindow(window)
        window.title("Simple Student Information System")
        window.geometry("1040x600")
        window.configure(bg="Maroon")
        window.resizable(False,False)
        window.mainloop()



