<template>
    <div id="mapContainer" class="center"></div>
</template>

<script>
    import "leaflet/dist/leaflet.css";
    import L from "leaflet";
    export default {
        name: "Map",
        data() {
            return {
                center: [44.368, -121.139]
            }
        },
        methods: {
            setupLeafletMap: function() {
                var mymap = L.map("mapContainer").setView(this.center, 13);
                const markerIcon = L.icon({
                    iconSize: [25, 41],
                    iconAnchor: [10, 41],
                    popupAnchor: [2, -40],
                    // specify the path here
                    iconUrl: "https://unpkg.com/leaflet@1.5.1/dist/images/marker-icon.png",
                    shadowUrl: "https://unpkg.com/leaflet@1.5.1/dist/images/marker-shadow.png"
                });
                L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
                    maxZoom: 17,
                    attribution: 'Map data:&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'
                }).addTo(mymap);
                L.marker(this.center, {
                    icon: markerIcon
                }).addTo(mymap).bindPopup("<b>Hello world!</b><br />I am a popup.").openPopup();
            },
        },
        mounted() {
            this.setupLeafletMap();
        }
    };
</script>

<style>
    #mapContainer {
        width: 90%;
        height: 80vh
    }

    .center {
        margin: auto;
        text-align: center;
    }
</style>