# Mar 2021 - A small GUI desktop app to show the CPU temperature of a Raspberry PI4
# every three seconds and warn if overheating (>70 degrees c) - Peter Bowers

import PySimpleGUI as sg
from gpiozero import CPUTemperature

# this is needed if logging to a file (see below)
#from time import sleep, strftime, time

# get the screen width and height (The app will show in the lower right corner)
my_screen= sg.Window.get_screen_size()
screen_width = (my_screen[0])
screen_height= (my_screen[1])

cpu = CPUTemperature()

sg.theme('Kayak')

layout = [[sg.Text('Raspberry Pi CPU Temperature is: ', font=40),sg.Text('', font=40, size=(8,1), key='-OUT-')],          
          [sg.ProgressBar(100, size=(30, 20), orientation='h', key='-BAR-')], 
          [sg.Text('Temperature is normal', font=40, key='-WARN-')], 
          [sg.Radio('Celsius', default=True,  group_id=1, key='-CEL-'), sg.Radio('Fahrenheit', default=False, auto_size_text=True, group_id=1, key='-FAH-'), sg.Button('Quit', size=(10,1))]]
          
# element_justification='center' will center all elements horizontally in the window
window = sg.Window('CPU Temperature', layout, no_titlebar=True, location=(screen_width-420, screen_height-300), default_element_size=(50, 2),element_justification='center', element_padding=((10, 10), (10, 10)), grab_anywhere=True)

while True:
    # round to one decimal place
    cel_temp = round(cpu.temperature, 1)
    # convert celsius to fahrenheit
    fah_temp = round((cel_temp * 9/5) + 32, 1)  
    
    # if desired, log the temperature readings to a .csv file along with date and time
    #with open("/home/pi/apps/Projects/PySimpleGUI/Temp/cpu_temp1.csv", "a") as log:        
    #    log.write("{0},{1}\n".format(strftime("%Y-%m-%d %H:%M:%S"),str(cel_temp)))

    # update the temperature display every three seconds
    event, values = window.read(timeout=3000)
    if event == 'Quit' or event == sg.WIN_CLOSED:        
        break        
    # display the temp in either Celsius or farhenheit depending on radio button chosen
    if (values['-CEL-']):
        window['-OUT-'].update(cel_temp)
        # update the progress bar
        window['-BAR-'].update(cel_temp)
    else:
        window['-OUT-'].update(fah_temp)
        window['-BAR-'].update(cel_temp) 

    if(cel_temp > 70):
        window['-WARN-'].update('Overheating!!', text_color='#de0917', font=100)
    else:
        window['-WARN-'].update('Temperature is normal', text_color='#363030', font=50)  

    # close the log file
    #log.close()

window.close()