echo(version=version());

for (i = [0 : 10]){
    translate([i * 15, 0, 0])
        rotate([90, 0, 0])
            linear_extrude(height = 180)
                square([0.3, height], center = true);
}
