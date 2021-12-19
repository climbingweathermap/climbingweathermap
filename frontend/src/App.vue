<template>
    <div v-if="gotData">
        <div class="content vh-100">
            <NavBar />
            <Options @dateChanged="onDateChange" :startDate="locations[0].weather[0].dt" :nDays="locations[0].weather.length-1" />
            <Map class=" item-main" :locations="locations" :viewDate="parseInt(viewDate)" :startDate="locations[0].weather[0].dt" @zoomed="onZoom" />
            <Footer />
        </div>
    </div>
    <div v-else>
        <Modal title="Error" text="Weather data could not be fetched. Please try again shortly" />
    </div>
</template>

<script>
    import Modal from './components/Modal.vue'
    import NavBar from './components/NavBar.vue'
    import Footer from './components/Footer.vue'
    import Options from './components/Options.vue'
    import Map from './components/Map.vue'
    import axios from 'axios';
    export default {
        name: 'App',
        components: {
            Modal,
            NavBar,
            Footer,
            Map,
            Options
        },
        data: function() {
            return {
                locations: [],
                viewDate: '',
                overlay: '',
                gotData: false,
                drill: 0,
            }
        },
        props: {
            zoom: Number,
        },
        methods: {
            onDateChange: function(viewDate) {
                this.viewDate = viewDate
            },
            getLocationPromise: function() {
                if (process.env.NODE_ENV === "production") {
                    var path = "http://climbing-weather-map.com/api/v1/locations"
                } else {
                    var path = "http://localhost:5000/api/v1/locations"
                }
                console.log(path)
                return axios({
                        url: path,
                        method: 'get',
                        params: {
                            'drill': this.drill
                        },
                        timeout: 8000
                    }).then(result => result.data)
                    .catch(err => console.error(err))
            },
            onZoom: function(zoom) {
                var newDrill
                if (zoom < 10) {
                    newDrill = 0
                } else {
                    newDrill = 1
                }
                if (newDrill != this.drill) {
                    this.drill = newDrill
                    this.getLocationPromise().then(result => {
                        if (result) {
                            this.locations = result
                            this.gotData = true
                        }
                    })
                }
            }
        },
        mounted: function() {
            this.getLocationPromise().then(result => {
                if (result) {
                    this.locations = result
                    this.gotData = true
                }
            })
        },
    };
</script>

<style>
    @import './assets/custom.css';

    #app {
        font-family: Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }

    .content {
        display: flex;
        align-items: stretch;
        align-content: stretch;
        flex-direction: column;
        justify-content: space-evenly;
    }

    .item-main {
        flex-grow: 4;
        z-index: 1;
    }
</style>