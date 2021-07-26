<template>
    <div>
        <l-map style="height:100%" @ready="onReady">
            <l-tile-layer url='https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png' attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>' subdomains='abcd'>
            </l-tile-layer>
            <l-marker v-if="overlay=='Summary'" v-for='(location, index) in locations' :key="index" :lat-lng='location.loc'>
                <l-icon :icon-url="location.weather[viewDate].icon" :icon-size="iconSize" />
                <l-popup>
                    <div class="popup center">
                        <h4>
                            <a :href="location.url">{{location.name}}</a>
                        </h4>
                        <img :src="getRainIcon(location)" />
                        <br>
                        <br>
                        <div>
                            {{location.weather[viewDate].text}} on {{formatDate(viewDate)}} </div>
                        <div>
                            Humidity:{{location.weather[viewDate].humidity}}% </div>
                        <div>
                            Temperature: {{location.weather[viewDate].min_temp}} / {{location.weather[viewDate].max_temp}} °C
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
            <l-marker v-if="overlay=='Rain'" v-for='(location, index) in locations' :key=" index" :lat-lng='location.loc'>
                <l-icon :icon-size="iconSize" :icon-url="getRainIcon(location)" />
                <l-popup>
                    <div class="popup center">
                        <h4>
                            <a :href="location.url">{{location.name}}</a>
                        </h4>
                        <img :src="location.weather[viewDate].icon">
                        <br>
                        <div>
                            {{location.weather[viewDate].text}} on {{viewDate}} </div>
                        <div>
                            Humidity:{{location.weather[viewDate].humidity}}% </div>
                        <div>
                            Temperature: {{location.weather[viewDate].min_temp_c}} / {{location.weather[viewDate].max_temp_c}} °C
                        </div>
                        <div>
                            Rain: {{location.weather[viewDate].rain_perc}}% = {{location.weather[viewDate].rain_mm}} mm
                        </div>
                        <div>
                            Rain last 2 days: {{location.weather[viewDate].["rain_last_2_day(mm)"]}} mm
                        </div>
                    </div>
                </l-popup>
            </l-marker>
            <l-marker v-if="overlay=='Temperature'" v-for='(location, index) in locations' :key=" index" :lat-lng='location.loc'>
                <l-icon :icon-size="iconSize" />
                <l-popup>
                    <div class="popup center">
                        <h4>
                            <a :href="location.url">{{location.name}}</a>
                        </h4>
                        <img :src="location.weather[viewDate].icon">
                        <br>
                        <img :src="getRainIcon(location)" />
                        <br>
                        <div>
                            {{location.weather[viewDate].text}} on {{viewDate}} </div>
                        <div>
                            Humidity:{{location.weather[viewDate].humidity}}% </div>
                        <div>
                            Temperature: {{location.weather[viewDate].min_temp_c}} / {{location.weather[viewDate].max_temp_c}} °C
                        </div>
                        <div>
                            Rain: {{location.weather[viewDate].rain_perc}}% = {{location.weather[viewDate].rain_mm}} mm
                        </div>
                        <div>
                            Rain last 2 days: {{location.weather[viewDate].["rain_last_2_day(mm)"]}} mm
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
                    maxZoom: 10
                })
            },
            getRainIcon: function(location) {
                return this.rain_icon[location.weather. [this.viewDate].rain_score]
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
    }

    .popup {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
    }
</style>