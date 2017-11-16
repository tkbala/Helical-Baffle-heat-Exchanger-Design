from Tkinter import *
from math import *
e=[]
user_layout="90"
user_tube_length = "2.483"
user_tube_OD = "0.01588"
user_helix_angle = 20
user_helix_overlap_ratio = 0.8
no_of_baffles = 4
user_HTC_guess = 1000
user_tube_metal = 40
Kw = 40 # thermal conductivity of tube metal

#Adjustable parameters
#----------------------------
port_diameter = 0.150 # diameter of entry and exit ports of shell, close to TEMA in dia, 148 mm & 152mm out dia
ssr = 5 # Ratio of no. tubes to no. of sealins strips
pitch_ratio = 2.25#1.25 # ratio of pitch to tube outer dia
sbr = 1.05 #ratio of shell inner dia to tube bundle dia
sbfr = 5.0 #ratio of shell inner dia to baffle spacing
dido = 0.8 #di/do of tubes
btr = 10 #shell ID toBaffle thickness ratio
pdc = 2 # pressure drop coefficient at inlet and outlet nozzles
#---------------------------------------------------------------------------
Ko = 300.0 #overall average heat transfer coefficient
Ko2 = 0 # calculated Ko
Ao = 0 #average HT area

Y=[1,1,1,1,1,1,1,1,1,1,1] # correction factors
Z=[1,1,1,1,1,1,1,1] # correction factors
def atoi(a,i):
    
    try:
        n=float(a)
    except:
        n=float(i)
    return n
class side:
    Tin = -300
    Tout = -300
    Cp = -1
    Rf = 0
    dP = 0
    dP_allowable = 100
    Pr = 0
    Re = 0
    G = 0 # mass velocity = massflowrate/crossection area
    m = 0
    dT = 0
    Nu = 0
    Q = 0
    layout = 90
    he = 45
    htc = -1000
    vel = 0
    Ks = 0.6 # thermal conductivity
    length = 2483
    OD = 0
    ID = 0
    no = 0
    A = 0 # cross flow area
    a = 0.8 #helix overlap ratio
    mu = 0.000894 # viscosity
    f = 0 #darcy's friction factor
    rho = 0 #density
    def getQ(self):
        if self.Tin<-273 or self.Tout<-273:
            self.Q=0
        else:    
            self.Q=self.m*self.Cp*abs(self.Tout-self.Tin)
tube = side()
shell = side()

'''
def sizing():
    print "Hello"
'''
def get_data():
    global e
    global tube
    global shell
    global user_HTC_guess
    global Ko
    global Kw
    
    tube.Tin=atoi(e[0].get(),-300)
    tube.Tout=atoi(e[1].get(),-300)
    tube.Cp=atoi(e[2].get(),-1)
    tube.Rf=atoi(e[3].get(),0)
    tube.Pr=atoi(e[4].get(),0)
    tube.m=atoi(e[5].get(),0)
    tube.dP_allowable=atoi(e[6].get(),10000000)
    tube.mu=atoi(e[7].get(),0.000894)
    tube.Ks=atoi(e[8].get(),0.6)
    tube.rho=atoi(e[9].get(),1000)
    
    shell.Tin=atoi(e[10].get(),-300)
    shell.Tout=atoi(e[11].get(),-300)
    shell.Cp=atoi(e[12].get(),-1)
    shell.Rf=atoi(e[13].get(),0)
    shell.Pr=atoi(e[14].get(),0)
    shell.m=atoi(e[15].get(),0)
    shell.dP_allowable=atoi(e[16].get(),10000000)
    shell.mu=atoi(e[17].get(),0.000894)
    shell.Ks=atoi(e[18].get(),0.6)
    shell.rho=atoi(e[19].get(),1000)
    '''
    tube.Tin=atoi(e[0].get(),210)
    tube.Tout=atoi(e[1].get(),160)
    tube.Cp=atoi(e[2].get(),4180)
    tube.Rf=atoi(e[3].get(),0)
    tube.Pr=atoi(e[4].get(),0.964)
    tube.m=atoi(e[5].get(),7.022)
    tube.dP_allowable=atoi(e[6].get(),100)
    tube.mu=atoi(e[7].get(),0.0000156)
    tube.Ks=atoi(e[8].get(),0.0319)
    tube.rho=atoi(e[9].get(),1000)
    
    shell.Tin=atoi(e[10].get(),85)
    shell.Tout=atoi(e[11].get(),95)
    shell.Cp=atoi(e[12].get(),4180)
    shell.Rf=atoi(e[13].get(),0)
    shell.Pr=atoi(e[14].get(),1.96)
    shell.m=atoi(e[15].get(),37.012)
    shell.dP_allowable=atoi(e[16].get(),100)
    shell.mu=atoi(e[17].get(),0.000314)
    shell.Ks=atoi(e[18].get(),0.675)
    shell.rho=atoi(e[19].get(),1000)
    '''
    print "Tube params : ",tube.Tin,tube.Tout,tube.Cp,tube.Rf,tube.Pr,tube.m,tube.dP_allowable,tube.mu
    print "Shell params : ",shell.Tin,shell.Tout,shell.Cp,shell.Rf,shell.Pr,shell.m,shell.dP_allowable,shell.mu
    Ko = atoi(user_HTC_guess.get(),1000)
    Kw = atoi(user_tube_metal.get(),40)
