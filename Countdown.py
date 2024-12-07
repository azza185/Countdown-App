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
        self.appContainter = None

        app.native.window_args['resizable'] = False
        app.native.start_args['debug'] = False
        app.native.settings['ALLOW_DOWNLOADS'] = True
        ui.button.default_props('rounded outline')

    def convert_current_date(self):
        '''
        This will convert the current date to a specified format,
        this will be changed in the future to actually be used properly.
        '''
        listOfTime= self.current_date.timetuple()
        # self.time = listOfTime[3],listOfTime[4],listOfTime[5]
        self.time = self.current_date.strftime('%H:%M:%S')
        self.dayOfYear = self.current_date.timetuple().tm_yday

    def clear_gui_and_add_events(self,containers):
        '''
        Testing of removing all elements and adding new ones.
        Then going back to the home page. Will be called when tab is
        switched
        '''
        # ui.clear() ## Find a way to do this
        for container in containers:
            container.clear()
        with self.appContainter:
            ui.label('Cleared')
            ui.button('Back', on_click=lambda: self.appSetup())

    def homePage(self):
        '''
        The setup for the home page. This will be the first page displayed
        and includes tabs for the user to switch between the home page, all events.
        This also includes a calendar that will display the closest event.
        '''
        tab = ui.row().style('justify-content: center; margin-top: 20px; width: 130vh;')
        textAndButtons = ui.row().style('justify-content: center; margin-top: 20px; width: 100%;')
        calendar = ui.row().style('justify-content: center; margin-top: 20px; width: 100%;')
        with tab:
                with ui.tabs().classes('w-full') as tabs:
                    one = ui.tab('Home Page')
                    two = ui.tab('All events')
                    three = ui.tab('Manage events')
                with ui.tab_panels(tabs, value=one).classes('w-full'):
                    with ui.tab_panel(one):
                        ui.label('Home Page')
                    with ui.tab_panel(two):
                        ui.label('All events')
                    with ui.tab_panel(three):
                        ui.label('Manage events')

        with textAndButtons:
            with ui.card() as a:
                ui.label('Select what type of countdown you want')
                ui.label('1. Days')
                ui.label('2. Days and actual time')
                ui.label('3. Select events from a file')
            with ui.row().style('justify-content: center; margin-top: 0px; width: 100%;'):
                ui.button('Days', on_click=lambda: ui.label('Countdown\nDays: ' + str(365 - self.dayOfYear)))
                ui.button('Days and Time', on_click=lambda: ui.label('Countdown\nDays: ' + str(365 - self.dayOfYear) + '\nTime: ' + self.time))
                ui.button('Clear', on_click=lambda: self.clear_gui_and_add_events([tab,textAndButtons,calendar]))

        # with ui.row(): # scrollable area
        #     with ui.scroll_area().classes('w-32 h-32 border'):
        #         ui.label('I scroll. ' * 20)

        ## Make this display the closest event
        with calendar:
            ui.date({'from': '2023-01-01', 'to': '2023-01-05'}).props('range')
        return [tab,textAndButtons,calendar]

    def appSetup(self):
        '''
        This will setup the app and display the home page. It is 
        within its own function as it will make it easier to switch pages
        '''
        ## This function is needed to ensure we can clear the gui and add new events
        if self.appContainter:
            self.appContainter.clear()
        self.appContainter = ui.column().style('height: 75vh; justify-content: center; align-items: center; display: flex;')
        with self.appContainter:
            container = self.homePage()


    def runApp(self):
        '''
        This will run the app and display the home page
        '''
        with ui.row().style('justify-content: center; margin-top: 20px; width: 100%;'):
            ui.label('Countdown').style('font-size: 50px;')
        self.appSetup()

        ui.run(
            title='Countdown',
            native=True, 
            window_size=(1200, 900), 
            fullscreen=False,
            reload=False,
            dark=None, # uses auto
            tailwind=False # cant use auto without disabling this
        )

def main():
    ## May remove this function later
    countdown = Countdown()
    countdown.runApp()     


if __name__ in {"__main__", "__mp_main__"}:
    main()