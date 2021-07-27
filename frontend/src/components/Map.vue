<template>
    <div>
        <l-map style="height:100%" @ready="onReady" v-model:zoom="zoom">
            <l-tile-layer url='https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png' attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>' subdomains='abcd'>
            </l-tile-layer>
            <l-marker class="center" v-for='(location, index) in locations' :key="index" :lat-lng='location.loc'>
                <l-icon>
                    <Icon :title="location.name" :summaryIcon="location.weather[viewDate].icon" :rainIcon="getRainIcon(location)" :temp="location.weather[viewDate].temp" :zoom="zoom" />
                </l-icon>
                <l-popup>
                    <div class=" popup center bg-light">
                        <h4>
                            <a :href="location.url">{{location.name}}</a>
                        </h4>
                        <div>
                            {{location.weather[viewDate].text}} on {{formatDate(viewDate)}} </div>
                        <div>
                            Humidity:{{location.weather[viewDate].humidity}}% </div>
                        <div>
                            Temperature: {{location.weather[viewDate].min_temp}} -> {{location.weather[viewDate].max_temp}} °C
                        </div>
                        <div>
                            Rain: {{location.weather[viewDate].rain_perc}}% = {{location.weather[viewDate].rain}} mm
                        </div>
                        <div>
                            Rain last 2 days: {{location.weather[viewDate].["rain_last_2_day"]}} mm
                        </div>
                    </div>
                </l-popup>
            </l-marker>
        </l-map>
    </div>
</template>

<script>
    import "leaflet/dist/leaflet.css";
    import Icon from './Icon.vue'
    import {
        LMap,
        LTileLayer,
        LMarker,
        LPopup,
        LIcon,
    } from "@vue-leaflet/vue-leaflet";
    import dateformat from "dateformat"
    export default {
        name: "Map",
        components: {
            LMap,
            LTileLayer,
            LMarker,
            LPopup,
            LIcon,
            Icon,
        },
        props: {
            locations: Array,
            viewDate: Number,
            overlay: String,
            startDate: Number,
        },
        data: function() {
            return {
                iconWidth: 64,
                iconHeight: 64,
                layer: "temp_new",
                day: (1000 * 24 * 60 * 60),
                zoom: 6,
            }
        },
        computed: {
            iconSize() {
                return [this.iconWidth, this.iconHeight];
            },
            rain_icon() {
                return [require("../assets/icons/Rain_0_64x64.png"), require("../assets/icons/Rain_1_64x64.png"), require("../assets/icons/Rain_2_64x64.png"), require("../assets/icons/Rain_3_64x64.png")]
            },
        },
        methods: {
            onReady: (mapObject) => {
                mapObject.locate({
                    setView: true,
                    maxZoom: 15
                })
            },
            getRainIcon: function(location) {
                var index = location.weather[this.viewDate].rain_score
                var iconPath = this.rain_icon[index]
                return iconPath
            },
            formatDate: function(value) {
                const options = {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                };
                var unixDate = 1000 * (this.startDate) + (value * this.day)
                return new Date(unixDate).toLocaleDateString(undefined, options)
            },
        },
    }
</script>

<style>
    .center {
        text-align: center;
        align-items: center;
    }

    .popup {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
    }
</style>