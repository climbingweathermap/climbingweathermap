<template>
    <l-map style="height:100%" class="center" ref="map" @ready="onReady">
        <l-tile-layer url='https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png' attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>' subdomains='abcd'>
        </l-tile-layer>
        <l-marker v-for='location in locations' v-bind:lat-lng='location.loc'>
            <l-popup class="center">
                <h4>{{location.name}}</h4>
                {{location.count}} Routes
                <br>
                {{location.weather}}
            </l-popup>
        </l-marker>
    </l-map>
</template>

<script>
    import "leaflet/dist/leaflet.css";
    import {
        LMap,
        LTileLayer,
        LMarker,
        LPopup,
    } from "@vue-leaflet/vue-leaflet";
    import axios from 'axios';
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
            }
        },
        methods: {
            getLocationPromise: function() {
                const path = 'http://localhost:5000/api/v1/locations'
                return axios({
                        url: path,
                        method: 'get',
                        timeout: 8000
                    }).then(res => res.data)
                    .catch(err => console.error(err))
            },
            onReady: (mapObject) => {
                mapObject.locate({
                    setView: true,
                    maxZoom: 10
                })
            },
        },
        mounted: function() {
            this.getLocationPromise().then(res => {
                this.locations = res
            })
        }
    }
</script>

<style>
    .center {
        margin: auto;
        text-align: center;
    }
</style>