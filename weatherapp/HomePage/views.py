from django.shortcuts import render, redirect
import requests
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import StringIO

# Create your views here.
def home(request):
    return render(request, 'home.html')

#global variables
locProvided = False
locValue = ""
current_weather_selected = True
a = '<a  href="input_loc" id="chLoc">Change Location</a>'

def input_loc(request):
    global a

    a = '''
        <form action="handle_input">
            <input type="text" placeholder="Name of City" name="city">
            <input type="submit">
        </form>
    '''
    if current_weather_selected:
        return redirect('CurrentWeather')
    return redirect('WeatherForecast')

def handle_input(request):
    global a, locProvided, locValue
    locProvided = True
    locValue = request.GET.get('city')
    a = '<a  href="input_loc" id="chLoc">Change Location</a>'
    if current_weather_selected:
        return redirect('CurrentWeather')
    return redirect('WeatherForecast')

def weather_forecast(request):
    global current_weather_selected
    current_weather_selected = False
    key = '0a63f50c04c0406cbb5194314232103'
    q = 'auto:ip'
    method = "forecast"
    days = 5

    if locProvided:
        try:
            q = locValue
            api = requests.get('http://api.weatherapi.com/v1/{}.json?key={}&q={}&days={}'.format(method, key, q, days)).text

            json_parsed = json.loads(api)

        
            city = json_parsed['location']['name']
            region = json_parsed['location']['region']
            country = json_parsed['location']['country']
        except:
            q = "auto:ip"
            api = requests.get('http://api.weatherapi.com/v1/{}.json?key={}&q={}&days={}'.format(method, key, q, days)).text

            json_parsed = json.loads(api)

        
            city = json_parsed['location']['name']
            region = json_parsed['location']['region']
            country = json_parsed['location']['country']
    else:
        api = requests.get('http://api.weatherapi.com/v1/{}.json?key={}&q={}&days={}'.format(method, key, q, days)).text

        json_parsed = json.loads(api)

        
        city = json_parsed['location']['name']
        region = json_parsed['location']['region']
        country = json_parsed['location']['country']

    
    cur_loc = city
    if region != "":
        cur_loc += (", " + region)
    if country != "":
        cur_loc += (", " + country)

    # tempeature
    maxtemp = []
    mintemp = []
    avgtemp = []
    days_y = []
    cnt = 0

    for i in json_parsed['forecast']['forecastday']:
        maxtemp.append(i['day']['maxtemp_c'])
        mintemp.append(i['day']['mintemp_c'])
        avgtemp.append(i['day']['avgtemp_c'])
        cnt += 1
        days_y.append(cnt)

    plt.clf()

    plt.plot(days_y, maxtemp)
    plt.plot(days_y, mintemp)
    plt.plot(days_y, avgtemp)

    plt.title('Temperature')
    plt.xlabel('Days')
    plt.ylabel('Celsius')
    plt.legend(['max temp', 'min temp', 'avg temp'])

    imgdata = StringIO()
    plt.savefig(imgdata, format='svg')
    imgdata.seek(0)

    graph_temp = imgdata.getvalue()

    # wind
    maxwind = []
    days_y = []
    cnt = 0

    for i in json_parsed['forecast']['forecastday']:
        maxwind.append(i['day']['maxwind_kph'])
        cnt += 1
        days_y.append(cnt)

    plt.clf()

    plt.plot(days_y, maxwind)

    plt.title('Wind Speed')
    plt.xlabel('Days')
    plt.ylabel('kmh')
    plt.legend(['max wind'])

    imgdata = StringIO()
    plt.savefig(imgdata, format='svg')
    imgdata.seek(0)

    graph_wind = imgdata.getvalue()

    # precipitation
    total_precip_mm = []
    total_precip_in = []
    days_y = []
    cnt = 0

    for i in json_parsed['forecast']['forecastday']:
        total_precip_mm.append(i['day']['totalprecip_mm'])
        total_precip_in.append(i['day']['totalprecip_in'])
        cnt += 1
        days_y.append(cnt)

    plt.clf()

    plt.plot(days_y, total_precip_mm)
    plt.plot(days_y, total_precip_in)

    plt.title('Precipitation')
    plt.xlabel('Days')
    plt.ylabel('precipitation')
    plt.legend(['total precipitation(mm)', 'total precipitation(inches)'])

    imgdata = StringIO()
    plt.savefig(imgdata, format='svg')
    imgdata.seek(0)

    graph_precip = imgdata.getvalue()

    # visibility
    avg_vis = []
    days_y = []
    cnt = 0

    for i in json_parsed['forecast']['forecastday']:
        avg_vis.append(i['day']['avgvis_km'])
        cnt += 1
        days_y.append(cnt)

    plt.clf()

    plt.plot(days_y, avg_vis)

    plt.title('Visibility')
    plt.xlabel('Days')
    plt.ylabel('km')
    plt.legend(['avg visibility'])

    imgdata = StringIO()
    plt.savefig(imgdata, format='svg')
    imgdata.seek(0)

    graph_vis = imgdata.getvalue()

    return render(request, 'weather_forecast.html', {'graph_vis':graph_vis,'graph_precip':graph_precip,'graph_wind':graph_wind,'graph_temp':graph_temp,'location':cur_loc, 'a':a})

