<template>
    <div>
        <h3> {{test}}</h3>
        <l-map style="height:100%" @ready="onReady">
            <l-tile-layer url='https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png' attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>' subdomains='abcd'>
            </l-tile-layer>
            <l-marker v-for='(location, index) in locations' :key="index" v-bind:lat-lng='location.loc'>
                <h1>index</h1>
                <l-popup class="center">
                    <h4>{{location.name}}</h4>
                    {{location.count}} Routes
                    <br>
                    {{location.weather}} on {{viewDate}}
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
    } from "@vue-leaflet/vue-leaflet";
    export default {
        name: "Map",
        components: {
            LMap,
            LTileLayer,
            LMarker,
            LPopup,
        },
        data: function() {
            return {
                locations: [],
                viewDate: '',
                test: 'test'
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
</style>