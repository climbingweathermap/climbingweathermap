<template>
    <div class="mt-5 ms-5 me-5 row align-items-center">
        <div class=" col-lg">
            <Slider class="sliders me-auto" v-model="viewDate" :min="dates[0]" :max="dates[1]" :format="formatDate" :step="day" @update="dateChanged" />
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