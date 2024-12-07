import datetime
from nicegui import ui
from nicegui import app
import csv
import numpy as np

# Set the file path to the events file if it needs changing. I was using a bash script so i had to set from root.
FILE = 'events/events.csv'
class Countdown():
    def __init__(self) -> None:
        ## I dont like the way these variables are done. I will change to a better format later.
        self.event_dates = {} 
        self.current_date = datetime.datetime.now()
        self.time = None
        self.dayOfYear = None
        self.year = None
        self.date = str(self.current_date.date()).split('-')[::-1]
        self.date = '-'.join(self.date)
        self.date = str(self.current_date.date())
        self.convert_current_date()
        self.closest_event = 1000
        self.closes_event_date = None
        self.closest_event_name = None
        self.time_unit = 'days'

        app.native.window_args['resizable'] = False
        app.native.start_args['debug'] = False
        app.native.settings['ALLOW_DOWNLOADS'] = True
        ui.button.default_props('rounded outline')

    def get_events(self) -> None:
        '''
        This will get the events from a file and convert them as a dictionary
        '''
        with open(FILE, mode='r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[1] == 'Date':
                    continue
                days = (int(row[1].split('-')[0]) - self.current_date.year) * 365
                days += int(row[-1]) - (self.dayOfYear - 1)
                if days == 0:
                    time = row[2].split(':')
                    self.event_dates[row[0]] = [row[1], row[2]]

                    current_time = (self.current_date.hour + self.current_date.minute / 60)
                    how_far_in_day = (int(time[0]) + int(time[1]) / 60) - current_time

                    if self.time_unit == 'hours' and how_far_in_day > self.closest_event:
                        continue

                    self.closest_event = how_far_in_day
                    self.closest_event_name = row[0]
                    self.closes_event_date = str(row[1])
                    self.time_unit = 'hours'

                    continue
                elif days < 0:
                    continue

                self.event_dates[row[0]] = [row[1], row[2]]
                ## No point going into this if hours has already be done
                if days < self.closest_event and days > 0 and self.time_unit == 'days':
                    self.closest_event = days
                    self.closest_event_name = row[0]
                    self.closes_event_date = str(row[1])
                    self.time_unit = 'days'

    def convert_current_date(self) -> None:
        '''
        This will convert the current date to a specified format,
        this will be changed in the future to actually be used properly.
        '''
        self.dayOfYear = self.current_date.timetuple().tm_yday
        self.time = self.current_date.strftime("%H:%M:%S")
    
    def save_event(self, name: str, date: str, time: str) -> None:
        '''
        This will save the event to a file in the correct format.

        Args:
            name (str): The name of the event inputted by the user
            date (str): The date of the event inputted by the user
            time (str): The time of the event inputted by the user
        '''
        if name in self.event_dates:
            ui.notify('Event Already Exists', type='negative')
            return
        
        date = date.split(':')[-1].strip(' ')
        day = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        start_of_year = datetime.datetime(day.year, 1, 1).date()
        day = (day - start_of_year).days
        time = time.split(':')
        time = time[-2].strip(' ') + ':' + time[-1]
        
        with open(FILE, mode='a') as f:
            writer = csv.writer(f)
            writer.writerow([name, date, time, day])
        
    
    def setUpPage(self) -> None:
        '''
        This will set up all the ui and functionallity for the app.
        This makes two rows, one for the countdown and one for the events.
        '''
        with ui.row().style('display: flex; justify-content: center; margin-top: 50px; width: 130vh;'):
            ui.label('Countdown').style('font-size: 50px;')

        textAndButtons = ui.row().style('display: flex; justify-content: space-between; margin-top: 50px; width: 130vh;')
        ui.separator()
        with ui.row().style('display: flex; justify-content: center; margin-top: 50px; width: 130vh;'):
            ui.label('Make a new event').style('font-size: 40px;')
        
        makeEvent = ui.row().style('display: flex; justify-content: space-between; margin-top: 50px; width: 130vh;')

        with textAndButtons:
            with ui.card().style('height: 45vh; width: 40vh') as a:
                # Make the closest event
                if self.time_unit == 'hours':
                    self.closest_event = np.round(self.closest_event,5)
                ui.label('Closest event').style('font-size: 40px;')
                ui.label(f'{self.closest_event_name} - {self.closest_event} {self.time_unit} away').style('font-size: 30px;')
                ui.label(f'Date: {self.event_dates[self.closest_event_name][0]}').style('font-size: 20px;')

            with ui.card().style('height: 45vh; width: 40vh;') as a:
                # Make all events display here
                with ui.list().props('dense separator'):
                    for event in self.event_dates:
                        ui.item(f'{event} - {self.event_dates[event][0]} - {self.event_dates[event][1]}').style('font-size: 20px;')
            
            ui.date({'from': str(self.date), 'to': str(self.closes_event_date)}).props('range').style('height: 45vh; width: 40vh;')
        with makeEvent:
            with ui.card() as card:
                name = ui.input('Name', value='Paul', on_change=lambda e: label.set_text(f'Name: {e.value}'))
                name.add_slot('append')
                icon = ui.icon('face')

            date = ui.date(value=self.current_date, on_change=lambda e: date.set_text(f'Date: {e.value}'))
            clock = ui.time(value='12:00', on_change=lambda e: time.set_text(f'Time: {e.value}'))
            
            with ui.card():
                with ui.column().style('width: 30vh;'):
                    date = ui.label(f'Date: {date.value.date()}')
                    time = ui.label(f'Time: {clock.value}')
                    label = ui.label(f'Name: {name.value}')
                    ui.button('Save', on_click=lambda: self.save_event(name.value, date.text, time.text))


    def runApp(self) -> None:
        '''
        This will run the app and display the home page
        '''
        self.get_events()
        self.setUpPage()

        ui.run(
            title='Countdown',
            native=True, 
            window_size=(1200, 900), 
            fullscreen=False,
            reload=False,
            dark=None, # uses auto
            tailwind=False # cant use auto without disabling this
        )     


if __name__ in {"__main__", "__mp_main__"}:
    countdown = Countdown()
    countdown.runApp()