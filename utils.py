"""
Utility functions for the JavaScript Framework Comparison App
"""

import os
import streamlit as st


def load_css(css_file_path='styles.css'):
    """
    Load CSS file and return its content as a string.
    
    Args:
        css_file_path (str): Path to the CSS file
        
    Returns:
        str: CSS content as string
    """
    try:
        # Get the directory of the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        css_path = os.path.join(current_dir, css_file_path)
        
        with open(css_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        st.error(f"CSS file not found: {css_file_path}")
        return ""
    except Exception as e:
        st.error(f"Error loading CSS file: {str(e)}")
        return ""


def apply_css(css_file_path='styles.css'):
    """
    Load and apply CSS styling to the Streamlit app.
    
    Args:
        css_file_path (str): Path to the CSS file
    """
    css_content = load_css(css_file_path)
    if css_content:
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
