import sqlite3
import easygui

MENU_BUTTONS = ['Add', 'View', 'Search', 'Delete', 'Exit']
MENU_TITLE = "Main menu"

easygui.buttonbox("Welcome to your Movie Catalog!", title=MENU_TITLE, choices=MENU_BUTTONS)