def calc_heat_duty():
    global shell
    global tube
    shell.getQ()
    tube.getQ()
    print "Shell Q = ", shell.Q," Tube Q = ",tube.Q
    if (shell.Q == 0 ) and tube.Q != 0:
        shell.Q=tube.Q
    elif (shell.Q != 0 ) and tube.Q == 0:
        tube.Q=shell.Q
    elif (shell.Q!=0) and (tube.Q !=0) and (100*(abs(shell.Q-tube.Q))/(0.5*(shell.Q+tube.Q)))<5:
        tube.Q = max(tube.Q,shell.Q)
        shell.Q = tube.Q
    if not ((tube.Tin == -300) or (tube.Tout == -300)):
        if  (shell.Tin == -300) and shell.Tout != -300:
            if(tube.Tout>tube.Tin):
                shell.Tin = shell.Tout + (shell.Q/(shell.m*shell.Cp))
            elif(tube.Tout<tube.Tin):
                shell.Tin = shell.Tout - (shell.Q/(shell.m*shell.Cp))
            else:
                shell.Tin = shell.Tout
    if not ((shell.Tin == -300) or (shell.Tout == -300)):
        if  (tube.Tin == -300) and tube.Tout != -300:
            if(shell.Tout>shell.Tin):
                tube.Tin = tube.Tout + (tube.Q/(tube.m*tube.Cp))
            elif(shell.Tout<shell.Tin):
                tube.Tin = tube.Tout - (tube.Q/(tube.m*tube.Cp))
            else:
                tube.Tin = tube.Tout    
    #code to calc temperatures after this    
def calc_tube_layout():
    # 30 - triangular, 60 - rotated triangular, 90 - square, 45- rotated square ; 30,45,60 are staggered, 90 is inline refer pf 242 in kuppan
    #https://books.google.co.in/books?id=hmzRBQAAQBAJ&pg=PA242&lpg=PA242&dq=tube+layout+pattern&source=bl&ots=Dgkvkcblr3&sig=bT__N5NtCNPxxjmxSbqzX6mk9UU&hl=en&sa=X&ei=A_ViVcWFFNGJuATs3IPgCQ&ved=0CCQQ6AEwAQ#v=onepage&q=tube%20layout%20pattern&f=false
    global tube
    global user_layout
    tube.layout = int(user_layout.get())
    print tube.layout," <---- tube layout"
def calc_area():
    global shell
    global tube
    global Ao
    global Ko
    sdT = abs(shell.Tout-tube.Tin)
    tdT = abs(tube.Tout-shell.Tin)
    lmtd = (sdT - tdT)/log(sdT/tdT)
    Ao = shell.Q/(Ko*lmtd)
    print Ao," <-- Area required"
def calc_tube_length():
    global tube
    global user_tube_length
    global no_of_baffles
    tube.length = atoi(user_tube_length.get(),2600)#2483)
    tube.length = tube.length/1000
    shell.length = tube.length
    print tube.length, " <-- tube length"
