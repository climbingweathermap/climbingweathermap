<template>
    <div class="container align-center">
        <div id="mapContainer"></div>
    </div>
</template>

<script>
    import "leaflet/dist/leaflet.css";
    import L from "leaflet";
    export default {
        name: "Map",
        data() {
            return {
                center: [44, 368, -121, 139]
            }
        },
        methods: {
            setupLeafletMap: function() {
                const mapDiv = L.map("mapContainer").setView(this.center, 13);
                L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
                    maxZoom: 17,
                    attribution: 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'
                }).addTo(mapDiv);
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
        height: 75vh;
        top: 60px;
        position: center;


    }
</style>
Once we have our imports, we wil