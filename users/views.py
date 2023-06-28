from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
import pytz
from geopy.geocoders import Nominatim
from kerykeion import KrInstance, MakeSvgInstance
from .models import Client
from collections import Counter



@login_required(login_url='login')
def HomePage(request):
    if request.method=='POST':
        input_name=request.POST.get('name')
        input_birthdate=request.POST.get('date')
        input_birthtime=request.POST.get('time')
        input_birthplace=request.POST.get('place')
        request.session['input_name'] = input_name
        request.session['input_birthdate'] = input_birthdate
        request.session['input_birthtime'] = input_birthtime
        request.session['input_birthplace'] = input_birthplace
        print("home input_birthdate", input_birthdate)
        return redirect('results')
    return render(request, 'home.html')
  
def IntroPage(request):
    button1_text = "Sign up"
    button1_url = "/signup/"
    button2_text = "Account"
    button2_url = "/account/"
    button3_text = "Discover"
    button3_url = "/discover/"
    button4_text = "Motivation"
    button4_url = "/motivation/"
    context = {
           'button1_text': button1_text,
           'button1_url' : button1_url,
           'button2_text' : button2_text,
           'button2_url' : button2_url,
           'button3_text' : button3_text,
           'button4_text' : button4_text,
           'button3_url' : button3_url,
           'button4_url' : button4_url,
        }
    return render(request, 'intro.html', context)

def DiscoverPage(request):
    button3_url ="/discover/"
    button3_text = "Discover"
    button4_text = "Motivation"
    button4_url = "/motivation/"
    button5_url = "/account/"
    button5_text = "Account"
    context = {

           'button3_text' : button3_text,
           'button4_text' : button4_text,
           'button3_url' : button3_url,
           'button4_url' : button4_url,
           'button5_url' : button5_url,
           'button5_text': button5_text

        }
    return render(request, 'discover.html', context)

def MotivationPage(request):
    
    button3_url ="/discover/"
    button3_text = "Discover"
    button4_text = "Motivation"
    button4_url = "/motivation/"
    button5_url = "/account/"
    button5_text = "Account"
    context = {
           
           'button3_text' : button3_text,
           'button4_text' : button4_text,
           'button3_url' : button3_url,
           'button4_url' : button4_url,
           'button5_url' : button5_url,
           'button5_text': button5_text
           
        }
    return render(request, 'motivation.html', context)
    

