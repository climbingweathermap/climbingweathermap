<template>
    <div>
        <l-map style="height:100%" @ready="onReady" v-model:zoom="zoom">
            <l-tile-layer url='https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png' attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>' subdomains='abcd'>
            </l-tile-layer>
            <l-marker v-for='(location, index) in locations' :key="index" :lat-lng='location.loc' @click="togglePop(index)" :ref="(el)=>setItemRef(el,index)">
                <l-icon>
                    <Icon :location="location" :zoom="zoom" :viewDate="viewDate" :startDate="startDate" :ref="(el)=>setIconRef(el,index)" />
                </l-icon>
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
        LIcon,
    } from "@vue-leaflet/vue-leaflet";
    import dateformat from "dateformat"
    export default {
        name: "Map",
        components: {
            LMap,
            LTileLayer,
            LMarker,
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
                zoom: 2,
                itemRefs: {},
                iconRefs: {},
            }
        },
        computed: {
            iconSize() {
                return [this.iconWidth, this.iconHeight];
            },
        },
        methods: {
            onReady: (mapObject) => {
                mapObject.locate({
                    setView: true,
                    maxZoom: 15
                })
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
            togglePop: function(index) {
                this.iconRefs[index].togglePopup()
            },
            setItemRef: function(el, index) {
                if (el) {
                    this.itemRefs[index] = el
                }
            },
            setIconRef: function(el, index) {
                if (el) {
                    // Overwrite ref to be sub component
                    this.iconRefs[index] = el
                }
            },
        },
        beforeUpdate() {
            this.itemRefs = {}
            this.iconRefs = {}
        },
    };
</script>

<style>
    .center {
        text-align: center;
        align-items: center;
    }
</style>