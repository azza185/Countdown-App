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
    ui.label('Select what type of countdown you want: \n 1. Days \n 2. Days and actual time \n 3. Select events from a file')
    ui.button('Days', on_click=lambda: ui.label('Countdown\nDays: ' + str(365 - dayOfYear)))
    ui.button('Days and Time', on_click=lambda: ui.label('Countdown\nDays: ' + str(365 - dayOfYear) + '\nTime: ' + time))
    ui.button('Events from file', on_click=lambda: clear_gui_and_add_events())
    dark = ui.dark_mode()
    dark.enable()
    # ui.label('Countdown')
    # ui.label('Time: ' + time)
    # ui.label('Day of Year: ' + str(dayOfYear))
    # ui.button('enlarge', on_click=lambda: app.native.main_window.resize(1000, 700))

    ui.run(
        title='Countdown',
        native=True, 
        window_size=(400, 300), 
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

def clear_gui_and_add_events():
    # ui.clear() ## Find a way to do this
    ui.label('Add events here')
    ui.button('Add event', on_click=lambda: ui.label('Event added'))
    ui.button('Back', on_click=main)    


if __name__ in {"__main__", "__mp_main__"}:
    main()