% Utility tool for BSLI liquids test firing. Graphs all non-voltage 

clc
clear
close all

%Prompt user for file selection
[file,path] = uigetfile('*.csv');

%Form filepath for loading
datapath = strcat(path,file);

%Exit if dialogue is cancelled
if (isequal(file,0))
   exit
end

%Load data from csv file using readmatrix
dataopts = detectImportOptions(datapath);
data = readmatrix(datapath,dataopts);

%Load data headers from csv file using readmatrix
% This must be done since each column contians boh strings and doubles
headeropts = detectImportOptions(datapath,"Range","1:6");
dataheaders = readmatrix(datapath,headeropts,"OutputType","string");

%Get sizes for number of columns for loop
datasizes = size(data);

%For all non-time vars, since time is always the first column
for i = 2:datasizes(2)
    %If not voltage data
    if (dataheaders(3,i) ~= "V")
        
        figure
        plot(data(:,1),data(:,i))
        title(dataheaders(2,i) + " vs time")
        ylabel(dataheaders(3,i))
        xlabel("Seconds from Initialization")
    
    end
end

%Add any additional graphs here