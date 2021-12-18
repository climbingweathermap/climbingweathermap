<template>
    <div class=" popup center">
        <div>
            {{location.weather[viewDate].text}} on {{formatDate(viewDate)}} </div>
        <div>
            Humidity: {{location.weather[viewDate].humidity}}% </div>
        <div>
            Temperature: {{location.weather[viewDate].min_temp}} -> {{location.weather[viewDate].max_temp}} °C
        </div>
        <div>
            Rain: {{location.weather[viewDate].rain_perc}}% = {{location.weather[viewDate].rain}} mm
        </div>
        <div>
            Rain last 2 days: {{location.weather[viewDate].rain_last_2_day}} mm
        </div>
    </div>
</template>

<script type="text/javascript">
    export default {
        name: "Wpopup",
        props: {
            location: Object,
            viewDate: Number,
            startDate: Number,
        },
        data: function() {
            return {
                day: (1000 * 24 * 60 * 60),
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
        }
    }
</script>

<style type="text/css">
    .center {
        text-align: center;
        align-items: center;
    }

    .popup {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
        background: var(--bs-dark2);
        color: var(--bs-light);
        padding: 5px;
        min-width: 200px;
        overflow: hidden;
        border-radius: 5px;
    }
</style>