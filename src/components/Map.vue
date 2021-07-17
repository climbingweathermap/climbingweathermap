<template>
    <div id="mapContainer" class="center"></div>
</template>

<script>
    import "leaflet/dist/leaflet.css";
    import L from "leaflet";
    export default {
        name: "Map",
        data: function() {
            return {}
        },
        methods: {},
        mounted: function() {
            var mymap = L.map("mapContainer").fitWorld();
            mymap.locate({
                setView: true,
                maxZoom: 10
            });
            const markerIcon = L.icon({
                iconSize: [25, 41],
                iconAnchor: [10, 41],
                popupAnchor: [2, -40],
                // specify the path here
                iconUrl: "https://unpkg.com/leaflet@1.5.1/dist/images/marker-icon.png",
                shadowUrl: "https://unpkg.com/leaflet@1.5.1/dist/images/marker-shadow.png"
            });
            L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
                subdomains: 'abcd',
                maxZoom: 19
            }).addTo(mymap);
            L.marker([44.368, -121.139], {
                icon: markerIcon
            }).addTo(mymap).bindPopup("Smith Rock");
        },
    }
</script>

<style>
    #mapContainer {
        width: 100%;
        height: 100%;
        z-index: 0;
    }

    .center {
        margin: auto;
        text-align: center;
    }
</style>