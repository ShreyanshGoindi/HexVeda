from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.graphics import Color, Line, Ellipse
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.textfield import MDTextField
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDIconButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDDatePicker

import datetime
import re
import random
from enum import Enum
from typing import Optional

# ------------------ Responsive Label -------------------
class ResponsiveLabel(MDLabel):
    base_font_size = 16  # default reference size

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(size=self.update_font_size)
        self.update_font_size()

    def update_font_size(self, *args):
        scale = Window.width / 1080
        scale = max(0.6, scale)
        self.font_size = self.base_font_size * scale

# ------------------ Side Menu -------------------
class SideMenu(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouse_pos, size=self.on_window_resize)
        self.expanded = False
        self.text_labels = []
        self.mobile_mode = Window.width < 600

    def on_kv_post(self, base_widget):
        self.text_labels = [w for w in self.walk(restrict=True) if isinstance(w, ResponsiveLabel)]
        self.on_window_resize(Window, Window.size)

    def on_window_resize(self, window, size):
        if size[0] < 600:
            self.mobile_mode = True
            self.collapse(force=True)
        else:
            self.mobile_mode = False

    def on_mouse_pos(self, window, pos):
        if not self.get_root_window() or self.mobile_mode:
            return
        inside = self.collide_point(*self.to_widget(*pos))
        if inside and not self.expanded:
            self.expand()
        elif not inside and self.expanded:
            self.collapse()

    def expand(self):
        self.expanded = True
        Animation(width=dp(220), d=0.2).start(self)
        for lbl in self.text_labels:
            Animation(opacity=1, d=0.2).start(lbl)

    def collapse(self, force=False):
        self.expanded = False
        Animation(width=dp(70), d=0.2).start(self)
        for lbl in self.text_labels:
            Animation(opacity=0 if force or not self.mobile_mode else 1, d=0.2).start(lbl)

# ------------------ Screen Classes -------------------
# Original screens
class HomeScreen(Screen):
    pass

class ScheduleScreen(Screen):
    pass

class PrecautionsScreen(Screen):
    pass

class ProgressScreen(Screen):
    pass

# New integrated screens
class HomepageScreen(Screen):
    pass

class AppointmentScreen(Screen):
    pass

class ConfirmationScreen(Screen):
    message = StringProperty('')

class DoctorDashboardScreen(Screen):
    pass

class FeedbackScreen(Screen):
    pass

class AppointmentsScreen(Screen):
    pass

class MedicineScreen(Screen):
    pass

class UserSignupScreen(Screen):
    pass

class StaffRegistrationScreen(Screen):
    pass

class AdminPanelScreen(Screen):
    pass

