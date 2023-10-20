echo(version=version());

use <Blackout Midnight.ttf>

itemlen = 40;
count = 11;
width = 10;
gap = 2;
fontsize=4;
for (i = [0 : (len(tags) - 1)]){
    rotate([0, 0, -90])
        translate([i * (width + gap), 0, 0])
            difference() {
                rotate([90, 0, 0])
                    linear_extrude(height = itemlen)
                        square([width, 0.2], center = true);
                translate([0, -itemlen+2, -0.2])
                    rotate([0, 0, 90])
                        linear_extrude(height = 0.4)
                            offset(delta=-0.2)
                                text(text=tags[i], font="Blackout Midnight", size=fontsize, valign="center");
            }
}

/*
// I'm not sure this is actually useful
holderthickness = 5;
translate([-width / 2, -holderthickness / 2, 0.2])
    rotate([90, 0, 90])
        linear_extrude(height = count * (width + gap) - gap)
            square([holderthickness, 0.2], center = true);
*/
