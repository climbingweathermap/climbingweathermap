import "leaflet/dist/leaflet.css"
import $L from "leaflet";

const createMap = (divId, options) => {
    let map = $L.map(divId, options);
    this.map = map;
    return map;
};

export default { createMap };

const createTileLayer = async (map, url, options) => {
    let tileLayer = await $L.tileLayer(url, options);
    tileLayer.addTo(map);
    return tileLayer;
};
Copy code