def calc_tube_OD():
    global tube
    global user_tube_OD
    tube.OD = atoi(user_tube_OD.get(),19)#15.88)
    tube.OD = tube.OD/1000
    tube.ID = tube.OD*dido
    print tube.OD, " <-- tube OD"
    print tube.ID, " <-- tube ID"
def calc_tube_no():
    global tube
    global Ao
    tube.no = Ao/(3.14159*tube.OD*tube.length)
    print tube.no, " <-- tube No."
def calc_shell_ID():
    global shell
    global tube
    global sbr
    global pitch_ratio
    if tube.layout in {45,90}:
        C1=1.0
    else:
        C1=0.86
        
    shell.ID = sqrt(tube.no*C1*pitch_ratio*tube.OD*tube.OD/0.78)
    
    print shell.ID," <-- shell ID"
def calc_helix_angle_ratio():
    global shell
    global user_helix_angle
    global user_helix_overlap_ratio
    global no_of_baffles
    shell.he = atoi(user_helix_angle.get(),40)#,20)
    shell.a = atoi(user_helix_overlap_ratio.get(),0.8)
    if shell.a > 1 or shell.a<0:
        shell.a = 0.8
    print shell.he, " <-- shell helix angle"
    print shell.a, " <-- overlap ratio"
    print no_of_baffles, " <-- No. of baffles"
def calc_shell_velocity():
    global shell
    global tube
    global pitch_ratio
    global sbr
    global sbfr
    Pt = tube.OD*pitch_ratio
    shell.A = 0.5*((Pt-tube.OD)*shell.ID*shell.ID/sbfr)/Pt
    shell.G = shell.m/shell.A
    shell.vel = shell.G/shell.rho
    if tube.layout in {45,90}:
        de = (4*((Pt*Pt)-(3.14159*tube.OD*tube.OD/4)))/(3.14159*tube.OD)
    else:
        de = (4*(((sqrt(3)/4)*Pt*Pt)-(3.14159*tube.OD*tube.OD/8)))/(3.14159*tube.OD/2)
    shell.Re = shell.G*de/shell.mu
    print shell.Re," <-- shell Re"
    
def calc_tube_velocity():
    global tube
    tube.A = 3.14159*tube.ID*tube.ID/4
    tube.G = tube.m/(tube.no*tube.A)
    tube.vel = tube.G/tube.rho
    tube.Re = tube.G*tube.ID/tube.mu
    print tube.Re," <-- tube Re"
def calc_correction_facts():
    global Y
    global Z
    global tube
    global shell
    global ssr
    global no_of_baffles
    global btr
    global sbr
    global sbfr
    global B
    #Y2,Z2
    Y[2] = 1
    Z[2] = 1
    #Y3
    if tube.layout == 30:
        Y[3] = 1 +2/(3*(sqrt(3)/2))
    elif tube.layout == 60:
        Y[3] = 1+ (2/3)
    elif tube.layout == 45:
        Y[3] = 1 + 2/(3*sqrt(2))
    elif tube.layout == 90:
        e = 1 - (3.14159/(4))
        Y[3] = 1 + ((0.7*0.7)/(e*sqrt(e)*1.7*1.7))
    else:
        Y[3] = 1
    #Y7 & Z3
    shell.no = no_of_baffles
    B = shell.a*shell.no*shell.ID*sin(3.14159/shell.no)*tan(shell.he*3.14159/180)
    Sp = shell.ID/(1.0*btr)
    Sss = 0.5*(B -(Sp/cos(shell.he*3.14159/180)))*(shell.ID -(shell.ID/sbr) - 0.25*tube.OD)
    S2z = shell.A #verify
    y = Sss/S2z
    x = 1.25*tube.OD * (tube.no/ssr)/shell.ID
    Y[7] = exp(-1.343*x*(1-((2*y)**0.338)))
    Z[3] = exp(-3.560*x*(1-((2*y)**0.363)))
    # Y8 & Z5
    lto = shell.length - (shell.ID/sbfr) # assuming end lengths without baffle = 2*0.5* bafflespacing
    x = (shell.length -lto)/shell.length
    y = B/shell.ID
    Y[8] = (1.079*(y**0.0487) )- (0.445*(y**(-0.301))*(x**1.2))
    Z[5] = (-0.0172 + 0.0899*y)*(x**(-1.2))
    # Y[4]
    Y[4] = 1
    # Y9 & Z6
    if shell.he<=45 and shell.he >= 18:
        Y[9] = 0.977 + (0.00455*(shell.he)) - (0.0001821*(shell.he)*(shell.he))
    else:
        Y[9]=1
    Z[6] = 0.289 - (0.000506*(shell.he)) - (0.0000453*(shell.he)*(shell.he))
    #Y10 & Z7
    if shell.he<45.01 and shell.he>24.9:
        Y[10] = -56.39 + (8.28*(shell.he)) - (0.46 *(shell.he**2)) + (0.012 * (shell.he**3)) - (0.000164*(shell.he**4))
    else:
        Y[10]=1
    if shell.he<45.01 and shell.he>21.9:
        Z[7] = -5.411 + (0.379*(shell.he)) - (0.00402*(shell.he**2))
    else:
        Z[7]=1
    
    
