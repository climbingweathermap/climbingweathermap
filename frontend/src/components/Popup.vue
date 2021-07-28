<template>
    <div class=" popup center bg-light">
        <h4>
            <a :href="location.url">{{location.name}}</a>
        </h4>
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
            Rain last 2 days: {{location.weather[viewDate].["rain_last_2_day"]}} mm
        </div>
    </div>
</template>

<script type="text/javascript">
    export default {
        name: "Map",
        props: {
            location: Array,
        },
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
    }
</style>