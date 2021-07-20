<template>
    <div>
        <l-map style="height:100%" @ready="onReady">
            <l-tile-layer url='https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png' attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>' subdomains='abcd'>
            </l-tile-layer>
            <l-marker v-for='(location, index) in locations' :key="index" :lat-lng='location.loc'>
                <l-icon :icon-url="location.weather[viewDateIso].icon" :icon-size="iconSize" />
                <l-popup>
                    <div class="popup center">
                        <h4>{{location.name}}</h4>
                        {{location.count}} Routes
                        <br>
                        <br>
                        <div>
                            {{location.weather[viewDateIso].text}} on {{viewDate}} </div>
                        <div>
                            Humidity:{{location.weather[viewDateIso].humidity}}% </div>
                        <div>
                            Temperature: {{location.weather[viewDateIso].min_temp_c}} / {{location.weather[viewDateIso].max_temp_c}} °C
                        </div>
                        <div>
                            Rain today {{location.weather[viewDateIso].rain_perc}}% = {{location.weather[viewDateIso].totalprecip_mm}} mm
                        </div>
                        <div>
                            Rain last 2 days: {{location.weather[viewDateIso].["rain_last_2_day(mm)"]}} mm
                        </div>
                    </div>
                </l-popup>
            </l-marker>
        </l-map>
    </div>
</template>

<script>
    import "leaflet/dist/leaflet.css";
    import {
        LMap,
        LTileLayer,
        LMarker,
        LPopup,
        LIcon
    } from "@vue-leaflet/vue-leaflet";
    import dateformat from "dateformat"
    export default {
        name: "Map",
        components: {
            LMap,
            LTileLayer,
            LMarker,
            LPopup,
            LIcon
        },
        props: ['locations',
            'viewDate'
        ],
        data: function() {
            return {
                iconWidth: 64,
                iconHeight: 64,
            }
        },
        computed: {
            iconSize() {
                return [this.iconWidth, this.iconHeight];
            },
            viewDateIso() {
                var dateFormat = require("dateformat");
                var _temp = new Date(this.viewDate)
                return dateFormat(_temp, "isoDate")
            }
        },
        methods: {
            onReady: (mapObject) => {
                mapObject.locate({
                    setView: true,
                    maxZoom: 10
                })
            },
        },
    }
</script>

<style>
    .center {
        text-align: center;
    }

    .popup {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
    }
</style>