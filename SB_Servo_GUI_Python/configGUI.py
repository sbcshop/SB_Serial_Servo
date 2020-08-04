#! /usr/bin/python3

"""
This file contains GUI code for Configuring of SB Serial Servo
Developed by - SB Components
http://sb-components.co.uk
"""

from servo_instruction import SBSServo
import logging
import meter
import threading
import webbrowser
import shutil
from tkinter import font
import tkinter as tk
from tkinter import messagebox
from time import sleep
from os import path, system, name

COMPORT_BASE = ""
if name == "posix":
    COMPORT_BASE = "/dev/"
    COMPORT = "ttyS0"
else:
    COMPORT = ""


class MainApp(tk.Tk):
    """
    This is a class for Creating Frames and Buttons for left and top frame
    """

    def __init__(self, *args, **kwargs):
        global logo, img, xy_pos

        tk.Tk.__init__(self, *args, **kwargs)

        self.screen_width = tk.Tk.winfo_screenwidth(self)
        self.screen_height = tk.Tk.winfo_screenheight(self)
        self.app_width = 800
        self.app_height = 480
        self.xpos = (self.screen_width / 2) - (self.app_width / 2)
        self.ypos = (self.screen_height / 2) - (self.app_height / 2)
        xy_pos = self.xpos, self.ypos

        self.geometry(
            "%dx%d+%d+%d" % (self.app_width, self.app_height, self.xpos,
                             self.ypos))
        self.title(" Servo Configuration")
        if not self.screen_width > self.app_width:
            self.attributes('-fullscreen', True)

        self.config(bg="gray85")

        img = tk.PhotoImage(file=Root_Dir + '/Images/settings.png')
        logo = tk.PhotoImage(file=Root_Dir + '/Images/sblogo.png')

        self.top_frame = tk.Frame(self, height=int(self.app_height / 15), bd=2,
                                  width=self.app_width, bg="gray85")
        self.top_frame.pack(padx=(225, 0), side="top", fill="both")
        self.top_frame.pack_propagate(0)

        self.left_frame = tk.Frame(self, width=int(self.app_width / 4),
                                   bg="gray85")
        self.left_frame.pack(side="left", fill="both")
        self.left_frame.pack_propagate(0)

        self.right_frame = tk.Frame(self, bg="gray85")
        self.right_frame.pack(side="left", fill="both", expand=True)

        self.label_font = font.Font(family="Helvetica", size=10)
        self.heading_font = font.Font(family="Helvetica", size=12)

        self.top_frame_contents()

        self.frames = {}

        for F in (OperateFrame, ParameterFrame, AboutFrame):
            frame_name = F.__name__
            frame = F(parent=self.right_frame, controller=self)
            self.frames[frame_name] = frame
            frame.config(bg="white")
            frame.grid(row=0, column=0, sticky="nsew")

        self.left_frame_contents()
        self.show_frame("OperateFrame")

        tk.Label(self, text="SB Serial Servo", bg="gray85",
                 fg='SteelBlue',
                 font=("Helvetica", 21)).place(x=10, y=0)

    def close_robot(self):
        """
        This function delete the temp folder and close
        """
        try:
            shutil.rmtree(Root_Dir + '/.Temp')
        except FileNotFoundError:
            pass
        logging.info('SB Servo Closed Successfully..!!')
        self.destroy()

    def operateButton(self):
        """
        This function raise and sunk Operate button on top frame
        """
        self.operate_button.config(relief="sunken", fg="SteelBlue2")
        self.about_button.config(relief="raised", fg="black")
        self.param_button.config(relief="raised", fg="black")
        self.show_frame("OperateFrame")

    def parameterButton(self):
        """
        This function raise and sunk Parameter button on top frame
        """
        self.operate_button.config(relief="raised", fg="black")
        self.about_button.config(relief="raised", fg="black")
        self.param_button.config(relief="sunken", fg="turquoise4")
        ret_frame = self.get_frame("OperateFrame")
        if ret_frame.readFlag == True:
            ret_frame.servoContinousRead()
        self.show_frame("ParameterFrame")

    def about_button(self):
        """
        This function raise and sunk About Us button on top frame
        """
        self.operate_button.config(relief="raised", fg="black")
        self.param_button.config(relief="raised", fg="black")
        self.about_button.config(relief="sunken", fg="SteelBlue2")
        self.show_frame("AboutFrame")

    @staticmethod
    def manual_button():
        """
        This function will open a pdf file in pdf reader
        """
        system("xdg-open " + Root_Dir + "/Manuals/SB_Servo_User_Manual.pdf")

    def top_frame_contents(self):
        """
        This function creates the top frame buttons
        """
        self.closeButton = tk.Button(self.top_frame, text='Close', fg="black",
                                     bg="gray90", font=self.label_font, bd=2,
                                     highlightthickness=0,
                                     command=self.close_robot)
        self.closeButton.pack(padx=15, side="right")

        self.manual_button = tk.Button(self.top_frame, text="Manual",
                                       fg="black",
                                       bg="gray90", font=self.label_font, bd=2,
                                       highlightthickness=0,
                                       command=self.manual_button)
        self.manual_button.pack(padx=15, side="right")

        self.about_button = tk.Button(self.top_frame, text="About Us",
                                      fg="black",
                                      bg="gray90", font=self.label_font, bd=2,
                                      highlightthickness=0,
                                      command=self.about_button)
        self.about_button.pack(padx=15, side="right")

        self.param_button = tk.Button(self.top_frame, text="Parameters",
                                      fg="black",
                                      bg="gray90", font=self.label_font, bd=2,
                                      highlightthickness=0,
                                      command=self.parameterButton)
        self.param_button.pack(padx=15, side="right")

        self.operate_button = tk.Button(self.top_frame, text="Operation",
                                        fg="black",
                                        bg="gray90", font=self.label_font,
                                        bd=2,
                                        highlightthickness=0,
                                        command=self.operateButton)
        self.operate_button.pack(padx=15, side="right")

    def left_frame_contents(self):
        """
        This function creates the left frame widgets
        """
        global logo

        serial_box = tk.Canvas(self.left_frame, width=180,
                               height=150, bg="white", bd=2)
        serial_box.grid(row=0, column=0, sticky="e", padx=12, pady=20)
        serial_box.grid_propagate(False)

        for i in range(4):
            serial_box.grid_rowconfigure(i, weight=1)
            if i < 3:
                serial_box.grid_columnconfigure(i, weight=1)

        serial_heading = tk.Label(serial_box, bg="SteelBlue2", fg="white",
                                  text="Serial", font=self.heading_font)
        serial_heading.grid(row=0, column=0, columnspan=3, sticky="new", padx=2, pady=2)

        com_label = tk.Label(serial_box, bg="white", fg="Black",
                             text="Comm Port",
                             font=self.label_font)
        com_label.grid(row=1, column=0)

        self.com_entry = tk.Entry(serial_box,
                                  width=13, font=self.label_font)
        self.com_entry.grid(row=1, column=2)
        self.com_entry.insert(0, COMPORT)

        baud_label = tk.Label(serial_box, bg="white", fg="Black",
                              text="Baudrate",
                              font=self.label_font)
        baud_label.grid(row=2, column=0)

        baud_entry = tk.Entry(serial_box, width=13, font=self.label_font)
        baud_entry.insert("end", "115200")
        baud_entry.grid(row=2, column=2)
        baud_entry.config(state="readonly")

        self.circle = tk.Canvas(serial_box, height=40, width=40, bg="white",
                                bd=0)
        self.indication = self.circle.create_oval(10, 10, 30, 30, fill="red")
        self.circle.grid(row=3, column=0)

        self.connect_button = tk.Button(serial_box, text="Connect",
                                        bg="gray90",
                                        font=self.label_font,
                                        command=self.connect_port)
        self.connect_button.grid(row=3, column=2)

        label = tk.Label(self.left_frame, image=logo, height=40, width=225,
                         bg='white')
        label.place(x=0, y=400)

    def connect_port(self):
        """
        This function connects the serial port
        """
        if self.connect_button.cget(
                'text') == 'Connect' and self.com_entry.get():
            robot.connect(COMPORT_BASE + self.com_entry.get())
            if robot.alive:
                self.connect_button.config(relief="sunken", text="Disconnect")
                self.circle.itemconfigure(self.indication, fill="green3")
                self.com_entry.config(state="readonly")

        elif self.connect_button.cget('text') == 'Disconnect':
            ret_frame = self.get_frame("OperateFrame")
            if ret_frame.readFlag:
                ret_frame.servoContinousRead()

            self.connect_button.config(relief="raised", text="Connect")
            self.circle.itemconfigure(self.indication, fill="red")
            self.com_entry.config(state="normal")
            robot.disconnect()
        else:
            errorLabel = tk.Label(self.left_frame, text="Enter Comm Port..!!",
                                  bg="yellow")
            errorLabel.grid(row=4, column=0)
            errorLabel.after(2000, errorLabel.grid_forget)

    def show_frame(self, frame_name):
        """
        This function raise the frame on Top
        Args:
            frame_name: Name of the Frame
        """
        frame = self.frames[frame_name]
        frame.tkraise()

    def get_frame(self, frame_name):
        """
        This function returns the address of given frame
        Args:
            frame_name: Name of the Frame
        Return:
            Address of frame_name
        """
        return self.frames[frame_name]


