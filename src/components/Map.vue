<template>
    <div>
        <l-map style="height:100%" @ready="onReady">
            <l-tile-layer url='https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png' attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>' subdomains='abcd'>
            </l-tile-layer>
            <l-marker v-for='(location, index) in locations' :key="index" :lat-lng='location.loc'>
                <l-icon :icon-url="location.weather.icon" :icon-size="iconSize" />
                <l-popup class="center">
                    <h4>{{location.name}}</h4>
                    {{location.count}} Routes
                    <br>
                    {{location.weather.text}} on {{viewDate}}
                    <br>
                    <img :src="location.weather.icon">
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
            iconUrl() {
                return `https://placekitten.com/${this.iconWidth}/${this.iconHeight}`;
            },
            iconSize() {
                return [this.iconWidth, this.iconHeight];
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
</style>