def calc_HTC():
    global shell
    global tube
    global Y
    
    Nulam = 0.664 *(shell.Re**0.5)*(shell.Pr**0.33)
    Nuturb = (0.037*(shell.Re**0.7)*(shell.Pr))/(1+(2.433*(shell.Re**(-0.1))*((shell.Pr**0.67)-1)))
    shell.Nu = 0.62*(0.3+sqrt((Nulam**2)+(Nuturb**2)))*Y[2]*Y[3]*Y[4]*Y[7]*Y[8]*Y[9]*Y[10]
    shell.htc = (shell.Nu)*(shell.Ks)/(3.14159*tube.OD/2)
    shell.f = 1/((0.790*(log(shell.Re))-1.64)**2)
    
    tube.f = 1/((0.790*(log(tube.Re))-1.64)**2) #petukhov relation
    if tube.Re>3000:
        tube.Nu = ((tube.f/8)*(tube.Re-1000)*tube.Pr)/(1+(12.7*sqrt((tube.f/8))*((tube.Pr**(2/3))-1)))#Mills relation
    else:
        tube.Nu = 0.023*((tube.Re)**0.8)*((tube.Pr)**0.4)#dittus-beolter
    tube.htc = (tube.Nu)*(tube.Ks)/(tube.ID)
def calc_dP_shell():
    global shell
    global tube
    global no_of_baffles
    global sbr
    global sbfr
    global pitch_ratio
    global Z
    global B
    global pdc
    global port_diameter
    global nr
    global dP1
    global dP2
    global dP3
    global dP4
    global lto
    if tube.layout in {30,60}:
        nr = (int(((sqrt(3)*(shell.ID/sbr)/(2*pitch_ratio*tube.OD)) + 1)))/2
    else:
        nr = int((shell.ID/sbr)/(sqrt(2)*pitch_ratio*tube.OD))+1
    dP1 = 2*shell.f*nr*shell.rho*shell.vel*shell.vel*Z[2]*Z[6]*Z[7]
    lto = shell.length - (shell.ID/sbfr) # assuming end lengths without baffle = 2*0.5* bafflespacing
    dP2 = dP1 * lto * Z[3] / B #add
    dP3 = dP1 * Z[5] #add
    port_area = 3.14159*port_diameter*port_diameter/4.0
    port_vel = shell.m/(shell.rho*port_area)
    dP4 = pdc*0.5*shell.rho*port_vel*port_vel#add
    shell.dP = (dP2+dP3+dP4)/100000
    print shell.dP," <- Shell pressure drop in bar "
    
def calc_dP_tube():
    tube.dP = (tube.f * tube.length * tube.rho * tube.vel *tube.vel)/(tube.ID*2*100000)
    print tube.dP," <-- Tube pressure drop in bar"
def calc_overall_HTC():
    global Kw
    global tube
    global shell
    global Ko2
    Ko2 = (tube.OD/((tube.htc)*tube.ID))+((tube.OD *log(tube.OD/tube.ID))/(2*Kw))+(1/shell.htc) + shell.Rf + tube.Rf
    Ko2 = 1/Ko2
    print Ko2," <-- calculated HTC"
    print Ko," <-- assumed HTC"

    
