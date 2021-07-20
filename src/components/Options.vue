<template>
    <div class="my-options-bar">
        <Slider class="sliders-secondary date-slider" v-model="viewDate" :min="dates[0]" :max="dates[1]" :format="formatDate" :step="day" @update="dateChanged" />
        <div>
            <h3>
                test</h3>
        </div>
    </div>
</template>

<script>
    import Slider from '@vueform/slider'
    export default {
        name: "Options",
        components: {
            Slider
        },
        // 1000 = 1s
        data: function() {
            return {
                day: (1000 * 60 * 60 * 24),
                viewDate: Date.now(),
                dates: [Date.now(),
                    Date.now() + ((1000 * 60 * 60 * 24) * 4)
                ],
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
        align-items: center;
        flex-direction: row;
        flex-wrap: nowrap;
        justify-content: space-between;
        margin-top: 40px;
        margin-bottom: 10px;
        margin-right: 50px;
        margin-left: 50px;
    }

    .date-slider {
        width: 80%;
    }
</style>