clear global;  clear all; close all; clc; 

disp('% ----------------------------------------------------------------------- %')
disp('%                                                                         %')
disp('%                              0111000                                    %')
disp('%                           100 1 100 001                                 %')
disp('%                         10    1  1  1 00                                %')
disp('%                        01  1  1  1      0                               %')
disp('%                       0 1  1  1   1  1 1 0                              %')
disp('%                       0   1   1   1  1  1 0                             %')
disp('%                       0 1     1   1  1  1 0                             %')
disp('%                       0 1  1  1   1  0  1 0                             %')
disp('%                       0 1  1  1   0  1    0                             %')
disp('%                       01 1        1  1 1 0                              %')
disp('%                        0    0  1  0 1   0                               %')
disp('%                         0         1    0                                %')
disp('%                    10010 0 1101111110111                                %')
disp('%                  10 1 1  1111111111 11 11                               %')
disp('%                 0 1 1 1 11111111101011010111                            %')
disp('%                01 11    11111111 1  1    1 110                          %')
disp('%               011    1 1 111111110011  1 1 1 110                        %')
disp('%               0   11 1 1 1 111      0  1 1 1   10                       %')
disp('%               0 1   11  1  0         1 1 1 1 1 1 0                      %')
disp('%               1  11 1 1   11          0  1 1 1 1 11                     %')
disp('%                0     1 1  0           011  1 1 1 10                     %')
disp('%                10 1   1  0             0  1 1 1  11                     %')
disp('%                 10     01               01      10                      %')
disp('%                   10001                   001 100                       %')
disp('%                                             111                         %')
disp('%                                                                         %')
disp('%             ____                   _____                                %')
disp('%            / __ \                 |  __ \                               %')
disp('%           | |  | |_ __   ___ _ __ | |__) | __ ___  _ __                 %')
disp('%           | |  | | ''_ \ / _ \ ''_ \|  ___/ ''__/ _ \| ''_ \                %')
disp('%           | |__| | |_) |  __/ | | | |   | | | (_) | |_) |               %')
disp('%            \____/| .__/ \___|_| |_|_|   |_|  \___/| .__/                %')
disp('%                  | |                              | |                   %')
disp('%                  |_|                              |_|                   %')
disp('%                                                                         %')
disp('%             An integrated rotor design and analysis tool.               %')
disp('%                                                                         %')
disp('%                                                                         %')
disp('% Copyright (C) 2011, Brenden Epps.                                       %')
disp('%                                                                         %')
disp('% This program is free software; you can redistribute it and/or modify it %')
disp('% under the terms of the GNU General Public License as published by the   %')
disp('% Free Software Foundation.                                               %')
disp('%                                                                         %')
disp('% This program is distributed in the hope that it will be useful, but     %')
disp('% WITHOUT ANY WARRANTY; without even the implied warranty of              %')
disp('% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.                    %')
disp('% See the GNU General Public License for more details.                    %')
disp('%                                                                         %')
disp('% ----------------------------------------------------------------------- %')

addpath  ./SourceCode

%run('./SourceCode/OpenPropSingle.m')

filename = 'predicted_design.csv';
%thrust,vel_ship,rpm,dia,eff,cd1,cd2,cd3,cd4,cd5,cd6,cd7,cd8,cd9,cd10
result=[];
test=0;
max_loop =100;
predicted_design= csvread(filename);
num_predicted_design=size(predicted_design,1);


if test==0 
 disp('not in test loop')
 for loop =1:max_loop
  run('./SourceCode/OpenProp_edit.m');
  sim_out=ans;
  eff=sim_out(38);
  rpm=sim_out(2);
  dia=sim_out(3);
  thrust=sim_out(4);
  ship_vel=sim_out(5);
  shape_fin=sim_out(6:15);
  
  if eff > 0.01 && eff <1 
   result=[result;sim_out];
  end
  clear global pt
  clear  global Plots PlotPanels Toggle OnDesignValues ConversionValues systemToggle;
  clear  global OpenPropDirectory SpecificationsValues DuctValues FlagValues FoilValues Filename...
           XR_in XCoD_in XCD_in VAI_in ri_in VTI_in Xt0oD_in skew0_in rake0_in...
           Meanline_cell Thickness_cell; % CavValues
 end
elseif test == 1
 for loop =1:num_predicted_design
  %disp('% In prediction loop                %')
  %disp(predicted_design(loop,:));
  run('./SourceCode/OpenProp_eval(predicted_design(loop,:)).m');
  sim_out=ans;
  eff=sim_out(1);
  result=[result;sim_out];
  clear global pt
  clear  global Plots PlotPanels Toggle OnDesignValues ConversionValues systemToggle;
  clear  global OpenPropDirectory SpecificationsValues DuctValues FlagValues FoilValues Filename...
           XR_in XCoD_in XCD_in VAI_in ri_in VTI_in Xt0oD_in skew0_in rake0_in...
           Meanline_cell Thickness_cell; % CavValues
 end

end

csvwrite("sim_data_set2.csv",result);

%}