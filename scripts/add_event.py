import argparse
import csv
import datetime

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add an event to the countdown app')
    parser.add_argument('--name', type=str, help='The name of the event')
    parser.add_argument('--date', type=str, help='The date of the event')
    parser.add_argument('--time', type=str, help='The time of the event')
    args = parser.parse_args()
    
    day = datetime.datetime.strptime(args.date, '%Y-%m-%d').date()
    start_of_year = datetime.datetime(day.year, 1, 1).date()
    day = (day - start_of_year).days

    # Add the event to the file
    with open('events/events.csv', mode='a') as f:
        writer = csv.writer(f)
        writer.writerow([args.name, args.date, args.time, day])