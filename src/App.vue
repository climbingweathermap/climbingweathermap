<template>
    <div class="content  vh-100">
        <NavBar class="p-2" />
        <Options class="p-2" @dateChanged="onDateChanged" />
        <Map class=" p-2 item-main" :locations="locations" :viewDate="viewDate" />
        <Footer class="p-2" />
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
            }
        },
        methods: {
            onDateChanged: function(viewDate) {
                const options = {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                };
                this.viewDate = new Date(viewDate).toLocaleDateString(undefined, options)
            },
            getLocationPromise: function() {
                const path = 'http://localhost:5000/api/v1/locations'
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
                this.locations = result
            })
        }
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
    }

    .options-bar {
        display: flex;
        align-items: flex-center;
        align-content: center;
        flex-direction: row;
        flex-wrap: nowrap;
        justify-content: space-evenly;
        margin-top: 100px;
        margin-bottom: 100px;
        margin-right: 50px;
        margin-left: 100px;
    }
</style>