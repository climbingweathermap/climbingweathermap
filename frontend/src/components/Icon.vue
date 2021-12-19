<template>
    <div>
        <div class="iconBox">
            <div>
                <img :src="location.weather[viewDate].icon" height="32" />
            </div>
            <div>
                <img :src="getRainIcon(location)" height="32" />
            </div>
            <div>
                <p>{{location.weather[viewDate].temp.toFixed(1)}}C</p>
            </div>
            <div v-if="largeIcon || showPopup">
                <a v-if="location.url" :href="location.url">
                    <p>{{location.name}}</p>
                </a>
                <p v-else>{{location.name}}</p>
            </div>
        </div>
        <Wpopup v-if="showPopup" :location="location" :viewDate="viewDate" :startDate="startDate" />
    </div>
</template>

<script type="text/javascript">
    import Wpopup from './Wpopup.vue'
    export default {
        name: "Icon",
        components: {
            Wpopup,
        },
        props: {
            location: Object,
            zoom: Number,
            viewDate: Number,
            startDate: Number,
        },
        data: function() {
            return {
                showPopup: false,
            }
        },
        methods: {
            toFixed: (value, precision) => {
                var power = Math.pow(10, precision || 0);
                return String(Math.round(value * power) / power);
            },
            getRainIcon: function(location) {
                var index = location.weather[this.viewDate].rain_score
                var iconPath = this.rain_icon[index]
                return iconPath
            },
            togglePopup: function() {
                this.showPopup = !this.showPopup
            }
        },
        computed: {
            largeIcon() {
                return (this.zoom > 10)
            },
            rain_icon() {
                return [require("../assets/icons/Rain_0_64x64.png"), require("../assets/icons/Rain_1_64x64.png"), require("../assets/icons/Rain_2_64x64.png"), require("../assets/icons/Rain_3_64x64.png")]
            },
        },
    };
</script>

<style>
    .iconBox {
        display: flex;
        background: var(--bs-dark2);
        color: var(--bs-light);
        padding: 5px;
        max-height: 32px;
        overflow: hidden;
        flex-direction: row;
        justify-content: flex-start;
        align-items: center;
        border-radius: 5px;
        z-index: 4;
        margin-bottom: 2px;

    }

    .iconBox p {
        color: var(--bs-light);

        margin: 0;
        margin-left: 5px;
        max-width: 80px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap
    }

    .iconBox a {
        color: var(--bs-light);

    }
</style>