def AccountPage(request):
    button1_text = "Create an account"
    button1_url = "/signup/"
    button2_text = "Log into account"
    button2_url = "/login/"
    button3_url ="/discover/"
    button3_text = "Discover"
    button4_text = "Motivation"
    button4_url = "/motivation/"
    button5_url = "/account/"
    button5_text = "Account"
    context = {
           'button1_text': button1_text,
           'button1_url' : button1_url,
           'button2_text' : button2_text,
           'button3_text' : button3_text,
           'button4_text' : button4_text,
           'button3_url' : button3_url,
           'button2_url' : button2_url,
           'button4_url' : button4_url,
           'button5_url' : button5_url,
           'button5_text': button5_text
           
        }
    return render(request, 'account.html', context)

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        
        user_exists = User.objects.filter(username=uname).exists()
        if user_exists:
                    return redirect('login')

        if pass1==pass2:
            my_user=User.objects.create_user(uname, email, pass1)
            my_user.save()
            return redirect('login')
        else:
            messages.warning(request,"Passwords do not match")

        
        
    return render(request, 'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,"Incorrect username/password")
    button3_url ="/discover/"
    button3_text = "Discover"
    button4_text = "Motivation"
    button4_url = "/motivation/"
    button5_url = "/account/"
    button5_text = "Account"
    context = {
           
           'button3_text' : button3_text,
           'button4_text' : button4_text,
           'button3_url' : button3_url,
           'button4_url' : button4_url,
           'button5_url' : button5_url,
           'button5_text': button5_text
           
        }
    return render(request, 'login.html', context)

def LogoutPage(request):
    logout(request)
    return redirect('login')

def ResultsPage(request):
    #object_id = request.GET.get ('object_id')
    input_name = request.session.get('input_name')
    input_birthdate = request.session.get('input_birthdate')
    input_birthtime = request.session.get('input_birthtime')
    input_birthplace = request.session.get('input_birthplace')
    str_date = str(input_birthdate)
    str_time = str(input_birthtime)
    dt_date=datetime.strptime(str_date, '%d/%m/%Y')
    dt_time=datetime.strptime(str_time, '%H:%M')
    locator = Nominatim(user_agent="myGeocoder")
    location = locator.geocode(input_birthplace)
    calculations = KrInstance(input_name,dt_date.year, dt_date.month, dt_date.day,
                             dt_time.hour,dt_time.minute,input_birthplace, location.latitude, location.longitude)
    sun_sign = getattr(calculations.sun,"sign" )
    moon_sign = getattr(calculations.moon,"sign" )
    mercury_sign = getattr(calculations.mercury,"sign" )
    venus_sign = getattr(calculations.venus,"sign" )
    mars_sign = getattr(calculations.mars,"sign" )
    jupiter_sign = getattr(calculations.jupiter,"sign" )
    saturn_sign = getattr(calculations.saturn,"sign" )
    true_node = getattr(calculations.true_node, "sign")
    ascendant = getattr(calculations.first_house, "sign")
    zodiac_signs = [ascendant, sun_sign, moon_sign, mercury_sign, venus_sign, mars_sign, jupiter_sign, saturn_sign]
    most_common_sign = Counter(zodiac_signs).most_common(1)[0][0]
   

    if sun_sign == 'Ari':
        v_sun_rec = '''the Sun's natural vital force flows brightly, natural vitality is very strong in this sign, 
moving outward in sudden, sporadic bursts.
Take care of hair health, acne, toothache, headache, seizures.
A focus on managing angry outbursts should prevent accumulating of bad energy '''
    elif sun_sign == 'Tau':
        v_sun_rec = '''the vital force is steady and enhancing of vitality. 
The life force burns slowly. Fine resistance. 
Take care of not holding toxins within the body, nor supressing emotions. 
Notice tendencies of overeating of rich and sweet foods, as they might cause problems.
Taureans should take care not to get congested colon, tonsillitis, vocal chord afflictions, dental issues.'''
    elif sun_sign == 'Gem':
       v_sun_rec = '''your vital energy has a tendency to scatter. Grounding yourself by noticing your breath might help.
The nervous system is overactive in this sign and needs to be nourished. Take notice of nervous diseases, speech impediments,
learning disorders, carpal tunnel syndrome, neurological problems and accidents to the shoulders, arms and hands'''
    elif sun_sign == 'Can':
        v_sun_rec = '''your vital force is to be taken care of, you need time
 to retreat yourself and make yourself feel emotionally safe. 
Take frequent naps when needed. Take care not to get excessive about sun exposure, exercise, straining physical work. 
Take notice of eating disorders, sensitive teeth or gums, sun intolerance, weak stomach and fatigue. '''
    elif sun_sign == 'Leo':
        v_sun_rec = '''this is the Sun's home sign, giving excellent vitality. Leos have tremendous
life force. Take care of not getting dehydrated. You should take care of your back, spinal cord and heart condition.
 '''
    elif sun_sign == 'Vir':
        v_sun_rec = '''this is a wiry and yet hardy sign with great stamina. 
Nevertheless, the Virgo vital force requires careful maintenance
and great attention to the diet and digestive organs. 
Take care of not feeling too stressed, insomnia, premature gray.'''
    elif sun_sign == 'Lib':
        v_sun_rec = '''your vital force is excellent, being rarely sick. An attitude of taking it easy works for you greatly.
Take care of not ingesting too much sugar, alcohol, as the the kidneys and alkaline balance of the blood are sensitive in this sign'''
    elif sun_sign == 'Sco':
        v_sun_rec = '''your vital force is very powerful. Your toxin-eliminating system is very powerful,
so it might help balacing it out with alternative herbs ,
sweat baths. Take care and prevent possible energetic imbalance in the reproductive system'''
    elif sun_sign == 'Sag':
        v_sun_rec = '''your vital force is powerful and expressive, much energy is stored in the muscular and nervous system. 
Take fresh air frequently and exercise frequently. You should take care of your hips, spinal area. 
Take care not to deplete yourself from too much activity '''
    elif sun_sign == 'Cap':
        v_sun_rec = '''your vital force is slow burning. You may require attention to your diet and skin, have balanced meals, beware of under eating. 
Cleansing of liver and gall bladder may help, don't let poor habits accumulate. 
Take care of teeth and bone structure by getting ideal calcium consumption '''
    elif sun_sign == 'Aqu':
        v_sun_rec = '''your vital force is electric, you may have periods of great power surges followed by periods of low force. 
You should take care of over-exposion to computers and other electromagnetically toxic devices. Take care of nervous sensitvity,
prevent fatigue, computer addictions, mental extremes. '''
    elif sun_sign == 'Pis':
        v_sun_rec = '''you are recommended to have a great sleep schedule and take your time to diffuse your conciousness away from worldly stress.
The vital force is difussed, grounding into the body may help. 
Take care of sleepiness, foot problems, weak immunity and perception of reality.'''
    else:
        v_sun_rec = '''no recommendation available for this zodiac sign'''


    if moon_sign == 'Ari':
        v_moon_rec = '''Also, the vital force distributes itself in bright, enthusiastic, short-lived bursts. 
Responsiveness is immediate and feisty. The Moon Sign speeds up the vital force as shown by the Sun sign'''
    elif moon_sign == 'Tau':
        v_moon_rec = '''Also, the vital force distributes itself in a calm and steady manner, but may require stimulation to prevent stagnation . '''
    elif moon_sign == 'Gem':
       v_moon_rec = '''Also, the vital life force distributes itself in an irregular and jumpy manner, like changeable breezes. 
The flow is largely to the nervous system, mind, verbal centers and hands. '''
    elif moon_sign == 'Can':
        v_moon_rec = '''Also, the vital flow moves inward, into the emotions, womb stomach.
The flow of force appears highly reactive and receptive to incoming influences.
The emotional life, brain chemistry, hormones and general health may change abruptly in response to external conditions. 
The responsiveness is so great in this sign that the native may appear fearful or defensive. These natives need to feel safe and protected.'''
    elif moon_sign == 'Leo':
        v_moon_rec = '''Also, the vital force distributes itself with concentrated power, warmth and joy.
There can be an excess build up of heat within the system. The native may disguise their pains and/or refuse medical help '''
    elif moon_sign == 'Vir':
        v_moon_rec = '''Also, the vital force distributes itself quickly yet steadily and in a somewhat finicky manner. Never overload the digestive tract. '''
    elif moon_sign == 'Lib':
        v_moon_rec = '''
Also, the vital force "rests" in this sign, creating a pleasant and easygoing effect in these natives. 
Balance of mind, perception or hormones may be too easily upset in response to outside stimulation. '''
    elif moon_sign == 'Sco':
        v_moon_rec = '''Also, the vital force distributes itself in a concentrated and highly intense manner, 
largely flowing into the emotional and sexual systems, though not uncommonly transformed towards spiritual efforts '''
    elif moon_sign == 'Sag':
        v_moon_rec = '''The vital force distributes itself outwardly, sometimes scattering, often into mental flights of fancy, 
interests or vision. The Moon in this sign acts as a stepping up transformer to the life force. 
The effect is a restless and positive in quality. If the Sun is weak, the Sagittarian Moon native may throw out more vital force than thev have in the bank!
These natives flee under restraint or pressure. '''
    elif moon_sign == 'Cap':
        v_moon_rec = '''The vital force may become obstructed in this sign and too cold. 
Persons with this Moon position need to be extra attentive to their physical and emotional health.
The vital force expends itself conservatively, giving excellent stamina and endurance '''
    elif moon_sign == 'Aqu':
        v_moon_rec = '''The vital force distributes itself erratically in power surges and power outages. 
The life force flows readily into the mental body, enlivening the aspirations and imagination. '''
    elif moon_sign == 'Pis':
        v_moon_rec = '''The vital force is distributed in a sleepy and vague manner. 
This Moon sign appears to diffuse the vital force of the Sun's sign and slow it down.
Stimulants and exercise may be required to offset this tendency.
These natives tend to procrastinate, and when pressured, prefer to escape reality. 
They are accepting of others and sweet natured. '''
    else:
        v_moon_rec = '''No recommendation available for this zodiac sign'''

    if true_node == 'Ari':
        v_true_node_rec = '''
“When I trust myself and follow my impulses, everyone wins.”
“Before I can support others, I have to learn how to nurture myself.”
“I can help others best by truly being myself.”
 '''
    elif true_node == 'Tau':
        v_true_node_rec = '''
“To win, I need to proceed slowly and persistently, step by step.”
“When I satisfy my own needs and the expressed needs of others, I build a stable base for relationships.”
“What others think of me is none of my business.”
 '''
    elif true_node == 'Gem':
       v_true_node_rec = ''' 
“This is a people-oriented lifetime.”
“When I am willing to listen and learn about the other person, I win.”
“If I don't understand, it's okay to ask questions.”
'''
    elif true_node == 'Can':
        v_true_node_rec = '''
“When I share my feelings, I win.”
“I win when I acknowledge the capacity of others to take charge of their own lives.”
“It's okay to let my feelings show.”
 '''
    elif true_node == 'Leo':
        v_true_node_rec = '''
“The only person who can create my happiness is me.”
“When I follow the impulses of the child within, I win.”
“When I bring joy to others, I feel included.”
 '''
    elif true_node == 'Vir':
        v_true_node_rec = '''
“I'm the only person who can put this situation in order, so I might as well do it.”
“When I withdraw, I lose; when I participate in creating positive results, I win.”
“When I focus and have a plan, the whole universe opens the pathway to success.”
'''
    elif true_node == 'Lib':
        v_true_node_rec = '''
“When I focus on supporting others, I feel confident.”
“When I successfully stimulate self-confidence in others, we both win.”
“When I share with others, I have more.”
'''
    elif true_node == 'Sco':
        v_true_node_rec = '''
“Embracing change will lead to vitality.”
“When I choose energizing change, I win; when I choose the status quo, I lose.”
“As I empower others, they recognize my worth.”
 '''
    elif true_node == 'Sag':
        v_true_node_rec = '''
“When I follow my own sense of truth, I win.”
“My intuition will show me the right road, spontaneously, as events occur.” 
“When I let others be themselves, I am free.”
 '''
    elif true_node == 'Cap':
        v_true_node_rec = '''
“When I take charge, I win.”
“When I feel self-respect, I'm on the right path.” 
“I don't need to depend on anyone else to take care of me.”
 '''
    elif true_node == 'Aqu':
        v_true_node_rec = '''
“When I do what's best for everyone involved, I win.”
“Once I decide what I want, the universe will bring it to me.”
“I don't have to dominate others to feel okay about myself.”
 '''
    elif true_node == 'Pis':
        v_true_node_rec = '''
 “All is well and everything is unfolding as it should.”
 “God's spiritual government can never fall out of place.”
 “When I 'Let Go and Let God'—I win.”
 '''
    else:
        v_true_node_rec = '''No recommendation available for this zodiac sign'''

    chart = MakeSvgInstance(calculations, chart_type='Natal')
    chart.makeSVG()
    file_name1 = input_name + 'NatalChart'
    source_file_path = 'C:/Users/ovycl/' + file_name1 + '.svg'
    
    with open(source_file_path, 'r') as source_file:
        svg_content = source_file.read()
    
    
    Profile_instance=Client(name = input_name,birth_date = input_birthdate,birth_time = input_birthtime,
                                birth_place = input_birthplace,rising= ascendant, sun = sun_sign,moon = moon_sign,mercury = mercury_sign,
                                venus = venus_sign,mars = mars_sign,jupiter = jupiter_sign,saturn = saturn_sign,
                                sun_rec = v_sun_rec, moon_rec = v_moon_rec, true_node_rec = v_true_node_rec, svg_content=svg_content)
    Profile_instance.save()
    latest_client = Client.objects.latest('id')
    svg_content = latest_client.svg_content
    button2_text = "Log out"
    button2_url = "/login/"
    button3_text = "Discover"
    button3_url = "/discover/"
    button4_text = "Motivation"
    button4_url = "/motivation/"
    context = {
           'latest_client': latest_client,
           'svg_content' : svg_content,
           'button2_text' : button2_text,
           'button2_url' : button2_url,
           'button3_text' : button3_text,
           'button4_text' : button4_text,
           'button3_url' : button3_url,
           'button4_url' : button4_url,
        }
    
    return render(request, 'results.html', context)
    

def handler400(request, exception):
    return (render(request, "400.html", status=400))

def handler403(request, exception):
    return (render(request, "403.html", status=403))

def handler404(request, exception):
    return (render(request, "404.html", status=404))

def handler500(request):
    return (render(request, "500.html", status=500))
