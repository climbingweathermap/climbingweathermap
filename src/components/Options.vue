<template>
    <div class="my-options-bar">
        <Slider class="sliders-secondary date-slider" v-model="viewDate" :min="dates[0]" :max="dates[1]" :format="formatDate" :step="day" @update="dateChanged" />
        <Dropdown class="overlay-dropdown" title="Change Overlay" defaultOption="Summary" :options="overlays" @setSelectedOption="changeOverlay" />
    </div>
</template>

<script>
    import Slider from '@vueform/slider'
    import Dropdown from './Dropdown.vue'
    export default {
        name: "Options",
        components: {
            Slider,
            Dropdown
        },
        // 1000 = 1s
        data: function() {
            return {
                day: (1000 * 60 * 60 * 24),
                viewDate: Date.now(),
                dates: [Date.now(),
                    Date.now() + ((1000 * 60 * 60 * 24) * 4)
                ],
                overlays: ["Summary", "Rain", "Temperature"]
            }
        },
        methods: {
            formatDate: (value) => {
                const options = {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                };
                return new Date(value).toLocaleDateString(undefined, options)
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
        }
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
        margin-right: 50px;
        margin-left: 50px;
    }

    .overlay-dropdown {
        margin-top: 5px;
        margin-bottom: 5px;
        margin-right: 100px;
        margin-left: 5px;
    }
</style>