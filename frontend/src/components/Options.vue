<template>
    <div class="my-options-bar">
        <Slider class="sliders-secondary date-slider" v-model="viewDate" :min="0" :max="nDays" :format="formatDate" @update="dateChanged" />
<Dropdown class="overlay-dropdown" title="Change Overlay" defaultOption="Summary" :options="overlays" @setSelectedOption="changeOverlay" />
    </div>
</template>

<script>
    import Slider from '@vueform/slider'
    import Dropdown from './Dropdown.vue'
    export default {
        name: "Options",
        props: {
            'startDate': Number,
            'nDays': Number
        },
        components: {
            Slider,
            Dropdown
        },
        // 1000 = 1s
        data: function() {
            return {
                day: (1000 * 3600 * 24),
                viewDate: 0,
                overlays: ["Summary", "Rain", "Temperature"]
            }
        },
        methods: {
            formatDate: function(value) {
                const options = {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                };
                var unixDate = 1000 * (this.startDate) + (value * this.day)
                return new Date(unixDate).toLocaleDateString(undefined, options)
            },
            dateChanged: function() {
                this.$emit("dateChanged", this.viewDate)
            },
            changeOverlay: function(selectedOption) {
                this.$emit("overlayChanged", selectedOption)
            }
        },
        mounted: function() {
            this.$emit("dateChanged", this.viewDate)
        },
    }
</script>

<style src="@vueform/slider/themes/default.css">
</style>

<style>
    .my-options-bar {
        display: flex;
        align-items: flex-end;
        flex-direction: row;
        flex-wrap: nowrap;
        justify-content: space-between;

    }

    .date-slider {
        flex-grow: 4;
        margin-top: 50px;
        margin-bottom: 10px;
        margin-right: 55px;
        margin-left: 55px;
    }

    .overlay-dropdown {
        margin-top: 5px;
        margin-bottom: 5px;
        margin-right: 25px;
        margin-left: 5px;
    }
</style>