def compute():
    global e
    global shell
    global tube
    global Ko
    global Ko2
    global ex
    get_data()
    i=0
    print "~~~~~~ iteration: ",i
# step 1 Heat duty computation
    calc_heat_duty()
#dbs    print "Shell Q = ",shell.Q," Tube Q = ",tube.Q
# step 2 determine tube layout
    calc_tube_layout()
#step 3 thermophysical props are entered by user

#step 4 - assume a overall average HTC ko = 1000 (global variable) and calculate provisional area
    calc_area()
#step 5 - fix tube length and dia -> calculate no. of tubes -> tube bundle dia -> shell ID

    calc_tube_length()
    calc_tube_OD()
    calc_tube_no()
    calc_shell_ID()
#step 6 - choose helical angle and overlap ratio of helical baffles    
    calc_helix_angle_ratio()
#step 7a - calculate shell side velocity and tube side velocity
    calc_shell_velocity()
    calc_tube_velocity()
#step 7b - calculate correction factors    
    calc_correction_facts()
#step 8a - calculate heat transfer coefficent of shell & tube
    calc_HTC()
#step 8b - calculate pressure drop
#omitted for now
#step 8c - calculate overal HTC
    calc_overall_HTC()
    calc_dP_shell()
    calc_dP_tube()
    print "percentage error in HTC = ",(Ko2-Ko)/Ko
    while abs((Ko2-Ko)/Ko)>0.15 or Ko2<Ko-0.01 :
        i=i+1
        print "~~~~~~ iteration: ",i
        Ko = (Ko+Ko2)/2.0
        calc_area()
        calc_tube_length()
        calc_tube_OD()
        calc_tube_no()
        calc_shell_ID()
        calc_helix_angle_ratio()
        calc_shell_velocity()
        calc_tube_velocity()
        calc_correction_facts()
        calc_HTC()
        calc_overall_HTC()
        calc_dP_shell()
        calc_dP_tube()
    ex.create_window()
