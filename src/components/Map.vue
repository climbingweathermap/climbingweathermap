<template>
    <div id="mapContainer" class="center"></div>
</template>

<script>
    import "leaflet/dist/leaflet.css";
    import L from "leaflet";
    import axios from 'axios'
    export default {
        name: "Map",
        data: function() {
            return {
                locations: [],
                myMap: null,
                markerIcon: L.icon({
                    iconSize: [25, 41],
                    iconAnchor: [10, 41],
                    popupAnchor: [2, -40],
                    // specify the path here
                    iconUrl: "https://unpkg.com/leaflet@1.5.1/dist/images/marker-icon.png",
                    shadowUrl: "https://unpkg.com/leaflet@1.5.1/dist/images/marker-shadow.png"
                }),
            }
        },
        methods: {
            createMap() {
                this.myMap = L.map("mapContainer").fitWorld();
                this.myMap.locate({
                    setView: true,
                    maxZoom: 10
                });
                L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
                    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
                    subdomains: 'abcd',
                    maxZoom: 19
                }).addTo(this.myMap);
            },
            getLocationPromise: function() {
                const path = 'http://localhost:5000/api/v1/locations'
                return axios({
                        url: path,
                        method: 'get',
                        timeout: 8000
                    }).then(res => res.data)
                    .catch(err => console.error(err))
            }
        },
        mounted: function() {
            this.createMap()
            this.getLocationPromise().then(res => {
                this.location = res
                for (let i in res) {
                    //Plot markers
                    var location = res[i];
                    L.marker(location.loc, {
                        icon: this.markerIcon
                    }).addTo(this.myMap).bindPopup("<a href=" + location.url + " > " + location.name + " </a>");
                }
            })
        }
    }
</script>
<!-- 
                        
 -->

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