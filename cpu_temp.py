# Mar 2021 - A small GUI desktop app to show the CPU tempreature of a Raspberry PI4 - Peter Bowers

import PySimpleGUI as sg
from gpiozero import CPUTemperature
from time import sleep, strftime, time

cpu = CPUTemperature()

# my favourite theme so far
sg.theme('Kayak')

layout = [[sg.Text('CPU Temp is: '),sg.Text('', text_color= sg.BLUES[0], font=40, size=(10,1),justification='left', key='-OUT-')],
          [sg.Radio('Celsius', default=True, group_id=1, key='-CEL-'), sg.Radio('Fahrenheit', default=False, group_id=1, key='-FAH-') ],
          [sg.ProgressBar(max_value=10, bar_color='#9FB8AD', size=(250, 1), orientation='horizontal', key='-BAR-')],          
          [sg.Button('Quit', size=(20,1))]]

# element_justification='center' will center all elements horizontally in the window
window = sg.Window('PI CPU Temp', layout, size=(400, 100),no_titlebar=True, element_justification='center', grab_anywhere=True)

while True:
    # round to two decimal places
    cel_temp = round(cpu.temperature, 2)
    # convert celsius to fahrenheit
    fah_temp = round((cel_temp * 9/5) + 32, 2)

    # write the temp readings to a .csv file with date and time
    with open("/home/pi/cpu_temp1.csv", "a") as log:        
        log.write("{0},{1}\n".format(strftime("%Y-%m-%d %H:%M:%S"),str(cel_temp)))

    # update the temp display every three seconds
    event, values = window.read(timeout=5000)
    if event == 'Quit' or event == sg.WIN_CLOSED:        
        break        
    # display the temp in either Celsius or farhenheit depending on radio button chosen
    if (values['-CEL-']):
        window['-OUT-'].update(cel_temp)
        window['-BAR-'].update_bar(cel_temp)
    else:
        window['-OUT-'].update(fah_temp)  
    # close the log file
    log.close()

window.close()