class OperateFrame(tk.Frame):
    """
    This is a class for creating widgets for Operate frame
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.readFlag = False
        for i in range(2):
            self.grid_columnconfigure(i, weight=1)

        self.controller.operate_button.config(relief="sunken", fg="SteelBlue3")

        self.IDVar = tk.IntVar()
        self.IDVar.set(1)
        self.posScaleVar = tk.IntVar()
        self.posScaleVar.set(500)
        self.timeScaleVar = tk.IntVar()
        self.timeScaleVar.set(500)
        self.speedScaleVar = tk.IntVar()
        self.speedScaleVar.set(500)
        #  Test
        self.Dir_Var = tk.IntVar()
        self.Dir_Var.set(1)
        self.motor_stat = 0

        #  ID
        id_box = tk.Canvas(self, width=int(self.controller.app_width / 3.5),
                           height=int(self.controller.app_height / 5), bd=2,
                           bg="white")
        id_box.grid(row=0, column=0, padx=10, pady=5)
        id_box.grid_propagate(0)

        for i in range(3):
            id_box.grid_columnconfigure(i, weight=1)
            if i < 2:
                id_box.grid_rowconfigure(i, weight=1)

        id_heading = tk.Label(id_box, bg="SteelBlue2", fg="white",
                              text="ID", font=self.controller.heading_font)
        id_heading.grid(row=0, column=0, columnspan=3, sticky="new", padx=2,
                        pady=2)

        id_label = tk.Label(id_box, bg="white", fg="Black",
                            text="Servo ID (1~253):",
                            font=self.controller.label_font)
        id_label.grid(row=1, column=0, pady=(0, 8))

        id_vcmd = (self.register(self.id_validate), '%P')

        self.id_entry = tk.Entry(id_box, validate='key',
                                 validatecommand=id_vcmd,
                                 width=6, textvariable=self.IDVar)
        self.id_entry.grid(row=1, column=2, pady=(0, 8))

        self.readServo_button = tk.Button(id_box, text="Read", bg="gray90",
                                          command=self.servoContinousRead)
        self.readServo_button.grid(row=2, column=0, pady=(0, 5))

        # Servo test
        servo_box = tk.Canvas(self, width=int(self.controller.app_width / 3.5),
                              height=int((self.controller.app_height / 4)),
                              bg="white", bd=2)
        servo_box.grid(row=1, column=0, padx=10, pady=5)
        servo_box.grid_propagate(0)

        for i in range(4):
            servo_box.grid_columnconfigure(i, weight=1)
        servo_heading = tk.Label(servo_box, bg="SteelBlue2", fg="white",
                                 text="Servo Test",
                                 font=self.controller.heading_font)
        servo_heading.grid(row=0, column=0, columnspan=4, sticky="new", padx=2,
                           pady=1)

        tk.Button(servo_box, text="Motor Mode", bg="gray90", width=30,
                  command=lambda: self.mode_win(0)).grid(row=1, column=0,
                                                         padx=7,
                                                         pady=(10, 5))

        tk.Button(servo_box, text="Servo Mode", bg="gray90", width=30,
                  command=lambda: self.mode_win(1)).grid(row=2, column=0,
                                                         padx=7,
                                                         pady=(0, 5))

        #  Torque
        motor_box = tk.Canvas(self,
                              width=int(self.controller.app_width / 3.5),
                              height=int(self.controller.app_height / 7),
                              bg="white", bd=2)
        motor_box.grid(row=2, column=0, padx=10, pady=1)
        motor_box.grid_propagate(0)
        motor_box.grid_columnconfigure(0, weight=1)

        motor_heading = tk.Label(motor_box, bg="SteelBlue2", fg="white",
                                 text="Torque On/Off ",
                                 font=self.controller.heading_font)
        motor_heading.grid(row=0, column=0, sticky="new", padx=2,
                           pady=1)
        self.motorButton = tk.Button(motor_box, text="ON", bg="green3",
                                     font=20, command=self.servoTorque)
        self.motorButton.grid(row=1, column=0, padx=5, pady=1)

        # Gauge Canvas
        status_box = tk.Canvas(self, width=int(self.controller.app_width /
                                               4.1),
                               height=int(self.controller.app_height / 1.14),
                               bg="white", bd=2)
        status_box.grid(row=0, column=1, rowspan=3, pady=5, padx=(0, 15),
                        sticky="w")
        status_box.grid_propagate(0)

        for i in range(3):
            status_box.grid_columnconfigure(i, weight=1)
            if i < 2:
                status_box.grid_rowconfigure(i, weight=1)

        status_heading = tk.Label(status_box, bg="SteelBlue2", fg="white",
                                  text="Current Status",
                                  font=self.controller.heading_font)
        status_heading.grid(row=0, column=0, sticky="new", padx=2, pady=2)

        self.posGauge = meter.PositionMeter(status_box, max_value=1000,
                                            min_value=0, size=180)
        self.posGauge.grid(row=1, column=0, pady=(0, 20))

        self.volGauge = meter.VoltageMeter(status_box, max_value=10,
                                           min_value=0,
                                           size=200)
        self.volGauge.grid(row=2, column=0)

        self.tempScale = tk.Scale(status_box, from_=-10, to=150, width=10,
                                  orient="horizontal",
                                  label="Temperature °C",
                                  font=("helvetica", 11), bg="white",
                                  troughcolor="tomato", fg="black",
                                  highlightthickness=0)
        self.tempScale.grid(row=3, column=0, columnspan=2, pady=20, padx=20,
                            sticky="nsew")

    def mode_win(self, mode):
        """ Motor Mode and Servo Mode options
        :param mode: Boolean, True for Servo Mode False for motor Mode
        :return: None
        """
        if robot.alive:
            servo_id = int(self.IDVar.get())

            width = int(self.controller.app_width / 4.2)
            height = int(self.controller.app_height / 2)

            top = tk.Toplevel(self, bg="white", bd=2)
            time_vcmd = (self.register(self.time_validate), '%P')
            top.resizable(False, False)

            top.grab_set()

            def destroy_top(obj):
                obj.motor_stat = 1
                obj.rot_motor()
                top.destroy()

            if mode:
                logging.info("Servo Mode")
                response = robot.readAngleLimit(servo_id)
                if not (response and response[1]):
                    robot.writeAngleLimit(ID=servo_id, angleMin=0,
                                          angleMax=1000)
                top.geometry("%dx%d+%d+%d" % (width, height, xy_pos[0] * 3 / 2,
                                              xy_pos[1] * 9/7))
                top.title("Servo Mode")
                time_label = tk.Label(top, text="Time (ms)", bg="white",
                                      fg="green",
                                      font=self.controller.label_font)
                time_label.grid(row=1, column=0)
                time_entry = tk.Entry(top, validate='key',
                                      validatecommand=time_vcmd,
                                      width=6, font=self.controller.label_font,
                                      textvariable=self.timeScaleVar)
                time_entry.grid(row=2, column=0)

                time_scale = tk.Scale(top, orient="horizontal", bg="white",
                                      from_=1, to=999,
                                      troughcolor="gray90",
                                      highlightthickness=0,
                                      variable=self.timeScaleVar)
                time_scale.grid(row=2, column=1, columnspan=3, sticky="ew",
                                padx=5,
                                pady=0)

                speed_label = tk.Label(top, text="Speed (°/s)", bg="white",
                                       fg="green",
                                       font=self.controller.label_font)
                speed_label.grid(row=3, column=0, pady=1)

                speed_entry = tk.Entry(top, validate='key',
                                       validatecommand=time_vcmd,
                                       width=6,
                                       font=self.controller.label_font,
                                       textvariable=self.speedScaleVar)
                speed_entry.grid(row=4, column=0)

                speed_scale = tk.Scale(top, orient="horizontal", bg="white",
                                       from_=1, to=999,
                                       troughcolor="gray90",
                                       highlightthickness=0,
                                       variable=self.speedScaleVar)
                speed_scale.grid(row=4, column=1, columnspan=3, sticky="ew",
                                 padx=5,
                                 pady=0)

                pos_label = tk.Label(top, text="Position", bg="white",
                                     fg="green",
                                     font=self.controller.label_font)
                pos_label.grid(row=5, column=0, pady=1)

                pos_vcmd = (self.register(self.pos_validate), '%P')
                pos_entry = tk.Entry(top, validate='key',
                                     validatecommand=pos_vcmd,
                                     width=6, font=self.controller.label_font,
                                     textvariable=self.posScaleVar)
                pos_entry.bind('<Return>', self.updatePosValue)
                pos_entry.grid(row=6, column=0)

                pos_scale = tk.Scale(top, orient="horizontal", bg="white",
                                     from_=0, to=999,
                                     variable=self.posScaleVar,
                                     command=self.updatePosValue,
                                     troughcolor="gray90",
                                     highlightthickness=0)
                pos_scale.grid(row=6, column=1, columnspan=3, sticky="ew",
                               padx=5,
                               pady=1)

                write_button = tk.Button(top, text="Write",
                                         command=self.writeServo)
                write_button.grid(row=7, column=0, pady=1)
                tk.Button(top, text="Exit", command=top.destroy).grid(row=7,
                                                                      column=2,
                                                                      pady=1)

            else:
                logging.info("Motor Mode")
                robot.writeAngleLimit(ID=servo_id, angleMin=0, angleMax=0)
                top.title("Motor Mode")
                top.geometry("%dx%d+%d+%d" % (width * 1.3, height / 1.4,
                                              xy_pos[0] * 3/2.06, xy_pos[1] * 9 / 7))

                tk.Radiobutton(top, text="Clockwise", variable=self.Dir_Var,
                               fg="black", bg="White", relief="flat",
                               value=1).grid(row=0, column=0, padx=10,
                                             pady=2.5, sticky='new')
                tk.Radiobutton(top, text="Anti-Clockwise",
                               variable=self.Dir_Var,
                               fg="black", bg="white", relief="flat",
                               value=0).grid(
                    row=0, column=1, padx=10, pady=5, sticky='new')

                speed_label = tk.Label(top, text="Speed (°/s)", bg="white",
                                       fg="green",
                                       font=self.controller.label_font)
                speed_label.grid(row=1, column=0, pady=1)

                speed_entry = tk.Entry(top, validate='key',
                                       validatecommand=time_vcmd,
                                       width=6,
                                       font=self.controller.label_font,
                                       textvariable=self.speedScaleVar)
                speed_entry.grid(row=2, column=0)

                speed_scale = tk.Scale(top, orient="horizontal", bg="white",
                                       from_=1, to=999,
                                       troughcolor="gray90",
                                       highlightthickness=0,
                                       variable=self.speedScaleVar)
                speed_scale.grid(row=2, column=1, columnspan=3, sticky="ew",
                                 padx=5,
                                 pady=0)

                self.start_stop = tk.Button(top, text="Start", bg="Green",
                                            command=self.rot_motor)
                self.start_stop.grid(row=3, column=0, pady=(10, 0))

                button = tk.Button(top, text="Exit", command=lambda: destroy_top(self))
                button.grid(row=3, column=1, pady=(10, 0))

        else:
            messagebox.showerror("Comm Error", "Comm Port is not "
                                               "Connected..!!")

    def rot_motor(self):
        """
        Operate in motor Mode
        :return: None
        """
        servo_id = int(self.id_entry.get())
        if not self.motor_stat:
            speed = self.speedScaleVar.get()
            direction = self.Dir_Var.get()
            if robot.alive:
                robot.motor_mode(servo_id, speed=speed, direction=direction)
                self.start_stop.config(text="Stop", bg="Red", )
                self.motor_stat = 1
            else:
                messagebox.showerror("Comm Error",
                                     "Comm Port is not Connected..!!")
        else:
            if robot.alive:
                robot.motor_mode(servo_id, speed=0, direction=0)
                self.start_stop.config(text="Start", bg="Green", )
                self.motor_stat = 0
            else:
                messagebox.showerror("Comm Error",
                                     "Comm Port is not Connected..!!")

    def id_validate(self, new_value):
        """
        Validate the ID of servo in Operate frame
        """
        try:
            if not new_value or 0 < int(new_value) <= 253:
                return True
            else:
                self.bell()
                return False
        except ValueError:
            self.bell()
            return False

    def time_validate(self, new_value):
        try:
            if not new_value or 0 <= int(new_value) <= 3000:
                return True
            else:
                self.bell()
                return False
        except ValueError:
            self.bell()
            return False

    def pos_validate(self, new_value):
        try:
            if not new_value or 0 <= int(new_value) <= 1000:
                return True
            else:
                self.bell()
                return False
        except ValueError:
            self.bell()
            return False

    def writeServo(self):
        """
        This function write time and position slider values to servo motor
        """
        try:
            if self.id_entry.get():
                if robot.alive:
                    robot.servoWrite(int(self.id_entry.get()),
                                     int(self.posScaleVar.get()),
                                     int(self.timeScaleVar.get()),
                                     int(self.speedScaleVar.get()))
                else:
                    messagebox.showerror("Comm Error",
                                         "Comm Port is not Connected..!!")
            else:
                messagebox.showerror("Value Error", "Enter Servo ID!")
        except ValueError:
            messagebox.showerror("Value Error", "Incorrect Entry Value")

    def servoTorque(self):
        """
        This function enable and disbale servo motor torque
        """
        if robot.alive:
            if self.motorButton.cget('text') == 'ON' and self.id_entry.get():
                self.motorButton.config(relief="sunken", bg="tomato",
                                        text="OFF")
                robot.torqueServo(int(self.id_entry.get()), 1)

            elif self.motorButton.cget('text') == 'OFF':
                self.motorButton.config(relief="raised", bg="green3",
                                        text="ON")
                robot.torqueServo(int(self.id_entry.get()), 0)
        else:
            messagebox.showerror("Comm Error",
                                 "Comm Port is not Connected..!!")

    def updatePosValue(self, value):
        """
        This function write time and position slider values to servo motor
        """
        if robot.alive:
            robot.servoWrite(int(self.id_entry.get()),
                             int(self.posScaleVar.get()),
                             int(self.timeScaleVar.get()),
                             int(self.speedScaleVar.get()))

    def servoContinousRead(self):
        """
        This function create thread to read params from servo motor
        """
        if robot.alive:
            if self.id_entry.get():
                if self.readServo_button.cget(
                        'text') == 'Read' and self.id_entry.get():
                    self.readServo_button.config(relief="sunken", text="Stop")
                    self.id_entry.config(state="readonly")
                    self.readFlag = True
                    self.threadContRead = threading.Thread(
                        target=self._continousRead)
                    self.threadContRead.daemon = True
                    self.threadContRead.start()

                elif self.readServo_button.cget('text') == 'Stop':
                    self.readServo_button.config(relief="raised", text="Read")
                    self.id_entry.config(state="normal")
                    self.readFlag = False
            else:
                messagebox.showerror("Value Error",
                                     "Enter Servo ID!")
        else:
            messagebox.showerror("Comm Error",
                                 "Comm Port is not Connected..!!")

    def _continousRead(self):
        """
        This thread read params from servo motor & display on gauge
        """
        try:
            ID = int(self.id_entry.get())
            while self.readFlag:
                #  Position Meter
                pos = robot.positionRead(ID)
                if pos and pos > 1023:
                    pos = 0
                self.posGauge.set_value(int(pos))

                #  Voltage Gauge
                voltage = robot.voltageRead(ID)
                self.volGauge.set_value(voltage)

                #  Temperature Meter
                temp = robot.tempRead(ID)
                self.tempScale.set(temp)

                if not self.readFlag:
                    self.posGauge.set_value(int(0))
                    self.volGauge.set_value(float(0))
                    self.tempScale.set(0)
                    break

        except TypeError:
            self.servoContinousRead()
            messagebox.showerror("Response Error",
                                 "No Response from Motor..!!")


class ParameterFrame(tk.Frame):
    """
    This is a class for Creating widgets for Parameter frame
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        for i in range(3):
            self.grid_columnconfigure(i, weight=1)

        #  ID
        self.ID_Var = tk.IntVar()
        self.New_ID = tk.IntVar()
        self.Answer_Var = tk.IntVar()

        #  Default variable Value
        self.ID_Var.set(1)
        self.New_ID.set(2)
        self.Answer_Var.set(0)

        #  Servo Search Box
        win_width = int(2 * (self.controller.app_width / 9))
        win_height = int(2 * (self.controller.app_height / 6))

        search_box = tk.Canvas(self, width=win_width, bd=2,
                               height=win_height, bg="white")
        search_box.grid(row=0, column=0, padx=8, pady=5, rowspan=2,
                        sticky="w")
        search_box.grid_propagate(0)

        for k in range(3):
            search_box.grid_columnconfigure(k, weight=1)
            if i < 2:
                search_box.grid_rowconfigure(k, weight=1)

        tk.Label(search_box, bg="turquoise3", fg="white", text="Servo List",
                 width=21, height=1,
                 font=self.controller.heading_font).place(x=0, y=2)

        #  #  Search Button
        serch_button = tk.Button(search_box, text="Search", bg="gray90",
                                 fg="black", width=8,
                                 command=self.search_id)
        serch_button.place(x=6, y=26)

        #  #  List box
        self.commandBox = tk.Listbox(search_box, height=6, width=20)
        self.commandBox.place(x=5, y=58)

        yscrollbar = tk.Scrollbar(search_box)
        yscrollbar.place(x=169, y=58, relheight=.65)

        #  Select ID
        id_box = tk.Canvas(self,
                           width=int(2 * (self.controller.app_width / 12)),
                           height=int(self.controller.app_height / 7),
                           bg="white", bd=2)
        id_box.grid(row=0, column=1, padx=0, pady=1, rowspan=1, sticky="w")
        id_box.grid_propagate(0)

        for k in range(3):
            id_box.grid_columnconfigure(k, weight=1)
            if i < 2:
                id_box.grid_rowconfigure(k, weight=1)

        id_heading = tk.Label(id_box, bg="turquoise3", fg="white",
                              text="ID",
                              font=self.controller.heading_font)
        id_heading.grid(row=0, column=0, columnspan=3, sticky="new", padx=2,
                        pady=2)

        id_label = tk.Label(id_box, bg="white", fg="Black", text="Servo ID:",
                            font=self.controller.label_font)
        id_label.grid(row=1, column=0, pady=10)

        id_vcmd = (self.register(self.id_validate), '%P')
        self.id_entry = tk.Entry(id_box, validate='key',
                                 validatecommand=id_vcmd,
                                 width=6, font=self.controller.label_font,
                                 textvariable=self.ID_Var)
        self.id_entry.grid(row=1, column=1)

        #  CHANGE ID
        change_id_box = tk.Canvas(self,
                                  width=int(
                                      2 * (self.controller.app_width / 12)),
                                  height=int(self.controller.app_height / 7),
                                  bg="white", bd=2)
        change_id_box.grid(row=1, column=1, padx=0, pady=1, sticky="w")
        change_id_box.grid_propagate(0)

        for k in range(3):
            change_id_box.grid_columnconfigure(k, weight=1)
            if i < 2:
                change_id_box.grid_rowconfigure(k, weight=1)

        id_heading = tk.Label(change_id_box, bg="turquoise3", fg="white",
                              text="Change ID",
                              font=self.controller.heading_font)
        id_heading.grid(row=0, column=0, columnspan=3, sticky="ew", padx=2,
                        pady=2)

        new_id_label = tk.Label(change_id_box, bg="white", fg="Black",
                                text="New ID:",
                                font=self.controller.label_font)
        new_id_label.grid(row=1, column=0, padx=5, pady=10)

        self.new_id_entry = tk.Entry(change_id_box, validate='key',
                                     validatecommand=id_vcmd,
                                     width=6, font=self.controller.label_font,
                                     textvariable=self.New_ID)
        self.new_id_entry.grid(row=1, column=1)

        #  Answer/Response Status
        canvas_answer = tk.Canvas(self, width=int(2 * (
                self.controller.app_width / 12)),
                                  height=int(self.controller.app_height / 3),
                                  bg="white", bd=2)
        canvas_answer.grid(row=0, column=2, padx=0, pady=5, rowspan=3, sticky="nw")
        canvas_answer.grid_propagate(0)
        for k in range(3):
            canvas_answer.grid_columnconfigure(k, weight=1)
            if i < 2:
                canvas_answer.grid_rowconfigure(k, weight=1)

        baud_heading = tk.Label(canvas_answer, bg="turquoise3", fg="white",
                                text="Response Status",
                                font=self.controller.heading_font)
        baud_heading.grid(row=0, column=0, columnspan=3, sticky="new", padx=2,
                          pady=2)

        tk.Radiobutton(canvas_answer, text="Off", variable=self.Answer_Var,
                       fg="black", bg="gray90", relief="groove",
                       value=0).grid(row=1, column=0, padx=10, pady=50,
                                     sticky='new')
        tk.Radiobutton(canvas_answer, text="On", variable=self.Answer_Var,
                       fg="black", bg="gray90", relief="groove", value=1).grid(
            row=1, column=1, padx=10, pady=50, sticky='new')

        #  Angle
        angle_box = tk.Canvas(self,
                              width=int(2 * (self.controller.app_width / 9)),
                              height=int(self.controller.app_height / 3),
                              bg="white", bd=2)
        angle_box.grid(row=2, column=0, padx=8, pady=5, sticky="w")
        angle_box.grid_propagate(0)
        angle_box.grid_columnconfigure(0, weight=1)

        angle_heading = tk.Label(angle_box, bg="turquoise3", fg="white",
                                 text="Angle",
                                 font=self.controller.heading_font)
        angle_heading.grid(row=0, column=0, sticky="new",
                           padx=2, pady=2)

        self.angleScale1 = tk.Scale(angle_box, orient="horizontal", bg="white",
                                    from_=0, to=1000, troughcolor="gray90",
                                    highlightthickness=0)
        self.angleScale1.grid(row=1, column=0, sticky="ew", padx=5, pady=20)
        self.angleScale1.set(1000)

        self.angleScale2 = tk.Scale(angle_box, orient="horizontal", bg="white",
                                    from_=0, to=1000, troughcolor="gray90",
                                    highlightthickness=0)
        self.angleScale2.grid(row=2, column=0, sticky="ew", padx=5)

        self.commandBox.config(yscrollcommand=yscrollbar.set)
        yscrollbar.config(command=self.commandBox.yview)
        self.commandBox.bind("<Double-Button-1>", self.onclick_play)

        #  Voltage
        voltage_box = tk.Canvas(self,
                                width=int((self.controller.app_width / 6) + 2),
                                height=int(
                                    2 * (self.controller.app_height / 6) + 2),
                                bg="white", bd=2)
        voltage_box.grid(row=2, column=1, pady=5, sticky="nw")
        voltage_box.grid_propagate(0)
        for jj in range(2):
            voltage_box.grid_columnconfigure(jj, weight=1)
            voltage_box.grid_rowconfigure(jj, weight=1)

        volt_heading = tk.Label(voltage_box, bg="turquoise3", fg="white",
                                text="Voltage",
                                font=self.controller.heading_font)
        volt_heading.grid(row=0, column=0, sticky="new", columnspan=2,
                          padx=2, pady=2)

        self.voltScale1 = tk.Scale(voltage_box, bg="white", from_=12, to=4.5,
                                   resolution=0.1, troughcolor="gray90",
                                   highlightthickness=0, label='L')
        self.voltScale1.grid(row=1, column=0, sticky="ns", pady=5)

        self.voltScale2 = tk.Scale(voltage_box, bg="white", from_=12, to=4.5,
                                   resolution=0.1, troughcolor="gray90",
                                   highlightthickness=0, label='H')
        self.voltScale2.grid(row=1, column=1, sticky="ns", pady=5)
        self.voltScale2.set(12)

        # Temperature
        temperature_box = tk.Canvas(self,
                                    width=int((self.controller.app_width / 6)),
                                    height=int(
                                        2 * (self.controller.app_height / 6)),
                                    bg="white", bd=2)
        temperature_box.grid(row=2, column=2, pady=5, sticky="nw")
        temperature_box.grid_propagate(0)
        temperature_box.grid_columnconfigure(0, weight=1)

        temperature_heading = tk.Label(temperature_box, bg="turquoise3",
                                       fg="white",
                                       font=self.controller.heading_font,
                                       text="Temperature (°F)", )
        temperature_heading.grid(row=0, column=0, sticky="new", padx=2, pady=2)

        self.temp_scale = tk.Scale(temperature_box, bg="white",
                                   orient="horizontal",
                                   from_=50, to=100, troughcolor="white",
                                   highlightthickness=0)
        self.temp_scale.grid(row=1, column=0, sticky="nsew", padx=5, pady=20)
        self.temp_scale.set(85)

        #  Buttons
        read_button = tk.Button(self, text="Read", bg="gray90",
                                command=self.read_parameters)
        read_button.grid(row=3, column=0, pady=10)

        write_button = tk.Button(self, text="Write", bg="gray90",
                                 command=self.write_parameters)
        write_button.grid(row=3, column=1, pady=10)

        default_button = tk.Button(self, text="Default", bg="gray90",
                                   command=self.default_write)
        default_button.grid(row=3, column=2, pady=10)

    def onclick_play(self, event):
        """
        This function handle double click play of command
        """
        index = self.commandBox.curselection()
        if index:
            rawData = self.commandBox.get(index)
            self.ID_Var.set(int(rawData))

    def search_id(self):
        if robot.alive:
            received_ids = robot.readID(total_servos=20)

            if received_ids:
                self.commandBox.delete(0, 'end')
                for servo_id in received_ids:
                    self.commandBox.insert('end', str(servo_id))
            else:
                self.commandBox.delete(0, 'end')
                messagebox.showerror("Value Error", "No Servo Connected!")
        else:
            messagebox.showerror("Comm Error", "Comm Port is not "
                                               "Connected..!!")

    def id_validate(self, new_value):
        try:
            if not new_value or 0 <= int(new_value) <= 253:
                return True
            else:
                self.bell()
                return False
        except ValueError:
            self.bell()
            return False

    def read_parameters(self):
        """
        This function read all the parameters from servo and display it
        """
        try:
            if robot.alive:
                #  Read Angle Limits
                servo_id = self.ID_Var.get()
                response = robot.readAngleLimit(servo_id)
                self.angleScale1.set(response[1])
                self.angleScale2.set(response[0])

                #  Read Voltage Limit
                min_voltage, max_voltage = robot.readVolLimit(servo_id)
                self.voltScale1.set(min_voltage)
                self.voltScale2.set(max_voltage)

                #  Answer status
                status = robot.read_answer(servo_id)
                self.Answer_Var.set(status)

                #  Read Temperature Limit
                max_temp = robot.readTempLimit(servo_id)
                self.temp_scale.set(max_temp)
                messagebox.showinfo("Data Read", "Read Done Successfully")

            else:
                messagebox.showerror("Comm Error",
                                     "Comm Port is not Connected..!!")
        except TypeError:
            messagebox.showerror("Read Error", "Motor not Connected..!!")

    def write_parameters(self):
        """
        This function write all the parameters to servo motor
        """
        try:
            if robot.alive:
                servo_id = self.ID_Var.get()
                new_id = self.New_ID.get()

                #  Unlock EEPROM for writing
                robot.write_lock_status(servo_id, 0)
                sleep(.01)

                #  Write ID of servo motor
                robot.writeID(ID=servo_id, new_id=new_id)

                #  Write Angle Limit
                robot.writeAngleLimit(new_id, self.angleScale2.get(),
                                      self.angleScale1.get())

                #  Write Voltage Limit
                robot.writeVolLimit(new_id, self.voltScale1.get(),
                                    self.voltScale2.get())

                #  Write Max Temperature
                robot.writeTempLimit(new_id, self.temp_scale.get())

                # Change Answer Status
                status_var = self.Answer_Var.get()
                robot.write_answer(new_id, status=status_var)

                #  Lock EEPROM for making changing permanent
                robot.write_lock_status(new_id, 1)

                messagebox.showinfo("Data Write", "Write Done Successfully")

            else:
                messagebox.showerror("Comm Error",
                                     "Comm Port is not Connected..!!")

        except ValueError as Ve:
            messagebox.showerror("Value Error", "Fill all fields!!")

    def default_write(self):
        """
        This function set default parameters of servo
        """
        if robot.alive:
            servo_id = self.ID_Var.get()

            #  Unlock EEPROM for writing
            robot.write_lock_status(servo_id, 0)
            sleep(.01)

            #  Write Angle Limit
            robot.writeAngleLimit(servo_id)

            #  Write Voltage Limit
            robot.writeVolLimit(servo_id)

            #  Write Max Temperature
            robot.writeTempLimit(servo_id)

            # Change Answer Status
            robot.write_answer(servo_id)

            #  Lock EEPROM for making changing permanent
            robot.write_lock_status(servo_id, 1)

            messagebox.showinfo("Default Write", "Default Done Successfully")
        else:
            messagebox.showerror("Comm Error",
                                 "Comm Port is not Connected..!!")


