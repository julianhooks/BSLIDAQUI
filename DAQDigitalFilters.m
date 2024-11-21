clc
clear
close all

n = 1000;

b = fir1(n,0.00000001,'low');

for i=1:(n+1)
    fprintf("%d,",b(i))
end