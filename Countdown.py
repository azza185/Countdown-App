import datetime
from nicegui import ui
from nicegui import app

## TODO: Add events from a file. Make the gui update constantly if seconds is selected.
## TODO: Make the gui look better. Add a countdown to the next event. Add a countdown to the end of the year.
## TODO: remove items if they are in the past. Add a way to add events from the gui. Add a way to add events from the command line.
## TODO: Fix how this code look cause my fucking god it look so bad.

class Countdown():
    def __init__(self):
        self.event_dates = {} # the items will be date,time etc etc
        self.current_date = datetime.datetime.now()
        self.time = None
        self.dayOfYear = None
        self.convert_current_date()

    def convert_current_date(self):
        listOfTime= self.current_date.timetuple()
        # self.time = listOfTime[3],listOfTime[4],listOfTime[5]
        self.time = self.current_date.strftime('%H:%M:%S')
        self.dayOfYear = self.current_date.timetuple().tm_yday

def main():
    countdown = Countdown()
    app.native.window_args['resizable'] = False
    app.native.start_args['debug'] = False
    app.native.settings['ALLOW_DOWNLOADS'] = True
    time = countdown.time
    dayOfYear = countdown.dayOfYear
    ui.button.default_props('rounded outline')
    with ui.column().style('height: 100vh; justify-content: center; align-items: center; display: flex;'):
        # with ui.row():
        #     ui.label('Countdown App')
        #     with ui.row().classes('w-full items-center'):
        #         result = ui.label().classes('mr-auto')
        #         with ui.button(icon='menu'):
        #             with ui.menu() as menu:
        #                 ui.menu_item('List of events', lambda: result.set_text('Selected item 1'))
        #                 ui.menu_item('Manage events', lambda: result.set_text('Selected item 2'))
        #                 ui.separator()
        #                 ui.menu_item('Close', menu.close)
        with ui.row().style('justify-content: center; margin-top: 20px; width: 130vh;'):
            with ui.tabs().classes('w-full') as tabs:
                one = ui.tab('Home Page')
                two = ui.tab('All events')
                three = ui.tab('Manage events')
            with ui.tab_panels(tabs, value=two).classes('w-full'):
                with ui.tab_panel(one):
                    ui.label('Home Page')
                with ui.tab_panel(two):
                    ui.label('All events')
                with ui.tab_panel(three):
                    ui.label('Manage events')

        with ui.row().style('justify-content: center; margin-top: 20px; width: 100%;'):
            with ui.card() as a:
                ui.label('Select what type of countdown you want')
                ui.label('1. Days')
                ui.label('2. Days and actual time')
                ui.label('3. Select events from a file')
            with ui.row().style('justify-content: center; margin-top: 0px; width: 100%;'):
                ui.button('Days', on_click=lambda: ui.label('Countdown\nDays: ' + str(365 - dayOfYear)))
                ui.button('Days and Time', on_click=lambda: ui.label('Countdown\nDays: ' + str(365 - dayOfYear) + '\nTime: ' + time))
                ui.button('Events from file', on_click=lambda: clear_gui_and_add_events())

        # with ui.row(): # scrollable area
        #     with ui.scroll_area().classes('w-32 h-32 border'):
        #         ui.label('I scroll. ' * 20)

        ## Make this display the closest event
        with ui.row().style('justify-content: center; margin-top: 20px; width: 100%;'):
            ui.date({'from': '2023-01-01', 'to': '2023-01-05'}).props('range')




    ui.run(
        title='Countdown',
        native=True, 
        window_size=(1200, 900), 
        fullscreen=False,
        reload=False,
        dark=None, # uses auto
        tailwind=False
    )
    # gui = ui # This is kinda cool icl
    # gui.label('Countdown to Christmas')
    # gui.label('Time: ' + countdown.time)
    # gui.label('Day of Year: ' + str(countdown.dayOfYear))
    # gui.run()


# Function to dynamically adjust object styles based on window size
def update_styles(window_width: int, window_height: int):
    scale_factor = min(window_width / 1920, window_height / 1080)  # Scale relative to a base size
    object_size = f"{scale_factor * 200}px"  # Example: Scale a 200px object
    ui.run_javascript(f"""
        document.getElementById("scalable-object").style.transform = "scale({scale_factor})";
        document.getElementById("scalable-object").style.width = "{object_size}";
        document.getElementById("scalable-object").style.height = "{object_size}";
    """)


def clear_gui_and_add_events():
    # ui.clear() ## Find a way to do this
    ui.label('Add events here')
    ui.button('Add event', on_click=lambda: ui.label('Event added'))
    ui.button('Back', on_click=main)    


if __name__ in {"__main__", "__mp_main__"}:
    main()