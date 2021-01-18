sim_data_set2: Phase 1 need atleast 50,000 design points 
     collected Data:  "num_blade,density,rpm,cod1,cod2,cod3,cod4,cod5,cod6,cod7,cod8,cod9,cod10,thrust_coeff,effy "

     % --------------------------- Design parameters(fixed) ---------------------------
    Z           = 3  ;      % number of blades
   
    ITER        = 40;       % number of iterations in analysis
    Rhv         = 0.5;   	% hub vortex radius / hub radius

    TAU         = 1; %str2double(get(DuctValues(1),'string'));      % Thrust ratio
    CDd         = 0.008; %str2double(get(DuctValues(2),'string'));      % Duct section drag coefficient

    
    rho         = 1000 ;     % Sea water density [kg/m^3]
    Mp          = 20 ;	    % number of vortex panels over the radius
    Np          = 20 ;	    % Number of points over the chord [ ]

    
    
    % ----Flags fixed---------------------------------

    Propeller_flag	= 1; % get(FlagValues(1),'value');               % 0 == turbine, 1 == propeller
    Hub_flag  	    = 1 ;% get(FlagValues(3),'value');                   % 0 == no hub, 1 == hub
    Duct_flag	    = 0; % get(FlagValues(4),'value');                   % 0 == no duct, 1 == duct

    Chord_flag	    = 0 ;% get(FlagValues(5),'value');                   % ** CHORD OPTIMIZATION FLAG **

    Viscous_flag	= 1 ;% get(FlagValues(6),'value');               % 0 == viscous forces off (CD = 0), 1 == viscous forces on
    Plot_flag       = 0 ;% get(FlagValues(7),'value');               % 0 == do not display plots, 1 == display plots



    Make2Dplot_flag = 0 ;%get(FlagValues(8),'value');               % 0 == do not make a 2D plot of the results, 1 == make plot
    Make3Dplot_flag = 0 ;% get(FlagValues(8),'value');               % 0 == do not make a 3D plot of the results, 1 == make plot

    Analyze_flag	= 0 ;% get(FlagValues(9),'value');

    % Cav_flag	= get(FlagValues(10),'value');                   % 0 == do not run cavitation mapping, 1 == run cavitation mapping
    
    Meanline_index  = 1; % 1 for yes, 0 for false
    Meanline        = 'NACA a=0.8'; %      % Meanline form

    Thickness_index	= 1; %1 for yes, 0 for false
    Thickness       = 'NACA 65A010'; % char(Thickness_cell(Thickness_index));            % Thickness form

    XCD     	=  [0.0090; 0.0090; 0.0090; 0.0090; 0.0090; 0.0090; 0.0090; 0.0090; 0.0090; 0.0090] ;str2double(get(XCD_in, 'string'));            	% section drag coefficient
    XR          = [0.2000; 0.3000; 0.4000; 0.5000;  0.6000; 0.7000; 0.8000; 0.9000; 0.9500; 1.0000];   %str2double(get(XR_in,  'string'));             	% radius / propeller radius
   
    ri          =  [NaN; NaN; NaN; NaN; NaN; NaN; NaN; NaN; NaN; NaN] ; %str2double(get(ri_in, 'string'));
    VAI         = [NaN; NaN; NaN; NaN; NaN; NaN; NaN; NaN; NaN; NaN]  ;           % axial      inflow velocity / ship velocity
    VTI         = [NaN; NaN; NaN; NaN; NaN; NaN; NaN; NaN; NaN; NaN] ;       	% tangential inflow velocity / ship velocity

    ri  = ri (~isnan(ri));
    VAI = VAI(~isnan(VAI));
    VTI = VTI(~isnan(VTI));

    skew0       = [0; 0; 0; 0; 0; 0; 0; 0; 0; 0] ;        	% skew
    rake0       = [0; 0; 0; 0; 0; 0; 0; 0; 0; 0]  ;    	% rake
    Xt0oD       = [0.0329; 0.0281; 0.0239; 0.0198; 0.0160; 0.0125; 0.0091; 0.0060; 0.0045; 0] ;% max section thickness / chord
    kt=0.25;
    % --------------------------- Design parameters(Sampled) -------------------------------
    % -------------------------------------------------------------------------------------- 
  
    rpm_range = 50:6000;                                    % set rpm range(50-6000 RPM)
    N           = randsample(rpm_range,1)  ;                % propeller speed [RPM]
    D           = 0.5+5.5*rand ;	                         % set propeller diameter [m] (0.5-10 METER)
    Dhub        = 0.17*D  ;                                 % hub diameter [m]= 0.17*D
    
    thrust_range = 100:500000;                              % set required thrust range(1,00-50,0000 N)
    THRUST           = randsample(thrust_range,1)  ;         % Thrust required [Newton]
    rps=rpm/60;
    D= (THRUST/(kt*rho*(rps)^2))^0.25  ;
    Vs= 20*rand ;                                              % ship velocity range : 0-20 m/s 

    %  Blade 2D section properties ----------------------
    cod1= 0.5*rand ;cod2= 0.5*rand ;cod3= 0.5*rand ;cod4= 0.5*rand ;cod5= 0.5*rand ;cod6= 0.5*rand ;cod7= 0.5*rand ;
    cod8= 0.5*rand ;cod9= 0.5*rand ; cod10=0.001; % MAX c/d is 1/2th of diameter	 

    XCoD        = [cod1; cod2; cod3;cod4; cod5; cod6; cod7; cod8; cod9; cod10] ; % chord / diameter
    
    XCLmax      = XCoD ; %If cord optimisation is off maximum lift coefficient (for chord optimization)
