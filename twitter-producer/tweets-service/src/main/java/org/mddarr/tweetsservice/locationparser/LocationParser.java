package org.mddarr.tweetsservice.locationparser;

import java.util.ArrayList;
import java.util.List;

public class LocationParser {
    public List<Double> parseLatLngFromLocation(String location){
        List<Double> coords = new ArrayList<>();
        coords.add(-98.0);
        coords.add(35.5);
        return coords;
    }
}