# Gender enum for signup
class Gender(Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"
    UNSPECIFIED = ""

class ValidationError(Exception):
    pass

# ------------------ Progress Chart -------------------
class ProgressChart(Widget):
    def __init__(self, data=None, **kwargs):
        super().__init__(**kwargs)
        self.data = data if data else []
        self.bind(pos=self.update_chart, size=self.update_chart)

    def update_chart(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(0.2, 0.6, 0.3, 1)
            if len(self.data) < 2:
                return
            points = []
            for i, y in enumerate(self.data):
                x_pos = self.x + i * 80
                y_pos = self.y + y
                points.extend([x_pos, y_pos])
                Ellipse(pos=(x_pos - 5, y_pos - 5), size=(10, 10))
            Line(points=points, width=2)

# ------------------ KV Layout -------------------
KV = """
<SideMenu>:
    orientation: "vertical"
    size_hint_x: None
    width: dp(70)
    md_bg_color: 0.9, 0.95, 0.9, 1
    spacing: dp(5)
    padding: dp(10)

    MDBoxLayout:
        orientation: "horizontal"
        size_hint_y: None
        height: dp(56)
        padding: dp(10), 0
        MDIconButton:
            icon: "home"
            on_release: app.change_screen("homepage")
        ResponsiveLabel:
            text: "Home"
            base_font_size: 16
            opacity: 0
            halign: "left"

    MDBoxLayout:
        orientation: "horizontal"
        size_hint_y: None
        height: dp(56)
        padding: dp(10), 0
        MDIconButton:
            icon: "calendar-plus"
            on_release: app.change_screen("appointment")
        ResponsiveLabel:
            text: "Book Appointment"
            base_font_size: 16
            opacity: 0
            halign: "left"

    MDBoxLayout:
        orientation: "horizontal"
        size_hint_y: None
        height: dp(56)
        padding: dp(10), 0
        MDIconButton:
            icon: "doctor"
            on_release: app.change_screen("doctor_dashboard")
        ResponsiveLabel:
            text: "Doctor Dashboard"
            base_font_size: 16
            opacity: 0
            halign: "left"

    MDBoxLayout:
        orientation: "horizontal"
        size_hint_y: None
        height: dp(56)
        padding: dp(10), 0
        MDIconButton:
            icon: "account-plus"
            on_release: app.change_screen("user_signup")
        ResponsiveLabel:
            text: "User Signup"
            base_font_size: 16
            opacity: 0
            halign: "left"

    MDBoxLayout:
        orientation: "horizontal"
        size_hint_y: None
        height: dp(56)
        padding: dp(10), 0
        MDIconButton:
            icon: "account-tie"
            on_release: app.change_screen("staff_registration")
        ResponsiveLabel:
            text: "Staff Registration"
            base_font_size: 16
            opacity: 0
            halign: "left"

    MDBoxLayout:
        orientation: "horizontal"
        size_hint_y: None
        height: dp(56)
        padding: dp(10), 0
        MDIconButton:
            icon: "shield-account"
            on_release: app.change_screen("admin_panel")
        ResponsiveLabel:
            text: "Admin Panel"
            base_font_size: 16
            opacity: 0
            halign: "left"

ScreenManager:
    HomepageScreen:
    AppointmentScreen:
    ConfirmationScreen:
    DoctorDashboardScreen:
    UserSignupScreen:
    StaffRegistrationScreen:
    AdminPanelScreen:

<HomepageScreen>:
    name: "homepage"
    RelativeLayout:
        Image:
            source: "background.jpeg"
            allow_stretch: True
            keep_ratio: False
            size: self.parent.size
            pos: self.parent.pos
        MDBoxLayout:
            orientation: "horizontal"
            SideMenu:
            MDBoxLayout:
                orientation: "vertical"
                spacing: dp(20)
                padding: dp(20)
                
                ResponsiveLabel:
                    text: "Ayurvedic Wellness Management"
                    halign: "center"
                    base_font_size: 32
                
                ScrollView:
                    do_scroll_x: False
                    do_scroll_y: True
                    MDBoxLayout:
                        orientation: 'vertical'
                        size_hint_y: None
                        height: self.minimum_height
                        padding: dp(40), dp(20), dp(40), dp(20)
                        spacing: dp(25)
                        
                        # Hero Section
                        MDCard:
                            size_hint_y: None
                            height: dp(200)
                            md_bg_color: "#EBF4FF"
                            radius: [15, 15, 15, 15]
                            elevation: 2
                            MDBoxLayout:
                                orientation: "vertical"
                                padding: dp(40)
                                spacing: dp(15)
                                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                                MDLabel:
                                    text: "Welcome to Panchakarma Management System"
                                    theme_text_color: "Custom"
                                    text_color: "#1E40AF"
                                    font_style: "H4"
                                    bold: True
                                    halign: "center"
                                    size_hint_y: None
                                    height: dp(40)
                                MDLabel:
                                    text: "Comprehensive healthcare management for traditional Ayurveda"
                                    halign: "center"
                                    theme_text_color: "Custom"
                                    text_color: "#64748B"
                                    font_style: "Body1"
                                    size_hint_y: None
                                    height: dp(25)
                        
                        # Departments Section
                        MDLabel:
                            text: "OUR DEPARTMENTS"
                            halign: "center"
                            font_style: "H5"
                            theme_text_color: "Custom"
                            text_color: "#1E293B"
                            bold: True
                            size_hint_y: None
                            height: dp(35)
                        
                        MDGridLayout:
                            cols: 2
                            spacing: dp(20)
                            size_hint_y: None
                            height: dp(400)
                            
                            MDCard:
                                md_bg_color: "#FFFFFF"
                                elevation: 4
                                radius: [15, 15, 15, 15]
                                padding: dp(20)
                                ripple_behavior: True
                                on_release: app.show_department_doctors("Ayurveda")
                                MDBoxLayout:
                                    orientation: "vertical"
                                    spacing: dp(10)
                                    MDIcon:
                                        icon: "leaf"
                                        theme_text_color: "Custom"
                                        text_color: "#D97706"
                                        font_size: "48sp"
                                        halign: "center"
                                        size_hint_y: None
                                        height: dp(60)
                                    MDLabel:
                                        text: "Ayurveda"
                                        font_style: "H6"
                                        bold: True
                                        theme_text_color: "Custom"
                                        text_color: "#1E293B"
                                        halign: "center"
                                        size_hint_y: None
                                        height: dp(28)
                                    MDLabel:
                                        text: "Traditional healing practices"
                                        font_style: "Caption"
                                        theme_text_color: "Custom"
                                        text_color: "#64748B"
                                        halign: "center"
                                        size_hint_y: None
                                        height: dp(20)
                            
                            MDCard:
                                md_bg_color: "#FFFFFF"
                                elevation: 4
                                radius: [15, 15, 15, 15]
                                padding: dp(20)
                                ripple_behavior: True
                                on_release: app.show_department_doctors("Physiotherapy")

                                MDLabel:
                                    text: "Physiotherapy\\n\\nPhysical rehabilitation"
                                    halign: "center"
                                    font_style: "H6"
                                    theme_text_color: "Custom"
                                    text_color: "#1E293B"
                            
                            MDCard:
                                md_bg_color: "#FFFFFF"
                                elevation: 4
                                radius: [15, 15, 15, 15]
                                padding: dp(20)
                                ripple_behavior: True
                                on_release: app.show_department_doctors("Nutrition")

                                MDLabel:
                                    text: "Nutrition\\n\\nDietary wellness guidance"
                                    halign: "center"
                                    font_style: "H6"
                                    theme_text_color: "Custom"
                                    text_color: "#1E293B"
                            
                            MDCard:
                                md_bg_color: "#FFFFFF"
                                elevation: 4
                                radius: [15, 15, 15, 15]
                                padding: dp(20)
                                ripple_behavior: True
                                on_release: app.show_department_doctors("Yoga")

                                MDLabel:
                                    text: "Yoga\\n\\nMind-body wellness"
                                    halign: "center"
                                    font_style: "H6"
                                    theme_text_color: "Custom"
                                    text_color: "#1E293B"

<AppointmentScreen>:
    name: "appointment"
    RelativeLayout:
        Image:
            source: "background.jpeg"
            allow_stretch: True
            keep_ratio: False
            size: self.parent.size
            pos: self.parent.pos
        MDBoxLayout:
            orientation: "horizontal"
            SideMenu:
            MDBoxLayout:
                orientation: "vertical"
                padding: dp(20)
                spacing: dp(20)
                
                MDCard:
                    orientation: "vertical"
                    radius: [20, 20, 20, 20]
                    padding: dp(20)
                    md_bg_color: "#FFFFFF"
                    elevation: 4
                    size_hint_y: None
                    height: dp(80)
                    MDLabel:
                        text: "Book Appointment"
                        font_style: "H5"
                        theme_text_color: "Custom"
                        text_color: "#1E40AF"
                        bold: True
                        halign: "center"

                ScrollView:
                    MDBoxLayout:
                        orientation: "vertical"
                        padding: dp(18)
                        spacing: dp(12)
                        size_hint_y: None
                        height: self.minimum_height

                        MDBoxLayout:
                            spacing: dp(12)
                            adaptive_height: True
                            MDTextField:
                                id: first_name
                                hint_text: "First Name*"
                                required: True
                                helper_text_mode: "on_error"
                            MDTextField:
                                id: last_name
                                hint_text: "Last Name*"
                                required: True
                                helper_text_mode: "on_error"

                        MDBoxLayout:
                            spacing: dp(12)
                            adaptive_height: True
                            MDTextField:
                                id: email
                                hint_text: "Email*"
                                required: True
                                helper_text_mode: "on_error"
                            MDTextField:
                                id: mobile
                                hint_text: "Mobile*"
                                required: True
                                helper_text_mode: "on_error"

                        MDBoxLayout:
                            spacing: dp(12)
                            adaptive_height: True
                            MDTextField:
                                id: dob
                                hint_text: "Date of Birth"
                                readonly: True
                                on_focus: app.show_date_dropdown(self) if self.focus else None
                            MDTextField:
                                id: gender
                                hint_text: "Gender"
                                readonly: True
                                on_focus: app.show_gender_menu(self) if self.focus else None

                        MDBoxLayout:
                            spacing: dp(12)
                            adaptive_height: True
                            MDTextField:
                                id: app_date
                                hint_text: "Appointment Date*"
                                readonly: True
                                on_focus: app.show_date_dropdown(self) if self.focus else None
                            MDTextField:
                                id: doctor
                                hint_text: "Preferred Doctor"

                        MDTextField:
                            id: issue_type
                            hint_text: "Chief Complaint / Issue*"
                            multiline: True
                            size_hint_y: None
                            height: dp(100)

                        MDTextField:
                            id: address
                            hint_text: "Address"
                            multiline: True
                            size_hint_y: None
                            height: dp(120)

                        MDBoxLayout:
                            size_hint_y: None
                            height: dp(56)
                            spacing: dp(12)
                            padding: [0, dp(6), 0, dp(6)]

                            MDRaisedButton:
                                text: "BOOK APPOINTMENT"
                                md_bg_color: "#1E40AF"
                                theme_text_color: "Custom"
                                text_color: "#FFFFFF"
                                on_release: app.submit_appointment()

                            MDFlatButton:
                                text: "CLEAR"
                                theme_text_color: "Custom"
                                text_color: "#64748B"
                                on_release: app.clear_appointment_form()

<ConfirmationScreen>:
    name: "confirmation"
    RelativeLayout:
        Image:
            source: "background.jpeg"
            allow_stretch: True
            keep_ratio: False
            size: self.parent.size
            pos: self.parent.pos
        MDBoxLayout:
            orientation: "horizontal"
            SideMenu:
            MDBoxLayout:
                orientation: "vertical"
                padding: dp(20)
                spacing: dp(20)
                
                MDCard:
                    orientation: "vertical"
                    radius: [20, 20, 20, 20]
                    padding: dp(20)
                    md_bg_color: "#E8F5E8"
                    elevation: 4
                    MDIcon:
                        icon: "check-circle"
                        theme_text_color: "Custom"
                        text_color: "#059669"
                        font_size: "64sp"
                        halign: "center"
                        size_hint_y: None
                        height: dp(80)
                    MDLabel:
                        text: "Appointment Confirmed!"
                        font_style: "H5"
                        theme_text_color: "Custom"
                        text_color: "#059669"
                        bold: True
                        halign: "center"
                        size_hint_y: None
                        height: dp(40)
                    MDLabel:
                        id: confirm_label
                        text: root.message
                        font_style: "Body1"
                        theme_text_color: "Custom"
                        text_color: "#374151"
                        halign: "center"
                        text_size: self.width, None
                
                MDRaisedButton:
                    text: "BOOK ANOTHER APPOINTMENT"
                    md_bg_color: "#1E40AF"
                    theme_text_color: "Custom"
                    text_color: "#FFFFFF"
                    size_hint_y: None
                    height: dp(48)
                    on_release: app.change_screen("appointment")

<DoctorDashboardScreen>:
    name: "doctor_dashboard"
    RelativeLayout:
        Image:
            source: "background.jpeg"
            allow_stretch: True
            keep_ratio: False
            size: self.parent.size
            pos: self.parent.pos
        MDBoxLayout:
            orientation: "horizontal"
            SideMenu:
            MDBoxLayout:
                orientation: "vertical"
                padding: dp(20)
                spacing: dp(20)
                
                # Header
                MDCard:
                    size_hint_y: None
                    height: dp(120)
                    md_bg_color: "#1E40AF"
                    elevation: 6
                    radius: [15, 15, 15, 15]
                    MDBoxLayout:
                        orientation: "vertical"
                        padding: dp(30), dp(15), dp(30), dp(15)
                        spacing: dp(8)
                        MDLabel:
                            text: "Doctor Dashboard"
                            font_style: "H5"
                            theme_text_color: "Custom"
                            text_color: "#FFFFFF"
                            bold: True
                            halign: "center"
                            size_hint_y: None
                            height: dp(30)
                        MDLabel:
                            text: "Manage patients, appointments, and medical records"
                            font_style: "Body2"
                            theme_text_color: "Custom"
                            text_color: "#BFDBFE"
                            halign: "center"
                            size_hint_y: None
                            height: dp(18)
                
                ScrollView:
                    MDBoxLayout:
                        orientation: 'vertical'
                        size_hint_y: None
                        height: self.minimum_height
                        padding: dp(20)
                        spacing: dp(25)
                        
                        # Quick Stats
                        MDGridLayout:
                            cols: 3
                            spacing: dp(20)
                            size_hint_y: None
                            height: dp(120)
                            
                            MDCard:
                                orientation: "vertical"
                                md_bg_color: "#FFFFFF"
                                elevation: 4
                                radius: [15, 15, 15, 15]
                                padding: dp(20)
                                spacing: dp(8)
                                MDIcon:
                                    icon: "calendar-check"
                                    theme_text_color: "Custom"
                                    text_color: "#1E40AF"
                                    font_size: "32sp"
                                    halign: "center"
                                    size_hint_y: None
                                    height: dp(40)
                                MDLabel:
                                    text: "8\\nAppointments"
                                    font_style: "H6"
                                    bold: True
                                    theme_text_color: "Custom"
                                    text_color: "#1E293B"
                                    halign: "center"
                                    size_hint_y: None
                                    height: dp(40)
                            
                            MDCard:
                                orientation: "vertical"
                                md_bg_color: "#FFFFFF"
                                elevation: 4
                                radius: [15, 15, 15, 15]
                                padding: dp(20)
                                spacing: dp(8)
                                MDIcon:
                                    icon: "message-text"
                                    theme_text_color: "Custom"
                                    text_color: "#D97706"
                                    font_size: "32sp"
                                    halign: "center"
                                    size_hint_y: None
                                    height: dp(40)
                                MDLabel:
                                    text: "5\\nNew Feedback"
                                    font_style: "H6"
                                    bold: True
                                    theme_text_color: "Custom"
                                    text_color: "#1E293B"
                                    halign: "center"
                                    size_hint_y: None
                                    height: dp(40)
                            
                            MDCard:
                                orientation: "vertical"
                                md_bg_color: "#FFFFFF"
                                elevation: 4
                                radius: [15, 15, 15, 15]
                                padding: dp(20)
                                spacing: dp(8)
                                MDIcon:
                                    icon: "pill"
                                    theme_text_color: "Custom"
                                    text_color: "#059669"
                                    font_size: "32sp"
                                    halign: "center"
                                    size_hint_y: None
                                    height: dp(40)
                                MDLabel:
                                    text: "24\\nPrescriptions"
                                    font_style: "H6"
                                    bold: True
                                    theme_text_color: "Custom"
                                    text_color: "#1E293B"
                                    halign: "center"
                                    size_hint_y: None
                                    height: dp(40)
                        
                        # Action Buttons
                        MDLabel:
                            text: "Quick Actions"
                            font_style: "H6"
                            theme_text_color: "Custom"
                            text_color: "#1E293B"
                            bold: True
                            size_hint_y: None
                            height: dp(30)
                        
                        MDCard:
                            orientation: "horizontal"
                            md_bg_color: "#FFFFFF"
                            elevation: 6
                            radius: [15, 15, 15, 15]
                            padding: dp(25)
                            spacing: dp(20)
                            ripple_behavior: True
                            size_hint_y: None
                            height: dp(70)
                            MDIcon:
                                icon: "message-reply-text"
                                theme_text_color: "Custom"
                                text_color: "#D97706"
                                size_hint_x: None
                                width: dp(40)
                            MDLabel:
                                text: "View Patient Feedback"
                                font_style: "H6"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: "#1E293B"
                                valign: "center"
                        
                        MDCard:
                            orientation: "horizontal"
                            md_bg_color: "#FFFFFF"
                            elevation: 6
                            radius: [15, 15, 15, 15]
                            padding: dp(25)
                            spacing: dp(20)
                            ripple_behavior: True
                            size_hint_y: None
                            height: dp(70)
                            MDIcon:
                                icon: "calendar-clock"
                                theme_text_color: "Custom"
                                text_color: "#1E40AF"
                                size_hint_x: None
                                width: dp(40)
                            MDLabel:
                                text: "Manage Appointments"
                                font_style: "H6"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: "#1E293B"
                                valign: "center"
                        
                        MDCard:
                            orientation: "horizontal"
                            md_bg_color: "#FFFFFF"
                            elevation: 6
                            radius: [15, 15, 15, 15]
                            padding: dp(25)
                            spacing: dp(20)
                            ripple_behavior: True
                            size_hint_y: None
                            height: dp(70)
                            MDIcon:
                                icon: "medical-bag"
                                theme_text_color: "Custom"
                                text_color: "#059669"
                                size_hint_x: None
                                width: dp(40)
                            MDLabel:
                                text: "Medicine Database"
                                font_style: "H6"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: "#1E293B"
                                valign: "center"

<UserSignupScreen>:
    name: "user_signup"
    RelativeLayout:
        Image:
            source: "background.jpeg"
            allow_stretch: True
            keep_ratio: False
            size: self.parent.size
            pos: self.parent.pos
        MDBoxLayout:
            orientation: "horizontal"
            SideMenu:
            MDBoxLayout:
                orientation: "vertical"
                spacing: dp(20)
                padding: dp(20)
                
                # Header
                MDCard:
                    size_hint_y: None
                    height: dp(100)
                    md_bg_color: "#0F766E"
                    elevation: 6
                    radius: [15, 15, 15, 15]
                    MDBoxLayout:
                        orientation: "vertical"
                        padding: dp(20)
                        spacing: dp(5)
                        MDLabel:
                            text: "Create New Account"
                            font_style: "H5"
                            theme_text_color: "Custom"
                            text_color: "#FFFFFF"
                            bold: True
                            halign: "center"
                            size_hint_y: None
                            height: dp(30)
                        MDLabel:
                            text: "Join our Ayurvedic wellness community"
                            font_style: "Body2"
                            theme_text_color: "Custom"
                            text_color: "#A7F3D0"
                            halign: "center"
                            size_hint_y: None
                            height: dp(20)
                
                ScrollView:
                    MDBoxLayout:
                        orientation: "vertical"
                        size_hint_y: None
                        height: self.minimum_height
                        spacing: dp(18)
                        padding: dp(20)

                        # Name Fields
                        MDBoxLayout:
                            orientation: "horizontal"
                            size_hint_y: None
                            height: dp(56)
                            spacing: dp(20)
                            MDTextField:
                                id: signup_first_name
                                hint_text: "First Name"
                                mode: "fill"
                                size_hint_x: 0.5
                                helper_text: "2-50 characters"
                                helper_text_mode: "on_focus"
                                on_text: app.validate_signup_name_field(self, "first")
                            MDTextField:
                                id: signup_last_name
                                hint_text: "Last Name"
                                mode: "fill"
                                size_hint_x: 0.5
                                helper_text: "2-50 characters"
                                helper_text_mode: "on_focus"
                                on_text: app.validate_signup_name_field(self, "last")

                        MDTextField:
                            id: signup_email
                            hint_text: "Email Address"
                            mode: "fill"
                            size_hint_y: None
                            height: dp(56)
                            helper_text: "example@domain.com"
                            helper_text_mode: "on_focus"
                            on_text: app.validate_signup_email_field(self)

                        MDTextField:
                            id: signup_phone
                            hint_text: "Phone Number"
                            mode: "fill"
                            input_filter: "int"
                            max_text_length: 10
                            size_hint_y: None
                            height: dp(56)
                            helper_text: "Enter 10 digits"
                            helper_text_mode: "on_focus"
                            on_text: app.validate_signup_phone_field(self)

                        MDTextField:
                            id: signup_department
                            hint_text: "Department/Organization"
                            mode: "fill"
                            size_hint_y: None
                            height: dp(56)
                            helper_text: "Minimum 2 characters"
                            helper_text_mode: "on_focus"

                        # Gender Selection
                        MDLabel:
                            text: "Gender"
                            font_style: "Subtitle1"
                            theme_text_color: "Custom"
                            text_color: "#374151"
                            size_hint_y: None
                            height: dp(24)

                        MDBoxLayout:
                            orientation: "horizontal"
                            size_hint_y: None
                            height: dp(40)
                            spacing: dp(32)
                            MDBoxLayout:
                                orientation: "horizontal"
                                size_hint: None, None
                                size: dp(90), dp(40)
                                spacing: dp(12)
                                MDCheckbox:
                                    id: signup_male
                                    group: "signup_gender"
                                    size_hint: None, None
                                    size: dp(28), dp(28)
                                    pos_hint: {"center_y": 0.5}
                                    on_active: if self.active: app.set_signup_gender("Male")
                                MDLabel:
                                    text: "Male"
                                    font_style: "Body1"
                                    theme_text_color: "Custom"
                                    text_color: "#374151"
                                    valign: "center"
                            MDBoxLayout:
                                orientation: "horizontal"
                                size_hint: None, None
                                size: dp(110), dp(40)
                                spacing: dp(12)
                                MDCheckbox:
                                    id: signup_female
                                    group: "signup_gender"
                                    size_hint: None, None
                                    size: dp(28), dp(28)
                                    pos_hint: {"center_y": 0.5}
                                    on_active: if self.active: app.set_signup_gender("Female")
                                MDLabel:
                                    text: "Female"
                                    font_style: "Body1"
                                    theme_text_color: "Custom"
                                    text_color: "#374151"
                                    valign: "center"
                            MDBoxLayout:
                                orientation: "horizontal"
                                size_hint: None, None
                                size: dp(100), dp(40)
                                spacing: dp(12)
                                MDCheckbox:
                                    id: signup_other
                                    group: "signup_gender"
                                    size_hint: None, None
                                    size: dp(28), dp(28)
                                    pos_hint: {"center_y": 0.5}
                                    on_active: if self.active: app.set_signup_gender("Other")
                                MDLabel:
                                    text: "Other"
                                    font_style: "Body1"
                                    theme_text_color: "Custom"
                                    text_color: "#374151"
                                    valign: "center"

                        # Password Fields
                        MDBoxLayout:
                            orientation: "horizontal"
                            size_hint_y: None
                            height: dp(56)
                            spacing: 0
                            MDTextField:
                                id: signup_password
                                hint_text: "Password"
                                mode: "fill"
                                password: True
                                helper_text: "8+ chars, uppercase, lowercase, number, special char"
                                helper_text_mode: "on_focus"
                                size_hint_x: 1
                                on_text: app.validate_signup_password_field(self)
                            MDIconButton:
                                id: signup_password_eye
                                icon: "eye-off"
                                theme_text_color: "Custom"
                                text_color: "#64748B"
                                size_hint: None, None
                                size: dp(48), dp(48)
                                pos_hint: {"center_y": 0.5}
                                on_release: app.toggle_signup_password_visibility()

                        MDBoxLayout:
                            orientation: "horizontal"
                            size_hint_y: None
                            height: dp(56)
                            spacing: 0
                            MDTextField:
                                id: signup_confirm_password
                                hint_text: "Confirm Password"
                                mode: "fill"
                                password: True
                                helper_text: "Must match password above"
                                helper_text_mode: "on_focus"
                                size_hint_x: 1
                                on_text: app.validate_signup_confirm_password_field(self)
                            MDIconButton:
                                id: signup_confirm_password_eye
                                icon: "eye-off"
                                theme_text_color: "Custom"
                                text_color: "#64748B"
                                size_hint: None, None
                                size: dp(48), dp(48)
                                pos_hint: {"center_y": 0.5}
                                on_release: app.toggle_signup_confirm_password_visibility()

                        # Blood Group
                        MDBoxLayout:
                            orientation: "horizontal"
                            size_hint_y: None
                            height: dp(56)
                            spacing: dp(20)
                            MDLabel:
                                text: "Blood Group:"
                                font_style: "Subtitle1"
                                theme_text_color: "Custom"
                                text_color: "#374151"
                                size_hint_x: 0.35
                                valign: "center"
                            MDRaisedButton:
                                id: signup_blood_group_btn
                                text: "Select Blood Group"
                                md_bg_color: "#0F766E"
                                theme_text_color: "Custom"
                                text_color: "#FFFFFF"
                                size_hint_x: 0.65
                                size_hint_y: None
                                height: dp(48)
                                elevation: 2
                                on_release: app.open_signup_blood_group_menu()

                        # Captcha
                        MDLabel:
                            text: "Security Verification"
                            font_style: "Subtitle1"
                            theme_text_color: "Custom"
                            text_color: "#374151"
                            size_hint_y: None
                            height: dp(24)

                        MDBoxLayout:
                            orientation: "horizontal"
                            size_hint_y: None
                            height: dp(44)
                            spacing: dp(16)
                            MDLabel:
                                id: signup_captcha_question
                                text: "5 + 3 = ?"
                                font_style: "Subtitle1"
                                theme_text_color: "Custom"
                                text_color: "#0F766E"
                                bold: True
                                size_hint_x: 0.3
                                valign: "center"
                                halign: "center"
                                canvas.before:
                                    Color:
                                        rgba: 0.94, 0.97, 0.99, 1
                                    RoundedRectangle:
                                        pos: self.pos
                                        size: self.size
                                        radius: [8]
                            MDTextField:
                                id: signup_captcha_answer
                                hint_text: "Enter answer"
                                mode: "fill"
                                input_filter: "int"
                                size_hint_x: 0.5
                                max_text_length: 3
                                on_text: app.validate_signup_captcha_field(self)
                            MDIconButton:
                                icon: "refresh"
                                theme_text_color: "Custom"
                                text_color: "#0F766E"
                                size_hint: None, None
                                size: dp(40), dp(40)
                                on_release: app.refresh_signup_captcha()

                        # Action Buttons
                        MDRaisedButton:
                            text: "CREATE ACCOUNT"
                            md_bg_color: "#0F766E"
                            theme_text_color: "Custom"
                            text_color: "#FFFFFF"
                            size_hint_y: None
                            height: dp(48)
                            elevation: 6
                            on_release: app.handle_user_registration()

<StaffRegistrationScreen>:
    name: "staff_registration"
    RelativeLayout:
        Image:
            source: "background.jpeg"
            allow_stretch: True
            keep_ratio: False
            size: self.parent.size
            pos: self.parent.pos
        MDBoxLayout:
            orientation: "horizontal"
            SideMenu:
            MDBoxLayout:
                orientation: "vertical"
                spacing: dp(20)
                padding: dp(20)
                
                # Header
                MDCard:
                    size_hint_y: None
                    height: dp(120)
                    md_bg_color: "#2563EB"
                    elevation: 6
                    radius: [15, 15, 15, 15]
                    MDBoxLayout:
                        orientation: "vertical"
                        padding: dp(20)
                        spacing: dp(8)
                        MDLabel:
                            text: "Staff Registration System"
                            font_style: "H5"
                            theme_text_color: "Custom"
                            text_color: "#FFFFFF"
                            bold: True
                            halign: "center"
                            size_hint_y: None
                            height: dp(30)
                        MDLabel:
                            text: "Register administrators and doctors"
                            font_style: "Body2"
                            theme_text_color: "Custom"
                            text_color: "#DBEAFE"
                            halign: "center"
                            size_hint_y: None
                            height: dp(18)
                        MDBoxLayout:
                            orientation: "horizontal"
                            size_hint_y: None
                            height: dp(35)
                            spacing: dp(10)
                            pos_hint: {"center_x": 0.5}
                            size_hint_x: 0.6
                            MDRaisedButton:
                                id: staff_admin_toggle_btn
                                text: "ðŸ‘¤ ADMIN"
                                md_bg_color: "#DC2626"
                                theme_text_color: "Custom"
                                text_color: "#FFFFFF"
                                size_hint_x: 0.5
                                elevation: 4
                                font_size: "13sp"
                                on_release: app.show_admin_registration_form()
                            MDRaisedButton:
                                id: staff_doctor_toggle_btn
                                text: "ðŸ©º DOCTOR"
                                md_bg_color: "#64748B"
                                theme_text_color: "Custom"
                                text_color: "#FFFFFF"
                                size_hint_x: 0.5
                                elevation: 2
                                font_size: "13sp"
                                on_release: app.show_doctor_registration_form()
                
                ScrollView:
                    MDBoxLayout:
                        id: staff_registration_content
                        orientation: "vertical"
                        size_hint_y: None
                        height: self.minimum_height
                        spacing: dp(15)
                        padding: dp(20)
                        
                        MDLabel:
                            text: "Select registration type above to begin"
                            font_style: "H6"
                            theme_text_color: "Custom"
                            text_color: "#64748B"
                            halign: "center"
                            size_hint_y: None
                            height: dp(200)

<AdminPanelScreen>:
    name: "admin_panel"
    RelativeLayout:
        Image:
            source: "background.jpeg"
            allow_stretch: True
            keep_ratio: False
            size: self.parent.size
            pos: self.parent.pos
        MDBoxLayout:
            orientation: "horizontal"
            SideMenu:
            MDBoxLayout:
                orientation: "vertical"
                spacing: dp(20)
                padding: dp(20)
                
                # Header
                MDCard:
                    size_hint_y: None
                    height: dp(100)
                    md_bg_color: "#DC2626"
                    elevation: 6
                    radius: [15, 15, 15, 15]
                    MDBoxLayout:
                        orientation: "horizontal"
                        padding: dp(20)
                        spacing: dp(15)
                        MDIcon:
                            icon: "shield-account"
                            theme_text_color: "Custom"
                            text_color: "#FFFFFF"
                            font_size: "48sp"
                            size_hint_x: None
                            width: dp(60)
                        MDBoxLayout:
                            orientation: "vertical"
                            spacing: dp(5)
                            MDLabel:
                                text: "Administrator Control Panel"
                                font_style: "H5"
                                theme_text_color: "Custom"
                                text_color: "#FFFFFF"
                                bold: True
                                size_hint_y: None
                                height: dp(30)
                            MDLabel:
                                text: "Secure administrative access"
                                font_style: "Body2"
                                theme_text_color: "Custom"
                                text_color: "#FECACA"
                                size_hint_y: None
                                height: dp(20)
                
                ScrollView:
                    MDBoxLayout:
                        orientation: "vertical"
                        size_hint_y: None
                        height: self.minimum_height
                        spacing: dp(20)
                        padding: dp(20)
                        
                        # Security Warning
                        MDCard:
                            orientation: "horizontal"
                            size_hint_y: None
                            height: dp(60)
                            padding: dp(20)
                            md_bg_color: "#FEF3C7"
                            radius: [10, 10, 10, 10]
                            elevation: 2
                            MDIcon:
                                icon: "alert"
                                theme_text_color: "Custom"
                                text_color: "#D97706"
                                size_hint_x: None
                                width: dp(40)
                            MDLabel:
                                text: "Only authorized administrators are allowed to access this panel"
                                font_style: "Body2"
                                theme_text_color: "Custom"
                                text_color: "#92400E"
                                bold: True
                                valign: "center"
                        
                        # Login Form
                        MDTextField:
                            id: admin_email
                            hint_text: "Admin Email Address"
                            mode: "fill"
                            size_hint_y: None
                            height: dp(56)
                            helper_text: "Enter your administrative email"
                            helper_text_mode: "on_focus"

                        MDTextField:
                            id: admin_role
                            hint_text: "Admin Role/Department"
                            mode: "fill"
                            size_hint_y: None
                            height: dp(56)
                            helper_text: "e.g., Super Admin, IT Admin, Medical Admin"
                            helper_text_mode: "on_focus"

                        MDBoxLayout:
                            orientation: "horizontal"
                            size_hint_y: None
                            height: dp(56)
                            spacing: 0
                            MDTextField:
                                id: admin_password
                                hint_text: "Admin Password"
                                mode: "fill"
                                password: True
                                helper_text: "Enter your secure admin password"
                                helper_text_mode: "on_focus"
                                size_hint_x: 1
                            MDIconButton:
                                id: admin_password_eye
                                icon: "eye-off"
                                theme_text_color: "Custom"
                                text_color: "#64748B"
                                size_hint: None, None
                                size: dp(48), dp(48)
                                pos_hint: {"center_y": 0.5}
                                on_release: app.toggle_admin_password_visibility()

                        # Captcha
                        MDBoxLayout:
                            orientation: "horizontal"
                            size_hint_y: None
                            height: dp(44)
                            spacing: dp(16)
                            MDLabel:
                                id: admin_captcha_question
                                text: "5 + 3 = ?"
                                font_style: "Subtitle1"
                                theme_text_color: "Custom"
                                text_color: "#DC2626"
                                bold: True
                                size_hint_x: 0.3
                                valign: "center"
                                halign: "center"
                                canvas.before:
                                    Color:
                                        rgba: 0.96, 0.95, 0.99, 1
                                    RoundedRectangle:
                                        pos: self.pos
                                        size: self.size
                                        radius: [6]
                            MDTextField:
                                id: admin_captcha_answer
                                hint_text: "Enter answer"
                                mode: "fill"
                                input_filter: "int"
                                size_hint_x: 0.5
                                max_text_length: 3
                            MDIconButton:
                                icon: "refresh"
                                theme_text_color: "Custom"
                                text_color: "#DC2626"
                                size_hint: None, None
                                size: dp(40), dp(40)
                                on_release: app.refresh_admin_captcha()

                        MDRaisedButton:
                            text: "ADMIN LOGIN"
                            md_bg_color: "#DC2626"
                            theme_text_color: "Custom"
                            text_color: "#FFFFFF"
                            size_hint_y: None
                            height: dp(48)
                            elevation: 6
                            on_release: app.handle_admin_login()
                        
                        # Additional Info
                        MDCard:
                            orientation: "vertical"
                            size_hint_y: None
                            height: dp(120)
                            padding: dp(16)
                            md_bg_color: "#F8FAFC"
                            elevation: 0
                            radius: [8, 8, 8, 8]
                            MDLabel:
                                text: "ðŸ›¡ï¸ Security Features"
                                font_style: "Subtitle2"
                                theme_text_color: "Custom"
                                text_color: "#1E293B"
                                bold: True
                                halign: "center"
                                size_hint_y: None
                                height: dp(25)
                            MDLabel:
                                text: "â€¢ Multi-factor Authentication\\nâ€¢ Encrypted Data Transmission\\nâ€¢ Session Management\\nâ€¢ Audit Logging"
                                font_style: "Caption"
                                theme_text_color: "Custom"
                                text_color: "#475569"
                                halign: "center"
                                size_hint_y: None
                                height: dp(60)
                        
                        MDLabel:
                            text: "ðŸŸ¢ System Status: Online â€¢ Secure Connection"
                            font_style: "Caption"
                            theme_text_color: "Custom"
                            text_color: "#059669"
                            halign: "center"
                            size_hint_y: None
                            height: dp(20)
"""

# ------------------ App -------------------
class HexVeda(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None
        self.gender_menu = None
        self.date_menu = None
        
        # Signup form variables
        self.signup_gender = Gender.UNSPECIFIED
        self.blood_groups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
        self.signup_menu = None
        self.signup_password_visible = False
        self.signup_confirm_password_visible = False
        self.signup_captcha_num1 = 0
        self.signup_captcha_num2 = 0
        self.signup_captcha_answer = 0
        
        # Admin panel variables
        self.admin_password_visible = False
        self.admin_captcha_num1 = 0
        self.admin_captcha_num2 = 0
        self.admin_captcha_answer = 0
        
        # Staff registration variables
        self.current_staff_form = "none"

    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"
        Window.set_icon("icon.jpeg")

        # Generate initial captchas
        self.generate_signup_captcha()
        self.generate_admin_captcha()

        self.departments = {
            "Ayurveda": ["Dr. Sharma - Senior Consultant", "Dr. Patel - Panchakarma Specialist"],
            "Physiotherapy": ["Dr. Mehta - Chief Physiotherapist"],
            "Nutrition": ["Dr. Reddy - Clinical Nutritionist"],
            "Yoga": ["Dr. Kapoor - Yoga Therapy Expert"],
        }
        # Enhanced doctor information
        self.doctor_info = {
            "Dr. Sharma": {
                "contact": "+91-9000000001", 
                "email": "sharma@panchakarma.com",
                "specialization": "Ayurveda & Panchakarma",
                "experience": "15+ years",
                "education": "BAMS, MD (Ayurveda)"
            },
            "Dr. Mehta": {
                "contact": "+91-9000000002", 
                "email": "mehta@panchakarma.com",
                "specialization": "Physiotherapy & Rehabilitation",
                "experience": "12+ years",
                "education": "BPT, MPT"
            },
            "Dr. Reddy": {
                "contact": "+91-9000000003", 
                "email": "reddy@panchakarma.com",
                "specialization": "Clinical Nutrition",
                "experience": "10+ years",
                "education": "MSc Nutrition, PhD"
            },
            "Dr. Kapoor": {
                "contact": "+91-9000000004", 
                "email": "kapoor@panchakarma.com",
                "specialization": "Yoga Therapy",
                "experience": "8+ years",
                "education": "Certified Yoga Instructor"
            },
            "Dr. Patel": {
                "contact": "+91-9000000005", 
                "email": "patel@panchakarma.com",
                "specialization": "Panchakarma Treatments",
                "experience": "18+ years",
                "education": "BAMS, Panchakarma Specialist"
            },
        }

        return Builder.load_string(KV)

    def show_department_doctors(self, department_name):
        """Show enhanced department information"""
        doctors = self.departments.get(department_name, [])
        if doctors:
            doctors_list = "\n".join([f"• {doctor}" for doctor in doctors])
            text = f"Our {department_name} Department offers comprehensive care with:\n\n{doctors_list}\n\nClick on individual doctors in the specialists section for detailed contact information."
        else:
            text = "No doctors found for this department."

        if self.dialog:
            self.dialog.dismiss()

        self.dialog = MDDialog(
            title=f"{department_name} Department",
            text=text,
            buttons=[
                MDFlatButton(
                    text="CLOSE", 
                    theme_text_color="Custom",
                    text_color="#1E40AF",
                    on_release=lambda x: self.dialog.dismiss()
                )
            ],
        )
        self.dialog.open()

    def show_doctor_info(self, doctor_name):
        """Show enhanced doctor information"""
        info = self.doctor_info.get(doctor_name)
        if info:
            text = f"""{info['specialization']}

Education: {info['education']}
Experience: {info['experience']}

Contact: {info['contact']}
Email: {info['email']}

Available for consultations and appointments."""
        else:
            text = "No information available for this doctor."

        if self.dialog:
            self.dialog.dismiss()

        self.dialog = MDDialog(
            title=f"Dr. Profile - {doctor_name}",
            text=text,
            buttons=[
                MDFlatButton(
                    text="BOOK APPOINTMENT", 
                    theme_text_color="Custom",
                    text_color="#059669",
                    on_release=lambda x: self.dialog.dismiss()
                ),
                MDFlatButton(
                    text="CLOSE", 
                    theme_text_color="Custom",
                    text_color="#64748B",
                    on_release=lambda x: self.dialog.dismiss()
                )
            ],
        )
        self.dialog.open()

    def view_all_doctors(self):
        """Show all doctors in a dialog"""
        doctors_text = "Complete list of our medical specialists:\n\n"

        for doctor, info in self.doctor_info.items():
            doctors_text += f"{doctor}\n"
            doctors_text += f"   Specialization: {info['specialization']}\n"
            doctors_text += f"   Experience: {info['experience']}\n"
            doctors_text += f"   Contact: {info['contact']}\n\n"

        if self.dialog:
            self.dialog.dismiss()

        self.dialog = MDDialog(
            title="All Our Specialists",
            text=doctors_text,
            buttons=[
                MDFlatButton(
                    text="CLOSE", 
                    theme_text_color="Custom",
                    text_color="#1E40AF",
                    on_release=lambda x: self.dialog.dismiss()
                )
            ],
        )
        self.dialog.open()

    def send_feedback(self):
        """Handle enhanced feedback submission"""
        try:
            message = self.root.ids.feedback_box.text.strip()
            if message:
                print(f"Feedback received: {message}")
                self.root.ids.feedback_box.text = ""

                # Show success dialog
                if self.dialog:
                    self.dialog.dismiss()

                self.dialog = MDDialog(
                    title="Thank You!",
                    text="Your feedback has been received successfully. We appreciate your input and will use it to improve our services.",
                    buttons=[
                        MDFlatButton(
                            text="OK", 
                            theme_text_color="Custom",
                            text_color="#059669",
                            on_release=lambda x: self.dialog.dismiss()
                        )
                    ],
                )
                self.dialog.open()
            else:
                # Show error for empty feedback
                if self.dialog:
                    self.dialog.dismiss()

                self.dialog = MDDialog(
                    title="Empty Feedback",
                    text="Please enter your feedback message before sending.",
                    buttons=[
                        MDFlatButton(
                            text="OK", 
                            theme_text_color="Custom",
                            text_color="#DC2626",
                            on_release=lambda x: self.dialog.dismiss()
                        )
                    ],
                )
                self.dialog.open()
        except Exception as e:
            print(f"Error sending feedback: {e}")

    def change_screen(self, screen_name):
        """Navigate between screens with smooth transitions"""
        sm = self.root
        sm.transition = SlideTransition(direction="right")
        sm.current = screen_name

    # ============== APPOINTMENT BOOKING METHODS ==============
    def show_date_dropdown(self, textfield):
        """Open date picker for appointment"""
        try:
            date_dialog = MDDatePicker()
            date_dialog.bind(on_save=lambda x, date_obj, date_range: self.get_date(date_obj, textfield))
            date_dialog.open()
        except Exception as e:
            print(f"Error opening date picker: {e}")

    def get_date(self, date_obj, textfield):
        """Handle selected date"""
        try:
            formatted_date = date_obj.strftime("%d/%m/%Y")
            textfield.text = formatted_date
        except Exception as e:
            print(f"Error setting date: {e}")

    def show_gender_menu(self, textfield):
        """Open gender selection menu"""
        try:
            gender_items = [
                {"text": "Male", "viewclass": "OneLineListItem", "on_release": lambda x="Male": self.set_gender(x, textfield)},
                {"text": "Female", "viewclass": "OneLineListItem", "on_release": lambda x="Female": self.set_gender(x, textfield)},
                {"text": "Other", "viewclass": "OneLineListItem", "on_release": lambda x="Other": self.set_gender(x, textfield)},
            ]
            self.gender_menu = MDDropdownMenu(caller=textfield, items=gender_items, width_mult=4)
            self.gender_menu.open()
        except Exception as e:
            print(f"Error opening gender menu: {e}")

    def set_gender(self, gender_text, textfield):
        """Set selected gender"""
        try:
            textfield.text = gender_text
            if self.gender_menu:
                self.gender_menu.dismiss()
        except Exception as e:
            print(f"Error setting gender: {e}")

    def submit_appointment(self):
        """Handle appointment submission"""
        try:
            # Get appointment screen
            screen = self.root.get_screen('appointment')
            
            # Collect form data
            data = {
                'first_name': screen.ids.first_name.text.strip(),
                'last_name': screen.ids.last_name.text.strip(),
                'email': screen.ids.email.text.strip(),
                'mobile': screen.ids.mobile.text.strip(),
                'dob': screen.ids.dob.text.strip(),
                'gender': screen.ids.gender.text.strip(),
                'app_date': screen.ids.app_date.text.strip(),
                'doctor': screen.ids.doctor.text.strip(),
                'issue_type': screen.ids.issue_type.text.strip(),
                'address': screen.ids.address.text.strip(),
            }
            
            # Basic validation
            required_fields = ['first_name', 'last_name', 'email', 'mobile', 'app_date', 'issue_type']
            missing = [field for field in required_fields if not data[field]]
            
            if missing:
                self.show_dialog("Missing Information", f"Please fill in: {', '.join(missing)}")
                return
            
            # Format confirmation message
            confirmation_message = f"""
Appointment Details:

Name: {data['first_name']} {data['last_name']}
Email: {data['email']}
Phone: {data['mobile']}
Date of Birth: {data['dob'] or 'Not provided'}
Gender: {data['gender'] or 'Not specified'}
Appointment Date: {data['app_date']}
Preferred Doctor: {data['doctor'] or 'Any available'}
Chief Complaint: {data['issue_type']}
Address: {data['address'] or 'Not provided'}

Your appointment has been scheduled successfully!
You will receive a confirmation call within 24 hours.
            """.strip()
            
            # Update confirmation screen and navigate
            confirm_screen = self.root.get_screen('confirmation')
            confirm_screen.message = confirmation_message
            self.change_screen('confirmation')
            
        except Exception as e:
            print(f"Error submitting appointment: {e}")
            self.show_dialog("Error", "Failed to submit appointment. Please try again.")

    def clear_appointment_form(self):
        """Clear appointment form"""
        try:
            screen = self.root.get_screen('appointment')
            fields = ['first_name', 'last_name', 'email', 'mobile', 'dob', 'gender', 'app_date', 'doctor', 'issue_type', 'address']
            for field in fields:
                screen.ids[field].text = ""
        except Exception as e:
            print(f"Error clearing form: {e}")

    # ============== USER SIGNUP METHODS ==============
    def generate_signup_captcha(self):
        """Generate captcha for signup"""
        self.signup_captcha_num1 = random.randint(1, 9)
        self.signup_captcha_num2 = random.randint(1, 9)
        self.signup_captcha_answer = self.signup_captcha_num1 + self.signup_captcha_num2
        try:
            Clock.schedule_once(lambda dt: self.update_signup_captcha_display(), 0.1)
        except:
            pass

    def update_signup_captcha_display(self):
        """Update signup captcha display"""
        try:
            screen = self.root.get_screen('user_signup')
            screen.ids.signup_captcha_question.text = f"{self.signup_captcha_num1} + {self.signup_captcha_num2} = ?"
            screen.ids.signup_captcha_answer.text = ""
        except:
            pass

    def refresh_signup_captcha(self):
        """Refresh signup captcha"""
        self.generate_signup_captcha()

    def validate_signup_name_field(self, field, name_type):
        """Validate name fields in signup"""
        try:
            text = field.text.strip() if field.text else ""
            if not text:
                field.error = False
                field.helper_text_mode = "on_focus"
                return
            if len(text) < 2:
                field.error = True
                field.helper_text = f"{name_type.capitalize()} name must be at least 2 characters"
                field.helper_text_mode = "on_error"
            elif not re.match(r"^[a-zA-Z\s'-]+$", text):
                field.error = True
                field.helper_text = "Only letters, spaces, hyphens and apostrophes allowed"
                field.helper_text_mode = "on_error"
            else:
                field.error = False
                field.helper_text = "Valid name"
                field.helper_text_mode = "persistent"
        except Exception as e:
            print(f"Error validating name: {e}")

    def validate_signup_email_field(self, field):
        """Validate email in signup"""
        try:
            email = field.text.strip() if field.text else ""
            if not email:
                field.error = False
                field.helper_text_mode = "on_focus"
                return
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                field.error = True
                field.helper_text = "Enter a valid email address"
                field.helper_text_mode = "on_error"
            else:
                field.error = False
                field.helper_text = "Valid email"
                field.helper_text_mode = "persistent"
        except Exception as e:
            print(f"Error validating email: {e}")

    def validate_signup_phone_field(self, field):
        """Validate phone in signup"""
        try:
            phone = field.text.strip() if field.text else ""
            if not phone:
                field.error = False
                field.helper_text_mode = "on_focus"
                return
            if len(phone) < 10:
                field.error = True
                field.helper_text = f"Need {10 - len(phone)} more digits"
                field.helper_text_mode = "on_error"
            elif len(phone) == 10:
                field.error = False
                field.helper_text = "Valid phone number"
                field.helper_text_mode = "persistent"
        except Exception as e:
            print(f"Error validating phone: {e}")

    def validate_signup_password_field(self, field):
        """Validate password in signup"""
        try:
            password = field.text if field.text else ""
            if not password:
                field.error = False
                field.helper_text_mode = "on_focus"
                return
            errors = []
            if len(password) < 8:
                errors.append("8+ characters")
            if not re.search(r'[A-Z]', password):
                errors.append("uppercase letter")
            if not re.search(r'[a-z]', password):
                errors.append("lowercase letter")
            if not re.search(r'\d', password):
                errors.append("number")
            if not re.search(r'[@$!%*?&]', password):
                errors.append("special character")
            
            if errors:
                field.error = True
                field.helper_text = f"Need: {', '.join(errors)}"
                field.helper_text_mode = "on_error"
            else:
                field.error = False
                field.helper_text = "Strong password"
                field.helper_text_mode = "persistent"
        except Exception as e:
            print(f"Error validating password: {e}")

    def validate_signup_confirm_password_field(self, field):
        """Validate confirm password in signup"""
        try:
            confirm_password = field.text if field.text else ""
            screen = self.root.get_screen('user_signup')
            password = screen.ids.signup_password.text if screen.ids.signup_password.text else ""
            
            if not confirm_password:
                field.error = False
                field.helper_text_mode = "on_focus"
                return
            if confirm_password != password:
                field.error = True
                field.helper_text = "Passwords do not match"
                field.helper_text_mode = "on_error"
            else:
                field.error = False
                field.helper_text = "Passwords match"
                field.helper_text_mode = "persistent"
        except Exception as e:
            print(f"Error validating confirm password: {e}")

    def validate_signup_captcha_field(self, field):
        """Validate captcha in signup"""
        try:
            answer = field.text.strip() if field.text else ""
            if not answer:
                field.error = False
                field.helper_text_mode = "on_focus"
                return
            try:
                if int(answer) == self.signup_captcha_answer:
                    field.error = False
                    field.helper_text = "Correct"
                    field.helper_text_mode = "persistent"
                else:
                    field.error = True
                    field.helper_text = "Incorrect answer"
                    field.helper_text_mode = "on_error"
            except ValueError:
                field.error = True
                field.helper_text = "Enter a number"
                field.helper_text_mode = "on_error"
        except Exception as e:
            print(f"Error validating captcha: {e}")

    def toggle_signup_password_visibility(self):
        """Toggle password visibility in signup"""
        try:
            screen = self.root.get_screen('user_signup')
            password_field = screen.ids.signup_password
            eye_icon = screen.ids.signup_password_eye
            
            if self.signup_password_visible:
                password_field.password = True
                eye_icon.icon = "eye-off"
                self.signup_password_visible = False
            else:
                password_field.password = False
                eye_icon.icon = "eye"
                self.signup_password_visible = True
        except Exception as e:
            print(f"Error toggling password visibility: {e}")

    def toggle_signup_confirm_password_visibility(self):
        """Toggle confirm password visibility in signup"""
        try:
            screen = self.root.get_screen('user_signup')
            password_field = screen.ids.signup_confirm_password
            eye_icon = screen.ids.signup_confirm_password_eye
            
            if self.signup_confirm_password_visible:
                password_field.password = True
                eye_icon.icon = "eye-off"
                self.signup_confirm_password_visible = False
            else:
                password_field.password = False
                eye_icon.icon = "eye"
                self.signup_confirm_password_visible = True
        except Exception as e:
            print(f"Error toggling confirm password visibility: {e}")

    def set_signup_gender(self, gender):
        """Set gender in signup"""
        try:
            self.signup_gender = Gender(gender)
        except ValueError:
            self.signup_gender = Gender.UNSPECIFIED

    def open_signup_blood_group_menu(self):
        """Open blood group menu in signup"""
        try:
            screen = self.root.get_screen('user_signup')
            btn = screen.ids.signup_blood_group_btn
            menu_items = [
                {"text": bg, "on_release": lambda x=bg: self.set_signup_blood_group(x)}
                for bg in self.blood_groups
            ]
            if self.signup_menu:
                self.signup_menu.dismiss()
            self.signup_menu = MDDropdownMenu(caller=btn, items=menu_items, width_mult=4)
            self.signup_menu.open()
        except Exception as e:
            print(f"Error opening blood group menu: {e}")

    def set_signup_blood_group(self, bg):
        """Set blood group in signup"""
        try:
            screen = self.root.get_screen('user_signup')
            btn = screen.ids.signup_blood_group_btn
            btn.text = bg
            if self.signup_menu:
                self.signup_menu.dismiss()
                self.signup_menu = None
        except Exception as e:
            print(f"Error setting blood group: {e}")

    def handle_user_registration(self):
        """Handle user registration"""
        try:
            screen = self.root.get_screen('user_signup')
            
            # Collect data
            data = {
                'first_name': screen.ids.signup_first_name.text.strip(),
                'last_name': screen.ids.signup_last_name.text.strip(),
                'email': screen.ids.signup_email.text.strip(),
                'phone': screen.ids.signup_phone.text.strip(),
                'department': screen.ids.signup_department.text.strip(),
                'password': screen.ids.signup_password.text,
                'confirm_password': screen.ids.signup_confirm_password.text,
                'blood_group': screen.ids.signup_blood_group_btn.text,
                'captcha_answer': screen.ids.signup_captcha_answer.text.strip(),
            }
            
            # Validation
            if not all([data['first_name'], data['last_name'], data['email'], data['phone'], data['department'], data['password']]):
                self.show_dialog("Incomplete Form", "Please fill in all required fields")
                return
            
            if data['password'] != data['confirm_password']:
                self.show_dialog("Password Mismatch", "Passwords do not match")
                return
            
            if data['blood_group'] == "Select Blood Group":
                self.show_dialog("Missing Information", "Please select your blood group")
                return
            
            if self.signup_gender == Gender.UNSPECIFIED:
                self.show_dialog("Missing Information", "Please select your gender")
                return
            
            try:
                if int(data['captcha_answer']) != self.signup_captcha_answer:
                    self.show_dialog("Security Check Failed", "Incorrect captcha answer")
                    self.refresh_signup_captcha()
                    return
            except ValueError:
                self.show_dialog("Security Check Failed", "Please enter a valid number for captcha")
                return
            
            # Success
            print("User registration successful!", data)
            self.show_dialog("Welcome!", f"Account created successfully for {data['first_name']} {data['last_name']}!")
            self.generate_signup_captcha()
            
        except Exception as e:
            print(f"Registration error: {e}")
            self.show_dialog("Error", "Registration failed. Please try again.")

    # ============== STAFF REGISTRATION METHODS ==============
    def show_admin_registration_form(self):
        """Show admin registration form"""
        try:
            screen = self.root.get_screen('staff_registration')
            # Update button states
            screen.ids.staff_admin_toggle_btn.md_bg_color = "#DC2626"
            screen.ids.staff_admin_toggle_btn.elevation = 4
            screen.ids.staff_doctor_toggle_btn.md_bg_color = "#64748B"
            screen.ids.staff_doctor_toggle_btn.elevation = 2
            
            # Clear and populate content
            content = screen.ids.staff_registration_content
            content.clear_widgets()
            
            # Add admin form fields
            content.add_widget(MDLabel(
                text="Administrator Registration",
                font_style="H6",
                theme_text_color="Custom",
                text_color="#DC2626",
                bold=True,
                size_hint_y=None,
                height=dp(40)
            ))
            
            # Add form fields (simplified)
            fields = [
                ("admin_first_name", "First Name*"),
                ("admin_last_name", "Last Name*"),
                ("admin_email", "Email Address*"),
                ("admin_phone", "Phone Number*"),
                ("admin_code", "Admin Code/ID*"),
                ("admin_password", "Password*")
            ]
            
            for field_id, hint in fields:
                field = MDTextField(
                    hint_text=hint,
                    size_hint_y=None,
                    height=dp(56),
                    line_color_focus="#DC2626"
                )
                setattr(field, 'id', field_id)  # Set ID for later reference
                content.add_widget(field)
            
            # Add register button
            register_btn = MDRaisedButton(
                text="REGISTER ADMIN",
                md_bg_color="#DC2626",
                theme_text_color="Custom",
                text_color="#FFFFFF",
                size_hint_y=None,
                height=dp(56),
                elevation=6,
                on_release=lambda x: self.register_staff_admin()
            )
            content.add_widget(register_btn)
            
            self.current_staff_form = "admin"
            
        except Exception as e:
            print(f"Error showing admin form: {e}")

    def show_doctor_registration_form(self):
        """Show doctor registration form"""
        try:
            screen = self.root.get_screen('staff_registration')
            # Update button states
            screen.ids.staff_doctor_toggle_btn.md_bg_color = "#059669"
            screen.ids.staff_doctor_toggle_btn.elevation = 4
            screen.ids.staff_admin_toggle_btn.md_bg_color = "#64748B"
            screen.ids.staff_admin_toggle_btn.elevation = 2
            
            # Clear and populate content
            content = screen.ids.staff_registration_content
            content.clear_widgets()
            
            # Add doctor form fields
            content.add_widget(MDLabel(
                text="Doctor Registration",
                font_style="H6",
                theme_text_color="Custom",
                text_color="#059669",
                bold=True,
                size_hint_y=None,
                height=dp(40)
            ))
            
            # Add form fields (simplified)
            fields = [
                ("doctor_first_name", "First Name*"),
                ("doctor_last_name", "Last Name*"),
                ("doctor_email", "Email Address*"),
                ("doctor_phone", "Phone Number*"),
                ("doctor_department", "Department/Specialization*"),
                ("doctor_code", "Doctor Code/License*"),
                ("doctor_password", "Password*")
            ]
            
            for field_id, hint in fields:
                field = MDTextField(
                    hint_text=hint,
                    size_hint_y=None,
                    height=dp(56),
                    line_color_focus="#059669"
                )
                setattr(field, 'id', field_id)  # Set ID for later reference
                content.add_widget(field)
            
            # Add register button
            register_btn = MDRaisedButton(
                text="REGISTER DOCTOR",
                md_bg_color="#059669",
                theme_text_color="Custom",
                text_color="#FFFFFF",
                size_hint_y=None,
                height=dp(56),
                elevation=6,
                on_release=lambda x: self.register_staff_doctor()
            )
            content.add_widget(register_btn)
            
            self.current_staff_form = "doctor"
            
        except Exception as e:
            print(f"Error showing doctor form: {e}")

    def register_staff_admin(self):
        """Register admin staff"""
        self.show_dialog("Admin Registered", "Admin registration completed successfully!")

    def register_staff_doctor(self):
        """Register doctor staff"""
        self.show_dialog("Doctor Registered", "Doctor registration completed successfully!")

    # ============== ADMIN PANEL METHODS ==============
    def generate_admin_captcha(self):
        """Generate captcha for admin panel"""
        self.admin_captcha_num1 = random.randint(1, 9)
        self.admin_captcha_num2 = random.randint(1, 9)
        self.admin_captcha_answer = self.admin_captcha_num1 + self.admin_captcha_num2
        try:
            Clock.schedule_once(lambda dt: self.update_admin_captcha_display(), 0.1)
        except:
            pass

    def update_admin_captcha_display(self):
        """Update admin captcha display"""
        try:
            screen = self.root.get_screen('admin_panel')
            screen.ids.admin_captcha_question.text = f"{self.admin_captcha_num1} + {self.admin_captcha_num2} = ?"
            screen.ids.admin_captcha_answer.text = ""
        except:
            pass

    def refresh_admin_captcha(self):
        """Refresh admin captcha"""
        self.generate_admin_captcha()

    def toggle_admin_password_visibility(self):
        """Toggle admin password visibility"""
        try:
            screen = self.root.get_screen('admin_panel')
            password_field = screen.ids.admin_password
            eye_icon = screen.ids.admin_password_eye
            
            if self.admin_password_visible:
                password_field.password = True
                eye_icon.icon = "eye-off"
                self.admin_password_visible = False
            else:
                password_field.password = False
                eye_icon.icon = "eye"
                self.admin_password_visible = True
        except Exception as e:
            print(f"Error toggling admin password visibility: {e}")

    def handle_admin_login(self):
        """Handle admin login"""
        try:
            screen = self.root.get_screen('admin_panel')
            
            # Collect data
            email = screen.ids.admin_email.text.strip()
            role = screen.ids.admin_role.text.strip()
            password = screen.ids.admin_password.text
            captcha_answer = screen.ids.admin_captcha_answer.text.strip()
            
            # Basic validation
            if not all([email, role, password, captcha_answer]):
                self.show_dialog("Missing Information", "Please fill in all fields")
                return
            
            # Check captcha
            try:
                if int(captcha_answer) != self.admin_captcha_answer:
                    self.show_dialog("Security Check Failed", "Incorrect captcha answer")
                    self.refresh_admin_captcha()
                    return
            except ValueError:
                self.show_dialog("Security Check Failed", "Please enter a valid number")
                return
            
            # Success (in real app, would verify credentials)
            self.show_dialog("Admin Access Granted", f"Welcome, {role}!\n\nEmail: {email}\nAccess Level: Administrator")
            self.refresh_admin_captcha()
            
        except Exception as e:
            print(f"Admin login error: {e}")
            self.show_dialog("Login Error", "Authentication failed. Please try again.")

    # ============== UTILITY METHODS ==============
    def show_dialog(self, title, text):
        """Show dialog with title and text"""
        if self.dialog:
            self.dialog.dismiss()
        
        self.dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=self.close_dialog
                )
            ]
        )
        self.dialog.open()

    def close_dialog(self, *args):
        """Close dialog"""
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None

if __name__ == "__main__":
    HexVeda().run()