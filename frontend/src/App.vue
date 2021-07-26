<template>
    <div v-if="gotData">
        <div class="content vh-100">
            <NavBar />
            <Options @dateChanged="onDateChange" @overlayChanged="onOverlayChange" :startDate="locations[0].weather['0'].dt" :nDays="locations[0].weather.length" />
            <Map class=" item-main" :locations="locations" :viewDate="parseInt(viewDate)" :overlay="overlay" :startDate="locations[0].weather['0'].dt" />
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
                apiKey: '',
            }
        },
        methods: {
            onDateChange: function(viewDate) {
                this.viewDate = viewDate
            },
            onOverlayChange: function(overlay) {
                this.overlay = overlay
            },
            getLocationPromise: function() {
                const path = process.env.VUE_APP_BACKEND_ADDRESS
                return axios({
                        url: path,
                        method: 'get',
                        timeout: 8000
                    }).then(result => result.data)
                    .catch(err => console.error(err))
            },
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