class AboutFrame(tk.Frame):
    """
    This is a class for Creating widgets for About Us frame
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, bg="white", fg="SteelBlue2", text="SB-Serial "
                                                                 "Servo",
                         font=('Helvetica', 25))
        label.grid(row=0, column=0, padx=200, pady=30)

        text = tk.Label(self, bg="white", fg="black", font=('Helvetica', 11),
                        text="SB components Serial Servos")
        text.grid(row=1, column=0, padx=(0, 150))

        text = tk.Label(self, bg="white", fg="black", font=('Helvetica', 11),
                        text="1. Open Source")
        text.grid(row=2, column=0, padx=(0, 425))

        text = tk.Label(self, bg="white", fg="black", font=('Helvetica', 11),
                        text="2. Serial UART Control")
        text.grid(row=3, column=0, padx=(0, 388))

        text = tk.Label(self, bg="white", fg="black", font=('Helvetica', 11),
                        text="4. Moves around with precise Smart Bus Servo "
                             "Motors")
        text.grid(row=4, column=0, padx=(0, 180))

        text = tk.Label(self, bg="white", fg="black", font=('Helvetica', 11),
                        text="4. It is upgradable and customizable with "
                             "various parts and sensors")
        text.grid(row=5, column=0, padx=(0, 95))

        label = tk.Label(self, bg='white', fg="black", font=('Helvetica', 12),
                         text="For More Info:")
        label.grid(row=6, column=0, pady=(80, 10))

        website = tk.Button(self, bg="SteelBlue2", fg="white",
                            font=('Helvetica', 15),
                            text="www.sb-components.co.uk",
                            command=self.mainWebsite)
        website.grid(row=7, column=0)

        shop = tk.Button(self, bg="tomato", fg="white", font=('Helvetica', 15),
                         text="Online Store", command=self.shopWebsite)
        shop.grid(row=8, column=0, padx=(0, 130), pady=10)

        github = tk.Button(self, bg="gray60", fg="white",
                           font=('Helvetica', 15),
                           text="Github", command=self.github)
        github.grid(row=8, column=0, padx=(180, 0))

    @staticmethod
    def mainWebsite():
        webbrowser.open("https://sb-components.co.uk")

    @staticmethod
    def shopWebsite():
        webbrowser.open("https://shop.sb-components.co.uk")

    @staticmethod
    def github():
        webbrowser.open("https://github.com/sbcshop/SB_Serial_Servo")


logo = None
img = None
Root_Dir = path.abspath(path.dirname(__file__))
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

if __name__ == "__main__":
    robot = SBSServo()
    app = MainApp()
    app.tk.call('wm', 'iconphoto', app._w, img)
    app.resizable(0, 0)
    app.mainloop()