<template>
    <div id="mapContainer" class="center"></div>
    <!-- <h2>{{center}}</h2> -->
</template>

<script>
    import "leaflet/dist/leaflet.css";
    import L from "leaflet";
    export default {
        name: "Map",
        data: function() {
            return {
                center: [44.368, -121.139]
            }
        },
        methods: {
            setupLeafletMap: function() {
                var mymap = L.map("mapContainer").setView(this.center, 10);
                const markerIcon = L.icon({
                    iconSize: [25, 41],
                    iconAnchor: [10, 41],
                    popupAnchor: [2, -40],
                    // specify the path here
                    iconUrl: "https://unpkg.com/leaflet@1.5.1/dist/images/marker-icon.png",
                    shadowUrl: "https://unpkg.com/leaflet@1.5.1/dist/images/marker-shadow.png"
                });
                L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/terrain/{z}/{x}/{y}{r}.{ext}', {
                    attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                    subdomains: 'abcd',
                    minZoom: 0,
                    maxZoom: 18,
                    ext: 'png'
                }).addTo(mymap);
                L.marker([44.368, -121.139], {
                    icon: markerIcon
                }).addTo(mymap).bindPopup("Smith Rock");
            },
            getCurrentLocation: function(callback) {
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(function(position) {
                        var loc = [position.coords.latitude,
                            position.coords.longitude
                        ];
                        callback(loc);
                    }, err => {
                        this.$emit("LocationNotFound")
                        callback(this.center)
                    })
                } else {
                    this.$emit("LocationNotFound");
                    callback(this.center)
                }
            },
        },
        beforeMount: function() {
            let $vm = this
            this.getCurrentLocation(function(loc) {
                $vm.center = loc,
                    $vm.setupLeafletMap()
            })
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