class Example(Frame):
    counter = 0
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent        
        self.initUI()
        
    def initUI(self):
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)     
        fileMenu = Menu(menubar)       
        fileMenu.add_command(label="Sizing",underline = 0, command=self.sizing)
        fileMenu.add_command(label="Rating")
        menubar.add_cascade(label="Process", underline=0, menu=fileMenu)
    def sizing(self):
        global root
        global e
        global user_layout
        global user_tube_length
        global user_tube_OD
        global user_helix_angle
        global user_helix_overlap_ratio
        global user_HTC_guess
        global user_tube_metal
        Label(root, text="Tube side T-in").grid(row=1,column=1)
        Label(root, text="Tube side T-out").grid(row=2,column=1)
        Label(root, text="Tube side Cp").grid(row=3,column=1)
        Label(root, text="Tube fouling resistance").grid(row=4,column=1)
        Label(root, text="Tube side prandtl no. @ avg. temp").grid(row=5,column=1)
        Label(root, text="Tube side mass flow rate").grid(row=6,column=1)
        Label(root, text="Tube allow. pressure drop in bar").grid(row=7,column=1)
        Label(root, text="Tube side viscosity @ avg. temp").grid(row=8,column=1)
        Label(root, text="Tube side thermal cond. @ avg. temp").grid(row=9,column=1)
        Label(root, text="Tube side density @ avg. temp").grid(row=10,column=1)
        Label(root, text="Shell side T-in").grid(row=1,column=3)
        Label(root, text="Shell side T-out").grid(row=2,column=3)
        Label(root, text="Shell side Cp").grid(row=3,column=3)
        Label(root, text="Shell fouling resistance").grid(row=4,column=3)
        Label(root, text="Shell side prandtl no. @ avg. temp").grid(row=5,column=3)
        Label(root, text="Shell side mass flow rate").grid(row=6,column=3)
        Label(root, text="Shell allow. pressure drop in bar").grid(row=7,column=3)
        Label(root, text="Shell side viscosity @avg. temp").grid(row=8,column=3)
        Label(root, text="Shell side thermal cond. @ avg. temp").grid(row=9,column=3)
        Label(root, text="Shell side density @ avg. temp").grid(row=10,column=3)
        Label(root, text="Choose Tube pattern (Default - inline i.e 90) \n from 90 to 30, HTC and dP increases \n 30,60 are compact,used for clean fluids\n45,90 used for fouling fluids").grid(row=1,column=5)
        Label(root, text="Choose Tube Length in mm (Default - 2438 mm) \nTEMA recommends 2438,3048,3657,4978,6096mm \n Long tube require more space and maintenace").grid(row=2,column=5)
        Label(root, text="Choose Tube O.D. in mm(Default - 15.88 mm) \nTEMA recommends \n6.35,9.53,12.7,15.88,\n19.05,22.23,25.40,31.75,38.10,50.80mm\n use 6.35mm for clean fluids \n and min.19.05mm for mech. cleaning ").grid(row=3,column=5)
        Label(root, text="Helix angle (default = 20)").grid(row=4,column=5)
        Label(root, text="Helix overlap ratio (<1)(default = 0.8)").grid(row=5,column=5)
        Label(root, text="Tube metal conductivity (default = 40)").grid(row=6,column=5)
        Label(root, text="Guess of Overall HTC (default = 1000)").grid(row=7,column=5)
        user_layout = StringVar(root)
        user_layout.set("90") # initial value
        user_tube_length = StringVar(root)
        option_layout = OptionMenu(root, user_layout, "90", "60", "45", "30")
        option_layout.grid(row = 1, column = 6)
        user_tube_length = Entry(root)
        user_tube_length.grid(row = 2, column = 6)
        user_tube_OD = Entry(root)
        user_tube_OD.grid(row = 3, column = 6)
        user_helix_angle = Entry(root)
        user_helix_angle.grid(row=4, column = 6)
        user_helix_overlap_ratio = Entry(root)
        user_helix_overlap_ratio.grid(row = 5, column = 6)
        user_tube_metal  = Entry(root)
        user_tube_metal.grid(row=6,column=6)
        user_HTC_guess = Entry(root)
        user_HTC_guess.grid(row = 7, column = 6)
        for j in {1,3}:
            for i in {1,2,3,4,5,6,7,8,9,10}:
                e1=Entry(root)
                e1.grid(row=i,column=j+1)
                e.append(e1)
        B = Button(root, text ="Design Now", command = compute)
        B.grid(row=11,column=4)
        Label(root, text="Note: Enter all values in SI").grid(row=11,column=1)
        
    def create_window(self):
        global tube
        global shell
        global Ao
        global no_of_baffles
        global Ko
        global Ko2
        self.counter += 1
        t = Toplevel(self)
        t.wm_title("Design result (in SI Units) - %s" % self.counter)
        Label(t, text="Tube layout : %s" % tube.layout).grid(row=0)
        Label(t, text="Heat transfer area : %s" % Ao).grid(row=1)
        Label(t, text="Tube length : %s" % tube.length).grid(row=2)
        Label(t, text="Tube OD : %s" % tube.OD).grid(row=3)
        Label(t, text="Tube ID : %s" % tube.ID).grid(row=4)
        Label(t, text="No. of tubes : %s" % tube.no).grid(row=5)
        Label(t, text="Shell ID : %s" % shell.ID).grid(row=6)
        Label(t, text="Shell helix angle : %s" % shell.he).grid(row=7)
        Label(t, text="Shell helix overalap ratio : %s" % shell.a).grid(row=8)
        Label(t, text="No. of Baffles : %s" % no_of_baffles).grid(row=9)
        Label(t, text="Assumed HTC : %s" % Ko).grid(row=10)
        Label(t, text="Calculated HTC ID : %s" % Ko2).grid(row=11)
        Label(t, text="Shell pressure drop (in bar) : %s" % shell.dP).grid(row=12)
        Label(t, text="Tube pressure drop (in bar) : %s" % tube.dP).grid(row=13)
        
        

root = Tk()
root.wm_title("Design of Shell and Tube Heat Exchangers with Helical Baffles")
ex = Example(root)
#root.geometry("300x150+300+300")
root.mainloop()  

