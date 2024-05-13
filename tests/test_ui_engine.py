from unittest import TestCase

import os
import textwrap
import tkinter as tk
import tkinter.ttk as ttk
from configparser import ConfigParser
from tkinter import messagebox, font

import sv_ttk
from tktooltip import ToolTip

from src.processing import Processing
import src.action_handler
from ui_engine import UIEngine


class TestUIEngine(TestCase):

    def setUp(self):
        # Create a Tkinter root window for testing
        self.root = tk.Tk()
        script_path = os.path.dirname(__file__)
        script_dir, _ = os.path.split(script_path)
        self.config_dir = os.path.join(script_dir, "config")
        self.ui_engine = UIEngine(self.root, self.config_dir)

    def tearDown(self):
        self.root.destroy()

    def test_delete_frame(self):
        # Setup: Create a UIEngine instance with mock data
        ui_engine = self.ui_engine

        # Create some mock action frames
        ui_engine._create_new_frame()
        ui_engine._create_new_frame()
        frame1, frame2 = ui_engine.frame_order[0], ui_engine.frame_order[1]

        # Test deleting a frame that exists
        ui_engine._select_frame(frame1)
        ui_engine.delete_frame()
        # Assert that frame1 is removed from UIEngine
        self.assertNotIn(frame1, ui_engine.frame_order)
        # Assert that frame2 still exists
        self.assertIn(frame2, ui_engine.frame_order)

        # Test deleting a frame that doesn't exist (nothing selected)
        ui_engine.delete_frame()
        self.assertIn(frame2, ui_engine.frame_order)


    def test_create_new_frame(self):
        # Test that a new frame is created and added to the UI
        initial_frame_count = len(self.ui_engine.scriptFrame.winfo_children())
        self.ui_engine._create_new_frame()
        final_frame_count = len(self.ui_engine.scriptFrame.winfo_children())
        self.assertEqual(final_frame_count, initial_frame_count + 1)

        new_frame = self.ui_engine.scriptFrame.winfo_children()[-1]
        label = new_frame.children['label']
        self.assertIsInstance(label, ttk.Label)
        self.assertEqual(label['text'], "Action:")
        option_menu = new_frame.children['option_menu']
        self.assertIsInstance(option_menu, ttk.OptionMenu)

        # Test that the navigation buttons are added to the new frame
        nav_button_frame = new_frame.children['nav_button_frame']
        self.assertIsInstance(nav_button_frame, ttk.Frame)

        # Test that the event binding is correctly set up to select the frame when clicked
        self.assertEqual(new_frame, self.ui_engine.selected_frame)

        # Test that the frame is added to the frame_order list
        self.assertIn(new_frame, self.ui_engine.frame_order)

    def test_handle_action_selection(self):
        self.fail()

    def test_check_for_errors(self):
        self.fail()

    def test_create_script(self):
        self.fail()

    def test_select_frame(self):
        self.fail()