def current_weather(request):
    global current_weather_selected
    current_weather_selected = True
    key = '0a63f50c04c0406cbb5194314232103'
    q = 'auto:ip'
    method = "current"

    if locProvided:
        try:
            q = locValue
            api = requests.get('http://api.weatherapi.com/v1/{}.json?key={}&q={}'.format(method, key, q)).text

            json_parsed = json.loads(api)

        
            city = json_parsed['location']['name']
            region = json_parsed['location']['region']
            country = json_parsed['location']['country']
        except:
            q = "auto:ip"
            api = requests.get('http://api.weatherapi.com/v1/{}.json?key={}&q={}'.format(method, key, q)).text

            json_parsed = json.loads(api)

        
            city = json_parsed['location']['name']
            region = json_parsed['location']['region']
            country = json_parsed['location']['country']
    else:
        api = requests.get('http://api.weatherapi.com/v1/{}.json?key={}&q={}'.format(method, key, q)).text

        json_parsed = json.loads(api)

        
        city = json_parsed['location']['name']
        region = json_parsed['location']['region']
        country = json_parsed['location']['country']

    
    cur_loc = city
    if region != "":
        cur_loc += (", " + region)
    if country != "":
        cur_loc += (", " + country)

    # conditions
    # condition image
    con_img = 'src="'+json_parsed['current']['condition']['icon']+'"'
    con_text = json_parsed['current']['condition']['text']

    #temprature
    temp_cel = str(json_parsed['current']['temp_c'])
    temp_fer = str(json_parsed['current']['temp_f'])
    feel = str(json_parsed['current']['feelslike_c'])+' C'

    #wind
    speed_kph = str(json_parsed['current']['wind_kph'])
    speed_mph = str(json_parsed['current']['wind_mph'])
    deg = str(json_parsed['current']['wind_degree'])
    wind_dir = str(json_parsed['current']['wind_dir'])

    #pressure
    mili = str(json_parsed['current']['pressure_mb'])
    inch = str(json_parsed['current']['pressure_in'])

    #precipitation
    mm = str(json_parsed['current']['precip_mm'])
    precip_inch = str(json_parsed['current']['precip_in'])

    #visibility
    vis_km = str(json_parsed['current']['vis_km'])
    vis_miles = str(json_parsed['current']['vis_miles'])

    return render(request, 'current_weather.html',{'vis_miles':vis_miles,'vis_km':vis_km,'precip_inch':precip_inch,'mm':mm,'inch':inch,'mili':mili,'speed_kph':speed_kph,'speed_mph':speed_mph,'deg':deg,'wind_dir':wind_dir,'feel':feel,'temp_fer':temp_fer,'temp_cel':temp_cel,'location':cur_loc, 'a':a, 'weather_image_src':con_img, 'weather_condition':con_text})