echo(version=version());

for (i = [0 : 180]){
    translate([i, 0, 0])
        rotate([90, 0, 0])
            linear_extrude(height = 180)
                square([0.5, 0.2], center = true);
}
