# tui_helpers.py
def wait_for_enter():
    try:
        input("\nPress ENTER to return to the menu...")
    except EOFError:
        # In case stdin is not interactive
        pass
