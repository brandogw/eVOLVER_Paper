%--------FOR a single MUX/DEMUX unit--------
solenoid_number = 48;% number of solenoids in setup
control = 2.^(0:(solenoid_number-1)); % Calculate decimal number for each port

% % % % ....MANUAL INPUT BELOW FOR NOW....[WILL WORK ON A MUX ALGORITHM]


%---These matrices indicate the ON inputs for both the MUX/DEMUX---
muxmat = [
    1,3,5,7;
    1,3,5,8;
    1,3,6,7;
    1,3,6,8;
    1,4,5,7;
    1,4,5,8;
    1,4,6,7;
    1,4,6,8;
    2,3,5,7;
    2,3,5,8;
    2,3,6,7;
    2,3,6,8;
    2,4,5,7;
    2,4,5,8;
    2,4,6,7;
    2,4,6,8];

addermat = 8*ones(16,4);

demuxmat = muxmat + addermat;

%--------FINAL MATRIX FOR MUX/DEMUX UNIT--------
vialmat = [muxmat;demuxmat];

    
%---This loop calculates the decimal values (inputs) for each vial
%output---

for j = 1:16
    mux(j) = sum(control(muxmat(j,:)));
    demux(j) = sum(control(demuxmat(j,:)));
end

